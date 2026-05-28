"""Span geometry and material definitions for validation."""

from typing import Dict


def get_cable_stayed_bridge_config() -> Dict:
    """Configuration for cable-stayed bridge validation case."""
    return {
        "span_length": 470.0,
        "tower_height": 120.0,
        "n_cables": 32,
        "deck_material": "steel_S355",
        "cable_material": "cable_steel",
        "traffic_load": 50e3,
        "wind_load": 1.5e3
    }


def get_roof_truss_config() -> Dict:
    """Configuration for roof truss validation case."""
    return {
        "span_length": 80.0,
        "truss_depth": 6.0,
        "n_panels": 20,
        "material": "steel_S235",
        "dead_load": 2.5e3,
        "live_load": 5.0e3
    }


def get_suspension_span_config() -> Dict:
    """Configuration for suspension span validation case."""
    return {
        "span_length": 1200.0,
        "cable_sag_ratio": 0.1,
        "deck_width": 28.0,
        "material": "steel_S460",
        "wind_load": 2.5e3
    }
