"""LSII composite index gauge display component."""

import streamlit as st
import plotly.graph_objects as go


def render_lsii_gauge(lsii_value: float):
    """Render LSII gauge widget."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=lsii_value,
        delta={"reference": 0.90, "increasing": {"color": "green"}},
        gauge={
            "axis": {"range": [0, 1], "tickwidth": 1},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 0.65], "color": "red"},
                {"range": [0.65, 0.75], "color": "orange"},
                {"range": [0.75, 0.90], "color": "yellow"},
                {"range": [0.90, 1.0], "color": "green"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": lsii_value
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
