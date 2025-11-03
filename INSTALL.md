# Pogadane - Installation Guide

**Simple cross-platform installation for Pogadane with all dependencies!**

This guide shows you how to install Pogadane on Windows, macOS, or Linux with a single command.

---

## 🚀 Quick Start (Recommended)

### Simple One-Command Installation

```bash
# Windows (PowerShell):
python install.py

# macOS/Linux:
python3 install.py
```

The installer provides **three installation modes**:

1. **LIGHTWEIGHT** (~500MB-2GB)
   - Python-based Whisper for transcription
   - Transformers AI for summaries
   - No external binaries required
   - Works on all platforms

2. **FULL** (All Features)
   - Everything from LIGHTWEIGHT
   - yt-dlp for YouTube downloads
   - Platform-specific enhancements
   - Faster-Whisper (Windows only)
   - Ollama instructions (all platforms)

3. **DEV** (Development Mode)
   - Everything from FULL
   - Testing tools (pytest, pylint, black)
   - Development dependencies

### Quick Launch Scripts

**Windows:**
```powershell
# Just double-click:
install.bat

# Or run in PowerShell:
python install.py
```

**macOS/Linux:**
```bash
# Make executable (one time):
chmod +x install.sh

# Run installer:
./install.sh
```

---

## 📋 Installation Options

### Interactive Mode (Default)

```bash
python install.py
```

The installer will guide you through:
- Choosing installation mode
- Confirming download sizes
- Setting up configuration
- Verifying installation

### Non-Interactive Mode

```bash
# Lightweight installation (fastest):
python install.py --lightweight

# Full installation:
python install.py --full

# Development mode:
python install.py --dev
```

---

## 🎯 Which Mode Should I Choose?

### LIGHTWEIGHT - Best for:
- ✅ First-time users
- ✅ Limited disk space
- ✅ Cross-platform compatibility
- ✅ Quick setup (no external binaries)
- ✅ Python-only environment

**Includes:**
- OpenAI Whisper (Python) - 75MB to 3GB models
- Transformers + PyTorch - AI summarization
- All core functionality

**Download size:** ~500MB-2GB

### FULL - Best for:
- ✅ Advanced users
- ✅ YouTube transcription
- ✅ Best quality transcription (Faster-Whisper on Windows)
- ✅ Local AI with Ollama
- ✅ Maximum features

**Includes:**
- Everything from LIGHTWEIGHT
- yt-dlp for YouTube downloads
- Platform-specific binaries (Windows)
- Instructions for Faster-Whisper and Ollama

**Download size:** ~1-5GB (depending on platform)

### DEV - Best for:
- ✅ Contributors and developers
- ✅ Code testing
- ✅ Running test suite
- ✅ Code quality tools

**Includes:**
- Everything from FULL
- pytest, pylint, black
- Development dependencies

---

## 🖥️ Platform-Specific Features

### Windows
- Full support for all modes
- Faster-Whisper binary available (FULL mode)
- Ollama desktop app (instructions provided)

### macOS
- All modes supported
- Ollama via Homebrew (instructions provided)
- Faster-Whisper via package manager

### Linux
- All modes supported
- Ollama via curl script (instructions provided)
- Faster-Whisper via package manager

---

## 📦 What Gets Installed

### LIGHTWEIGHT Mode
```
Python Packages:
├── openai-whisper>=20230314    # Transcription
├── transformers>=4.30.0        # AI summarization
├── torch>=2.0.0                # ML framework
├── ttkbootstrap                # GUI
└── google-generativeai         # Optional cloud AI

Configuration:
└── .config/config.py (auto-generated)
```

### FULL Mode (adds to LIGHTWEIGHT)
```
Additional Packages:
└── yt-dlp                      # YouTube downloads (pip)

Windows-Specific (optional):
├── dep/yt-dlp/yt-dlp.exe      # YouTube downloader
└── Instructions for Faster-Whisper and Ollama

macOS/Linux:
└── Instructions for Ollama installation
```

### DEV Mode (adds to FULL)
```
Development Tools:
├── pytest                      # Testing framework
├── pylint                      # Code linter
└── black                       # Code formatter
```

---

## ✅ Verifying Installation

After installation, test that everything works:

### 1. Check Installation

The installer shows success messages. Look for:
```
✅ Installation Complete!

You can now run Pogadane:
  GUI:  python -m pogadane.gui
  CLI:  python -m pogadane.transcribe_summarize_working --help
```

### 2. Test the GUI

```bash
# Windows:
python -m pogadane.gui

# macOS/Linux:
python3 -m pogadane.gui
```

### 3. Test the CLI

```bash
# Windows:
python -m pogadane.transcribe_summarize_working --help

# macOS/Linux:
python3 -m pogadane.transcribe_summarize_working --help
```

---

## 🔧 Troubleshooting

### "Python is not recognized"

**Windows:**
- Reinstall Python from https://www.python.org/
- ✅ Check "Add Python to PATH" during installation
- Restart PowerShell/Command Prompt

**macOS/Linux:**
- Use `python3` instead of `python`
- Install Python via package manager:
  - macOS: `brew install python3`
  - Ubuntu/Debian: `sudo apt install python3 python3-pip`
  - Fedora: `sudo dnf install python3 python3-pip`

### "No module named 'transformers'"

**Solution:**
```bash
# Windows:
pip install -r requirements-transformers.txt

# macOS/Linux:
pip3 install -r requirements-transformers.txt
```

### "No module named 'whisper'"

**Solution:**
```bash
# Windows:
pip install -r requirements-whisper.txt

# macOS/Linux:
pip3 install -r requirements-whisper.txt
```

### Model downloads are slow

**This is normal!** Models are downloaded once on first use:
- Whisper models: 75MB (tiny) to 3GB (large)
- Transformers models: 300MB to 1.6GB
- Models are cached - subsequent runs are instant

**Speed up:** Choose smaller models in `.config/config.py`:
```python
WHISPER_MODEL = "tiny"  # or "base"
TRANSFORMERS_MODEL = "google/flan-t5-small"  # 300MB
```

### Permission errors (Linux/macOS)

```bash
# Give install.sh execute permission:
chmod +x install.sh

# Or run with python3:
python3 install.py
```

### Installation fails on Windows

Try running PowerShell as Administrator:
1. Right-click PowerShell
2. Select "Run as Administrator"
3. Run `python install.py` again

---

## 🔄 Updating Pogadane

### Update Code

```bash
git pull origin main
```

### Update Dependencies

```bash
# Re-run installer to update everything:
python install.py

# Or update just Python packages:
pip install --upgrade -r requirements.txt
```

---

## 🧹 Uninstalling

### Remove Python Packages

```bash
pip uninstall pogadane
pip uninstall openai-whisper transformers torch ttkbootstrap
```

### Remove Project

```bash
# Navigate to parent directory
cd ..

# Remove project folder
# Windows:
Remove-Item -Recurse -Force pogadane

# macOS/Linux:
rm -rf pogadane
```

---

## 📖 Next Steps

After successful installation:

1. **Configure your preferences:**
   - Edit `.config/config.py` or use GUI Settings tab
   - Choose AI provider (Transformers, Ollama, or Google Gemini)
   - Set your preferred language

2. **Try the GUI:**
   ```bash
   python -m pogadane.gui
   ```

3. **Or use CLI:**
   ```bash
   python -m pogadane.transcribe_summarize_working --help
   ```

4. **Read documentation:**
   - [Quick Start Guide](QUICK_START.md) - Beginner-friendly
   - [README.md](README.md) - Complete documentation
   - [Architecture](doc/ARCHITECTURE.md) - Technical details

---

## ❓ Getting Help

If you encounter issues:

1. **Check this guide** - Most issues covered above
2. **Check terminal output** - Look for error messages
3. **Try lightweight mode** - `python install.py --lightweight`
4. **GitHub Issues** - https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues
5. **Quick Start Guide** - [QUICK_START.md](QUICK_START.md)

---

## 🎉 Success!

If you see this after running the installer:

```
✅ Installation Complete!
```

**Congratulations!** Pogadane is ready to use. 🚀

Enjoy transcribing and summarizing! 🎤📝
