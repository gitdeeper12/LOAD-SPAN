"""Traffic, wind, and fatigue loading scenarios for validation."""

import numpy as np
from typing import Dict


def get_traffic_loading_scenario() -> Dict:
    """Traffic loading scenario for cable-stayed bridge."""
    return {
        "daily_vehicles": 50000,
        "truck_fraction": 0.15,
        "peak_hour_factor": 0.1,
        "load_model": "LM1",
        "load_effect": 75e3  # N
    }


def get_wind_loading_scenario() -> Dict:
    """Wind loading scenario for suspension span."""
    return {
        "reference_wind_speed": 40.0,  # m/s
        "terrain_category": "II",
        "turbulence_intensity": 0.12,
        "gust_factor": 1.75
    }


def get_fatigue_loading_scenario() -> Dict:
    """Fatigue loading spectrum for connection details."""
    return {
        "stress_spectrum": [
            (30e6, 100000),
            (50e6, 50000),
            (70e6, 10000),
            (90e6, 1000)
        ],
        "detail_category": "FAT71",
        "cycles_per_year": 5e6
    }
