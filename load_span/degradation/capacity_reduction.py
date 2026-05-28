"""Member capacity reduction modeling."""

from typing import Dict, Tuple


class CapacityReductionModel:
    """
    Member capacity reduction due to combined degradation.
    
    R(t) = R₀ · (1 − D_corr(t) − D_fatigue(t))
    """
    
    def __init__(self):
        pass
    
    def compute_reduced_capacity(
        self,
        initial_capacity: float,
        corrosion_damage: float,
        fatigue_damage: float,
        max_reduction: float = 0.8
    ) -> float:
        """
        Compute reduced capacity after degradation.
        
        Args:
            initial_capacity: Initial member capacity (N)
            corrosion_damage: Corrosion damage index [0,1]
            fatigue_damage: Fatigue damage index [0,1]
            max_reduction: Maximum allowed reduction fraction
        
        Returns:
            Reduced capacity (N)
        """
        # Total damage (Miner sum with interaction)
        total_damage = corrosion_damage + fatigue_damage
        
        # Apply capacity reduction
        reduction_factor = 1.0 - min(total_damage, max_reduction)
        
        return initial_capacity * max(reduction_factor, 1.0 - max_reduction)
    
    def compute_capacity_evolution(
        self,
        initial_capacity: float,
        corrosion_rate: float,
        fatigue_rate: float,
        time_years: float,
        time_step: float = 1.0
    ) -> list:
        """
        Compute capacity evolution over time.
        
        Returns:
            List of (time, capacity) tuples
        """
        evolution = []
        current_time = 0.0
        
        while current_time <= time_years:
            corrosion_damage = min(1.0, corrosion_rate * current_time)
            fatigue_damage = min(1.0, fatigue_rate * current_time)
            
            capacity = self.compute_reduced_capacity(
                initial_capacity, corrosion_damage, fatigue_damage
            )
            
            evolution.append((current_time, capacity))
            current_time += time_step
        
        return evolution
    
    def compute_safety_margin(
        self,
        current_capacity: float,
        applied_load: float,
        required_safety_factor: float = 1.5
    ) -> Tuple[float, bool]:
        """
        Compute current safety margin.
        
        Returns:
            (margin, is_safe) where margin = capacity / (load × safety_factor)
        """
        required = applied_load * required_safety_factor
        
        if required <= 0:
            return float('inf'), True
        
        margin = current_capacity / required
        
        return margin, margin >= 1.0
    
    def get_degradation_state(
        self,
        initial_capacity: float,
        current_capacity: float
    ) -> str:
        """Classify degradation state based on capacity loss."""
        loss_fraction = 1.0 - current_capacity / initial_capacity
        
        if loss_fraction < 0.05:
            return "NEGLIGIBLE_DEGRADATION"
        elif loss_fraction < 0.15:
            return "LIGHT_DEGRADATION"
        elif loss_fraction < 0.30:
            return "MODERATE_DEGRADATION"
        elif loss_fraction < 0.50:
            return "SEVERE_DEGRADATION"
        else:
            return "CRITICAL_DEGRADATION"
