"""
Pogadane Dependency Manager - DEPRECATED

⚠️ WARNING: This module is DEPRECATED and will be removed in a future version.

The Pogadane project has migrated to a 100% pip-based installation approach.
All dependencies are now installed via pip:
- faster-whisper (pip install faster-whisper)
- openai-whisper (pip install openai-whisper)
- yt-dlp (pip install yt-dlp)
- ollama (install from ollama.com/download)

Binary executables are no longer used or supported.

See PIP_ONLY_INSTALLATION.md for current installation instructions.

---

LEGACY DOCUMENTATION (for historical reference only):

This module handled downloading and managing external binary dependencies
for Pogadane that cannot be installed via pip:
- faster-whisper-xxl.exe (transcription engine) - REPLACED by pip install faster-whisper
- yt-dlp.exe (YouTube downloader) - REPLACED by pip install yt-dlp
- Ollama (optional, for local LLM) - Install from ollama.com

All binaries were downloaded to the dep/ folder to keep the repository clean.
"""

import os
import sys
import urllib.request
import urllib.error
import json
import zipfile
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple
import subprocess


class DependencyManager:
    """Manages external binary dependencies for Pogadane."""
    
    # Dependency definitions
    DEPENDENCIES = {
        "yt-dlp": {
            "name": "yt-dlp",
            "display_name": "yt-dlp (YouTube Downloader)",
            "version_url": "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest",
            "file_pattern": "yt-dlp.exe",
            "download_url": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe",
            "install_path": "dep/yt-dlp/yt-dlp.exe",
            "required": True,
            "description": "Downloads audio from YouTube videos",
        },
        "faster-whisper": {
            "name": "faster-whisper",
            "display_name": "Faster-Whisper-XXL (Transcription Engine)",
            "version_url": "https://api.github.com/repos/Purfview/whisper-standalone-win/releases/tags/Faster-Whisper-XXL",
            "file_pattern": "Faster-Whisper-XXL_r*.7z",
            "download_url": "https://github.com/Purfview/whisper-standalone-win/releases/download/Faster-Whisper-XXL/Faster-Whisper-XXL_r245.4_windows.7z",
            "install_path": "dep/faster-whisper/faster-whisper-xxl.exe",
            "required": True,
            "description": "Converts speech to text (transcription)",
            "is_archive": True,
            "archive_exe_path": "Faster-Whisper-XXL/faster-whisper-xxl.exe",
        },
        "ollama": {
            "name": "ollama",
            "display_name": "Ollama (Local AI)",
            "download_url": "https://ollama.com/download/OllamaSetup.exe",
            "install_path": "dep/ollama/OllamaSetup.exe",
            "required": False,
            "description": "Local AI for generating summaries (alternative to Google Gemini)",
            "is_installer": True,
        },
    }
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize dependency manager.
        
        Args:
            base_dir: Base directory for Pogadane installation (default: current directory)
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.dep_dir = self.base_dir / "dep"
        self.dep_dir.mkdir(exist_ok=True)
        
    def print_status(self, message: str, success: bool = True, indent: int = 0) -> None:
        """Print status message with icon."""
        icon = "✅" if success else "❌"
        print(f"{'  ' * indent}{icon} {message}")
        
    def print_info(self, message: str, indent: int = 0) -> None:
        """Print info message."""
        print(f"{'  ' * indent}ℹ️  {message}")
        
    def print_warning(self, message: str, indent: int = 0) -> None:
        """Print warning message."""
        print(f"{'  ' * indent}⚠️  {message}")
        
    def download_file(self, url: str, destination: Path, show_progress: bool = True) -> bool:
        """
        Download a file from URL to destination.
        
        Args:
            url: URL to download from
            destination: Local path to save file
            show_progress: Whether to show download progress
            
        Returns:
            True if successful, False otherwise
        """
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            self.print_info(f"Downloading from: {url}")
            self.print_info(f"Saving to: {destination}")
            
            def reporthook(block_num, block_size, total_size):
                if show_progress and total_size > 0:
                    downloaded = block_num * block_size
                    percent = min(100, (downloaded / total_size) * 100)
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    print(f"\r  Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="")
            
            urllib.request.urlretrieve(url, destination, reporthook if show_progress else None)
            
            if show_progress:
                print()  # New line after progress
                
            self.print_status(f"Downloaded successfully", indent=1)
            return True
            
        except urllib.error.HTTPError as e:
            self.print_status(f"HTTP Error {e.code}: {e.reason}", success=False, indent=1)
            return False
        except urllib.error.URLError as e:
            self.print_status(f"Connection Error: {e.reason}", success=False, indent=1)
            return False
        except Exception as e:
            self.print_status(f"Download failed: {e}", success=False, indent=1)
            return False
    
    def extract_7z_archive(self, archive_path: Path, extract_to: Path) -> bool:
        """
        Extract .7z archive using py7zr if available, otherwise instruct user.
        
        Args:
            archive_path: Path to .7z file
            extract_to: Directory to extract to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import py7zr
            
            self.print_info(f"Extracting {archive_path.name}...")
            extract_to.mkdir(parents=True, exist_ok=True)
            
            with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                archive.extractall(path=extract_to)
                
            self.print_status("Extraction complete", indent=1)
            return True
            
        except ImportError:
            self.print_warning("py7zr not installed. Attempting manual extraction guide...", indent=1)
            self.print_info("Please install py7zr: pip install py7zr", indent=1)
            self.print_info(f"Or manually extract {archive_path} to {extract_to}", indent=1)
            return False
        except Exception as e:
            # py7zr doesn't support BCJ2 filter used by Faster-Whisper
            # Try using 7z command-line if available
            self.print_warning(f"py7zr extraction failed: {e}", indent=1)
            self.print_info("Attempting extraction with 7-Zip command-line...", indent=1)
            
            # Try to use 7z.exe from common locations
            seven_zip_paths = [
                r"C:\Program Files\7-Zip\7z.exe",
                r"C:\Program Files (x86)\7-Zip\7z.exe",
                "7z",  # If in PATH
            ]
            
            for seven_zip_exe in seven_zip_paths:
                try:
                    result = subprocess.run(
                        [seven_zip_exe, "x", str(archive_path), f"-o{extract_to}", "-y"],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    self.print_status("Extraction complete using 7-Zip", indent=1)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            # All extraction methods failed
            self.print_status("Automatic extraction failed", success=False, indent=1)
            return False
    
    def check_dependency_installed(self, dep_name: str) -> Tuple[bool, Optional[Path]]:
        """
        Check if a dependency is installed.
        
        Args:
            dep_name: Name of dependency (key from DEPENDENCIES)
            
        Returns:
            Tuple of (is_installed, path_to_exe)
        """
        dep_info = self.DEPENDENCIES.get(dep_name)
        if not dep_info:
            return False, None
            
        install_path = self.base_dir / dep_info["install_path"]
        
        if install_path.exists():
            return True, install_path
        else:
            return False, None
    
    def install_dependency(self, dep_name: str, force: bool = False) -> bool:
        """
        Install a specific dependency.
        
        Args:
            dep_name: Name of dependency to install
            force: Force reinstall even if already installed
            
        Returns:
            True if successful, False otherwise
        """
        dep_info = self.DEPENDENCIES.get(dep_name)
        if not dep_info:
            self.print_status(f"Unknown dependency: {dep_name}", success=False)
            return False
        
        print(f"\n{'=' * 70}")
        print(f"📦 Installing: {dep_info['display_name']}")
        print(f"   {dep_info['description']}")
        print(f"{'=' * 70}")
        
        # Check if already installed
        is_installed, install_path = self.check_dependency_installed(dep_name)
        if is_installed and not force:
            self.print_status(f"Already installed at: {install_path}")
            return True
        
        install_path = self.base_dir / dep_info["install_path"]
        
        # Handle installers (like Ollama)
        if dep_info.get("is_installer"):
            installer_path = self.dep_dir / dep_name / f"{dep_name}_setup.exe"
            
            if not self.download_file(dep_info["download_url"], installer_path):
                return False
            
            self.print_info(f"Installer downloaded to: {installer_path}")
            
            # Ask user if they want to run installer now
            self.print_warning("Ollama installer is ready.", indent=1)
            self.print_info("You can:", indent=1)
            self.print_info(f"  1. Run installer now: {installer_path}", indent=2)
            self.print_info(f"  2. Run it later manually", indent=2)
            self.print_info(f"  3. Skip if already installed", indent=2)
            
            # Try to launch installer (non-blocking)
            try:
                if sys.platform == "win32":
                    import subprocess
                    # Use Popen instead of os.startfile for non-blocking behavior
                    subprocess.Popen([str(installer_path)], shell=True)
                    self.print_status("Installer launched in background", indent=1)
                    self.print_info("Complete the installation, then continue here", indent=2)
            except Exception as e:
                self.print_warning(f"Could not auto-launch: {e}", indent=1)
                self.print_info(f"Please run manually: {installer_path}", indent=2)
            
            # Mark as successful - user needs to complete installation manually
            return True
        
        # Handle archives (like Faster-Whisper)
        if dep_info.get("is_archive"):
            archive_name = dep_info["download_url"].split("/")[-1]
            archive_path = self.dep_dir / dep_name / archive_name
            
            # Download archive
            if not self.download_file(dep_info["download_url"], archive_path):
                return False
            
            # Extract archive
            extract_dir = self.dep_dir / dep_name / "extracted"
            
            if archive_name.endswith(".7z"):
                if not self.extract_7z_archive(archive_path, extract_dir):
                    self.print_warning("Manual extraction required:", indent=1)
                    self.print_info(f"1. Install 7-Zip from https://www.7-zip.org/", indent=2)
                    self.print_info(f"2. Extract {archive_path}", indent=2)
                    self.print_info(f"3. Find {dep_info['archive_exe_path']}", indent=2)
                    self.print_info(f"4. Copy to {install_path}", indent=2)
                    return False
            elif archive_name.endswith(".zip"):
                self.print_info("Extracting ZIP archive...")
                try:
                    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    self.print_status("Extraction complete", indent=1)
                except Exception as e:
                    self.print_status(f"Extraction failed: {e}", success=False, indent=1)
                    return False
            
            # Find and move exe
            exe_in_archive = extract_dir / dep_info["archive_exe_path"]
            if exe_in_archive.exists():
                install_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(exe_in_archive, install_path)
                self.print_status(f"Installed to: {install_path}")
                
                # Cleanup
                try:
                    shutil.rmtree(extract_dir)
                    archive_path.unlink()
                    self.print_info("Cleanup completed", indent=1)
                except:
                    pass  # Cleanup is optional
                    
                return True
            else:
                self.print_status(f"Could not find {exe_in_archive} in extracted files", success=False)
                self.print_info(f"Expected path: {exe_in_archive}", indent=1)
                
                # List what we actually extracted
                if extract_dir.exists():
                    self.print_info("Extracted files:", indent=1)
                    try:
                        for item in extract_dir.rglob("*"):
                            if item.is_file():
                                rel_path = item.relative_to(extract_dir)
                                self.print_info(f"  {rel_path}", indent=2)
                                # Check if this is the exe we're looking for
                                if item.name.lower() == "faster-whisper-xxl.exe":
                                    self.print_info(f"Found exe at different location: {rel_path}", indent=1)
                                    install_path.parent.mkdir(parents=True, exist_ok=True)
                                    shutil.copy2(item, install_path)
                                    self.print_status(f"Installed to: {install_path}")
                                    return True
                    except Exception as e:
                        self.print_warning(f"Error listing files: {e}", indent=2)
                
                return False
        
        # Handle simple exe downloads (like yt-dlp)
        if not self.download_file(dep_info["download_url"], install_path):
            return False
        
        self.print_status(f"Installed to: {install_path}")
        return True
    
    def install_all(self, include_optional: bool = False) -> Dict[str, bool]:
        """
        Install all dependencies.
        
        Args:
            include_optional: Whether to include optional dependencies
            
        Returns:
            Dictionary mapping dependency names to installation success
        """
        results = {}
        
        for dep_name, dep_info in self.DEPENDENCIES.items():
            # Skip optional dependencies if not requested
            if not dep_info["required"] and not include_optional:
                self.print_info(f"Skipping optional dependency: {dep_info['display_name']}")
                continue
            
            results[dep_name] = self.install_dependency(dep_name)
        
        return results
    
    def update_config(self) -> bool:
        """
        Update .config/config.py with correct paths to installed dependencies.
        
        Returns:
            True if successful, False otherwise
        """
        config_path = self.base_dir / ".config" / "config.py"
        
        if not config_path.exists():
            self.print_warning(f"Config file not found: {config_path}")
            return False
        
        try:
            # Read current config
            with open(config_path, "r", encoding="utf-8") as f:
                config_content = f.read()
            
            # Update paths
            for dep_name in ["yt-dlp", "faster-whisper"]:
                is_installed, install_path = self.check_dependency_installed(dep_name)
                if is_installed:
                    # Make path relative to project root or absolute
                    rel_path = install_path.relative_to(self.base_dir)
                    
                    if dep_name == "yt-dlp":
                        # Update YT_DLP_EXE
                        config_content = config_content.replace(
                            'YT_DLP_EXE = "yt-dlp.exe"',
                            f'YT_DLP_EXE = r"{rel_path}"'
                        )
                    elif dep_name == "faster-whisper":
                        # Update FASTER_WHISPER_EXE
                        config_content = config_content.replace(
                            'FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"',
                            f'FASTER_WHISPER_EXE = r"{rel_path}"'
                        )
            
            # Write updated config
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(config_content)
            
            self.print_status(f"Updated config file: {config_path}")
            return True
            
        except Exception as e:
            self.print_status(f"Failed to update config: {e}", success=False)
            return False
    
    def verify_installation(self) -> Dict[str, bool]:
        """
        Verify all dependencies are correctly installed.
        
        Returns:
            Dictionary mapping dependency names to verification status
        """
        print(f"\n{'=' * 70}")
        print("🔍 Verifying Installation")
        print(f"{'=' * 70}\n")
        
        results = {}
        
        for dep_name, dep_info in self.DEPENDENCIES.items():
            is_installed, install_path = self.check_dependency_installed(dep_name)
            
            status = "✅ Installed" if is_installed else "❌ Missing"
            required = "Required" if dep_info["required"] else "Optional"
            
            print(f"{status} - {dep_info['display_name']} ({required})")
            if is_installed:
                print(f"  📁 Location: {install_path}")
            
            results[dep_name] = is_installed
        
        print()
        return results


def main():
    """Main function for standalone execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pogadane Dependency Manager - Install external binary dependencies"
    )
    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="Include optional dependencies (e.g., Ollama)"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify installation, don't install"
    )
    parser.add_argument(
        "--install",
        choices=list(DependencyManager.DEPENDENCIES.keys()),
        help="Install specific dependency"
    )
    
    args = parser.parse_args()
    
    manager = DependencyManager()
    
    if args.verify_only:
        manager.verify_installation()
    elif args.install:
        manager.install_dependency(args.install)
        manager.update_config()
    else:
        results = manager.install_all(include_optional=args.include_optional)
        manager.update_config()
        manager.verify_installation()


if __name__ == "__main__":
    main()
