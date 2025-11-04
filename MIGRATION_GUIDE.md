# Migration Guide: Modernizing Pogadane Package Structure

## Overview

This guide documents the migration from the old setup.py-based configuration to the modern pyproject.toml standard (PEP 621).

## What Changed

### ✅ 1. Modernized Packaging with pyproject.toml

**Before:**
- Configuration scattered across `setup.py` and multiple `requirements*.txt` files
- Duplicate dependency definitions
- Non-standard packaging approach

**After:**
- Single source of truth: `pyproject.toml`
- All metadata, dependencies, and build configuration in one place
- Modern PEP 621 compliant structure
- Thin wrapper `requirements*.txt` files that reference the package

**Migration:**
```bash
# Old way
pip install -r requirements.txt
pip install -r requirements-dev.txt

# New way (still supported for compatibility)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Or use extras directly
pip install -e .[dev]
pip install -e .[test]
pip install -e .[all]
```

### ✅ 2. Consolidated Dependency Definitions

**Before:**
- `setup.py` had `install_requires` and `extras_require`
- `requirements.txt` had production dependencies
- `requirements-dev.txt` duplicated dev dependencies
- `requirements-test.txt` duplicated test dependencies

**After:**
- `pyproject.toml` defines all dependencies once
- `requirements.txt` → `-e .` (references core dependencies)
- `requirements-dev.txt` → `-e .[dev]` (references dev extra)
- `requirements-test.txt` → `-e .[test]` (references test extra)

**Benefits:**
- No duplication
- No version conflicts
- Update once, applies everywhere
- Easier to maintain

### ✅ 3. Fixed pogadane-doctor Entry Point

**Before:**
```python
# setup.py
entry_points={
    "console_scripts": [
        "pogadane-doctor=pogadane_doctor:main",  # ❌ BROKEN
    ],
}
```

**Problem:** `pogadane_doctor.py` was in `tools/` directory, not part of the installable package.

**After:**
```python
# pyproject.toml
[project.scripts]
pogadane-doctor = "pogadane.doctor:main"  # ✅ FIXED
```

**File moved:** `tools/pogadane_doctor.py` → `src/pogadane/doctor.py`

**Now works:**
```bash
pip install -e .
pogadane-doctor  # ✅ Works!
```

### ✅ 4. Clarified External Binary Dependencies

**Before:**
- `tools/install.py` existed but wasn't well documented
- Users might skip it and have broken installations
- No clear warning about required manual step

**After:**
- Created comprehensive `INSTALLATION.md`
- Updated `README.md` to emphasize two-step installation
- Added better error messages in `tools/install.py`
- `pogadane-doctor` checks for missing binaries

**Required installation:**
```bash
# Step 1: Python dependencies (from PyPI)
pip install -e .

# Step 2: External binaries (custom installer)
python tools/install.py
```

## File Changes Summary

### New Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | **Main configuration** - All package metadata, dependencies, build settings |
| `INSTALLATION.md` | Comprehensive installation guide with troubleshooting |
| `MIGRATION_GUIDE.md` | This file - documents the changes |
| `src/pogadane/doctor.py` | Diagnostic tool (moved from `tools/pogadane_doctor.py`) |

### Modified Files

| File | Changes |
|------|---------|
| `setup.py` | Reduced to minimal shim (backward compatibility only) |
| `requirements.txt` | Now references `-e .` (package core dependencies) |
| `requirements-dev.txt` | Now references `-e .[dev]` (package dev extras) |
| `requirements-test.txt` | Now references `-e .[test]` (package test extras) |

### Deprecated/Legacy Files

| File | Status | Action |
|------|--------|--------|
| `tools/pogadane_doctor.py` | Superseded by `src/pogadane/doctor.py` | Keep for now, can be removed later |

## Dependency Changes

### Core Dependencies

**Simplified and PyPI-first approach:**

| Dependency | Status | Notes |
|------------|--------|-------|
| `flet>=0.24.0` | Core | Material 3 GUI framework |
| `google-generativeai>=0.3.0` | Core | Gemini API client |
| `py7zr>=0.20.0` | Core | Archive extraction |
| `yt-dlp>=2023.0.0` | Core | YouTube download (now on PyPI!) |

**Removed from core** (moved to optional extras):

| Dependency | New Location | Reason |
|------------|--------------|--------|
| `ttkbootstrap>=1.10.0` | `[legacy-gui]` | Legacy GUI, not needed for main Flet GUI |
| `customtkinter>=5.2.0` | `[legacy-gui]` | Legacy GUI, not needed for main Flet GUI |
| `transformers>=4.30.0` | `[transformers]` | Large optional dependency |
| `torch>=2.0.0` | `[transformers]` | Large optional dependency |

### New Optional Dependency Groups

```toml
[project.optional-dependencies]
dev = [...]           # Development tools (linters, formatters, build tools)
test = [...]          # Testing framework
transformers = [...]  # Local AI without Ollama
legacy-gui = [...]    # Old GUI frameworks
all = [...]           # Everything
```

## Breaking Changes

### ⚠️ For End Users

**None!** Installation still works with `requirements.txt`:

```bash
pip install -r requirements.txt
python tools/install.py
```

### ⚠️ For Developers

1. **Entry point changed:**
   ```bash
   # Old (broken)
   pogadane-doctor  # ImportError
   
   # New (fixed)
   pogadane-doctor  # Works after: pip install -e .
   ```

2. **Development setup:**
   ```bash
   # Old way (still works)
   pip install -r requirements-dev.txt
   
   # New way (recommended)
   pip install -e .[dev]
   ```

### ⚠️ For CI/CD

Update your build scripts:

```yaml
# Old
- pip install -r requirements.txt
- pip install -r requirements-test.txt

# New (recommended)
- pip install -e .[test]

# Or keep old way (still works)
- pip install -r requirements-test.txt
```

## Upgrade Path

### For Users

**No action required!** Your existing installation commands still work:

```bash
pip install -r requirements.txt
python tools/install.py
```

### For Developers

1. **Update your workflow:**
   ```bash
   # Old
   pip install -r requirements-dev.txt
   
   # New (recommended)
   pip install -e .[dev]
   ```

2. **Update documentation/scripts:**
   - Replace references to `requirements-*.txt` with extras
   - Update CI/CD pipelines if desired (optional)

3. **Benefit from new features:**
   ```bash
   # Install just what you need
   pip install -e .[test]           # Testing only
   pip install -e .[transformers]   # Add transformers backend
   pip install -e .[all]             # Everything
   ```

## Verification

After migration, verify everything works:

```bash
# 1. Reinstall package
pip uninstall pogadane -y
pip install -e .[dev]

# 2. Install external binaries
python tools/install.py

# 3. Run diagnostic tool
pogadane-doctor

# 4. Run tests
pytest

# 5. Launch GUI
pogadane-gui
```

## Rollback Plan

If you encounter issues, you can rollback:

```bash
# 1. Checkout previous commit
git checkout HEAD~1

# 2. Reinstall
pip uninstall pogadane -y
pip install -e .
python tools/install.py
```

## Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| Configuration files | Scattered (setup.py + multiple requirements.txt) | Centralized (pyproject.toml) |
| Dependency duplication | Yes (setup.py and requirements.txt) | No (single source of truth) |
| Standards compliance | Old (setup.py) | Modern (PEP 621) |
| `pogadane-doctor` entry point | Broken | Fixed |
| Installation documentation | Basic | Comprehensive |
| External binaries | Unclear | Well documented |
| Maintenance burden | High (sync multiple files) | Low (edit one file) |
| Developer experience | Confusing | Clear |

## FAQ

### Q: Do I need to change anything?

**A:** No! The old installation method still works:
```bash
pip install -r requirements.txt
python tools/install.py
```

### Q: What's the advantage of the new way?

**A:** Single source of truth, no duplication, modern standards:
```bash
pip install -e .[dev]
python tools/install.py
```

### Q: Can I still use `requirements.txt`?

**A:** Yes! It now references the package (`-e .`), ensuring dependencies stay in sync.

### Q: What happened to `pogadane-doctor`?

**A:** It moved from `tools/pogadane_doctor.py` to `src/pogadane/doctor.py` and now works correctly as a console script.

### Q: Why do I still need `python tools/install.py`?

**A:** External binaries (faster-whisper-xxl, ollama) aren't on PyPI. This script downloads and installs them. See `INSTALLATION.md` for details.

### Q: Can I skip Ollama?

**A:** Yes! Use Gemini API instead:
```bash
python tools/install.py --no-ollama
```

### Q: How do I update dependencies?

**A:** Edit `pyproject.toml` only. The `requirements*.txt` files automatically reference it.

## Related Documentation

- `INSTALLATION.md` - Complete installation guide
- `pyproject.toml` - Package configuration
- `README.md` - Project overview
- `CONSOLIDATION_SUMMARY.md` - GUI consolidation notes
- `GUI_ENHANCEMENTS.md` - Recent GUI improvements

## Credits

Migration completed: November 4, 2025  
Standards: PEP 517, PEP 518, PEP 621  
Build backend: setuptools >= 61.0
