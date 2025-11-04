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
import json
from pathlib import Path
import urllib.request
import shutil

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
    """Install lightweight configuration (Python-only, no external binaries)."""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.GREEN}📦 LIGHTWEIGHT INSTALLATION{Colors.END}")
    print("="*70)
    print("\nThis installs:")
    print("  • Python Whisper (transcription)")
    print("  • Transformers (AI summarization)")
    print("  • No external binaries required")
    print("  • Total download: ~500MB - 2GB")
    print()
    
    # Install Whisper
    print_header("Installing Whisper (Python Transcription)")
    install_package("openai-whisper>=20230314", "Lightweight transcription engine")
    
    # Install Transformers
    print_header("Installing Transformers (Python AI)")
    install_package("transformers>=4.30.0", "Lightweight AI summarization")
    install_package("torch>=2.0.0", "PyTorch for Transformers")
    
    # Update config
    print_header("Configuring for Lightweight Mode")
    update_config_for_lightweight()
    
    print_success("Lightweight installation complete!")
    print("\n" + "="*70)
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print("  1. Run the app: python run_gui_flet.py")
    print("  2. Transcription will use Python Whisper")
    print("  3. AI will use Transformers (English only)")
    print("  4. Edit .config/config.py to customize")
    print("="*70 + "\n")


def install_full():
    """Install full configuration (all features, larger download)."""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.GREEN}📦 FULL INSTALLATION{Colors.END}")
    print("="*70)
    print("\nThis installs:")
    print("  • yt-dlp (YouTube support)")
    print("  • Python Whisper (fallback transcription)")
    print("  • Transformers (AI summarization)")
    print("  • Total download: ~500MB - 2GB")
    print()
    print(f"{Colors.YELLOW}NOTE: Faster-Whisper and Ollama require manual installation{Colors.END}")
    print("      on macOS and Linux. See documentation for details.")
    print()
    
    # Install yt-dlp (cross-platform via pip)
    print_header("Installing yt-dlp (YouTube Support)")
    install_package("yt-dlp", "YouTube video/audio downloader")
    
    # Install Whisper
    print_header("Installing Whisper (Python Transcription)")
    install_package("openai-whisper>=20230314", "Transcription engine")
    
    # Install Transformers
    print_header("Installing Transformers (AI Summarization)")
    install_package("transformers>=4.30.0", "AI summarization")
    install_package("torch>=2.0.0", "PyTorch for AI")
    
    # Platform-specific installations
    if IS_WINDOWS:
        install_windows_binaries()
    else:
        print_header("Platform-Specific Instructions")
        print_info("For Faster-Whisper:")
        if IS_MAC:
            print("  brew install whisper")
        elif IS_LINUX:
            print("  See: https://github.com/SYSTRAN/faster-whisper")
        
        print_info("\nFor Ollama:")
        if IS_MAC:
            print("  brew install ollama")
        elif IS_LINUX:
            print("  curl https://ollama.ai/install.sh | sh")
    
    print_success("Full installation complete!")
    print("\n" + "="*70)
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print("  1. Run the app: python run_gui_flet.py")
    print("  2. Edit .config/config.py to configure paths")
    if not IS_WINDOWS:
        print("  3. Install Faster-Whisper and Ollama manually (see above)")
    print("="*70 + "\n")


def install_windows_binaries():
    """Install Windows-specific external binaries."""
    if not IS_WINDOWS:
        return
    
    # Download yt-dlp.exe
    print_header("Downloading yt-dlp.exe")
    yt_dlp_dir = DEP_DIR / "yt-dlp"
    yt_dlp_dir.mkdir(parents=True, exist_ok=True)
    yt_dlp_path = yt_dlp_dir / "yt-dlp.exe"
    
    if not yt_dlp_path.exists():
        try:
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            print_info(f"Downloading from {url}")
            urllib.request.urlretrieve(url, yt_dlp_path)
            print_success(f"Downloaded to {yt_dlp_path}")
        except Exception as e:
            print_error(f"Failed to download yt-dlp: {e}")
    else:
        print_info("yt-dlp.exe already exists")
    
    # Instructions for Faster-Whisper
    print_header("Faster-Whisper Instructions")
    print_warning("Faster-Whisper requires manual download due to large size (1.5GB)")
    print_info("Download from: https://github.com/Purfview/whisper-standalone-win/releases")
    print_info("Extract to: dep/faster-whisper/")
    print_info("Or use lightweight Python Whisper instead (already installed)")
    
    # Instructions for Ollama
    print_header("Ollama Instructions")
    print_info("Download from: https://ollama.com/download")
    print_info("Or skip and use Transformers for AI (already installed)")


def update_config_for_lightweight():
    """Update config file for lightweight installation."""
    config_file = CONFIG_DIR / "config.py"
    
    if not config_file.exists():
        # Create default config
        config_content = """# Pogadane Configuration (Lightweight Mode)

# Transcription Provider
TRANSCRIPTION_PROVIDER = "whisper"  # Using Python Whisper (lightweight)
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
WHISPER_LANGUAGE = "Polish"
WHISPER_DEVICE = "auto"  # auto, cpu, or cuda

# AI Summarization Provider
SUMMARY_PROVIDER = "transformers"  # Using Transformers (lightweight)
TRANSFORMERS_MODEL = "facebook/bart-large-cnn"  # Good quality, ~1.6GB
# Alternatives:
#   "sshleifer/distilbart-cnn-12-6"  # Faster, ~500MB
#   "google/flan-t5-small"           # Smallest, ~300MB
TRANSFORMERS_DEVICE = "auto"
SUMMARY_LANGUAGE = "English"  # Note: Most Transformers models only support English

# Google Gemini (Alternative cloud AI)
# SUMMARY_PROVIDER = "google"
# GOOGLE_API_KEY = ""  # Add your API key here
# GOOGLE_GEMINI_MODEL = "gemini-1.5-flash-latest"

# YouTube Support (if using yt-dlp from pip)
YT_DLP_EXE = "yt-dlp"  # Will use system yt-dlp from pip

# General Settings
DEBUG_MODE = False
TRANSCRIPTION_FORMAT = "txt"
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"
"""
        config_file.write_text(config_content, encoding='utf-8')
        print_success(f"Created config: {config_file}")
    else:
        print_info(f"Config already exists: {config_file}")


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
    print(f"{Colors.GREEN}1. LIGHTWEIGHT{Colors.END} (Recommended for beginners)")
    print("   • Pure Python, no external binaries")
    print("   • Whisper (Python) for transcription")
    print("   • Transformers for AI (English only)")
    print("   • Download: ~500MB - 2GB")
    print()
    print(f"{Colors.CYAN}2. FULL{Colors.END} (All features)")
    print("   • yt-dlp for YouTube support")
    print("   • Python Whisper for transcription")
    print("   • Transformers for AI")
    print("   • Download: ~500MB - 2GB")
    if IS_WINDOWS:
        print("   • Optional: Faster-Whisper, Ollama (manual)")
    else:
        print(f"   • Ollama: install via package manager (see docs)")
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
