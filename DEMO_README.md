# Pogadane UI Demo

A demo version that shows the complete Pogadane interface with **realistic simulated processing** - identical UI to the real app, but without actual transcription or AI dependencies.

## Features

✨ **Full UI Experience** - Identical interface to the real application
- 🎨 Material 3 Design with complete theming (light/dark mode)
- 📋 File queue management with drag & drop
- ⚙️ Full settings panel with all configuration options
- 📊 Console output with real-time progress updates
- 📄 Results viewer with transcription and summary tabs
- 🎭 **Realistic work simulation** - Progress bars, stage transitions, and timing that mimics real processing

## Simulated Processing

The demo simulates realistic work without dependencies:

✅ **Realistic progress updates** - Multi-stage processing (initializing → copying/downloading → transcribing → summarizing → complete)  
✅ **Timing delays** - Matches real processing speed (~5-15 seconds per file)  
✅ **YouTube detection** - Shows "downloading" for URLs, "copying" for local files  
✅ **Speaker diarization** - Demo transcription shows timestamped multi-speaker output  
✅ **AI summaries** - Demo output shows structured summary format  
✅ **Console logging** - Real-time progress messages with emojis  

❌ **No actual processing** - No transcription engines, AI models, or downloads occur  
❌ **Demo content** - Returns pre-written Polish transcription and summary text

## Quick Start

### 1. Install minimal dependencies (just Flet)

```bash
pip install -r requirements-demo.txt
```

**Download size:** ~50MB (vs ~500MB for full app)

### 2. Run the demo

```bash
python demo_ui.py
```

## What This Demo Does

✅ **Complete UI** - Full Material 3 interface identical to the real application  
✅ **Add files** - Click "Add Files" to select audio/video files or paste YouTube URLs  
✅ **Process queue** - Click "Start Processing" to see realistic simulated work  
✅ **Progress tracking** - Watch detailed progress bars and console output  
✅ **View results** - See demo transcription with speaker diarization and AI summary  
✅ **Change settings** - Explore all configuration options (whisper models, AI providers, etc.)  
✅ **Theme switching** - Toggle between light and dark mode  

❌ **Does NOT transcribe** - No Whisper/faster-whisper processing occurs  
❌ **Does NOT use AI** - No GGUF/Ollama/Transformers/Gemini backends are called  
❌ **Does NOT download** - YouTube URLs are detected but not actually downloaded  
❌ **Simulated output only** - Returns pre-written demo content in Polish

## Use Cases

- 🎨 **UI/UX Review** - Experience the complete interface without installation overhead
- 📱 **Feature Testing** - Test all UI features (queue management, settings, theming)
- 🖼️ **Screenshots** - Generate promotional materials showing the app in action
- 🎓 **Demonstrations** - Show the complete workflow without backend dependencies
- 🚀 **Quick Preview** - Evaluate the app before installing ~500MB of dependencies
- 👥 **User Training** - Practice using the interface before real processing

## Comparison

| Feature | Demo (`demo_ui.py`) | Full App (`run_gui_flet.py`) |
|---------|---------------------|------------------------------|
| **Dependencies** | Flet only (~50MB) | Full stack (~500MB) |
| **Install time** | ~30 seconds | ~5-10 minutes |
| **UI/UX** | ✅ Identical | ✅ Complete |
| **Progress tracking** | ✅ Simulated (realistic) | ✅ Real |
| **Console output** | ✅ Simulated logs | ✅ Real processing logs |
| **Transcription** | ❌ Demo text only | ✅ Yes (faster-whisper) |
| **AI summaries** | ❌ Demo text only | ✅ Yes (GGUF/Ollama/etc) |
| **YouTube support** | ❌ Detection only | ✅ Yes (yt-dlp) |
| **File processing** | ❌ Simulated | ✅ Real processing |
| **Results quality** | ❌ Pre-written demo | ✅ Actual AI output |

**Processing time comparison:**
- Demo: ~5-15 seconds per file (simulated delays)
- Real: ~2-10 minutes per file (depends on model, file length, hardware)

## Use Cases

- 🎨 **UI Design Review** - Preview the interface without full installation
- 📱 **Layout Testing** - Test responsive design and window sizes
- 🖼️ **Screenshots** - Generate promotional screenshots
- 🎓 **Demonstrations** - Show the UI concept quickly
- 🚀 **Quick Preview** - See the app before committing to full installation

## Upgrade to Full Version

To use the complete application with all features:

```bash
# Install full dependencies
python install.py

# Run the full application
python run_gui_flet.py
```

See [README.md](README.md) for complete installation instructions.

---

**Note:** This demo file (`demo_ui.py`) is completely standalone and doesn't require any other Pogadane files to run!
