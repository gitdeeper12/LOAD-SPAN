"""Canonical v1.0.0 parameter registry for validation."""

from typing import Dict


def get_default_parameters() -> Dict:
    """Get default parameter set for LOAD-SPAN v1.0.0."""
    return {
        "lsii": {
            "beta_target": 3.8,
            "lambda_target": 2.0,
            "d_limit": 0.80,
            "r_struct_target": 0.70,
            "w_beta": 0.35,
            "w_fatigue": 0.30,
            "w_redundancy": 0.20,
            "w_stability": 0.15
        },
        "dlrm": {
            "redundancy_min": 0.70,
            "redistribution_warn": 0.20,
            "max_dcr": 2.0
        },
        "lssam": {
            "lambda_cr_min": 2.0,
            "beta_min": 3.5,
            "gamma_max": 0.15
        },
        "farm": {
            "d_allowable": 0.80,
            "d_critical": 1.00,
            "sn_class": "FAT90"
        },
        "aisl": {
            "forecast_horizon": 48,
            "anomaly_threshold": 0.15,
            "max_ai_correction": 0.05
        }
    }


def get_validation_parameters() -> Dict:
    """Get parameters for validation runs."""
    return {
        "n_simulation_points": 10000,
        "confidence_level": 0.95,
        "tolerance": 1e-6,
        "max_iterations": 100
    }
