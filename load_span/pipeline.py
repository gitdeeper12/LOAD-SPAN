"""LOAD-SPAN main assessment pipeline."""

from dataclasses import dataclass
from typing import Optional, Dict, Any

import numpy as np

from load_span.lsii import LongSpanIntegrityIndex, LSIIResult, SafetySignal
from load_span.modules.dlrm import DynamicLoadRedistributionModule
from load_span.modules.lssam import LongSpanStabilityModule
from load_span.modules.farm import FatigueAndReliabilityModule
from load_span.modules.aisl import AISupportLayer


@dataclass
class PipelineResult:
    """Complete pipeline assessment result."""
    lsii_result: LSIIResult
    redistribution: Dict[str, float]
    stability: Dict[str, float]
    fatigue: Dict[str, float]
    ai_alerts: list
    collapse_risk: float


class LoadSpanAssessor:
    """
    Main LOAD-SPAN assessment pipeline.
    
    Integrates DLRM, LSSAM, FARM, and AISL modules into a continuous
    structural health assessment framework.
    """
    
    def __init__(
        self,
        span_config: Optional[Dict] = None,
        sensor_stream: str = "live",
        modules: Optional[Dict] = None
    ):
        self.span_config = span_config or {}
        self.sensor_stream = sensor_stream
        
        # Initialize modules
        self.dlrm = DynamicLoadRedistributionModule()
        self.lssam = LongSpanStabilityModule()
        self.farm = FatigueAndReliabilityModule()
        self.aisl = AISupportLayer()
        self.lsii = LongSpanIntegrityIndex()
        
        # Override module configs if provided
        if modules:
            if "dlrm" in modules:
                self.dlrm.configure(**modules["dlrm"])
            if "lssam" in modules:
                self.lssam.configure(**modules["lssam"])
            if "farm" in modules:
                self.farm.configure(**modules["farm"])
            if "aisl" in modules:
                self.aisl.configure(**modules["aisl"])
    
    def evaluate(self) -> PipelineResult:
        """
        Run full LOAD-SPAN assessment pipeline.
        
        Returns:
            PipelineResult with complete assessment data
        """
        # Run DLRM: Dynamic load redistribution analysis
        redistribution_result = self.dlrm.analyze()
        
        # Run LSSAM: Stability assessment
        stability_result = self.lssam.assess()
        
        # Run FARM: Fatigue and reliability
        fatigue_result = self.farm.compute()
        
        # Run AISL: Anomaly detection and forecasting
        ai_alerts = self.aisl.detect_anomalies()
        lsii_forecast = self.aisl.forecast_lsii(horizon_hours=48)
        
        # Compute LSII composite index
        lsii_result = self.lsii.compute(
            beta=stability_result.get("beta", 3.5),
            d_fatigue=fatigue_result.get("d_fatigue_max", 0.0),
            r_struct=redistribution_result.get("r_struct", 0.85),
            lambda_cr=stability_result.get("lambda_cr", 2.5)
        )
        
        # Compute collapse risk
        collapse_risk = self._compute_collapse_risk(
            redistribution_result,
            stability_result,
            fatigue_result
        )
        
        return PipelineResult(
            lsii_result=lsii_result,
            redistribution=redistribution_result,
            stability=stability_result,
            fatigue=fatigue_result,
            ai_alerts=ai_alerts,
            collapse_risk=collapse_risk
        )
    
    def _compute_collapse_risk(
        self,
        redistribution: Dict,
        stability: Dict,
        fatigue: Dict
    ) -> float:
        """Compute progressive collapse risk index."""
        # DCR (Demand-to-Capacity Ratio) based risk
        dcr = redistribution.get("max_dcr", 0.5)
        beta = stability.get("beta", 3.5)
        d_fatigue = fatigue.get("d_fatigue_max", 0.0)
        
        # Risk increases with DCR and fatigue damage, decreases with beta
        risk = (dcr / 2.0) * (1.0 + d_fatigue) * np.exp(-beta / 5.0)
        return min(risk, 1.0)
    
    def get_safety_signal(self) -> SafetySignal:
        """Get current safety governance signal."""
        result = self.evaluate()
        return result.lsii_result.signal
