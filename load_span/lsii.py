"""Long-Span Structural Integrity Index (LSII) composite metric."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SafetySignal(Enum):
    """Four-level governance safety signals."""
    STEADY_STATE = "🟢 STEADY_STATE"
    MONITORING_PHASE_1 = "🟠 MONITORING_PHASE_1"
    MITIGATION_PHASE_2 = "🟠 MITIGATION_PHASE_2"
    CRITICAL_BREACH = "🔴 CRITICAL_BREACH"


@dataclass
class LSIIResult:
    """LSII assessment result container."""
    lsii: float
    signal: SafetySignal
    beta: float              # Cornell-Hasofer-Lind reliability index
    d_fatigue_max: float     # Maximum Palmgren-Miner damage
    lambda_cr: float         # Critical load factor (Euler-Riks)
    r_struct: float          # Structural redundancy index


class LongSpanIntegrityIndex:
    """
    Long-Span Structural Integrity Index (LSII) composite metric.
    
    LSII = 0.35·(β/β_target) + 0.30·(1−D_fatigue) + 0.20·R_struct + 0.15·(λ_cr/λ_target)
    
    Where:
    - β: Cornell-Hasofer-Lind reliability index (target β_target = 3.8)
    - D_fatigue: Maximum Miner damage across all connections
    - R_struct: Structural redundancy index
    - λ_cr: Critical load factor (target λ_target = 2.0)
    """
    
    BETA_TARGET = 3.8
    LAMBDA_TARGET = 2.0
    D_LIMIT = 0.80
    
    # Weighting coefficients
    W_BETA = 0.35
    W_FATIGUE = 0.30
    W_REDUNDANCY = 0.20
    W_STABILITY = 0.15
    
    # Thresholds
    STEADY_THRESHOLD = 0.90
    MONITORING_THRESHOLD = 0.75
    MITIGATION_THRESHOLD = 0.65
    
    def compute(
        self,
        beta: float,
        d_fatigue: float,
        r_struct: float,
        lambda_cr: float
    ) -> LSIIResult:
        """
        Compute LSII composite index.
        
        Args:
            beta: Reliability index
            d_fatigue: Maximum fatigue damage (Miner sum)
            r_struct: Structural redundancy index
            lambda_cr: Critical load factor
            
        Returns:
            LSIIResult with composite score and safety signal
        """
        # Normalized components
        beta_norm = min(beta / self.BETA_TARGET, 1.0)
        fatigue_norm = max(1.0 - d_fatigue / self.D_LIMIT, 0.0)
        lambda_norm = min(lambda_cr / self.LAMBDA_TARGET, 1.0)
        
        # Weighted composite
        lsii = (
            self.W_BETA * beta_norm +
            self.W_FATIGUE * fatigue_norm +
            self.W_REDUNDANCY * r_struct +
            self.W_STABILITY * lambda_norm
        )
        
        # Bound LSII to [0, 1]
        lsii = max(0.0, min(lsii, 1.0))
        
        # Determine safety signal
        if lsii >= self.STEADY_THRESHOLD:
            signal = SafetySignal.STEADY_STATE
        elif lsii >= self.MONITORING_THRESHOLD:
            signal = SafetySignal.MONITORING_PHASE_1
        elif lsii >= self.MITIGATION_THRESHOLD:
            signal = SafetySignal.MITIGATION_PHASE_2
        else:
            signal = SafetySignal.CRITICAL_BREACH
        
        return LSIIResult(
            lsii=lsii,
            signal=signal,
            beta=beta,
            d_fatigue_max=d_fatigue,
            lambda_cr=lambda_cr,
            r_struct=r_struct
        )
    
    def get_governance_action(self, signal: SafetySignal) -> str:
        """Get governance action based on safety signal."""
        actions = {
            SafetySignal.STEADY_STATE: "Continuous monitoring, standard schedule",
            SafetySignal.MONITORING_PHASE_1: "Enhanced monitoring; targeted inspection",
            SafetySignal.MITIGATION_PHASE_2: "Operational load restriction; immediate review",
            SafetySignal.CRITICAL_BREACH: "Immediate closure; exclusion zone; emergency assessment"
        }
        return actions.get(signal, "Unknown signal")
