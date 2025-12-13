# Cross-Platform Compatibility Guide

## Platform Support Status

Pogadane is designed to work on **Windows, Linux, and macOS** with the same codebase.

### ✅ Fully Supported Platforms

| Platform | Python | Transcription | AI Summary | GUI | Status |
|----------|--------|---------------|------------|-----|--------|
| **Windows 10/11** | ✅ 3.7+ | ✅ faster-whisper, whisper | ✅ All providers | ✅ Flet | **Fully Tested** |
| **macOS** | ✅ 3.7+ | ✅ faster-whisper, whisper | ✅ All providers | ✅ Flet | **Compatible** |
| **Linux** | ✅ 3.7+ | ✅ faster-whisper, whisper | ✅ All providers | ✅ Flet | **Compatible** |

---

## Installation by Platform

### Windows

```powershell
# 1. Clone repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Run installer (installs all dependencies)
python install.py

# 4. Launch GUI
python run_gui_flet.py
```

### macOS

```bash
# 1. Clone repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Run installer (installs all dependencies)
python install.py

# 4. Launch GUI
python run_gui_flet.py
```

**macOS-specific notes:**
- Use `python3` and `pip3` instead of `python`/`pip`
- For faster-whisper GPU support: Install Metal framework dependencies
- For Ollama: `brew install ollama` or download from ollama.com

### Linux (Ubuntu/Debian)

```bash
# 1. Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg

# 2. Clone repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 3. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Run installer (installs all dependencies)
python install.py

# 5. Launch GUI
python run_gui_flet.py
```

**Linux-specific notes:**
- Install `ffmpeg` for audio processing: `sudo apt install ffmpeg`
- For Ollama: `curl https://ollama.ai/install.sh | sh`
- For faster-whisper GPU support: Install CUDA toolkit

---

## Platform-Specific Features

### Subprocess Console Handling

**Windows**: The GUI automatically hides console windows when running external commands
```python
# Handled internally in file_utils.py
if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.wShowWindow = subprocess.SW_HIDE
```

**Linux/macOS**: Console hiding not needed (no separate windows)

### Path Handling

All paths use `pathlib.Path` for cross-platform compatibility:
```python
# ✅ Cross-platform (works everywhere)
from pathlib import Path
config_path = Path.home() / ".config" / "pogadane" / "config.py"

# ❌ Windows-only (don't do this)
config_path = "C:\\Users\\user\\.config\\pogadane\\config.py"
```

### File Separators

The project automatically handles path separators:
- Windows: `\` (backslash)
- Linux/macOS: `/` (forward slash)
- **No manual separator handling needed** - `pathlib` does this automatically

---

## Transcription Engines

### faster-whisper (Recommended)

**All Platforms:**
```bash
pip install faster-whisper
```

**GPU Support:**
- **Windows**: CUDA toolkit from NVIDIA
- **Linux**: `pip install faster-whisper[cuda]`
- **macOS**: Metal framework (built-in on M1/M2)

### OpenAI Whisper (Fallback)

**All Platforms:**
```bash
pip install openai-whisper
```

**Notes:**
- Slower than faster-whisper but works everywhere
- CPU-only on macOS Intel chips
- Requires `ffmpeg` (install via package manager)

---

## AI Summary Providers

### Ollama (Recommended for Polish)

**Installation:**
- **Windows**: Download from https://ollama.com/download
- **macOS**: `brew install ollama` or download installer
- **Linux**: `curl https://ollama.ai/install.sh | sh`

**Starting Ollama:**
```bash
ollama serve  # All platforms
```

### Transformers (English only)

**All Platforms:**
```bash
pip install transformers torch
```

**GPU Support:**
- **Windows/Linux**: CUDA-enabled PyTorch
- **macOS**: MPS (Metal Performance Shaders) on M1/M2

### Google Gemini (Cloud)

**All Platforms:**
- Works everywhere with internet connection
- Requires API key from Google AI Studio
- Configure in `.config/config.py`

---

## Known Platform Differences

### 1. Virtual Environment Activation

| Platform | Command |
|----------|---------|
| **Windows PowerShell** | `.\.venv\Scripts\Activate.ps1` |
| **Windows CMD** | `.\.venv\Scripts\activate.bat` |
| **macOS/Linux Bash** | `source .venv/bin/activate` |
| **macOS/Linux Fish** | `source .venv/bin/activate.fish` |

### 2. Python Command

| Platform | Command |
|----------|---------|
| **Windows** | `python` |
| **macOS/Linux** | `python3` (or `python` if aliased) |

### 3. Audio Libraries

**FFmpeg required for all platforms:**
- **Windows**: Included with whisper installation, or download from ffmpeg.org
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) or `sudo yum install ffmpeg` (RHEL/CentOS)

### 4. GUI Framework (Flet)

**All Platforms:**
- Flet works consistently across Windows, macOS, and Linux
- Uses native rendering on each platform
- Material Design 3 components work identically

---

## Troubleshooting

### Windows

**Issue**: `pip install` fails with SSL errors
- **Fix**: Upgrade pip: `python -m pip install --upgrade pip`

**Issue**: Console windows flash during transcription
- **Fix**: This is automatically handled by `file_utils.py`

### macOS

**Issue**: "python: command not found"
- **Fix**: Use `python3` instead of `python`

**Issue**: Permission denied when installing packages
- **Fix**: Don't use `sudo` with pip in virtual environments

**Issue**: GUI doesn't launch on Apple Silicon (M1/M2)
- **Fix**: Ensure you're using native ARM Python, not Rosetta

### Linux

**Issue**: Missing FFmpeg
- **Fix**: `sudo apt install ffmpeg`

**Issue**: "No module named 'tkinter'"
- **Fix**: `sudo apt install python3-tk`

**Issue**: GUI font rendering issues
- **Fix**: Install Microsoft fonts: `sudo apt install ttf-mscorefonts-installer`

### All Platforms

**Issue**: Out of memory during transcription
- **Fix**: Use smaller Whisper model (`base` or `small` instead of `large`)

**Issue**: Slow transcription
- **Fix**: Install faster-whisper with GPU support, or use smaller model

---

## Testing on Different Platforms

### Running Tests

```bash
# All platforms
pytest

# With coverage
pytest --cov=src/pogadane

# Specific test file
pytest test/test_file_utils.py
```

### Platform-Specific Test Notes

- **Windows paths in tests**: Test files contain Windows path strings (e.g., `C:\Users\...`) but this is just test data, not actual file operations
- **All tests should pass on all platforms** - Path handling is abstracted via `pathlib`

---

## Configuration Files

### `.config/config.py`

**All Platforms** - Use forward slashes or `Path` objects:
```python
# ✅ Cross-platform
from pathlib import Path
GGUF_MODEL_PATH = str(Path("dep/models/gemma-3-4b-it-Q4_K_M.gguf"))

# ✅ Also works
GGUF_MODEL_PATH = "dep/models/gemma-3-4b-it-Q4_K_M.gguf"

# ❌ Windows-only (avoid)
GGUF_MODEL_PATH = r"dep\models\gemma-3-4b-it-Q4_K_M.gguf"
```

### `.config/settings.json`

**Runtime Preferences** - Platform-agnostic JSON:
```json
{
  "THEME_MODE": "dark"
}
```

---

## Contributing Cross-Platform Code

### Best Practices

1. **Always use `pathlib.Path`** for file operations:
   ```python
   from pathlib import Path
   config_dir = Path.home() / ".config" / "pogadane"
   ```

2. **Detect platform when needed**:
   ```python
   import platform
   if platform.system() == "Windows":
       # Windows-specific code
   elif platform.system() == "Darwin":
       # macOS-specific code
   elif platform.system() == "Linux":
       # Linux-specific code
   ```

3. **Use `os.name` for simple checks**:
   ```python
   import os
   if os.name == 'nt':  # Windows
       # Windows-specific subprocess handling
   ```

4. **Subprocess with platform handling**:
   ```python
   from pogadane.file_utils import run_subprocess
   # Automatically handles console hiding on Windows
   result = run_subprocess(["command", "arg1"], debug_mode=True)
   ```

5. **Avoid hardcoded paths**:
   ```python
   # ❌ Don't do this
   path = "C:\\Users\\user\\file.txt"
   
   # ✅ Do this
   from pathlib import Path
   path = Path.home() / "file.txt"
   ```

---

## Summary

**Pogadane is cross-platform ready!**

- ✅ Core codebase uses `pathlib` for all paths
- ✅ Platform detection implemented correctly
- ✅ Subprocess handling accounts for Windows/Unix differences
- ✅ Installation works on all platforms via `install.py`
- ✅ All dependencies available via pip on all platforms

**Recommended workflow:**
1. Use `python install.py --lightweight` on all platforms
2. Configure `.config/config.py` with platform-agnostic paths
3. Install Ollama separately from official sources
4. Run `python run_gui_flet.py` on any platform

For questions or platform-specific issues, please file an issue on GitHub.
