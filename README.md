# Pogadane

<p align="center">
  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>
  <br/>
  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>
</p>

---

## ✨ Highlights

- 🎙️ **Batch transcription** for local audio files and YouTube URLs
- 🤖 **AI-powered summaries** using local GGUF models, Ollama, Transformers, or Google Gemini
- 🖥️ **Material 3 Expressive GUI** with waveform visualization and results viewer
- ⚡ **4x faster transcription** with faster-whisper (GPU/CPU optimized)
- 🧠 **Efficient AI models** using GGUF quantization (e.g., Gemma 3 4B runs on 4GB RAM)
- ⚙️ **Easy configuration** stored in `.config/config.py` with in-app overrides
- 🧰 **Cross-platform** installer that prepares dependencies in one pass

---

## 🚀 Quick Start

```bash
# 1. Clone and enter the project
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create a virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate    # macOS/Linux

# 3. Run the guided installer (RECOMMENDED stack: ~500MB)
python install.py

# 4. Launch the GUI
python run_gui_flet.py
```

---

## 📦 Installation

### Recommended: Guided Installer

The installer sets up the optimal stack for Pogadane with **faster-whisper** (4x faster transcription) + **GGUF models** (efficient AI) + **yt-dlp** (YouTube support).

```bash
python install.py
```

The installer will:
1. Install core dependencies (Flet GUI, yt-dlp)
2. Set up faster-whisper for transcription
3. Download a GGUF model for summarization (Gemma 3 4B)
4. Create default configuration

### Manual Installation

```bash
# Core only (GUI + YouTube download)
pip install -r requirements.txt

# Add transcription engine (choose one)
pip install -r requirements-faster-whisper.txt  # Recommended: 4x faster
pip install -r requirements-whisper.txt         # Alternative: OpenAI Whisper

# Add AI summarization backend (optional)
pip install -r requirements-transformers.txt    # Offline HuggingFace models
```

---

## 🎯 Usage

### Launch GUI

```bash
python run_gui_flet.py
```

### Features

1. **Add Files** - Drag & drop audio/video files or paste YouTube URLs
2. **Configure** - Choose transcription engine and AI provider in Settings
3. **Process** - Click "Start Processing" to transcribe and summarize
4. **Review** - View results with speaker diarization and AI summaries

### Supported Formats

- **Audio**: MP3, WAV, M4A, OGG, FLAC, AAC
- **Video**: MP4, MKV, AVI, MOV, WebM
- **Online**: YouTube URLs (automatic download)

---

## ⚙️ Configuration

Settings are stored in `.config/config.py` and can be modified via the GUI Settings panel.

### Transcription Providers

| Provider | Speed | Quality | GPU Support |
|----------|-------|---------|-------------|
| **faster-whisper** | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ CUDA |
| **whisper** | ⚡⚡ | ⭐⭐⭐⭐ | ✅ CUDA |

### Summarization Providers

| Provider | Offline | Quality | Requirements |
|----------|---------|---------|--------------|
| **GGUF** | ✅ | ⭐⭐⭐⭐ | 4GB+ RAM |
| **Transformers** | ✅ | ⭐⭐⭐ | 8GB+ RAM |
| **Ollama** | ✅ | ⭐⭐⭐⭐ | Ollama server |
| **Google Gemini** | ❌ | ⭐⭐⭐⭐⭐ | API key |

---

## 📁 Project Structure

```
pogadane/
├── src/pogadane/         # Main application source
│   ├── gui_flet.py       # Material 3 GUI
│   ├── backend.py        # Processing backend
│   ├── transcription_providers.py
│   └── llm_providers.py
├── test/                 # Test suite
├── doc/                  # Documentation
├── install.py            # Guided installer
└── run_gui_flet.py       # GUI launcher
```

---

## 🧪 Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/pogadane
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **Gemma models**: Subject to [Google Gemma Terms of Use](doc/gemma_terms.md)
- See [NOTICES.md](NOTICES.md) for all third-party attributions

---

## 🤝 Contributing

This project was developed as part of the Problem-Based Learning program at WSB University.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

