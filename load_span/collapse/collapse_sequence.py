"""Progressive collapse sequence tracking and analysis."""

from typing import List, Dict, Set, Tuple
import numpy as np


class ProgressiveCollapseAnalyzer:
    """
    Progressive collapse sequence analyzer.
    
    Tracks iterative failure propagation through structure.
    """
    
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.history = []
    
    def analyze_sequence(
        self,
        elements: List[Dict],
        initial_failure_id: int,
        loads: np.ndarray
    ) -> Dict:
        """
        Analyze progressive collapse sequence.
        
        Returns:
            Dictionary with collapse propagation distance and final state
        """
        failed_members = {initial_failure_id}
        collapse_sequence = [(0, [initial_failure_id])]
        
        for step in range(1, self.max_iterations + 1):
            # Identify new failures from redistribution
            new_failures = self._identify_new_failures(
                elements, failed_members, loads
            )
            
            if not new_failures:
                # Stable configuration reached
                collapse_sequence.append((step, list(new_failures)))
                break
            
            failed_members.update(new_failures)
            collapse_sequence.append((step, list(new_failures)))
            
            # Check for complete collapse
            if len(failed_members) >= len(elements):
                collapse_sequence.append((step, ["COMPLETE_COLLAPSE"]))
                break
        
        # Determine final state
        propagation_distance = len(collapse_sequence) - 1
        
        if propagation_distance == 0:
            final_state = "STABLE_LOCAL_DAMAGE"
        elif propagation_distance <= 2:
            final_state = "LIMITED_PROPAGATION"
        elif propagation_distance <= 5:
            final_state = "EXTENSIVE_COLLAPSE"
        else:
            final_state = "DISPROPORTIONATE_COLLAPSE"
        
        # Check vulnerability per LOAD-SPAN criteria
        # C_prop > 2 indicates vulnerable to disproportionate collapse
        vulnerable = propagation_distance > 2
        
        return {
            "propagation_distance": propagation_distance,
            "total_failures": len(failed_members),
            "collapse_sequence": collapse_sequence,
            "final_state": final_state,
            "vulnerable_to_disproportionate_collapse": vulnerable,
            "final_failed_members": list(failed_members)
        }
    
    def _identify_new_failures(
        self,
        elements: List[Dict],
        existing_failures: Set[int],
        loads: np.ndarray
    ) -> Set[int]:
        """Identify members that fail after redistribution."""
        new_failures = set()
        
        for i, element in enumerate(elements):
            if i in existing_failures:
                continue
            
            # Compute redistributed demand
            demand = self._compute_redistributed_demand(i, existing_failures, loads)
            capacity = element.get('capacity', 1.0e6)
            
            if demand > capacity:
                new_failures.add(i)
        
        return new_failures
    
    def _compute_redistributed_demand(
        self,
        member_id: int,
        existing_failures: Set[int],
        loads: np.ndarray
    ) -> float:
        """Compute redistributed load demand on a member."""
        # Simplified redistribution model
        base_demand = 0.8e6  # Base load (N)
        failure_factor = 1.0 + 0.1 * len(existing_failures)
        
        return base_demand * failure_factor
    
    def get_collapse_propagation_distance(self, result: Dict) -> int:
        """Get collapse propagation distance C_prop."""
        return result.get("propagation_distance", 0)
    
    def is_vulnerable(self, result: Dict) -> bool:
        """Check if structure is vulnerable to disproportionate collapse."""
        return result.get("vulnerable_to_disproportionate_collapse", False)
