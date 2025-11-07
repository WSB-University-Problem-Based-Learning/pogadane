# Building Pogadane as a Single-File Executable

This guide explains how to build Pogadane as a standalone `.exe` file for Windows distribution.

## Overview

Pogadane can be packaged as a single-file executable using **PyInstaller**. This creates a portable application that users can run without installing Python or dependencies.

**Output:** `dist/Pogadane.exe` (~100-200 MB single file)

---

## Prerequisites

### 1. Install PyInstaller

```powershell
# In your virtual environment
.\.venv\Scripts\Activate.ps1
pip install pyinstaller
```

### 2. Verify Dependencies

Ensure all required packages are installed:

```powershell
pip install -r requirements.txt
```

---

## Building the Executable

### Option 1: Automated Build Script (Recommended)

```powershell
# Run the build script
.\build_exe.ps1
```

This script will:
1. Check for Python and PyInstaller
2. Clean previous builds
3. Build the executable using `pogadane.spec`
4. Report the output file size and location

### Option 2: Manual Build

```powershell
# Clean previous builds
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# Build with PyInstaller
pyinstaller pogadane.spec --clean
```

**Build time:** 5-10 minutes (depending on CPU)

---

## Output

### File Structure

```
dist/
└── Pogadane.exe        # Single-file executable (~100-200 MB)
```

### What's Included

The executable bundles:
- ✅ Python interpreter
- ✅ Flet framework
- ✅ All Python dependencies (google-generativeai, yt-dlp, py7zr)
- ✅ Pogadane source code
- ✅ Configuration template

### What's NOT Included

Users must install separately:
- ❌ **Transcription engines:** faster-whisper or openai-whisper
- ❌ **Ollama** (optional, for local AI)
- ❌ **FFmpeg** (usually comes with whisper)
- ❌ **AI models** (downloaded on first use)

---

## Testing the Executable

```powershell
# Run the built executable
.\dist\Pogadane.exe
```

The application should launch the Material 3 GUI.

**First run:**
- Configuration file will be created in `%USERPROFILE%\.pogadane\config.py`
- Settings can be configured via GUI

---

## Distribution

### Simple Distribution

1. Copy `dist/Pogadane.exe` to target machine
2. User double-clicks to run
3. No installation required!

### Recommended Distribution Package

Create a ZIP file with:

```
Pogadane-v0.1.8/
├── Pogadane.exe                    # Main executable
├── README.txt                      # Quick start guide
├── INSTALL_DEPENDENCIES.txt        # How to install whisper/ollama
└── LICENSE.txt                     # MIT License
```

**Example README.txt:**

```
Pogadane - Audio Transcription & AI Summarization
==================================================

Quick Start:
1. Run Pogadane.exe
2. Install dependencies (see INSTALL_DEPENDENCIES.txt)
3. Add audio files or YouTube URLs
4. Process and get transcriptions + summaries

For help, visit:
https://github.com/WSB-University-Problem-Based-Learning/pogadane
```

---

## Configuration

### Default Locations

- **Executable:** Runs from anywhere
- **Config file:** `%USERPROFILE%\.pogadane\config.py` (auto-created)
- **Temp files:** `%TEMP%\pogadane_temp_audio\`
- **Results:** Same directory as input files

### Portable Mode (Optional)

To make the app fully portable, modify `src/pogadane/config_loader.py`:

```python
# Use executable directory instead of user profile
if getattr(sys, "frozen", False):
    config_dir = Path(sys.executable).parent / ".config"
else:
    config_dir = Path.home() / ".pogadane"
```

---

## Customization

### Adding an Icon

1. Create or obtain an `.ico` file (e.g., `res/pogadane.ico`)
2. Edit `pogadane.spec`:

```python
exe = EXE(
    ...
    icon='res/pogadane.ico',  # Add this line
    ...
)
```

3. Rebuild

### Reducing File Size

**Current size:** ~100-200 MB

**Optimization options:**

1. **Exclude unused packages** (edit `pogadane.spec`):

```python
excludes=[
    'matplotlib',
    'PIL', 
    'tkinter',
    'PyQt5',
    'PyQt6',
    'pytest',
    'sphinx',
]
```

2. **UPX compression** (already enabled):

```python
upx=True,  # Compresses binaries
```

3. **Don't bundle heavy libraries:**
   - Don't include `transformers` (40+ MB)
   - Don't include `torch` (500+ MB)
   - Users install these separately if needed

**Minimal build:** ~80 MB (without transformers/torch)

---

## Advanced Options

### Multi-File Distribution (Faster Startup)

For faster startup, create a directory-based distribution:

Edit `pogadane.spec`:

```python
# Comment out the EXE section
# exe = EXE(...)

# Add COLLECT section
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Pogadane',
)
```

Output: `dist/Pogadane/` directory with multiple files

### Creating an Installer

Use **Inno Setup** to create a proper installer:

1. Install Inno Setup: https://jrsoftware.org/isinfo.php
2. Create `pogadane_installer.iss`:

```iss
[Setup]
AppName=Pogadane
AppVersion=0.1.8
DefaultDirName={pf}\Pogadane
DefaultGroupName=Pogadane
OutputDir=installer
OutputBaseFilename=Pogadane-Setup-v0.1.8

[Files]
Source: "dist\Pogadane.exe"; DestDir: "{app}"
Source: "LICENSE"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"

[Icons]
Name: "{group}\Pogadane"; Filename: "{app}\Pogadane.exe"
Name: "{commondesktop}\Pogadane"; Filename: "{app}\Pogadane.exe"

[Run]
Filename: "{app}\Pogadane.exe"; Description: "Launch Pogadane"; Flags: postinstall nowait skipifsilent
```

3. Compile with Inno Setup

---

## Troubleshooting

### Build Errors

**Error: "No module named 'flet'"**
- Solution: Ensure virtual environment is activated and flet is installed

**Error: "Unable to find 'pogadane' module"**
- Solution: Run from project root directory where `src/pogadane/` exists

**Error: "Failed to execute script"**
- Solution: Check `hiddenimports` in `pogadane.spec` - may be missing a module

### Runtime Errors

**Error: "Configuration file not found"**
- Expected on first run - app will create default config
- Check `%USERPROFILE%\.pogadane\` directory

**Error: "Transcription provider not available"**
- User needs to install `faster-whisper` or `openai-whisper`
- Show message in GUI: "Run: pip install faster-whisper"

**Error: "Google API key not configured"**
- User needs to set API key in settings
- Or install Ollama for local AI

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build Executable

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build executable
        run: pyinstaller pogadane.spec --clean
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: Pogadane-Windows
          path: dist/Pogadane.exe
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        if: startsWith(github.ref, 'refs/tags/')
        with:
          files: dist/Pogadane.exe
```

---

## Performance Considerations

### Startup Time

- **Single-file exe:** 3-5 seconds (unpacks to temp directory)
- **Directory distribution:** 1-2 seconds (faster)

**Trade-off:** Single file is more portable, directory is faster

### File Size

| Configuration | Size |
|--------------|------|
| Minimal (no AI libs) | ~80 MB |
| With Transformers | ~150 MB |
| With Transformers + PyTorch | ~600 MB |

**Recommendation:** Minimal build, let users install AI libraries separately

---

## Platform-Specific Builds

### Windows (This Guide)
- **Tool:** PyInstaller
- **Output:** `.exe`
- **Tested:** Windows 10/11

### macOS (Future)
- **Tool:** PyInstaller or py2app
- **Output:** `.app` bundle
- **Code signing:** Required for distribution

### Linux (Future)
- **Tool:** PyInstaller or AppImage
- **Output:** Binary or `.AppImage`
- **Dependencies:** User installs via package manager

---

## Alternatives to PyInstaller

### Nuitka
- Compiles Python to C++
- Faster runtime
- Smaller binaries
- More complex setup

```bash
pip install nuitka
python -m nuitka --standalone --onefile run_gui_flet.py
```

### cx_Freeze
- Cross-platform
- Simpler than PyInstaller
- Larger file sizes

```bash
pip install cx_Freeze
cxfreeze run_gui_flet.py --target-dir dist
```

---

## Best Practices

1. ✅ **Test the executable** on a clean Windows machine (no Python installed)
2. ✅ **Include README** with installation instructions for dependencies
3. ✅ **Version the executable** - include version in filename: `Pogadane-v0.1.8.exe`
4. ✅ **Sign the executable** (optional) - prevents Windows SmartScreen warnings
5. ✅ **Create installers** for professional distribution
6. ✅ **Document dependencies** clearly - what users need to install separately

---

## Security Note

**Antivirus False Positives:**

PyInstaller executables sometimes trigger antivirus warnings (false positives).

**Solutions:**
1. **Code signing** - Sign with a valid certificate
2. **VirusTotal submission** - Submit to VirusTotal to verify it's clean
3. **User education** - Explain in README that it's safe (open-source)

---

## Support

For build issues:
- Check PyInstaller docs: https://pyinstaller.org/
- File issue: https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues
- Include build log and error messages

---

**Last updated:** November 7, 2025
