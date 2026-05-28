"""Failure probability calculation from reliability index."""

import numpy as np
from scipy.special import ndtr


def failure_probability(beta: float) -> float:
    """
    Compute failure probability from reliability index.
    
    P_f = Φ(-β)
    
    Where Φ is the standard normal cumulative distribution function.
    """
    return ndtr(-beta)


def annual_failure_probability(beta: float, n_years: int = 1) -> float:
    """
    Compute annual failure probability.
    
    For time-dependent reliability.
    """
    p_f = failure_probability(beta)
    return 1.0 - (1.0 - p_f) ** (1.0 / n_years)


def target_reliability_index(target_pf: float = 1e-4) -> float:
    """
    Compute target reliability index from target failure probability.
    
    β_target = -Φ⁻¹(P_f,target)
    
    Typical targets:
    - P_f = 10⁻⁴ → β = 3.72 (high consequence)
    - P_f = 10⁻³ → β = 3.09 (normal)
    - P_f = 10⁻² → β = 2.33 (low consequence)
    """
    from scipy.special import ndtri
    return -ndtri(target_pf)


def reliability_classification(beta: float) -> str:
    """
    Classify reliability level.
    
    Based on Eurocode reliability classes.
    """
    if beta >= 4.7:
        return "RC3 - Very High Reliability"
    elif beta >= 3.8:
        return "RC2 - High Reliability"
    elif beta >= 2.9:
        return "RC1 - Medium Reliability"
    elif beta >= 1.5:
        return "RC0 - Low Reliability"
    else:
        return "Unacceptable - Immediate Action Required"


def remaining_safe_life(
    current_beta: float,
    degradation_rate: float,
    target_beta: float = 3.8
) -> float:
    """
    Estimate remaining safe operational life in years.
    
    Assumes linear degradation.
    """
    if degradation_rate <= 0:
        return float('inf')
    
    beta_remaining = current_beta - target_beta
    if beta_remaining <= 0:
        return 0.0
    
    return beta_remaining / degradation_rate
