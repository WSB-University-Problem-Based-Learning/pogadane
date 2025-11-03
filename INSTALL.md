# Pogadane - Automatic Installation Guide

**One-command installation for Pogadane with all dependencies!**

This guide shows you how to install Pogadane with a single command that handles everything automatically:
- ✅ Python package dependencies
- ✅ External binaries (yt-dlp, Faster-Whisper)
- ✅ Ollama AI (optional)
- ✅ Configuration setup
- ✅ Directory structure

---

## 🚀 Quick Start (Recommended)

### Windows PowerShell

```powershell
# 1. Clone or download Pogadane
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Run ONE COMMAND to install everything
python tools/install.py
```

That's it! The installer will:
1. Check your Python version (3.7+ required)
2. Upgrade pip to latest version
3. Install all Python packages
4. Download yt-dlp.exe to `dep/yt-dlp/`
5. Download and extract Faster-Whisper-XXL to `dep/faster-whisper/`
6. Download Ollama installer (optional)
7. Update configuration with correct paths
8. Verify everything is installed correctly

**Installation time:** 5-15 minutes (depending on internet speed)

---

## 📋 Installation Options

### Full Installation (with Ollama)

```powershell
python tools/install.py
```

### Skip Ollama (Use Google Gemini API Instead)

```powershell
python tools/install.py --no-ollama
```

### Include Development Tools

```powershell
python tools/install.py --dev
```

### Combination

```powershell
python tools/install.py --no-ollama --dev
```

---

## 📁 Where Files Are Installed

The installer creates this clean structure:

```
pogadane/
├── dep/                          # External dependencies (NOT in Git)
│   ├── yt-dlp/
│   │   └── yt-dlp.exe           # YouTube downloader
│   ├── faster-whisper/
│   │   └── faster-whisper-xxl.exe  # Transcription engine
│   └── ollama/
│       └── OllamaSetup.exe      # Ollama installer (if requested)
│
├── .config/
│   └── config.py                # Auto-updated with correct paths
│
├── src/pogadane/                # Your repository code
├── test/                        # Your tests
├── tools/                       # Installation tools
└── ...
```

**Key Benefits:**
- 🔒 **Clean repository**: No binaries in Git, only in `dep/` (gitignored)
- 📦 **Organized structure**: All external tools in one place
- ⚙️ **Auto-configuration**: Paths automatically updated in config
- 🔄 **Easy updates**: Re-run installer to update components

---

## 🛠️ Manual Installation (Advanced)

If automatic installation fails, you can install components manually:

### Step 1: Python Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: External Dependencies

```powershell
# Install just external binaries
python tools/dependency_manager.py

# Or install specific component
python tools/dependency_manager.py --install yt-dlp
python tools/dependency_manager.py --install faster-whisper

# Verify installation
python tools/dependency_manager.py --verify-only
```

### Step 3: Install Package (Optional)

```powershell
# Install as editable package (recommended for development)
pip install -e .

# Or regular install
pip install .
```

---

## ✅ Verifying Installation

After installation, verify everything works:

### 1. Check Dependencies

```powershell
python tools/dependency_manager.py --verify-only
```

You should see:
```
✅ Installed - yt-dlp (YouTube Downloader) (Required)
  📁 Location: dep\yt-dlp\yt-dlp.exe

✅ Installed - Faster-Whisper-XXL (Transcription Engine) (Required)
  📁 Location: dep\faster-whisper\faster-whisper-xxl.exe

✅ Installed - Ollama (Local AI) (Optional)
  📁 Location: dep\ollama\OllamaSetup.exe
```

### 2. Test the Application

```powershell
# Test GUI
python -m pogadane.gui

# Or if installed as package
pogadane-gui
```

### 3. Run Sample Test

```powershell
# Test with included sample audio
python -m pogadane.transcribe_summarize_working "samples/Styrta się pali.mp3"
```

---

## 🔧 Troubleshooting

### "Python not recognized"

**Problem:** Windows can't find Python

**Solution:**
1. Reinstall Python from https://www.python.org/
2. ✅ **Check "Add Python to PATH"** during installation
3. Restart PowerShell

### "Import setuptools could not be resolved"

**Problem:** Lint warning (harmless)

**Solution:** This is just a warning. Installation will work fine.

```powershell
# If you want to fix it:
pip install setuptools
```

### "py7zr import error"

**Problem:** Can't extract Faster-Whisper archive

**Solution:**
```powershell
# Install py7zr
pip install py7zr

# Or extract manually:
# 1. Download 7-Zip: https://www.7-zip.org/
# 2. Extract Faster-Whisper-XXL_r245.4_windows.7z
# 3. Copy faster-whisper-xxl.exe to dep/faster-whisper/
```

### "Permission denied" errors

**Problem:** Windows blocking downloads or file operations

**Solution:**
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as Administrator"

# Then run installer again
python tools/install.py
```

### Ollama installation fails

**Problem:** Automatic Ollama setup didn't work

**Solution:**
```powershell
# Download and install manually:
# 1. Visit https://ollama.com/
# 2. Download Ollama for Windows
# 3. Run installer
# 4. Download model:
ollama pull gemma3:4b
```

### Config file not updated

**Problem:** Paths in `.config/config.py` still point to current directory

**Solution:**
```powershell
# Manually update paths in .config/config.py:
FASTER_WHISPER_EXE = r"dep\faster-whisper\faster-whisper-xxl.exe"
YT_DLP_EXE = r"dep\yt-dlp\yt-dlp.exe"
```

### Internet connection issues

**Problem:** Downloads fail due to network issues

**Solution:**
```powershell
# Retry installation
python tools/install.py

# Or download manually:
# yt-dlp: https://github.com/yt-dlp/yt-dlp/releases/latest
# Faster-Whisper: https://github.com/Purfview/whisper-standalone-win/releases
```

---

## 🔄 Updating Pogadane

### Update Repository Code

```powershell
git pull origin main
```

### Update External Dependencies

```powershell
# Re-run installer to update all components
python tools/install.py

# Or update specific component
python tools/dependency_manager.py --install yt-dlp
```

### Update Python Packages

```powershell
pip install --upgrade -r requirements.txt
```

---

## 🧹 Uninstalling

### Remove External Dependencies

```powershell
# Simply delete the dep/ folder
Remove-Item -Recurse -Force dep/
```

### Uninstall Python Package

```powershell
pip uninstall pogadane
```

### Complete Removal

```powershell
# Remove entire pogadane directory
cd ..
Remove-Item -Recurse -Force pogadane/
```

---

## 📖 Next Steps

After successful installation:

1. **Configure your preferences:**
   - Open `.config/config.py` or use the GUI Settings tab
   - Choose LLM provider (Ollama local or Google Gemini API)
   - Set your preferred language

2. **Try the GUI:**
   ```powershell
   python -m pogadane.gui
   ```

3. **Or use CLI:**
   ```powershell
   python -m pogadane.transcribe_summarize_working --help
   ```

4. **Read documentation:**
   - [Quick Start Guide](QUICK_START.md) - Beginner-friendly guide
   - [README.md](README.md) - Complete documentation
   - [Architecture](doc/ARCHITECTURE.md) - Technical details

---

## 🎯 Installation Methods Comparison

| Method | Best For | Command |
|--------|----------|---------|
| **Automatic (Recommended)** | Everyone | `python tools/install.py` |
| **No Ollama** | Using Google Gemini API | `python tools/install.py --no-ollama` |
| **Development** | Contributors | `python tools/install.py --dev` |
| **Manual Components** | Troubleshooting | `python tools/dependency_manager.py` |
| **Python Only** | Advanced users | `pip install -r requirements.txt` |

---

## ❓ Getting Help

If you encounter issues:

1. **Check this guide** - Most issues are covered in Troubleshooting
2. **Run verification** - `python tools/dependency_manager.py --verify-only`
3. **Check logs** - Look for error messages in terminal output
4. **GitHub Issues** - https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues
5. **Quick Start Guide** - [QUICK_START.md](QUICK_START.md) for beginners

---

## 🎉 Success!

If you see this after running the installer:

```
✅ Installation Complete!

You can now run Pogadane:
  GUI:  python -m pogadane.gui
  CLI:  python -m pogadane.transcribe_summarize_working --help
```

**Congratulations!** Pogadane is ready to use. 🚀

Enjoy transcribing and summarizing! 🎤📝
