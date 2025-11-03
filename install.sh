#!/bin/bash
# Quick launcher for Pogadane Installer
# Run: bash install.sh or ./install.sh (after chmod +x install.sh)

echo "========================================"
echo "  Pogadane Installer"
echo "========================================"
echo ""
echo "Starting installer..."
echo ""

python3 install.py

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  Error: Installation failed"
    echo "========================================"
    echo ""
    echo "Possible causes:"
    echo "- Python 3.7+ not installed"
    echo "- Not running from pogadane directory"
    echo ""
    echo "Please ensure:"
    echo "1. Python 3.7+ is installed (try: python3 --version)"
    echo "2. You are in the pogadane directory"
    echo ""
    read -p "Press Enter to continue..."
fi
