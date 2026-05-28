"""AI prediction uncertainty quantification."""

import numpy as np
from typing import Tuple


class UncertaintyQuantifier:
    """Quantify uncertainty in AI-assisted predictions."""
    
    MAX_PREDICTION_ERROR = 0.15  # 15% maximum error
    
    def compute_prediction_interval(
        self,
        prediction: float,
        confidence_level: float = 0.95
    ) -> Tuple[float, float]:
        """Compute prediction interval at given confidence level."""
        z_score = 1.96 if confidence_level == 0.95 else 1.64
        std_error = self.MAX_PREDICTION_ERROR * prediction / 3
        
        lower = prediction - z_score * std_error
        upper = prediction + z_score * std_error
        
        return max(0.0, lower), min(1.0, upper)
    
    def compute_var_ai_error(self, n_samples: int = 100) -> float:
        """Compute variance of AI prediction error."""
        # Simulated error variance
        return 0.002  # 0.2% variance
