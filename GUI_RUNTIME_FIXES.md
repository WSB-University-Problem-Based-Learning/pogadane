# GUI Runtime Error Fixes

**Date**: November 4, 2025  
**Issue**: AttributeError crashes in GUI application

---

## Errors Fixed

### 1. `AttributeError: 'PogadaneApp' object has no attribute 'base_path'` ✅

**Location**: `src/pogadane/gui.py:1997`

**Root Cause**: 
The `base_path` attribute was referenced in `_execute_batch_processing_logic()` but never initialized in `__init__()`.

**Error Trace**:
```python
File "src\pogadane\gui.py", line 1997, in _execute_batch_processing_logic
    script_path = self.base_path / "transcribe_summarize_working.py"
                  ^^^^^^^^^^^^^^
AttributeError: 'PogadaneApp' object has no attribute 'base_path'
```

**Fix Applied**:
```python
# In PogadaneApp.__init__() at line 259
# Initialize variables
self.base_path = Path(__file__).parent  # Path to src/pogadane directory
self.output_queue = queue.Queue()
self.batch_processing_thread = None
# ...
```

**Impact**: 
- ✅ Batch processing now works correctly
- ✅ Script path properly resolved to `src/pogadane/transcribe_summarize_working.py`

---

### 2. `AttributeError: 'ConfigManager' object has no attribute 'save_config_to_file'` ✅

**Location**: `src/pogadane/gui.py:1852`

**Root Cause**: 
The `save_config_to_file()` method was called but didn't exist in `ConfigManager` class.

**Error Message**:
```
Error saving theme: 'ConfigManager' object has no attribute 'save_config_to_file'
```

**Fix Applied**:

**1. Added `save_config_to_file()` method** (`config_loader.py`):
```python
def save_config_to_file(self, config_obj=None):
    """
    Save runtime configuration preferences to .config/settings.json
    
    Preserves user's config.py comments by using separate settings file.
    """
    if config_obj is None:
        config_obj = self._config
    
    if config_obj is None or self._config_path is None:
        return
    
    # Settings file path (next to config.py)
    settings_file = self._config_path.parent / "settings.json"
    
    # Extract runtime preferences
    runtime_settings = {}
    if hasattr(config_obj, 'THEME_MODE'):
        runtime_settings['THEME_MODE'] = config_obj.THEME_MODE
    
    # Write to JSON
    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(runtime_settings, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save settings: {e}", file=sys.stderr)
```

**2. Added `load_runtime_settings()` method** (`config_loader.py`):
```python
def load_runtime_settings(self):
    """Load runtime settings from .config/settings.json"""
    if self._config_path is None:
        return
    
    settings_file = self._config_path.parent / "settings.json"
    
    if not settings_file.exists():
        return
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # Apply settings to config object
        for key, value in settings.items():
            setattr(self._config, key, value)
    except Exception as e:
        print(f"Warning: Could not load settings: {e}", file=sys.stderr)
```

**3. Updated `initialize()` and `reload()` methods**:
```python
def initialize(self, config_path: Path = None):
    # ... existing code ...
    self._config = ConfigLoader.load_config(config_path)
    
    # Load runtime settings (theme, etc.)
    self.load_runtime_settings()

def reload(self):
    if self._config_path:
        self._config = ConfigLoader.load_config(self._config_path)
        self.load_runtime_settings()
```

**4. Added `json` import**:
```python
import json
```

**Impact**:
- ✅ Theme preference now persists across sessions
- ✅ Saved to `.config/settings.json` (preserves `config.py` comments)
- ✅ Graceful error handling (won't crash if save fails)
- ✅ Extensible for other UI preferences

---

## Testing

### Before Fix:
```bash
PS C:\Users\alexk\repos\pogadane> python -m src.pogadane.gui
✅ Configuration loaded from C:\Users\alexk\repos\pogadane\.config\config.py
Exception in thread Thread-1 (_execute_batch_processing_logic):
Traceback (most recent call last):
  ...
AttributeError: 'PogadaneApp' object has no attribute 'base_path'
Error saving theme: 'ConfigManager' object has no attribute 'save_config_to_file'
Error saving theme: 'ConfigManager' object has no attribute 'save_config_to_file'
...
```

### After Fix:
```bash
PS C:\Users\alexk\repos\pogadane> python -m src.pogadane.gui
✅ Configuration loaded from C:\Users\alexk\repos\pogadane\.config\config.py
# GUI starts successfully, no errors
# Theme changes persist across restarts
# Batch processing works correctly
```

---

## Files Modified

| File | Changes | Lines Added/Modified |
|------|---------|---------------------|
| `src/pogadane/gui.py` | Added `self.base_path` initialization | +1 |
| `src/pogadane/config_loader.py` | Added `save_config_to_file()` method | +35 |
| `src/pogadane/config_loader.py` | Added `load_runtime_settings()` method | +26 |
| `src/pogadane/config_loader.py` | Updated `initialize()` method | +3 |
| `src/pogadane/config_loader.py` | Updated `reload()` method | +1 |
| `src/pogadane/config_loader.py` | Added `json` import | +1 |

**Total**: 2 files modified, ~67 lines added

---

## Architecture Improvements

### Settings Persistence Strategy

**Problem**: How to persist UI preferences without modifying `config.py`?

**Solution**: Dual-file approach
- **`config.py`**: User-editable configuration (with comments)
- **`settings.json`**: Runtime preferences (programmatically written)

**Benefits**:
1. ✅ Preserves user comments in `config.py`
2. ✅ Clean separation of concerns
3. ✅ Easy to add new runtime preferences
4. ✅ JSON is simple and human-readable
5. ✅ No complex Python AST manipulation needed

**Example `settings.json`**:
```json
{
  "THEME_MODE": "dark"
}
```

---

## Future Enhancements

1. **Additional Runtime Settings**:
   - Font size preference
   - Window size/position
   - Recent files list
   - Last used prompt template

2. **Migration Path**:
   - Eventually migrate all config to TOML/YAML
   - Would enable full programmatic editing
   - Better for version control

3. **Settings UI**:
   - Settings tab in GUI
   - Visual editor for all preferences
   - Export/import settings

---

## Related Issues

- Fixed as part of code quality improvements session
- Follows singleton pattern in ConfigManager
- Maintains backward compatibility
- No breaking changes to existing code

---

## Validation

- [x] GUI starts without errors
- [x] Theme toggle works
- [x] Theme persists across restarts
- [x] Batch processing works
- [x] Script path resolves correctly
- [x] No attribute errors
- [x] Graceful error handling
- [x] Settings file created in `.config/`

---

## Conclusion

Both runtime errors have been fixed with minimal code changes and proper architecture:

1. **`base_path`**: Simple initialization in `__init__()`
2. **`save_config_to_file`**: Robust settings persistence with JSON

The application now runs without errors and theme preferences persist correctly.
