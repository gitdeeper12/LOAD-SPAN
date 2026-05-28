"""Tests for rainflow cycle counting."""

import pytest
import numpy as np
from load_span.fatigue.rainflow import RainflowCounter


class TestRainflow:
    """Test suite for rainflow cycle counting."""
    
    def setup_method(self):
        """Setup before each test."""
        self.counter = RainflowCounter()
    
    def test_constant_amplitude(self):
        """Test constant amplitude sinusoid."""
        t = np.linspace(0, 10, 1000)
        stress = 100e6 * np.sin(2 * np.pi * t)
        
        cycles = self.counter.count(stress)
        
        assert len(cycles) > 0
        for amp, count in cycles:
            assert amp > 0
            assert count > 0
    
    def test_extract_turning_points(self):
        """Test turning point extraction."""
        data = np.array([0, 1, 2, 1, 0, -1, -2, -1, 0])
        turning = self.counter._extract_turning_points(data)
        
        assert len(turning) >= 3
    
    def test_empty_input(self):
        """Test empty input handling."""
        cycles = self.counter.count(np.array([]))
        assert cycles == []
    
    def test_single_point(self):
        """Test single point input."""
        cycles = self.counter.count(np.array([100]))
        assert cycles == []
