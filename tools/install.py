"""
Pogadane - Complete Installation Script

This is the ONE-COMMAND installation script for Pogadane.
It handles everything:
- Python environment setup
- Python package dependencies
- External binary downloads (yt-dlp, faster-whisper)
- Configuration file setup
- Ollama installation (optional)

Usage:
    python tools/install.py                    # Full automatic installation
    python tools/install.py --no-ollama        # Skip Ollama
    python tools/install.py --dev              # Include development tools
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Add tools directory to path to import dependency_manager
sys.path.insert(0, str(Path(__file__).parent))

from dependency_manager import DependencyManager


class PogadaneInstaller:
    """Complete installer for Pogadane application."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize installer.
        
        Args:
            base_dir: Base directory for installation (default: parent of tools/)
        """
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Get parent directory of tools/
            self.base_dir = Path(__file__).parent.parent
        
        self.dep_manager = DependencyManager(self.base_dir)
    
    def print_header(self, title: str) -> None:
        """Print section header."""
        print(f"\n{'=' * 70}")
        print(f"🚀 {title}")
        print(f"{'=' * 70}\n")
    
    def print_status(self, message: str, success: bool = True, indent: int = 0) -> None:
        """Print status message."""
        icon = "✅" if success else "❌"
        print(f"{'  ' * indent}{icon} {message}")
    
    def print_info(self, message: str, indent: int = 0) -> None:
        """Print info message."""
        print(f"{'  ' * indent}ℹ️  {message}")
    
    def check_python_version(self) -> bool:
        """
        Check if Python version meets requirements.
        
        Returns:
            True if version is adequate, False otherwise
        """
        self.print_header("Checking Python Version")
        
        major, minor = sys.version_info.major, sys.version_info.minor
        version_str = f"{major}.{minor}.{sys.version_info.micro}"
        
        if major >= 3 and minor >= 7:
            self.print_status(f"Python {version_str} (OK, >= 3.7 required)")
            return True
        else:
            self.print_status(f"Python {version_str} (Too old, >= 3.7 required)", success=False)
            self.print_info("Please install Python 3.7 or newer from https://www.python.org/", indent=1)
            return False
    
    def check_pip(self) -> bool:
        """
        Check if pip is available.
        
        Returns:
            True if pip is available, False otherwise
        """
        self.print_header("Checking pip")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
            self.print_status("pip is available")
            self.print_info(result.stdout.strip(), indent=1)
            return True
        except subprocess.CalledProcessError:
            self.print_status("pip is not available", success=False)
            self.print_info("Please install pip: python -m ensurepip --upgrade", indent=1)
            return False
    
    def upgrade_pip(self) -> bool:
        """
        Upgrade pip to latest version.
        
        Returns:
            True if successful, False otherwise
        """
        self.print_header("Upgrading pip")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                check=True,
                capture_output=True
            )
            self.print_status("pip upgraded to latest version")
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to upgrade pip: {e}", success=False)
            return False
    
    def install_python_packages(self, include_dev: bool = False) -> bool:
        """
        Install Python package dependencies.
        
        Args:
            include_dev: Whether to include development dependencies
            
        Returns:
            True if successful, False otherwise
        """
        self.print_header("Installing Python Packages")
        
        # Install from requirements.txt
        requirements_file = self.base_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.print_status(f"requirements.txt not found at {requirements_file}", success=False)
            return False
        
        self.print_info(f"Installing from: {requirements_file}")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                check=True
            )
            self.print_status("Python packages installed successfully")
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to install Python packages: {e}", success=False)
            return False
        
        # Install test dependencies if requested
        if include_dev:
            test_requirements = self.base_dir / "requirements-test.txt"
            if test_requirements.exists():
                self.print_info(f"Installing test dependencies from: {test_requirements}")
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-r", str(test_requirements)],
                        check=True
                    )
                    self.print_status("Test dependencies installed successfully")
                except subprocess.CalledProcessError as e:
                    self.print_status(f"Failed to install test dependencies: {e}", success=False)
        
        # Install py7zr for extracting Faster-Whisper archive
        self.print_info("Installing py7zr for archive extraction")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "py7zr"],
                check=True,
                capture_output=True
            )
            self.print_status("py7zr installed successfully")
        except subprocess.CalledProcessError:
            self.print_status("py7zr installation failed (will use manual extraction)", success=False)
        
        return True
    
    def install_package_editable(self) -> bool:
        """
        Install Pogadane package in editable mode.
        
        Returns:
            True if successful, False otherwise
        """
        self.print_header("Installing Pogadane Package")
        
        setup_file = self.base_dir / "setup.py"
        
        if not setup_file.exists():
            self.print_info("setup.py not found, skipping editable install")
            return True
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", str(self.base_dir)],
                check=True
            )
            self.print_status("Pogadane package installed in editable mode")
            self.print_info("You can now run: pogadane-gui or pogadane-cli", indent=1)
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to install package: {e}", success=False)
            return False
    
    def install_external_dependencies(self, include_ollama: bool = True) -> bool:
        """
        Install external binary dependencies.
        
        Args:
            include_ollama: Whether to include Ollama installation
            
        Returns:
            True if all required dependencies installed successfully
        """
        self.print_header("Installing External Dependencies")
        
        results = self.dep_manager.install_all(include_optional=include_ollama)
        
        # Check if all required dependencies succeeded
        all_required_ok = all(
            results.get(dep_name, False)
            for dep_name, dep_info in DependencyManager.DEPENDENCIES.items()
            if dep_info["required"]
        )
        
        return all_required_ok
    
    def setup_ollama_model(self) -> bool:
        """
        Download Ollama model if Ollama is installed.
        
        Returns:
            True if successful or skipped, False on error
        """
        self.print_header("Setting Up Ollama Model")
        
        # Check if Ollama is available
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
            self.print_status("Ollama is installed")
            self.print_info(result.stdout.strip(), indent=1)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_info("Ollama not found or not in PATH")
            self.print_info("Install Ollama from https://ollama.com/ to use local AI", indent=1)
            return True  # Not an error, just skip
        
        # Pull default model
        default_model = "gemma3:4b"
        self.print_info(f"Downloading model: {default_model}")
        self.print_info("This may take 5-15 minutes depending on your connection", indent=1)
        
        try:
            subprocess.run(
                ["ollama", "pull", default_model],
                check=True
            )
            self.print_status(f"Model {default_model} downloaded successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to download model: {e}", success=False)
            self.print_info("You can manually download it later: ollama pull gemma3:4b", indent=1)
            return False
    
    def create_directories(self) -> bool:
        """
        Create necessary directory structure.
        
        Returns:
            True if successful
        """
        self.print_header("Creating Directory Structure")
        
        directories = [
            self.base_dir / "dep",
            self.base_dir / ".config",
            self.base_dir / "samples",
            self.base_dir / "doc",
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            self.print_info(f"Created: {directory}")
        
        self.print_status("Directory structure created")
        return True
    
    def verify_installation(self) -> None:
        """Verify complete installation."""
        self.print_header("Verifying Installation")
        
        # Verify external dependencies
        dep_results = self.dep_manager.verify_installation()
        
        # Check if config file exists
        config_file = self.base_dir / ".config" / "config.py"
        if config_file.exists():
            self.print_status(f"Config file found: {config_file}")
        else:
            self.print_status(f"Config file missing: {config_file}", success=False)
        
        # Summary
        all_required = all(
            dep_results.get(dep_name, False)
            for dep_name, dep_info in DependencyManager.DEPENDENCIES.items()
            if dep_info["required"]
        )
        
        print(f"\n{'=' * 70}")
        if all_required:
            print("✅ Installation Complete!")
            print("\nYou can now run Pogadane:")
            print("  GUI:  python -m pogadane.gui")
            print("  CLI:  python -m pogadane.transcribe_summarize_working --help")
            print("\nOr if installed as package:")
            print("  GUI:  pogadane-gui")
            print("  CLI:  pogadane-cli --help")
        else:
            print("⚠️  Installation completed with some issues")
            print("\nPlease review the errors above and install missing components manually.")
        print(f"{'=' * 70}\n")
    
    def run_full_installation(
        self, 
        include_ollama: bool = True, 
        include_dev: bool = False
    ) -> bool:
        """
        Run complete installation process.
        
        Args:
            include_ollama: Whether to include Ollama
            include_dev: Whether to include development tools
            
        Returns:
            True if installation successful
        """
        print(f"\n{'#' * 70}")
        print("# POGADANE - AUTOMATIC INSTALLATION")
        print(f"# Version 0.1.8")
        print(f"{'#' * 70}\n")
        
        # Step 1: Check prerequisites
        if not self.check_python_version():
            return False
        
        if not self.check_pip():
            return False
        
        # Step 2: Create directory structure
        self.create_directories()
        
        # Step 3: Upgrade pip
        self.upgrade_pip()
        
        # Step 4: Install Python packages
        if not self.install_python_packages(include_dev=include_dev):
            return False
        
        # Step 5: Install package in editable mode
        self.install_package_editable()
        
        # Step 6: Install external dependencies
        if not self.install_external_dependencies(include_ollama=include_ollama):
            print("\n⚠️  Some external dependencies failed to install")
            print("You can retry with: python tools/dependency_manager.py")
        
        # Step 7: Update config with correct paths
        self.dep_manager.update_config()
        
        # Step 8: Setup Ollama model (if Ollama requested)
        if include_ollama:
            self.setup_ollama_model()
        
        # Step 9: Verify installation
        self.verify_installation()
        
        return True


def main():
    """Main entry point for installation script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pogadane Complete Installation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/install.py                  # Full installation with Ollama
  python tools/install.py --no-ollama      # Skip Ollama installation
  python tools/install.py --dev            # Include development tools
  python tools/install.py --no-ollama --dev # Skip Ollama, include dev tools
        """
    )
    
    parser.add_argument(
        "--no-ollama",
        action="store_true",
        help="Skip Ollama installation (use Google Gemini API instead)"
    )
    
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Include development and testing dependencies"
    )
    
    args = parser.parse_args()
    
    installer = PogadaneInstaller()
    
    try:
        success = installer.run_full_installation(
            include_ollama=not args.no_ollama,
            include_dev=args.dev
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Installation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
