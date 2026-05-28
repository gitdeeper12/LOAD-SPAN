"""Tests for Euler buckling analysis."""

import pytest
import numpy as np
from load_span.stability.euler_buckling import (
    compute_euler_critical_load,
    compute_dynamic_buckling_threshold,
    compute_critical_load_factor
)


class TestEulerBuckling:
    """Test suite for Euler buckling analysis."""
    
    def test_euler_critical_load_formula(self):
        """Test Euler critical load formula."""
        E = 200e9
        I = 1e-4
        L = 10.0
        K = 1.0
        
        P_cr = compute_euler_critical_load(E, I, L, K)
        
        # P_cr = π²·E·I / (K·L)²
        expected = (np.pi**2 * E * I) / (10.0**2)
        assert abs(P_cr - expected) < 1e-6
    
    def test_dynamic_buckling_reduction(self):
        """Test dynamic buckling reduces critical load."""
        P_euler = 1e6
        gamma = 0.1
        a_max = 0.05
        omega = 1.0
        t = 0
        
        P_dynamic = compute_dynamic_buckling_threshold(P_euler, gamma, a_max, omega, t)
        
        assert P_dynamic <= P_euler
    
    def test_critical_load_factor(self):
        """Test critical load factor computation."""
        P_cr = 2e6
        P_applied = 1e6
        
        lambda_cr = compute_critical_load_factor(P_cr, P_applied)
        
        assert lambda_cr == 2.0
    
    def test_zero_applied_load(self):
        """Test infinite factor for zero applied load."""
        lambda_cr = compute_critical_load_factor(1e6, 0)
        assert lambda_cr == float('inf')
