"""Streamlit application entry point for LOAD-SPAN dashboard."""

import streamlit as st


def run_dashboard():
    """Launch the LOAD-SPAN monitoring dashboard."""
    st.set_page_config(
        page_title="LOAD-SPAN Dashboard",
        page_icon="🏗️",
        layout="wide"
    )
    
    st.title("LOAD-SPAN Structural Health Monitoring")
    st.markdown("### Long-Span Structural Integrity Index (LSII)")
    
    # Placeholder for dashboard content
    st.info("Dashboard components loaded. Use create_dashboard() for full interface.")


if __name__ == "__main__":
    run_dashboard()
