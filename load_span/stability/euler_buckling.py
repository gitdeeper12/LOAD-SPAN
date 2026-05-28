"""Euler critical buckling load computation."""

import numpy as np


def compute_euler_critical_load(
    E: float,
    I: float,
    L: float,
    K_factor: float = 1.0
) -> float:
    """
    Compute Euler critical buckling load.
    
    P_cr = π²·E·I / (K·L)²
    
    Args:
        E: Young's modulus (Pa)
        I: Second moment of area (m⁴)
        L: Member length (m)
        K_factor: Effective length factor (boundary condition dependent)
            - K = 0.5: Fixed-fixed
            - K = 0.7: Fixed-pinned
            - K = 1.0: Pinned-pinned
            - K = 2.0: Fixed-free
    
    Returns:
        Critical buckling load (N)
    """
    if L <= 0:
        return float('inf')
    
    return (np.pi**2 * E * I) / (K_factor * L)**2


def get_effective_length_factor(
    end_condition_1: str,
    end_condition_2: str
) -> float:
    """
    Get effective length factor K based on end conditions.
    
    Parameters:
        end_condition_1, end_condition_2: 'fixed', 'pinned', or 'free'
    """
    conditions = {
        ('fixed', 'fixed'): 0.5,
        ('fixed', 'pinned'): 0.7,
        ('pinned', 'pinned'): 1.0,
        ('fixed', 'free'): 2.0,
        ('pinned', 'free'): 2.0,
    }
    
    key = tuple(sorted([end_condition_1, end_condition_2]))
    return conditions.get(key, 1.0)


def compute_dynamic_buckling_threshold(
    P_cr_euler: float,
    gamma_ml: float,
    a_max: float,
    omega: float,
    t: float,
    g: float = 9.81
) -> float:
    """
    Compute dynamic buckling threshold with imperfection effects.
    
    P_cr,predicted = P_cr,euler · [1 - γ_ML · (a_max/g) · sin(Ω·t)]
    
    Args:
        P_cr_euler: Euler critical load
        gamma_ml: Imperfection sensitivity coefficient (≤ 0.15)
        a_max: Measured vibration amplitude (m)
        omega: Excitation frequency (rad/s)
        t: Time (s)
        g: Gravitational acceleration (m/s²)
    
    Returns:
        Dynamic critical load
    """
    imperfection_term = gamma_ml * (a_max / g) * np.sin(omega * t)
    reduction = max(0.0, 1.0 - imperfection_term)
    
    return P_cr_euler * reduction


def compute_critical_load_factor(
    P_cr: float,
    P_applied: float
) -> float:
    """
    Compute critical load factor λ_cr.
    
    λ_cr = P_cr / P_applied
    λ_cr ≥ 2.0 target per design codes
    """
    if P_applied <= 0:
        return float('inf')
    
    return P_cr / P_applied
