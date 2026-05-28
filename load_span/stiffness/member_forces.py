"""Member axial, shear, and moment extraction."""

import numpy as np
from typing import Dict, List, Tuple


def extract_member_forces(
    u: np.ndarray,
    elements: List[dict]
) -> List[Dict]:
    """
    Extract internal forces for each member.
    
    Returns axial force, shear force, and bending moment.
    """
    member_forces = []
    
    for element in elements:
        # Get element DOFs
        dofs = get_element_dofs(element['connectivity'])
        u_e = u[dofs]
        
        # Compute element forces
        forces = compute_element_forces(
            u_e,
            E=element.get('E', 200e9),
            A=element.get('A', 0.01),
            I=element.get('I', 1e-3),
            L=element.get('L', 10.0)
        )
        
        member_forces.append({
            'id': element.get('id', 0),
            'axial': forces[0],
            'shear': forces[1],
            'moment': forces[2],
            'status': 'ok' if abs(forces[0]) < element.get('capacity', 1e6) else 'overloaded'
        })
    
    return member_forces


def compute_element_forces(
    u_e: np.ndarray,
    E: float,
    A: float,
    I: float,
    L: float
) -> Tuple[float, float, float]:
    """Compute axial force, shear, and moment from displacements."""
    # Axial displacement
    delta_axial = u_e[3] - u_e[0]
    axial_force = E * A / L * delta_axial
    
    # Rotation and deflection
    theta1 = u_e[2]
    theta2 = u_e[5]
    delta_trans = u_e[4] - u_e[1]
    
    # Shear force
    shear = 12 * E * I / L**3 * delta_trans + 6 * E * I / L**2 * (theta1 + theta2)
    
    # Bending moment at node 1
    moment = 6 * E * I / L**2 * delta_trans + 4 * E * I / L * theta1 + 2 * E * I / L * theta2
    
    return axial_force, shear, moment


def compute_demand_capacity_ratio(
    force: float,
    capacity: float
) -> float:
    """
    Compute Demand-to-Capacity Ratio (DCR).
    
    DCR = F_redistributed / F_capacity
    DCR > 1.0 indicates potential failure
    """
    if capacity <= 0:
        return float('inf')
    return force / capacity


def get_element_dofs(connectivity: List[int]) -> List[int]:
    """Get global DOF indices for an element."""
    dofs = []
    for node in connectivity:
        dofs.extend([node*3, node*3+1, node*3+2])
    return dofs
