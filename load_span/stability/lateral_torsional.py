"""Lateral-torsional buckling assessment for beams."""

import numpy as np


def compute_lateral_torsional_buckling_moment(
    E: float,
    G: float,
    I_y: float,
    I_w: float,
    J: float,
    L: float,
    C1: float = 1.0
) -> float:
    """
    Compute elastic lateral-torsional buckling moment M_cr.
    
    M_cr = C1 * (π²·E·I_y / L²) * √(I_w/I_y + G·J·L²/(π²·E·I_y))
    """
    term1 = np.pi**2 * E * I_y / L**2
    term2 = np.sqrt(I_w / I_y + G * J * L**2 / (np.pi**2 * E * I_y))
    
    return C1 * term1 * term2


def check_lateral_torsional_stability(M_applied: float, M_cr: float, safety_factor: float = 1.5) -> bool:
    """Check if member is safe against lateral-torsional buckling."""
    return M_applied * safety_factor <= M_cr
