"""
Pogadane Installer

Installs all required dependencies for Pogadane.
Works on Windows, macOS, and Linux.

Usage:
    python install.py
    python install.py --dev  # Include development tools
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"

PROJECT_ROOT = Path(__file__).parent
DEP_DIR = PROJECT_ROOT / "dep"
CONFIG_DIR = PROJECT_ROOT / ".config"


class Colors:
    if IS_WINDOWS:
        os.system("")
    
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    print(f"   {text}")


def run_pip(package):
    """Install a Python package."""
    print_info(f"Installing {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.9+ required (you have {version.major}.{version.minor})")
        return False


def install():
    """Install Pogadane dependencies."""
    print_header("🎙️  POGADANE INSTALLER")
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}\n")
    
    # Check Python
    if not check_python():
        return False
    
    # Create directories
    DEP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    (DEP_DIR / "models").mkdir(parents=True, exist_ok=True)
    
    # Upgrade pip
    print_header("Upgrading pip")
    run_pip("--upgrade pip setuptools")
    
    # Install core + transcription + summarization
    print_header("Installing Dependencies")
    
    packages = [
        "flet>=0.24.0",           # GUI
        "yt-dlp>=2023.0.0",       # YouTube download
        "faster-whisper>=1.0.0",  # Transcription
        "llama-cpp-python>=0.2.0", # GGUF summarization
        "google-generativeai>=0.3.0",  # Optional: Gemini API
    ]
    
    for pkg in packages:
        if not run_pip(pkg):
            print_error(f"Failed to install {pkg}")
    
    # Install package in editable mode
    print_header("Installing Pogadane")
    run_pip(f"-e {PROJECT_ROOT}")
    
    print_header("Installation Complete!")
    print(f"""
{Colors.GREEN}Next steps:{Colors.END}

  1. Download a GGUF model for summarization:
     https://huggingface.co/google/gemma-3-4b-it-GGUF
     Place it in: dep/models/

  2. Run the app:
     {Colors.BOLD}python -m pogadane{Colors.END}

  3. Configure in Settings or edit .config/config.py
""")
    return True


def install_dev():
    """Install development dependencies."""
    print_header("Installing Dev Tools")
    
    dev_packages = [
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.11.1",
        "black>=23.0.0",
        "pylint>=2.17.0",
    ]
    
    for pkg in dev_packages:
        run_pip(pkg)
    
    print_success("Dev tools installed")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Pogadane Installer")
    parser.add_argument("--dev", action="store_true", help="Include dev tools")
    args = parser.parse_args()
    
    try:
        if not install():
            sys.exit(1)
        
        if args.dev:
            install_dev()
            
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
