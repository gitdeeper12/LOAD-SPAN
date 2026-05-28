"""Response spectrum seismic input for long-span structures."""

import numpy as np


class SeismicLoadModel:
    """Seismic load modeling using response spectrum."""
    
    def __init__(self, peak_ground_acceleration: float = 0.2):
        self.pga = peak_ground_acceleration  # in g
    
    def compute_response_spectrum(self, periods: np.ndarray, soil_type: str = 'D') -> np.ndarray:
        """Compute spectral acceleration for given periods."""
        # Simplified spectrum per ASCE 7
        Sa = np.zeros_like(periods)
        
        for i, T in enumerate(periods):
            if T < 0.1:
                Sa[i] = self.pga * (1 + 10 * T)
            elif T < 0.5:
                Sa[i] = self.pga * 2.5
            else:
                Sa[i] = self.pga * 2.5 * 0.5 / T
        
        return Sa * 9.81  # Convert to m/s²
    
    def compute_base_shear(self, weight: float, spectral_acceleration: float) -> float:
        """Compute seismic base shear."""
        # V = C_s · W
        C_s = spectral_acceleration / 9.81
        return C_s * weight
