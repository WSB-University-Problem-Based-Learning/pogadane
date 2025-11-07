# Build Script for Pogadane Executable
# Creates a single-file .exe for Windows distribution

# Prerequisites check
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Pogadane Build Script - Single File Executable Builder" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found in PATH!" -ForegroundColor Red
    exit 1
}

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "  Virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "  WARNING: No virtual environment detected!" -ForegroundColor Yellow
    Write-Host "  Recommended: Activate .venv first" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit 0
    }
}

Write-Host ""

# Install PyInstaller if not present
Write-Host "Checking PyInstaller installation..." -ForegroundColor Yellow
try {
    $pyinstallerVersion = pyinstaller --version 2>&1
    Write-Host "  PyInstaller found: $pyinstallerVersion" -ForegroundColor Green
} catch {
    Write-Host "  PyInstaller not found. Installing..." -ForegroundColor Yellow
    python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR: Failed to install PyInstaller!" -ForegroundColor Red
        exit 1
    }
    Write-Host "  PyInstaller installed successfully" -ForegroundColor Green
}

Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "  Removed build/" -ForegroundColor Green
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "  Removed dist/" -ForegroundColor Green
}

Write-Host ""

# Build the executable
Write-Host "Building Pogadane.exe..." -ForegroundColor Yellow
Write-Host "  This may take 5-10 minutes..." -ForegroundColor Cyan
Write-Host ""

pyinstaller pogadane.spec --clean

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ERROR: Build failed!" -ForegroundColor Red
    Write-Host "  Check the output above for errors" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "  Build completed successfully!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""

# Check output
if (Test-Path "dist\Pogadane.exe") {
    $exeSize = (Get-Item "dist\Pogadane.exe").Length / 1MB
    Write-Host "Executable created: dist\Pogadane.exe" -ForegroundColor Green
    Write-Host "  Size: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Yellow
    Write-Host "  .\dist\Pogadane.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "To distribute:" -ForegroundColor Yellow
    Write-Host "  1. Copy dist\Pogadane.exe to target machine" -ForegroundColor White
    Write-Host "  2. User runs Pogadane.exe (no installation needed)" -ForegroundColor White
    Write-Host "  3. Configuration will be created on first run" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: Users still need to install:" -ForegroundColor Yellow
    Write-Host "  - faster-whisper or whisper (for transcription)" -ForegroundColor White
    Write-Host "  - Ollama (optional, for local AI)" -ForegroundColor White
    Write-Host "  - Or configure Google Gemini API key" -ForegroundColor White
} else {
    Write-Host "  ERROR: Pogadane.exe not found in dist/" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Build artifacts:" -ForegroundColor Cyan
Write-Host "  dist/Pogadane.exe    - Distributable executable" -ForegroundColor White
Write-Host "  build/               - Temporary build files (can be deleted)" -ForegroundColor Gray
Write-Host ""
