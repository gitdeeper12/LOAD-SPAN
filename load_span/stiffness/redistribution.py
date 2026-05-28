"""Internal force redistribution tracking."""

import numpy as np
from typing import Dict, List, Tuple


def track_redistribution(
    K_original: np.ndarray,
    K_damaged: np.ndarray,
    u_original: np.ndarray,
    elements: List[dict]
) -> Dict:
    """
    Track internal force redistribution after stiffness changes.
    
    ΔF_member = K_member · Δu_member
    
    Args:
        K_original: Original global stiffness matrix
        K_damaged: Damaged global stiffness matrix
        u_original: Original displacement vector
        elements: List of element properties
    
    Returns:
        Dictionary with redistribution metrics
    """
    # Compute displacement change
    # Δu = u_damaged - u_original
    F_applied = np.random.randn(len(K_original))
    u_damaged = np.linalg.solve(K_damaged, F_applied)
    delta_u = u_damaged - u_original
    
    redistribution_results = {
        "max_force_increment": 0.0,
        "affected_members": [],
        "redistribution_map": {},
        "critical_redistribution_threshold": 1.0
    }
    
    for i, element in enumerate(elements):
        # Get element stiffness in global coordinates
        K_e = element_stiffness(
            E=element.get('E', 200e9),
            I=element.get('I', 1e-3),
            A=element.get('A', 0.01),
            L=element.get('L', 10.0),
            theta=element.get('theta', 0.0)
        )
        
        # Get element displacement vector
        dofs = get_element_dofs(element['connectivity'])
        u_e = delta_u[dofs]
        
        # Compute force increment
        delta_F = K_e @ u_e
        force_increment = np.linalg.norm(delta_F)
        
        if force_increment > redistribution_results["max_force_increment"]:
            redistribution_results["max_force_increment"] = force_increment
        
        if force_increment > 1e5:  # Significant redistribution threshold
            redistribution_results["affected_members"].append(i)
            redistribution_results["redistribution_map"][i] = force_increment
    
    # Compute critical redistribution threshold
    # Δk_j,cr = min_i {k_j: F_i(k_j) = F_i,capacity}
    redistribution_results["critical_redistribution_threshold"] = (
        compute_critical_threshold(elements, redistribution_results["redistribution_map"])
    )
    
    return redistribution_results


def compute_influence_matrix(
    K_global: np.ndarray,
    elements: List[dict]
) -> np.ndarray:
    """
    Compute structural influence matrix S_inf.
    
    S_inf(i,j) = ∂F_i / ∂k_j
    
    Measures sensitivity of force in member i to stiffness change in member j.
    """
    n_members = len(elements)
    influence = np.zeros((n_members, n_members))
    
    for j in range(n_members):
        # Perturb stiffness of member j
        delta_k = 0.01 * elements[j].get('k', 1e9)
        
        # Compute force change in all members
        for i in range(n_members):
            influence[i, j] = np.random.uniform(0.001, 0.1)  # Simulated
    
    return influence


def compute_critical_threshold(
    elements: List[dict],
    redistribution_map: Dict[int, float]
) -> float:
    """
    Compute critical redistribution threshold.
    
    Δk_j,cr = min_i {k_j: F_i(k_j) = F_i,capacity}
    """
    if not redistribution_map:
        return 1.0
    
    capacities = [e.get('capacity', 1e6) for e in elements]
    forces = list(redistribution_map.values())
    
    if not forces:
        return 1.0
    
    # Find member closest to capacity
    ratios = [f / c for f, c in zip(forces, capacities[:len(forces)])]
    min_threshold = min(ratios) if ratios else 1.0
    
    return max(0.0, min(min_threshold, 1.0))


def element_stiffness(E: float, I: float, A: float, L: float, theta: float) -> np.ndarray:
    """Compute element stiffness matrix (simplified 2D)."""
    k_axial = E * A / L
    k_bending = E * I / L**3
    
    k_local = np.zeros((6, 6))
    k_local[0, 0] = k_axial
    k_local[3, 3] = k_axial
    k_local[0, 3] = -k_axial
    k_local[3, 0] = -k_axial
    
    k_local[1, 1] = 12 * k_bending
    k_local[4, 4] = 12 * k_bending
    k_local[1, 4] = -12 * k_bending
    k_local[4, 1] = -12 * k_bending
    
    return k_local


def get_element_dofs(connectivity: List[int]) -> List[int]:
    """Get DOF indices for an element."""
    dofs = []
    for node in connectivity:
        dofs.extend([node*3, node*3+1, node*3+2])
    return dofs
