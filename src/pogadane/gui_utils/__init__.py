"""
GUI utility modules for Pogadane application.

This package contains helper classes for GUI components:
- FontManager: Font settings and dynamic font scaling
- ResultsManager: Processed results storage and display
"""

from .font_manager import FontManager
from .results_manager import ResultsManager

__all__ = ["FontManager", "ResultsManager"]
