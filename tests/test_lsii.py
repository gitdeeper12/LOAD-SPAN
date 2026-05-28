"""Tests for LSII composite index computation."""

import pytest
from load_span.lsii import LongSpanIntegrityIndex, SafetySignal


class TestLSII:
    """Test suite for LongSpanIntegrityIndex."""
    
    def setup_method(self):
        """Setup before each test."""
        self.lsii = LongSpanIntegrityIndex()
    
    def test_steady_state(self):
        """Test steady state classification."""
        result = self.lsii.compute(
            beta=4.5,
            d_fatigue=0.30,
            r_struct=0.85,
            lambda_cr=2.5
        )
        assert result.lsii >= 0.90
        assert result.signal == SafetySignal.STEADY_STATE
    
    def test_monitoring_phase(self):
        """Test monitoring phase classification."""
        result = self.lsii.compute(
            beta=3.2,
            d_fatigue=0.60,
            r_struct=0.72,
            lambda_cr=1.8
        )
        assert 0.75 <= result.lsii < 0.90
        assert result.signal == SafetySignal.MONITORING_PHASE_1
    
    def test_mitigation_phase(self):
        """Test mitigation phase classification."""
        result = self.lsii.compute(
            beta=2.0,
            d_fatigue=0.75,
            r_struct=0.60,
            lambda_cr=1.4
        )
        assert 0.65 <= result.lsii < 0.75
        assert result.signal == SafetySignal.MITIGATION_PHASE_2
    
    def test_critical_breach(self):
        """Test critical breach classification."""
        result = self.lsii.compute(
            beta=1.0,
            d_fatigue=0.95,
            r_struct=0.40,
            lambda_cr=0.8
        )
        assert result.lsii < 0.65
        assert result.signal == SafetySignal.CRITICAL_BREACH
    
    def test_lsii_bounds(self):
        """Test LSII stays within [0, 1] bounds."""
        result = self.lsii.compute(
            beta=10.0,
            d_fatigue=-0.5,
            r_struct=2.0,
            lambda_cr=5.0
        )
        assert 0.0 <= result.lsii <= 1.0
    
    def test_governance_action(self):
        """Test governance action retrieval."""
        action = self.lsii.get_governance_action(SafetySignal.STEADY_STATE)
        assert "Continuous monitoring" in action
        
        action = self.lsii.get_governance_action(SafetySignal.CRITICAL_BREACH)
        assert "Immediate closure" in action
