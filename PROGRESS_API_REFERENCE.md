# Native Python Progress System - Quick Reference

## 🚀 Quick Start

### Basic Usage

```python
from pogadane.backend import PogadaneBackend, ProgressUpdate

def my_callback(update: ProgressUpdate):
    print(f"[{update.progress:.0%}] {update.message}")

backend = PogadaneBackend()
transcription, summary = backend.process_file(
    "audio.mp3",
    progress_callback=my_callback
)
```

## 📊 ProgressUpdate Structure

```python
@dataclass
class ProgressUpdate:
    stage: ProcessingStage        # Current processing stage
    message: str                  # Human-readable message
    progress: float               # 0.0 to 1.0
    details: Optional[Dict]       # Additional context
```

## 🎯 Processing Stages

| Stage | Icon | Description | Progress Range |
|-------|------|-------------|----------------|
| `INITIALIZING` | 🔧 | Setup and validation | 0.0 - 0.1 |
| `DOWNLOADING` | 📥 | YouTube download | 0.1 - 0.3 |
| `COPYING` | 📄 | Local file copy | 0.1 - 0.3 |
| `TRANSCRIBING` | 🎤 | Audio to text | 0.3 - 0.7 |
| `SUMMARIZING` | 🤖 | Text summarization | 0.7 - 0.9 |
| `CLEANING` | 🧹 | Cleanup temp files | 0.9 - 1.0 |
| `COMPLETED` | ✅ | Success | 1.0 |
| `ERROR` | ❌ | Error occurred | 1.0 |

## 💡 Callback Examples

### Simple Console Output
```python
def simple_callback(update: ProgressUpdate):
    print(f"{update.message}")
```

### Detailed Console Output
```python
def detailed_callback(update: ProgressUpdate):
    print(f"[{update.progress:>5.1%}] {update.stage.value}: {update.message}")
    if update.details:
        for key, value in update.details.items():
            print(f"  {key}: {value}")
```

### GUI Integration (Flet)
```python
def gui_callback(update: ProgressUpdate):
    # Update progress bar
    progress_bar.value = update.progress
    
    # Update status text
    status_text.value = update.message
    
    # Update UI
    progress_bar.update()
    status_text.update()
```

### GUI Integration (Tkinter)
```python
def tk_callback(update: ProgressUpdate):
    progress_var.set(update.progress * 100)
    status_var.set(update.message)
    root.update_idletasks()
```

### Queue-Based (Thread-Safe)
```python
import queue

update_queue = queue.Queue()

def queue_callback(update: ProgressUpdate):
    update_queue.put(update)

# In another thread:
while True:
    update = update_queue.get()
    # Process update...
```

### Logging Integration
```python
import logging
logger = logging.getLogger(__name__)

def logging_callback(update: ProgressUpdate):
    log_level = {
        ProcessingStage.ERROR: logging.ERROR,
        ProcessingStage.COMPLETED: logging.INFO,
    }.get(update.stage, logging.DEBUG)
    
    logger.log(log_level, f"{update.stage.value}: {update.message}")
```

### Web API (FastAPI/Flask)
```python
from fastapi import WebSocket

async def websocket_callback(update: ProgressUpdate, websocket: WebSocket):
    await websocket.send_json({
        "stage": update.stage.value,
        "message": update.message,
        "progress": update.progress,
        "details": update.details
    })
```

## 🔍 Accessing Progress Details

```python
def detailed_callback(update: ProgressUpdate):
    if update.stage == ProcessingStage.TRANSCRIBING:
        audio_file = update.details.get("audio_file")
        print(f"Transcribing: {audio_file}")
    
    elif update.stage == ProcessingStage.COMPLETED:
        trans_len = update.details.get("transcription_length", 0)
        summ_len = update.details.get("summary_length", 0)
        print(f"Done! {trans_len} chars → {summ_len} chars")
```

## 🎨 Custom Progress Display

### Progress Bar (Rich)
```python
from rich.progress import Progress

def rich_callback(update: ProgressUpdate, task_id, progress_bar: Progress):
    progress_bar.update(
        task_id,
        completed=update.progress * 100,
        description=f"[{update.stage.value}] {update.message}"
    )
```

### Notification System
```python
def notify_callback(update: ProgressUpdate):
    if update.stage == ProcessingStage.COMPLETED:
        send_notification("Processing Complete!", update.message)
    elif update.stage == ProcessingStage.ERROR:
        send_notification("Error!", update.message, urgency="critical")
```

## 🐛 Error Handling

```python
def safe_callback(update: ProgressUpdate):
    if update.stage == ProcessingStage.ERROR:
        logger.error(f"Processing error: {update.message}")
        if "error" in update.details:
            logger.error(f"Details: {update.details['error']}")
        # Handle error...
    else:
        # Normal processing...
        pass
```

## 📝 Logging Configuration

### Basic Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### File + Console Logging
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pogadane.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

### Custom Logger
```python
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# File handler
fh = logging.FileHandler('my_app.log')
fh.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
```

## 🧪 Testing

### Unit Test Example
```python
import unittest

class TestProgressCallback(unittest.TestCase):
    def test_callback_receives_updates(self):
        updates = []
        
        def callback(update: ProgressUpdate):
            updates.append(update)
        
        backend = PogadaneBackend()
        # Process test file...
        
        self.assertGreater(len(updates), 0)
        self.assertEqual(updates[0].stage, ProcessingStage.INITIALIZING)
        self.assertEqual(updates[-1].stage, ProcessingStage.COMPLETED)
        self.assertEqual(updates[-1].progress, 1.0)
```

### Mock Testing
```python
from unittest.mock import Mock

def test_progress_callback():
    callback = Mock()
    
    backend = PogadaneBackend()
    backend.process_file("test.mp3", callback)
    
    # Verify callback was called
    callback.assert_called()
    
    # Check call count
    assert callback.call_count > 0
    
    # Verify arguments
    first_call = callback.call_args_list[0]
    update = first_call[0][0]
    assert isinstance(update, ProgressUpdate)
```

## 🎓 Best Practices

1. **Keep Callbacks Fast**: Don't block in callbacks
2. **Handle Errors**: Wrap callback logic in try-except
3. **Use Type Hints**: Help IDE with auto-completion
4. **Log Appropriately**: Use logging module, not just print
5. **Thread Safety**: Use queues for cross-thread communication
6. **Test Callbacks**: Write unit tests for your callbacks

## 📚 Additional Resources

- Main documentation: `NATIVE_PYTHON_REFACTORING.md`
- Demo script: `demo_native_progress.py`
- Backend source: `src/pogadane/backend.py`
- GUI example: `src/pogadane/gui_flet.py`

## 🆘 Troubleshooting

### No progress updates?
```python
# Check if callback is None
if callback is None:
    print("Warning: No callback provided!")
```

### Callback not being called?
```python
# Ensure you pass the callback
backend.process_file("audio.mp3", progress_callback=my_callback)
                                # ^^^ Don't forget this!
```

### Type errors?
```python
# Use proper type hints
def my_callback(update: ProgressUpdate) -> None:
    #                      ^^^^^^^^^^^^^ 
    pass
```
