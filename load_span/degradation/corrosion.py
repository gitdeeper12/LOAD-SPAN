"""ISO 9224 corrosion rate model for structural steel."""

import numpy as np
from typing import Dict, Optional


class CorrosionModel:
    """
    Corrosion degradation model per ISO 9224.
    
    Models section loss due to atmospheric corrosion.
    Corrosion categories: C1 (very low) to C5 (very high)
    """
    
    # Corrosion rates (μm/year) per ISO 9224 for carbon steel
    CORROSION_RATES = {
        'C1': 1.0,      # Very low
        'C2': 5.0,      # Low
        'C3': 20.0,     # Medium
        'C4': 50.0,     # High
        'C5': 80.0,     # Very high
        'CX': 120.0,    # Extreme
    }
    
    def __init__(self, category: str = 'C3'):
        self.category = category
        self.rate = self.CORROSION_RATES.get(category, 20.0)  # μm/year
    
    def compute_section_loss(
        self,
        years: float,
        initial_area: float,
        is_protected: bool = False
    ) -> float:
        """
        Compute cross-sectional area loss due to corrosion.
        
        Args:
            years: Time in service (years)
            initial_area: Initial cross-sectional area (m²)
            is_protected: Whether protective coating is applied
        
        Returns:
            Remaining area (m²)
        """
        # Apply protection factor
        protection_factor = 0.2 if is_protected else 1.0
        
        # Convert corrosion rate from μm/year to m/year
        loss_rate_m = self.rate * 1e-6 * protection_factor
        
        # For a typical section, area loss is proportional to perimeter × loss depth
        # Simplified: area loss = rate × time × effective perimeter factor
        effective_perimeter = np.sqrt(initial_area) * 4  # Approximate perimeter
        
        area_loss = loss_rate_m * years * effective_perimeter
        
        remaining_area = max(0.0, initial_area - area_loss)
        
        return remaining_area
    
    def compute_corrosion_damage_index(
        self,
        years: float,
        initial_area: float,
        critical_area: float
    ) -> float:
        """
        Compute corrosion damage index D_corr.
        
        D_corr = (A_initial - A_remaining) / (A_initial - A_critical)
        """
        remaining = self.compute_section_loss(years, initial_area)
        max_loss = initial_area - critical_area
        
        if max_loss <= 0:
            return 0.0
        
        damage = (initial_area - remaining) / max_loss
        
        return min(damage, 1.0)
    
    def get_corrosion_category(self, environment: str) -> str:
        """Get corrosion category based on environment description."""
        mapping = {
            'indoor_dry': 'C1',
            'indoor_humid': 'C2',
            'urban': 'C3',
            'industrial': 'C4',
            'coastal': 'C5',
            'marine_industrial': 'CX',
        }
        return mapping.get(environment, 'C3')
    
    def estimate_remaining_service_life(
        self,
        initial_area: float,
        critical_area: float,
        protection_factor: float = 1.0
    ) -> float:
        """
        Estimate remaining service life in years.
        
        T_rem = (A_rem - A_crit) / (dA/dt)
        """
        if critical_area >= initial_area:
            return 0.0
        
        max_loss = initial_area - critical_area
        
        # Annual loss rate
        effective_perimeter = np.sqrt(initial_area) * 4
        annual_loss = self.rate * 1e-6 * effective_perimeter * protection_factor
        
        if annual_loss <= 0:
            return float('inf')
        
        remaining_years = max_loss / annual_loss
        
        return remaining_years
