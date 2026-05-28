"""Linear variable differential transformer (LVDT) displacement sensor."""

import numpy as np
from typing import Dict


class DisplacementSensor:
    """LVDT displacement sensor parser."""
    
    def __init__(self, sensitivity: float = 1.0, range_mm: float = 100.0):
        self.sensitivity = sensitivity
        self.range_mm = range_mm
    
    def parse_voltage(self, voltage: np.ndarray, excitation_voltage: float = 5.0) -> np.ndarray:
        """Convert voltage reading to displacement in mm."""
        # Displacement = (V_out / V_excitation) * range
        displacement = (voltage / excitation_voltage) * self.range_mm
        return displacement
    
    def compute_deflection(self, displacement: np.ndarray) -> Dict:
        """Compute deflection metrics."""
        return {
            "max_deflection_mm": float(np.max(displacement)),
            "min_deflection_mm": float(np.min(displacement)),
            "range_mm": float(np.ptp(displacement)),
            "midspan_deflection_mm": float(np.median(displacement))
        }
