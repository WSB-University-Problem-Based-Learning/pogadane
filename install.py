"""
Pogadane Simple Installer

Cross-platform installation wizard with lightweight and full installation options.
Works on Windows, macOS, and Linux.

Usage:
    python install.py [--lightweight] [--full] [--dev]
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

# Detect platform
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DEP_DIR = PROJECT_ROOT / "dep"
CONFIG_DIR = PROJECT_ROOT / ".config"

# Colors for terminal output (cross-platform)
class Colors:
    if IS_WINDOWS:
        # Enable ANSI colors on Windows
        os.system("")
    
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}🚀 {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def run_command(cmd, description="", check=True):
    """Run a command and return success status."""
    if description:
        print_info(description)
    
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Command failed: {' '.join(cmd)}")
            if e.stderr:
                print(e.stderr)
        return False
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        return False


def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python {version_str} detected")
    
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python version OK (>= 3.7 required)")
        return True
    else:
        print_error(f"Python 3.7+ required, you have {version_str}")
        return False


def install_package(package_name, description=""):
    """Install a Python package."""
    if description:
        print_info(description)
    
    return run_command(
        [sys.executable, "-m", "pip", "install", package_name],
        f"Installing {package_name}...",
        check=False
    )


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directory Structure")
    
    directories = [
        DEP_DIR,
        CONFIG_DIR,
        PROJECT_ROOT / "samples",
        PROJECT_ROOT / "doc"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_info(f"Created: {directory}")
    
    print_success("Directory structure created")
    return True


def install_core_packages():
    """Install core Python packages."""
    print_header("Installing Core Python Packages")
    
    # First ensure pip and setuptools
    print_info("Ensuring pip and setuptools are up to date...")
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools"],
        check=False
    )
    
    core_packages = [
        "flet>=0.24.0",
        "google-generativeai>=0.3.0"
    ]
    
    for package in core_packages:
        install_package(package)
    
    print_success("Core packages installed")
    return True


def install_lightweight():
    """Install recommended default configuration (faster-whisper + yt-dlp + GGUF)."""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.GREEN}📦 RECOMMENDED INSTALLATION (Default Stack){Colors.END}")
    print("="*70)
    print("\nThis installs:")
    print("  • yt-dlp (YouTube support)")
    print("  • faster-whisper (4x faster transcription with GPU support)")
    print("  • llama-cpp-python (for GGUF models like Gemma)")
    print("  • Total download: ~500MB")
    print()
    print(f"{Colors.CYAN}Default model: dep/models/gemma-3-4b-it-Q4_K_M.gguf{Colors.END}")
    print(f"{Colors.YELLOW}Note: Download model separately (see README.md){Colors.END}")
    print()
    
    # Install yt-dlp
    print_header("Installing yt-dlp (YouTube Support)")
    install_package("yt-dlp", "YouTube video/audio downloader")
    
    # Install faster-whisper
    print_header("Installing faster-whisper (Recommended Transcription)")
    install_package("faster-whisper>=1.0.0", "Fast transcription with GPU support")
    
    # Install llama-cpp-python for GGUF models
    print_header("Installing llama-cpp-python (GGUF Model Support)")
    install_package("llama-cpp-python", "Run quantized GGUF models efficiently")
    
    print_success("Recommended installation complete!")
    print("\n" + "="*70)
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print("  1. Download GGUF model: see README.md for instructions")
    print("  2. Run the app: python run_gui_flet.py")
    print("  3. Transcription: faster-whisper (automatic download)")
    print("  4. AI Summary: GGUF model (gemma-3-4b-it-Q4_K_M.gguf)")
    print("  5. Optional: Install Ollama for more models (ollama.com)")
    print("  6. Edit .config/config.py to customize")
    print("="*70 + "\n")


def install_full():
    """Install all options (including optional backends)."""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.GREEN}📦 FULL INSTALLATION (All Options){Colors.END}")
    print("="*70)
    print("\nThis installs:")
    print("  • yt-dlp (YouTube support)")
    print("  • faster-whisper (recommended transcription)")
    print("  • llama-cpp-python (GGUF models)")
    print("  • openai-whisper (alternative transcription)")
    print("  • transformers + torch (alternative AI)")
    print("  • Total download: ~1GB - 3GB")
    print()
    print(f"{Colors.YELLOW}NOTE: This includes optional backends. Most users should use lightweight.{Colors.END}")
    print()
    
    # Install yt-dlp
    print_header("Installing yt-dlp (YouTube Support)")
    install_package("yt-dlp", "YouTube video/audio downloader")
    
    # Install faster-whisper
    print_header("Installing Faster-Whisper (Recommended)")
    install_package("faster-whisper>=1.0.0", "Fast transcription engine with GPU support")
    
    # Install llama-cpp-python
    print_header("Installing llama-cpp-python (GGUF Models)")
    install_package("llama-cpp-python", "GGUF model support")
    
    # Install optional backends
    print_header("Installing Optional: OpenAI Whisper")
    install_package("openai-whisper>=20230314", "Alternative transcription engine")
    
    print_header("Installing Optional: Transformers")
    install_package("transformers>=4.30.0", "Alternative AI summarization")
    install_package("torch>=2.0.0", "PyTorch for Transformers")
    
    print_success("Full installation complete!")
    print("\n" + "="*70)
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print("  1. Download GGUF model (see README.md)")
    print("  2. Run the app: python run_gui_flet.py")
    print("  3. Optional: Install Ollama from ollama.com/download")
    print("  4. Edit .config/config.py to customize")
    print("="*70 + "\n")


def install_dev_packages():
    """Install development packages."""
    print_header("Installing Development Packages")
    
    dev_packages = [
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.11.1",
        "pylint>=2.17.0",
        "black>=23.0.0"
    ]
    
    for package in dev_packages:
        install_package(package)
    
    print_success("Development packages installed")
    return True


def install_pogadane_package():
    """Install Pogadane package in editable mode."""
    print_header("Installing Pogadane Package")
    
    if (PROJECT_ROOT / "setup.py").exists():
        success = run_command(
            [sys.executable, "-m", "pip", "install", "-e", str(PROJECT_ROOT)],
            "Installing in editable mode...",
            check=False
        )
        
        if success:
            print_success("Pogadane package installed")
            print_info("You can now run: python run_gui_flet.py")
            return True
        else:
            print_warning("Package installation failed, but you can still run from source")
            print_info("Use: python run_gui_flet.py")
            return True
    else:
        print_info("No setup.py found, skipping package installation")
        print_info("You can run from source: python run_gui_flet.py")
        return True


def show_welcome():
    """Show welcome message and installation options."""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}{'  '*10}🎙️  POGADANE INSTALLER  🎙️{Colors.END}")
    print("="*70)
    print(f"\n{Colors.BOLD}Audio transcription and AI-powered summaries{Colors.END}")
    print(f"\nPlatform: {Colors.GREEN}{platform.system()} {platform.release()}{Colors.END}")
    print(f"Python: {Colors.GREEN}{sys.version.split()[0]}{Colors.END}")
    print("\n" + "="*70)
    print(f"\n{Colors.BOLD}Choose installation type:{Colors.END}\n")
    print(f"{Colors.GREEN}1. RECOMMENDED{Colors.END} (Default Stack)")
    print("   • faster-whisper for transcription")
    print("   • llama-cpp-python for GGUF models")
    print("   • yt-dlp for YouTube support")
    print("   • Download: ~500MB")
    print("   • Requires: GGUF model file (see README)")
    print()
    print(f"{Colors.CYAN}2. FULL{Colors.END} (All Options)")
    print("   • Recommended stack +")
    print("   • openai-whisper (alternative transcription)")
    print("   • transformers + torch (alternative AI)")
    print("   • Download: ~1GB - 3GB")
    print()
    print(f"{Colors.YELLOW}3. DEV{Colors.END} (Development environment)")
    print("   • Full installation + dev tools")
    print("   • pytest, pylint, black, etc.")
    print()
    print("="*70 + "\n")


def interactive_install():
    """Interactive installation with user prompts."""
    show_welcome()
    
    choice = input(f"{Colors.BOLD}Enter choice (1/2/3) or 'q' to quit: {Colors.END}").strip().lower()
    
    if choice == 'q':
        print("\nInstallation cancelled.")
        return False
    
    # Check Python version first
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install core packages
    install_core_packages()
    
    # Install based on choice
    if choice == '1':
        install_lightweight()
    elif choice == '2':
        install_full()
    elif choice == '3':
        install_full()
        install_dev_packages()
    else:
        print_error("Invalid choice!")
        return False
    
    # Install pogadane package
    install_pogadane_package()
    
    return True


def main():
    """Main installation function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pogadane Installer - Cross-platform installation"
    )
    parser.add_argument(
        "--lightweight",
        action="store_true",
        help="Install lightweight version (Python only)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Install full version (all features)"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Install with development tools"
    )
    
    args = parser.parse_args()
    
    # Non-interactive mode
    if args.lightweight or args.full or args.dev:
        if not check_python_version():
            sys.exit(1)
        
        create_directories()
        install_core_packages()
        
        if args.lightweight:
            install_lightweight()
        elif args.full or args.dev:
            install_full()
            if args.dev:
                install_dev_packages()
        
        install_pogadane_package()
        return
    
    # Interactive mode
    try:
        success = interactive_install()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Installation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
