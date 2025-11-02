"""
Application constants and configuration values.

This module contains all magic numbers, default values, and constants
used throughout the Pogadane application.
"""

# Application metadata
APP_VERSION = "0.1.8"
APP_NAME = "Pogadane"

# File markers for GUI parsing
TRANSCRIPTION_START_MARKER = "--- POCZĄTEK TRANSKRYPCJI ---"
TRANSCRIPTION_END_MARKER = "--- KONIEC TRANSKRYPCJI ---"
SUMMARY_START_MARKER = "--- POCZĄTEK STRESZCZENIA ---"
SUMMARY_END_MARKER = "--- KONIEC STRESZCZENIA ---"

# GUI status messages
FILE_STATUS_PENDING = "⏳ Oczekuje"
FILE_STATUS_PROCESSING = "⚙️ Przetwarzanie..."
FILE_STATUS_COMPLETED = "✅ Ukończono"
FILE_STATUS_ERROR = "❌ Błąd"

# Custom prompt option
CUSTOM_PROMPT_OPTION_TEXT = "(Własny prompt poniżej)"

# Default configuration values
DEFAULT_CONFIG = {
    "FASTER_WHISPER_EXE": "faster-whisper-xxl.exe",
    "YT_DLP_EXE": "yt-dlp.exe",
    "WHISPER_LANGUAGE": "Polish",
    "WHISPER_MODEL": "turbo",
    "ENABLE_SPEAKER_DIARIZATION": False,
    "DIARIZE_METHOD": "pyannote_v3.1",
    "DIARIZE_SPEAKER_PREFIX": "MÓWCA",
    "SUMMARY_PROVIDER": "ollama",
    "SUMMARY_LANGUAGE": "Polish",
    "LLM_PROMPT_TEMPLATES": {
        "Standardowy": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:",
        "Elementy Akcji": "Przeanalizuj poniższy tekst i wypisz wyłącznie listę zadań do wykonania (action items), przypisanych osób (jeśli wspomniano) i terminów (jeśli wspomniano) w formie punktów.",
        "Główne Tematy": "Wylistuj główne tematy poruszone w poniższej dyskusji.",
        "Kluczowe Pytania": "Na podstawie poniższej dyskusji, sformułuj listę kluczowych pytań, które pozostały bez odpowiedzi lub wymagają dalszej analizy.",
        "ELI5": "Wyjaśnij główne tezy i wnioski z poniższego tekstu w maksymalnie prosty sposób, unikając skomplikowanego słownictwa."
    },
    "LLM_PROMPT_TEMPLATE_NAME": "Standardowy",
    "LLM_PROMPT": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:",
    "OLLAMA_MODEL": "gemma3:4b",
    "GOOGLE_API_KEY": "",
    "GOOGLE_GEMINI_MODEL": "gemini-1.5-flash-latest",
    "TRANSCRIPTION_FORMAT": "txt",
    "DOWNLOADED_AUDIO_FILENAME": "downloaded_audio.mp3",
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
