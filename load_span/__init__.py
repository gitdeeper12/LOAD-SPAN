"""LOAD-SPAN: Dynamic Load Redistribution Analysis for Long-Span Structures.

LOAD-SPAN is a structural mechanics framework for dynamic load redistribution
analysis and stability assessment in long-span structures, incorporating an
AI-assisted analytical support layer as a bounded auxiliary tool.
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__license__ = "MIT"
__doi__ = "10.5281/zenodo.20422430"

from load_span.pipeline import LoadSpanAssessor
from load_span.lsii import LongSpanIntegrityIndex

__all__ = [
    "LoadSpanAssessor",
    "LongSpanIntegrityIndex",
]
