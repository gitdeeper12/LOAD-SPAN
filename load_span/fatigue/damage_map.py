"""Spatial fatigue damage distribution mapping."""

import numpy as np
from typing import Dict, List, Tuple


class FatigueDamageMap:
    """Spatial distribution of fatigue damage across structure."""
    
    def __init__(self, n_nodes: int = 100):
        self.damage_values = np.zeros(n_nodes)
        self.node_coordinates = None
    
    def set_damage_at_node(self, node_id: int, damage: float):
        """Set fatigue damage at a specific node."""
        self.damage_values[node_id] = damage
    
    def interpolate_damage(self, coordinates: np.ndarray) -> np.ndarray:
        """Interpolate damage at given coordinates."""
        # Linear interpolation between nodes
        return np.interp(coordinates, self.node_coordinates, self.damage_values)
    
    def get_hotspots(self, threshold: float = 0.5) -> List[int]:
        """Identify fatigue hotspots (nodes above threshold)."""
        return np.where(self.damage_values > threshold)[0].tolist()
    
    def compute_average_damage(self) -> float:
        """Compute average fatigue damage across structure."""
        return float(np.mean(self.damage_values))
