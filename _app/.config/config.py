# config.py
# Configuration file for Pogadane application
# GUI changes are saved here automatically

# --- Configuration (100% pip-based) ---

# --- Ustawienia Transkrypcji (pip: faster-whisper lub openai-whisper) ---
TRANSCRIPTION_PROVIDER = "faster-whisper" # Dostawca: "faster-whisper" (4x szybszy, GPU) lub "whisper" (oryginalny)

# Ustawienia Faster-Whisper (pip install faster-whisper)
FASTER_WHISPER_DEVICE = "auto" # "cuda", "cpu", lub "auto"
FASTER_WHISPER_COMPUTE_TYPE = "auto" # "float16", "int8", "int8_float16", lub "auto"
FASTER_WHISPER_BATCH_SIZE = 0 # 0 = bez batch, >0 dla przyspieszenia
FASTER_WHISPER_VAD_FILTER = False # Voice Activity Detection

# Ustawienia Whisper (wspólne dla obu)
WHISPER_LANGUAGE = "Polish" # Język transkrypcji (np. "Polish", "English")
WHISPER_MODEL = "turbo" # Model: "tiny", "base", "small", "medium", "large", "turbo", "large-v3"

# Ustawienia dla openai-whisper (jeśli TRANSCRIPTION_PROVIDER="whisper")
WHISPER_DEVICE = "auto"     # Urządzenie: "auto", "cpu", "cuda"

# YouTube Downloads (pip: yt-dlp)
YT_DLP_PATH = "yt-dlp" # Komenda lub pełna ścieżka

# --- Ustawienia Podsumowania ---
SUMMARY_PROVIDER = "gguf" # Dostawca: "transformers" (pip, offline), "ollama" (lokalnie, wymaga instalacji), "google" (cloud API), lub "gguf" (llama-cpp, quantized models)
SUMMARY_LANGUAGE = "Polish" # Język podsumowania (uwaga: większość modeli Transformers działa tylko po angielsku)

# --- Szablony Promptów LLM ---
# System Prompt - Definiuje rolę i zachowanie AI
SYSTEM_PROMPT = "You are a helpful AI assistant that creates clear, concise summaries of text content. Focus on key points, decisions, and actionable items."

# User Prompt Template - Szablon z {text} jako placeholder dla transkrypcji
USER_PROMPT_TEMPLATE = "Please summarize the following text in {language}:\n\n{text}"

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
OLLAMA_MODEL = "gemma3:4b" # Model językowy Ollama do podsumowań

# Ustawienia Google Gemini API (jeśli SUMMARY_PROVIDER="google")
GOOGLE_API_KEY = "" # Wymagany, jeśli SUMMARY_PROVIDER="google". Wklej tutaj swój klucz API.
GOOGLE_GEMINI_MODEL = "gemini-1.5-pro" # Model Google Gemini do podsumowań

# Ustawienia Transformers (jeśli SUMMARY_PROVIDER="transformers")
# Transformers to lekkie modele AI, które działają lokalnie bez Ollama
# Wymagają instalacji: pip install transformers torch
TRANSFORMERS_MODEL = "google/gemma-3-4b-it" # Domyślny model (dobra jakość, ~1.6GB)
# Alternatywy:
#   "sshleifer/distilbart-cnn-12-6"  - Szybszy, mniejszy (~500MB)
#   "google/flan-t5-base"            - Uniwersalny (~900MB)
#   "google/flan-t5-small"           - Bardzo szybki, podstawowa jakość (~300MB)
TRANSFORMERS_DEVICE = "auto" # Urządzenie: "auto" (automatyczny wybór GPU/CPU), "cpu", "cuda"

# Ustawienia GGUF / Llama.cpp (jeśli SUMMARY_PROVIDER="gguf")
# GGUF to format skwantyzowanych modeli - mniejsze, szybsze, działają na CPU
# Wymagają instalacji: pip install llama-cpp-python
GGUF_MODEL_PATH = "_app/dep/models/gemma-3-4b-it-Q4_K_M.gguf" # Ścieżka do pliku GGUF
GGUF_N_GPU_LAYERS = 0 # Liczba warstw na GPU (0 = tylko CPU, >0 = użyj GPU dla przyspieszenia)

# Ustawienia Ogólne Skryptu
TRANSCRIPTION_FORMAT = "txt"  # Format pliku transkrypcji (używany wewnętrznie przez skrypt CLI)
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"  # Bazowa nazwa pliku dla pobranego audio (może być modyfikowana przez skrypt dla unikalności)
DEBUG_MODE = False # Ustaw na True, aby włączyć szczegółowe logowanie komend i ich wyników (stdout/stderr)

# --- End Configuration ---