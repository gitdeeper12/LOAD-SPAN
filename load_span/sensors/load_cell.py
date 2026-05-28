"""Cable force and bearing load cell data processing."""

import numpy as np
from typing import Dict


class LoadCellParser:
    """Load cell data parser for cable force measurement."""
    
    def __init__(self, capacity_kn: float = 1000.0, calibration_factor: float = 1.0):
        self.capacity = capacity_kn * 1000  # Convert to N
        self.calibration = calibration_factor
    
    def parse_voltage(self, voltage: np.ndarray, excitation: float = 10.0) -> np.ndarray:
        """Convert voltage to force in Newtons."""
        force = (voltage / excitation) * self.capacity * self.calibration
        return force
    
    def compute_cable_force_statistics(self, force: np.ndarray) -> Dict:
        """Compute cable force statistics."""
        return {
            "mean_force_n": float(np.mean(force)),
            "max_force_n": float(np.max(force)),
            "min_force_n": float(np.min(force)),
            "std_force_n": float(np.std(force)),
            "force_range_n": float(np.ptp(force))
        }
    
    def detect_cable_loss(self, force: np.ndarray, threshold_ratio: float = 0.1) -> bool:
        """Detect sudden cable loss based on force drop."""
        current_force = force[-1] if len(force) > 0 else self.capacity
        return current_force < self.capacity * threshold_ratio
