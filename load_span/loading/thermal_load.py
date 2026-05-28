"""Thermal expansion and restraint force models."""

import numpy as np


class ThermalLoadModel:
    """Thermal load modeling for long-span structures."""
    
    def __init__(self, thermal_expansion_coefficient: float = 12e-6):
        self.alpha = thermal_expansion_coefficient
    
    def compute_thermal_strain(self, temperature_change: float) -> float:
        """Compute thermal strain from temperature change."""
        # ε = α·ΔT
        return self.alpha * temperature_change
    
    def compute_thermal_force(self, temperature_change: float, area: float, E: float) -> float:
        """Compute thermal restraint force for fully restrained member."""
        # F = E·A·α·ΔT
        return E * area * self.alpha * temperature_change
    
    def compute_temperature_gradient_effects(self, top_temp: float, bottom_temp: float, depth: float) -> float:
        """Compute moment due to thermal gradient through depth."""
        delta_T = top_temp - bottom_temp
        # Simplified moment calculation
        return delta_T * depth**2 * 1e5
