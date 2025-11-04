# Pogadane# Pogadane# Pogadane# Pogadane# Pogadane



<p align="center">

  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>

</p><p align="center">



<p align="center">  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>

  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>

</p></p><p align="center">



---



## Highlights<p align="center">  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>



- 🎙️ Batch transcription for local audio files and YouTube URLs  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>

- 🤖 Summaries powered by Ollama, local Transformers, or Google Gemini

- 🖥️ Material 3 Expressive GUI with waveform visualisation and results viewer</p></p><p align="center"><p align="center">

- ⚙️ Configuration stored in `.config/config.py` with in-app overrides

- 🧰 Cross-platform installer that prepares dependencies in one pass



------



## Quick Start



```bash## Highlights<p align="center">  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>

# 1. Clone and enter the project

git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git

cd pogadane

- 🎙️ Batch transcription for local audio files and YouTube URLs  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>

# 2. Create a virtual environment (recommended)

python -m venv .venv- 🤖 Summaries powered by Ollama, local Transformers, or Google Gemini

.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# source .venv/bin/activate    # macOS/Linux- 🖥️ Material 3 Expressive GUI with waveform visualisation and results viewer</p></p></p>



# 3. Install project requirements- ⚙️ Configuration stored in `.config/config.py` with in-app overrides

pip install -r requirements.txt

- 🧰 Cross-platform installer that prepares dependencies in one pass

# 4. Run the guided installer

python install.py --lightweight



# 5. Launch the GUI------

python run_gui_flet.py

```



---## Quick Start



## Installation



### Guided Installer (Recommended)```bash## Highlights<p align="center"><p align="center">



```bash# 1. Clone and enter the project

python install.py                # interactive wizard

python install.py --full         # all features + external binariesgit clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git

python install.py --lightweight  # pure Python toolchain

python install.py --dev          # adds developer toolingcd pogadane

```

- 🎙️ Batch transcription for local audio files and YouTube URLs  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>

### Manual Setup

# 2. Create a virtual environment (recommended)

1. **Install Python 3.9+** and ensure `python`/`pip` are on PATH

2. **Install dependencies:**python -m venv .venv- 🤖 Summaries powered by Ollama, local Transformers, or Google Gemini

   ```bash

   pip install -r requirements.txt.\.venv\Scripts\Activate.ps1  # Windows PowerShell

   pip install -r requirements-transformers.txt   # optional: local AI

   pip install -r requirements-whisper.txt        # optional: Python Whisper# source .venv/bin/activate    # macOS/Linux- 🖥️ Material 3 Expressive GUI with waveform visualisation and results viewer</p>## Pogadane

   ```

3. **Download optional binaries:**

   - yt-dlp: https://github.com/yt-dlp/yt-dlp/releases

   - faster-whisper-xxl.exe: https://github.com/Purfview/whisper-standalone-win# 3. Install project requirements- ⚙️ Configuration stored in `.config/config.py` with in-app overrides



---pip install -r requirements.txt



## Running Pogadane- 🧰 Cross-platform installer that prepares dependencies in one pass



### GUI# 4. Run the guided installer



```bashpython install.py --lightweight

python run_gui_flet.py

```



Features:# 5. Launch the GUI------Pogadane turns long-form audio recordings and YouTube videos into searchable transcripts and AI-assisted summaries that stay on your machine. The project ships with a modern Material 3 GUI and a CLI workflow.

- 🎨 Material Design 3 with Flutter

- 📊 Waveform visualisation and topic timelinepython run_gui_flet.py

- 📋 Queue management with per-file results

- 🌓 Automatic dark/light mode```

- 💫 60fps animations



### CLI

---## Quick Start

```bash

# Single file

python -m pogadane.transcribe_summarize_working audio.mp3

## Installation Options

# Multiple files

python -m pogadane.transcribe_summarize_working file1.mp3 file2.wav https://youtube.com/watch?v=...



# Options### Guided Installer (Recommended)```bash## Highlights---

python -m pogadane.transcribe_summarize_working --help

```



---```bash# 1. Clone and enter the project



## Configurationpython install.py                # interactive wizard



Settings are in `.config/config.py`. Edit the file directly or use the GUI Settings dialog (⚙️ icon).python install.py --full         # all features + external binariesgit clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git



**Transcription:**python install.py --lightweight  # pure Python toolchain

- `TRANSCRIPTION_PROVIDER` — `"faster-whisper"` or `"whisper"`

- `WHISPER_MODEL` — `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"`, `"turbo"`python install.py --dev          # adds developer toolingcd pogadane

- `WHISPER_LANGUAGE` — e.g., `"pl"`, `"en"`

- `ENABLE_SPEAKER_DIARIZATION` — `True`/`False````



**Summarization:**- 🎙️ Batch transcription for local audio files and YouTube URLs## Highlights

- `SUMMARY_PROVIDER` — `"ollama"`, `"transformers"`, or `"google"`

- `OLLAMA_MODEL` — e.g., `"gemma3:4b"`The installer validates Python, installs dependencies, downloads helper binaries when needed, and creates `.config/config.py` with sensible defaults.

- `TRANSFORMERS_MODEL` — e.g., `"facebook/bart-large-cnn"`

- `GOOGLE_API_KEY` — your Gemini API key# 2. Create a virtual environment (recommended)

- `SUMMARY_LANGUAGE` — e.g., `"Polish"`, `"English"`

### Manual Setup

**External Tools:**

- `YT_DLP_EXE` — path to yt-dlppython -m venv .venv- 🤖 Summaries powered by Ollama, local Transformers, or Google Gemini

- `FASTER_WHISPER_EXE` — path to faster-whisper-xxl.exe

1. **Install Python 3.9+** and ensure `python`/`pip` are on PATH

---

2. **Install core dependencies:**.\.venv\Scripts\Activate.ps1  # Windows PowerShell

## Transcription Options

   ```bash

### Faster-Whisper (Recommended)

- ✅ GPU acceleration (CUDA)   pip install -r requirements.txt# source .venv/bin/activate    # macOS/Linux- 🖥️ Material 3 Expressive GUI with waveform visualisation and results viewer- 🎙️ Batch transcription for local audio files and YouTube URLs

- ✅ Speaker diarization

- ✅ Best quality and speed   ```

- ⚠️ Requires external binary (~2GB)

3. **Install optional components:**

**Setup:**

1. Download from https://github.com/Purfview/whisper-standalone-win/releases   ```bash

2. Configure `FASTER_WHISPER_EXE` in `.config/config.py`

   # For local AI summaries (no Ollama needed)# 3. Install project requirements- ⚙️ Configuration stored in `.config/config.py` with in-app overrides- 🤖 Summaries powered by Ollama, local Transformers, or Google Gemini

### Whisper (Python)

- ✅ Pure Python, no binaries   pip install -r requirements-transformers.txt

- ✅ Easy: `pip install -r requirements-whisper.txt`

- ⚠️ No speaker diarization   pip install -r requirements.txt

- ⚠️ Slower

   # For Python-based Whisper transcription

**Setup:**

```bash   pip install -r requirements-whisper.txt- 🧰 Cross-platform installer that prepares dependencies in one pass- 🖥️ Material 3 Expressive GUI with waveform visualisation and results viewer

pip install -r requirements-whisper.txt

```   

Set `TRANSCRIPTION_PROVIDER = "whisper"` in config.

   # For development tools# 4. Run the guided installer

---

   pip install -r requirements-dev.txt

## Summary Options

   ```python install.py --lightweight- ⚙️ Configuration stored in `.config/config.py` with in-app overrides

### Ollama (Recommended)

- ✅ Completely local and private4. **Download helper binaries** (optional, for advanced features):

- ✅ Multi-language support

- ✅ Best quality   - `yt-dlp` for YouTube downloads — https://github.com/yt-dlp/yt-dlp/releases



**Setup:**   - `faster-whisper-xxl.exe` for GPU-accelerated transcription — https://github.com/Purfview/whisper-standalone-win

1. Install from https://ollama.com/

2. `ollama pull gemma3:4b`5. **Configure paths** via the GUI settings dialog or edit `.config/config.py` directly# 5. Launch the GUI---- 🧰 Cross-platform installer (`install.py`) that prepares dependencies in one pass

3. Set `SUMMARY_PROVIDER = "ollama"`



### Transformers (Lightweight)

- ✅ Pure Python---python run_gui_flet.py

- ✅ Lightweight (300MB-1.6GB)

- ⚠️ English only



**Setup:**## Running Pogadane```

```bash

pip install -r requirements-transformers.txt

```

Set `SUMMARY_PROVIDER = "transformers"`### GUI



**Models:**

- `"google/flan-t5-small"` (~300MB, fastest)

- `"sshleifer/distilbart-cnn-12-6"` (~500MB)```bash---## Quick Start---

- `"google/flan-t5-base"` (~900MB)

- `"facebook/bart-large-cnn"` (~1.6GB, best)python run_gui_flet.py



### Google Gemini (Cloud)```

- ✅ Excellent quality

- ✅ Multi-language

- ⚠️ Requires internet & API key

Features:## Installation Options

**Setup:**

1. Get key from https://aistudio.google.com/- 🎨 Modern Material Design 3 with Flutter

2. Set `GOOGLE_API_KEY` in `.config/config.py`

3. Set `SUMMARY_PROVIDER = "google"`- 📊 Waveform visualisation and topic timeline



---- 📋 Queue management with per-file results



## Development- 🌓 Automatic dark/light mode### Option A — Guided Installer (Recommended)```bash## Quick Start



```bash- 💫 Smooth 60fps animations

# Install dev dependencies

pip install -r requirements-dev.txt



# Run tests### CLI

pytest

```bash# 1. Clone and enter the project

# Code quality

black src/ test/Process single file:

flake8 src/ test/

pylint src/pogadane/```bashpython install.py                # interactive wizard

mypy src/pogadane/

```python -m pogadane.transcribe_summarize_working audio_file.mp3



**Project Structure:**```python install.py --full         # all features + external binariesgit clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git```bash

```

pogadane/

├── src/pogadane/

│   ├── gui_flet.py                         # Material 3 GUIProcess multiple sources:python install.py --lightweight  # pure Python toolchain

│   ├── transcribe_summarize_working.py     # CLI

│   ├── config_loader.py                    # Config handling```bash

│   ├── llm_providers.py                    # Summary providers

│   └── transcription_providers.py          # Transcriptionpython -m pogadane.transcribe_summarize_working file1.mp3 file2.wav https://youtube.com/watch?v=...python install.py --dev          # adds developer toolingcd pogadane# 1. Clone and enter the project

├── test/                                    # Tests

├── tools/                                   # Installation tools```

├── .config/                                 # User config

└── requirements*.txt                        # Dependencies```

```

Common options:

---

- `--config path/to/config.py` — use custom configgit clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git

## Troubleshooting

- `--output-dir path/to/results` — save results directory

**GUI won't start:**

```bash- `--summary-provider {ollama,transformers,google}` — override summary providerThe installer validates Python, installs dependencies, downloads helper binaries when needed, and creates `.config/config.py` with sensible defaults.

# Install dependencies

pip install -r requirements.txt- `--help` — show all options

# Run from project root

python run_gui_flet.py# 2. Create a virtual environment (recommended)cd pogadane

```

---

**Transcription issues:**

- Missing faster-whisper: Configure path in GUI Settings or switch to `whisper` provider### Option B — Manual Setup

- Missing whisper module: `pip install -r requirements-whisper.txt`

## Configuration

**Summary issues:**

- Ollama not responding: Check service is running (`ollama list`)python -m venv .venv

- Transformers out of memory: Use smaller model (`"google/flan-t5-small"`)

- Gemini API error: Check API key and internet connectionRuntime settings are stored in `.config/config.py`. You can:



**Performance:**- Edit the file directly with any text editor1. **Install Python 3.9+** and ensure `python`/`pip` are on PATH

- First run downloads models (1-2GB, normal)

- Ongoing slowness: Try smaller model or enable GPU- Use the Settings dialog (⚙️ icon) in the GUI



---2. **Install core dependencies:**.\.venv\Scripts\Activate.ps1  # Windows PowerShell# 2. Create a virtual environment (optional but recommended)



## License & CreditsKey settings:



- **License:** [MIT](LICENSE)   ```bash

- **Third-party Licenses:** [NOTICES.md](NOTICES.md)

- **Maintained by:** WSB University Problem-Based Learning**Transcription:**

- **Issues:** https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues

- `TRANSCRIPTION_PROVIDER` — `"faster-whisper"` (external binary) or `"whisper"` (Python library)   pip install -r requirements.txt# source .venv/bin/activate    # macOS/Linuxpython -m venv .venv

---

- `WHISPER_MODEL` — Model size: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"`, `"turbo"`

## Quick Reference

- `WHISPER_LANGUAGE` — Language code (e.g., `"pl"`, `"en"`)   ```

### Full Setup

```bash- `ENABLE_SPEAKER_DIARIZATION` — `True` or `False` (requires Faster-Whisper)

git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git

cd pogadane3. **Install optional components:**.\.venv\Scripts\Activate.ps1  # PowerShell on Windows

python -m venv .venv

.\.venv\Scripts\Activate.ps1**Summarization:**

pip install -r requirements.txt

pip install -r requirements-transformers.txt- `SUMMARY_PROVIDER` — `"ollama"` (local), `"transformers"` (local, lightweight), or `"google"` (cloud)   ```bash

python run_gui_flet.py

```- `OLLAMA_MODEL` — Model name (e.g., `"gemma3:4b"`)



### Lightweight Setup- `TRANSFORMERS_MODEL` — Model name (e.g., `"facebook/bart-large-cnn"`)   # For local AI summaries (no Ollama needed)# 3. Install project requirements

```bash

pip install -r requirements.txt- `GOOGLE_API_KEY` — Your Google Gemini API key (required for `"google"` provider)

pip install -r requirements-whisper.txt

pip install -r requirements-transformers.txt- `SUMMARY_LANGUAGE` — Language for summary (e.g., `"Polish"`, `"English"`)   pip install -r requirements-transformers.txt

python run_gui_flet.py

```



Set in `.config/config.py`:**External Tools:**   pip install -r requirements.txt# 3. Install project requirements and run the guided setup

- `TRANSCRIPTION_PROVIDER = "whisper"`

- `SUMMARY_PROVIDER = "transformers"`- `YT_DLP_EXE` — Path to `yt-dlp.exe` (or `"yt-dlp"` if on PATH)



### Commands- `FASTER_WHISPER_EXE` — Path to `faster-whisper-xxl.exe`   # For Python-based Whisper transcription

```bash

python run_gui_flet.py                                          # GUI

python -m pogadane.transcribe_summarize_working audio.mp3       # CLI single

python -m pogadane.transcribe_summarize_working *.mp3 *.wav     # CLI batch---   pip install -r requirements-whisper.txtpip install -r requirements.txt

pytest                                                          # Tests

```


## Transcription Providers   



### Faster-Whisper (Recommended)   # For development tools# 4. Run the guided installerpython install.py --lightweight

- ✅ GPU acceleration (CUDA)

- ✅ Speaker diarization   pip install -r requirements-dev.txt

- ✅ Best quality and speed

- ⚠️ Requires external binary (~2GB download)   ```python install.py --lightweight



**Setup:**4. **Download helper binaries** (optional, for advanced features):

1. Download from https://github.com/Purfview/whisper-standalone-win/releases

2. Extract and configure `FASTER_WHISPER_EXE` in `.config/config.py`   - `yt-dlp` for YouTube downloads — https://github.com/yt-dlp/yt-dlp/releases# 4. Launch the GUI



### Whisper (Python Library)   - `faster-whisper-xxl.exe` for GPU-accelerated transcription — https://github.com/Purfview/whisper-standalone-win

- ✅ Pure Python, no external binaries

- ✅ Easy installation: `pip install -r requirements-whisper.txt`5. **Configure paths** via the GUI settings dialog or edit `.config/config.py` directly# 5. Launch the GUIpython -m pogadane.gui

- ⚠️ No speaker diarization

- ⚠️ Slower than Faster-Whisper



**Setup:**---python run_gui_flet.py```

```bash

pip install -r requirements-whisper.txt

```

Set `TRANSCRIPTION_PROVIDER = "whisper"` in config.## Running Pogadane```



---



## Summary Providers### GUI (Recommended)Re-run the installer with `--full` for yt-dlp/Faster-Whisper helpers or `--dev` when you need pytest and linters.



### Ollama (Recommended for Offline Use)

- ✅ Completely local and private

- ✅ Multi-language support**Material 3 Expressive (Latest):**---

- ✅ Best quality summaries

- ⚠️ Requires ~4GB RAM and model download```bash



**Setup:**python run_gui_flet.py---

1. Install Ollama from https://ollama.com/

2. Pull a model: `ollama pull gemma3:4b````

3. Set `SUMMARY_PROVIDER = "ollama"` in config

## Installation Options

### Transformers (Lightweight)

- ✅ Pure Python, no external servicesFeatures:

- ✅ Lightweight (300MB-1.6GB models)

- ✅ Easy installation: `pip install -r requirements-transformers.txt`- 🎨 Modern Material Design 3 with Flutter## Installation Options

- ⚠️ English summaries only

- ⚠️ Lower quality than Ollama/Gemini- 📊 Waveform visualisation and topic timeline



**Setup:**- 📋 Queue management with per-file results### Option A — Guided Installer (Recommended)

```bash

pip install -r requirements-transformers.txt- 🌓 Automatic dark/light mode

```

Set `SUMMARY_PROVIDER = "transformers"` in config.- 💫 Smooth 60fps animations### Option A — Guided Installer (Recommended)



**Available models:**

- `"google/flan-t5-small"` (~300MB, fastest)

- `"sshleifer/distilbart-cnn-12-6"` (~500MB)**Legacy GUI (Stable):**```bash

- `"google/flan-t5-base"` (~900MB)

- `"facebook/bart-large-cnn"` (~1.6GB, best quality)```bash



### Google Gemini (Cloud)python -m pogadane.guipython install.py                # interactive wizard```bash

- ✅ Excellent quality

- ✅ Multi-language support```

- ✅ No local resources needed

- ⚠️ Requires internet connectionpython install.py --full         # all features + external binariespython install.py            # interactive wizard

- ⚠️ Requires API key (free tier available)

### CLI Workflow

**Setup:**

1. Get API key from https://aistudio.google.com/python install.py --lightweight  # pure Python toolchainpython install.py --full     # all features + external binaries

2. Set `GOOGLE_API_KEY = "your_key_here"` in `.config/config.py`

3. Set `SUMMARY_PROVIDER = "google"` in configProcess single file:



---```bashpython install.py --dev          # adds developer toolingpython install.py --lightweight  # pure Python toolchain



## Developmentpython -m pogadane.transcribe_summarize_working audio_file.mp3



### Running Tests``````python install.py --dev      # adds developer tooling

```bash

pip install -r requirements-dev.txt

pytest

```Process multiple sources:```



### Code Quality```bash

```bash

# Format codepython -m pogadane.transcribe_summarize_working file1.mp3 file2.wav https://youtube.com/watch?v=...The installer validates Python, installs dependencies, downloads helper binaries when needed, and creates `.config/config.py` with sensible defaults.

black src/ test/

```

# Lint

flake8 src/ test/The script validates Python, installs project dependencies, downloads helper binaries when needed, and writes `.config/config.py` with sensible defaults.

pylint src/pogadane/

Common options:

# Type checking

mypy src/pogadane/- `--config path/to/config.py` — use custom config### Option B — Manual Setup

```

- `--output-dir path/to/results` — save results directory

### Project Structure

```- `--summary-provider {ollama,transformers,google}` — override summary provider### Option B — Manual Setup

pogadane/

├── src/pogadane/          # Main application code- `--help` — show all options

│   ├── gui_flet.py        # Material 3 GUI

│   ├── transcribe_summarize_working.py  # CLI1. **Install Python 3.9+** and ensure `python`/`pip` are on PATH

│   ├── config_loader.py   # Configuration handling

│   ├── llm_providers.py   # Summary providers---

│   └── transcription_providers.py  # Transcription providers

├── test/                  # Test suite2. **Install core dependencies:**1. Install Python 3.9+ and ensure `python`/`pip` are on PATH.

├── tools/                 # Installation and maintenance tools

├── .config/              # User configuration## Configuration

├── requirements*.txt     # Dependency specifications

└── install.py            # Installation wizard   ```bash2. Install core dependencies:

```

Runtime settings are stored in `.config/config.py`. You can:

---

- Edit the file directly with any text editor   pip install -r requirements.txt   ```bash

## Troubleshooting

- Use the Settings dialog (⚙️ icon) in the GUI

### GUI Won't Start

**Error:** `No module named 'flet'`   ```   pip install -r requirements.txt

- **Solution:** Install dependencies: `pip install -r requirements.txt`

Key settings:

**Error:** `ModuleNotFoundError: No module named 'pogadane'`

- **Solution:** Run from project root: `python run_gui_flet.py` (not `python -m run_gui_flet`)3. **Install optional components:**   pip install -r requirements-transformers.txt   # optional local summaries



### Transcription Issues**Transcription:**

**Error:** `File not found: faster-whisper-xxl.exe`

- **Solution 1:** Configure path in GUI Settings (⚙️ icon)- `TRANSCRIPTION_PROVIDER` — `"faster-whisper"` (external binary) or `"whisper"` (Python library)   ```bash   pip install -r requirements-whisper.txt        # optional Whisper backend

- **Solution 2:** Switch to Whisper: `pip install -r requirements-whisper.txt` and set `TRANSCRIPTION_PROVIDER = "whisper"`

- **Solution 3:** Place `faster-whisper-xxl.exe` in project root- `WHISPER_MODEL` — Model size: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"`, `"turbo"`



**Error:** `No module named 'whisper'`- `WHISPER_LANGUAGE` — Language code (e.g., `"pl"`, `"en"`)   # For local AI summaries (no Ollama needed)   ```

- **Solution:** Install Whisper: `pip install -r requirements-whisper.txt`

- `ENABLE_SPEAKER_DIARIZATION` — `True` or `False` (requires Faster-Whisper)

### Summary Issues

**Error:** Ollama not responding   pip install -r requirements-transformers.txt3. Download helper binaries if required:

- **Check:** Ollama service is running (system tray icon)

- **Verify:** Run `ollama list` to confirm model is downloaded**Summarization:**

- **Test:** Try `ollama run gemma3:4b` in terminal

- `SUMMARY_PROVIDER` — `"ollama"` (local), `"transformers"` (local, lightweight), or `"google"` (cloud)      - `yt-dlp` for YouTube downloads — <https://github.com/yt-dlp/yt-dlp/releases>

**Error:** Transformers out of memory

- **Solution:** Use smaller model in config: `TRANSFORMERS_MODEL = "google/flan-t5-small"`- `OLLAMA_MODEL` — Model name (e.g., `"gemma3:4b"`)



**Error:** Google Gemini API error- `TRANSFORMERS_MODEL` — Model name (e.g., `"facebook/bart-large-cnn"`)   # For Python-based Whisper transcription   - `faster-whisper-xxl.exe` for high-quality transcription — <https://github.com/Purfview/whisper-standalone-win>

- **Check:** Valid API key in `.config/config.py`

- **Verify:** `SUMMARY_PROVIDER = "google"` in config- `GOOGLE_API_KEY` — Your Google Gemini API key (required for `"google"` provider)

- **Internet:** Ensure active connection

- **Quota:** Check limits at https://aistudio.google.com/- `SUMMARY_LANGUAGE` — Language for summary (e.g., `"Polish"`, `"English"`)   pip install -r requirements-whisper.txt4. Point to the binaries via the GUI settings dialog or by editing `.config/config.py` (`YT_DLP_EXE`, `FASTER_WHISPER_EXE`).



### YouTube Download Issues

- **Update yt-dlp:** Download latest from https://github.com/yt-dlp/yt-dlp/releases

- **Check internet:** Ensure active connection**External Tools:**   

- **Age-restricted videos:** May require cookies/authentication

- `YT_DLP_EXE` — Path to `yt-dlp.exe` (or `"yt-dlp"` if on PATH)

### Performance Issues

**First run is slow:**- `FASTER_WHISPER_EXE` — Path to `faster-whisper-xxl.exe`   # For development tools---

- Models are downloaded on first use (1-2GB for Whisper models)

- This is normal and only happens once



**Ongoing slowness:**---   pip install -r requirements-dev.txt

- Try smaller Whisper model: `"base"` or `"small"`

- Check Task Manager for CPU/memory usage

- Enable GPU if available (Faster-Whisper only)

## Transcription Providers   ```## Running Pogadane

---



## License & Credits

### Faster-Whisper (Recommended)4. **Download helper binaries** (optional, for advanced features):

- **Project License:** [MIT](LICENSE)

- **Third-party Licenses:** [NOTICES.md](NOTICES.md)- ✅ GPU acceleration (CUDA)

- **Maintained by:** WSB University Problem-Based Learning

- **Contributions:** Welcome! See issues at https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues- ✅ Speaker diarization   - `yt-dlp` for YouTube downloads — https://github.com/yt-dlp/yt-dlp/releases### GUI (Material 3 Expressive)



---- ✅ Best quality and speed



## Quick Reference- ⚠️ Requires external binary (~2GB download)   - `faster-whisper-xxl.exe` for GPU-accelerated transcription — https://github.com/Purfview/whisper-standalone-win



### Recommended Setup (All Features)

```bash

# 1. Install Python 3.9+**Setup:**5. **Configure paths** via the GUI settings dialog or edit `.config/config.py` directly```bash

# 2. Clone repository

git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git1. Download from https://github.com/Purfview/whisper-standalone-win/releases

cd pogadane

2. Extract and configure `FASTER_WHISPER_EXE` in `.config/config.py`python -m pogadane.gui

# 3. Create virtual environment

python -m venv .venv

.\.venv\Scripts\Activate.ps1  # Windows

# source .venv/bin/activate    # macOS/Linux### Whisper (Python Library)---```



# 4. Install dependencies- ✅ Pure Python, no external binaries

pip install -r requirements.txt

pip install -r requirements-transformers.txt  # for local AI- ✅ Easy installation: `pip install -r requirements-whisper.txt`



# 5. Install Ollama (optional, for best summaries)- ⚠️ No speaker diarization

# Download from https://ollama.com/

ollama pull gemma3:4b- ⚠️ Slower than Faster-Whisper## Running Pogadane- Queue files and URLs on the **Kolejka** tab



# 6. Run GUI

python run_gui_flet.py

```**Setup:**- Track progress in the persistent status bar



### Minimal Setup (Lightweight)```bash

```bash

# Pure Python, no external binariespip install -r requirements-whisper.txt### GUI (Recommended)- Review waveform, topic timeline, transcription, and summary inside **Przeglądarka Wyników**

pip install -r requirements.txt

pip install -r requirements-whisper.txt```

pip install -r requirements-transformers.txt

python run_gui_flet.pySet `TRANSCRIPTION_PROVIDER = "whisper"` in config.- Inspect runtime logs on the **Konsola** tab

```



Set in `.config/config.py`:

- `TRANSCRIPTION_PROVIDER = "whisper"`---**Material 3 Expressive (Latest):**

- `SUMMARY_PROVIDER = "transformers"`



### Common Commands

```bash## Summary Providers```bash### CLI Workflow

# GUI

python run_gui_flet.py



# CLI - Single file### Ollama (Recommended for Offline Use)python run_gui_flet.py

python -m pogadane.transcribe_summarize_working audio.mp3

- ✅ Completely local and private

# CLI - Multiple files

python -m pogadane.transcribe_summarize_working file1.mp3 file2.wav url.youtube.com- ✅ Multi-language support``````bash



# CLI - Batch file- ✅ Best quality summaries

python -m pogadane.transcribe_summarize_working -a batch_list.txt -o output_dir/

- ⚠️ Requires ~4GB RAM and model downloadpython -m pogadane.transcribe_summarize_working <audio_or_url> [more_sources]

# Tests

pytest

```

**Setup:**Features:```

---

1. Install Ollama from https://ollama.com/

**For more help:** https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues

2. Pull a model: `ollama pull gemma3:4b`- 🎨 Modern Material Design 3 with Flutter

3. Set `SUMMARY_PROVIDER = "ollama"` in config

- 📊 Waveform visualisation and topic timelineCommon flags:

### Transformers (Lightweight)

- ✅ Pure Python, no external services- 📋 Queue management with per-file results

- ✅ Lightweight (300MB-1.6GB models)

- ✅ Easy installation: `pip install -r requirements-transformers.txt`- 🌓 Automatic dark/light mode- `--config path/to/config.py`

- ⚠️ English summaries only

- ⚠️ Lower quality than Ollama/Gemini- 💫 Smooth 60fps animations- `--output-dir path/to/results`



**Setup:**- `--summary-provider {ollama,transformers,google}`

```bash

pip install -r requirements-transformers.txt**Legacy GUI (Stable):**

```

Set `SUMMARY_PROVIDER = "transformers"` in config.```bashRun with `--help` to see the full command list.



**Available models:**python -m pogadane.gui

- `"google/flan-t5-small"` (~300MB, fastest)

- `"sshleifer/distilbart-cnn-12-6"` (~500MB)```---

- `"google/flan-t5-base"` (~900MB)

- `"facebook/bart-large-cnn"` (~1.6GB, best quality)



### Google Gemini (Cloud)### CLI Workflow## Configuration

- ✅ Excellent quality

- ✅ Multi-language support

- ✅ No local resources needed

- ⚠️ Requires internet connectionProcess single file:Runtime options live in `.config/config.py`. Edit the file directly or use the Settings dialog (gear icon) in the GUI—both paths keep the same configuration file up to date.

- ⚠️ Requires API key (free tier available)

```bash

**Setup:**

1. Get API key from https://aistudio.google.com/python -m pogadane.transcribe_summarize_working audio_file.mp3Key settings:

2. Set `GOOGLE_API_KEY = "your_key_here"` in `.config/config.py`

3. Set `SUMMARY_PROVIDER = "google"` in config```



---- `TRANSCRIPTION_PROVIDER` — `faster-whisper` or `whisper`



## DevelopmentProcess multiple sources:- `SUMMARY_PROVIDER` — `ollama`, `transformers`, or `google`



### Running Tests```bash- Model names (`WHISPER_MODEL`, `TRANSFORMERS_MODEL`, `OLLAMA_MODEL`)

```bash

pip install -r requirements-dev.txtpython -m pogadane.transcribe_summarize_working file1.mp3 file2.wav https://youtube.com/watch?v=...- External tool paths (`YT_DLP_EXE`, `FASTER_WHISPER_EXE`)

pytest

``````



### Code Quality---

```bash

# Format codeCommon options:

black src/ test/

- `--config path/to/config.py` — use custom config## Development Workflow

# Lint

flake8 src/ test/- `--output-dir path/to/results` — save results directory

pylint src/pogadane/

- `--summary-provider {ollama,transformers,google}` — override summary provider```bash

# Type checking

mypy src/pogadane/- `--help` — show all optionspip install -r requirements-dev.txt

```

pytest

### Project Structure

```---```

pogadane/

├── src/pogadane/          # Main application code

│   ├── gui_flet.py        # Material 3 GUI

│   ├── gui.py             # Legacy GUI## ConfigurationHandy scripts:

│   ├── transcribe_summarize_working.py  # CLI

│   ├── config_loader.py   # Configuration handling

│   ├── llm_providers.py   # Summary providers

│   └── transcription_providers.py  # Transcription providersRuntime settings are stored in `.config/config.py`. You can:- `python tools/dependency_manager.py --verify-only` — confirm external binaries (Windows)

├── test/                  # Test suite

├── tools/                 # Installation and maintenance tools- Edit the file directly with any text editor- `python tools/pogadane_doctor.py` — legacy diagnostics when the new installer is unavailable

├── .config/              # User configuration

├── requirements*.txt     # Dependency specifications- Use the Settings dialog (⚙️ icon) in the GUI

└── install.py            # Installation wizard

```Before opening a PR, run tests (`pytest`) and your preferred linters/formatters.



---Key settings:



## Troubleshooting---



### GUI Won't Start**Transcription:**

**Error:** `No module named 'flet'`

- **Solution:** Install dependencies: `pip install -r requirements.txt`- `TRANSCRIPTION_PROVIDER` — `"faster-whisper"` (external binary) or `"whisper"` (Python library)## Troubleshooting



**Error:** `ModuleNotFoundError: No module named 'pogadane'`- `WHISPER_MODEL` — Model size: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"`, `"turbo"`

- **Solution:** Run from project root: `python run_gui_flet.py` (not `python -m run_gui_flet`)

- `WHISPER_LANGUAGE` — Language code (e.g., `"pl"`, `"en"`)- Re-run `python install.py --full` to repair a broken environment

### Transcription Issues

**Error:** `File not found: faster-whisper-xxl.exe`- `ENABLE_SPEAKER_DIARIZATION` — `True` or `False` (requires Faster-Whisper)- Confirm binary paths in `.config/config.py`

- **Solution 1:** Configure path in GUI Settings (⚙️ icon)

- **Solution 2:** Switch to Whisper: `pip install -r requirements-whisper.txt` and set `TRANSCRIPTION_PROVIDER = "whisper"`- Use the **Konsola** tab to inspect runtime logs

- **Solution 3:** Place `faster-whisper-xxl.exe` in project root

**Summarization:**- File issues at <https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues>

**Error:** `No module named 'whisper'`

- **Solution:** Install Whisper: `pip install -r requirements-whisper.txt`- `SUMMARY_PROVIDER` — `"ollama"` (local), `"transformers"` (local, lightweight), or `"google"` (cloud)



### Summary Issues- `OLLAMA_MODEL` — Model name (e.g., `"gemma3:4b"`)---

**Error:** Ollama not responding

- **Check:** Ollama service is running (system tray icon)- `TRANSFORMERS_MODEL` — Model name (e.g., `"facebook/bart-large-cnn"`)

- **Verify:** Run `ollama list` to confirm model is downloaded

- **Test:** Try `ollama run gemma3:4b` in terminal- `GOOGLE_API_KEY` — Your Google Gemini API key (required for `"google"` provider)## License & Notices



**Error:** Transformers out of memory- `SUMMARY_LANGUAGE` — Language for summary (e.g., `"Polish"`, `"English"`)

- **Solution:** Use smaller model in config: `TRANSFORMERS_MODEL = "google/flan-t5-small"`

- Project license: [MIT](LICENSE)

**Error:** Google Gemini API error

- **Check:** Valid API key in `.config/config.py`**External Tools:**- Third-party licenses: [NOTICES.md](NOTICES.md)

- **Verify:** `SUMMARY_PROVIDER = "google"` in config

- **Internet:** Ensure active connection- `YT_DLP_EXE` — Path to `yt-dlp.exe` (or `"yt-dlp"` if on PATH)

- **Quota:** Check limits at https://aistudio.google.com/

- `FASTER_WHISPER_EXE` — Path to `faster-whisper-xxl.exe`Pogadane is maintained by WSB University Problem-Based Learning. Contributions and bug reports are always welcome!

### YouTube Download Issues

- **Update yt-dlp:** Download latest from https://github.com/yt-dlp/yt-dlp/releases1.  **Uzyskaj Klucz API Google Gemini:**

- **Check internet:** Ensure active connection

- **Age-restricted videos:** May require cookies/authentication---      * Przejdź do Google AI Studio ([https://aistudio.google.com/](https://aistudio.google.com/)).



### Performance Issues      * Zaloguj się kontem Google.

**First run is slow:**

- Models are downloaded on first use (1-2GB for Whisper models)## Transcription Providers      * Utwórz nowy projekt lub wybierz istniejący.

- This is normal and only happens once

      * Wygeneruj klucz API ("Get API key"). Skopiuj go i przechowuj w bezpiecznym miejscu.

**Ongoing slowness:**

- Try smaller Whisper model: `"base"` or `"small"`### Faster-Whisper (Recommended)2.  **Konfiguracja w `pogadane`:**

- Check Task Manager for CPU/memory usage

- Enable GPU if available (Faster-Whisper only)- ✅ GPU acceleration (CUDA)    * Otwórz plik `.config/config.py` (lub użyj GUI).



---- ✅ Speaker diarization      * Ustaw `SUMMARY_PROVIDER = "google"`.



## License & Credits- ✅ Best quality and speed      * Wklej swój klucz API do `GOOGLE_API_KEY = "TWOJ_KLUCZ_API_TUTAJ"`.



- **Project License:** [MIT](LICENSE)- ⚠️ Requires external binary (~2GB download)      * Możesz również dostosować `GOOGLE_GEMINI_MODEL` (domyślnie "gemini-1.5-flash-latest").

- **Third-party Licenses:** [NOTICES.md](NOTICES.md)

- **Maintained by:** WSB University Problem-Based Learning

- **Contributions:** Welcome! See issues at https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues

**Setup:**#### Krok 5: Instalacja bibliotek Python dla GUI i Google API

---

1. Download from https://github.com/Purfview/whisper-standalone-win/releases

## Quick Reference

2. Extract and configure `FASTER_WHISPER_EXE` in `.config/config.py`Aby uruchomić interfejs graficzny oraz korzystać z Google Gemini API, potrzebne są dodatkowe biblioteki Python. Jeśli nie użyłeś `pogadane_doctor.py`, zainstaluj je ręcznie:

### Recommended Setup (All Features)

```bash

# 1. Install Python 3.9+

# 2. Clone repository### Whisper (Python Library)1.  Otwórz terminal PowerShell.

git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git

cd pogadane- ✅ Pure Python, no external binaries2.  Wpisz polecenia:



# 3. Create virtual environment- ✅ Easy installation: `pip install -r requirements-whisper.txt`    ```powershell

python -m venv .venv

.\.venv\Scripts\Activate.ps1  # Windows- ⚠️ No speaker diarization    pip install ttkbootstrap

# source .venv/bin/activate    # macOS/Linux

- ⚠️ Slower than Faster-Whisper    pip install google-generativeai

# 4. Install dependencies

pip install -r requirements.txt    ```

pip install -r requirements-transformers.txt  # for local AI

**Setup:**    Poczekaj na zakończenie instalacji.

# 5. Install Ollama (optional, for best summaries)

# Download from https://ollama.com/```bash

ollama pull gemma3:4b

pip install -r requirements-whisper.txt-----

# 6. Run GUI

python run_gui_flet.py```

```

Set `TRANSCRIPTION_PROVIDER = "whisper"` in config.## Konfiguracja Pliku `.config/config.py`

### Minimal Setup (Lightweight)

```bash

# Pure Python, no external binaries

pip install -r requirements.txt---Skrypt `src/pogadane/transcribe_summarize_working.py` oraz interfejs `src/pogadane/gui.py` zarządzają konfiguracją w następujący sposób:

pip install -r requirements-whisper.txt

pip install -r requirements-transformers.txt

python run_gui_flet.py

```## Summary Providers1.  **Plik `.config/config.py` (Zalecane):** Aplikacja w pierwszej kolejności próbuje załadować konfigurację z pliku `.config/config.py`. Skrypt `pogadane_doctor.py` pobiera najnowszą wersję tego pliku z repozytorium (tworząc backup Twojej lokalnej wersji, jeśli istnieje).



Set in `.config/config.py`:    * **Edycja przez GUI:** Możesz wygodnie edytować większość opcji konfiguracyjnych bezpośrednio w zakładce "⚙️ Konfiguracja" w aplikacji GUI. Zmiany są zapisywane do pliku `.config/config.py`.

- `TRANSCRIPTION_PROVIDER = "whisper"`

- `SUMMARY_PROVIDER = "transformers"`### Ollama (Recommended for Offline Use)    * **Edycja Manualna:** Możesz również bezpośrednio edytować plik `.config/config.py`.



### Common Commands- ✅ Completely local and private2.  **Konfiguracja Domyślna (Fallback):** Jeśli plik `.config/config.py` nie zostanie znaleziony, skrypt CLI i GUI użyją predefiniowanych wartości domyślnych.

```bash

# GUI- ✅ Multi-language support

python run_gui_flet.py                    # Material 3 GUI

python -m pogadane.gui                    # Legacy GUI- ✅ Best quality summaries**Aby dostosować konfigurację, zaleca się użycie zakładki "Konfiguracja" w GUI lub edycję pliku `.config/config.py` (po jego pobraniu przez `pogadane_doctor.py` lub ręcznie).**



# CLI - Single file- ⚠️ Requires ~4GB RAM and model download

python -m pogadane.transcribe_summarize_working audio.mp3

Przykładowa zawartość pliku `.config/config.py` znajduje się w repozytorium (i jest pobierana przez `pogadane_doctor.py`).

# CLI - Multiple files

python -m pogadane.transcribe_summarize_working file1.mp3 file2.wav url.youtube.com**Setup:**



# CLI - Batch file1. Install Ollama from https://ollama.com/**Opis opcji konfiguracyjnych (dostępnych w `config.py` oraz w GUI):**

python -m pogadane.transcribe_summarize_working -a batch_list.txt -o output_dir/

2. Pull a model: `ollama pull gemma3:4b`

# Tests

pytest3. Set `SUMMARY_PROVIDER = "ollama"` in config  * `FASTER_WHISPER_EXE`: Ścieżka do `faster-whisper-xxl.exe`.

```

  * `YT_DLP_EXE`: Ścieżka do `yt-dlp.exe`.

---

### Transformers (Lightweight)  * `WHISPER_LANGUAGE`: Język transkrypcji dla Faster Whisper (domyślnie "Polish").

**For more help:** https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues

- ✅ Pure Python, no external services  * `WHISPER_MODEL`: Model Faster Whisper (domyślnie "turbo").

- ✅ Lightweight (300MB-1.6GB models)  * `ENABLE_SPEAKER_DIARIZATION`: Włącza/wyłącza diaryzację mówców (domyślnie `False`).

- ✅ Easy installation: `pip install -r requirements-transformers.txt`  * `DIARIZE_METHOD`: Metoda diaryzacji (np. `"pyannote_v3.1"`).

- ⚠️ English summaries only  * `DIARIZE_SPEAKER_PREFIX`: Prefiks dla mówców (np. `"MÓWCA"`).

- ⚠️ Lower quality than Ollama/Gemini  * `SUMMARY_PROVIDER`: Wybór systemu do generowania podsumowań. Dostępne opcje: `"ollama"` (domyślnie, lokalnie) lub `"google"` (wymaga `GOOGLE_API_KEY` i połączenia z internetem).

  * `SUMMARY_LANGUAGE`: Język, w którym ma być wygenerowane podsumowanie (domyślnie "Polish").

**Setup:**  * `LLM_PROMPT_TEMPLATES`: Słownik zawierający predefiniowane szablony promptów dla LLM. Klucze to nazwy szablonów, a wartości to rdzenie promptów. GUI pozwala wybrać jeden z nich.

```bash  * `LLM_PROMPT_TEMPLATE_NAME`: Nazwa wybranego szablonu promptu z `LLM_PROMPT_TEMPLATES`. Jeśli ustawiona, ten szablon zostanie użyty.

pip install -r requirements-transformers.txt  * `LLM_PROMPT`: Niestandardowy rdzeń promptu używany, gdy `LLM_PROMPT_TEMPLATE_NAME` jest puste, nie wskazuje na istniejący szablon, lub gdy w GUI wybrano opcję promptu niestandardowego (opcja "(Własny prompt poniżej)"). Skrypt automatycznie dołączy instrukcję językową (`SUMMARY_LANGUAGE`) oraz tekst transkrypcji.

```  * `OLLAMA_MODEL`: Model językowy Ollama (używany, gdy `SUMMARY_PROVIDER="ollama"`, domyślnie "gemma3:4b").

Set `SUMMARY_PROVIDER = "transformers"` in config.  * `GOOGLE_API_KEY`: Klucz API do Google Gemini (wymagany, gdy `SUMMARY_PROVIDER="google"`). **Pamiętaj, aby go uzupełnić\!**

  * `GOOGLE_GEMINI_MODEL`: Model Google Gemini (używany, gdy `SUMMARY_PROVIDER="google"`, domyślnie "gemini-1.5-flash-latest").

**Available models:**  * `DOWNLOADED_AUDIO_FILENAME`: Bazowa nazwa tymczasowego pliku audio pobieranego z YouTube. Skrypt może dodać do niej unikalny identyfikator przy przetwarzaniu wielu URL-i.

- `"google/flan-t5-small"` (~300MB, fastest)  * `TRANSCRIPTION_FORMAT`: Format pliku wyjściowego transkrypcji używany wewnętrznie przez skrypt CLI (domyślnie 'txt').

- `"sshleifer/distilbart-cnn-12-6"` (~500MB)  * `DEBUG_MODE`: Ustaw na `True`, aby włączyć bardziej szczegółowe logowanie w konsoli, w tym pełne wyniki stdout/stderr dla uruchamianych komend. Domyślnie `False`.

- `"google/flan-t5-base"` (~900MB)

- `"facebook/bart-large-cnn"` (~1.6GB, best quality)-----



### Google Gemini (Cloud)## Uruchomienie Aplikacji (Wersja Alpha v0.1.8+)

- ✅ Excellent quality

- ✅ Multi-language support1.  **Przygotuj Środowisko:** Uruchom `pogadane_doctor.py` lub wykonaj kroki instalacji ręcznej.

- ✅ No local resources needed2.  **Skonfiguruj `config.py`:** Upewnij się, że `config.py` jest poprawnie skonfigurowany (ścieżki do narzędzi, modele, klucze API jeśli potrzebne). Możesz to zrobić przez GUI lub edytując plik bezpośrednio.

- ⚠️ Requires internet connection

- ⚠️ Requires API key (free tier available)### Uruchomienie Interfejsu Graficznego (GUI) (Zalecane)



**Setup:**Pogadane oferuje **trzy interfejsy graficzne** do wyboru:

1. Get API key from https://aistudio.google.com/

2. Set `GOOGLE_API_KEY = "your_key_here"` in `.config/config.py`#### � Material 3 Expressive GUI (NAJNOWSZY - Zalecany)

3. Set `SUMMARY_PROVIDER = "google"` in configNajnowocześniejszy interfejs z prawdziwym Material Design 3, płynnymi animacjami 60fps i renderowaniem Flutter.



---```powershell

python run_gui_flet.py

## Development```



### Running Tests**Funkcje:**

```bash- 💫 Płynne animacje 60fps (Flutter)

pip install -r requirements-dev.txt- 🌓 Automatyczne wykrywanie motywu systemowego

pytest- 🎨 Prawdziwy Material Design 3 (nie tylko inspirowany!)

```- 📱 Wersja webowa dostępna (`flet run --web`)

- 🔔 Natywne powiadomienia (snackbars)

### Code Quality- 📂 Natywne okna dialogowe systemu

```bash- 🚀 Potencjał mobilny (Android/iOS w przyszłości)

# Format code

black src/ test/**Dokumentacja:** [GUI_MATERIAL_3_EXPRESSIVE.md](doc/GUI_MATERIAL_3_EXPRESSIVE.md)



# Lint#### 🎨 Material Design GUI (CustomTkinter)

flake8 src/ test/Nowoczesny interfejs z Material Design, wsparciem dla trybu ciemnego i zaokrąglonymi rogami.

pylint src/pogadane/

```powershell

# Type checkingpython run_gui_material.py

mypy src/pogadane/```

```

**Funkcje:**

### Project Structure- 🌙 Przełącznik trybu ciemnego/jasnego

```- 🎯 Nowoczesny wygląd Material Design 2

pogadane/- 📱 Zaokrąglone rogi i karty

├── src/pogadane/          # Main application code- ⚡ Szybkie uruchamianie

│   ├── gui_flet.py        # Material 3 GUI

│   ├── gui.py             # Legacy GUI**Dokumentacja:** [GUI_MATERIAL_DESIGN.md](doc/GUI_MATERIAL_DESIGN.md)

│   ├── transcribe_summarize_working.py  # CLI

│   ├── config_loader.py   # Configuration handling#### 🖥️ Legacy Bootstrap GUI

│   ├── llm_providers.py   # Summary providersStabilny, sprawdzony interfejs w stylu Bootstrap.

│   └── transcription_providers.py  # Transcription providers

├── test/                  # Test suite```powershell

├── tools/                 # Installation and maintenance toolspython -m pogadane.gui

├── .config/              # User configuration```

├── requirements*.txt     # Dependency specifications

└── install.py            # Installation wizard**Funkcje:**

```- 🏆 Maksymalna stabilność

- ⚡ Najlżejszy (najmniej pamięci)

---- 🔧 Sprawdzony w boju



## Troubleshooting**Zobacz również:** [Porównanie GUI](doc/GUI_COMPARISON_ALL.md) aby wybrać najlepszą opcję dla siebie.



### GUI Won't Start#### Korzystanie z GUI (wszystkie wersje):

**Error:** `No module named 'flet'`

- **Solution:** Install dependencies: `pip install -r requirements.txt`1.  **Otwórz Terminal:** Otwórz terminal PowerShell.

2.  **Przejdź do Katalogu Projektu:** Użyj polecenia `cd`, aby przejść do katalogu, w którym umieściłeś pliki.

**Error:** `ModuleNotFoundError: No module named 'pogadane'`    ```powershell

- **Solution:** Run from project root: `python run_gui_flet.py` (not `python -m run_gui_flet`)    cd "C:\Sciezka\Do\Twojego\Katalogu\Pogadane"

    ```

### Transcription Issues3.  **Uruchom wybraną wersję GUI** (zobacz powyżej)

**Error:** `File not found: faster-whisper-xxl.exe`

- **Solution 1:** Configure path in GUI Settings (⚙️ icon)4.  **Korzystanie z GUI:**

- **Solution 2:** Switch to Whisper: `pip install -r requirements-whisper.txt` and set `TRANSCRIPTION_PROVIDER = "whisper"`      * **Dane Wejściowe:** W polu tekstowym "Pliki audio / URL-e YouTube" wprowadź jedną lub więcej ścieżek do lokalnych plików audio lub URL-i YouTube, **każdą w nowej linii**. Możesz użyć przycisku "➕ Dodaj Pliki Audio" do wybrania i dodania plików.

- **Solution 3:** Place `faster-whisper-xxl.exe` in project root      * **Kolejka Przetwarzania:** Poniżej pola wejściowego znajduje się tabela "Kolejka Przetwarzania", która wyświetli dodane pliki i ich status podczas przetwarzania.

      * **Konfiguracja:** Przejdź do zakładki "⚙️ Konfiguracja", aby dostosować ustawienia. Pamiętaj, aby kliknąć "💾 Zapisz i Zastosuj". Dostępne są również przyciski "A+" / "A-" do zmiany rozmiaru czcionki w aplikacji. Wiele elementów interfejsu posiada podpowiedzi (tooltips) po najechaniu myszką.

**Error:** `No module named 'whisper'`      * **Uruchomienie:** Kliknij przycisk "🚀 Rozpocznij Przetwarzanie Wsadowe". Aplikacja przetworzy każde źródło sekwencyjnie. Postęp ogólny będzie widoczny na pasku postępu.

- **Solution:** Install Whisper: `pip install -r requirements-whisper.txt`      * **Wyniki:**

          * **🖥️ Konsola:** Wyświetla szczegółowe logi z całego procesu przetwarzania.

### Summary Issues          * **📊 Wyniki (Transkrypcje i Streszczenia):** Ta zakładka zawiera listę rozwijaną "Wybierz przetworzony plik". Po wybraniu pliku z tej listy, jego indywidualna transkrypcja i streszczenie zostaną wyświetlone w odpowiednich polach poniżej.

**Error:** Ollama not responding      * **Zapisywanie:** Przycisk "💾 Zapisz Log" w zakładce "Konsola" pozwala zapisać cały log. Indywidualne transkrypcje i streszczenia można skopiować z pól w zakładce "Wyniki".

- **Check:** Ollama service is running (system tray icon)

- **Verify:** Run `ollama list` to confirm model is downloaded### Uruchomienie Skryptu z Linii Komend (CLI)

- **Test:** Try `ollama run gemma3:4b` in terminal

Skrypt `transcribe_summarize_working.py` obsługuje przetwarzanie wsadowe.

**Error:** Transformers out of memory

- **Solution:** Use smaller model in config: `TRANSFORMERS_MODEL = "google/flan-t5-small"`1.  **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell i przejdź do katalogu ze skryptami.



**Error:** Google Gemini API error2.  **Wykonaj Polecenie Uruchomienia Skryptu:**

- **Check:** Valid API key in `.config/config.py`

- **Verify:** `SUMMARY_PROVIDER = "google"` in config    **Ogólny wzór:**

- **Internet:** Ensure active connection

- **Quota:** Check limits at https://aistudio.google.com/    ```powershell

    python -m pogadane.transcribe_summarize_working [<ścieżka1_LUB_URL1> <ścieżka2_LUB_URL2>...] [-a <plik_wsadowy.txt>] [--diarize | --no-diarize] [-o "<ścieżka_do_katalogu_LUB_pliku_podsumowania>"]

### YouTube Download Issues    ```

- **Update yt-dlp:** Download latest from https://github.com/yt-dlp/yt-dlp/releases

- **Check internet:** Ensure active connection      * `<ścieżka1_LUB_URL1> ...`: Jedna lub więcej ścieżek do plików audio lub URL-i YouTube, podanych bezpośrednio. Można pominąć, jeśli używana jest opcja `-a`.

- **Age-restricted videos:** May require cookies/authentication      * `-a <plik_wsadowy.txt>` lub `--batch-file <plik_wsadowy.txt>`: Ścieżka do pliku tekstowego z listą źródeł (jedno na linię).

      * `--diarize` | `--no-diarize`: Nadpisuje ustawienie diaryzacji z `config.py`.

### Performance Issues      * `-o "<ścieżka_wyjściowa>"`:

**First run is slow:**          * Jeśli podano jedno wejście (i `-o` nie jest istniejącym katalogiem oraz nie wygląda jak katalog bez rozszerzenia): pełna ścieżka do pliku podsumowania.

- Models are downloaded on first use (1-2GB for Whisper models)          * Jeśli podano wiele wejść (bezpośrednio lub przez `-a`) LUB jeśli `-o` wskazuje na istniejący katalog (lub nie istnieje, ale nie ma rozszerzenia): ścieżka do KATALOGU, gdzie zostaną zapisane pliki podsumowań (np. `nazwa_pliku.summary.txt`).

- This is normal and only happens once

    **Przykłady:**

**Ongoing slowness:**

- Try smaller Whisper model: `"base"` or `"small"`    ```powershell

- Check Task Manager for CPU/memory usage    # Przetwarzanie jednego pliku, zapis podsumowania do konkretnego pliku

- Enable GPU if available (Faster-Whisper only)    python -m pogadane.transcribe_summarize_working "C:\Nagrania\spotkanie.mp3" -o "C:\Podsumowania\spotkanie_summary.txt"



---    # Przetwarzanie wielu URL-i, zapis podsumowań do katalogu "WynikiYouTube"

    python -m pogadane.transcribe_summarize_working "URL_YOUTUBE_1" "URL_YOUTUBE_2" -o "C:\MojeDokumenty\WynikiYouTube"

## License & Credits

    # Przetwarzanie z pliku wsadowego, podsumowania drukowane do konsoli

- **Project License:** [MIT](LICENSE)    python -m pogadane.transcribe_summarize_working -a "C:\lista_do_przetworzenia.txt"

- **Third-party Licenses:** [NOTICES.md](NOTICES.md)    ```

- **Maintained by:** WSB University Problem-Based Learning

- **Contributions:** Welcome! See issues at https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues3.  **Monitoruj Proces:** Skrypt wyświetli postęp przetwarzania dla każdego pliku.



------



## Quick Reference## Quick Start (English)



### Recommended Setup (All Features)This short Quick Start helps non-experts run the Pogadane GUI or CLI on Windows.

```bashIt's intentionally minimal — follow Polish docs above for full details.

# 1. Install Python 3.9+

# 2. Clone repositoryPrerequisites (simple):

git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git- Windows

cd pogadane- Python 3.8+ installed (select "Add Python to PATH" during install)

- Optional: Faster-Whisper standalone (`faster-whisper-xxl.exe`), `yt-dlp.exe`, or Ollama if you plan to use those features.

# 3. Create virtual environment

python -m venv .venv1) Create and activate a virtual environment (recommended):

.\.venv\Scripts\Activate.ps1  # Windows

# source .venv/bin/activate    # macOS/Linux```powershell

cd C:\path\to\pogadane

# 4. Install dependenciespython -m venv .venv

pip install -r requirements.txt& .\.venv\Scripts\Activate.ps1

pip install -r requirements-transformers.txt  # for local AI```



# 5. Install Ollama (optional, for best summaries)2) Install Python dependencies (GUI + Google API client):

# Download from https://ollama.com/

ollama pull gemma3:4b```powershell

pip install --upgrade pip

# 6. Run GUIpip install ttkbootstrap google-generativeai

python run_gui_flet.py```

```

3) (Optional) Run the helper script to fetch recommended files and Python packages:

### Minimal Setup (Lightweight)

```bash```powershell

# Pure Python, no external binariespython tools\pogadane_doctor.py

pip install -r requirements.txt```

pip install -r requirements-whisper.txt

pip install -r requirements-transformers.txt4) Configure optional external tools:

python run_gui_flet.py- If you want to transcribe YouTube videos, download `yt-dlp.exe` and put its path in `.config\config.py` or keep it in the project folder.

```- For transcription, choose one option:

  * **Faster-Whisper (recommended)**: Download Faster-Whisper standalone and set `FASTER_WHISPER_EXE` in `.config\config.py`. Best quality, GPU support, speaker diarization.

Set in `.config/config.py`:  * **Whisper (lightweight)**: Run `pip install -r requirements-whisper.txt`. Pure Python, no executables needed. Models: 75MB-3GB.

- `TRANSCRIPTION_PROVIDER = "whisper"`- For AI summaries, choose one option:

- `SUMMARY_PROVIDER = "transformers"`  * **Ollama (recommended)**: Install Ollama and pull a model (e.g. `ollama pull gemma3:4b`). Multi-language support.

  * **Transformers (lightweight)**: Run `pip install -r requirements-transformers.txt`. No Ollama needed, but English summaries only.

### Common Commands  * **Google Gemini**: Set `GOOGLE_API_KEY` in `.config\config.py`. Requires internet.

```bash

# GUI5) Run the GUI (recommended for beginners):

python run_gui_flet.py                    # Material 3 GUI

python -m pogadane.gui                    # Legacy GUI```powershell

# from project root with venv activated

# CLI - Single filepython -m pogadane.gui

python -m pogadane.transcribe_summarize_working audio.mp3```



# CLI - Multiple files6) Run the CLI (batch runs / automation):

python -m pogadane.transcribe_summarize_working file1.mp3 file2.wav url.youtube.com

```powershell

# CLI - Batch filepython -m pogadane.transcribe_summarize_working "C:\path\to\file.mp3" -o "C:\path\to\summary.txt"

python -m pogadane.transcribe_summarize_working -a batch_list.txt -o output_dir/

# or multiple sources

# Testspython -m pogadane.transcribe_summarize_working "URL1" "C:\file2.wav" -o "C:\output_dir"

pytest```

```

7) Sample test audio included:

---- `samples/` contains `Styrta się pali.mp3` (small test audio taken from YouTube). Use it to verify a complete run.



**For more help:** https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues### Troubleshooting


**Problem: "Python is not recognized as an internal or external command"**
- **Solution:** Reinstall Python and ensure "Add Python to PATH" is checked during installation
- **Verify:** Open new PowerShell and run `python --version`

**Problem: "No module named 'ttkbootstrap'" or "No module named 'google.generativeai'"**
- **Solution:** Activate virtual environment and install dependencies:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

**Problem: "No module named 'transformers'" or "No module named 'torch'"**
- **Solution:** You're using `SUMMARY_PROVIDER="transformers"` but libraries aren't installed:
  ```powershell
  pip install -r requirements-transformers.txt
  # Or manually: pip install transformers torch
  ```
- **Verify:** `python -c "import transformers; print('OK')"`

**Problem: "No module named 'whisper'"**
- **Solution:** You're using `TRANSCRIPTION_PROVIDER="whisper"` but library isn't installed:
  ```powershell
  pip install -r requirements-whisper.txt
  # Or manually: pip install openai-whisper
  ```
- **Verify:** `python -c "import whisper; print('OK')"`

**Problem: GUI window doesn't open**
- **Check:** Are you in the correct directory? (`cd C:\path\to\pogadane`)
- **Check:** Is venv activated? (you should see `(.venv)` in prompt)
- **Try:** Run with full module path: `python -m pogadane.gui`
- **Check logs:** Look for error messages in terminal

**Problem: Transcription fails with "File not found: faster-whisper-xxl.exe"**
- **Solution:** Configure path in GUI (⚙️ Konfiguracja tab → Plik Faster Whisper → click 📂)
- **Alternative:** Use lightweight Whisper: `pip install -r requirements-whisper.txt` and set `TRANSCRIPTION_PROVIDER="whisper"` in config
- **Alternative:** Place `faster-whisper-xxl.exe` in project root directory
- **Verify:** Check `.config/config.py` has correct `FASTER_WHISPER_EXE` path

**Problem: YouTube download fails**
- **Solution:** Ensure `yt-dlp.exe` is in project folder or configured in settings
- **Check:** Internet connection is active
- **Update:** Download latest version from [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases/latest)

**Problem: Summary generation fails with Ollama**
- **Check:** Ollama service is running (should be in system tray)
- **Verify model:** Run `ollama list` to confirm model is downloaded
- **Test:** Try `ollama run gemma3:4b` in terminal
- **Logs:** Check GUI Console tab for detailed error messages

**Problem: Summary generation fails with Google Gemini**
- **Check:** Valid API key is set in `.config/config.py` (`GOOGLE_API_KEY`)
- **Verify:** `SUMMARY_PROVIDER` is set to `"google"` in configuration
- **Internet:** Ensure you have active internet connection
- **Quota:** Check if you've exceeded free tier limits at [Google AI Studio](https://aistudio.google.com/)

**Problem: Transcription is in wrong language**
- **Solution:** Set correct language in GUI (⚙️ Konfiguracja → Język transkrypcji)
- **Save:** Click 💾 Zapisz i Zastosuj after making changes

**Problem: "Access Denied" or permission errors**
- **Solution:** Run PowerShell as Administrator
- **Alternative:** Install project in user directory (e.g., `C:\Users\YourName\Documents\pogadane`)

**Problem: Process is slow or freezes**
- **First transcription:** Faster-Whisper downloads models on first run (this is normal, ~1-2GB)
- **Check:** Task Manager → ensure Python isn't using 100% CPU indefinitely
- **Try:** Smaller model in settings (⚙️ Konfiguracja → Model Whisper → try "small" or "base")

**Problem: Virtual environment activation fails with "execution of scripts is disabled"**
- **Solution:** Enable script execution (run PowerShell as Administrator):
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Then retry:** `.\.venv\Scripts\Activate.ps1`

**Need more help?**
- See detailed Polish documentation above
- Check [QUICK_START.md](QUICK_START.md) for beginner-friendly guide
- Visit [Issues](https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues) on GitHub

For more detailed instructions, see the Polish sections above or `doc/README.md`.
