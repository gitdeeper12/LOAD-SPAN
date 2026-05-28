"""LSII governance dashboard layout and components."""

import streamlit as st
import plotly.graph_objects as go
import numpy as np


def create_dashboard(lsii_value: float, signal: str, metrics: dict):
    """Create full LSII governance dashboard."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # LSII Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=lsii_value,
            title={"text": "LSII Score"},
            gauge={
                "axis": {"range": [0, 1]},
                "bar": {"color": _get_color(lsii_value)},
                "steps": [
                    {"range": [0, 0.65], "color": "red"},
                    {"range": [0.65, 0.75], "color": "orange"},
                    {"range": [0.75, 0.90], "color": "yellow"},
                    {"range": [0.90, 1.0], "color": "green"},
                ]
            }
        ))
        st.plotly_chart(fig)
    
    with col2:
        st.metric("Safety Signal", signal)
        st.metric("β (Reliability)", f"{metrics.get('beta', 0):.2f}")
    
    with col3:
        st.metric("Fatigue Damage", f"{metrics.get('d_fatigue', 0):.3f}")
        st.metric("λ_cr (Buckling)", f"{metrics.get('lambda_cr', 0):.2f}")


def _get_color(lsii: float) -> str:
    if lsii >= 0.90:
        return "green"
    elif lsii >= 0.75:
        return "yellow"
    elif lsii >= 0.65:
        return "orange"
    else:
        return "red"
