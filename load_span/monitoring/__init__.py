"""Real-time monitoring dashboard for LOAD-SPAN."""

from load_span.monitoring.app import run_dashboard
from load_span.monitoring.dashboard import create_dashboard

__all__ = ["run_dashboard", "create_dashboard"]
