"""Mode shape extraction and eigenvalue buckling analysis."""

import numpy as np


def compute_buckling_modes(
    K_elastic: np.ndarray,
    K_geometric_ref: np.ndarray,
    n_modes: int = 5
) -> tuple:
    """
    Solve eigenvalue buckling problem.
    
    (K_elastic + λ·K_geometric) · φ = 0
    
    Returns (eigenvalues, eigenvectors)
    """
    # Solve generalized eigenvalue problem
    eigenvalues, eigenvectors = np.linalg.eig(np.linalg.solve(K_elastic, -K_geometric_ref))
    
    # Sort by eigenvalue magnitude
    idx = np.argsort(np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Return first n_modes
    return eigenvalues[:n_modes], eigenvectors[:, :n_modes]


def extract_mode_shape(eigenvector: np.ndarray, dof_per_node: int = 6) -> np.ndarray:
    """
    Extract mode shape displacements from eigenvector.
    """
    n_nodes = len(eigenvector) // dof_per_node
    mode_shape = eigenvector.reshape(n_nodes, dof_per_node)
    
    return mode_shape
