"""Palmgren-Miner linear damage accumulation."""

import numpy as np
from typing import List, Tuple


class PalmgrenMiner:
    """
    Palmgren-Miner linear damage accumulation.
    
    D(t) = Σ [n_i(t) / N_i(Δσ_i)]
    
    Failure occurs when D = 1.0 (theoretical)
    Warning threshold D_allowable = 0.80 (20% safety margin)
    """
    
    D_ALLOWABLE = 0.80
    D_CRITICAL = 1.00
    
    def __init__(self, sn_curve):
        self.sn_curve = sn_curve
    
    def accumulate(
        self,
        cycles: List[Tuple[float, int]]
    ) -> float:
        """
        Accumulate fatigue damage.
        
        Args:
            cycles: List of (stress_amplitude, count) from rainflow counting
        
        Returns:
            Miner sum D(t)
        """
        d_total = 0.0
        
        for delta_sigma, n_i in cycles:
            # Get cycles to failure at this amplitude
            n_f = self.sn_curve.get_cycles_to_failure(delta_sigma)
            
            if n_f > 0:
                d_total += n_i / n_f
        
        return min(d_total, 2.0)  # Cap at 2.0 for numerical stability
    
    def compute_remaining_life(self, d_current: float) -> float:
        """
        Compute remaining life fraction.
        
        Returns:
            Remaining life factor (1 - D/D_critical)
        """
        if d_current >= self.D_CRITICAL:
            return 0.0
        
        return (self.D_CRITICAL - d_current) / self.D_CRITICAL


class SNCurve:
    """
    S-N curve for fatigue design.
    
    log(N_f) = log(C) - m·log(Δσ)
    
    FAT classes per Eurocode 3 EN 1993-1-9.
    """
    
    # FAT class constants (Δσ_c in MPa at 2 million cycles)
    FAT_CLASSES = {
        'FAT36': {'sigma_c': 36e6, 'm': 3},
        'FAT40': {'sigma_c': 40e6, 'm': 3},
        'FAT45': {'sigma_c': 45e6, 'm': 3},
        'FAT50': {'sigma_c': 50e6, 'm': 3},
        'FAT56': {'sigma_c': 56e6, 'm': 3},
        'FAT63': {'sigma_c': 63e6, 'm': 3},
        'FAT71': {'sigma_c': 71e6, 'm': 3},
        'FAT80': {'sigma_c': 80e6, 'm': 3},
        'FAT90': {'sigma_c': 90e6, 'm': 3},
        'FAT100': {'sigma_c': 100e6, 'm': 3},
        'FAT112': {'sigma_c': 112e6, 'm': 3},
        'FAT125': {'sigma_c': 125e6, 'm': 3},
        'FAT140': {'sigma_c': 140e6, 'm': 3},
        'FAT160': {'sigma_c': 160e6, 'm': 3},
    }
    
    def __init__(self, fat_class: str = 'FAT90'):
        if fat_class not in self.FAT_CLASSES:
            raise ValueError(f"Unknown FAT class: {fat_class}")
        
        self.fat_class = fat_class
        self.sigma_c = self.FAT_CLASSES[fat_class]['sigma_c']
        self.m = self.FAT_CLASSES[fat_class]['m']
        
        # Constant C = (Δσ_c)^m × 2e6
        self.C = (self.sigma_c ** self.m) * 2e6
    
    def get_cycles_to_failure(self, delta_sigma: float) -> float:
        """
        Get number of cycles to failure at given stress range.
        
        N_f = C / (Δσ)^m
        """
        if delta_sigma <= 0:
            return float('inf')
        
        return self.C / (delta_sigma ** self.m)
    
    def get_detail_category(self) -> str:
        """Get the detail category string."""
        return self.fat_class
