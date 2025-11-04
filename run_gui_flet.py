#!/usr/bin/env python3
"""
Pogadane - Material 3 Expressive GUI Launcher
Launch the beautiful Material Design 3 interface powered by Flet
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Launch Material 3 Expressive GUI
import flet as ft
from pogadane.gui_flet import main

if __name__ == "__main__":
    print("🎧 Launching Pogadane - Material 3 Expressive GUI...")
    ft.app(target=main)
