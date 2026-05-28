"""Tests for Fatigue Accumulation and Reliability Module."""

import pytest
from load_span.modules.farm import FatigueAndReliabilityModule


class TestFARM:
    """Test suite for FARM."""
    
    def setup_method(self):
        """Setup before each test."""
        self.farm = FatigueAndReliabilityModule()
        self.farm.configure(d_limit=0.80, d_crit=1.00, sn_class="FAT90")
    
    def test_compute_returns_dict(self):
        """Test compute method returns dictionary."""
        result = self.farm.compute()
        assert isinstance(result, dict)
        assert 'd_fatigue_max' in result
        assert 'beta_augmented' in result
    
    def test_fatigue_damage_non_negative(self):
        """Test fatigue damage is non-negative."""
        result = self.farm.compute()
        assert result['d_fatigue_max'] >= 0.0
    
    def test_warning_trigger(self):
        """Test warning trigger logic."""
        result = self.farm.compute()
        assert 'warning_triggered' in result
        assert isinstance(result['warning_triggered'], bool)
    
    def test_remaining_life_non_negative(self):
        """Test remaining life is non-negative."""
        result = self.farm.compute()
        assert result['remaining_life_days'] >= 0.0
