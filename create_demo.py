"""
Script to Generate demo_ui.py from gui_flet.py
===============================================

This script creates demo_ui.py - a standalone demo version of Pogadane
that has the identical UI to the real application but with all backend
processing replaced by realistic simulations.

Usage:
    python create_demo.py

Output:
    - demo_ui.py: Standalone demo with mocked dependencies

The demo:
- Uses ONLY flet as a dependency (~50MB)
- Has identical UI to src/pogadane/gui_flet.py
- Simulates realistic processing (5-15 seconds per file)
- Returns pre-written demo transcription and summary
- Does NOT actually transcribe or use AI models
"""

import re

# Read the original GUI file
with open('src/pogadane/gui_flet.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace imports with mocks
content = re.sub(
    r'from \.constants import.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n\)',
    '''# Mock constants
APP_VERSION = "1.0.0-demo"
CUSTOM_PROMPT_OPTION_TEXT = "Custom Prompt"
FILE_STATUS_PENDING = "pending"
FILE_STATUS_PROCESSING = "processing"
FILE_STATUS_COMPLETED = "completed"
FILE_STATUS_ERROR = "error"
DEFAULT_CONFIG = {}''',
    content,
    flags=re.DOTALL
)

content = content.replace('from .text_utils import strip_ansi, extract_transcription_and_summary', '''# Mock text utils
def strip_ansi(text):
    return re.sub(r'\\x1b\\[[0-9;]*m', '', text)

def extract_transcription_and_summary(text):
    return "Demo transcription", "Demo summary"''')

content = content.replace('from .config_loader import ConfigManager', '''# Mock ConfigManager
class MockConfig:
    TRANSCRIPTION_PROVIDER = "faster-whisper"
    WHISPER_MODEL = "base"
    WHISPER_LANGUAGE = "pl"
    ENABLE_SPEAKER_DIARIZATION = True
    SUMMARY_PROVIDER = "gguf"
    GGUF_MODEL_PATH = "dep/models/gemma-3-4b-it-Q4_K_M.gguf"
    SUMMARY_LANGUAGE = "Polish"
    OUTPUT_DIR = "output"
    
class ConfigManager:
    def __init__(self):
        self.config = MockConfig()
    def initialize(self):
        pass
    def save_config(self):
        pass''')

content = content.replace('from .gui_utils import ResultsManager', '''# Mock ResultsManager
class ResultsManager:
    def __init__(self):
        self.results = []
    def add_result(self, *args, **kwargs):
        pass
    def get_all_results(self):
        return []
    def get_result(self, file_path):
        return None
    def clear_results(self):
        pass''')

content = content.replace('from .backend import PogadaneBackend, ProgressUpdate, ProcessingStage', '''# Mock Backend
class ProcessingStage:
    INITIALIZING = "initializing"
    DOWNLOADING = "downloading"
    COPYING = "copying"
    CLEANING = "cleaning"
    TRANSCRIBING = "transcribing"
    SUMMARIZING = "summarizing"
    COMPLETED = "completed"
    ERROR = "error"

class ProgressUpdate:
    def __init__(self, stage, progress, message):
        self.stage = stage
        self.progress = progress
        self.message = message

class PogadaneBackend:
    def __init__(self, config):
        self.config = config
    def process_file(self, file_path, progress_callback=None):
        import time
        import random
        from pathlib import Path
        
        filename = Path(file_path).name
        is_youtube = file_path.startswith('http')
        
        # Simulate realistic processing with detailed progress
        if progress_callback:
            # Initialization
            progress_callback(ProgressUpdate(ProcessingStage.INITIALIZING, 2, "🔧 Initializing processing pipeline..."))
            time.sleep(0.3)
            
            # Download or copy stage
            if is_youtube:
                progress_callback(ProgressUpdate(ProcessingStage.DOWNLOADING, 5, f"📥 Downloading from YouTube..."))
                time.sleep(0.4)
                for i in range(5, 16, 2):
                    progress_callback(ProgressUpdate(ProcessingStage.DOWNLOADING, i, f"📥 Downloading... {i}%"))
                    time.sleep(0.2)
            else:
                progress_callback(ProgressUpdate(ProcessingStage.COPYING, 10, f"📋 Preparing {filename}..."))
                time.sleep(0.3)
            
            # Transcription stage - simulate realistic whisper processing
            progress_callback(ProgressUpdate(ProcessingStage.TRANSCRIBING, 18, "🎤 Loading Whisper model..."))
            time.sleep(0.4)
            progress_callback(ProgressUpdate(ProcessingStage.TRANSCRIBING, 22, "🎤 Detecting audio parameters..."))
            time.sleep(0.3)
            
            # Simulate transcription progress
            for i in range(25, 61, 5):
                msg = f"🎤 Transcribing audio... {i-20}% complete"
                if i > 40:
                    msg = f"🎤 Transcribing (speaker diarization)... {i-20}%"
                progress_callback(ProgressUpdate(ProcessingStage.TRANSCRIBING, i, msg))
                time.sleep(random.uniform(0.3, 0.5))
            
            # Summarization stage - simulate AI processing
            progress_callback(ProgressUpdate(ProcessingStage.SUMMARIZING, 65, "🤖 Loading AI model..."))
            time.sleep(0.4)
            progress_callback(ProgressUpdate(ProcessingStage.SUMMARIZING, 70, "🤖 Analyzing transcription..."))
            time.sleep(0.4)
            
            # Simulate AI thinking/generation
            for i in range(75, 96, 5):
                msg = f"🤖 Generating summary... {i-70}%"
                progress_callback(ProgressUpdate(ProcessingStage.SUMMARIZING, i, msg))
                time.sleep(random.uniform(0.3, 0.5))
            
            # Final stage
            progress_callback(ProgressUpdate(ProcessingStage.SUMMARIZING, 98, "💾 Saving results..."))
            time.sleep(0.2)
            progress_callback(ProgressUpdate(ProcessingStage.COMPLETED, 100, "✅ Processing complete!"))
            time.sleep(0.1)
        
        # Generate realistic demo content
        demo_transcription = """[Speaker 1 - 00:00:00]
Witam wszystkich w dzisiejszym nagraniu. Dzisiaj będziemy omawiać bardzo ważny temat...

[Speaker 2 - 00:00:15]
Dziękuję za wprowadzenie. To rzeczywiście fascynujący temat, który wymaga dokładnej analizy.

[Speaker 1 - 00:00:30]
Dokładnie tak. Zacznijmy od podstaw i przejdźmy przez kluczowe punkty...

[DEMO MODE - This is simulated transcription text. In the real application, this would be the actual transcription from Whisper with speaker diarization, timestamps, and full content of the audio file.]
"""

        demo_summary = """📊 PODSUMOWANIE (DEMO)

🎯 Główne tematy:
• Wprowadzenie do omawianego zagadnienia
• Analiza kluczowych aspektów
• Dyskusja nad praktycznymi zastosowaniami
• Wnioski i podsumowanie

💡 Kluczowe wnioski:
1. Temat wymaga szczegółowej analizy
2. Istnieje wiele praktycznych zastosowań
3. Dalsze badania są wskazane

⏱️ Czas trwania: ~5 minut
👥 Liczba mówców: 2

[DEMO MODE - This is simulated AI summary. In the real application, this would be generated by the configured AI provider (GGUF/Ollama/Transformers/Google Gemini) based on the actual transcription content.]
"""
        
        return {
            "success": True,
            "transcription": demo_transcription,
            "summary": demo_summary
        }''')

# Write the demo file
with open('demo_ui.py', 'w', encoding='utf-8') as f:
    f.write('"""\n')
    f.write('Pogadane UI Demo - Identical to Real GUI (No Processing)\n')
    f.write('=' * 60 + '\n')
    f.write('This demo replicates the exact GUI from gui_flet.py but with mocked processing.\n')
    f.write('Dependencies: flet only\n')
    f.write('"""\n\n')
    f.write(content)

# Fix backend initialization to pass config
with open('demo_ui.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'backend = PogadaneBackend()',
    'backend = PogadaneBackend(self.config_module)'
)

with open('demo_ui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ demo_ui.py created successfully!")
print("Run with: python demo_ui.py")
