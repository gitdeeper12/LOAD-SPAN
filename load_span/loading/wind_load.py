"""Dynamic wind pressure and buffeting models."""

import numpy as np


class WindLoadModel:
    """Wind load modeling for long-span structures."""
    
    def __init__(self, air_density: float = 1.225):
        self.air_density = air_density
    
    def compute_wind_pressure(self, wind_speed: float, drag_coefficient: float = 1.2) -> float:
        """Compute dynamic wind pressure."""
        # P = 0.5 * ρ * C_d * V²
        return 0.5 * self.air_density * drag_coefficient * wind_speed**2
    
    def compute_buffeting_forces(self, mean_wind_speed: float, turbulence_intensity: float = 0.1) -> float:
        """Compute buffeting forces due to wind turbulence."""
        return self.compute_wind_pressure(mean_wind_speed) * (1 + 3 * turbulence_intensity)
    
    def generate_wind_speed_series(self, mean_speed: float, duration: float, dt: float = 0.1) -> np.ndarray:
        """Generate wind speed time series using Kaimal spectrum."""
        t = np.arange(0, duration, dt)
        # Simplified turbulence simulation
        turbulence = np.random.normal(0, 0.1 * mean_speed, len(t))
        return mean_speed + turbulence
