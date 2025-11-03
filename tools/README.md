# Pogadane Tools Directory

This folder contains utility scripts for maintaining and troubleshooting Pogadane.

> **Note:** The main installation system has been replaced with `install.py` in the project root.  
> The scripts in this folder are **legacy tools** kept for troubleshooting and advanced use cases.

---

## 🆕 NEW Installation System (Recommended)

### Use `install.py` in Project Root

The new cross-platform installer is located in the project root directory:

```bash
# Windows:
python install.py

# macOS/Linux:
python3 install.py

# Or use convenient launchers:
# Windows: install.bat
# macOS/Linux: ./install.sh
```

**Features:**
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Three installation modes (LIGHTWEIGHT, FULL, DEV)
- ✅ Interactive wizard or command-line flags
- ✅ No setuptools required
- ✅ Automatic configuration
- ✅ Lightweight Python-only option

**See:** [INSTALL.md](../INSTALL.md) for complete documentation

---

## 🔧 Legacy Tools (Advanced/Troubleshooting)

The following scripts are older tools that remain available for specific use cases:

### `pogadane_doctor.py` - Legacy Setup Tool

**Status:** ⚠️ DEPRECATED - Use `install.py` instead

Original helper script for checking and installing dependencies.

```powershell
python tools/pogadane_doctor.py
```

**Note:** This script may reference outdated installation methods. Use the new `install.py` for current installation.

---

### `install.py` (Legacy - in tools/)

**Status:** ⚠️ DEPRECATED - Use root `install.py` instead

Original command-line installer (Windows-focused).

**Why deprecated:**
- Not cross-platform
- Complex binary downloading logic
- Requires external binaries
- No lightweight mode

**Replacement:**  
Use `/install.py` (in project root) which provides cross-platform support and lightweight installation options.

---

### `install_gui.py` - GUI Installer

**Status:** ⚠️ DEPRECATED - Needs updating

Graphical installation wizard.

```powershell
python tools/install_gui.py
```

**Issues:**
- May not work with current project structure
- References old installation system
- Tkinter dependency

**Note:** This tool needs to be updated to work with the new installation system, or may be removed in future versions.

---

### `dependency_manager.py` - Binary Dependency Manager

**Status:** ✅ FUNCTIONAL (for specific use cases)

Standalone tool for managing external binary dependencies (Windows-specific).

```powershell
# Verify installed binaries
python tools/dependency_manager.py --verify-only

# Install specific component
python tools/dependency_manager.py --install yt-dlp
python tools/dependency_manager.py --install faster-whisper
python tools/dependency_manager.py --install ollama
```

**Use when:**
- Troubleshooting specific binary installations
- You need to update just one component
- Working with Windows-specific binaries

**Note:** The new `install.py` handles most of these tasks automatically.

---

###`extract_faster_whisper.py` - 7-Zip Extraction Helper

**Status:** ✅ FUNCTIONAL

Helper for when automatic extraction fails (BCJ2 filter issue with py7zr).

```powershell
python tools/extract_faster_whisper.py
```

**What it does:**
- Locates 7-Zip on your system
- Extracts Faster-Whisper archive using 7-Zip CLI
- Works around py7zr BCJ2 compression limitation

**When to use:**
- Faster-Whisper extraction fails during installation
- Error message mentions "BCJ2 filter not supported"
- You have 7-Zip installed

---

## 📊 Tool Comparison

| Tool | Status | Platform | Purpose | Recommendation |
|------|--------|----------|---------|----------------|
| **`/install.py`** (root) | ✅ CURRENT | All | Main installer | **Use this!** |
| `pogadane_doctor.py` | ⚠️ DEPRECATED | All | Legacy setup | Use `/install.py` |
| `tools/install.py` | ⚠️ DEPRECATED | Windows | Old CLI installer | Use `/install.py` |
| `install_gui.py` | ⚠️ NEEDS UPDATE | Windows | GUI wizard | Needs work |
| `dependency_manager.py` | ✅ FUNCTIONAL | Windows | Binary management | For troubleshooting |
| `extract_faster_whisper.py` | ✅ FUNCTIONAL | Windows | Extraction helper | For BCJ2 errors |

---

## 🎯 Recommended Workflow

### For New Users

1. **Use the new installer:**
   ```bash
   python install.py --lightweight
   ```

2. **If you encounter issues:**
   - Check [INSTALL.md](../INSTALL.md) troubleshooting section
   - Try different installation mode
   - Check GitHub issues

### For Advanced Users / Troubleshooting

1. **Try new installer first:**
   ```bash
   python install.py --full
   ```

2. **If specific component fails:**
   - Use `dependency_manager.py` to install that component
   - Use `extract_faster_whisper.py` for extraction issues
   - Check tool-specific documentation

### For Developers

1. **Install in DEV mode:**
   ```bash
   python install.py --dev
   ```

2. **Run tests:**
   ```bash
   pytest
   ```

3. **See:**
   - [test/README.md](../test/README.md) - Testing guide
   - [doc/ARCHITECTURE.md](../doc/ARCHITECTURE.md) - Technical docs

---

## 📖 Documentation

- **Installation Guide:** [INSTALL.md](../INSTALL.md) - Complete installation documentation
- **Quick Start:** [QUICK_START.md](../QUICK_START.md) - Beginner-friendly guide
- **Main README:** [README.md](../README.md) - Full project documentation
- **Architecture:** [doc/ARCHITECTURE.md](../doc/ARCHITECTURE.md) - Technical details

---

## 🚨 Migration Notes

If you previously used the old installation tools:

### Old System → New System

**Before (old):**
```powershell
python tools/install.py              # Windows-only, complex
python tools/install_gui.py          # GUI wizard
python tools/pogadane_doctor.py      # Legacy setup
```

**Now (new):**
```bash
python install.py                    # Cross-platform, simple
python install.py --lightweight      # Pure Python mode
python install.py --full             # All features
```

### Key Differences

| Feature | Old System | New System |
|---------|-----------|-----------|
| Platform Support | Windows only | Windows, macOS, Linux |
| Setup Complexity | Multiple scripts | Single script |
| Lightweight Mode | ❌ Not available | ✅ Available |
| External Binaries | Always required | Optional (lightweight mode) |
| Configuration | Manual editing | Auto-generated |
| Setuptools Required | ✅ Yes | ❌ No |

---

## ❓ FAQ

### Q: Should I still use pogadane_doctor.py?
**A:** No. Use `python install.py` instead. It's simpler and cross-platform.

### Q: What about install_gui.py?
**A:** It needs updating to work with the new system. Use the command-line `install.py` for now.

### Q: When should I use dependency_manager.py?
**A:** Only for troubleshooting specific binary installations on Windows. The new installer handles this automatically.

### Q: Will the old tools be removed?
**A:** They're kept for compatibility and troubleshooting, but may be archived in future versions.

### Q: I used the old installer. Can I switch?
**A:** Yes! Just run `python install.py` and it will set up the new configuration.

---

## 🔄 Future Plans

- [ ] Update `install_gui.py` to work with new system
- [ ] Archive fully deprecated tools
- [ ] Add more platform-specific helpers
- [ ] Improve error handling in legacy tools

---

**Last Updated:** 2025-11-04  
**Status:** Tools directory contains legacy scripts + extraction helpers  
**Recommendation:** Use `/install.py` for all new installations

For help, see [INSTALL.md](../INSTALL.md) or create an issue on GitHub.
