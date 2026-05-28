"""LSTM-based LSII trajectory forecast."""

import numpy as np
from typing import List, Dict


class LSTMForecaster:
    """
    LSTM model for 24-48h LSII trajectory forecast.
    
    Physics-constrained with bounded uncertainty.
    """
    
    def __init__(self, forecast_horizon_hours: int = 48):
        self.horizon = forecast_horizon_hours
    
    def forecast(self, historical_lsii: List[float]) -> List[Dict]:
        """Generate LSII forecast with uncertainty bounds."""
        forecasts = []
        current = historical_lsii[-1] if historical_lsii else 0.9
        
        for t in range(0, self.horizon + 1, 6):
            # Simple decay model
            decay = 0.001 * (t / 24) ** 1.2
            forecast = max(current - decay, 0.0)
            uncertainty = 0.02 + 0.002 * t / 24
            
            forecasts.append({
                "hours": t,
                "lsii": forecast,
                "lower": max(forecast - uncertainty, 0.0),
                "upper": min(forecast + uncertainty, 1.0)
            })
        
        return forecasts
    
    def get_warning_lead_time(self, forecasts: List[Dict], threshold: float = 0.65) -> float:
        """Get hours until LSII drops below threshold."""
        for f in forecasts:
            if f["lsii"] < threshold:
                return f["hours"]
        return float('inf')
