"""Cornell first-order second-moment (FOSM) reliability index."""

import numpy as np
from typing import Tuple


def compute_cornell_index(
    mean_resistance: float,
    mean_load: float,
    std_resistance: float,
    std_load: float
) -> float:
    """
    Compute Cornell reliability index β.
    
    β = (μ_R - μ_S) / √(σ_R² + σ_S²)
    
    Where:
        μ_R: Mean resistance
        μ_S: Mean load effect
        σ_R: Standard deviation of resistance
        σ_S: Standard deviation of load
    
    Returns:
        Reliability index (higher = safer)
        Target β ≥ 3.8 for annual failure probability ~10⁻⁴
    """
    if std_resistance <= 0 and std_load <= 0:
        return float('inf')
    
    numerator = mean_resistance - mean_load
    
    if numerator <= 0:
        return 0.0
    
    denominator = np.sqrt(std_resistance**2 + std_load**2)
    
    return numerator / denominator


def compute_augmented_reliability_index(
    mean_resistance: float,
    mean_load: float,
    std_resistance: float,
    std_load: float,
    var_ai_error: float = 0.0
) -> float:
    """
    Compute AI-augmented reliability index.
    
    β_augmented = (μ_R - μ_S) / √(σ_R² + σ_S² + σ_AI²)
    
    Conservative adjustment - AI uncertainty reduces reliability index.
    """
    numerator = mean_resistance - mean_load
    
    if numerator <= 0:
        return 0.0
    
    denominator = np.sqrt(std_resistance**2 + std_load**2 + var_ai_error)
    
    return numerator / denominator


def compute_time_dependent_reliability(
    initial_beta: float,
    degradation_rate: float,
    time_years: float,
    fatigue_damage: float = 0.0
) -> float:
    """
    Compute time-dependent reliability index.
    
    β(t) = β₀ - η·t - λ·D(t)
    
    Where:
        η: Degradation rate per year
        λ: Fatigue damage sensitivity
        D(t): Cumulative fatigue damage
    """
    eta = 0.05  # Typical degradation rate
    lamb = 1.5  # Fatigue sensitivity
    
    beta_t = initial_beta - eta * time_years - lamb * fatigue_damage
    
    return max(beta_t, 0.0)
