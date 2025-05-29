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

# Ustawienia Whisper
WHISPER_LANGUAGE = "Polish"  # Język transkrypcji (np. "Polish", "English")
WHISPER_MODEL = "turbo"     # Model Faster Whisper (np. "large-v3", "medium", "small", "base", "tiny", "turbo")

# --- Ustawienia Diaryzacji Mówców ---
ENABLE_SPEAKER_DIARIZATION = False  # Ustaw na True, aby włączyć diaryzację mówców
                                   # W GUI: można to zmienić w zakładce Konfiguracja.
                                   # W CLI: można również nadpisać z linii komend: --diarize lub --no-diarize

# Metoda diaryzacji używana przez Faster Whisper.
# Dostępne opcje to np. "pyannote_v3.0", "pyannote_v3.1", "reverb_v1", "reverb_v2".
# "pyannote_v3.1" jest często dobrym wyborem. Szczegóły w dokumentacji Faster Whisper.
# ([https://github.com/Purfview/whisper-standalone-win](https://github.com/Purfview/whisper-standalone-win) -> --diarize)
DIARIZE_METHOD = "pyannote_v3.1"

# Prefiks używany do oznaczania mówców w transkrypcji, np. "MÓWCA_01", "SPEAKER_A".
# Faster Whisper automatycznie doda numer (np. _01, _02).
DIARIZE_SPEAKER_PREFIX = "MÓWCA"

# --- Ustawienia Podsumowania ---
SUMMARY_PROVIDER = "ollama" # Dostawca podsumowania: "ollama" (lokalnie) lub "google" (Google Gemini API)
SUMMARY_LANGUAGE = "Polish" # Język, w którym ma być wygenerowane podsumowanie (np. "Polish", "English")

# Ustawienia Ollama (jeśli SUMMARY_PROVIDER="ollama")
OLLAMA_MODEL = "gemma3:4b"  # Model językowy Ollama do podsumowań

# Ustawienia Google Gemini API (jeśli SUMMARY_PROVIDER="google")
GOOGLE_API_KEY = ""  # Wymagany, jeśli SUMMARY_PROVIDER="google". Wklej tutaj swój klucz API.
GOOGLE_GEMINI_MODEL = "gemini-1.5-flash-latest" # Model Google Gemini do podsumowań

# Prompt dla modelu językowego (Ollama/Google).
# To jest główna część instrukcji, np. "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:"
# Skrypt automatycznie doda instrukcję językową i tekst transkrypcji.
LLM_PROMPT = "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:"

# Ustawienia Ogólne Skryptu
TRANSCRIPTION_FORMAT = "txt"  # Format pliku transkrypcji (używany wewnętrznie przez skrypt CLI)
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"  # Tymczasowa nazwa pliku dla pobranego audio

# --- End Configuration ---