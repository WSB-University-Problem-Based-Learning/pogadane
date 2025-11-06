# Pogadane - Pip-Only Installation Guide

## Overview

Pogadane now works **100% with pip components** - no external executables required! 🎉

All dependencies are Python packages installable via pip:
- ✅ **faster-whisper** - High-performance transcription (recommended)
- ✅ **openai-whisper** - Alternative transcription backend
- ✅ **yt-dlp** - YouTube video downloads
- ✅ **flet** - Material 3 GUI
- ✅ **google-generativeai** - Gemini AI summaries

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Base Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Transcription Backend

Choose one:

#### Option A: Faster-Whisper (Recommended - 4x faster!)

```bash
pip install faster-whisper
```

**Benefits:**
- 4x faster than openai-whisper
- Lower memory usage
- GPU acceleration (with CUDA)
- Batched transcription support

**GPU Support (Optional):**
- Requires NVIDIA GPU + CUDA 12 + cuDNN 9
- See: https://github.com/SYSTRAN/faster-whisper#gpu

#### Option B: OpenAI Whisper (Lightweight)

```bash
pip install openai-whisper
```

**Benefits:**
- Simpler installation
- No GPU dependencies
- Good for CPU-only systems

### 5. Install YouTube Downloader

```bash
pip install yt-dlp
```

Or use the system package manager:
```bash
# Windows (winget)
winget install yt-dlp.yt-dlp

# macOS (homebrew)
brew install yt-dlp

# Linux (apt)
sudo apt install yt-dlp
```

### 6. Install AI Summary Backend (Choose One)

#### Option A: Ollama (Recommended - Local & Private)

1. Install Ollama: https://ollama.com/
2. Pull a model:
   ```bash
   ollama pull gemma3:4b
   ```

#### Option B: Google Gemini (Cloud-based)

Get API key from: https://aistudio.google.com/apikey

Set in config:
```python
GOOGLE_API_KEY = "your-api-key"
SUMMARY_PROVIDER = "google"
```

#### Option C: Transformers (Fully Local)

```bash
pip install transformers torch
```

Set in config:
```python
SUMMARY_PROVIDER = "transformers"
```

### 7. Run Pogadane

```bash
python run_gui_flet.py
```

## Complete Installation (All Features)

Install everything at once:

```bash
# Base + all transcription backends + transformers
pip install -e .[all]

# Or individually
pip install -e .[faster-whisper]  # Recommended transcription
pip install -e .[whisper]          # Alternative transcription
pip install -e .[transformers]     # Local AI summarization
```

## Configuration

Default config works out of the box! Optional tweaks in `.config/config.py`:

### Transcription Settings

```python
# Use faster-whisper (default)
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_DEVICE = "auto"  # "cuda" for GPU, "cpu" for CPU
FASTER_WHISPER_COMPUTE_TYPE = "auto"  # "float16" (GPU) or "int8" (CPU)
FASTER_WHISPER_BATCH_SIZE = 0  # Set to 8-16 for speed boost!
WHISPER_MODEL = "turbo"  # tiny, base, small, medium, large-v3, turbo
WHISPER_LANGUAGE = "Polish"

# Or use openai-whisper
# TRANSCRIPTION_PROVIDER = "whisper"
# WHISPER_DEVICE = "auto"
```

### Summary Settings

```python
# Ollama (default)
SUMMARY_PROVIDER = "ollama"
OLLAMA_MODEL = "gemma3:4b"

# Or Google Gemini
# SUMMARY_PROVIDER = "google"
# GOOGLE_API_KEY = "your-key"

# Or Transformers
# SUMMARY_PROVIDER = "transformers"
# TRANSFORMERS_MODEL = "facebook/bart-large-cnn"
```

### YouTube Downloads

```python
# If yt-dlp is in PATH
YT_DLP_PATH = "yt-dlp"

# Or specify full path
# YT_DLP_PATH = "C:/path/to/yt-dlp.exe"
```

## Performance Optimization

### GPU Acceleration (Faster-Whisper)

```python
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_DEVICE = "cuda"
FASTER_WHISPER_COMPUTE_TYPE = "float16"
FASTER_WHISPER_BATCH_SIZE = 16  # Faster transcription!
```

**Requirements:**
- NVIDIA GPU with CUDA support
- CUDA 12: https://developer.nvidia.com/cuda-downloads
- cuDNN 9: https://developer.nvidia.com/cudnn

### CPU Optimization (Faster-Whisper)

```python
FASTER_WHISPER_DEVICE = "cpu"
FASTER_WHISPER_COMPUTE_TYPE = "int8"  # Less memory, faster
FASTER_WHISPER_BATCH_SIZE = 8
WHISPER_MODEL = "small"  # Smaller = faster
```

### Batched Transcription

```python
# Dramatically faster transcription
FASTER_WHISPER_BATCH_SIZE = 16  # GPU: 8-16
# FASTER_WHISPER_BATCH_SIZE = 8   # CPU: 4-8
```

**Speed comparison (large-v3 model):**
- No batching: 1m03s
- Batch size 8: **17s** (3.7x faster!)

## Dependencies Overview

### Core (Always Required)

```
flet>=0.24.0              # Material 3 GUI
google-generativeai       # Gemini API (for summaries)
py7zr                     # Archive extraction
yt-dlp                    # YouTube downloads
```

### Transcription (Choose One)

```
faster-whisper>=1.0.0     # Recommended (4x faster)
openai-whisper            # Alternative (lighter)
```

### AI Summary (Choose One or More)

```
# Ollama - External tool (https://ollama.com/)
# Google Gemini - API key required
transformers              # Local Hugging Face models
torch                     # Required for transformers
```

## Troubleshooting

### faster-whisper Not Found

```
❌ Error: faster-whisper library not installed.
```

**Solution:**
```bash
pip install faster-whisper
```

### GPU Not Detected

**Check CUDA:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**If False:**
1. Install CUDA 12: https://developer.nvidia.com/cuda-downloads
2. Install cuDNN 9: https://developer.nvidia.com/cudnn
3. Reinstall PyTorch with CUDA: https://pytorch.org/get-started/locally/

### Out of Memory (GPU)

```python
# Reduce batch size or use int8
FASTER_WHISPER_BATCH_SIZE = 4
FASTER_WHISPER_COMPUTE_TYPE = "int8_float16"

# Or use smaller model
WHISPER_MODEL = "small"
```

### yt-dlp Not Found

**Install via pip:**
```bash
pip install yt-dlp
```

**Or download binary:**
- Windows: https://github.com/yt-dlp/yt-dlp/releases
- Place in PATH or specify full path in config

### Slow CPU Transcription

```python
# Use int8 quantization
FASTER_WHISPER_COMPUTE_TYPE = "int8"
FASTER_WHISPER_BATCH_SIZE = 8
WHISPER_MODEL = "small"  # Or "tiny" for max speed
```

## Migration from Binary Dependencies

### Old Way (Executables)

```python
FASTER_WHISPER_EXE = "dep/faster-whisper/faster-whisper-xxl.exe"
YT_DLP_EXE = "dep/yt-dlp/yt-dlp.exe"
```

### New Way (Pip Only)

```bash
pip install faster-whisper yt-dlp
```

```python
TRANSCRIPTION_PROVIDER = "faster-whisper"
YT_DLP_PATH = "yt-dlp"
```

**No downloads, no manual extraction, no platform-specific binaries!**

## Minimal Installation (Fastest Setup)

For testing or lightweight systems:

```bash
# 1. Core only
pip install -r requirements.txt

# 2. Minimal transcription
pip install openai-whisper

# 3. Skip YouTube support (process local files only)
# No yt-dlp needed!

# 4. Use Ollama for summaries (external tool)
# Install: https://ollama.com/
```

## Development Installation

```bash
# Install with dev dependencies
pip install -r requirements-dev.txt

# Or specific groups
pip install -e .[dev]              # Development tools
pip install -e .[test]             # Testing tools
pip install -e .[all]              # Everything
```

## Platform-Specific Notes

### Windows

```powershell
# Virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install
pip install faster-whisper yt-dlp

# Run
python run_gui_flet.py
```

### macOS/Linux

```bash
# Virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install faster-whisper yt-dlp

# Run
python run_gui_flet.py
```

## Testing Installation

```bash
# Run integration test
python test_faster_whisper_integration.py
```

Expected output:
```
✅ PASS: Configuration
✅ PASS: Provider Creation
✅ PASS: Factory Auto-Selection
```

## Summary

✅ **100% pip-based** - No external executables  
✅ **Cross-platform** - Works on Windows, macOS, Linux  
✅ **Simple installation** - Just `pip install`  
✅ **Fast performance** - 4x faster with faster-whisper  
✅ **Flexible** - Multiple backend options  
✅ **Modern** - Latest Python libraries  

**Total install time:** ~2 minutes  
**External downloads:** 0  
**Manual configuration:** Optional  

🎉 **Just install and run!**
