"""β index and P_f trend panel."""

import plotly.graph_objects as go
import numpy as np


def create_reliability_trend(beta_history: list, target_beta: float = 3.8):
    """Create reliability index trend plot."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(beta_history))),
        y=beta_history,
        mode="lines+markers",
        name="β (t)",
        line=dict(color="blue", width=2)
    ))
    
    fig.add_hline(y=target_beta, line_dash="dash", line_color="green", annotation_text="Target β=3.8")
    fig.add_hline(y=1.5, line_dash="dash", line_color="red", annotation_text="Critical β=1.5")
    
    fig.update_layout(
        title="Reliability Index Evolution",
        xaxis_title="Time Step",
        yaxis_title="β (Reliability Index)"
    )
    
    return fig
