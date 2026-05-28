"""Physical bounds enforcement on AI outputs."""

from typing import Dict, Any, Tuple


class PhysicsConstraints:
    """
    Enforce physical constraints on AI-generated predictions.
    
    Ensures AI outputs do not violate:
    - Mechanical equilibrium
    - Thermodynamic constraints
    - Established material behavior models
    """
    
    # Maximum allowed AI correction (5% of primary mechanics)
    MAX_AI_CORRECTION = 0.05
    
    # Physical bounds
    BOUNDS = {
        "stress": (0.0, 500e6),      # 0 to 500 MPa
        "strain": (-0.01, 0.01),      # ±1% strain
        "stiffness_degradation": (0.0, 0.30),  # Max 30% degradation
        "fatigue_damage": (0.0, 1.5),  # Miner sum bounds
        "reliability_index": (0.0, 8.0),  # β bounds
        "buckling_factor": (0.0, 5.0),   # λ_cr bounds
        "anomaly_index": (0.0, 2.0),     # A_index bounds
    }
    
    @classmethod
    def enforce_bounds(
        cls,
        value: float,
        quantity: str,
        default: float = 0.0
    ) -> float:
        """
        Enforce physical bounds on a quantity.
        
        Args:
            value: AI-predicted value
            quantity: Name of quantity (e.g., "stress", "strain")
            default: Default value if bound violation
        
        Returns:
            Bounded value
        """
        if quantity not in cls.BOUNDS:
            return value
        
        lower, upper = cls.BOUNDS[quantity]
        
        if value < lower or value > upper:
            # Flag violation and return bounded value
            bounded = max(lower, min(value, upper))
            return bounded
        
        return value
    
    @classmethod
    def enforce_ai_correction_bound(
        cls,
        mechanics_value: float,
        ai_correction: float
    ) -> float:
        """
        Enforce bound on AI correction term.
        
        ε_AI(t) ≤ 0.05·ΔR_max
        """
        max_correction = cls.MAX_AI_CORRECTION * abs(mechanics_value)
        
        if abs(ai_correction) > max_correction:
            # Clip correction to bound
            return max_correction * (1 if ai_correction > 0 else -1)
        
        return ai_correction
    
    @classmethod
    def validate_prediction(
        cls,
        prediction: float,
        quantity: str,
        mechanics_value: float
    ) -> Tuple[float, bool, str]:
        """
        Validate AI prediction against physics.
        
        Returns:
            (validated_value, is_valid, warning_message)
        """
        # Apply bounds
        bounded = cls.enforce_bounds(prediction, quantity, mechanics_value)
        
        # Check against mechanics value if available
        if mechanics_value is not None:
            deviation = abs(bounded - mechanics_value) / max(abs(mechanics_value), 1e-6)
            
            if deviation > 0.20:  # More than 20% deviation
                warning = f"Large deviation ({deviation:.1%}) from mechanics. Using mechanics value."
                return mechanics_value, False, warning
        
        if bounded != prediction:
            warning = f"Value {prediction:.3e} out of bounds. Clipped to {bounded:.3e}."
            return bounded, False, warning
        
        return bounded, True, ""
    
    @classmethod
    def enforce_conservatism(cls, value: float, quantity: str) -> float:
        """
        Apply conservative adjustment for safety-critical quantities.
        
        For safety, when uncertain, bias toward conservative side.
        """
        conservative_map = {
            "fatigue_damage": 1.1,   # Increase damage by 10%
            "reliability_index": 0.9,  # Decrease reliability by 10%
            "buckling_factor": 0.95,   # Decrease buckling capacity by 5%
        }
        
        if quantity in conservative_map:
            return value * conservative_map[quantity]
        
        return value
