"""Moving load and traffic stream models for bridges."""

import numpy as np


class TrafficLoadModel:
    """Traffic load modeling for bridge deck."""
    
    def __init__(self, lane_width: float = 3.5, n_lanes: int = 2):
        self.lane_width = lane_width
        self.n_lanes = n_lanes
    
    def compute_traffic_load(self, traffic_intensity: float) -> float:
        """Compute traffic load based on intensity (vehicles/hour)."""
        # Simplified load calculation
        load_per_vehicle = 100e3  # 100 kN per vehicle
        return traffic_intensity / 3600 * load_per_vehicle
    
    def generate_load_spectrum(self, duration_hours: float = 24) -> np.ndarray:
        """Generate time-varying traffic load spectrum."""
        t = np.linspace(0, duration_hours, int(duration_hours * 3600))
        # Diurnal pattern
        load = 50e3 * (1 + 0.5 * np.sin(2 * np.pi * t / 24))
        return load
