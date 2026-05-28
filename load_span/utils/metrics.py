"""LSII, β, D_fatigue, R_struct computation utilities."""

import numpy as np
from typing import Dict, List, Tuple


def compute_metrics(
    beta: float,
    d_fatigue: float,
    r_struct: float,
    lambda_cr: float
) -> Dict:
    """
    Compute comprehensive structural metrics.
    
    Returns:
        Dictionary with normalized and raw metrics
    """
    target_beta = 3.8
    target_lambda = 2.0
    d_limit = 0.80
    
    # Normalized values
    beta_norm = min(beta / target_beta, 1.0)
    fatigue_norm = max(1.0 - d_fatigue / d_limit, 0.0)
    lambda_norm = min(lambda_cr / target_lambda, 1.0)
    
    # LSII (simplified - use LongSpanIntegrityIndex class for full)
    lsii = 0.35 * beta_norm + 0.30 * fatigue_norm + 0.20 * r_struct + 0.15 * lambda_norm
    
    return {
        'beta_raw': beta,
        'beta_normalized': beta_norm,
        'd_fatigue_raw': d_fatigue,
        'd_fatigue_normalized': fatigue_norm,
        'r_struct_raw': r_struct,
        'lambda_cr_raw': lambda_cr,
        'lambda_cr_normalized': lambda_norm,
        'lsii': min(max(lsii, 0.0), 1.0)
    }


def compute_reliability_target(p_f: float = 1e-4) -> float:
    """Compute target reliability index from failure probability."""
    from scipy.special import ndtri
    return -ndtri(p_f)


def compute_fatigue_damage_rate(
    daily_increment: float,
    n_days: int = 365
) -> float:
    """Compute annual fatigue damage rate."""
    return daily_increment * n_days


def estimate_remaining_life_from_metrics(
    d_fatigue: float,
    degradation_rate: float,
    r_struct: float,
    critical_damage: float = 1.0
) -> float:
    """
    Estimate remaining operational life in years.
    
    Considers fatigue damage and structural redundancy.
    """
    if d_fatigue >= critical_damage:
        return 0.0
    
    remaining_damage_capacity = critical_damage - d_fatigue
    
    # Redundancy extends life
    redundancy_factor = 0.5 + 0.5 * r_struct
    
    if degradation_rate <= 0:
        return float('inf')
    
    remaining_years = (remaining_damage_capacity / degradation_rate) * redundancy_factor
    
    return remaining_years


def compute_damage_interaction_factor(
    fatigue_damage: float,
    corrosion_damage: float
) -> float:
    """
    Compute synergistic damage interaction factor.
    
    Accounts for combined effects of fatigue and corrosion.
    """
    # Simple multiplicative interaction
    if fatigue_damage <= 0 or corrosion_damage <= 0:
        return 1.0
    
    interaction = 1.0 + 0.5 * fatigue_damage * corrosion_damage
    
    return min(interaction, 2.0)
