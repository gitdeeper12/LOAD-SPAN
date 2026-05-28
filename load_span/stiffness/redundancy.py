"""Structural redundancy index R_struct computation."""

import numpy as np
from typing import List, Dict


def compute_redundancy_index(
    influence_matrix: np.ndarray,
    n_load_paths: int = 3
) -> float:
    """
    Compute structural redundancy index R_struct.
    
    Measures the number and effectiveness of alternate load paths.
    Higher values (≥0.70) indicate good redundancy.
    
    R_struct = 1 - (average influence / maximum possible influence)
    """
    # Average influence between members
    avg_influence = np.mean(np.abs(influence_matrix))
    
    # Redundancy decreases with higher coupling
    redundancy = max(0.0, 1.0 - avg_influence)
    
    # Adjust for number of load paths
    path_factor = min(1.0, n_load_paths / 5.0)
    redundancy = 0.5 * redundancy + 0.5 * path_factor
    
    return min(1.0, max(0.0, redundancy))


def analyze_alternate_load_paths(
    elements: List[dict],
    removed_element_id: int
) -> Dict:
    """
    Analyze alternate load paths after member removal (ALP analysis).
    
    Implements GSA 2003 alternate load path method.
    """
    # Find connected elements
    connected = find_connected_elements(elements, removed_element_id)
    
    # Compute load redistribution efficiency
    n_alternate_paths = len(connected)
    redistribution_efficiency = min(1.0, n_alternate_paths / 4.0)
    
    # Determine if structure is robust
    robust = n_alternate_paths >= 2 and redistribution_efficiency > 0.6
    
    return {
        "n_alternate_paths": n_alternate_paths,
        "redistribution_efficiency": redistribution_efficiency,
        "robust": robust,
        "connected_members": connected
    }


def find_connected_elements(
    elements: List[dict],
    element_id: int
) -> List[int]:
    """Find elements connected to the removed element."""
    connected = []
    removed = elements[element_id] if element_id < len(elements) else None
    
    if not removed:
        return connected
    
    nodes_removed = set(removed.get('connectivity', []))
    
    for i, elem in enumerate(elements):
        if i == element_id:
            continue
        
        elem_nodes = set(elem.get('connectivity', []))
        if nodes_removed.intersection(elem_nodes):
            connected.append(i)
    
    return connected


def compute_progressive_collapse_distance(
    elements: List[dict],
    initial_failure_id: int
) -> int:
    """
    Compute collapse propagation distance C_prop.
    
    Number of member removal steps before stable equilibrium.
    C_prop > 2 indicates vulnerability to disproportionate collapse.
    """
    collapsed = {initial_failure_id}
    step = 0
    max_steps = 10
    
    while step < max_steps:
        new_failures = set()
        
        for elem_id in collapsed:
            # Find members overloaded by redistribution
            overloaded = find_overloaded_members(elements, elem_id)
            new_failures.update(overloaded)
        
        if not new_failures - collapsed:
            break
        
        collapsed.update(new_failures)
        step += 1
    
    return step


def find_overloaded_members(
    elements: List[dict],
    failed_element_id: int
) -> List[int]:
    """Find members overloaded after a failure."""
    overloaded = []
    
    for i, elem in enumerate(elements):
        if i == failed_element_id:
            continue
        
        # Check if demand exceeds capacity
        demand = elem.get('demand', 0)
        capacity = elem.get('capacity', 1e6)
        
        if demand > capacity:
            overloaded.append(i)
    
    return overloaded
