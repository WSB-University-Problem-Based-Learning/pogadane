#!/usr/bin/env python3
"""
Pogadane - GUI Launcher

Simple launcher script. You can also run:
  - python -m pogadane
  - pogadane-gui (after pip install)
"""

import sys
from pathlib import Path

# Add src to path for running from source
src_path = Path(__file__).parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import flet as ft
    from pogadane.gui_flet import main
    
    print("Launching Pogadane...")
    ft.app(target=main)
