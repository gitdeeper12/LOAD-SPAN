"""Multi-sensor data fusion and quality control."""

import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy.stats import zscore


class SensorDataFusion:
    """
    Multi-sensor data fusion for structural health monitoring.
    
    Combines data from:
    - Accelerometers (dynamic response)
    - Strain gauges (stress/strain)
    - Load cells (cable forces)
    - Displacement transducers (deflection)
    """
    
    def __init__(self):
        self.fusion_weights = {}
    
    def fuse_modal_parameters(
        self,
        accelerometer_data: List[Dict],
        strain_data: List[Dict]
    ) -> Dict:
        """
        Fuse data from multiple sensors for modal identification.
        
        Returns:
            Combined modal parameters (frequencies, damping ratios)
        """
        # Extract frequencies from accelerometers
        acc_freqs = []
        for acc in accelerometer_data:
            if 'natural_frequencies' in acc:
                acc_freqs.extend(acc['natural_frequencies'])
        
        # Extract from strain gauges
        strain_freqs = []
        for strain in strain_data:
            if 'natural_frequencies' in strain:
                strain_freqs.extend(strain['natural_frequencies'])
        
        # Combine and find consensus frequencies
        all_freqs = np.array(acc_freqs + strain_freqs)
        
        if len(all_freqs) == 0:
            return {"natural_frequencies": [], "confidence": 0.0}
        
        # Use median for robust estimation
        unique_freqs = np.unique(np.round(all_freqs, decimals=2))
        
        return {
            "natural_frequencies": unique_freqs.tolist(),
            "n_sensors": len(accelerometer_data) + len(strain_data),
            "confidence": min(1.0, len(all_freqs) / 20.0)
        }
    
    def detect_outliers(
        self,
        data: np.ndarray,
        method: str = 'zscore',
        threshold: float = 3.0
    ) -> Tuple[np.ndarray, List[int]]:
        """
        Detect outliers in sensor data.
        
        Args:
            data: Sensor data array
            method: 'zscore' or 'iqr'
            threshold: Outlier threshold
        
        Returns:
            (filtered_data, outlier_indices)
        """
        if method == 'zscore':
            z_scores = np.abs(zscore(data))
            outlier_indices = np.where(z_scores > threshold)[0].tolist()
        elif method == 'iqr':
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_indices = np.where((data < lower_bound) | (data > upper_bound))[0].tolist()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Remove outliers
        filtered_data = np.delete(data, outlier_indices)
        
        return filtered_data, outlier_indices
    
    def interpolate_missing_data(
        self,
        data: np.ndarray,
        method: str = 'linear'
    ) -> np.ndarray:
        """
        Interpolate missing or corrupted sensor data.
        
        Methods: 'linear', 'cubic', 'nearest'
        """
        n = len(data)
        mask = np.isnan(data)
        
        if not np.any(mask):
            return data
        
        x = np.arange(n)
        x_missing = x[mask]
        x_valid = x[~mask]
        y_valid = data[~mask]
        
        if len(x_valid) < 2:
            # Not enough valid data points
            return data
        
        from scipy.interpolate import interp1d
        interpolator = interp1d(x_valid, y_valid, kind=method, fill_value='extrapolate')
        y_interp = interpolator(x_missing)
        
        result = data.copy()
        result[mask] = y_interp
        
        return result
    
    def compute_data_quality_score(
        self,
        data: np.ndarray,
        expected_sampling_rate: float,
        actual_sampling_rate: float
    ) -> float:
        """
        Compute overall data quality score (0-1).
        
        Considers:
        - Completeness (missing data fraction)
        - Sampling rate fidelity
        - Signal-to-noise ratio (estimated)
        """
        # Completeness
        missing_fraction = np.isnan(data).mean()
        completeness_score = 1.0 - missing_fraction
        
        # Sampling rate fidelity
        sampling_ratio = actual_sampling_rate / expected_sampling_rate
        sampling_score = min(1.0, sampling_ratio)
        
        # Estimated SNR (simplified)
        data_clean = data[~np.isnan(data)]
        if len(data_clean) > 0:
            noise_estimate = np.std(np.diff(data_clean)) / 2
            signal_estimate = np.std(data_clean)
            snr = signal_estimate / (noise_estimate + 1e-6)
            snr_score = min(1.0, snr / 10.0)
        else:
            snr_score = 0.0
        
        # Weighted average
        quality = 0.4 * completeness_score + 0.3 * sampling_score + 0.3 * snr_score
        
        return quality
