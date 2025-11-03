@echo off
REM Quick launcher for Pogadane GUI Installer
REM Double-click this file to start the installation wizard

echo ========================================
echo   Pogadane Installation Wizard
echo ========================================
echo.
echo Starting GUI installer...
echo.

python tools\install_gui.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Error: Installation failed to start
    echo ========================================
    echo.
    echo Possible causes:
    echo - Python not installed or not in PATH
    echo - Not running from pogadane directory
    echo.
    echo Please ensure:
    echo 1. Python 3.7+ is installed
    echo 2. You are in the pogadane directory
    echo 3. Run from Command Prompt if needed
    echo.
    pause
)
