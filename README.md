# pogadane
Aplikacja do generowania streszczeń z nagrań audio (np. spotkań Teams, podcastów) lub filmów na YouTube. Działa lokalnie (offline, poza pobieraniem z YouTube), co zapewnia bezpieczeństwo danych. Umożliwia szybkie uzyskanie najważniejszych informacji z długich materiałów.

**Instrukcja Uruchomienia Skryptu (Wersja Alpha v0.1.3+)** 

Poniższe kroki opisują proces instalacji niezbędnych komponentów oraz uruchomienia głównego skryptu `transcribe_summarize_working.py` w środowisku Windows.

**Wymagania Wstępne:**

* System operacyjny Windows.
* Połączenie z Internetem (do pobrania oprogramowania i opcjonalnie materiałów z YouTube).
* Uprawnienia administratora mogą być wymagane do instalacji niektórych programów.
* Narzędzie do dekompresji archiwów `.7z` (np. [7-Zip](https://www.7-zip.org/)).

**Konfiguracja (Opcjonalnie)**

Na początku skryptu `transcribe_summarize_working.py` znajdują się stałe konfiguracyjne, które można modyfikować:

* `FASTER_WHISPER_EXE`: Ścieżka do `faster-whisper-xxl.exe` (jeśli nie jest w tym samym katalogu co skrypt).
* `YT_DLP_EXE`: Ścieżka do `yt-dlp.exe` (jeśli nie jest w tym samym katalogu co skrypt).
* `WHISPER_LANGUAGE`: Język transkrypcji (domyślnie "Polish").
* `WHISPER_MODEL`: Model Faster Whisper (domyślnie "turbo"). Można zmienić na inne dostępne modele, np. "large-v3".
* `OLLAMA_MODEL`: Model językowy Ollama do podsumowań (domyślnie "gemma3:4b").
* `LLM_PROMPT`: Szablon promptu używany do generowania podsumowania przez Ollama. **Musi zawierać placeholder `{text}`**, który zostanie zastąpiony przez transkrypcję. Domyślnie: `"Streść poniższy tekst po polsku, skupiając się na kluczowych wnioskach i decyzjach:\n\n{text}"`.
* `DOWNLOADED_AUDIO_FILENAME`: Nazwa tymczasowego pliku audio pobieranego z YouTube.

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

1.  **Pobierz Faster-Whisper:** Przejdź do repozytorium GitHub Purfview/whisper-standalone-win w sekcji Releases ([Release Faster-Whisper-XXL r245.4 · Purfview/whisper-standalone-win](https://github.com/Purfview/whisper-standalone-win/releases/tag/Faster-Whisper-XXL)). Znajdź wersję `Faster-Whisper-XXL r245.4` i pobierz archiwum dla Windows: `Faster-Whisper-XXL_r245.4_windows.7z` (rozmiar ok. 1.33 GB).
2.  **Rozpakuj Archiwum:** Użyj narzędzia typu 7-Zip, aby wypakować zawartość pobranego archiwum `Faster-Whisper-XXL_r245.4_windows.7z` do wybranej przez siebie lokalizacji (np. `C:\%userprofile%\Downloads\pogadane`). W wyniku powstanie folder, np. `C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows`.
3.  **Zlokalizuj Katalog Główny Faster-Whisper:** Wewnątrz rozpakowanego folderu znajduje się podkatalog `\Faster-Whisper-XXL` zawierający plik wykonywalny `faster-whisper-xxl.exe` (np. `C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL`). **Zapamiętaj lub skopiuj pełną ścieżkę do tego katalogu.** Będzie on głównym katalogiem roboczym dla skryptu.

**Krok 3: Pobranie yt-dlp (do obsługi YouTube)**

1.  **Pobierz yt-dlp:** Przejdź na stronę najnowszych wydań projektu yt-dlp na GitHub: [https://github.com/yt-dlp/yt-dlp/releases/latest](https://github.com/yt-dlp/yt-dlp/releases/latest).
2.  **Pobierz Plik:** Znajdź i pobierz plik `yt-dlp.exe`.
3.  **Umieść Plik:** Skopiuj pobrany plik `yt-dlp.exe` **dokładnie do tego samego katalogu**, w którym znajduje się plik `faster-whisper-xxl.exe` (czyli do katalogu zlokalizowanego w Kroku 2, punkcie 3, np. `C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL`).

**Krok 4: Instalacja Ollama i Pobranie Modelu Językowego**

1.  **Pobierz Ollama:** Przejdź na oficjalną stronę Ollama ([https://ollama.com/](https://ollama.com/)) i kliknij przycisk "Download", a następnie wybierz wersję dla Windows.
2.  **Zainstaluj Ollama:** Uruchom pobrany instalator i postępuj zgodnie z instrukcjami. Ollama zazwyczaj instaluje się jako usługa działająca w tle.
3.  **Pobierz Model Gemma:** Po instalacji otwórz terminal PowerShell i wykonaj polecenie, aby pobrać model językowy `gemma3:4b`, który jest domyślnie używany w skrypcie (`OLLAMA_MODEL`):
    ```powershell
    ollama pull gemma3:4b
    ```
    Poczekaj na zakończenie pobierania modelu.
4.  **Sprawdź Działanie Ollama:** Upewnij się, że Ollama działa w tle (zazwyczaj widoczna jest ikona w zasobniku systemowym). Możesz też wpisać w PowerShell `ollama list`, aby zobaczyć pobrane modele.

**Krok 5: Przygotowanie i Umieszczenie Głównego Skryptu**

1.  **Pobierz/Skopiuj Skrypt:** Upewnij się, że masz najnowszą wersję głównego pliku skryptu: `transcribe_summarize_working.py`.
2.  **Umieść Skrypt:** Skopiuj plik `transcribe_summarize_working.py` **dokładnie do tego samego katalogu**, w którym znajdują się pliki `faster-whisper-xxl.exe` oraz `yt-dlp.exe` (czyli do katalogu zlokalizowanego w Kroku 2, punkcie 3, np. `C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL`). Jest to kluczowe, aby skrypt mógł znaleźć pliki `.exe` bez modyfikacji jego wewnętrznej konfiguracji.

**Krok 6: Uruchomienie Skryptu**

1.  **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell. Użyj polecenia `cd` (change directory), aby przejść do katalogu, w którym umieściłeś skrypt `transcribe_summarize_working.py` oraz pliki `faster-whisper-xxl.exe` i `yt-dlp.exe`. Przykład:
    ```powershell
    cd "C:\%userprofile%\Downloads\pogadane\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL"
    ```
    *Pamiętaj, aby użyć ścieżki ustalonej w Kroku 2, punkcie 3.*
2.  **Przygotuj Źródło Wejściowe:**
    * **Plik Lokalny:** Upewnij się, że plik audio, który chcesz przetworzyć (np. `spotkanie.mp3`), znajduje się w znanej lokalizacji (np. na Pulpicie: `C:\Users\TwojaNazwaUzytkownika\Desktop\spotkanie.mp3`).
    * **URL YouTube:** Skopiuj adres URL filmu z YouTube, który chcesz przetworzyć.
3.  **Wykonaj Polecenie Uruchomienia Skryptu:** W terminalu PowerShell wpisz polecenie `python`, nazwę skryptu (`transcribe_summarize_working.py`), ścieżkę do pliku audio LUB URL YouTube (najlepiej w cudzysłowach, jeśli zawiera spacje lub znaki specjalne) oraz opcjonalnie flagę `-o` ze ścieżką do pliku wyjściowego dla podsumowania (również w cudzysłowach).

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
    python transcribe_summarize_working.py "[https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=)..." -o "C:\Users\Moje\Dokumenty\podsumowanie_wykladu.txt"
    ```

    *Zastąp przykładowe ścieżki i URL odpowiednimi wartościami dla Twojego systemu i potrzeb.*

4.  **Monitoruj Proces:** Skrypt rozpocznie działanie. W terminalu pojawią się komunikaty informujące o postępie (pobieranie z YouTube, jeśli dotyczy, transkrypcja, podsumowanie). Poczekaj na zakończenie procesu. Podsumowanie zostanie zapisane w pliku podanym po fladze `-o`. Jeśli flaga `-o` nie zostanie użyta, podsumowanie zostanie tylko wyświetlone w terminalu wraz ze wskazówką, jak je zapisać.

**Poprzednie Wersje**

Historyczne wersje skryptu (np. `transcribe_summarize_working_0.1.py`, `transcribe_summarize_working_0.1.1.py`) są archiwizowane w katalogu `previous_versions` w repozytorium projektu.