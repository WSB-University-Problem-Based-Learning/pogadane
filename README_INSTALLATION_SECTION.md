# Installation Section for README.md

Add this to your main README.md file:

---

## 📦 Installation

### Quick Start (Recommended)

```bash
# 1. Install Python package with dependencies
pip install -e .

# 2. Install external binaries (required)
python tools/install.py
```

That's it! You can now run:
- `pogadane-gui` - Launch the beautiful Material 3 GUI
- `pogadane-cli` - Use the command-line interface
- `pogadane-doctor` - Run diagnostic checks

> **Important:** Both steps are required. The first installs Python dependencies from PyPI, the second downloads external binaries (faster-whisper, ollama, yt-dlp) that aren't available on PyPI.

### Detailed Installation

See [INSTALLATION.md](INSTALLATION.md) for:
- Development setup
- Testing setup
- Optional features (transformers, legacy GUIs)
- Platform-specific instructions
- Troubleshooting

### Installation Options

```bash
# For end users (default)
pip install -e .

# For developers (includes linters, formatters, build tools)
pip install -e .[dev]

# For testing (includes pytest and coverage tools)
pip install -e .[test]

# For all features (everything)
pip install -e .[all]
```

### External Dependencies

This project uses some external tools not available on PyPI:
- **faster-whisper-xxl** - Speech-to-text engine
- **ollama** - Local LLM for summarization
- **yt-dlp** - YouTube video downloader

These are automatically installed by `python tools/install.py`.

### Verification

After installation, run the diagnostic tool:

```bash
pogadane-doctor
```

This checks:
- ✅ Python version (>=3.7)
- ✅ Python dependencies
- ✅ External binaries
- ✅ Configuration files

---

## 🚀 Usage

### GUI Mode (Recommended)

```bash
pogadane-gui
```

Launches the beautiful Material 3 interface with:
- Audio waveform visualization
- Interactive topic timeline
- Real-time transcription
- AI-powered summaries
- Dark/light theme (persists your preference)

### Command-Line Mode

```bash
pogadane-cli path/to/audio.mp3
pogadane-cli https://youtube.com/watch?v=...
```

See `pogadane-cli --help` for all options.

---

## 🔧 Development

### Setup Development Environment

```bash
# 1. Clone repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install with dev dependencies
pip install -e .[dev]

# 4. Install external binaries
python tools/install.py

# 5. Run tests
pytest
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pogadane

# Run specific test file
pytest test/test_config.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/
pylint src/pogadane/

# Type checking
mypy src/
```

---

## 📚 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Complete installation guide
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Package modernization details
- **[GUI_ENHANCEMENTS.md](GUI_ENHANCEMENTS.md)** - Recent GUI improvements
- **[CONSOLIDATION_SUMMARY.md](CONSOLIDATION_SUMMARY.md)** - GUI consolidation notes
- **[M3_EXPRESSIVE_DESIGN_SYSTEM.md](M3_EXPRESSIVE_DESIGN_SYSTEM.md)** - Design system reference

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'pogadane'"

Install the package:
```bash
pip install -e .
```

### "FileNotFoundError: faster-whisper-xxl.exe not found"

Install external binaries:
```bash
python tools/install.py
```

### "pogadane-doctor: command not found"

The package isn't installed correctly. Reinstall:
```bash
pip install -e .
```

For more troubleshooting, see [INSTALLATION.md](INSTALLATION.md#troubleshooting).

---
