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

### Option 1: GUI Installer (Easiest!)

**NEW! User-friendly graphical installer with step-by-step wizard:**

```powershell
# Method 1: Double-click the batch file
# Just double-click: install.bat

# Method 2: Run from PowerShell
cd pogadane
python tools\install_gui.py
```

The GUI installer provides:
- ✅ Visual step-by-step wizard
- ✅ Checkbox options for components
- ✅ Real-time progress tracking
- ✅ Detailed installation logs
- ✅ Automatic configuration
- ✅ Launch button when complete

### Option 2: Command-Line Installer

**One command to install everything:**

```powershell
# From the pogadane directory
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

**Installation time:** 5-15 minutes (depending on internet speed and selected options)

### 🤖 AI Summarization Options

Pogadane supports **three AI providers** for generating summaries:

1. **Ollama** (default) - Full-featured local AI
   - ✅ Best quality
   - ✅ Multi-language support
   - ✅ Large model selection
   - ❌ Requires separate installation (~3GB download)

2. **Transformers** - Lightweight local AI (NEW!)
   - ✅ Works without Ollama
   - ✅ Pure Python (pip install)
   - ✅ GPU acceleration support
   - ⚠️ English summaries only
   - 📦 Models: 300MB - 1.6GB

3. **Google Gemini** - Cloud AI
   - ✅ No local installation
   - ✅ Multi-language support
   - ❌ Requires API key
   - ❌ Needs internet connection

**To use Transformers (no Ollama needed):**
```powershell
# Install transformers support
pip install -r requirements-transformers.txt

# Or manually:
pip install transformers torch

# Then in .config/config.py:
# SUMMARY_PROVIDER = "transformers"
```

---

### 🎙️ Transcription Options

Pogadane supports **two transcription engines**:

1. **Faster-Whisper** (default) - High-quality external binary
   - ✅ Best accuracy
   - ✅ GPU acceleration
   - ✅ Speaker diarization support
   - ❌ Requires ~1.5GB download
   - ❌ Windows executable needed

2. **Whisper** (Python) - Lightweight Python library (NEW!)
   - ✅ Pure Python (pip install)
   - ✅ No external executables
   - ✅ GPU acceleration support
   - ✅ Models: 75MB - 3GB (smaller options available)
   - ⚠️ No speaker diarization

**To use Whisper (Python):**
```powershell
# Install Whisper support
pip install -r requirements-whisper.txt

# Then in .config/config.py:
# TRANSCRIPTION_PROVIDER = "whisper"
# WHISPER_MODEL = "base"  # or "tiny", "small", "medium", "large"
```

---

## 📋 Installation Options

### Full Installation (with Ollama)

```powershell
python tools/install.py
```

### Skip Ollama (Use Alternative AI)

```powershell
# Option A: Use Transformers (lightweight local AI, no Ollama)
python tools/install.py --no-ollama
pip install -r requirements-transformers.txt
# Then set SUMMARY_PROVIDER = "transformers" in .config/config.py

# Option B: Use Google Gemini (cloud AI)
python tools/install.py --no-ollama
# Then set SUMMARY_PROVIDER = "google" and add your API key in .config/config.py
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

### "py7zr extraction failed: BCJ2 filter is not supported"

**Problem:** py7zr can't extract Faster-Whisper archive (BCJ2 compression not supported)

**Solution - Automatic (Recommended):**
```powershell
# Use our helper script (requires 7-Zip installed)
python tools/extract_faster_whisper.py
```

**Solution - Manual:**
```powershell
# 1. Install 7-Zip from: https://www.7-zip.org/

# 2. Extract the archive:
# Right-click on dep/faster-whisper/Faster-Whisper-XXL_r245.4_windows.7z
# Select: 7-Zip → Extract Here

# 3. Find faster-whisper-xxl.exe in the extracted folders

# 4. Copy it to:
#    dep/faster-whisper/faster-whisper-xxl.exe

# 5. Delete the extracted folders and .7z file
```

**Note:** The automatic installer will try to use 7-Zip command-line if available, but if py7zr fails and 7-Zip is not installed, you'll need to extract manually.

### "No module named 'transformers'" or "No module named 'torch'"

**Problem:** Using SUMMARY_PROVIDER="transformers" but libraries not installed

**Solution:**
```powershell
# Install transformers support
pip install -r requirements-transformers.txt

# Or manually install
pip install transformers torch

# Verify installation
python -c "import transformers; print('OK')"
```

**GPU Acceleration (Optional):**
```powershell
# For NVIDIA GPUs with CUDA support
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Transformers model download is slow

**Problem:** First-time model download takes long time

**Solution:**
This is normal! Models are 300MB-1.6GB and download from Hugging Face.
- Default model (BART): ~1.6GB
- Smaller alternative: Change to `"google/flan-t5-small"` in config (~300MB)
- Models cache in `~/.cache/huggingface/` - only downloaded once

**Speed up:**
```powershell
# Use smaller, faster model in .config/config.py:
TRANSFORMERS_MODEL = "google/flan-t5-small"
```

### "No module named 'whisper'" or Whisper transcription fails

**Problem:** Using TRANSCRIPTION_PROVIDER="whisper" but library not installed

**Solution:**
```powershell
# Install Whisper support
pip install -r requirements-whisper.txt

# Or manually install
pip install openai-whisper

# Verify installation
python -c "import whisper; print('OK')"
```

**GPU Acceleration (Optional):**
```powershell
# For NVIDIA GPUs with CUDA support
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Whisper model download is slow

**Problem:** First-time Whisper model download takes time

**Solution:**
This is normal! Whisper models are downloaded on first use:
- tiny: ~75MB (fastest, basic quality)
- base: ~150MB (recommended for lightweight)
- small: ~500MB (balanced)
- medium: ~1.5GB (high quality)
- large: ~3GB (best quality)

Models cache in `~/.cache/whisper/` - only downloaded once.

**Speed up:**
```powershell
# Use smaller model in .config/config.py:
TRANSCRIPTION_PROVIDER = "whisper"
WHISPER_MODEL = "tiny"  # or "base" for better quality
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

### Ollama installation fails or not detected

**Problem:** Automatic Ollama setup didn't work or shows as "Missing" after installation

**Solution:**
```powershell
# Option 1: Install manually from downloaded file
# The installer was downloaded to: dep/ollama/ollama_setup.exe
# Just double-click it to install

# Option 2: Download fresh from website
# 1. Visit https://ollama.com/
# 2. Download Ollama for Windows
# 3. Run installer
# 4. Download model:
ollama pull gemma3:4b

# Verify installation:
ollama --version
ollama list
```

**Note:** Ollama verification might show "Missing" because it's an installer, not a standalone exe. As long as `ollama --version` works in your terminal, it's installed correctly.

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
