"""GSA 2003 progressive collapse assessment protocol."""

from typing import Dict, List


class GSAProtocol:
    """
    GSA 2003 progressive collapse analysis guidelines.
    
    Implements alternate load path method with load amplification G + 0.25Q.
    """
    
    LOAD_AMPLIFICATION = 1.25  # G + 0.25Q for sudden removal
    
    def check_compliance(self, max_dcr: float) -> Dict:
        """Check GSA compliance."""
        compliant = max_dcr <= 2.0
        
        return {
            "compliant": compliant,
            "max_dcr": max_dcr,
            "limit": 2.0,
            "status": "PASS" if compliant else "FAIL"
        }
    
    def get_removal_categories(self) -> Dict:
        """Get member removal categories per GSA."""
        return {
            "Category_1": "Columns at ground level",
            "Category_2": "Primary beams",
            "Category_3": "Corner columns",
            "Category_4": "Transfer girders"
        }
