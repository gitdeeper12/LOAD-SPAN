"""Governance signal status panel."""

import streamlit as st


def render_signal_panel(signal: str, lsii: float):
    """Render safety signal panel."""
    colors = {
        "STEADY_STATE": "green",
        "MONITORING_PHASE_1": "orange",
        "MITIGATION_PHASE_2": "orange",
        "CRITICAL_BREACH": "red"
    }
    
    icons = {
        "STEADY_STATE": "🟢",
        "MONITORING_PHASE_1": "🟠",
        "MITIGATION_PHASE_2": "🟠",
        "CRITICAL_BREACH": "🔴"
    }
    
    st.markdown(f"""
    <div style="background-color: {colors.get(signal, 'gray')}20; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="font-size: 48px;">{icons.get(signal, '⚪')}</h1>
        <h2>{signal.replace('_', ' ')}</h2>
        <p>LSII = {lsii:.3f}</p>
    </div>
    """, unsafe_allow_html=True)
