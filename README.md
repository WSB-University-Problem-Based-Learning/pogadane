# pogadane
Aplikacja do generowania streszczeń z nagrań audio (np. spotkań Teams, podcastów) lub filmów na YouTube. Działa lokalnie (offline, poza pobieraniem z YouTube), co zapewnia bezpieczeństwo danych. Umożliwia szybkie uzyskanie najważniejszych informacji z długich materiałów.

Projekt zawiera zarówno interfejs linii komend (CLI) `transcribe_summarize_working.py`, jak i interfejs graficzny użytkownika (GUI) `gui.py`.

**Spis Treści**
1.  [Wymagania Wstępne](#wymagania-wstępne)
2.  [Konfiguracja](#konfiguracja)
3.  [Instalacja Komponentów](#instalacja-komponentów)
    * [Krok 1: Instalacja środowiska Python](#krok-1-instalacja-środowiska-python)
    * [Krok 2: Instalacja Faster-Whisper Standalone](#krok-2-instalacja-faster-whisper-standalone)
    * [Krok 3: Pobranie yt-dlp](#krok-3-pobranie-yt-dlp-do-obsługi-youtube)
    * [Krok 4: Instalacja Ollama i Pobranie Modelu Językowego](#krok-4-instalacja-ollama-i-pobranie-modelu-językowego)
    * [Krok 5: Instalacja biblioteki GUI](#krok-5-instalacja-biblioteki-gui-ttkbootstrap)
4.  [Uruchomienie Aplikacji](#uruchomienie-aplikacji)
    * [Uruchomienie Interfejsu Graficznego (GUI) (Zalecane)](#uruchomienie-interfejsu-graficznego-gui-zalecane)
    * [Uruchomienie Skryptu z Linii Komend (CLI)](#uruchomienie-skryptu-z-linii-komend-cli)
5.  [Poprzednie Wersje](#poprzednie-wersje)

---
## Wymagania Wstępne

* System operacyjny Windows.
* Python (zalecany 3.7+).
* Połączenie z Internetem (do pobrania oprogramowania i opcjonalnie materiałów z YouTube).
* Uprawnienia administratora mogą być wymagane do instalacji niektórych programów.
* Narzędzie do dekompresji archiwów `.7z` (np. [7-Zip](https://www.7-zip.org/)).

---
## Konfiguracja

Skrypt `transcribe_summarize_working.py` oraz interfejs `gui.py` zarządzają konfiguracją w następujący sposób:

1.  **Plik `config.py` (Zalecane):** Aplikacja w pierwszej kolejności próbuje załadować konfigurację z pliku `config.py` znajdującego się w tym samym katalogu co skrypty. **Plik `config.py` z domyślnymi ustawieniami jest dołączony do repozytorium.**
    * **Edycja przez GUI:** Możesz wygodnie edytować większość opcji konfiguracyjnych bezpośrednio w zakładce "⚙️ Konfiguracja" w aplikacji GUI. Zmiany są zapisywane do pliku `config.py`.
    * **Edycja Manualna:** Możesz również bezpośrednio edytować plik `config.py` dowolnym edytorem tekstu.
2.  **Konfiguracja Domyślna (Fallback):** Jeśli plik `config.py` nie zostanie znaleziony (np. zostanie przypadkowo usunięty), skrypt CLI wyświetli ostrzeżenie i automatycznie użyje predefiniowanych wartości domyślnych zaszytych w kodzie. GUI również posiada wbudowane wartości domyślne, których użyje w takiej sytuacji.

**Aby dostosować konfigurację, zaleca się użycie zakładki "Konfiguracja" w GUI lub edycję pliku `config.py` znajdującego się w repozytorium.**

Zawartość przykładowego pliku `config.py` (który jest również plikiem domyślnym w repozytorium):
```python
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
WHISPER_LANGUAGE = "Polish"  # Język transkrypcji oraz streszczenia
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

# Ustawienia Ollama
OLLAMA_MODEL = "gemma3:4b"  # Model językowy Ollama do podsumowań

# Prompt dla modelu językowego (Ollama).
# GUI automatycznie dodaje instrukcję językową (np. "From now write only in Polish!") oraz placeholder {text} na końcu.
# Wpisz tutaj główną część polecenia, np. "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:"
LLM_PROMPT = "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:"

# Ustawienia Ogólne Skryptu
TRANSCRIPTION_FORMAT = "txt"  # Format pliku transkrypcji (używany wewnętrznie przez skrypt CLI)
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"  # Tymczasowa nazwa pliku dla pobranego audio

# --- End Configuration ---
```

**Opis opcji konfiguracyjnych (dostępnych w `config.py` oraz w GUI):**

* `FASTER_WHISPER_EXE`: Ścieżka do `faster-whisper-xxl.exe`.
* `YT_DLP_EXE`: Ścieżka do `yt-dlp.exe`.
* `WHISPER_LANGUAGE`: Język transkrypcji i domyślny język streszczenia (domyślnie "Polish").
* `WHISPER_MODEL`: Model Faster Whisper (domyślnie "turbo"). Można zmienić na inne dostępne modele, np. "large-v3".
* `ENABLE_SPEAKER_DIARIZATION`: Wartość logiczna (`True`/`False`) włączająca/wyłączająca diaryzację mówców. Domyślnie `False`.
* `DIARIZE_METHOD`: Metoda diaryzacji używana przez Faster Whisper (np. `"pyannote_v3.1"`).
* `DIARIZE_SPEAKER_PREFIX`: Prefiks używany do oznaczania mówców w wynikowej transkrypcji (np. `"MÓWCA"`).
* `OLLAMA_MODEL`: Model językowy Ollama do podsumowań (domyślnie "gemma3:4b").
* `LLM_PROMPT`: Główna część promptu używanego do generowania podsumowania przez Ollama. GUI automatycznie dołącza instrukcję językową i placeholder `{text}`.
* `DOWNLOADED_AUDIO_FILENAME`: Nazwa tymczasowego pliku audio pobieranego z YouTube.
* `TRANSCRIPTION_FORMAT`: Format pliku wyjściowego transkrypcji używany przez skrypt CLI (domyślnie 'txt'). GUI pozwala zapisywać w różnych formatach.

---
## Instalacja Komponentów

### Krok 1: Instalacja środowiska Python

1.  **Pobierz Instalator Python:** Przejdź na oficjalną stronę Python ([https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)) i pobierz najnowszy stabilny instalator dla systemu Windows (np. "Windows installer (64-bit)").
2.  **Uruchom Instalator:** Otwórz pobrany plik `.exe`.
3.  **Konfiguracja Instalacji:** **Bardzo ważne:** W pierwszym oknie instalatora zaznacz opcję **"Add Python X.Y to PATH"** (gdzie X.Y to numer wersji). Następnie kliknij "Install Now".
4.  **Weryfikacja Instalacji:** Po zakończeniu instalacji otwórz terminal PowerShell (możesz go znaleźć, wpisując "PowerShell" w menu Start) i wpisz polecenie:
    ```powershell
    python --version
    ```
    Jeśli instalacja przebiegła poprawnie, wyświetlona zostanie zainstalowana wersja Pythona.

### Krok 2: Instalacja Faster-Whisper Standalone

1.  **Pobierz Faster-Whisper:** Przejdź do repozytorium GitHub Purfview/whisper-standalone-win w sekcji Releases ([Release Faster-Whisper-XXL r245.4 · Purfview/whisper-standalone-win](https://www.google.com/search?q=https://github.com/Purfview/whisper-standalone-win/releases/tag/Faster-Whisper-XXL)). Znajdź wersję `Faster-Whisper-XXL r245.4` (lub nowszą, która wspiera diaryzację) i pobierz archiwum dla Windows: `Faster-Whisper-XXL_r245.4_windows.7z`.
2.  **Rozpakuj Archiwum:** Użyj narzędzia typu 7-Zip, aby wypakować zawartość pobranego archiwum do wybranej przez siebie lokalizacji (np. `C:\pogadane_narzedzia`). W wyniku powstanie folder, np. `C:\pogadane_narzedzia\Faster-Whisper-XXL_r245.4_windows`.
3.  **Zlokalizuj Katalog Główny Faster-Whisper:** Wewnątrz rozpakowanego folderu znajduje się podkatalog `\Faster-Whisper-XXL` zawierający plik wykonywalny `faster-whisper-xxl.exe`. Skonfiguruj ścieżkę do tego pliku w `config.py` (lub w GUI) albo umieść go w katalogu projektu.

### Krok 3: Pobranie yt-dlp (do obsługi YouTube)

1.  **Pobierz yt-dlp:** Przejdź na stronę najnowszych wydań projektu yt-dlp na GitHub: [https://www.google.com/search?q=https://github.com/yt-dlp/yt-dlp/releases/latest](https://www.google.com/search?q=https://github.com/yt-dlp/yt-dlp/releases/latest).
2.  **Pobierz Plik:** Znajdź i pobierz plik `yt-dlp.exe`.
3.  **Umieść Plik:** Skopiuj pobrany plik `yt-dlp.exe` do katalogu, w którym znajdują się skrypty `gui.py` i `transcribe_summarize_working.py`, lub skonfiguruj ścieżkę w `config.py` (lub w GUI).

### Krok 4: Instalacja Ollama i Pobranie Modelu Językowego

1.  **Pobierz Ollama:** Przejdź na oficjalną stronę Ollama ([https://ollama.com/](https://ollama.com/)) i kliknij przycisk "Download", a następnie wybierz wersję dla Windows.
2.  **Zainstaluj Ollama:** Uruchom pobrany instalator i postępuj zgodnie z instrukcjami.
3.  **Pobierz Model Językowy:** Po instalacji otwórz terminal PowerShell i wykonaj polecenie, aby pobrać model językowy zdefiniowany w `config.py` lub w GUI (domyślnie `gemma3:4b`):
    ```powershell
    ollama pull gemma3:4b
    ```
    (Jeśli zmieniłeś `OLLAMA_MODEL` w konfiguracji, użyj tutaj odpowiedniej nazwy modelu).
4.  **Sprawdź Działanie Ollama:** Upewnij się, że Ollama działa w tle. Możesz wpisać w PowerShell `ollama list`, aby zobaczyć pobrane modele.

### Krok 5: Instalacja biblioteki GUI (ttkbootstrap)
Aby uruchomić interfejs graficzny, potrzebna jest biblioteka `ttkbootstrap`. Zainstaluj ją używając pip:
1.  Otwórz terminal PowerShell.
2.  Wpisz polecenie:
    ```powershell
    pip install ttkbootstrap
    ```
    Poczekaj na zakończenie instalacji.

---
## Uruchomienie Aplikacji

1.  **Pobierz/Skopiuj Skrypty:** Upewnij się, że masz najnowsze wersje plików `gui.py`, `transcribe_summarize_working.py` oraz `config.py` z repozytorium. Umieść je wszystkie w jednym katalogu.
2.  **Dostosuj `config.py` (Opcjonalnie):** Możesz wstępnie dostosować `config.py` lub zrobić to później przez GUI.

### Uruchomienie Interfejsu Graficznego (GUI) (Wersja Alpha v0.1.6+) (Zalecane)

Interfejs graficzny `gui.py` jest zalecanym sposobem korzystania z aplikacji.

1.  **Otwórz Terminal:** Otwórz terminal PowerShell.
2.  **Przejdź do Katalogu Projektu:** Użyj polecenia `cd`, aby przejść do katalogu, w którym umieściłeś pliki `gui.py`, `transcribe_summarize_working.py` i `config.py`.
    ```powershell
    cd "C:\Sciezka\Do\Twojego\Katalogu\Pogadane"
    ```
3.  **Uruchom GUI:** Wpisz polecenie:
    ```powershell
    python gui.py
    ```
4.  **Korzystanie z GUI:**
    * **Dane Wejściowe:** Wprowadź ścieżkę do lokalnego pliku audio lub URL YouTube w polu na górze. Możesz użyć przycisku "📂" do przeglądania plików.
    * **Konfiguracja:** Przejdź do zakładki "⚙️ Konfiguracja", aby dostosować ustawienia (ścieżki do programów, modele, język, prompt itp.). Pamiętaj, aby kliknąć "💾 Zapisz i Zastosuj", aby zmiany zostały zapisane w `config.py` i uwzględnione.
    * **Uruchomienie:** Kliknij przycisk "🚀 Transkrybuj i Streść".
    * **Wyniki:** Postęp i logi będą widoczne w zakładce "🖥️ Konsola". Gotowa transkrypcja pojawi się w "📝 Transkrypcja", a streszczenie w "📌 Streszczenie".
    * **Zapisywanie:** Użyj przycisków "💾 Zapisz" lub "📁 Zapisz Jako..." w odpowiednich zakładkach, aby zapisać log, transkrypcję lub streszczenie.

### Uruchomienie Skryptu z Linii Komend (CLI) (Wersja Alpha v0.1.6+)

Skrypt `transcribe_summarize_working.py` może być również uruchamiany bezpośrednio z linii komend.

1.  **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell. Użyj polecenia `cd` (change directory), aby przejść do katalogu, w którym umieściłeś skrypt `transcribe_summarize_working.py` oraz `config.py`.
2.  **Wykonaj Polecenie Uruchomienia Skryptu:** W terminalu PowerShell wpisz polecenie `python`, nazwę skryptu, ścieżkę do pliku audio LUB URL YouTube, opcjonalnie flagę `--diarize` LUB `--no-diarize` oraz opcjonalnie flagę `-o` ze ścieżką do pliku wyjściowego dla podsumowania.

    **Ogólny wzór:**
    ```powershell
    python transcribe_summarize_working.py "<ścieżka_do_pliku_LUB_URL_YouTube>" [--diarize | --no-diarize] -o "<pełna_ścieżka_do_pliku_z_podsumowaniem.txt>"
    ```
    * Flagi `--diarize` lub `--no-diarize` nadpisują ustawienie `ENABLE_SPEAKER_DIARIZATION` z `config.py`. Jeśli żadna z tych flag nie jest użyta, wartość brana jest z `config.py`.

    **Przykład 1: Użycie pliku lokalnego z włączoną diaryzacją**
    ```powershell
    python transcribe_summarize_working.py "C:\Users\Moje\Desktop\nagranie_spotkania.mp3" --diarize -o "C:\Users\alexk\Desktop\nagranie_spotkania_summary.txt"
    ```
    **Przykład 2: Użycie adresu URL YouTube (ustawienie diaryzacji z `config.py`)**
    ```powershell
    python transcribe_summarize_working.py "[https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)" -o "C:\Users\Moje\Dokumenty\podsumowanie_wykladu.txt"
    ```
3.  **Monitoruj Proces:** Skrypt rozpocznie działanie. W terminalu pojawią się komunikaty informujące o postępie. Podsumowanie zostanie zapisane w pliku podanym po fladze `-o`. Jeśli flaga `-o` nie zostanie użyta, podsumowanie zostanie tylko wyświetlone w terminalu.

---
## Poprzednie Wersje

Historyczne wersje skryptu są archiwizowane w katalogu `previous_versions` w repozytorium projektu.