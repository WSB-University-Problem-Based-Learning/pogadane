# pogadane
Aplikacja do generowania streszczeń ze spotkań na Teams lub podcastów. Działa lokalnie (offline), co zapewnia bezpieczeństwo danych. Umożliwia szybkie uzyskanie najważniejszych informacji z długich nagrań.

**Instrukcja Uruchomienia Skryptu (Wersja Alpha v0.1.0)**

Poniższe kroki opisują proces instalacji niezbędnych komponentów oraz uruchomienia skryptu [transcribe\_summarize\_working_0.1.py](https://trello.com/1/cards/680e9725e7a2c73deb932e6e/attachments/680e9748ff33a60390d0556f/download/transcribe_summarize_working_0.1.py "‌") w środowisku Windows.

**Wymagania Wstępne:**

- System operacyjny Windows.
- Połączenie z Internetem do pobrania oprogramowania.
- Uprawnienia administratora mogą być wymagane do instalacji niektórych programów.
- Narzędzie do dekompresji archiwów `.7z` (np. 7-Zip).

**Krok 1: Instalacja środowiska Python**

1. **Pobierz Instalator Python:** Przejdź na oficjalną stronę Python ([https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/ "‌")) i pobierz najnowszy stabilny instalator dla systemu Windows (np. "Windows installer (64-bit)").
2. **Uruchom Instalator:** Otwórz pobrany plik `.exe`.
3. **Konfiguracja Instalacji:** **Bardzo ważne:** W pierwszym oknie instalatora zaznacz opcję **"Add Python X.Y to PATH"** (gdzie X.Y to numer wersji). Następnie kliknij "Install Now".
4. **Weryfikacja Instalacji:** Po zakończeniu instalacji otwórz terminal PowerShell (możesz go znaleźć, wpisując "PowerShell" w menu Start) i wpisz polecenie:
   ```powershell
   python --version
   ```
    Jeśli instalacja przebiegła poprawnie i Python został dodany do PATH, wyświetlona zostanie zainstalowana wersja Pythona.

**Krok 2: Instalacja Faster-Whisper Standalone**

1. **Pobierz Faster-Whisper:** Przejdź do repozytorium GitHub Purfview/whisper-standalone-win w sekcji Releases [Release Faster-Whisper-XXL r245.4 · Purfview/whisper-standalone-win](https://github.com/Purfview/whisper-standalone-win/releases/tag/Faster-Whisper-XXL "‌"). Znajdź wersję `Faster-Whisper-XXL r245.4` i pobierz archiwum dla Windows: `Faster-Whisper-XXL_r245.4_windows.7z` (rozmiar ok. 1.33 GB).
2. **Rozpakuj Archiwum:** Użyj narzędzia typu 7-Zip, aby wypakować zawartość pobranego archiwum `Faster-Whisper-XXL_r245.4_windows.7z` do wybranej przez siebie lokalizacji (np. `C:\%userprofile%\Downloads`). W wyniku powstanie folder, np. `C:\%userprofile%\Downloads\Faster-Whisper-XXL_r245.4_windows`.
3. **Zlokalizuj Katalog Główny Faster-Whisper:** Wewnątrz rozpakowanego folderu znajduje się podkatalog `\Faster-Whisper-XXL` zawierający plik wykonywalny `faster-whisper-xxl.exe`. (np. `C:\%userprofile%\Downloads\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL`). **Zapamiętaj lub skopiuj pełną ścieżkę do tego katalogu.**

**Krok 3: Instalacja Ollama i Pobranie Modelu Językowego**

1. **Pobierz Ollama:** Przejdź na oficjalną stronę Ollama ([https://ollama.com/](https://ollama.com/ "‌")) i kliknij przycisk "Download", a następnie wybierz wersję dla Windows.
2. **Zainstaluj Ollama:** Uruchom pobrany instalator i postępuj zgodnie z instrukcjami. Ollama zazwyczaj instaluje się jako usługa działająca w tle.
3. **Pobierz Model Gemma:** Po instalacji otwórz terminal PowerShell i wykonaj polecenie, aby pobrać model językowy `gemma3:4b`, który jest zdefiniowany w skrypcie (`OLLAMA_MODEL`):
   ```powershell
   ollama pull gemma3:4b
   ```
    Poczekaj na zakończenie pobierania modelu.
4. **Sprawdź Działanie Ollama:** Upewnij się, że Ollama działa w tle (zazwyczaj widoczna jest ikona w zasobniku systemowym). Możesz też wpisać w PowerShell `ollama list`, aby zobaczyć pobrane modele.

**Krok 4: Przygotowanie i Umieszczenie Skryptu Python**

1. **Zapisz Skrypt:** Upewnij się, że masz zapisany plik [transcribe\_summarize\_working_0.1.py](https://trello.com/1/cards/680e9725e7a2c73deb932e6e/attachments/680e9748ff33a60390d0556f/download/transcribe_summarize_working_0.1.py "‌")
2. **Skopiuj Skrypt do Katalogu Faster-Whisper:** Skopiuj plik [transcribe\_summarize\_working_0.1.py](https://trello.com/1/cards/680e9725e7a2c73deb932e6e/attachments/680e9748ff33a60390d0556f/download/transcribe_summarize_working_0.1.py "‌") i wklej go **dokładnie do tego samego katalogu**, w którym znajduje się plik wykonywalny `faster-whisper-xxl.exe` (czyli do katalogu zlokalizowanego w Kroku 2, punkcie 3, np. `C:\%userprofile%\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL`). Jest to kluczowe, aby skrypt mógł znaleźć plik `.exe` bez modyfikacji jego wewnętrznej konfiguracji (`FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"`).

**Krok 5: Uruchomienie Skryptu**

1. **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell. Użyj polecenia `cd` (change directory), aby przejść do katalogu, w którym umieściłeś skrypt [transcribe\_summarize\_working_0.1.py](https://trello.com/1/cards/680e9725e7a2c73deb932e6e/attachments/680e9748ff33a60390d0556f/download/transcribe_summarize_working_0.1.py "‌") oraz gdzie znajduje się `faster-whisper-xxl.exe`. Przykład:
   ```powershell
   cd "C:\Users\alexk\Downloads\Faster-Whisper-XXL_r245.4_windows\Faster-Whisper-XXL"
   ```
   _Pamiętaj, aby użyć ścieżki ustalonej w Kroku 2, punkcie 3. (%userprofile% zmień za ścieżkę swojego użytkownika)_
2. **Przygotuj Plik Audio:** Upewnij się, że plik audio, który chcesz przetworzyć (np. `spotkanie.mp3`), znajduje się w znanej lokalizacji (np. na Pulpicie: `C:\Users\TwojaNazwaUzytkownika\Desktop\spotkanie.mp3`).
3. **Wykonaj Polecenie Uruchomienia Skryptu:** W terminalu PowerShell wpisz polecenie `python`, nazwę skryptu, ścieżkę do pliku audio (najlepiej pełną, w cudzysłowach, jeśli zawiera spacje) oraz opcjonalnie flagę `-o` ze ścieżką do pliku wyjściowego dla podsumowania (również w cudzysłowach).
   **Ogólny wzór:**
   ```powershell
   python transcribe_summarize_working_0.1.py "<pełna_ścieżka_do_pliku_audio>" -o "<pełna_ścieżka_do_pliku_z_podsumowaniem.txt>"
   ```
   **Konkretny przykład użycia:**
   ```powershell
   python transcribe_summarize_working_0.1.py "C:\Users\alexk\Desktop\spotkanie.mp3" -o "C:\Users\alexk\Desktop\spotkanie_summary.txt"
   ```
   _Zastąp_ `"C:\Users\alexk\Desktop..."` _odpowiednimi ścieżkami dla Twojego systemu i plików._
4. **Monitoruj Proces:** Skrypt rozpocznie działanie. W terminalu pojawią się komunikaty informujące o postępie transkrypcji (z Faster-Whisper) oraz podsumowania (z Ollama). Poczekaj na zakończenie procesu. Podsumowanie zostanie zapisane w pliku podanym po fladze `-o` lub wyświetlone w terminalu, jeśli flaga `-o` nie została użyta.