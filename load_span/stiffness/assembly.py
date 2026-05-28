"""Global stiffness matrix assembly K·u = f."""

import numpy as np
from typing import List, Tuple


def assemble_global_stiffness(
    elements: List[dict],
    nodes: List[dict],
    dof_per_node: int = 6
) -> np.ndarray:
    """
    Assemble global stiffness matrix from element stiffness matrices.
    
    K_global = Σ K_e (element assembly)
    
    Args:
        elements: List of element properties (E, I, A, L, connectivity)
        nodes: List of node coordinates
        dof_per_node: Degrees of freedom per node (default 6 for 3D)
    
    Returns:
        Global stiffness matrix K (n_dof x n_dof)
    """
    n_nodes = len(nodes)
    n_dof = n_nodes * dof_per_node
    
    K_global = np.zeros((n_dof, n_dof))
    
    for element in elements:
        # Get element stiffness matrix in global coordinates
        K_element = element_stiffness_matrix(
            E=element.get('E', 200e9),
            I=element.get('I', 1e-3),
            A=element.get('A', 0.01),
            L=element.get('L', 10.0),
            theta=element.get('theta', 0.0)
        )
        
        # Get degrees of freedom for this element
        dof_indices = get_element_dof_indices(
            element['connectivity'],
            dof_per_node
        )
        
        # Assemble into global matrix
        for i, idx_i in enumerate(dof_indices):
            for j, idx_j in enumerate(dof_indices):
                K_global[idx_i, idx_j] += K_element[i, j]
    
    return K_global


def element_stiffness_matrix(
    E: float, I: float, A: float, L: float, theta: float
) -> np.ndarray:
    """
    Compute element stiffness matrix in global coordinates.
    
    For a 2D beam-column element with 6 DOF (2 nodes × 3 DOF):
    [u1, v1, θ1, u2, v2, θ2]
    """
    # Local stiffness matrix (6x6)
    k_local = np.zeros((6, 6))
    
    # Axial stiffness
    k_axial = E * A / L
    k_local[0, 0] = k_axial
    k_local[3, 3] = k_axial
    k_local[0, 3] = -k_axial
    k_local[3, 0] = -k_axial
    
    # Bending stiffness
    k_bending = E * I / L**3
    k_local[1, 1] = 12 * k_bending
    k_local[4, 4] = 12 * k_bending
    k_local[1, 4] = -12 * k_bending
    k_local[4, 1] = -12 * k_bending
    
    # Moment terms
    k_local[1, 2] = 6 * k_bending * L
    k_local[2, 1] = 6 * k_bending * L
    k_local[1, 5] = -6 * k_bending * L
    k_local[5, 1] = -6 * k_bending * L
    k_local[2, 4] = -6 * k_bending * L
    k_local[4, 2] = -6 * k_bending * L
    k_local[2, 2] = 4 * k_bending * L**2
    k_local[5, 5] = 4 * k_bending * L**2
    k_local[2, 5] = 2 * k_bending * L**2
    k_local[5, 2] = 2 * k_bending * L**2
    
    # Transform to global coordinates
    c = np.cos(theta)
    s = np.sin(theta)
    T = np.zeros((6, 6))
    T[0, 0] = c
    T[0, 1] = s
    T[1, 0] = -s
    T[1, 1] = c
    T[2, 2] = 1
    T[3, 3] = c
    T[3, 4] = s
    T[4, 3] = -s
    T[4, 4] = c
    T[5, 5] = 1
    
    return T.T @ k_local @ T


def get_element_dof_indices(
    connectivity: List[int],
    dof_per_node: int
) -> List[int]:
    """Get global DOF indices for an element."""
    indices = []
    for node_id in connectivity:
        start_dof = node_id * dof_per_node
        indices.extend(range(start_dof, start_dof + dof_per_node))
    return indices


def solve_displacements(
    K: np.ndarray,
    F: np.ndarray,
    fixed_dofs: List[int]
) -> np.ndarray:
    """
    Solve for displacements: K·u = f.
    
    Apply boundary conditions for fixed degrees of freedom.
    """
    n_dof = len(K)
    free_dofs = [i for i in range(n_dof) if i not in fixed_dofs]
    
    # Partition matrices
    K_ff = K[np.ix_(free_dofs, free_dofs)]
    F_f = F[free_dofs]
    
    # Solve
    u_f = np.linalg.solve(K_ff, F_f)
    
    # Assemble full displacement vector
    u = np.zeros(n_dof)
    u[free_dofs] = u_f
    
    return u
