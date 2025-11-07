"""
Manual Faster-Whisper Extraction Helper - DEPRECATED

⚠️ WARNING: This script is DEPRECATED and will be removed in a future version.

The Pogadane project has migrated to a 100% pip-based installation.
Instead of downloading faster-whisper-xxl.exe, use:

    pip install faster-whisper

Or for the original Whisper:

    pip install openai-whisper

See PIP_ONLY_INSTALLATION.md for current installation instructions.

---

LEGACY DOCUMENTATION (for historical reference only):

This script helped extract Faster-Whisper when automatic extraction failed
due to py7zr not supporting BCJ2 compression filter.

Usage:
    python tools/extract_faster_whisper.py
"""

import sys
import subprocess
from pathlib import Path


def print_status(message: str, success: bool = True, indent: int = 0) -> None:
    """Print status message."""
    icon = "✅" if success else "❌"
    print(f"{'  ' * indent}{icon} {message}")


def print_info(message: str, indent: int = 0) -> None:
    """Print info message."""
    print(f"{'  ' * indent}ℹ️  {message}")


def print_warning(message: str, indent: int = 0) -> None:
    """Print warning message."""
    print(f"{'  ' * indent}⚠️  {message}")


def find_7zip() -> Path:
    """
    Find 7-Zip installation.
    
    Returns:
        Path to 7z.exe or None
    """
    common_paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]
    
    for path in common_paths:
        if Path(path).exists():
            return Path(path)
    
    # Try PATH
    try:
        result = subprocess.run(
            ["where", "7z.exe"],
            check=True,
            capture_output=True,
            text=True
        )
        path = result.stdout.strip().split('\n')[0]
        if path:
            return Path(path)
    except:
        pass
    
    return None


def extract_faster_whisper() -> bool:
    """
    Extract Faster-Whisper archive using 7-Zip.
    
    Returns:
        True if successful
    """
    print("\n" + "=" * 70)
    print("🔧 Faster-Whisper Manual Extraction Helper")
    print("=" * 70 + "\n")
    
    # Find base directory
    base_dir = Path(__file__).parent.parent
    archive_path = base_dir / "dep" / "faster-whisper" / "Faster-Whisper-XXL_r245.4_windows.7z"
    extract_dir = base_dir / "dep" / "faster-whisper" / "extracted"
    install_path = base_dir / "dep" / "faster-whisper" / "faster-whisper-xxl.exe"
    
    # Check if already installed
    if install_path.exists():
        print_status(f"Faster-Whisper already installed at: {install_path}")
        return True
    
    # Check if archive exists
    if not archive_path.exists():
        print_status(f"Archive not found: {archive_path}", success=False)
        print_info("Please run: python tools/install.py", indent=1)
        return False
    
    print_info(f"Archive found: {archive_path}")
    print_info(f"Size: {archive_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Find 7-Zip
    seven_zip = find_7zip()
    
    if not seven_zip:
        print_warning("7-Zip not found!")
        print_info("Please install 7-Zip:")
        print_info("  1. Download from: https://www.7-zip.org/", indent=1)
        print_info("  2. Install 7-Zip", indent=1)
        print_info("  3. Run this script again", indent=1)
        return False
    
    print_status(f"Found 7-Zip: {seven_zip}")
    
    # Extract archive
    print_info("Extracting archive (this may take 2-5 minutes)...")
    
    try:
        result = subprocess.run(
            [str(seven_zip), "x", str(archive_path), f"-o{extract_dir}", "-y"],
            check=True,
            capture_output=True,
            text=True
        )
        print_status("Extraction complete")
    except subprocess.CalledProcessError as e:
        print_status("Extraction failed", success=False)
        print_info(f"Error: {e.stderr}", indent=1)
        return False
    
    # Find the exe
    print_info("Locating faster-whisper-xxl.exe...")
    
    exe_candidates = list(extract_dir.rglob("faster-whisper-xxl.exe"))
    
    if not exe_candidates:
        print_status("faster-whisper-xxl.exe not found in extracted files", success=False)
        print_info("Extracted directory contents:", indent=1)
        for item in extract_dir.rglob("*"):
            if item.is_file():
                print_info(f"  {item.relative_to(extract_dir)}", indent=2)
        return False
    
    # Copy exe to install location
    exe_source = exe_candidates[0]
    print_info(f"Found: {exe_source.relative_to(extract_dir)}")
    
    install_path.parent.mkdir(parents=True, exist_ok=True)
    
    import shutil
    shutil.copy2(exe_source, install_path)
    print_status(f"Installed to: {install_path}")
    
    # Cleanup
    print_info("Cleaning up temporary files...")
    try:
        shutil.rmtree(extract_dir)
        archive_path.unlink()
        print_status("Cleanup complete")
    except Exception as e:
        print_warning(f"Cleanup failed (not critical): {e}")
    
    # Update config
    print_info("Updating configuration...")
    config_path = base_dir / ".config" / "config.py"
    
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_content = f.read()
            
            rel_path = install_path.relative_to(base_dir)
            
            config_content = config_content.replace(
                'FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"',
                f'FASTER_WHISPER_EXE = r"{rel_path}"'
            )
            
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(config_content)
            
            print_status(f"Configuration updated")
        except Exception as e:
            print_warning(f"Config update failed: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Faster-Whisper extraction complete!")
    print("=" * 70 + "\n")
    
    return True


def main():
    """Main function."""
    try:
        success = extract_faster_whisper()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Extraction cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Extraction failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
