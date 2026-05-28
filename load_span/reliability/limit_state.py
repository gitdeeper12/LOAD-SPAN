"""Limit state function definitions for reliability analysis."""

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass
class LimitStateFunction:
    """Container for limit state function and its parameters."""
    
    name: str
    function: Callable
    parameters: Dict[str, float]
    description: str = ""
    
    def evaluate(self, variables: Dict[str, float]) -> float:
        """Evaluate limit state function."""
        return self.function(variables)


def fatigue_limit_state(variables: Dict[str, float]) -> float:
    """
    Fatigue limit state function.
    
    g(X) = D_limit - D_accumulated
    Failure when g(X) < 0
    """
    d_limit = variables.get('D_limit', 1.0)
    d_accumulated = variables.get('D_accumulated', 0.0)
    
    return d_limit - d_accumulated


def buckling_limit_state(variables: Dict[str, float]) -> float:
    """
    Buckling limit state function.
    
    g(X) = P_cr - P_applied
    Failure when g(X) < 0
    """
    p_cr = variables.get('P_cr', 1e6)
    p_applied = variables.get('P_applied', 0.0)
    
    return p_cr - p_applied


def strength_limit_state(variables: Dict[str, float]) -> float:
    """
    Strength limit state function.
    
    g(X) = R - S
    Failure when g(X) < 0
    """
    resistance = variables.get('resistance', 1e6)
    load_effect = variables.get('load_effect', 0.0)
    
    return resistance - load_effect


def deflection_limit_state(variables: Dict[str, float]) -> float:
    """
    Deflection limit state function.
    
    g(X) = δ_limit - δ_actual
    """
    delta_limit = variables.get('delta_limit', 0.025)  # L/400 typical
    delta_actual = variables.get('delta_actual', 0.0)
    
    return delta_limit - delta_actual


def fatigue_with_corrosion_limit_state(variables: Dict[str, float]) -> float:
    """
    Combined fatigue and corrosion limit state.
    
    g(X) = D_limit - D_fatigue - D_corrosion
    """
    d_limit = variables.get('D_limit', 1.0)
    d_fatigue = variables.get('D_fatigue', 0.0)
    d_corrosion = variables.get('D_corrosion', 0.0)
    
    return d_limit - (d_fatigue + d_corrosion)


def system_limit_state(
    limit_states: List[LimitStateFunction],
    variables: Dict[str, float],
    system_type: str = "series"
) -> float:
    """
    Evaluate system-level limit state (series or parallel).
    
    Series system: g_system = min(g_i)
    Parallel system: g_system = max(g_i)
    """
    g_values = [ls.evaluate(variables) for ls in limit_states]
    
    if system_type == "series":
        return min(g_values)
    elif system_type == "parallel":
        return max(g_values)
    else:
        raise ValueError(f"Unknown system type: {system_type}")
