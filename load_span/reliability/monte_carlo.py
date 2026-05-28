"""Monte Carlo sampling for failure probability verification."""

import numpy as np
from typing import Callable, Tuple


def monte_carlo_failure_probability(
    limit_state: Callable,
    n_samples: int = 100000,
    random_variables: dict = None
) -> Tuple[float, float]:
    """
    Estimate failure probability using Monte Carlo simulation.
    
    Args:
        limit_state: Limit state function g(X)
        n_samples: Number of Monte Carlo samples
        random_variables: Dict of variable distributions
    
    Returns:
        (failure_probability, coefficient_of_variation)
    """
    n_failures = 0
    
    for _ in range(n_samples):
        # Sample random variables
        X = {}
        for var_name, dist in random_variables.items():
            X[var_name] = np.random.normal(dist['mean'], dist['std'])
        
        # Evaluate limit state
        g = limit_state(X)
        
        if g < 0:
            n_failures += 1
    
    p_f = n_failures / n_samples
    cov = np.sqrt((1 - p_f) / (n_samples * p_f)) if p_f > 0 else 0
    
    return p_f, cov


def importance_sampling(
    limit_state: Callable,
    n_samples: int = 10000,
    design_point: np.ndarray = None
) -> float:
    """Importance sampling for rare event simulation."""
    # Simplified importance sampling
    n_failures = 0
    
    for _ in range(n_samples):
        # Sample around design point
        X = design_point + np.random.normal(0, 1, len(design_point)) if design_point is not None else np.random.normal(0, 1, 5)
        g = limit_state(X)
        
        if g < 0:
            n_failures += 1
    
    return n_failures / n_samples
