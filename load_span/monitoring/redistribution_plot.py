"""Internal force redistribution display."""

import plotly.graph_objects as go
import numpy as np


def create_redistribution_plot(forces_before: np.ndarray, forces_after: np.ndarray, member_ids: list):
    """Create bar chart comparing forces before and after redistribution."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=member_ids,
        y=forces_before,
        name="Before Redistribution",
        marker_color="blue"
    ))
    
    fig.add_trace(go.Bar(
        x=member_ids,
        y=forces_after,
        name="After Redistribution",
        marker_color="red"
    ))
    
    fig.update_layout(
        title="Internal Force Redistribution",
        xaxis_title="Member ID",
        yaxis_title="Force (N)",
        barmode="group"
    )
    
    return fig
