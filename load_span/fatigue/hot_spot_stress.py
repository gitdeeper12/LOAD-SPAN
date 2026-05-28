"""IIW hot-spot stress extrapolation method."""

import numpy as np


def compute_hot_spot_stress_linear(
    strain_04t: float,
    strain_10t: float,
    E: float = 200e9
) -> float:
    """
    Compute hot-spot stress using linear extrapolation (IIW method).
    
    Extrapolates from strain gauge readings at 0.4t and 1.0t.
    """
    epsilon_hotspot = strain_04t + (strain_04t - strain_10t) * 0.4 / 0.6
    return epsilon_hotspot * E


def compute_hot_spot_stress_quadratic(
    strain_04t: float,
    strain_10t: float,
    strain_16t: float,
    E: float = 200e9
) -> float:
    """Quadratic extrapolation using three measurement points."""
    # Quadratic fit through 0.4t, 1.0t, 1.6t
    epsilon_hotspot = 3 * strain_04t - 3 * strain_10t + strain_16t
    return epsilon_hotspot * E
