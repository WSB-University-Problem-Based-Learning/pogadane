"""
File and path utilities.

This module contains utility functions for file operations,
path manipulation, filename generation, and subprocess execution.
"""

import os
import re
import sys
import shlex
import subprocess
from pathlib import Path
from typing import Optional


def run_subprocess(
    command_list: list,
    input_data: Optional[str] = None,
    debug_mode: bool = False
) -> Optional[subprocess.CompletedProcess]:
    """
    Run subprocess with platform-specific console hiding and consistent error handling.
    
    This utility centralizes subprocess execution logic to avoid duplication across
    transcription and LLM providers. It handles:
    - Windows console hiding (SW_HIDE)
    - Debug vs. production logging
    - Proper error handling and reporting
    - UTF-8 encoding
    
    Args:
        command_list: Command and arguments as list (e.g., ["program", "arg1", "arg2"])
        input_data: Optional stdin data to send to process
        debug_mode: Enable detailed debug logging of command and output
        
    Returns:
        CompletedProcess object on success, None on failure (FileNotFoundError, etc.)
        
    Example:
        >>> result = run_subprocess(["echo", "hello"], debug_mode=True)
        >>> if result and result.returncode == 0:
        ...     print(result.stdout)
    """
    cmd_str = ' '.join(shlex.quote(str(s)) for s in command_list)
    
    if debug_mode:
        print(f"🐞 DEBUG: Running command: {cmd_str}")
    else:
        print(f"▶️ Running: {cmd_str}")
    
    # Windows-specific startup info to hide console window
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    
    try:
        process = subprocess.run(
            command_list,
            input=input_data,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
            shell=False,
            startupinfo=startupinfo
        )
        
        if debug_mode:
            print(f"☑️ Exit code: {process.returncode}")
            if process.stdout:
                print(f"--- stdout ---\n{process.stdout.strip()}\n--------------")
            if process.stderr:
                print(f"--- stderr ---\n{process.stderr.strip()}\n--------------", 
                      file=sys.stderr)
        else:
            if process.returncode == 0:
                print(f"☑️ Command finished successfully")
            else:
                print(f"⚠️ Command exited with code {process.returncode}", 
                      file=sys.stderr)
                if process.stderr:
                    print(f"--- Error output ---\n{process.stderr.strip()}\n-------------------",
                          file=sys.stderr)
        
        return process
    except FileNotFoundError:
        print(f"❌ Error: Executable not found: {command_list[0]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Unexpected error running '{command_list[0]}': {e}", file=sys.stderr)
        return None


def get_unique_filename(base_url: str, base_name: str = "downloaded_audio", extension: str = ".mp3") -> str:
    """
    Generate unique filename from URL or random hex.
    
    Args:
        base_url: URL to extract identifier from
        base_name: Base name for the file
        extension: File extension (including dot)
        
    Returns:
        Unique filename string
    """
    base_stem = Path(base_name).stem
    base_suffix = Path(base_name).suffix or extension
    
    try:
        # Try to extract YouTube video ID
        url_match = re.search(r"v=([^&]+)", base_url)
        if url_match:
            unique_id = url_match.group(1)
        else:
            # Use URL path or random hex
            unique_id = Path(base_url.split("?")[0]).name or os.urandom(4).hex()
        
        # Sanitize filename
        unique_id = re.sub(r'[\\/*?:"<>|]', '', unique_id)
        return f"{base_stem}_{unique_id}{base_suffix}"
        
    except:
        return f"{base_stem}_{os.urandom(4).hex()}{base_suffix}"


def get_input_name_stem(source_str: str) -> str:
    """
    Extract a clean name stem from file path or URL.
    
    Args:
        source_str: File path or URL
        
    Returns:
        Clean name stem suitable for use in filenames
    """
    # Check if it's a URL
    if re.match(r'^https?://', source_str):
        try:
            # Try to extract YouTube video ID
            yt_match = re.search(
                r"(?:v=|\/embed\/|\/watch\?v=|\.be\/)([a-zA-Z0-9_-]{11})",
                source_str
            )
            if yt_match:
                return f"youtube_{yt_match.group(1)}"
            
            # Use sanitized URL path
            safe_name = re.sub(r'[\\/*?:"<>|]', "", Path(source_str.split("?")[0]).name)
            return safe_name if safe_name else f"url_{os.urandom(4).hex()}"
            
        except:
            return f"url_{os.urandom(4).hex()}"
    else:
        # It's a file path
        return Path(source_str).stem


def safe_delete_file(file_path: Path, file_description: str = "file") -> bool:
    """
    Safely delete a file with error handling.
    
    Args:
        file_path: Path to file to delete
        file_description: Description of file for logging
        
    Returns:
        True if successfully deleted, False otherwise
    """
    if not file_path or not file_path.exists():
        return False
    
    print(f"🧹 Cleaning up temp {file_description}: {file_path.name}")
    try:
        os.remove(file_path)
        print(f"✅ Deleted {file_path.name}")
        return True
    except OSError as e:
        print(f"⚠️ Warning: Could not delete {file_path.name}: {e}")
        return False


def safe_create_directory(dir_path: Path, description: str = "directory") -> bool:
    """
    Safely create a directory with error handling.
    
    Args:
        dir_path: Path to directory to create
        description: Description for logging
        
    Returns:
        True if successfully created or already exists, False on error
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"ℹ️ {description.capitalize()}: {dir_path}")
        return True
    except OSError as e:
        print(f"❌ Error creating {description} '{dir_path}': {e}")
        return False


def cleanup_temp_directory(temp_dir: Path) -> bool:
    """
    Remove temporary directory if empty.
    
    Args:
        temp_dir: Path to temporary directory
        
    Returns:
        True if removed or doesn't exist, False on error
    """
    try:
        if temp_dir.exists() and not any(temp_dir.iterdir()):
            temp_dir.rmdir()
            print(f"ℹ️ Cleaned empty temp dir: {temp_dir}")
            return True
        return False
    except OSError as e:
        print(f"⚠️ Warning: Could not remove temp dir {temp_dir}: {e}")
        return False


def find_output_file(
    base_path: Path,
    stem: str,
    extension: str,
    keywords: Optional[list] = None
) -> Optional[Path]:
    """
    Find output file matching pattern and optional keywords.
    
    Args:
        base_path: Directory to search in
        stem: Base filename stem
        extension: File extension (without dot)
        keywords: Optional list of keywords that should appear in filename
        
    Returns:
        Path to found file or None
    """
    pattern = f"{stem}*.{extension}"
    found_files = list(base_path.glob(pattern))
    
    if not found_files:
        return None
    
    # If keywords provided, try to find file matching them
    if keywords:
        keywords_lower = [k.lower() for k in keywords if k]
        for file in found_files:
            if any(keyword in file.name.lower() for keyword in keywords_lower):
                return file
    
    # Otherwise return first match or file with exact stem
    exact_match = base_path / f"{stem}.{extension}"
    return exact_match if exact_match in found_files else found_files[0]
