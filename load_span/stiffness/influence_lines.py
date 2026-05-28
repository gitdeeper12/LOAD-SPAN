"""Moving load influence line computation for long-span structures."""

import numpy as np
from typing import List, Tuple


def compute_influence_line(
    positions: np.ndarray,
    response_function: callable,
    n_points: int = 100
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute influence line for a given response function.
    
    Args:
        positions: Array of load positions along the span
        response_function: Function that returns response at given position
        n_points: Number of points for influence line discretization
    
    Returns:
        (positions, influence_values)
    """
    x = np.linspace(0, max(positions), n_points)
    influence = np.array([response_function(xi) for xi in x])
    
    return x, influence


def compute_maximum_influence(
    influence_values: np.ndarray,
    load_magnitude: float = 1.0
) -> float:
    """Compute maximum influence value."""
    return np.max(influence_values) * load_magnitude


def compute_influence_area(influence_values: np.ndarray, dx: float) -> float:
    """Compute area under influence line (total effect)."""
    return np.trapz(influence_values, dx=dx)
