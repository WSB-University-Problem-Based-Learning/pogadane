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
# 1. Clone the project
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # macOS/Linux

# 3. Run the installer
python install.py

# 4. Launch the app
python run_gui_flet.py
# or: python -m pogadane
```

---

## 📦 Installation

### Option 1: Guided Installer (Recommended)

```bash
python install.py
```

The installer automatically sets up:
- **faster-whisper** - 4x faster transcription with GPU support
- **llama-cpp-python** - Efficient GGUF model support
- **yt-dlp** - YouTube video/audio download

### Option 2: Manual Installation

```bash
# Install core + recommended transcription
pip install -e .
pip install faster-whisper

# Optional: Alternative backends
pip install -r requirements-whisper.txt         # OpenAI Whisper
pip install -r requirements-transformers.txt    # HuggingFace models
```

---

## 🎯 Usage

### Launch the App

```bash
python run_gui_flet.py
# or
python -m pogadane
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
pip install -e .[dev]

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

