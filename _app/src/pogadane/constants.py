"""
Application constants and configuration values.

This module contains all magic numbers, default values, and constants
used throughout the Pogadane application.
"""

from pathlib import Path

# Application metadata
APP_VERSION = "0.1.8"
APP_NAME = "Pogadane"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEP_DIR = PROJECT_ROOT / "dep"
MODELS_DIR = DEP_DIR / "models"

# Ensure directories exist
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# GUI status messages
FILE_STATUS_PENDING = "⏳ Oczekuje"
FILE_STATUS_PROCESSING = "⚙️ Przetwarzanie..."
FILE_STATUS_COMPLETED = "✅ Ukończono"
FILE_STATUS_ERROR = "❌ Błąd"

# Custom prompt option
CUSTOM_PROMPT_OPTION_TEXT = "(Własny prompt poniżej)"

# Default configuration values
DEFAULT_CONFIG = {
    # Transcription (Faster-Whisper)
    "TRANSCRIPTION_PROVIDER": "faster-whisper",
    "FASTER_WHISPER_DEVICE": "auto",  # "cuda", "cpu", or "auto"
    "FASTER_WHISPER_COMPUTE_TYPE": "auto",  # "float16", "int8", or "auto"
    "FASTER_WHISPER_BATCH_SIZE": 0,  # 0=no batching
    "FASTER_WHISPER_VAD_FILTER": False,
    "WHISPER_LANGUAGE": "Polish",
    "WHISPER_MODEL": "turbo",
    
    # YouTube download
    "YT_DLP_PATH": "yt-dlp",
    
    # Summarization (GGUF)
    "SUMMARY_PROVIDER": "gguf",
    "SUMMARY_LANGUAGE": "Polish",
    "GGUF_MODEL_PATH": str(MODELS_DIR / "gemma-3-4b-it-Q4_K_M.gguf"),
    "GGUF_CONTEXT_SIZE": 4096,
    "GGUF_GPU_LAYERS": 0,  # 0=CPU only
    
    # Prompt templates
    "LLM_PROMPT_TEMPLATES": {
        "Standardowy": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:",
        "Elementy Akcji": "Przeanalizuj poniższy tekst i wypisz wyłącznie listę zadań do wykonania (action items), przypisanych osób (jeśli wspomniano) i terminów (jeśli wspomniano) w formie punktów.",
        "Główne Tematy": "Wylistuj główne tematy poruszone w poniższej dyskusji.",
        "Kluczowe Pytania": "Na podstawie poniższej dyskusji, sformułuj listę kluczowych pytań, które pozostały bez odpowiedzi lub wymagają dalszej analizy.",
        "ELI5": "Wyjaśnij główne tezy i wnioski z poniższego tekstu w maksymalnie prosty sposób, unikając skomplikowanego słownictwa."
    },
    "LLM_PROMPT_TEMPLATE_NAME": "Standardowy",
    "LLM_PROMPT": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:",
    
    # Optional: Ollama
    "OLLAMA_MODEL": "gemma3:4b",
    
    # Optional: Google Gemini
    "GOOGLE_API_KEY": "",
    "GOOGLE_GEMINI_MODEL": "gemini-1.5-flash-latest",
    
    # Other
    "TRANSCRIPTION_FORMAT": "txt",
    "DEBUG_MODE": False,
}

# Font settings
DEFAULT_FONT_SIZE = 10
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 24
FONT_FAMILY_DEFAULT = "Segoe UI Emoji"
FONT_FAMILY_LABEL = "Segoe UI"

# GUI dimensions
DEFAULT_WINDOW_WIDTH = 950
DEFAULT_WINDOW_HEIGHT = 800

# Processing settings
TEMP_AUDIO_FOLDER_NAME = "pogadane_temp_audio"
