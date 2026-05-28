"""Vibrating-wire strain gauge data processing."""

import numpy as np
from typing import Dict, List, Optional


class StrainGaugeParser:
    """
    Parse and process vibrating-wire strain gauge data.
    
    Typical applications:
    - Fatigue-critical connection monitoring
    - Hot-spot stress measurement
    - Long-term drift monitoring
    """
    
    YOUNG_MODULUS = 200e9  # E for steel (Pa)
    
    def __init__(self, gauge_factor: float = 1.0, temperature_compensated: bool = True):
        self.gauge_factor = gauge_factor
        self.temperature_compensated = temperature_compensated
    
    def parse_raw_data(self, raw_data: np.ndarray) -> Dict:
        """
        Parse raw strain gauge data.
        
        Args:
            raw_data: Strain readings (microstrain or strain)
        
        Returns:
            Dictionary with processed strains
        """
        # Convert microstrain to strain if needed
        if np.max(np.abs(raw_data)) > 0.01:  # Likely in microstrain
            strain = raw_data * 1e-6
        else:
            strain = raw_data
        
        return {
            "strain": strain,
            "stress": strain * self.YOUNG_MODULUS,
            "time": np.arange(len(strain)),
            "mean_strain": float(np.mean(strain)),
            "max_strain": float(np.max(strain)),
            "min_strain": float(np.min(strain)),
            "strain_range": float(np.ptp(strain))
        }
    
    def compute_hot_spot_stress(
        self,
        strain_at_04t: float,
        strain_at_10t: float,
        t_thickness: float
    ) -> float:
        """
        Compute hot-spot stress using IIW surface extrapolation method.
        
        Uses strain gauge readings at 0.4t and 1.0t from weld toe.
        
        ε_hotspot = ε_0.4t + (ε_0.4t - ε_1.0t) × (0.4/0.6)
        """
        epsilon_04 = strain_at_04t
        epsilon_10 = strain_at_10t
        
        # Linear extrapolation to weld toe
        epsilon_hotspot = epsilon_04 + (epsilon_04 - epsilon_10) * 0.4 / 0.6
        
        # Convert to stress
        stress_hotspot = epsilon_hotspot * self.YOUNG_MODULUS
        
        return stress_hotspot
    
    def compute_stress_range_spectrum(
        self,
        strain_history: np.ndarray,
        n_bins: int = 20
    ) -> Dict:
        """
        Compute stress range spectrum for fatigue analysis.
        
        Returns histogram of stress ranges.
        """
        stress_history = strain_history * self.YOUNG_MODULUS
        stress_range = np.abs(np.diff(stress_history))
        
        hist, bin_edges = np.histogram(stress_range, bins=n_bins)
        
        return {
            "histogram": hist.tolist(),
            "bin_edges": bin_edges.tolist(),
            "mean_range": float(np.mean(stress_range)),
            "max_range": float(np.max(stress_range))
        }
    
    def detect_zero_crossings(self, strain: np.ndarray) -> int:
        """Count zero crossings for cycle counting."""
        zero_crossings = np.where(np.diff(np.signbit(strain)))[0]
        return len(zero_crossings)
    
    def apply_temperature_correction(
        self,
        strain: np.ndarray,
        temperature_change: float,
        thermal_expansion: float = 12e-6
    ) -> np.ndarray:
        """
        Apply temperature correction to strain readings.
        
        ε_corrected = ε_measured - α·ΔT
        """
        if not self.temperature_compensated:
            thermal_strain = thermal_expansion * temperature_change
            return strain - thermal_strain
        
        return strain
