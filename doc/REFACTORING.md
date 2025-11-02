# Refactoring Guide - Clean Code Architecture

This document describes the clean code refactoring in progress for the Pogadane project.

## ✅ Completed Modules

### 1. **constants.py** - Constants and Configuration Values
Centralized all magic numbers and default configuration values.

**Benefits:**
- Eliminates magic numbers throughout codebase
- Single source of truth for constants
- Easy to update values in one place

**Usage:**
```python
from pogadane.constants import APP_VERSION, DEFAULT_CONFIG, FILE_STATUS_COMPLETED
```

---

### 2. **config_loader.py** - Configuration Management (Factory Pattern)
Provides robust configuration loading with fallback mechanisms.

**Benefits:**
- Factory pattern for creating config objects
- Singleton pattern for config management
- Consistent error handling
- Testable (can mock config easily)

**Usage:**
```python
from pogadane.config_loader import ConfigManager

# Initialize once
config_manager = ConfigManager()
config_manager.initialize()

# Get values with fallback
whisper_model = config_manager.get('WHISPER_MODEL', 'turbo')

# Set runtime values
config_manager.set('DEBUG_MODE', True)
```

---

### 3. **llm_providers.py** - LLM Provider Abstraction (Strategy Pattern)
Abstract interface for LLM providers with concrete implementations.

**Benefits:**
- Strategy pattern allows easy provider switching
- Easy to add new providers (OpenAI, Anthropic, etc.)
- Testable in isolation
- Follows Open/Closed Principle

**Usage:**
```python
from pogadane.llm_providers import LLMProviderFactory

# Create provider based on configuration
provider = LLMProviderFactory.create_provider(
    provider_type='ollama',
    ollama_model='gemma3:4b'
)

# Use provider (same interface for all)
summary = provider.summarize(
    text=transcription,
    prompt=prompt_template,
    language='Polish',
    source_name='meeting.mp3'
)
```

**Adding New Provider:**
```python
class OpenAIProvider(LLMProvider):
    def summarize(self, text, prompt, language, source_name=""):
        # OpenAI-specific implementation
        pass
    
    def is_available(self):
        # Check API key and library
        pass
```

---

### 4. **text_utils.py** - Text Processing Utilities
Utility functions for text manipulation and formatting.

**Benefits:**
- Single Responsibility Principle
- Reusable across GUI and CLI
- Well-tested helper functions

**Usage:**
```python
from pogadane.text_utils import (
    strip_ansi,
    extract_transcription_and_summary,
    insert_with_markdown,
    is_valid_url
)

# Clean ANSI codes from subprocess output
clean_text = strip_ansi(raw_output)

# Extract from log markers
trans, summary = extract_transcription_and_summary(log_text)

# Render markdown in tkinter Text widget
insert_with_markdown(text_widget, markdown_content)

# Validate URLs
if is_valid_url(input_text):
    download_youtube_audio(input_text)
```

---

### 5. **file_utils.py** - File Operations Utilities
Safe file and path manipulation utilities.

**Benefits:**
- Consistent error handling
- Safe operations with proper cleanup
- Cross-platform path handling

**Usage:**
```python
from pogadane.file_utils import (
    get_unique_filename,
    get_input_name_stem,
    safe_delete_file,
    safe_create_directory,
    cleanup_temp_directory,
    find_output_file
)

# Generate unique filename from URL
filename = get_unique_filename('https://youtube.com/watch?v=abc123')

# Extract clean stem from input
stem = get_input_name_stem('/path/to/meeting.mp3')  # Returns: 'meeting'

# Safe file deletion with logging
success = safe_delete_file(temp_file, "temporary audio")

# Create directory safely
if safe_create_directory(output_dir, "output directory"):
    # Directory created successfully
    pass
```

---

## 🔄 Migration Path for Existing Code

### Step 1: Update Imports
Replace old imports with new utility modules:

```python
# OLD
import re
from pathlib import Path

def is_valid_url(text):
    return re.match(r'^https?://', text) is not None

# NEW
from pogadane.text_utils import is_valid_url

# Use directly
if is_valid_url(text):
    # ...
```

### Step 2: Replace Magic Numbers
```python
# OLD
if font_size < 8:
    font_size = 8
if font_size > 24:
    font_size = 24

# NEW
from pogadane.constants import MIN_FONT_SIZE, MAX_FONT_SIZE

if font_size < MIN_FONT_SIZE:
    font_size = MIN_FONT_SIZE
if font_size > MAX_FONT_SIZE:
    font_size = MAX_FONT_SIZE
```

### Step 3: Use ConfigManager
```python
# OLD
config = _load_config_module()
value = getattr(config, 'WHISPER_MODEL', DefaultConfig.WHISPER_MODEL)

# NEW
from pogadane.config_loader import ConfigManager

config_manager = ConfigManager()
config_manager.initialize()
value = config_manager.get('WHISPER_MODEL')
```

### Step 4: Use LLM Provider Pattern
```python
# OLD
if provider == "ollama":
    # Ollama-specific code
    # ...
elif provider == "google":
    # Google-specific code
    # ...

# NEW
from pogadane.llm_providers import LLMProviderFactory

provider = LLMProviderFactory.create_provider(
    provider_type=config_manager.get('SUMMARY_PROVIDER'),
    ollama_model=config_manager.get('OLLAMA_MODEL'),
    google_api_key=config_manager.get('GOOGLE_API_KEY'),
    google_model=config_manager.get('GOOGLE_GEMINI_MODEL'),
    debug_mode=config_manager.get('DEBUG_MODE')
)

summary = provider.summarize(text, prompt, language, source_name)
```

---

## 🎯 Next Steps

### High Priority:
1. **Refactor gui.py**
   - Extract font management to `FontManager` class
   - Extract queue management to `QueueManager` class
   - Extract results display to `ResultsManager` class
   - Use ConfigManager instead of direct config access
   - Use text_utils functions

2. **Refactor transcribe_summarize_working.py**
   - Replace all `getattr(config, ...)` with `config_manager.get(...)`
   - Remove duplicate function definitions
   - Use file_utils for file operations
   - Use LLMProviderFactory for summarization
   - Use text_utils for URL validation

3. **Update tools/pogadane_doctor.py**
   - Use constants for version numbers
   - Use file_utils for safe operations

### Medium Priority:
4. **Add unit tests**
   - Test each utility module
   - Test LLM provider implementations
   - Test config loading edge cases

5. **Add integration tests**
   - Test full transcription pipeline
   - Test batch processing
   - Test GUI components

6. **Improve error handling**
   - Use custom exception classes
   - Add retry logic for network operations
   - Better error messages for users

---

## 📊 Design Patterns Reference

### Strategy Pattern (LLM Providers)
**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable.

```python
class LLMProvider(ABC):
    @abstractmethod
    def summarize(...): pass

class OllamaProvider(LLMProvider): ...
class GoogleGeminiProvider(LLMProvider): ...
```

### Factory Pattern (Config & Provider Creation)
**Intent:** Define an interface for creating objects, letting subclasses decide which class to instantiate.

```python
class LLMProviderFactory:
    @staticmethod
    def create_provider(provider_type, ...):
        if provider_type == "ollama":
            return OllamaProvider(...)
        elif provider_type == "google":
            return GoogleGeminiProvider(...)
```

### Singleton Pattern (Config Manager)
**Intent:** Ensure a class has only one instance and provide global access to it.

```python
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints for all functions
- Write docstrings (Google style)
- Maximum line length: 100 characters
- Maximum function length: 50 lines

### SOLID Principles Checklist
- ✅ **S**ingle Responsibility: Each class/function does one thing
- ✅ **O**pen/Closed: Open for extension, closed for modification
- ✅ **L**iskov Substitution: Subtypes must be substitutable
- ✅ **I**nterface Segregation: Small, focused interfaces
- ✅ **D**ependency Inversion: Depend on abstractions, not concretions

### Testing Guidelines
- Write tests BEFORE refactoring code
- Aim for 80%+ code coverage
- Use mocking for external dependencies
- Test edge cases and error conditions

---

## 📝 Commit Message Format

```
Type: Brief description (50 chars max)

- Detailed change 1 (use Polish for tasks)
- Detailed change 2
- Detailed change 3

Refs: #issue-number (if applicable)
```

**Types:** 
- `Refactor`: Code restructuring without behavior change
- `Feat`: New feature
- `Fix`: Bug fix
- `Docs`: Documentation only
- `Test`: Adding tests
- `Chore`: Maintenance tasks

---

## 🎓 Resources

- **Clean Code** by Robert C. Martin
- **Design Patterns** by Gang of Four
- **Refactoring** by Martin Fowler
- **Python Design Patterns**: https://refactoring.guru/design-patterns/python
- **SOLID Principles**: https://realpython.com/solid-principles-python/

---

**Last Updated:** 2025-11-02  
**Status:** 🟡 In Progress (5/10 modules refactored)  
**Target Completion:** Phase 1 by 2025-11-15
