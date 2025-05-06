# pogadane
Aplikacja do generowania streszczeń z nagrań audio (np. spotkań Teams, podcastów) lub filmów na YouTube. Działa lokalnie (offline, poza pobieraniem z YouTube), co zapewnia bezpieczeństwo danych. Umożliwia szybkie uzyskanie najważniejszych informacji z długich materiałów.

**Instrukcja Uruchomienia Skryptu (Wersja Alpha v0.1.4+)**

Poniższe kroki opisują proces instalacji niezbędnych komponentów oraz uruchomienia głównego skryptu `transcribe_summarize_working.py` w środowisku Windows.

**Wymagania Wstępne:**

* System operacyjny Windows.
* Połączenie z Internetem (do pobrania oprogramowania i opcjonalnie materiałów z YouTube).
* Uprawnienia administratora mogą być wymagane do instalacji niektórych programów.
* Narzędzie do dekompresji archiwów `.7z` (np. [7-Zip](https://www.7-zip.org/)).

**Konfiguracja**

Skrypt `transcribe_summarize_working.py` zarządza konfiguracją w następujący sposób:

1.  **Plik `config.py` (Zalecane):** Skrypt w pierwszej kolejności próbuje załadować konfigurację z pliku `config.py` znajdującego się w tym samym katalogu. **Plik `config.py` z domyślnymi ustawieniami jest dołączony do repozytorium.** Możesz bezpośrednio edytować ten plik, aby dostosować ścieżki do plików wykonywalnych, modele językowe, prompty itp.
2.  **Konfiguracja Domyślna (Fallback):** Jeśli plik `config.py` nie zostanie znaleziony (np. zostanie przypadkowo usunięty), skrypt wyświetli ostrzeżenie i automatycznie użyje predefiniowanych wartości domyślnych, które są zaszyte w kodzie. Pozwala to na podstawowe uruchomienie skryptu nawet bez pliku `config.py`.

**Aby dostosować konfigurację, edytuj plik `config.py` znajdujący się w repozytorium.**

Zawartość przykładowego pliku `config.py` (który jest również plikiem domyślnym w repozytorium):
```python
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
````

**Opis opcji konfiguracyjnych w `config.py` (lub wartości domyślnych w skrypcie):**

  * `FASTER_WHISPER_EXE`: Ścieżka do `faster-whisper-xxl.exe`.
  * `YT_DLP_EXE`: Ścieżka do `yt-dlp.exe`.
  * `WHISPER_LANGUAGE`: Język transkrypcji (domyślnie "Polish").
  * `WHISPER_MODEL`: Model Faster Whisper (domyślnie "turbo"). Można zmienić na inne dostępne modele, np. "large-v3".
  * `OLLAMA_MODEL`: Model językowy Ollama do podsumowań (domyślnie "gemma3:4b").
  * `LLM_PROMPT`: Szablon promptu używany do generowania podsumowania przez Ollama. **Musi zawierać placeholder `{text}`**, który zostanie zastąpiony przez transkrypcję.
  * `DOWNLOADED_AUDIO_FILENAME`: Nazwa tymczasowego pliku audio pobieranego z YouTube.
  * `TRANSCRIPTION_FORMAT`: Format pliku wyjściowego transkrypcji (domyślnie 'txt').

**Krok 1: Instalacja środowiska Python**

1.  **Pobierz Instalator Python:** Przejdź na oficjalną stronę Python ([https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)) i pobierz najnowszy stabilny instalator dla systemu Windows (np. "Windows installer (64-bit)").
2.  **Uruchom Instalator:** Otwórz pobrany plik `.exe`.
3.  **Konfiguracja Instalacji:** **Bardzo ważne:** W pierwszym oknie instalatora zaznacz opcję **"Add Python X.Y to PATH"** (gdzie X.Y to numer wersji). Następnie kliknij "Install Now".
4.  **Weryfikacja Instalacji:** Po zakończeniu instalacji otwórz terminal PowerShell (możesz go znaleźć, wpisując "PowerShell" w menu Start) i wpisz polecenie:
    ```powershell
    python --version
    ```
    Jeśli instalacja przebiegła poprawnie i Python został dodany do PATH, wyświetlona zostanie zainstalowana wersja Pythona.

**Krok 2: Instalacja Faster-Whisper Standalone**

1.  **Pobierz Faster-Whisper:** Przejdź do repozytorium GitHub Purfview/whisper-standalone-win w sekcji Releases ([Release Faster-Whisper-XXL r245.4 · Purfview/whisper-standalone-win](https://www.google.com/search?q=https://github.com/Purfview/whisper-standalone-win/releases/tag/Faster-Whisper-XXL)). Znajdź wersję `Faster-Whisper-XXL r245.4` i pobierz archiwum dla Windows: `Faster-Whisper-XXL_r245.4_windows.7z` (rozmiar ok. 1.33 GB).
2.  **Rozpakuj Archiwum:** Użyj narzędzia typu 7-Zip, aby wypakować zawartość pobranego archiwum `Faster-Whisper-XXL_r245.4_windows.7z` do wybranej przez siebie lokalizacji (np. `C:\%userprofile%\Downloads\pogadane`). W wyniku powstanie folder, np. `C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows`.
3.  **Zlokalizuj Katalog Główny Faster-Whisper:** Wewnątrz rozpakowanego folderu znajduje się podkatalog `\Faster-Whisper-XXL` zawierający plik wykonywalny `faster-whisper-xxl.exe` (np. `C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL`). **Zapamiętaj lub skopiuj pełną ścieżkę do tego katalogu.** Jeśli nie chcesz umieszczać skryptu i `config.py` w tym katalogu, upewnij się, że ścieżka do `faster-whisper-xxl.exe` jest poprawnie ustawiona w `config.py` (lub polegaj na PATH systemowym, jeśli tak skonfigurowałeś).

**Krok 3: Pobranie yt-dlp (do obsługi YouTube)**

1.  **Pobierz yt-dlp:** Przejdź na stronę najnowszych wydań projektu yt-dlp na GitHub: [https://www.google.com/search?q=https://github.com/yt-dlp/yt-dlp/releases/latest](https://www.google.com/search?q=https://github.com/yt-dlp/yt-dlp/releases/latest).
2.  **Pobierz Plik:** Znajdź i pobierz plik `yt-dlp.exe`.
3.  **Umieść Plik:** Skopiuj pobrany plik `yt-dlp.exe` do katalogu, w którym planujesz uruchamiać skrypt `transcribe_summarize_working.py` (lub do lokalizacji wskazanej w `config.py` dla `YT_DLP_EXE`). Jeśli `FASTER_WHISPER_EXE` i `YT_DLP_EXE` w `config.py` (lub w wartościach domyślnych) są ustawione na same nazwy plików (np. `"yt-dlp.exe"`), oznacza to, że skrypt oczekuje ich w tym samym katalogu co on sam, lub w katalogu dodanym do systemowej zmiennej PATH.

**Krok 4: Instalacja Ollama i Pobranie Modelu Językowego**

1.  **Pobierz Ollama:** Przejdź na oficjalną stronę Ollama ([https://ollama.com/](https://ollama.com/)) i kliknij przycisk "Download", a następnie wybierz wersję dla Windows.
2.  **Zainstaluj Ollama:** Uruchom pobrany instalator i postępuj zgodnie z instrukcjami. Ollama zazwyczaj instaluje się jako usługa działająca w tle.
3.  **Pobierz Model Językowy:** Po instalacji otwórz terminal PowerShell i wykonaj polecenie, aby pobrać model językowy zdefiniowany w `config.py` lub w wartościach domyślnych (domyślnie `gemma3:4b`):
    ```powershell
    ollama pull gemma3:4b
    ```
    (Jeśli zmieniłeś `OLLAMA_MODEL` w `config.py`, użyj tutaj odpowiedniej nazwy modelu).
    Poczekaj na zakończenie pobierania modelu.
4.  **Sprawdź Działanie Ollama:** Upewnij się, że Ollama działa w tle (zazwyczaj widoczna jest ikona w zasobniku systemowym). Możesz też wpisać w PowerShell `ollama list`, aby zobaczyć pobrane modele.

**Krok 5: Przygotowanie Głównego Skryptu i Pliku Konfiguracyjnego**

1.  **Pobierz/Skopiuj Skrypty:** Upewnij się, że masz najnowszą wersję głównego pliku skryptu `transcribe_summarize_working.py` oraz pliku `config.py` z repozytorium.
2.  **Umieść Skrypty:** Umieść pliki `transcribe_summarize_working.py` i `config.py` w wybranym przez siebie katalogu roboczym. Dostosuj `config.py` według potrzeb. Upewnij się, że ścieżki do `faster-whisper-xxl.exe` i `yt-dlp.exe` w `config.py` (lub w wartościach domyślnych skryptu) są prawidłowe, lub że te pliki `.exe` znajdują się w tym samym katalogu co skrypty (jeśli używasz tylko nazw plików).

**Krok 6: Uruchomienie Skryptu**

1.  **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell. Użyj polecenia `cd` (change directory), aby przejść do katalogu, w którym umieściłeś skrypt `transcribe_summarize_working.py` oraz `config.py`.
    Przykład:

    ```powershell
    cd "C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL"
    ```

2.  **Przygotuj Źródło Wejściowe:**

      * **Plik Lokalny:** Upewnij się, że plik audio, który chcesz przetworzyć (np. `spotkanie.mp3`), znajduje się w znanej lokalizacji.
      * **URL YouTube:** Skopiuj adres URL filmu z YouTube, który chcesz przetworzyć.

3.  **Wykonaj Polecenie Uruchomienia Skryptu:** W terminalu PowerShell wpisz polecenie `python`, nazwę skryptu (`transcribe_summarize_working.py`), ścieżkę do pliku audio LUB URL YouTube (najlepiej w cudzysłowach) oraz opcjonalnie flagę `-o` ze ścieżką do pliku wyjściowego dla podsumowania.

    **Ogólny wzór:**

    ```powershell
    python transcribe_summarize_working.py "<ścieżka_do_pliku_LUB_URL_YouTube>" -o "<pełna_ścieżka_do_pliku_z_podsumowaniem.txt>"
    ```

    **Przykład 1: Użycie pliku lokalnego**

    ```powershell
    python transcribe_summarize_working.py "C:\Users\Moje\Desktop\nagranie_spotkania.mp3" -o "C:\Users\alexk\Desktop\nagranie_spotkania_summary.txt"
    ```

    **Przykład 2: Użycie adresu URL YouTube**

    ```powershell
    python transcribe_summarize_working.py "[https://www.youtube.com/watch?v=przykladowyURL](https://www.youtube.com/watch?v=przykladowyURL)" -o "C:\Users\Moje\Dokumenty\podsumowanie_wykladu.txt"
    ```

    *Zastąp przykładowe ścieżki i URL odpowiednimi wartościami dla Twojego systemu i potrzeb.*

4.  **Monitoruj Proces:** Skrypt rozpocznie działanie. W terminalu pojawią się komunikaty informujące o postępie. Poczekaj na zakończenie procesu. Podsumowanie zostanie zapisane w pliku podanym po fladze `-o`. Jeśli flaga `-o` nie zostanie użyta, podsumowanie zostanie tylko wyświetlone w terminalu.

**Poprzednie Wersje**

Historyczne wersje skryptu są archiwizowane w katalogu `previous_versions` w repozytorium projektu.