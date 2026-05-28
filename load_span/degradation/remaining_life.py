"""Remaining service life estimation."""

import numpy as np
from typing import Dict, List, Optional


class RemainingLifeEstimator:
    """
    Remaining life estimation for degraded structural members.
    
    T_rem = (A_rem - A_crit) / (dA/dt)
    """
    
    def __init__(self):
        self.degradation_models = []
    
    def estimate_remaining_life(
        self,
        current_capacity: float,
        initial_capacity: float,
        degradation_rate: float,
        critical_fraction: float = 0.5
    ) -> float:
        """
        Estimate remaining life based on linear degradation.
        
        Args:
            current_capacity: Current load capacity (N)
            initial_capacity: Initial load capacity (N)
            degradation_rate: Annual capacity loss rate (N/year)
            critical_fraction: Fraction of initial capacity considered failure
        
        Returns:
            Remaining years until critical state
        """
        critical_capacity = initial_capacity * critical_fraction
        
        if current_capacity <= critical_capacity:
            return 0.0
        
        if degradation_rate <= 0:
            return float('inf')
        
        remaining_years = (current_capacity - critical_capacity) / degradation_rate
        
        return remaining_years
    
    def probabilistic_life_estimate(
        self,
        mean_capacity: float,
        std_capacity: float,
        degradation_rate_mean: float,
        degradation_rate_std: float,
        critical_fraction: float = 0.5,
        n_samples: int = 10000
    ) -> Dict:
        """
        Estimate remaining life with uncertainty (Monte Carlo).
        
        Returns:
            Dictionary with mean, median, and percentiles
        """
        # Sample capacity and degradation rate
        capacities = np.random.normal(mean_capacity, std_capacity, n_samples)
        rates = np.random.normal(degradation_rate_mean, degradation_rate_std, n_samples)
        rates = np.maximum(rates, 0.001)  # Ensure positive
        
        critical_capacity = mean_capacity * critical_fraction
        
        # Compute remaining life for each sample
        remaining_lives = []
        
        for cap, rate in zip(capacities, rates):
            if cap <= critical_capacity or rate <= 0:
                remaining_lives.append(0.0)
            else:
                remaining_lives.append((cap - critical_capacity) / rate)
        
        lives = np.array(remaining_lives)
        
        return {
            "mean_life": float(np.mean(lives)),
            "median_life": float(np.median(lives)),
            "std_life": float(np.std(lives)),
            "p10_life": float(np.percentile(lives, 10)),
            "p90_life": float(np.percentile(lives, 90)),
            "min_life": float(np.min(lives)),
            "max_life": float(np.max(lives))
        }
    
    def estimate_from_fatigue_only(
        self,
        current_damage: float,
        annual_damage_rate: float,
        critical_damage: float = 1.0
    ) -> float:
        """
        Estimate remaining life from fatigue damage only.
        
        T_rem = (D_crit - D_current) / (dD/dt)
        """
        if current_damage >= critical_damage:
            return 0.0
        
        if annual_damage_rate <= 0:
            return float('inf')
        
        remaining = (critical_damage - current_damage) / annual_damage_rate
        
        return remaining
    
    def combined_degradation_rate(
        self,
        fatigue_rate: float,
        corrosion_rate: float,
        interaction_factor: float = 1.2
    ) -> float:
        """
        Compute combined degradation rate from multiple mechanisms.
        
        Accounts for synergistic effects between fatigue and corrosion.
        """
        # Corrosion accelerates fatigue by reducing section
        # Fatigue accelerates corrosion by cracking protective layers
        combined = fatigue_rate + corrosion_rate
        
        # Apply interaction factor for synergistic effects
        combined *= interaction_factor
        
        return combined
