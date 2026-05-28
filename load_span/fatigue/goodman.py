"""Goodman mean stress correction for fatigue analysis."""

import numpy as np


def goodman_correction(
    stress_amplitude: float,
    mean_stress: float,
    ultimate_strength: float
) -> float:
    """
    Apply Goodman mean stress correction.
    
    σ_a,eq = σ_a / (1 - σ_m/σ_u)
    
    Args:
        stress_amplitude: Alternating stress amplitude (Pa)
        mean_stress: Mean stress (Pa)
        ultimate_strength: Ultimate tensile strength (Pa)
    
    Returns:
        Equivalent fully-reversed stress amplitude
    """
    if mean_stress >= ultimate_strength:
        return float('inf')
    
    if mean_stress <= 0:
        return stress_amplitude
    
    return stress_amplitude / (1 - mean_stress / ultimate_strength)


def gerber_correction(stress_amplitude: float, mean_stress: float, ultimate_strength: float) -> float:
    """Gerber parabolic mean stress correction."""
    if mean_stress >= ultimate_strength:
        return float('inf')
    
    return stress_amplitude / (1 - (mean_stress / ultimate_strength)**2)
