# Pogadane

<p align="center">
  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Pogadane" width="600"/>
  <br/>
  <strong>Audio transcription and AI-powered summaries</strong>
</p>

## Features

- 🎙️ Transcribe audio/video files and YouTube URLs
- 🤖 Generate AI summaries using local GGUF models
- ⚡ 4x faster transcription with Faster-Whisper
- 🖥️ Modern Material 3 GUI

## Installation

```bash
# Clone
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# Create virtual environment (in _app folder)
cd _app
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # Linux/macOS

# Install
python install.py
cd ..
```

### GGUF Model Setup

Download a GGUF model for AI summarization:

1. Go to [HuggingFace - Gemma 3 4B GGUF](https://huggingface.co/google/gemma-3-4b-it-GGUF)
2. Download `gemma-3-4b-it-Q4_K_M.gguf` (~2.5GB)
3. Place in `_app/dep/models/`

## Usage

**Windows**: Double-click `Pogadane.exe` or `Pogadane.bat`

**Command line**:
```bash
cd _app
python -m pogadane
```

1. **Add files** - Drag & drop audio/video or paste YouTube URLs
2. **Process** - Click "Start Processing"
3. **Review** - View transcription and AI summary

### Supported Formats

- **Audio**: MP3, WAV, M4A, OGG, FLAC
- **Video**: MP4, MKV, AVI, MOV, WebM
- **Online**: YouTube URLs

## Configuration

Settings are in `_app/.config/config.py` or use the GUI Settings panel.

| Setting | Default | Description |
|---------|---------|-------------|
| `WHISPER_MODEL` | `turbo` | Whisper model size |
| `WHISPER_LANGUAGE` | `Polish` | Transcription language |
| `GGUF_MODEL_PATH` | `_app/dep/models/gemma-3-4b-it-Q4_K_M.gguf` | GGUF model file |

## Project Structure

```
pogadane/
├── Pogadane.bat        # Windows launcher
├── Pogadane.exe        # Windows launcher (exe)
├── README.md
├── LICENSE
├── _app/               # Application source
│   ├── src/pogadane/   # Python package
│   ├── res/            # Assets & resources
│   ├── dep/models/     # GGUF models (not in git)
│   ├── .venv/          # Virtual environment (not in git)
│   ├── install.py
│   └── pyproject.toml
└── _dev/               # Development
    ├── test/           # Unit tests
    ├── doc/            # Documentation
    ├── samples/        # Test samples
    └── build/          # PyInstaller output (not in git)
```

## Development

```bash
# Install with dev tools
cd _app
python install.py --dev

# Run tests
cd ..
pytest _dev/test/
```

## License

MIT License - see [LICENSE](LICENSE)

Third-party: [NOTICES.md](NOTICES.md)

