@echo off
REM Quick launcher for Pogadane Installer
REM Double-click this file to start the installation

echo ========================================
echo   Pogadane Installer
echo ========================================
echo.
echo Starting installer...
echo.

python install.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Error: Installation failed
    echo ========================================
    echo.
    echo Possible causes:
    echo - Python not installed or not in PATH
    echo - Not running from pogadane directory
    echo.
    echo Please ensure:
    echo 1. Python 3.7+ is installed
    echo 2. You are in the pogadane directory
    echo.
    pause
)
