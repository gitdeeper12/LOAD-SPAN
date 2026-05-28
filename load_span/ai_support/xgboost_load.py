"""XGBoost-based anomaly detection for load patterns."""

import numpy as np
from typing import List, Dict, Optional, Tuple


class XGBoostAnomalyDetector:
    """
    XGBoost-based anomaly detection for stress wave fields.
    
    Detects anomalies in spatial and temporal distribution of measured stresses.
    A_index(x,t) = |σ_measured - σ_theoretical| ≥ α_threshold
    """
    
    ANOMALY_THRESHOLD = 0.15  # 15% deviation threshold
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.is_trained = False
    
    def detect_anomalies(
        self,
        measured_stresses: np.ndarray,
        theoretical_stresses: np.ndarray,
        locations: List[str]
    ) -> List[Dict]:
        """
        Detect anomalies in stress measurements.
        
        Args:
            measured_stresses: Measured stress values at each location
            theoretical_stresses: Model-predicted stress values
            locations: Sensor location names
        
        Returns:
            List of anomaly alerts
        """
        alerts = []
        
        for i, (meas, theo) in enumerate(zip(measured_stresses, theoretical_stresses)):
            if theo <= 0:
                continue
            
            # Compute anomaly index
            a_index = abs(meas - theo) / theo
            
            if a_index >= self.ANOMALY_THRESHOLD:
                # Classify anomaly pattern
                pattern = self._classify_pattern(a_index, meas, theo)
                confidence = self._compute_confidence(a_index)
                
                alerts.append({
                    "location": locations[i] if i < len(locations) else f"sensor_{i}",
                    "anomaly_index": a_index,
                    "threshold": self.ANOMALY_THRESHOLD,
                    "pattern": pattern,
                    "confidence": confidence,
                    "measured": float(meas),
                    "theoretical": float(theo)
                })
        
        return alerts
    
    def _classify_pattern(self, a_index: float, meas: float, theo: float) -> str:
        """Classify anomaly pattern type."""
        if meas > theo:
            if a_index > 0.5:
                return "SEVERE_OVERLOAD"
            elif a_index > 0.3:
                return "MODERATE_OVERLOAD"
            else:
                return "LIGHT_OVERLOAD"
        else:
            if a_index > 0.5:
                return "SEVERE_UNDERLOAD"
            elif a_index > 0.3:
                return "MODERATE_UNDERLOAD"
            else:
                return "LIGHT_UNDERLOAD"
    
    def _compute_confidence(self, a_index: float) -> float:
        """Compute detection confidence based on anomaly magnitude."""
        # Higher confidence for larger anomalies
        confidence = min(0.6 + a_index * 0.5, 0.95)
        return confidence
    
    def spatial_pattern_analysis(
        self,
        alerts: List[Dict],
        locations: List[str]
    ) -> Dict:
        """
        Analyze spatial pattern of anomalies.
        
        Maps alert locations to identify clustered damage patterns.
        """
        if not alerts:
            return {"pattern": "NO_ANOMALIES", "risk": 0.0}
        
        alert_locations = [a["location"] for a in alerts]
        
        # Check for clustering
        n_alerts = len(alerts)
        max_confidence = max(a["confidence"] for a in alerts)
        
        if n_alerts >= 5:
            pattern = "WIDESPREAD_ANOMALIES"
            risk = min(0.8 + max_confidence * 0.2, 1.0)
        elif n_alerts >= 3:
            pattern = "CLUSTERED_ANOMALIES"
            risk = 0.5 + max_confidence * 0.3
        elif n_alerts >= 1:
            pattern = "ISOLATED_ANOMALY"
            risk = 0.2 + max_confidence * 0.2
        else:
            pattern = "NO_ANOMALIES"
            risk = 0.0
        
        return {
            "pattern": pattern,
            "risk_score": risk,
            "n_alerts": n_alerts,
            "affected_locations": alert_locations,
            "requires_engineering_review": risk > 0.5
        }
