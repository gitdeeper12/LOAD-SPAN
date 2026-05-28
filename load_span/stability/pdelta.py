"""P-delta geometric stiffness matrix K_G for second-order analysis."""

import numpy as np


def compute_geometric_stiffness(
    axial_force: float,
    length: float,
    element_type: str = "beam"
) -> np.ndarray:
    """
    Compute geometric stiffness matrix K_G for P-delta effects.
    
    Accounts for stiffness modification due to axial forces.
    """
    if element_type == "beam":
        # 6x6 geometric stiffness for beam-column
        K_G = np.zeros((6, 6))
        factor = axial_force / length
        
        K_G[1, 1] = 6/5 * factor
        K_G[4, 4] = 6/5 * factor
        K_G[1, 4] = -6/5 * factor
        K_G[4, 1] = -6/5 * factor
        K_G[2, 2] = 2/15 * factor * length**2
        K_G[5, 5] = 2/15 * factor * length**2
        K_G[2, 5] = 1/30 * factor * length**2
        K_G[5, 2] = 1/30 * factor * length**2
        
        return K_G
    else:
        return np.zeros((6, 6))


def compute_tangent_stiffness(K_elastic: np.ndarray, K_geometric: np.ndarray) -> np.ndarray:
    """
    Compute tangent stiffness matrix K_T = K_elastic + K_geometric(P).
    """
    return K_elastic + K_geometric
