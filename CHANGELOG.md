# Changelog

All notable changes to the Pogadane project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🎉 Major Refactoring - Clean Code Architecture (2025-01-20)

This release represents a complete architectural refactoring of Pogadane, implementing professional design patterns and SOLID principles while maintaining 100% backward compatibility.

#### Added

##### New Utility Modules (7 files)
- **`src/pogadane/constants.py`** - Centralized constants and default configuration values
  - Eliminates magic numbers throughout codebase
  - Single source of truth for application defaults
  - Font size limits, status messages, file markers, etc.

- **`src/pogadane/config_loader.py`** - Configuration management system
  - `ConfigManager` class implementing Singleton pattern
  - `ConfigLoader` factory for safe configuration loading
  - Automatic fallback to defaults on error
  - `get()` and `set()` methods for runtime configuration
  - `reload()` method for dynamic config updates

- **`src/pogadane/llm_providers.py`** - LLM provider abstraction layer
  - `LLMProvider` abstract base class (Strategy pattern)
  - `OllamaProvider` implementation for local LLM
  - `GoogleGeminiProvider` implementation for Google Gemini API
  - `LLMProviderFactory` for provider creation
  - Easy extension point for new providers (OpenAI, Anthropic, etc.)

- **`src/pogadane/text_utils.py`** - Text processing utilities
  - `strip_ansi()` - Remove ANSI color codes from terminal output
  - `is_valid_url()` - URL validation
  - `extract_transcription_and_summary()` - Parse marked sections from logs
  - `insert_with_markdown()` - Render Markdown in Tkinter Text widgets
  - Shared between GUI and CLI (eliminates duplication)

- **`src/pogadane/file_utils.py`** - File operation utilities
  - `get_unique_filename()` - Generate unique filenames from URLs/paths
  - `get_input_name_stem()` - Extract clean filename stems
  - `safe_delete_file()` - Safe file deletion with logging
  - `safe_create_directory()` - Safe directory creation
  - `cleanup_temp_directory()` - Temporary directory cleanup
  - `find_output_file()` - Find output files with multiple extensions

- **`src/pogadane/gui_utils/font_manager.py`** - GUI font management
  - `FontManager` class for centralized font handling
  - Dynamic font scaling (A+/A- buttons)
  - Font size limits (8-24 range)
  - TTK style integration
  - Manages 7 different font types

- **`src/pogadane/gui_utils/results_manager.py`** - GUI results management
  - `ResultsManager` class for results storage
  - In-memory result caching
  - Display management with Markdown support
  - Export functionality
  - Result retrieval by source

##### Documentation
- **`PULL_REQUEST.md`** - Comprehensive pull request summary
- **`CHANGELOG.md`** - This changelog file
- Updated `doc/ARCHITECTURE.md` with refactored architecture diagrams
- Updated `doc/REFACTORING.md` with completion summary and metrics

##### Docstrings
- Added comprehensive docstrings to all CLI functions:
  - `run_command()` - Subprocess execution with error handling
  - `get_unique_download_filename()` - Duplicate filename resolution
  - `download_youtube_audio()` - YouTube audio extraction
  - `transcribe_audio()` - Faster-Whisper transcription
  - `summarize_text()` - LLM-based summarization

#### Changed

##### Core Refactoring

**`src/pogadane/gui.py`** (Major refactoring, -120 lines)
- Integrated `FontManager` for all font operations
- Integrated `ResultsManager` for results storage and display
- Replaced direct config access with `ConfigManager.get()`
- Removed `DummyConfigFallback` class (no longer needed)
- Removed manual `importlib.util` configuration loading
- Replaced `reload_config_module()` with `config_manager.reload()`
- Used `text_utils` functions instead of local duplicates
- Imported status constants from `constants.py`
- Reduced complexity from ~650 to ~530 lines
- **Result**: Cleaner, more maintainable code following SRP

**`src/pogadane/transcribe_summarize_working.py`** (Major refactoring, -105 lines)
- Integrated `LLMProviderFactory` for provider selection
- Replaced 35-line if/elif provider logic with Factory pattern
- Removed `ensure_google_ai_available()` function (10 lines)
- Removed `genai` global variable
- Updated all `DefaultConfig.KEY` → `DEFAULT_CONFIG['KEY']`
- Used `file_utils` for file operations
- Used `text_utils` for text processing
- Added comprehensive docstrings to all major functions
- Improved error handling with try/except wrappers
- **Result**: Professional architecture following Strategy pattern

##### Documentation Updates
- `doc/ARCHITECTURE.md`:
  - Added "Latest Updates" section highlighting refactoring
  - New "Refactored Architecture" section with SOLID principles
  - Updated component diagrams showing utility modules
  - Comprehensive documentation of all new modules
  - Code examples for each design pattern

- `doc/REFACTORING.md`:
  - Added Phase 3/4 completion summary
  - Metrics table showing improvements (225+ lines removed)
  - Git commit timeline with all 6 commits
  - Testing results confirmation
  - Updated status from "In Progress" to "Complete"

#### Removed

##### Eliminated Duplicate Code (-225+ lines total)
- Removed duplicate `strip_ansi()` function from `gui.py` (now in `text_utils`)
- Removed duplicate `extract_transcription_and_summary()` (now in `text_utils`)
- Removed duplicate `insert_with_markdown()` (now in `text_utils`)
- Removed duplicate `is_valid_url()` (now in `text_utils`)
- Removed `DummyConfigFallback` class (replaced by `ConfigManager`)
- Removed manual `importlib.util` config loading logic
- Removed 35-line if/elif provider selection chain
- Removed `ensure_google_ai_available()` helper function
- Removed `genai` global variable
- Removed ~120 lines from `gui.py`
- Removed ~105 lines from `transcribe_summarize_working.py`

#### Fixed

- **Configuration Management**:
  - Fixed `ConfigManager` initialization (proper Singleton usage)
  - Added missing `config_path` property to `ConfigManager`
  - Improved error handling in config loading

- **Code Quality**:
  - Eliminated magic numbers throughout codebase
  - Fixed inconsistent configuration access patterns
  - Improved error messages and logging

#### Security

- No security changes in this release
- All existing security considerations maintained
- Local processing option (Ollama) still available for privacy

#### Performance

- No significant performance changes
- Slightly improved memory usage due to singleton pattern
- Faster configuration access (cached in ConfigManager)

#### Deprecated

- None - all changes are backward compatible

#### Breaking Changes

**None!** This is a pure refactoring release with 100% backward compatibility:
- ✅ GUI works identically
- ✅ CLI arguments unchanged
- ✅ Configuration file format unchanged
- ✅ All user-facing functionality preserved

---

## Design Patterns Implemented

### Strategy Pattern (LLM Providers)
- Abstract `LLMProvider` base class
- Concrete implementations: `OllamaProvider`, `GoogleGeminiProvider`
- Easy to extend with new providers (OpenAI, Anthropic, etc.)

### Factory Pattern (Provider Creation)
- `LLMProviderFactory` creates appropriate provider instances
- `ConfigLoader` factory for configuration loading
- Centralized object creation with validation

### Singleton Pattern (Configuration)
- `ConfigManager` ensures single configuration instance
- Global access without global variables
- Thread-safe implementation

---

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of Code (GUI) | ~650 | ~530 | -120 (-18%) |
| Lines of Code (CLI) | ~345 | ~240 | -105 (-30%) |
| Code Duplication | High | Minimal | -225+ lines |
| Utility Modules | 0 | 7 | +7 modules |
| Design Patterns | 0 | 3 | +3 patterns |
| Docstrings | Partial | Comprehensive | +100% |
| Compilation Errors | 0 | 0 | ✅ Stable |
| Test Status | GUI ✅ CLI ✅ | GUI ✅ CLI ✅ | ✅ Working |

---

## Git Commits

This release includes the following commits:

1. **ff4a5bb** - `docs: Update ARCHITECTURE.md and REFACTORING.md with Phase 3/4 completion`
2. **5f8b83a** - `feat: Integrate LLMProviderFactory into CLI and add comprehensive docstrings`
3. **89f5825** - `refactor(cli): integrate utility modules in CLI script`
4. **0d65da3** - `fix(config): add config_path property and fix ConfigManager initialization`
5. **a8748a3** - `refactor(gui): complete GUI refactoring with utility modules`
6. **df33f68** - `feat: add GUI utility modules (FontManager, ResultsManager)`

---

## Migration Guide

### For Developers

If you're extending or modifying Pogadane code:

#### Configuration Access
```python
# OLD
config = _load_config_module()
value = getattr(config, 'WHISPER_MODEL', DefaultConfig.WHISPER_MODEL)

# NEW
from pogadane.config_loader import ConfigManager
config_manager = ConfigManager()
value = config_manager.get('WHISPER_MODEL')
```

#### Adding New LLM Providers
```python
# Create new provider class
from pogadane.llm_providers import LLMProvider

class OpenAIProvider(LLMProvider):
    def summarize(self, text, prompt, language, source_name=""):
        # Implementation
        pass
    
    def is_available(self):
        # Check API key
        pass

# Register in LLMProviderFactory
# (modify create_provider method)
```

### For Users

**No changes required!** All functionality remains the same:
- Configuration file (`.config/config.py`) format unchanged
- GUI interface identical
- CLI arguments and behavior unchanged
- No breaking changes to existing workflows

---

## Acknowledgments

This refactoring follows industry best practices from:
- **Clean Code** by Robert C. Martin
- **Design Patterns** by Gang of Four
- **Refactoring** by Martin Fowler
- **SOLID Principles** for object-oriented design

---

## [0.1.8] - 2025-01-15

### Added
- LLM prompt template selection
- Batch processing in CLI and GUI
- Results manager in GUI
- Font size adjustment (A+/A-)
- `pogadane_doctor.py` setup tool

### Changed
- Improved GUI layout
- Enhanced batch processing queue
- Better error handling

---

## [0.1.7] - Previous releases

See git history for older releases.

---

**Maintained by**: Pogadane Development Team  
**Repository**: https://github.com/WSB-University-Problem-Based-Learning/pogadane  
**Branch**: `feature/restructure-compliance` → merging to `main`
