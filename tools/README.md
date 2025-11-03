# Pogadane Installation Tools

This folder contains tools for installing and managing Pogadane dependencies.

## 🚀 Main Installation Script

### `install.py` - Complete Automatic Installation

**One-command installation for everything:**

```powershell
python tools/install.py
```

**What it does:**
- ✅ Checks Python version (3.7+)
- ✅ Upgrades pip
- ✅ Installs Python packages
- ✅ Downloads yt-dlp.exe
- ✅ Downloads and extracts Faster-Whisper
- ✅ Downloads Ollama installer
- ✅ Updates config paths
- ✅ Verifies installation

**Options:**
```powershell
python tools/install.py              # Full installation with Ollama
python tools/install.py --no-ollama  # Skip Ollama (use Google Gemini API)
python tools/install.py --dev        # Include development tools
```

---

## 🔧 Utility Scripts

### `dependency_manager.py` - Manage External Dependencies

**Standalone tool for managing yt-dlp, Faster-Whisper, and Ollama:**

```powershell
# Verify what's installed
python tools/dependency_manager.py --verify-only

# Install specific dependency
python tools/dependency_manager.py --install yt-dlp
python tools/dependency_manager.py --install faster-whisper
python tools/dependency_manager.py --install ollama

# Install all with optional dependencies
python tools/dependency_manager.py --include-optional
```

**Use when:**
- Main installer fails
- You want to update a specific component
- You need to verify installation

---

### `extract_faster_whisper.py` - Fix Faster-Whisper Extraction

**Helper for when automatic extraction fails (BCJ2 filter issue):**

```powershell
python tools/extract_faster_whisper.py
```

**What it does:**
- Finds 7-Zip installation on your system
- Extracts Faster-Whisper archive using 7-Zip
- Locates faster-whisper-xxl.exe
- Copies to correct location
- Updates configuration
- Cleans up temporary files

**Requirements:**
- 7-Zip must be installed: https://www.7-zip.org/
- Archive must be downloaded (run `install.py` first)

**Use when:**
- You see error: "BCJ2 filter is not supported by py7zr"
- Faster-Whisper shows as "Missing" after installation
- Manual extraction is needed

---

### `pogadane_doctor.py` - Legacy Installation Helper

**Original installation helper (still works):**

```powershell
python tools/pogadane_doctor.py
```

**What it does:**
- Checks Python and pip
- Installs Python packages
- Downloads project files from GitHub
- Creates backups of config files

**Note:** This is the older method. Use `install.py` for new installations.

---

## 📋 Common Workflows

### Fresh Installation
```powershell
# 1. Run main installer
python tools/install.py

# 2. If Faster-Whisper extraction fails:
python tools/extract_faster_whisper.py

# 3. Verify everything
python tools/dependency_manager.py --verify-only
```

### Update Dependencies
```powershell
# Update all
python tools/dependency_manager.py --include-optional

# Update specific
python tools/dependency_manager.py --install yt-dlp
```

### Troubleshooting
```powershell
# Check what's installed
python tools/dependency_manager.py --verify-only

# Fix Faster-Whisper
python tools/extract_faster_whisper.py

# Re-run full installation
python tools/install.py
```

---

## 🐛 Known Issues & Fixes

### Issue: "BCJ2 filter is not supported by py7zr"

**Cause:** py7zr library can't extract Faster-Whisper archive

**Fix:**
```powershell
python tools/extract_faster_whisper.py
```

**Requirements:** 7-Zip must be installed

---

### Issue: Ollama shows as "Missing" after installation

**Cause:** Ollama is an installer, not a standalone exe

**Fix:** This is normal! Verify with:
```powershell
ollama --version
ollama list
```

If these commands work, Ollama is installed correctly.

---

### Issue: "The script py7zr.exe is installed in ... which is not on PATH"

**Cause:** Python Scripts folder not in PATH

**Fix 1 - Add to PATH:**
```powershell
# Add C:\Users\<YourName>\AppData\Roaming\Python\Python313\Scripts to PATH
```

**Fix 2 - Use full path:**
```powershell
python -m py7zr ...
```

**Fix 3 - Ignore:**
This is just a warning. The installer still works.

---

## 📖 Documentation

- [INSTALL.md](../INSTALL.md) - Complete installation guide
- [README.md](../README.md) - Main project documentation
- [QUICK_START.md](../QUICK_START.md) - Beginner guide

---

## 🎯 Which Tool Should I Use?

| Situation | Tool | Command |
|-----------|------|---------|
| **Fresh installation** | install.py | `python tools/install.py` |
| **Faster-Whisper extraction failed** | extract_faster_whisper.py | `python tools/extract_faster_whisper.py` |
| **Update one component** | dependency_manager.py | `python tools/dependency_manager.py --install <name>` |
| **Verify installation** | dependency_manager.py | `python tools/dependency_manager.py --verify-only` |
| **Legacy method** | pogadane_doctor.py | `python tools/pogadane_doctor.py` |

---

**Need help?** See [INSTALL.md](../INSTALL.md) for comprehensive troubleshooting.
