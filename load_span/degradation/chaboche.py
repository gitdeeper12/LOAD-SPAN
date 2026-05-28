"""Chaboche continuum damage mechanics model."""

import numpy as np


class ChabocheDamageModel:
    """
    Chaboche nonlinear damage accumulation model.
    
    Accounts for load sequence effects in fatigue.
    """
    
    def __init__(self, alpha: float = 0.5, beta: float = 1.0):
        self.alpha = alpha
        self.beta = beta
    
    def compute_damage_increment(
        self,
        current_damage: float,
        stress_range: float,
        cycles: int
    ) -> float:
        """Compute damage increment using Chaboche rule."""
        # D = D_current + (1 - D_current)^α * (Δσ)^β * Δn
        increment = (1 - current_damage) ** self.alpha * stress_range ** self.beta * cycles
        return min(increment, 1.0 - current_damage)
    
    def predict_failure(self, damage_sequence: np.ndarray) -> float:
        """Predict remaining cycles to failure."""
        if len(damage_sequence) < 2:
            return float('inf')
        
        # Extrapolate to D = 1.0
        rates = np.diff(damage_sequence)
        avg_rate = np.mean(rates)
        
        if avg_rate <= 0:
            return float('inf')
        
        remaining = (1.0 - damage_sequence[-1]) / avg_rate
        return max(0.0, remaining)
