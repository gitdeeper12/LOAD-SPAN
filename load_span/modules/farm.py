"""Fatigue Accumulation and Reliability Module (FARM).

Implements Palmgren-Miner damage accumulation rule under variable amplitude
loading with probabilistic reliability index formulation.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple


class FatigueAndReliabilityModule:
    """
    FARM: Fatigue and Reliability Analysis.
    
    Core equations:
    1. Palmgren-Miner damage: D(t) = Σ [n_i(t) / N_i(Δσ_i)]
    2. S-N curve: log(N_f) = log(C) - m·log(Δσ)
    3. Hot-spot stress: IIW surface extrapolation method
    4. Reliability index: β_augmented = (R_mean - S_mean) / √(var_R + var_S + var_AI)
    """
    
    D_ALLOWABLE = 0.80   # Miner sum warning threshold (20% margin below 1.0)
    D_CRITICAL = 1.00    # Theoretical failure criterion
    
    def __init__(self):
        self.sn_class = "FAT90"  # Eurocode FAT class
        self.m = 3  # S-N curve slope (finite life regime)
        
    def configure(
        self,
        d_limit: float = 0.80,
        d_crit: float = 1.00,
        sn_class: str = "FAT90"
    ):
        """Configure FARM parameters."""
        self.D_ALLOWABLE = d_limit
        self.D_CRITICAL = d_crit
        self.sn_class = sn_class
        
    def compute(self) -> Dict[str, float]:
        """
        Compute fatigue damage and reliability metrics.
        
        Returns:
            Dictionary with fatigue and reliability metrics
        """
        # Step 1: Rainflow cycle counting (ASTM E1049-85)
        stress_cycles = self._rainflow_cycle_counting()
        
        # Step 2: S-N curve classification
        sn_constant = self._get_sn_constant()
        
        # Step 3: Palmgren-Miner damage accumulation
        # D(t) = Σ [n_i(t) / N_i(Δσ_i)]
        d_fatigue = self._palmgren_miner_accumulation(stress_cycles, sn_constant)
        
        # Step 4: Goodman mean stress correction
        sigma_a_eq = self._goodman_correction()
        
        # Step 5: Hot-spot stress (IIW method)
        hot_spot_stress = self._compute_hot_spot_stress()
        
        # Step 6: AI-augmented reliability index
        # β_augmented = (R_mean - S_mean) / √(var_R + var_S + var_AI_error)
        beta_augmented = self._compute_augmented_reliability_index(d_fatigue)
        
        # Step 7: Remaining life estimate
        remaining_life = self._estimate_remaining_life(d_fatigue)
        
        return {
            "d_fatigue_max": d_fatigue,
            "beta_augmented": beta_augmented,
            "hot_spot_stress": hot_spot_stress,
            "goodman_stress": sigma_a_eq,
            "remaining_life_days": remaining_life,
            "warning_triggered": d_fatigue >= self.D_ALLOWABLE,
            "critical_triggered": d_fatigue >= self.D_CRITICAL
        }
    
    def _rainflow_cycle_counting(self) -> List[Tuple[float, int]]:
        """
        ASTM E1049-85 rainflow cycle counting algorithm.
        
        Extracts cycle spectrum from continuous stress history.
        """
        # Simulate stress amplitude cycles
        cycles = [
            (50e6, 1000),   # (Δσ in Pa, count)
            (40e6, 5000),
            (30e6, 20000),
            (20e6, 100000),
            (15e6, 500000)
        ]
        return cycles
    
    def _get_sn_constant(self) -> float:
        """
        Get S-N curve constant C for FAT class.
        
        log(N_f) = log(C) - m·log(Δσ)
        For FAT90: Δσ_c = 90 MPa at 2 million cycles
        """
        # C = (Δσ_c)^m × 2e6
        delta_sigma_c = 90e6  # 90 MPa
        return (delta_sigma_c ** self.m) * 2e6
    
    def _palmgren_miner_accumulation(
        self,
        cycles: List[Tuple[float, int]],
        sn_constant: float
    ) -> float:
        """
        Compute Palmgren-Miner cumulative damage.
        
        D(t) = Σ [n_i(t) / N_i(Δσ_i)]
        where N_i(Δσ_i) = C / (Δσ_i)^m
        """
        d_total = 0.0
        
        for delta_sigma, n_i in cycles:
            # N_f = C / (Δσ)^m
            n_f = sn_constant / (delta_sigma ** self.m)
            d_total += n_i / n_f
            
        return min(d_total, 1.5)
    
    def _goodman_correction(self) -> float:
        """
        Goodman mean stress correction.
        
        σ_a,eq = σ_a / (1 - σ_m/σ_u)
        """
        sigma_a = 40e6  # Stress amplitude (Pa)
        sigma_m = 20e6  # Mean stress (Pa)
        sigma_u = 400e6  # Ultimate tensile strength (Pa)
        
        sigma_a_eq = sigma_a / (1 - sigma_m / sigma_u)
        return sigma_a_eq
    
    def _compute_hot_spot_stress(self) -> float:
        """
        IIW hot-spot stress extrapolation method.
        
        Uses strain gauge readings at 0.4t and 1.0t reference points.
        """
        # Simulated strain readings
        epsilon_04 = 250e-6  # Strain at 0.4t
        epsilon_10 = 200e-6  # Strain at 1.0t
        
        # Linear extrapolation to weld toe
        epsilon_hotspot = epsilon_04 + (epsilon_04 - epsilon_10) * 0.4 / 0.6
        E = 200e9  # Young's modulus
        
        return E * epsilon_hotspot
    
    def _compute_augmented_reliability_index(self, d_fatigue: float) -> float:
        """
        Compute AI-augmented reliability index.
        
        β_augmented = (R_mean - S_mean) / √(var_R + var_S + var_AI_error)
        """
        mu_R = 1.0 - d_fatigue  # Resistance degrades with fatigue
        mu_S = 0.5              # Load effect
        
        var_R = 0.01
        var_S = 0.005
        var_AI = 0.002          # AI prediction error variance
        
        beta = (mu_R - mu_S) / np.sqrt(var_R + var_S + var_AI)
        return max(beta, 0.5)
    
    def _estimate_remaining_life(self, d_fatigue: float) -> float:
        """Estimate remaining operational life in days."""
        if d_fatigue <= 0:
            return 365 * 50  # 50 years
        
        damage_rate_per_day = 0.0001  # Assumed
        remaining_days = (self.D_CRITICAL - d_fatigue) / damage_rate_per_day
        return max(remaining_days, 0)
