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

# --- NEW: Ustawienia Diaryzacji Mówców ---
ENABLE_SPEAKER_DIARIZATION = True  # Ustaw na True, aby włączyć diaryzację mówców
                                   # Można również nadpisać z linii komend: --diarize lub --no-diarize

# Metoda diaryzacji używana przez Faster Whisper.
# Dostępne opcje to np. "pyannote_v3.0", "pyannote_v3.1", "reverb_v1", "reverb_v2".
# "pyannote_v3.1" jest często dobrym wyborem. Szczegóły w dokumentacji Faster Whisper.
# (https://github.com/Purfview/whisper-standalone-win -> --diarize)
DIARIZE_METHOD = "pyannote_v3.1"

# Prefiks używany do oznaczania mówców w transkrypcji, np. "MÓWCA_01", "SPEAKER_A".
# Faster Whisper automatycznie doda numer (np. _01, _02).
DIARIZE_SPEAKER_PREFIX = "MÓWCA"

# Opcjonalne dodatkowe parametry diaryzacji (jeśli potrzebne, odkomentuj i dostosuj):
# NUM_SPEAKERS = 0  # Dokładna liczba mówców (jeśli znana, 0 = auto-detect)
# MIN_SPEAKERS = 0  # Minimalna liczba mówców (0 = brak)
# MAX_SPEAKERS = 0  # Maksymalna liczba mówców (0 = brak)
# --- END: Ustawienia Diaryzacji Mówców ---


# Ustawienia Ollama
OLLAMA_MODEL = "gemma3:4b"  # Model językowy Ollama do podsumowań

# Prompt dla modelu językowego (Ollama). Musi zawierać placeholder {text}.
LLM_PROMPT = "Streść poniższy tekst po polsku, skupiając się na kluczowych wnioskach i decyzjach:\n\n{text}"

# Ustawienia Ogólne Skryptu
TRANSCRIPTION_FORMAT = "txt"  # Format pliku transkrypcji (używany wewnętrznie)
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"  # Tymczasowa nazwa pliku dla pobranego audio

# --- End Configuration ---