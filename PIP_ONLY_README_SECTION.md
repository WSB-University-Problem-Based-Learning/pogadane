# Pogadane - 100% pip-based Installation

## Quick Start (Recommended)

Pogadane now uses **100% pip-installable dependencies**. No binary executables required!

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# 3. Install the package
pip install -e .

# 4. Install dependencies (choose one):

# Option A: Lightweight (faster install, ~500MB)
pip install openai-whisper yt-dlp transformers torch

# Option B: Full (faster transcription, ~1GB-3GB)
pip install faster-whisper openai-whisper yt-dlp transformers torch

# Option C: Use automated installer
python install.py --full
```

### Launch the GUI

```bash
python run_gui_flet.py
```

## Dependencies Overview

All dependencies are now installed via pip:

### Transcription Engines

1. **faster-whisper** (RECOMMENDED - 4x faster, GPU support)
   ```bash
   pip install faster-whisper
   ```
   - Config: `TRANSCRIPTION_PROVIDER = "faster-whisper"`
   - GPU support (CUDA)
   - Batching & VAD filtering
   - Device auto-detection

2. **openai-whisper** (Original, works everywhere)
   ```bash
   pip install openai-whisper
   ```
   - Config: `TRANSCRIPTION_PROVIDER = "whisper"`
   - Simpler, more compatible
   - Slower but reliable

### YouTube Downloads

```bash
pip install yt-dlp
```
- Config: `YT_DLP_PATH = "yt-dlp"`
- Cross-platform
- No exe needed!

### AI Summarization

1. **Ollama** (RECOMMENDED for Polish - requires separate install)
   - Install from: https://ollama.com/download
   - Then: `ollama pull gemma2:2b` or `ollama pull llama3.2:1b`
   - Config: `SUMMARY_PROVIDER = "ollama"`
   - Best for Polish language
   - Runs locally

2. **Transformers** (pip-based, English only)
   ```bash
   pip install transformers torch
   ```
   - Config: `SUMMARY_PROVIDER = "transformers"`
   - No extra setup needed
   - Works offline

3. **Google Gemini** (cloud-based)
   - Free API key from: https://aistudio.google.com
   - Config: `SUMMARY_PROVIDER = "google"`
   - Supports Polish

## Configuration

Create `.config/config.py`:

```python
# Transcription (pip: faster-whisper)
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_DEVICE = "auto"  # cuda, cpu, or auto
FASTER_WHISPER_COMPUTE_TYPE = "auto"  # float16, int8, or auto
FASTER_WHISPER_BATCH_SIZE = 0  # 0=no batching, >0 for speed
FASTER_WHISPER_VAD_FILTER = False  # Voice Activity Detection
WHISPER_MODEL = "turbo"  # tiny, base, small, medium, large, turbo
WHISPER_LANGUAGE = "Polish"

# Alternative: openai-whisper
# TRANSCRIPTION_PROVIDER = "whisper"
# WHISPER_DEVICE = "auto"

# YouTube (pip: yt-dlp)
YT_DLP_PATH = "yt-dlp"

# AI Summarization (Ollama recommended for Polish)
SUMMARY_PROVIDER = "ollama"
OLLAMA_MODEL = "gemma2:2b"  # or llama3.2:1b
SUMMARY_LANGUAGE = "Polish"

# Alternative: Transformers (English only)
# SUMMARY_PROVIDER = "transformers"
# TRANSFORMERS_MODEL = "facebook/bart-large-cnn"

# Alternative: Google Gemini
# SUMMARY_PROVIDER = "google"
# GOOGLE_API_KEY = "your-api-key-here"
```

## Troubleshooting

### Import errors
```bash
# Reinstall dependencies
pip install --upgrade faster-whisper openai-whisper yt-dlp transformers torch
```

### GPU not detected
```python
# In config.py:
FASTER_WHISPER_DEVICE = "cuda"  # Force GPU
# Or:
FASTER_WHISPER_DEVICE = "cpu"  # Force CPU
```

### Ollama not working
```bash
# Check if Ollama is running
ollama list

# Pull a model
ollama pull gemma2:2b

# Test it
ollama run gemma2:2b "Hello"
```

## Migration from Old exe-based Setup

If you're upgrading from the old exe-based system:

1. **Uninstall old binaries:**
   ```bash
   # Remove dep/ folder (no longer needed)
   rm -rf dep/
   ```

2. **Update config.py:**
   ```python
   # OLD (remove these):
   # FASTER_WHISPER_EXE = "dep/faster-whisper/faster-whisper-xxl.exe"
   # YT_DLP_EXE = "dep/yt-dlp/yt-dlp.exe"
   
   # NEW (use these):
   TRANSCRIPTION_PROVIDER = "faster-whisper"
   YT_DLP_PATH = "yt-dlp"
   ```

3. **Install pip packages:**
   ```bash
   pip install faster-whisper yt-dlp
   ```

See `PIP_ONLY_INSTALLATION.md` for detailed migration guide.

## What Changed?

### Before (exe-based)
- ❌ Manual download of faster-whisper-xxl.exe (1.5GB)
- ❌ Manual download of yt-dlp.exe
- ❌ Complex extraction with 7-Zip
- ❌ Platform-specific binaries
- ❌ dep/ folder management

### Now (pip-based)
- ✅ `pip install faster-whisper` (automatic)
- ✅ `pip install yt-dlp` (automatic)
- ✅ Cross-platform compatibility
- ✅ Automatic updates via pip
- ✅ No manual downloads

## Performance Comparison

| Engine | Speed | GPU Support | Installation |
|--------|-------|-------------|--------------|
| faster-whisper (pip) | ⚡⚡⚡⚡ (4x faster) | ✅ CUDA | `pip install` |
| openai-whisper (pip) | ⚡ (baseline) | ✅ CUDA | `pip install` |
| ~~faster-whisper-xxl.exe~~ | ⚡⚡⚡ | ❌ CPU only | DEPRECATED |

**Recommendation:** Use `faster-whisper` from pip for best performance!

## Documentation

- **PIP_ONLY_INSTALLATION.md** - Detailed installation guide
- **FASTER_WHISPER_LIBRARY.md** - faster-whisper technical details
- **GUI_QUICK_START.md** - GUI usage guide
- **README.md** - Full project documentation

## Support

- Issues: https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues
- Discussions: Check the repository for community support

---

**All dependencies are now 100% pip-installable! No exe files needed! 🎉**
