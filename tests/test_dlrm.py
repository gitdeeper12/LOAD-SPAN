"""Tests for Dynamic Load Redistribution Module."""

import pytest
from load_span.modules.dlrm import DynamicLoadRedistributionModule


class TestDLRM:
    """Test suite for DLRM."""
    
    def setup_method(self):
        """Setup before each test."""
        self.dlrm = DynamicLoadRedistributionModule()
        self.dlrm.configure(redundancy_min=0.70, redistribution_warn=0.20)
    
    def test_analyze_returns_dict(self):
        """Test analyze method returns dictionary."""
        result = self.dlrm.analyze()
        assert isinstance(result, dict)
        assert 'r_struct' in result
        assert 'max_dcr' in result
    
    def test_redundancy_index_range(self):
        """Test redundancy index is between 0 and 1."""
        result = self.dlrm.analyze()
        assert 0.0 <= result['r_struct'] <= 1.0
    
    def test_max_dcr_non_negative(self):
        """Test max DCR is non-negative."""
        result = self.dlrm.analyze()
        assert result['max_dcr'] >= 0.0
