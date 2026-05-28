#!/bin/bash
# LOAD-SPAN Dashboard Launcher

echo "Starting LOAD-SPAN Dashboard..."
streamlit run load_span/monitoring/app.py --server.port 8501
