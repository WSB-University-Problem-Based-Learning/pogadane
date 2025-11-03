#!/usr/bin/env python3
"""
Pogadane - Material Design GUI Launcher
Launch the modern Material Design interface for Pogadane
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Launch Material Design GUI
from pogadane.gui_material import main

if __name__ == "__main__":
    print("🎧 Launching Pogadane - Material Design GUI...")
    main()
