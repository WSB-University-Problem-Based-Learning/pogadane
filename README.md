# Pogadane

<p align="center">
  <img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="600"/>
</p>

<p align="center">
  <strong>Transform audio recordings and YouTube videos into transcripts and AI-powered summaries</strong>
## Pogadane

Pogadane turns long-form audio recordings and YouTube videos into searchable transcripts and AI-assisted summaries that stay on your machine. The project ships with a modern Material 3 GUI and a CLI workflow.

---

## Highlights

- 🎙️ Batch transcription for local audio files and YouTube URLs
- 🤖 Summaries powered by Ollama, local Transformers, or Google Gemini
- 🖥️ Material 3 Expressive GUI with waveform visualisation and results viewer
- ⚙️ Configuration stored in `.config/config.py` with in-app overrides
- 🧰 Cross-platform installer (`install.py`) that prepares dependencies in one pass

---

## Quick Start

```bash
# 1. Clone and enter the project
git clone https://github.com/WSB-University-Problem-Based-Learning/pogadane.git
cd pogadane

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell on Windows

# 3. Install project requirements and run the guided setup
pip install -r requirements.txt
python install.py --lightweight

# 4. Launch the GUI
python -m pogadane.gui
```

Re-run the installer with `--full` for yt-dlp/Faster-Whisper helpers or `--dev` when you need pytest and linters.

---

## Installation Options

### Option A — Guided Installer (Recommended)

```bash
python install.py            # interactive wizard
python install.py --full     # all features + external binaries
python install.py --lightweight  # pure Python toolchain
python install.py --dev      # adds developer tooling
```

The script validates Python, installs project dependencies, downloads helper binaries when needed, and writes `.config/config.py` with sensible defaults.

### Option B — Manual Setup

1. Install Python 3.9+ and ensure `python`/`pip` are on PATH.
2. Install core dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-transformers.txt   # optional local summaries
   pip install -r requirements-whisper.txt        # optional Whisper backend
   ```
3. Download helper binaries if required:
   - `yt-dlp` for YouTube downloads — <https://github.com/yt-dlp/yt-dlp/releases>
   - `faster-whisper-xxl.exe` for high-quality transcription — <https://github.com/Purfview/whisper-standalone-win>
4. Point to the binaries via the GUI settings dialog or by editing `.config/config.py` (`YT_DLP_EXE`, `FASTER_WHISPER_EXE`).

---

## Running Pogadane

### GUI (Material 3 Expressive)

```bash
python -m pogadane.gui
```

- Queue files and URLs on the **Kolejka** tab
- Track progress in the persistent status bar
- Review waveform, topic timeline, transcription, and summary inside **Przeglądarka Wyników**
- Inspect runtime logs on the **Konsola** tab

### CLI Workflow

```bash
python -m pogadane.transcribe_summarize_working <audio_or_url> [more_sources]
```

Common flags:

- `--config path/to/config.py`
- `--output-dir path/to/results`
- `--summary-provider {ollama,transformers,google}`

Run with `--help` to see the full command list.

---

## Configuration

Runtime options live in `.config/config.py`. Edit the file directly or use the Settings dialog (gear icon) in the GUI—both paths keep the same configuration file up to date.

Key settings:

- `TRANSCRIPTION_PROVIDER` — `faster-whisper` or `whisper`
- `SUMMARY_PROVIDER` — `ollama`, `transformers`, or `google`
- Model names (`WHISPER_MODEL`, `TRANSFORMERS_MODEL`, `OLLAMA_MODEL`)
- External tool paths (`YT_DLP_EXE`, `FASTER_WHISPER_EXE`)

---

## Development Workflow

```bash
pip install -r requirements-dev.txt
pytest
```

Handy scripts:

- `python tools/dependency_manager.py --verify-only` — confirm external binaries (Windows)
- `python tools/pogadane_doctor.py` — legacy diagnostics when the new installer is unavailable

Before opening a PR, run tests (`pytest`) and your preferred linters/formatters.

---

## Troubleshooting

- Re-run `python install.py --full` to repair a broken environment
- Confirm binary paths in `.config/config.py`
- Use the **Konsola** tab to inspect runtime logs
- File issues at <https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues>

---

## License & Notices

- Project license: [MIT](LICENSE)
- Third-party licenses: [NOTICES.md](NOTICES.md)

Pogadane is maintained by WSB University Problem-Based Learning. Contributions and bug reports are always welcome!
1.  **Uzyskaj Klucz API Google Gemini:**
      * Przejdź do Google AI Studio ([https://aistudio.google.com/](https://aistudio.google.com/)).
      * Zaloguj się kontem Google.
      * Utwórz nowy projekt lub wybierz istniejący.
      * Wygeneruj klucz API ("Get API key"). Skopiuj go i przechowuj w bezpiecznym miejscu.
2.  **Konfiguracja w `pogadane`:**
    * Otwórz plik `.config/config.py` (lub użyj GUI).
      * Ustaw `SUMMARY_PROVIDER = "google"`.
      * Wklej swój klucz API do `GOOGLE_API_KEY = "TWOJ_KLUCZ_API_TUTAJ"`.
      * Możesz również dostosować `GOOGLE_GEMINI_MODEL` (domyślnie "gemini-1.5-flash-latest").

#### Krok 5: Instalacja bibliotek Python dla GUI i Google API

Aby uruchomić interfejs graficzny oraz korzystać z Google Gemini API, potrzebne są dodatkowe biblioteki Python. Jeśli nie użyłeś `pogadane_doctor.py`, zainstaluj je ręcznie:

1.  Otwórz terminal PowerShell.
2.  Wpisz polecenia:
    ```powershell
    pip install ttkbootstrap
    pip install google-generativeai
    ```
    Poczekaj na zakończenie instalacji.

-----

## Konfiguracja Pliku `.config/config.py`

Skrypt `src/pogadane/transcribe_summarize_working.py` oraz interfejs `src/pogadane/gui.py` zarządzają konfiguracją w następujący sposób:

1.  **Plik `.config/config.py` (Zalecane):** Aplikacja w pierwszej kolejności próbuje załadować konfigurację z pliku `.config/config.py`. Skrypt `pogadane_doctor.py` pobiera najnowszą wersję tego pliku z repozytorium (tworząc backup Twojej lokalnej wersji, jeśli istnieje).
    * **Edycja przez GUI:** Możesz wygodnie edytować większość opcji konfiguracyjnych bezpośrednio w zakładce "⚙️ Konfiguracja" w aplikacji GUI. Zmiany są zapisywane do pliku `.config/config.py`.
    * **Edycja Manualna:** Możesz również bezpośrednio edytować plik `.config/config.py`.
2.  **Konfiguracja Domyślna (Fallback):** Jeśli plik `.config/config.py` nie zostanie znaleziony, skrypt CLI i GUI użyją predefiniowanych wartości domyślnych.

**Aby dostosować konfigurację, zaleca się użycie zakładki "Konfiguracja" w GUI lub edycję pliku `.config/config.py` (po jego pobraniu przez `pogadane_doctor.py` lub ręcznie).**

Przykładowa zawartość pliku `.config/config.py` znajduje się w repozytorium (i jest pobierana przez `pogadane_doctor.py`).

**Opis opcji konfiguracyjnych (dostępnych w `config.py` oraz w GUI):**

  * `FASTER_WHISPER_EXE`: Ścieżka do `faster-whisper-xxl.exe`.
  * `YT_DLP_EXE`: Ścieżka do `yt-dlp.exe`.
  * `WHISPER_LANGUAGE`: Język transkrypcji dla Faster Whisper (domyślnie "Polish").
  * `WHISPER_MODEL`: Model Faster Whisper (domyślnie "turbo").
  * `ENABLE_SPEAKER_DIARIZATION`: Włącza/wyłącza diaryzację mówców (domyślnie `False`).
  * `DIARIZE_METHOD`: Metoda diaryzacji (np. `"pyannote_v3.1"`).
  * `DIARIZE_SPEAKER_PREFIX`: Prefiks dla mówców (np. `"MÓWCA"`).
  * `SUMMARY_PROVIDER`: Wybór systemu do generowania podsumowań. Dostępne opcje: `"ollama"` (domyślnie, lokalnie) lub `"google"` (wymaga `GOOGLE_API_KEY` i połączenia z internetem).
  * `SUMMARY_LANGUAGE`: Język, w którym ma być wygenerowane podsumowanie (domyślnie "Polish").
  * `LLM_PROMPT_TEMPLATES`: Słownik zawierający predefiniowane szablony promptów dla LLM. Klucze to nazwy szablonów, a wartości to rdzenie promptów. GUI pozwala wybrać jeden z nich.
  * `LLM_PROMPT_TEMPLATE_NAME`: Nazwa wybranego szablonu promptu z `LLM_PROMPT_TEMPLATES`. Jeśli ustawiona, ten szablon zostanie użyty.
  * `LLM_PROMPT`: Niestandardowy rdzeń promptu używany, gdy `LLM_PROMPT_TEMPLATE_NAME` jest puste, nie wskazuje na istniejący szablon, lub gdy w GUI wybrano opcję promptu niestandardowego (opcja "(Własny prompt poniżej)"). Skrypt automatycznie dołączy instrukcję językową (`SUMMARY_LANGUAGE`) oraz tekst transkrypcji.
  * `OLLAMA_MODEL`: Model językowy Ollama (używany, gdy `SUMMARY_PROVIDER="ollama"`, domyślnie "gemma3:4b").
  * `GOOGLE_API_KEY`: Klucz API do Google Gemini (wymagany, gdy `SUMMARY_PROVIDER="google"`). **Pamiętaj, aby go uzupełnić\!**
  * `GOOGLE_GEMINI_MODEL`: Model Google Gemini (używany, gdy `SUMMARY_PROVIDER="google"`, domyślnie "gemini-1.5-flash-latest").
  * `DOWNLOADED_AUDIO_FILENAME`: Bazowa nazwa tymczasowego pliku audio pobieranego z YouTube. Skrypt może dodać do niej unikalny identyfikator przy przetwarzaniu wielu URL-i.
  * `TRANSCRIPTION_FORMAT`: Format pliku wyjściowego transkrypcji używany wewnętrznie przez skrypt CLI (domyślnie 'txt').
  * `DEBUG_MODE`: Ustaw na `True`, aby włączyć bardziej szczegółowe logowanie w konsoli, w tym pełne wyniki stdout/stderr dla uruchamianych komend. Domyślnie `False`.

-----

## Uruchomienie Aplikacji (Wersja Alpha v0.1.8+)

1.  **Przygotuj Środowisko:** Uruchom `pogadane_doctor.py` lub wykonaj kroki instalacji ręcznej.
2.  **Skonfiguruj `config.py`:** Upewnij się, że `config.py` jest poprawnie skonfigurowany (ścieżki do narzędzi, modele, klucze API jeśli potrzebne). Możesz to zrobić przez GUI lub edytując plik bezpośrednio.

### Uruchomienie Interfejsu Graficznego (GUI) (Zalecane)

Pogadane oferuje **trzy interfejsy graficzne** do wyboru:

#### � Material 3 Expressive GUI (NAJNOWSZY - Zalecany)
Najnowocześniejszy interfejs z prawdziwym Material Design 3, płynnymi animacjami 60fps i renderowaniem Flutter.

```powershell
python run_gui_flet.py
```

**Funkcje:**
- 💫 Płynne animacje 60fps (Flutter)
- 🌓 Automatyczne wykrywanie motywu systemowego
- 🎨 Prawdziwy Material Design 3 (nie tylko inspirowany!)
- 📱 Wersja webowa dostępna (`flet run --web`)
- 🔔 Natywne powiadomienia (snackbars)
- 📂 Natywne okna dialogowe systemu
- 🚀 Potencjał mobilny (Android/iOS w przyszłości)

**Dokumentacja:** [GUI_MATERIAL_3_EXPRESSIVE.md](doc/GUI_MATERIAL_3_EXPRESSIVE.md)

#### 🎨 Material Design GUI (CustomTkinter)
Nowoczesny interfejs z Material Design, wsparciem dla trybu ciemnego i zaokrąglonymi rogami.

```powershell
python run_gui_material.py
```

**Funkcje:**
- 🌙 Przełącznik trybu ciemnego/jasnego
- 🎯 Nowoczesny wygląd Material Design 2
- 📱 Zaokrąglone rogi i karty
- ⚡ Szybkie uruchamianie

**Dokumentacja:** [GUI_MATERIAL_DESIGN.md](doc/GUI_MATERIAL_DESIGN.md)

#### 🖥️ Legacy Bootstrap GUI
Stabilny, sprawdzony interfejs w stylu Bootstrap.

```powershell
python -m pogadane.gui
```

**Funkcje:**
- 🏆 Maksymalna stabilność
- ⚡ Najlżejszy (najmniej pamięci)
- 🔧 Sprawdzony w boju

**Zobacz również:** [Porównanie GUI](doc/GUI_COMPARISON_ALL.md) aby wybrać najlepszą opcję dla siebie.

#### Korzystanie z GUI (wszystkie wersje):

1.  **Otwórz Terminal:** Otwórz terminal PowerShell.
2.  **Przejdź do Katalogu Projektu:** Użyj polecenia `cd`, aby przejść do katalogu, w którym umieściłeś pliki.
    ```powershell
    cd "C:\Sciezka\Do\Twojego\Katalogu\Pogadane"
    ```
3.  **Uruchom wybraną wersję GUI** (zobacz powyżej)

4.  **Korzystanie z GUI:**
      * **Dane Wejściowe:** W polu tekstowym "Pliki audio / URL-e YouTube" wprowadź jedną lub więcej ścieżek do lokalnych plików audio lub URL-i YouTube, **każdą w nowej linii**. Możesz użyć przycisku "➕ Dodaj Pliki Audio" do wybrania i dodania plików.
      * **Kolejka Przetwarzania:** Poniżej pola wejściowego znajduje się tabela "Kolejka Przetwarzania", która wyświetli dodane pliki i ich status podczas przetwarzania.
      * **Konfiguracja:** Przejdź do zakładki "⚙️ Konfiguracja", aby dostosować ustawienia. Pamiętaj, aby kliknąć "💾 Zapisz i Zastosuj". Dostępne są również przyciski "A+" / "A-" do zmiany rozmiaru czcionki w aplikacji. Wiele elementów interfejsu posiada podpowiedzi (tooltips) po najechaniu myszką.
      * **Uruchomienie:** Kliknij przycisk "🚀 Rozpocznij Przetwarzanie Wsadowe". Aplikacja przetworzy każde źródło sekwencyjnie. Postęp ogólny będzie widoczny na pasku postępu.
      * **Wyniki:**
          * **🖥️ Konsola:** Wyświetla szczegółowe logi z całego procesu przetwarzania.
          * **📊 Wyniki (Transkrypcje i Streszczenia):** Ta zakładka zawiera listę rozwijaną "Wybierz przetworzony plik". Po wybraniu pliku z tej listy, jego indywidualna transkrypcja i streszczenie zostaną wyświetlone w odpowiednich polach poniżej.
      * **Zapisywanie:** Przycisk "💾 Zapisz Log" w zakładce "Konsola" pozwala zapisać cały log. Indywidualne transkrypcje i streszczenia można skopiować z pól w zakładce "Wyniki".

### Uruchomienie Skryptu z Linii Komend (CLI)

Skrypt `transcribe_summarize_working.py` obsługuje przetwarzanie wsadowe.

1.  **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell i przejdź do katalogu ze skryptami.

2.  **Wykonaj Polecenie Uruchomienia Skryptu:**

    **Ogólny wzór:**

    ```powershell
    python -m pogadane.transcribe_summarize_working [<ścieżka1_LUB_URL1> <ścieżka2_LUB_URL2>...] [-a <plik_wsadowy.txt>] [--diarize | --no-diarize] [-o "<ścieżka_do_katalogu_LUB_pliku_podsumowania>"]
    ```

      * `<ścieżka1_LUB_URL1> ...`: Jedna lub więcej ścieżek do plików audio lub URL-i YouTube, podanych bezpośrednio. Można pominąć, jeśli używana jest opcja `-a`.
      * `-a <plik_wsadowy.txt>` lub `--batch-file <plik_wsadowy.txt>`: Ścieżka do pliku tekstowego z listą źródeł (jedno na linię).
      * `--diarize` | `--no-diarize`: Nadpisuje ustawienie diaryzacji z `config.py`.
      * `-o "<ścieżka_wyjściowa>"`:
          * Jeśli podano jedno wejście (i `-o` nie jest istniejącym katalogiem oraz nie wygląda jak katalog bez rozszerzenia): pełna ścieżka do pliku podsumowania.
          * Jeśli podano wiele wejść (bezpośrednio lub przez `-a`) LUB jeśli `-o` wskazuje na istniejący katalog (lub nie istnieje, ale nie ma rozszerzenia): ścieżka do KATALOGU, gdzie zostaną zapisane pliki podsumowań (np. `nazwa_pliku.summary.txt`).

    **Przykłady:**

    ```powershell
    # Przetwarzanie jednego pliku, zapis podsumowania do konkretnego pliku
    python -m pogadane.transcribe_summarize_working "C:\Nagrania\spotkanie.mp3" -o "C:\Podsumowania\spotkanie_summary.txt"

    # Przetwarzanie wielu URL-i, zapis podsumowań do katalogu "WynikiYouTube"
    python -m pogadane.transcribe_summarize_working "URL_YOUTUBE_1" "URL_YOUTUBE_2" -o "C:\MojeDokumenty\WynikiYouTube"

    # Przetwarzanie z pliku wsadowego, podsumowania drukowane do konsoli
    python -m pogadane.transcribe_summarize_working -a "C:\lista_do_przetworzenia.txt"
    ```

3.  **Monitoruj Proces:** Skrypt wyświetli postęp przetwarzania dla każdego pliku.

---

## Quick Start (English)

This short Quick Start helps non-experts run the Pogadane GUI or CLI on Windows.
It's intentionally minimal — follow Polish docs above for full details.

Prerequisites (simple):
- Windows
- Python 3.8+ installed (select "Add Python to PATH" during install)
- Optional: Faster-Whisper standalone (`faster-whisper-xxl.exe`), `yt-dlp.exe`, or Ollama if you plan to use those features.

1) Create and activate a virtual environment (recommended):

```powershell
cd C:\path\to\pogadane
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

2) Install Python dependencies (GUI + Google API client):

```powershell
pip install --upgrade pip
pip install ttkbootstrap google-generativeai
```

3) (Optional) Run the helper script to fetch recommended files and Python packages:

```powershell
python tools\pogadane_doctor.py
```

4) Configure optional external tools:
- If you want to transcribe YouTube videos, download `yt-dlp.exe` and put its path in `.config\config.py` or keep it in the project folder.
- For transcription, choose one option:
  * **Faster-Whisper (recommended)**: Download Faster-Whisper standalone and set `FASTER_WHISPER_EXE` in `.config\config.py`. Best quality, GPU support, speaker diarization.
  * **Whisper (lightweight)**: Run `pip install -r requirements-whisper.txt`. Pure Python, no executables needed. Models: 75MB-3GB.
- For AI summaries, choose one option:
  * **Ollama (recommended)**: Install Ollama and pull a model (e.g. `ollama pull gemma3:4b`). Multi-language support.
  * **Transformers (lightweight)**: Run `pip install -r requirements-transformers.txt`. No Ollama needed, but English summaries only.
  * **Google Gemini**: Set `GOOGLE_API_KEY` in `.config\config.py`. Requires internet.

5) Run the GUI (recommended for beginners):

```powershell
# from project root with venv activated
python -m pogadane.gui
```

6) Run the CLI (batch runs / automation):

```powershell
python -m pogadane.transcribe_summarize_working "C:\path\to\file.mp3" -o "C:\path\to\summary.txt"

# or multiple sources
python -m pogadane.transcribe_summarize_working "URL1" "C:\file2.wav" -o "C:\output_dir"
```

7) Sample test audio included:
- `samples/` contains `Styrta się pali.mp3` (small test audio taken from YouTube). Use it to verify a complete run.

### Troubleshooting

**Problem: "Python is not recognized as an internal or external command"**
- **Solution:** Reinstall Python and ensure "Add Python to PATH" is checked during installation
- **Verify:** Open new PowerShell and run `python --version`

**Problem: "No module named 'ttkbootstrap'" or "No module named 'google.generativeai'"**
- **Solution:** Activate virtual environment and install dependencies:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

**Problem: "No module named 'transformers'" or "No module named 'torch'"**
- **Solution:** You're using `SUMMARY_PROVIDER="transformers"` but libraries aren't installed:
  ```powershell
  pip install -r requirements-transformers.txt
  # Or manually: pip install transformers torch
  ```
- **Verify:** `python -c "import transformers; print('OK')"`

**Problem: "No module named 'whisper'"**
- **Solution:** You're using `TRANSCRIPTION_PROVIDER="whisper"` but library isn't installed:
  ```powershell
  pip install -r requirements-whisper.txt
  # Or manually: pip install openai-whisper
  ```
- **Verify:** `python -c "import whisper; print('OK')"`

**Problem: GUI window doesn't open**
- **Check:** Are you in the correct directory? (`cd C:\path\to\pogadane`)
- **Check:** Is venv activated? (you should see `(.venv)` in prompt)
- **Try:** Run with full module path: `python -m pogadane.gui`
- **Check logs:** Look for error messages in terminal

**Problem: Transcription fails with "File not found: faster-whisper-xxl.exe"**
- **Solution:** Configure path in GUI (⚙️ Konfiguracja tab → Plik Faster Whisper → click 📂)
- **Alternative:** Use lightweight Whisper: `pip install -r requirements-whisper.txt` and set `TRANSCRIPTION_PROVIDER="whisper"` in config
- **Alternative:** Place `faster-whisper-xxl.exe` in project root directory
- **Verify:** Check `.config/config.py` has correct `FASTER_WHISPER_EXE` path

**Problem: YouTube download fails**
- **Solution:** Ensure `yt-dlp.exe` is in project folder or configured in settings
- **Check:** Internet connection is active
- **Update:** Download latest version from [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases/latest)

**Problem: Summary generation fails with Ollama**
- **Check:** Ollama service is running (should be in system tray)
- **Verify model:** Run `ollama list` to confirm model is downloaded
- **Test:** Try `ollama run gemma3:4b` in terminal
- **Logs:** Check GUI Console tab for detailed error messages

**Problem: Summary generation fails with Google Gemini**
- **Check:** Valid API key is set in `.config/config.py` (`GOOGLE_API_KEY`)
- **Verify:** `SUMMARY_PROVIDER` is set to `"google"` in configuration
- **Internet:** Ensure you have active internet connection
- **Quota:** Check if you've exceeded free tier limits at [Google AI Studio](https://aistudio.google.com/)

**Problem: Transcription is in wrong language**
- **Solution:** Set correct language in GUI (⚙️ Konfiguracja → Język transkrypcji)
- **Save:** Click 💾 Zapisz i Zastosuj after making changes

**Problem: "Access Denied" or permission errors**
- **Solution:** Run PowerShell as Administrator
- **Alternative:** Install project in user directory (e.g., `C:\Users\YourName\Documents\pogadane`)

**Problem: Process is slow or freezes**
- **First transcription:** Faster-Whisper downloads models on first run (this is normal, ~1-2GB)
- **Check:** Task Manager → ensure Python isn't using 100% CPU indefinitely
- **Try:** Smaller model in settings (⚙️ Konfiguracja → Model Whisper → try "small" or "base")

**Problem: Virtual environment activation fails with "execution of scripts is disabled"**
- **Solution:** Enable script execution (run PowerShell as Administrator):
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Then retry:** `.\.venv\Scripts\Activate.ps1`

**Need more help?**
- See detailed Polish documentation above
- Check [QUICK_START.md](QUICK_START.md) for beginner-friendly guide
- Visit [Issues](https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues) on GitHub

For more detailed instructions, see the Polish sections above or `doc/README.md`.
