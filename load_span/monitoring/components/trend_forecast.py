"""LSII trajectory forecast component."""

import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict


def render_forecast_chart(forecast_data: List[Dict]):
    """Render LSII forecast with uncertainty bands."""
    hours = [f["hours"] for f in forecast_data]
    lsii = [f["lsii"] for f in forecast_data]
    lower = [f["lower"] for f in forecast_data]
    upper = [f["upper"] for f in forecast_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=lsii,
        mode="lines",
        name="Forecast",
        line=dict(color="blue", width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=hours + hours[::-1],
        y=upper + lower[::-1],
        fill="toself",
        fillcolor="rgba(0, 100, 255, 0.2)",
        line=dict(color="rgba(255,255,255,0)"),
        name="95% Confidence"
    ))
    
    fig.add_hline(y=0.90, line_dash="dash", line_color="green")
    fig.add_hline(y=0.65, line_dash="dash", line_color="red")
    
    fig.update_layout(
        title="LSII 48-Hour Forecast",
        xaxis_title="Hours Ahead",
        yaxis_title="LSII",
        yaxis_range=[0, 1]
    )
    
    st.plotly_chart(fig, use_container_width=True)
