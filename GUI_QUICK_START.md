# Pogadane GUI - Quick Start Guide

## Running the Application

```bash
# From project root
python -m src.pogadane.gui

# Or with Flet CLI
flet run src/pogadane/gui.py
```

## Application Structure

### Main Window Layout

```
┌─────────────────────────────────────────────────┐
│  🎙️ Pogadane v1.0.0        [⚙️] [🌙/☀️]       │  <- App Bar
├─────────────────────────────────────────────────┤
│  📥 Wejście  │  📊 Wyniki  │  🎵 Wizualizacja  │  <- Tabs
├─────────────────────────────────────────────────┤
│                                                 │
│  [Tab Content Area]                             │
│                                                 │
│                                                 │
├─────────────────────────────────────────────────┤
│  Status: Ready  |  Progress: 0%                 │  <- Status Bar
└─────────────────────────────────────────────────┘
```

## Tab Guide

### 📥 Wejście (Input)
**Purpose:** Add files/URLs and start batch processing

**Components:**
- **Input Field**: Multi-line text area for file paths or URLs
  - Separate each source with a new line
  - Supports: Local files, YouTube URLs, audio files
  
- **File Picker**: Browse button to select files
  
- **Queue Display**: Shows all files to be processed (ListView)
  - Status indicators: ⏳ Pending, 🔄 Processing, ✅ Completed, ❌ Error
  
- **Action Buttons**:
  - `+ Dodaj plik` - Add file via file picker
  - `🚀 Rozpocznij przetwarzanie` - Start batch processing
  
- **Progress Section**:
  - Progress bar with percentage
  - Status text (current operation)
  
- **Console Output**:
  - Real-time processing logs
  - Clear button with animation
  - Save log button

### 📊 Wyniki (Results)
**Purpose:** View transcriptions and summaries

**Components:**
- **File Selector**: Dropdown to choose processed file
  
- **Results Display**:
  - Left panel: Full transcription (scrollable)
  - Right panel: Summary (scrollable)
  
- **Export Button**: Save all results to file

### 🎵 Wizualizacja (Visualization)
**Purpose:** View audio waveform and topic timeline

**Components:**
- **Waveform Display**:
  - 100-bar visualization
  - Hover tooltips with amplitude values
  - Click to seek audio position
  
- **Topic Timeline**:
  - Color-coded topic segments
  - Timestamp markers
  - Hover effects
  - Click to play from topic start
  
- **Playback Controls**:
  - Play/Pause button
  - Seek slider
  - Time display (current / total)
  - Volume control

**Note:** Visualization auto-generates when you select a file in the Results tab

## Settings Dialog (⚙️)

Access via gear icon in app bar.

**Sections:**

### Ogólne (General)
- Language selection
- Theme preference
- Auto-save settings

### Transkrypcja (Transcription)
- Model selection (faster-whisper variants)
- Language detection
- Quality settings
- Batch size

### Podsumowanie (Summary)
- LLM provider (Ollama, OpenAI, Anthropic)
- Model selection
- Custom prompts
- Temperature/creativity settings

### Ścieżki (Paths)
- Output directory
- Temporary files location
- Log file location

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file picker |
| `Ctrl+S` | Save console log |
| `Ctrl+,` | Open settings |
| `Ctrl+Q` | Clear console |
| `Ctrl+R` | Start/resume processing |
| `Space` | Play/Pause (in visualization) |
| `F11` | Toggle fullscreen |

## Processing Workflow

### Standard Flow
1. **Add Sources** → Enter file paths or URLs in input field
2. **Review Queue** → Check files to be processed
3. **Start Processing** → Click "Rozpocznij przetwarzanie"
4. **Monitor Progress** → Watch console output and progress bar
5. **View Results** → Switch to "Wyniki" tab, select file
6. **Visualize Audio** → Switch to "Wizualizacja" tab (auto-generated)

### Behind the Scenes
```
Input → Queue → transcribe_summarize_working.py → Extract Results → Display
         ↓                ↓                              ↓
      ListView      Console Output                ResultsManager
```

## Message Queue Protocol

The application uses a queue-based system for thread-safe UI updates:

```python
# Message types
("log", text, "", "")                          # Console output
("error", message, "", "")                     # Error message
("update_status", item_id, status, "")         # Queue status update
("result", source, transcription, summary)     # Processing complete
("finished_all", "", "", "")                   # All files done
```

## Design Tokens Reference

### Spacing Scale (8px base unit)
- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `xxl`: 48px

### Border Radius (M3 Expressive)
- `sm`: 8px
- `md`: 12px
- `lg`: 16px
- `xl`: 20px
- `xxl`: 28px

### Typography Roles
- **Display Large**: 57px / 64px
- **Headline Large**: 32px / 40px
- **Title Large**: 22px / 28px
- **Body Large**: 16px / 24px
- **Label Large**: 14px / 20px

### Brand Colors
- **Primary**: Blue (#2563EB)
- **Secondary**: Purple (#7C3AED)
- **Tertiary**: Green (#34D399)

## Troubleshooting

### Application Won't Start
```bash
# Check Python version (requires 3.8+)
python --version

# Install/update Flet
pip install --upgrade flet

# Run with debug output
python -m src.pogadane.gui --debug
```

### Processing Errors
- Check console output for detailed error messages
- Verify file paths are correct
- Ensure external tools are installed (faster-whisper-xxl, ollama, yt-dlp)
- Check configuration in settings

### Visualization Not Showing
- Ensure file was successfully processed
- Check if audio file is WAV format (other formats may not visualize)
- Select file in Results tab first

### Queue Not Updating
- Backend processing is asynchronous
- Wait for "finished_all" message
- Check console for errors

## Advanced Usage

### Custom Configuration
```python
# Edit .config/config.py for persistent settings
DEFAULT_CONFIG = {
    "transcription_model": "large-v3",
    "summarization_provider": "ollama",
    "output_directory": "output",
    # ... more settings
}
```

### Batch Processing Multiple Files
```
# Input field format (one per line)
C:\audio\file1.wav
C:\audio\file2.wav
https://youtube.com/watch?v=xyz
```

### Export All Results
1. Process files
2. Go to "Wyniki" tab
3. Click "Eksportuj wszystkie wyniki"
4. Choose save location

## API Reference (For Developers)

### Main Class: PogadaneApp

**Key Methods:**
```python
start_batch_processing(e)                    # Start processing
_execute_batch_processing_logic(sources)     # Backend worker
_poll_output_queue_for_batch()               # UI updater
display_selected_result(e)                   # Show results
generate_visualization(e)                    # Create audio viz
analyze_audio_file(path)                     # Extract waveform
parse_transcription_topics(trans, summ)      # Extract topics
```

**Key Properties:**
```python
self.results_manager                         # ResultsManager instance
self.output_queue                            # Queue for thread communication
self.config_manager                          # ConfigManager instance
self.base_path                               # Path to project root
```

## Support

For issues, feature requests, or contributions:
- Documentation: `doc/` directory
- Design system: `M3_EXPRESSIVE_DESIGN_SYSTEM.md`
- Consolidation notes: `CONSOLIDATION_SUMMARY.md`
