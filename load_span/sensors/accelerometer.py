"""Tri-axial MEMS accelerometer data parser."""

import numpy as np
from typing import Dict, List, Tuple, Optional


class AccelerometerParser:
    """
    Parse and process tri-axial accelerometer data.
    
    Typical sensors: MEMS accelerometers with ±2g to ±16g range
    Sampling rates: 50-200 Hz for structural monitoring
    """
    
    def __init__(self, sampling_rate: float = 200.0):
        self.sampling_rate = sampling_rate
        self.dt = 1.0 / sampling_rate
    
    def parse_raw_data(self, raw_data: np.ndarray) -> Dict:
        """
        Parse raw accelerometer data.
        
        Args:
            raw_data: Array of shape (n_samples, 3) for x, y, z axes
        
        Returns:
            Dictionary with processed accelerations
        """
        if raw_data.shape[1] < 3:
            raise ValueError("Expected at least 3 columns (x, y, z)")
        
        return {
            "acc_x": raw_data[:, 0],
            "acc_y": raw_data[:, 1],
            "acc_z": raw_data[:, 2],
            "time": np.arange(len(raw_data)) * self.dt,
            "sampling_rate": self.sampling_rate
        }
    
    def compute_fft(self, acceleration: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT for frequency domain analysis.
        
        Returns:
            (frequencies, amplitudes)
        """
        n = len(acceleration)
        fft_vals = np.fft.rfft(acceleration)
        amplitudes = np.abs(fft_vals) / n
        
        frequencies = np.fft.rfftfreq(n, self.dt)
        
        return frequencies, amplitudes
    
    def identify_natural_frequencies(
        self,
        acceleration: np.ndarray,
        n_modes: int = 5,
        prominence: float = 0.1
    ) -> List[float]:
        """
        Identify natural frequencies from acceleration response.
        
        Uses peak picking in frequency domain.
        """
        freqs, amps = self.compute_fft(acceleration)
        
        # Find peaks
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(amps, prominence=prominence)
        
        # Sort by amplitude and take top n_modes
        if len(peaks) > 0:
            peak_amplitudes = amps[peaks]
            sorted_idx = np.argsort(peak_amplitudes)[::-1]
            top_peaks = peaks[sorted_idx[:n_modes]]
            natural_freqs = freqs[top_peaks].tolist()
        else:
            natural_freqs = []
        
        return natural_freqs
    
    def compute_rms_acceleration(self, acceleration: np.ndarray) -> float:
        """Compute root mean square acceleration."""
        return np.sqrt(np.mean(acceleration**2))
    
    def compute_peak_acceleration(self, acceleration: np.ndarray) -> float:
        """Compute peak acceleration."""
        return np.max(np.abs(acceleration))
    
    def detect_impacts(self, acceleration: np.ndarray, threshold: float = 5.0) -> List[int]:
        """
        Detect impact events (e.g., vehicle impacts, cable fractures).
        
        Args:
            acceleration: Acceleration time series (m/s²)
            threshold: Impact detection threshold (m/s²)
        
        Returns:
            Indices where impacts were detected
        """
        abs_acc = np.abs(acceleration)
        impact_indices = np.where(abs_acc > threshold)[0]
        
        return impact_indices.tolist()
