@echo off
cd /d "%~dp0"
if exist "_app\.venv\Scripts\python.exe" (
    _app\.venv\Scripts\python.exe -m pogadane
) else (
    python -m pogadane
)
