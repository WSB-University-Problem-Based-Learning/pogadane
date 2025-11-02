# Pogadane - Technical Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Module Structure](#module-structure)
5. [Configuration System](#configuration-system)
6. [GUI Architecture](#gui-architecture)
7. [CLI Architecture](#cli-architecture)
8. [External Dependencies](#external-dependencies)
9. [Error Handling](#error-handling)
10. [Security Considerations](#security-considerations)

---

## System Overview

Pogadane is a modular Python application designed for audio transcription and AI-powered summarization with both GUI and CLI interfaces.

### Key Features

- **Dual Interface**: Graphical (ttkbootstrap) and Command-line
- **Batch Processing**: Sequential processing of multiple audio sources
- **Flexible AI Backend**: Supports local (Ollama) and cloud (Google Gemini) LLMs
- **Speaker Diarization**: Optional speaker identification in transcriptions
- **YouTube Integration**: Direct video-to-text conversion via yt-dlp
- **Privacy-Focused**: Local processing option (Ollama) keeps data on-premises

### Technology Stack

- **Language**: Python 3.8+
- **GUI Framework**: ttkbootstrap (Bootstrap-themed tkinter)
- **Transcription Engine**: Faster-Whisper (standalone binary)
- **Video Download**: yt-dlp (standalone binary)
- **LLM Options**:
  - Ollama (local, offline)
  - Google Gemini API (cloud, online)

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Pogadane Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐              ┌───────────────────────┐   │
│  │   GUI Layer  │              │     CLI Layer         │   │
│  │  (gui.py)    │              │  (transcribe_...py)   │   │
│  └──────┬───────┘              └───────────┬───────────┘   │
│         │                                   │                │
│         └───────────────┬───────────────────┘                │
│                         │                                     │
│              ┌──────────▼──────────┐                         │
│              │   Core Logic        │                         │
│              │   - Audio Download  │                         │
│              │   - Transcription   │                         │
│              │   - Summarization   │                         │
│              └──────────┬──────────┘                         │
│                         │                                     │
│         ┌───────────────┼───────────────┐                    │
│         │               │               │                     │
│    ┌────▼─────┐   ┌────▼────┐   ┌─────▼──────┐             │
│    │ yt-dlp   │   │ Faster  │   │ LLM Engine │             │
│    │ (binary) │   │ Whisper │   │ (Ollama/   │             │
│    │          │   │ (binary)│   │  Gemini)   │             │
│    └──────────┘   └─────────┘   └────────────┘             │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                   Configuration System                       │
│                    (.config/config.py)                       │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### 1. GUI Layer (`src/pogadane/gui.py`)
- User interface management (ttkbootstrap)
- Input validation and file selection
- Batch queue management and progress tracking
- Results presentation with tabbed interface
- Configuration editor with live updates
- Font size adjustment for accessibility

#### 2. CLI Layer (`src/pogadane/transcribe_summarize_working.py`)
- Core business logic implementation
- External process management (subprocesses)
- File I/O operations
- Error handling and logging
- Batch processing from file or arguments

#### 3. Configuration System (`.config/config.py`)
- Centralized settings management
- Dynamic module loading via importlib
- Fallback to default values
- GUI-editable with automatic backup

#### 4. External Binaries
- **yt-dlp**: YouTube audio extraction
- **Faster-Whisper**: Speech-to-text conversion with optional diarization

#### 5. LLM Integration
- **Ollama**: Local model execution via CLI
- **Google Gemini**: Cloud API integration via google-generativeai library

---

## Data Flow

### Standard Processing Pipeline

```
┌─────────────┐
│  User Input │
│ (File/URL)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Input Validation  │
│   & Normalization   │
└──────┬──────────────┘
       │
       ▼
┌──────────────────┐      ┌──────────────┐
│  Is URL?         ├─Yes─▶│   yt-dlp     │
└─────┬────────────┘      │   Download   │
      │No                 └──────┬───────┘
      │                          │
      ▼                          │
┌─────────────────┐             │
│  Local File     │◀────────────┘
│  Preparation    │
└─────┬───────────┘
      │
      ▼
┌─────────────────────┐
│  Faster-Whisper     │
│  Transcription      │
│  (+Diarization?)    │
└─────┬───────────────┘
      │
      ▼
┌────────────────┐
│ Transcription  │
│  Text (.txt)   │
└─────┬──────────┘
      │
      ▼
┌─────────────────────┐
│  LLM Prompt         │
│  Construction       │
│  (Template + Lang)  │
└─────┬───────────────┘
      │
      ▼
┌──────────────────┐      ┌──────────────┐
│  Provider?       ├─ollama▶│   Ollama    │
└─────┬────────────┘      │   Local LLM  │
      │google             └──────┬───────┘
      │                          │
      ▼                          │
┌─────────────────┐             │
│  Google Gemini  │             │
│  API Call       │             │
└─────┬───────────┘             │
      │                         │
      └──────────┬──────────────┘
                 │
                 ▼
         ┌──────────────┐
         │   Summary    │
         │   Text       │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │   Output     │
         │ (GUI/File)   │
         └──────────────┘
```

### Batch Processing Flow (GUI)

```
GUI receives N inputs
    │
    ├─ Parse into list
    │
    ├─ Display in queue (status: ⏳ Pending)
    │
    └─ For each input (sequential):
         │
         ├─ Update status: ⚙️ Processing
         │
         ├─ Spawn thread → Call CLI logic
         │
         ├─ Stream output to console tab
         │
         ├─ Extract transcription & summary from markers
         │
         ├─ Update status: ✅ Completed / ❌ Error
         │
         ├─ Store results in memory
         │
         └─ Update progress bar
    │
    └─ On completion: Switch to Results tab
```

---

## Module Structure

### File Organization

```
src/pogadane/
├── __init__.py                  # Package initialization
├── gui.py                       # GUI application entry point
└── transcribe_summarize_working.py  # CLI & core logic

.config/
└── config.py                    # User configuration (editable)

tools/
└── pogadane_doctor.py          # Setup & maintenance utility

doc/
├── ARCHITECTURE.md             # This file
├── NOTICES.md                  # License information
├── README.md                   # Documentation index
└── cli_help/                   # Command reference
    ├── faster-whisper-xxl_help.txt
    ├── ollama_help.txt
    └── yt-dlp_help.txt
```

### Key Classes and Functions

#### `gui.py`

```python
class TranscriberApp(ttk.Window):
    """Main GUI application window"""
    
    def __init__(self):
        # Initialize ttkbootstrap window
        # Setup font management system
        # Create tabbed interface
        # Initialize configuration editor
    
    def run_batch_script(self):
        # Spawn worker thread for batch processing
        # Manage queue and progress tracking
    
    def _execute_batch_processing_logic(self, sources):
        # Sequential processing of all inputs
        # Calls CLI script for each source
        # Captures and parses output
    
    def display_selected_result(self):
        # Load results from memory
        # Render with Markdown support
    
    def save_config_to_file(self):
        # Serialize GUI settings to config.py
        # Create backup before overwrite
```

**Helper Classes:**
- `ToolTip`: Hover tooltips with font awareness
- `DummyConfigFallback`: Emergency config when file missing

**Helper Functions:**
- `strip_ansi()`: Remove ANSI color codes from subprocess output
- `extract_transcription_and_summary()`: Parse marked sections from log
- `insert_with_markdown()`: Render Markdown in Text widgets

#### `transcribe_summarize_working.py`

```python
class DefaultConfig:
    """Fallback configuration values"""
    FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
    YT_DLP_EXE = "yt-dlp.exe"
    # ... all default settings

def _load_config_module():
    """Dynamically load .config/config.py"""
    # Uses importlib.util for safe loading
    # Falls back to DefaultConfig on error

def run_command(command_list, ...):
    """Execute external binary with error handling"""
    # Subprocess management
    # Debug logging when enabled
    # Platform-specific startup info (Windows)

def download_youtube_audio(url, target_dir):
    """Download audio from YouTube URL"""
    # Calls yt-dlp with mp3 conversion
    # Generates unique filenames
    # Validates output file

def transcribe_audio(audio_path, original_name):
    """Transcribe audio file to text"""
    # Calls Faster-Whisper
    # Applies diarization if enabled
    # Handles multiple output file formats

def summarize_text(text, original_name):
    """Generate AI summary from transcription"""
    # Constructs prompt from template/custom
    # Routes to Ollama or Google Gemini
    # Applies language setting
    # Prints with markers for GUI parsing

def main():
    """CLI entry point with argument parsing"""
    # argparse configuration
    # Batch file support
    # Diarization override flags
    # Output path handling
```

---

## Configuration System

### Configuration Loading Hierarchy

1. **Primary Source**: `.config/config.py` (if exists)
2. **Fallback**: `DefaultConfig` class in CLI script
3. **GUI Overrides**: Temporary in-memory changes (until saved)

### Dynamic Configuration Features

```python
# Configuration is loaded dynamically at runtime
spec = importlib.util.spec_from_file_location("config", CONFIG_PATH)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)
```

**Benefits:**
- No hardcoded paths
- Easy updates without code changes
- User can edit configuration file directly
- GUI can read and write seamlessly

### Configuration Parameters

| Parameter | Type | Purpose |
|-----------|------|---------|
| `FASTER_WHISPER_EXE` | str | Path to transcription binary |
| `YT_DLP_EXE` | str | Path to YouTube downloader |
| `WHISPER_LANGUAGE` | str | Transcription language |
| `WHISPER_MODEL` | str | Whisper model size (tiny to turbo) |
| `ENABLE_SPEAKER_DIARIZATION` | bool | Toggle speaker identification |
| `DIARIZE_METHOD` | str | Diarization algorithm |
| `DIARIZE_SPEAKER_PREFIX` | str | Label for speakers in output |
| `SUMMARY_PROVIDER` | str | "ollama" or "google" |
| `SUMMARY_LANGUAGE` | str | Summary output language |
| `LLM_PROMPT_TEMPLATES` | dict | Named prompt presets |
| `LLM_PROMPT_TEMPLATE_NAME` | str | Selected template |
| `LLM_PROMPT` | str | Custom prompt text |
| `OLLAMA_MODEL` | str | Local LLM model name |
| `GOOGLE_API_KEY` | str | Gemini API credential |
| `GOOGLE_GEMINI_MODEL` | str | Gemini model variant |
| `DEBUG_MODE` | bool | Verbose logging toggle |

---

## GUI Architecture

### Window Structure

```
┌─────────────────────────────────────────────────┐
│  Pogadane GUI v0.1.8         [A+] [A-]          │
├─────────────────────────────────────────────────┤
│  Input Field (Multi-line Text)                  │
│  [➕ Dodaj Pliki Audio]                         │
├─────────────────────────────────────────────────┤
│  [🚀 Rozpocznij Przetwarzanie Wsadowe]          │
├─────────────────────────────────────────────────┤
│  Kolejka Przetwarzania (Treeview)               │
│  ┌──────────────────────┬────────────────────┐  │
│  │ Plik / URL           │ Status             │  │
│  ├──────────────────────┼────────────────────┤  │
│  │ example.mp3          │ ✅ Ukończono       │  │
│  └──────────────────────┴────────────────────┘  │
│  [Progress: 1/3] ████████░░░░░░░░░░░░░░ 33%    │
├─────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────┐  │
│  │ [🖥️ Konsola] [📊 Wyniki] [⚙️ Konfiguracja]│  │
│  ├──────────────────────────────────────────┤  │
│  │                                           │  │
│  │  Tab Content (Dynamic)                    │  │
│  │                                           │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### State Management

**Application State:**
- `processed_results_data`: Dict mapping source → {transcription, summary}
- `batch_processing_thread`: Worker thread reference
- `output_queue`: Thread-safe queue for subprocess communication
- `font_settings`: Dict of font objects for dynamic sizing

**Queue States:**
- ⏳ Pending: Awaiting processing
- ⚙️ Processing: Currently active
- ✅ Completed: Successfully finished
- ❌ Error: Failed with error

### Thread Communication

```python
# GUI Thread (Main)
self.output_queue = queue.Queue()
self.batch_processing_thread = threading.Thread(
    target=self._execute_batch_processing_logic,
    args=(sources,),
    daemon=True
)
self.batch_processing_thread.start()
self._poll_output_queue_for_batch()

# Worker Thread
for source in sources:
    # Process each source
    self.output_queue.put(("update_status", idx, status))
    self.output_queue.put(("log", message, source))
    self.output_queue.put(("result", source, trans, summ))

# Polling Loop (Main Thread)
def _poll_output_queue_for_batch(self):
    try:
        while True:
            msg_type, data1, data2 = self.output_queue.get_nowait()
            # Update GUI based on message type
    except queue.Empty:
        self.after(100, self._poll_output_queue_for_batch)
```

### ScrolledText Widget Handling

**Important Implementation Detail:**

ttkbootstrap's `ScrolledText` is a wrapper widget. Direct text operations must access the inner `.text` property:

```python
# ❌ INCORRECT - Will raise TclError
scrolled_widget.config(state=NORMAL)
scrolled_widget.delete("1.0", END)

# ✅ CORRECT - Access inner Text widget
scrolled_widget.text.config(state=NORMAL)
scrolled_widget.text.delete("1.0", END)
```

---

## CLI Architecture

### Argument Parsing

```python
parser = argparse.ArgumentParser(
    description="Transcribe & Summarize audio/YouTube."
)
parser.add_argument("input_sources", nargs='*')
parser.add_argument("-a", "--batch-file")
parser.add_argument("--diarize", action='store_true')
parser.add_argument("--no-diarize", action='store_true')
parser.add_argument("-o", "--output")
```

### Execution Flow

1. **Parse Arguments**: Extract sources (direct or from batch file)
2. **Load Configuration**: Attempt `.config/config.py` → DefaultConfig
3. **Apply CLI Overrides**: Diarization flags supersede config
4. **Determine Output Mode**:
   - Single input + file path → Write summary to that file
   - Multiple inputs or directory → Write to directory as separate files
   - No `-o` → Print to console only
5. **Process Each Source**:
   - Validate input (URL vs. file)
   - Download if URL
   - Copy to temp if local file
   - Transcribe with Faster-Whisper
   - Summarize with selected LLM
   - Output results
   - Cleanup temp files
6. **Cleanup**: Remove temp directory if empty

### Output Markers for GUI Parsing

The CLI script prints special markers that the GUI searches for:

```
--- POCZĄTEK TRANSKRYPCJI ---
<transcription text here>
--- KONIEC TRANSKRYPCJI ---

--- POCZĄTEK STRESZCZENIA ---
<summary text here>
--- KONIEC STRESZCZENIA ---
```

This allows the GUI to extract structured data from subprocess stdout.

---

## External Dependencies

### Python Libraries

| Library | Purpose | Import |
|---------|---------|--------|
| `ttkbootstrap` | Modern themed Tkinter widgets | `import ttkbootstrap as ttk` |
| `google-generativeai` | Google Gemini API client | `import google.generativeai` |
| Standard Library | subprocess, threading, queue, argparse, importlib, pathlib, re, shutil, time, os, sys | Various |

### External Binaries

#### Faster-Whisper
- **Purpose**: Speech-to-text transcription
- **Communication**: Subprocess with CLI arguments
- **Input**: Audio file path
- **Output**: Text file (txt/srt/vtt/etc.)
- **Special Features**: Diarization, language detection, multiple models

**Example Command:**
```bash
faster-whisper-xxl.exe audio.mp3 --language Polish --model turbo --diarize pyannote_v3.1
```

#### yt-dlp
- **Purpose**: YouTube audio extraction
- **Communication**: Subprocess with CLI arguments
- **Input**: YouTube URL
- **Output**: MP3 file
- **Options**: Format selection, quality control

**Example Command:**
```bash
yt-dlp.exe -x --audio-format mp3 --force-overwrite -o output.mp3 <URL>
```

#### Ollama
- **Purpose**: Local LLM inference
- **Communication**: Subprocess with stdin (prompt text)
- **Input**: Text prompt via stdin
- **Output**: Generated text via stdout
- **Models**: User must download separately (e.g., `ollama pull gemma3:4b`)

**Example Command:**
```bash
ollama run gemma3:4b < prompt.txt
```

---

## Error Handling

### Hierarchical Error Management

```
┌─────────────────────────────────────┐
│  User Action (GUI/CLI)              │
└───────────┬─────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│  Input Validation                   │
│  - File existence                   │
│  - URL format                       │
└───────────┬─────────────────────────┘
            │ ✅ Valid
            ▼
┌─────────────────────────────────────┐
│  External Process Execution         │
│  - try/except subprocess.run()      │
│  - Check return codes               │
│  - Validate output files            │
└───────────┬─────────────────────────┘
            │
            ├─ ❌ Error → Log & Skip
            │
            ▼ ✅ Success
┌─────────────────────────────────────┐
│  Result Processing                  │
│  - File I/O exceptions              │
│  - Parsing errors                   │
└───────────┬─────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│  User Feedback                      │
│  - GUI: Status updates, error tabs  │
│  - CLI: Stderr messages, exit codes │
└─────────────────────────────────────┘
```

### Error Categories

1. **Configuration Errors**:
   - Missing `.config/config.py` → Use defaults + warning
   - Invalid config syntax → Use defaults + error message

2. **Dependency Errors**:
   - Binary not found (yt-dlp, faster-whisper) → Clear error message with path
   - Missing Python library → Import error with installation hint

3. **Runtime Errors**:
   - Network failures (YouTube download) → Retry logic not implemented, fails with message
   - File I/O errors → Logged with path and reason
   - Subprocess crashes → Captured stderr, logged

4. **LLM Errors**:
   - Ollama not running → Connection error
   - Google API key invalid → API error message
   - Model not available → Specific model error

### Logging Strategy

```python
# Debug mode (when enabled)
if debug_mode:
    print(f"🐞 DEBUG: Running command: {cmd_str}")
    print(f"☑️ CMD exit code: {process.returncode}")
    print(f"--- stdout ---\n{process.stdout.strip()}")
    print(f"--- stderr ---\n{process.stderr.strip()}")

# Production mode (default)
else:
    if process.returncode == 0:
        print(f"☑️ CMD finished successfully")
    else:
        print(f"⚠️ CMD Warning: Exited with {process.returncode}")
```

---

## Security Considerations

### Data Privacy

✅ **Local Processing** (Ollama mode):
- Audio files never leave the computer
- Transcriptions processed locally
- LLM inference on local machine
- No external API calls

⚠️ **Cloud Processing** (Google Gemini mode):
- Transcription text sent to Google servers
- Subject to Google's privacy policy
- Requires API key (credential management)
- Internet connection required

### File System Safety

1. **Temp File Management**:
   - Unique filenames prevent collisions
   - Cleanup after processing
   - Temp directory in project folder (not system temp)

2. **Path Validation**:
   - Uses `pathlib.Path` for cross-platform safety
   - No arbitrary path execution
   - Config paths can be relative or absolute

3. **Process Isolation**:
   - External binaries run in subprocess
   - Passes arguments as a list (avoids shell=True for safer argument escaping)
   - Startup info hides windows on Windows

### Credential Management

**Google API Key:**
- Stored in `.config/config.py` (plain text)
- ⚠️ User responsible for file permissions
- Not committed to version control (.gitignore)
- Recommended: Use environment variables for production

**Future Improvements:**
- Keyring integration
- Encrypted storage option
- Environment variable support

### Input Sanitization

**URL Handling:**
```python
def is_valid_url(text):
    return re.match(r'^https?://', text) is not None
```

**File Path Handling:**
```python
audio_path = Path(audio_path_str)
if not audio_path.is_file():
    print(f"❌ Error: Audio file not found")
    return None
```

**Command Construction:**
```python
# Uses list format, not shell strings
command = [exe_path, str(input_file), "--language", lang]
# NOT: f"{exe_path} {input_file} --language {lang}"
```

---

## Performance Considerations

### Bottlenecks

1. **Transcription** (Slowest):
   - Depends on audio length and model size
   - GPU acceleration available (CUDA)
   - Estimated: 1-5x real-time (1 hour audio = 12-60 min processing)

2. **LLM Summarization**:
   - Local (Ollama): Fast, depends on model size
   - Cloud (Gemini): Network latency + API limits
   - Estimated: 5-30 seconds per summary

3. **YouTube Download**:
   - Network bandwidth dependent
   - No progress tracking implemented
   - Estimated: 10-60 seconds per video

### Optimization Strategies

**Current:**
- Sequential batch processing (one at a time)
- Subprocess reuse for same binary
- Temp file cleanup after each item

**Potential Improvements:**
- Parallel processing with thread pool
- Caching of downloaded YouTube audio
- Progress callbacks for long operations
- Model preloading for faster-whisper
- Batch LLM API calls (Gemini supports this)

### Resource Usage

**Memory:**
- GUI: ~50-100 MB base
- Faster-Whisper: 1-4 GB (model dependent)
- Ollama: 2-8 GB (model dependent)
- Peak: ~10 GB with large models

**Disk:**
- Project code: <10 MB
- Models (downloaded separately):
  - Faster-Whisper: 1-3 GB
  - Ollama models: 2-7 GB each
- Temp audio files: Cleaned after processing
- Output files: Negligible (<1 MB per summary)

**Network:**
- YouTube downloads: Video bitrate dependent
- Ollama: None (local only)
- Gemini: ~1 KB per API call (text only)

---

## Future Architecture Considerations

### Planned Enhancements

1. **Plugin System**:
   - Custom LLM providers
   - Alternative transcription engines
   - Output format converters

2. **Database Integration**:
   - SQLite for result history
   - Search functionality
   - Tag and categorize transcripts

3. **API Server**:
   - RESTful API for remote access
   - Webhook notifications
   - Job queue management

4. **Advanced UI**:
   - Real-time transcription preview
   - Audio player integration
   - Transcript editing tools

### Scalability Paths

**Current Limitations:**
- Single-machine processing
- Sequential batch execution
- No distributed computing

**Scaling Options:**
- Celery task queue for async processing
- Docker containerization
- Kubernetes for multi-node deployment
- Cloud functions for serverless model

---

## Development Guidelines

### Code Style

- **PEP 8** compliance for Python code
- **Type hints** encouraged but not enforced
- **Docstrings** for all public functions and classes
- **Comments** for complex logic blocks

### Testing

**Current State:**
- Manual testing via GUI and CLI
- No automated test suite

**Recommended:**
- Unit tests for core functions
- Integration tests for subprocess calls
- GUI automation with pytest-qt
- CI/CD with GitHub Actions

### Version Control

**Branch Strategy:**
- `main`: Stable releases
- `feature/*`: New development
- `bugfix/*`: Issue fixes

**Commit Messages:**
- English headers for global audience
- Polish bullet points for local team
- Reference issue numbers

---

## Troubleshooting Guide for Developers

### Common Development Issues

1. **Import Errors**:
   - Ensure virtual environment is activated
   - Check `PYTHONPATH` includes project root
   - Verify `src/pogadane/__init__.py` exists

2. **Configuration Not Loading**:
   - Validate `.config/config.py` syntax
   - Check `importlib` error messages
   - Confirm file path resolution

3. **GUI Not Starting**:
   - Verify `ttkbootstrap` installation
   - Check for Tkinter availability (OS-dependent)
   - Review console for stack traces

4. **Subprocess Failures**:
   - Test binaries directly in terminal
   - Check file permissions (execute bit)
   - Review debug logs with `DEBUG_MODE=True`

### Debugging Tools

```python
# Enable debug mode in config
DEBUG_MODE = True

# Or set environment variable
import os
os.environ['DEBUG'] = '1'

# Logging to file
import logging
logging.basicConfig(
    filename='pogadane_debug.log',
    level=logging.DEBUG
)
```

---

## Conclusion

Pogadane's architecture prioritizes:
- **Modularity**: Separate GUI, CLI, and core logic
- **Flexibility**: Multiple LLM backends, configurable pipelines
- **Privacy**: Local processing option
- **Usability**: Simple GUI for non-technical users
- **Extensibility**: Easy to add new features

For questions or contributions, see the main `README.md` and project repository.

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-02  
**Maintainer**: Pogadane Development Team
