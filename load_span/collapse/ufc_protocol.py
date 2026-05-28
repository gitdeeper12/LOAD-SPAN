"""UFC 4-023-03 tie force method for progressive collapse."""

from typing import Dict


class UFCProtocol:
    """
    UFC 4-023-03 tie force method for robustness assessment.
    """
    
    def compute_tie_force_requirements(self, span_length: float, dead_load: float, live_load: float) -> Dict:
        """Compute required tie forces per UFC."""
        # Longitudinal tie force
        F_long = 1.33 * (dead_load + 0.5 * live_load) * span_length
        
        # Transverse tie force
        F_trans = 1.33 * (dead_load + 0.5 * live_load) * span_length / 2
        
        # Vertical tie force
        F_vert = 2.0 * dead_load * span_length
        
        return {
            "longitudinal_tie": F_long,
            "transverse_tie": F_trans,
            "vertical_tie": F_vert
        }
    
    def check_tie_capacity(self, required: float, provided: float) -> bool:
        """Check if provided tie capacity meets requirement."""
        return provided >= required
