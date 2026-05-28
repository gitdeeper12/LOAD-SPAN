"""Demand-to-capacity ratio (DCR) computation."""

from typing import List, Dict


def compute_demand_capacity_ratio(
    demand: float,
    capacity: float
) -> float:
    """
    Compute Demand-to-Capacity Ratio (DCR).
    
    DCR = Q_UD / Q_CE
    
    Where:
        Q_UD: Ultimate demand (redistributed load)
        Q_CE: Expected capacity
    
    GSA criteria:
        DCR ≤ 2.0 for all members
        DCR > 1.0 indicates potential failure
    """
    if capacity <= 0:
        return float('inf')
    
    return demand / capacity


def assess_progressive_collapse_risk(
    dcr_values: List[float],
    redistribution_magnitude: float,
    redundancy_index: float
) -> Dict:
    """
    Assess progressive collapse risk.
    
    Returns risk classification and recommended actions.
    """
    max_dcr = max(dcr_values) if dcr_values else 0.0
    n_overloaded = sum(1 for dcr in dcr_values if dcr > 1.0)
    
    # Calculate risk score
    risk_score = (
        0.4 * min(max_dcr / 2.0, 1.0) +
        0.3 * min(n_overloaded / 5.0, 1.0) +
        0.3 * (1.0 - redundancy_index)
    )
    
    if risk_score < 0.3:
        classification = "LOW RISK"
        action = "Continue standard monitoring"
    elif risk_score < 0.6:
        classification = "MEDIUM RISK"
        action = "Enhanced monitoring; inspect overloaded members"
    elif risk_score < 0.8:
        classification = "HIGH RISK"
        action = "Reduce operational loads; schedule detailed inspection"
    else:
        classification = "CRITICAL RISK"
        action = "Immediate closure; emergency structural assessment"
    
    return {
        "risk_score": risk_score,
        "classification": classification,
        "action": action,
        "max_dcr": max_dcr,
        "n_overloaded_members": n_overloaded
    }


def compute_tie_force_capacity(
    reinforcement_area: float,
    yield_strength: float,
    n_bars: int = 1
) -> float:
    """
    Compute tie force capacity per UFC 4-023-03.
    
    T = A_s × f_y × n_bars
    """
    return reinforcement_area * yield_strength * n_bars


def gsa_robustness_index(
    n_load_paths: int,
    max_dcr: float,
    redundancy: float
) -> float:
    """
    Compute GSA robustness index.
    
    RI = (n_paths / n_paths_min) × (1/max_dcr) × redundancy
    """
    n_paths_min = 2.0
    dcr_factor = 1.0 / max(1.0, max_dcr)
    
    robustness = (n_load_paths / n_paths_min) * dcr_factor * redundancy
    
    return min(robustness, 1.0)
