"""Tests for main LOAD-SPAN pipeline."""

import pytest
from load_span.pipeline import LoadSpanAssessor
from load_span.lsii import SafetySignal


class TestPipeline:
    """Test suite for LoadSpanAssessor."""
    
    def setup_method(self):
        """Setup before each test."""
        self.assessor = LoadSpanAssessor()
    
    def test_evaluate_returns_result(self):
        """Test evaluate method returns result."""
        result = self.assessor.evaluate()
        
        assert hasattr(result, 'lsii_result')
        assert hasattr(result, 'redistribution')
        assert hasattr(result, 'stability')
        assert hasattr(result, 'fatigue')
        assert hasattr(result, 'ai_alerts')
        assert hasattr(result, 'collapse_risk')
    
    def test_lsii_in_bounds(self):
        """Test LSII is within bounds."""
        result = self.assessor.evaluate()
        lsii = result.lsii_result.lsii
        
        assert 0.0 <= lsii <= 1.0
    
    def test_safety_signal_is_valid(self):
        """Test safety signal is a valid enum member."""
        result = self.assessor.evaluate()
        signal = result.lsii_result.signal
        
        assert signal in SafetySignal
    
    def test_collapse_risk_in_bounds(self):
        """Test collapse risk is within bounds."""
        result = self.assessor.evaluate()
        
        assert 0.0 <= result.collapse_risk <= 1.0
    
    def test_get_safety_signal(self):
        """Test get_safety_signal method."""
        signal = self.assessor.get_safety_signal()
        
        assert signal in SafetySignal
