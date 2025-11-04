# Installation Guide for Pogadane

## Quick Start

### Standard Installation (Recommended)

```bash
# 1. Install the package with core dependencies
pip install -e .

# 2. Install external binaries (faster-whisper, ollama, yt-dlp)
python tools/install.py
```

That's it! You can now run:
- `pogadane-gui` - Launch the GUI
- `pogadane-cli` - Use the command-line interface
- `pogadane-doctor` - Run diagnostics

---

## Detailed Installation Options

### For End Users

```bash
# Install with all recommended dependencies
pip install -e .

# Install external binaries (required for transcription)
python tools/install.py
```

### For Developers

```bash
# Install with development tools (linters, formatters, build tools)
pip install -e .[dev]

# Or using requirements file
pip install -r requirements-dev.txt

# Install external binaries
python tools/install.py
```

### For Testing

```bash
# Install with testing dependencies
pip install -e .[test]

# Or using requirements file
pip install -r requirements-test.txt

# Run tests
pytest
```

### Optional Features

```bash
# Install with legacy GUI support (ttkbootstrap, customtkinter)
pip install -e .[legacy-gui]

# Install with transformers backend (for local AI without Ollama)
pip install -e .[transformers]

# Install everything
pip install -e .[all]
```

---

## Understanding External Dependencies

Pogadane relies on some external binaries that are **not** available on PyPI:

1. **faster-whisper-xxl.exe** - Speech-to-text transcription
2. **ollama** - Local LLM for summarization (optional)
3. **yt-dlp** - YouTube video download (available on PyPI, but we manage it separately)

### Why `tools/install.py`?

These tools are installed via `python tools/install.py` because:

- **faster-whisper-xxl** is a pre-built executable (not a Python package)
- **ollama** requires platform-specific installation
- We need specific versions and configurations

### What Does `tools/install.py` Do?

1. Downloads faster-whisper-xxl to `dep/faster-whisper-xxl/`
2. Downloads yt-dlp to `dep/yt-dlp/`
3. Optionally installs Ollama (system-wide)
4. Validates checksums and installation
5. Creates necessary directories

### Important: This Step is Required!

Running `pip install .` alone will install Python dependencies, but **will not** install the external binaries. Your installation will be incomplete.

**Always run:**
```bash
pip install -e .
python tools/install.py
```

---

## Installation Verification

After installation, verify everything works:

```bash
# Run the diagnostic tool
pogadane-doctor

# Or manually check:
python -m pogadane.doctor
```

This will check:
- ✅ Python version (>=3.7)
- ✅ Python dependencies installed
- ✅ faster-whisper-xxl present
- ✅ yt-dlp present
- ✅ Ollama installation (if used)
- ✅ Configuration files

---

## Dependency Management Philosophy

### Single Source of Truth: `pyproject.toml`

All package metadata and dependencies are defined in `pyproject.toml` (PEP 621 standard).

### Requirements Files

The `requirements*.txt` files are **thin wrappers** that reference the package:

**requirements.txt:**
```
-e .
```
Installs the package with core dependencies from `pyproject.toml`.

**requirements-dev.txt:**
```
-e .[dev]
```
Installs the package with development dependencies from `pyproject.toml`.

**requirements-test.txt:**
```
-e .[test]
```
Installs the package with testing dependencies from `pyproject.toml`.

This ensures:
- ✅ No duplication
- ✅ No version conflicts
- ✅ Easy maintenance
- ✅ Always in sync

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pogadane'"

**Solution:** Install the package:
```bash
pip install -e .
```

### "FileNotFoundError: faster-whisper-xxl.exe not found"

**Solution:** Install external binaries:
```bash
python tools/install.py
```

### "pogadane-doctor: command not found"

**Cause:** The package wasn't installed, or the entry point is broken.

**Solution:**
```bash
# Reinstall the package
pip install -e .

# Verify entry points
pip show -f pogadane | grep console_scripts
```

### "ImportError: cannot import name 'main' from 'pogadane.doctor'"

**Cause:** The `doctor.py` module doesn't have a `main()` function.

**Solution:** Check that `src/pogadane/doctor.py` exists and has a `main()` function, or update the entry point in `pyproject.toml`.

---

## Migration from Old Installation

If you previously installed using the old setup:

```bash
# 1. Uninstall old version
pip uninstall pogadane -y

# 2. Clean old files (optional)
rm -rf build dist *.egg-info

# 3. Install new version
pip install -e .

# 4. Install external binaries
python tools/install.py
```

---

## Development Workflow

```bash
# 1. Clone repository
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install in development mode with dev dependencies
pip install -e .[dev]

# 4. Install external binaries
python tools/install.py

# 5. Run tests
pytest

# 6. Run linters
black src/
flake8 src/
pylint src/pogadane/

# 7. Build package (optional)
python -m build
```

---

## CI/CD Integration

For continuous integration, use:

```bash
# Install package with test dependencies
pip install -e .[test]

# Install external binaries (if needed for integration tests)
python tools/install.py --non-interactive

# Run tests with coverage
pytest --cov=pogadane --cov-report=xml
```

---

## Platform-Specific Notes

### Windows
```bash
# PowerShell
pip install -e .
python tools\install.py
```

### Linux/macOS
```bash
pip install -e .
python tools/install.py
```

---

## Summary

| Command | Purpose |
|---------|---------|
| `pip install -e .` | Install package with core dependencies |
| `pip install -e .[dev]` | Install with development tools |
| `pip install -e .[test]` | Install with testing tools |
| `pip install -e .[all]` | Install with all optional features |
| `python tools/install.py` | Install external binaries (**required**) |
| `pogadane-doctor` | Verify installation |

**Remember:** Both steps are required for a complete installation:
1. `pip install -e .` (Python dependencies)
2. `python tools/install.py` (External binaries)
