"""ASTM E1049-85 rainflow cycle counting algorithm."""

import numpy as np
from typing import List, Tuple


class RainflowCounter:
    """
    Rainflow cycle counting for variable amplitude fatigue analysis.
    
    Implements ASTM E1049-85 standard for extracting cycle spectra
    from continuous stress time histories.
    """
    
    def count(self, stress_history: np.ndarray) -> List[Tuple[float, int]]:
        """
        Perform rainflow cycle counting.
        
        Args:
            stress_history: Array of stress values (Pa)
        
        Returns:
            List of (stress_amplitude, count) tuples
        """
        # Extract turning points (peaks and valleys)
        turning_points = self._extract_turning_points(stress_history)
        
        if len(turning_points) < 3:
            return []
        
        # Perform rainflow counting
        cycles = self._rainflow_algorithm(turning_points)
        
        # Bin cycles by amplitude
        binned_cycles = self._bin_by_amplitude(cycles)
        
        return binned_cycles
    
    def _extract_turning_points(self, data: np.ndarray) -> np.ndarray:
        """Extract peaks and valleys from stress history."""
        if len(data) < 3:
            return data
        
        turning = [data[0]]
        
        for i in range(1, len(data) - 1):
            if (data[i] > data[i-1] and data[i] > data[i+1]) or \
               (data[i] < data[i-1] and data[i] < data[i+1]):
                turning.append(data[i])
        
        turning.append(data[-1])
        return np.array(turning)
    
    def _rainflow_algorithm(self, points: np.ndarray) -> List[Tuple[float, float]]:
        """
        Implement rainflow counting algorithm.
        
        Returns list of (range, mean) for each cycle.
        """
        if len(points) < 3:
            return []
        
        cycles = []
        stack = list(points)
        idx = 0
        
        while len(stack) >= 3 and idx < len(stack) - 2:
            x = stack[idx]
            y = stack[idx + 1]
            z = stack[idx + 2]
            
            # Check for full cycle
            if abs(y - x) <= abs(z - y):
                # Extract cycle
                amplitude = abs(y - x) / 2
                mean = (x + y) / 2
                cycles.append((amplitude, mean))
                
                # Remove points x and y
                stack.pop(idx)
                stack.pop(idx)
                
                # Reset index
                idx = max(0, idx - 1)
            else:
                idx += 1
        
        # Half cycles for remaining points
        for i in range(len(stack) - 1):
            amplitude = abs(stack[i + 1] - stack[i]) / 2
            mean = (stack[i] + stack[i + 1]) / 2
            cycles.append((amplitude, mean))
        
        return cycles
    
    def _bin_by_amplitude(
        self,
        cycles: List[Tuple[float, float]],
        n_bins: int = 20
    ) -> List[Tuple[float, int]]:
        """Bin cycles by stress amplitude."""
        if not cycles:
            return []
        
        amplitudes = [c[0] for c in cycles]
        max_amp = max(amplitudes)
        min_amp = min(amplitudes)
        
        if max_amp == min_amp:
            return [(max_amp, len(cycles))]
        
        bin_edges = np.linspace(min_amp, max_amp, n_bins + 1)
        bins = [[] for _ in range(n_bins)]
        
        for amp in amplitudes:
            bin_idx = min(int((amp - min_amp) / (max_amp - min_amp) * n_bins), n_bins - 1)
            bins[bin_idx].append(amp)
        
        result = []
        for i, bin_cycles in enumerate(bins):
            if bin_cycles:
                mean_amp = np.mean(bin_cycles)
                result.append((mean_amp, len(bin_cycles)))
        
        return result
