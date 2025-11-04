"""
Pogadane - Setup Configuration (Backward Compatibility Shim)

This setup.py is kept for backward compatibility with older tools.
All configuration has been moved to pyproject.toml (PEP 621).

Modern installation:
    pip install -e .                    # Development install
    pip install .                       # Regular install
    pip install -e .[dev]               # With development dependencies
    pip install -e .[test]              # With testing dependencies
    pip install -e .[all]               # With all optional dependencies
    
External binaries installation:
    python tools/install.py             # Install faster-whisper, ollama, etc.

For more information, see pyproject.toml and README.md.
"""

from setuptools import setup

# All configuration is in pyproject.toml
# This setup.py exists only for backward compatibility
setup()
