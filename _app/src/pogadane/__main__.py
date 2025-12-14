"""
Pogadane - Main entry point for running as a module

This allows running Pogadane with: python -m pogadane
"""

import sys


def main():
    """Main entry point - launches the GUI."""
    try:
        from .gui_flet import main as gui_main
        import flet as ft
        
        print("Launching Pogadane - Material 3 Expressive GUI...")
        ft.app(target=gui_main)
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("\nPlease ensure Flet is installed:")
        print("  pip install flet>=0.24.0")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching Pogadane: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
