# config.py
# Plik konfiguracyjny dla skryptu transcribe_summarize_working.py
# oraz Pogadane GUI. Zmiany w GUI są zapisywane tutaj.

# --- Configuration ---

# Ścieżki do plików wykonywalnych
# Opcja 1: Załóż, że pliki wykonywalne są w bieżącym katalogu lub w PATH
FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
YT_DLP_EXE = "yt-dlp.exe"
# Opcja 2: Podaj pełną ścieżkę, jeśli jest to potrzebne (użyj r"..." dla ścieżek Windows)
# FASTER_WHISPER_EXE = r"C:\sciezka\do\twojego\faster-whisper-xxl.exe"
# YT_DLP_EXE = r"C:\sciezka\do\twojego\yt-dlp.exe"

# --- Ustawienia Transkrypcji ---
TRANSCRIPTION_PROVIDER = "faster-whisper" # Dostawca transkrypcji: "faster-whisper" (zewnętrzny exe, lepsza jakość) lub "whisper" (Python, lekki)
# Ustawienia Whisper
WHISPER_LANGUAGE = "Polish"  # Język transkrypcji (np. "Polish", "English")
WHISPER_MODEL = "turbo"     # Model Faster Whisper (np. "large-v3", "medium", "small", "base", "tiny", "turbo")
# Model dla Whisper (Python): "tiny", "base", "small", "medium", "large" (jeśli TRANSCRIPTION_PROVIDER="whisper")
WHISPER_DEVICE = "auto"     # Urządzenie dla Whisper (Python): "auto" (automatyczny wybór GPU/CPU), "cpu", "cuda"

# --- Ustawienia Diaryzacji Mówców ---
ENABLE_SPEAKER_DIARIZATION = False  # Ustaw na True, aby włączyć diaryzację mówców
DIARIZE_METHOD = "pyannote_v3.1"    # Metoda diaryzacji (np. "pyannote_v3.0", "pyannote_v3.1")
DIARIZE_SPEAKER_PREFIX = "MÓWCA"    # Prefiks dla mówców (np. "MÓWCA", "SPEAKER")

# --- Ustawienia Podsumowania ---
SUMMARY_PROVIDER = "ollama" # Dostawca podsumowania: "ollama" (lokalnie z Ollama), "google" (Google Gemini API), lub "transformers" (lokalnie bez Ollama)
SUMMARY_LANGUAGE = "Polish" # Język, w którym ma być wygenerowane podsumowanie (np. "Polish", "English")

# --- Szablony Promptów LLM ---
# Klucze to nazwy wyświetlane w GUI. Wartości to rdzenie promptów.
# Skrypt automatycznie doda instrukcję językową i tekst transkrypcji.
LLM_PROMPT_TEMPLATES = {
    "Standardowy": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:",
    "Elementy Akcji": "Przeanalizuj poniższy tekst i wypisz wyłącznie listę zadań do wykonania (action items), przypisanych osób (jeśli wspomniano) i terminów (jeśli wspomniano) w formie punktów.",
    "Główne Tematy": "Wylistuj główne tematy poruszone w poniższej dyskusji.",
    "Kluczowe Pytania": "Na podstawie poniższej dyskusji, sformułuj listę kluczowych pytań, które pozostały bez odpowiedzi lub wymagają dalszej analizy.",
    "ELI5": "Wyjaśnij główne tezy i wnioski z poniższego tekstu w maksymalnie prosty sposób, unikając skomplikowanego słownictwa."
}
# Nazwa szablonu promptu do użycia. Jeśli pusta lub nie ma w LLM_PROMPT_TEMPLATES, użyty zostanie LLM_PROMPT.
# W GUI odpowiada to wyborowi w Combobox.
LLM_PROMPT_TEMPLATE_NAME = "Standardowy"

# Prompt niestandardowy (fallback lub gdy wybrany w GUI jako "(Własny prompt poniżej)")
# To jest główna część instrukcji, np. "Streść poniższy tekst..."
# Skrypt automatycznie doda instrukcję językową i tekst transkrypcji.
LLM_PROMPT = "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:"

# Ustawienia Ollama (jeśli SUMMARY_PROVIDER="ollama")
OLLAMA_MODEL = "gemma3:4b"  # Model językowy Ollama do podsumowań

# Ustawienia Google Gemini API (jeśli SUMMARY_PROVIDER="google")
GOOGLE_API_KEY = ""  # Wymagany, jeśli SUMMARY_PROVIDER="google". Wklej tutaj swój klucz API.
GOOGLE_GEMINI_MODEL = "gemini-1.5-flash-latest" # Model Google Gemini do podsumowań

# Ustawienia Transformers (jeśli SUMMARY_PROVIDER="transformers")
# Transformers to lekkie modele AI, które działają lokalnie bez Ollama
# Wymagają instalacji: pip install transformers torch
TRANSFORMERS_MODEL = "facebook/bart-large-cnn" # Domyślny model (dobra jakość, ~1.6GB)
# Alternatywy:
#   "sshleifer/distilbart-cnn-12-6"  - Szybszy, mniejszy (~500MB)
#   "google/flan-t5-base"            - Uniwersalny (~900MB)
#   "google/flan-t5-small"           - Bardzo szybki, podstawowa jakość (~300MB)
TRANSFORMERS_DEVICE = "auto" # Urządzenie: "auto" (automatyczny wybór GPU/CPU), "cpu", "cuda"

# Ustawienia Ogólne Skryptu
TRANSCRIPTION_FORMAT = "txt"  # Format pliku transkrypcji (używany wewnętrznie przez skrypt CLI)
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"  # Bazowa nazwa pliku dla pobranego audio (może być modyfikowana przez skrypt dla unikalności)
DEBUG_MODE = False # Ustaw na True, aby włączyć szczegółowe logowanie komend i ich wyników (stdout/stderr)

# --- End Configuration ---