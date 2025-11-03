# Dependency Directory Structure

This directory contains external binary dependencies for Pogadane.

## Structure

```
dep/
├── yt-dlp/              # YouTube downloader
│   └── yt-dlp.exe       # Downloaded by installer
├── faster-whisper/      # Speech-to-text engine
│   └── faster-whisper-xxl.exe  # Downloaded by installer
└── ollama/              # Local AI (optional)
    └── OllamaSetup.exe  # Downloaded by installer
```

## Installation

Run the automatic installer to download all dependencies:

```powershell
python tools/install.py
```

See [INSTALL.md](../INSTALL.md) for details.

## Manual Download

If automatic installation fails:

- **yt-dlp**: https://github.com/yt-dlp/yt-dlp/releases/latest
- **Faster-Whisper**: https://github.com/Purfview/whisper-standalone-win/releases
- **Ollama**: https://ollama.com/

## Note

These binaries are:
- ✅ Downloaded automatically by `tools/install.py`
- ✅ Stored locally in `dep/` folder
- ❌ NOT stored in Git (kept clean via `.gitignore`)
- ✅ Paths auto-configured in `.config/config.py`
