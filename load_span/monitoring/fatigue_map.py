"""Spatial fatigue damage map renderer."""

import plotly.graph_objects as go
import numpy as np


def create_fatigue_damage_map(damage_values: np.ndarray, node_coordinates: np.ndarray):
    """Create spatial heatmap of fatigue damage distribution."""
    fig = go.Figure(data=go.Heatmap(
        z=damage_values.reshape(int(np.sqrt(len(damage_values))), -1),
        colorscale="Viridis",
        zmin=0,
        zmax=1,
        colorbar_title="Fatigue Damage D(t)"
    ))
    
    fig.update_layout(
        title="Spatial Fatigue Damage Distribution",
        xaxis_title="Span Position",
        yaxis_title="Width"
    )
    
    return fig
