# config.py
# Plik konfiguracyjny dla skryptu transcribe_summarize_working.py

# --- Configuration ---

# Ścieżki do plików wykonywalnych
# Opcja 1: Załóż, że pliki wykonywalne są w bieżącym katalogu lub w PATH
FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
YT_DLP_EXE = "yt-dlp.exe"
# Opcja 2: Podaj pełną ścieżkę, jeśli jest to potrzebne (użyj r"..." dla ścieżek Windows)
# FASTER_WHISPER_EXE = r"C:\sciezka\do\twojego\faster-whisper-xxl.exe"
# YT_DLP_EXE = r"C:\sciezka\do\twojego\yt-dlp.exe"

# Ustawienia Whisper
WHISPER_LANGUAGE = "Polish"  # Język transkrypcji
WHISPER_MODEL = "turbo"     # Model Faster Whisper (np. "large-v3", "medium", "small", "base", "tiny", "turbo")

# Ustawienia Ollama
OLLAMA_MODEL = "gemma3:4b"  # Model językowy Ollama do podsumowań

# Prompt dla modelu językowego (Ollama). Musi zawierać placeholder {text}.
LLM_PROMPT = "Streść poniższy tekst po polsku, skupiając się na kluczowych wnioskach i decyzjach:\n\n{text}"

# Ustawienia Ogólne Skryptu
TRANSCRIPTION_FORMAT = "txt"  # Format pliku transkrypcji (używany wewnętrznie)
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"  # Tymczasowa nazwa pliku dla pobranego audio

# --- End Configuration ---