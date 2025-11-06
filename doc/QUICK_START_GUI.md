# Quick Start - 100% GUI-Based Pogadane

## Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment
python -m venv .venv

# 3. Activate (Windows)
.venv\Scripts\activate

# Or activate (macOS/Linux)
# source .venv/bin/activate

# 4. Install dependencies
pip install -e .
pip install faster-whisper openai-whisper yt-dlp transformers torch

# 5. Launch GUI
python run_gui_flet.py
```

## First Use

### 1. Start the GUI
```bash
python run_gui_flet.py
```

### 2. Add Files
- Click "Dodaj plik(i)" button in "Kolejka zadań" tab
- Select one or more audio files (.mp3, .wav, .m4a, etc.)
- Or paste YouTube URL in URL field and click "Dodaj URL"

### 3. Configure (Optional)
- Go to "Konsola" tab → Settings (⚙️) icon
- Choose transcription engine: `faster-whisper` (recommended) or `whisper`
- Choose AI provider: `transformers` (offline) or `ollama` (better Polish)
- Click "Zapisz konfigurację"

### 4. Process
- Go back to "Kolejka zadań" tab
- Click "Rozpocznij przetwarzanie" button
- Watch progress in console output

### 5. View Results
- Go to "Przeglądarka Wyników" tab
- Select processed file from dropdown
- View transcription and summary

## What Happens on First Run?

### Models Download Automatically

When you first process a file with **transformers** provider:

```
🔄 Summarizing 'filename' with Transformers (facebook/bart-large-cnn)
   Loading model 'facebook/bart-large-cnn' from C:\...\pogadane\dep\models
   (First time may take a few minutes to download...)
```

**Download size:** ~1.6GB for `facebook/bart-large-cnn`

**Download location:** `pogadane/dep/models/` (in your project folder)

**Subsequent runs:** Instant loading from cache, no download needed!

## Configuration Examples

### Fast & Offline (Recommended for Testing)

```python
# .config/config.py

# Transcription
TRANSCRIPTION_PROVIDER = "whisper"  # Faster install, smaller models
WHISPER_MODEL = "base"  # ~140MB
WHISPER_LANGUAGE = "Polish"
WHISPER_DEVICE = "cpu"

# AI Summary
SUMMARY_PROVIDER = "transformers"
TRANSFORMERS_MODEL = "sshleifer/distilbart-cnn-12-6"  # Only ~500MB!
SUMMARY_LANGUAGE = "English"
```

### Best Quality (Recommended for Production)

```python
# .config/config.py

# Transcription
TRANSCRIPTION_PROVIDER = "faster-whisper"  # 4x faster!
FASTER_WHISPER_DEVICE = "cuda"  # Use GPU
FASTER_WHISPER_COMPUTE_TYPE = "float16"
WHISPER_MODEL = "large-v3"
WHISPER_LANGUAGE = "Polish"

# AI Summary (Polish support)
SUMMARY_PROVIDER = "ollama"  # Install separately from ollama.com
OLLAMA_MODEL = "gemma2:2b"
SUMMARY_LANGUAGE = "Polish"
```

### Balanced (Good for Most Users)

```python
# .config/config.py

# Transcription
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_DEVICE = "auto"  # Auto-detect GPU
FASTER_WHISPER_COMPUTE_TYPE = "int8"  # Quantized for speed
WHISPER_MODEL = "turbo"
WHISPER_LANGUAGE = "Polish"

# AI Summary
SUMMARY_PROVIDER = "transformers"
TRANSFORMERS_MODEL = "facebook/bart-large-cnn"
SUMMARY_LANGUAGE = "English"
```

## Folder Structure After First Run

```
pogadane/
├── dep/
│   └── models/                    # ← Models cached here
│       ├── models--facebook--bart-large-cnn/
│       │   ├── snapshots/
│       │   └── [model files]
│       └── .gitkeep
├── .config/
│   └── config.py                  # Your settings
├── src/
│   └── pogadane/
│       ├── backend.py             # NEW: Direct backend
│       ├── gui_flet.py            # GUI
│       └── [other modules]
└── run_gui_flet.py                # Launch this!
```

## Common Tasks

### Process Local Audio File
1. Click "Dodaj plik(i)"
2. Select file
3. Click "Rozpocznij przetwarzanie"

### Process YouTube Video
1. Copy YouTube URL
2. Paste in URL field
3. Click "Dodaj URL"
4. Click "Rozpocznij przetwarzanie"

### Process Multiple Files (Batch)
1. Click "Dodaj plik(i)"
2. Select multiple files (Ctrl+Click or Shift+Click)
3. All files appear in queue
4. Click "Rozpocznij przetwarzanie" once
5. All files process automatically

### Export Results
1. Go to "Przeglądarka Wyników"
2. Select file from dropdown
3. Copy transcription/summary text
4. Or use "Zapisz jako..." to save to file

### Change Models
1. Go to "Konsola" tab
2. Click ⚙️ Settings
3. Change `TRANSFORMERS_MODEL` to:
   - `sshleifer/distilbart-cnn-12-6` - Faster, smaller
   - `google/flan-t5-small` - Very fast
   - `facebook/bart-large-cnn` - Best quality
4. Click "Zapisz konfigurację"
5. Restart GUI

## Troubleshooting

### Models Not Downloading?

**Check internet connection:**
```bash
ping huggingface.co
```

**Check model cache:**
```bash
ls -lh dep/models/
# or on Windows:
dir dep\models\
```

**Manually set cache:**
```python
# In config.py
TRANSFORMERS_CACHE_DIR = "C:/path/to/pogadane/dep/models"
```

### GUI Won't Start?

**Check Python version:**
```bash
python --version
# Need Python 3.10+
```

**Check dependencies:**
```bash
pip list | grep flet
pip list | grep transformers
```

**Reinstall:**
```bash
pip uninstall pogadane
pip install -e .
```

### Processing Fails?

**Check logs in Console tab** - detailed error messages shown

**Common issues:**
- Missing model: First run downloads automatically
- No GPU: Set `FASTER_WHISPER_DEVICE = "cpu"` in config
- Out of memory: Use smaller model (`base` instead of `large`)

### Slow Performance?

**Use faster-whisper:**
```python
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_COMPUTE_TYPE = "int8"  # Quantized
```

**Use smaller models:**
```python
WHISPER_MODEL = "turbo"  # or "base"
TRANSFORMERS_MODEL = "sshleifer/distilbart-cnn-12-6"
```

**Enable GPU:**
```python
FASTER_WHISPER_DEVICE = "cuda"
TRANSFORMERS_DEVICE = "cuda"
```

## Tips & Tricks

### Offline Use

After first download, models are cached locally:
- Disconnect internet
- GUI still works!
- Models load from `dep/models/`

### Portable Installation

Copy entire folder to USB drive:
```bash
xcopy pogadane E:\pogadane /E /I
# Now run on any computer!
```

### Multiple Configurations

Create different config files:
```bash
.config/config_fast.py
.config/config_quality.py
.config/config_offline.py
```

Point to specific config in GUI settings.

### Batch Processing

Process entire folders:
1. Select all files in folder
2. Add to queue
3. Click process once
4. Get coffee ☕
5. Come back to all results ready!

---

## Next Steps

- Read `GUI_REFACTORING_COMPLETE.md` for technical details
- Check `PIP_ONLY_INSTALLATION.md` for advanced setup
- See `FASTER_WHISPER_LIBRARY.md` for transcription tuning
- Visit GitHub for updates and issues

**Enjoy your 100% GUI-based Pogadane! 🎉**
