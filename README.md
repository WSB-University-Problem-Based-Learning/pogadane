# pogadane

<img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane"/>

Aplikacja do generowania streszczeń z nagrań audio (np. spotkań Teams, podcastów) lub filmów na YouTube. Działa lokalnie (offline dla transkrypcji i podsumowań Ollama, poza pobieraniem z YouTube), co zapewnia bezpieczeństwo danych. Umożliwia szybkie uzyskanie najważniejszych informacji z długich materiałów. Od wersji v0.1.7 wspiera również Google Gemini API jako alternatywnego dostawcę podsumowań. Wersja v0.1.8 wprowadza możliwość wyboru szablonów promptów LLM, przetwarzanie wsadowe w CLI i GUI, menedżer wyników w GUI oraz opcję dostosowania rozmiaru czcionki.

Projekt zawiera zarówno interfejs linii komend (CLI) `transcribe_summarize_working.py`, jak i interfejs graficzny użytkownika (GUI) `gui.py`.

**Spis Treści**
1.  [Architektura Systemu](#architektura-systemu)
2.  [Wymagania Wstępne](#wymagania-wstępne)
3.  [Konfiguracja](#konfiguracja)
4.  [Instalacja Komponentów](#instalacja-komponentów)
    * [Krok 1: Instalacja środowiska Python](#krok-1-instalacja-środowiska-python)
    * [Krok 2: Instalacja Faster-Whisper Standalone](#krok-2-instalacja-faster-whisper-standalone)
    * [Krok 3: Pobranie yt-dlp](#krok-3-pobranie-yt-dlp-do-obsługi-youtube)
    * [Krok 4: Instalacja Systemu Podsumowań](#krok-4-instalacja-systemu-podsumowań)
        * [Opcja A: Instalacja Ollama i Pobranie Modelu Językowego (Lokalnie)](#opcja-a-instalacja-ollama-i-pobranie-modelu-językowego-lokalnie)
        * [Opcja B: Konfiguracja Google Gemini API (Online)](#opcja-b-konfiguracja-google-gemini-api-online)
    * [Krok 5: Instalacja biblioteki GUI](#krok-5-instalacja-biblioteki-gui-ttkbootstrap)
5.  [Uruchomienie Aplikacji](#uruchomienie-aplikacji)
    * [Uruchomienie Interfejsu Graficznego (GUI) (Wersja Alpha v0.1.8+) (Zalecane)](#uruchomienie-interfejsu-graficznego-gui-wersja-alpha-v018-zalecane)
    * [Uruchomienie Skryptu z Linii Komend (CLI) (Wersja Alpha v0.1.8+)](#uruchomienie-skryptu-z-linii-komend-cli-wersja-alpha-v018)
6.  [Poprzednie Wersje](#poprzednie-wersje)

---
## Architektura Systemu

Poniższy diagram przedstawia ogólną architekturę aplikacji "pogadane":

```mermaid
flowchart TD
 subgraph pogadane_app["Aplikacja Pogadane"]
    direction LR
        gui_app["GUI (z obsługą wsadową)"]
        cli_script["Skrypt Główny (CLI / Logika)"]
  end
 subgraph summarization_choice["Wybór Systemu Streszczeń"]
    direction LR
        ollama_sum{{"Ollama (LLM Lokalny)"}}
        google_gemini_sum{{"Google Gemini API (LLM Online)"}}
  end
 subgraph processing_pipeline["Pipeline Przetwarzania (dla każdego źródła)"]
    direction LR
        yt_dlp{{"yt-dlp"}}
        downloaded_audio[("Pobrane Audio")]
        faster_whisper{{"Faster-Whisper"}}
        transcription_text["Tekst Transkrypcji"]
        summarization_choice
  end
    user["Użytkownik"] --> input_source["Dostarcza Wejście (Plik(i) Audio / URL(e) YouTube)"]
    input_source -- Poprzez pole tekstowe (wiele linii) --> gui_app
    user -. Uruchamia CLI (opcjonalnie) .-> cli_script
    input_source -. Argumenty / Plik wsadowy .-> cli_script
    
    config_file["config.py"] <-. Konfiguruje .-> gui_app
    config_file -. Odczytuje konfigurację .-> cli_script
    
    gui_app -- Wywołuje logikę (sekwencyjnie dla każdego źródła) --> cli_script
    
    cli_script -. "1.Pobierz (jeśli URL)" .-> yt_dlp
    yt_dlp --> downloaded_audio
    cli_script -- 2.Transkrybuj Audio --> faster_whisper
    downloaded_audio -.-> faster_whisper
    faster_whisper --> transcription_text
    cli_script -- "3.Streszczaj<br>(na podst. config:<br>PROVIDER, PROMPT_TEMPLATE, LANG)" --> summarization_choice
    transcription_text -- Tekst transkrypcji --> summarization_choice
    summarization_choice -- Wybór: ollama --> ollama_sum
    summarization_choice -- Wybór: google --> google_gemini_sum
    ollama_sum -- Tekst streszczenia --> cli_script
    google_gemini_sum -- Tekst streszczenia --> cli_script
    
    cli_script -- Generuje wynik (dla każdego źródła) --> individual_results["Indywidualne Wyniki"]
    individual_results -- Prezentowane w GUI (menedżer wyników) / Zapisywane (CLI) --> final_output["Wynik Końcowy (Streszczenie, Transkrypcja)"]
    gui_app -. Prezentuje / Umożliwia Zapis .-> final_output


    style gui_app fill:#C8E6C9,stroke:#333,stroke-width:2px
    style cli_script fill:#B3E5FC,stroke:#333,stroke-width:2px
    style ollama_sum fill:#FFCDD2,stroke:#333,stroke-width:2px
    style google_gemini_sum fill:#FFDDAA,stroke:#333,stroke-width:2px 
    style yt_dlp fill:#FFCCBC,stroke:#333,stroke-width:2px
    style downloaded_audio fill:#FFCCBC,stroke:#333,stroke-width:2px
    style faster_whisper fill:#D1C4E9,stroke:#333,stroke-width:2px
    style transcription_text fill:#E1BEE7,stroke:#333,stroke-width:2px
    style summarization_choice fill:#F0F4C3,stroke:#333,stroke-width:1px
    style input_source fill:#E3F2FD,stroke:#333,stroke-width:2px
    style final_output fill:#A5D6A7,stroke:#333,stroke-width:2px
    style processing_pipeline fill:#F5F5F5,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
    style individual_results fill:#FFF9C4,stroke:#333,stroke-width:1px
```

**Opis komponentów:**

  * **Użytkownik**: Osoba inicjująca proces transkrypcji i streszczenia.
  * **Wejście (Plik(i) Audio / URL(e) YouTube)** (`input_source`): Plik(i) audio dostarczone przez użytkownika lub adres(y) URL do materiału(ów) na YouTube. GUI pozwala na wprowadzenie wielu źródeł w polu tekstowym (każde w nowej linii). CLI akceptuje wiele źródeł jako argumenty lub z pliku wsadowego.
  * **config.py** (`config_file`): Plik konfiguracyjny aplikacji, zawierający ustawienia takie jak ścieżki do narzędzi, wybór modeli, parametry transkrypcji, dostawcę podsumowań, szablony promptów LLM oraz prompt niestandardowy.
  * **Aplikacja Pogadane** (`pogadane_app`):
      * **Interfejs Graficzny (GUI)** (`gui_app`): Zalecany sposób interakcji. Umożliwia wprowadzenie wielu źródeł, zarządzanie konfiguracją (`config.py`), śledzenie postępu w kolejce, przeglądanie indywidualnych wyników dla każdego przetworzonego pliku w menedżerze wyników oraz dostosowanie rozmiaru czcionki. Wywołuje Skrypt Główny sekwencyjnie dla każdego źródła.
      * **Skrypt Główny (CLI / Logika)** (`cli_script`): Plik `transcribe_summarize_working.py`. Rdzeń logiki: pobieranie audio, transkrypcja, generowanie streszczenia. Może być uruchamiany bezpośrednio z linii komend (z obsługą wsadową) lub być wywoływany przez GUI (dla pojedynczych zadań z listy wsadowej GUI).
  * **Pipeline Przetwarzania (dla każdego źródła)** (`processing_pipeline`): Sekwencja operacji wykonywana dla każdego pliku/URL-a z listy:
      * **yt-dlp** (`yt_dlp`): Narzędzie do pobierania audio z URL.
      * **Pobrane Audio** (`downloaded_audio`): Tymczasowy plik audio.
      * **Faster-Whisper** (`faster_whisper`): Narzędzie do transkrypcji audio na tekst.
      * **Tekst Transkrypcji** (`transcription_text`): Wynik działania `Faster-Whisper`.
      * **Wybór Systemu Streszczeń** (`summarization_choice`): Logika w skrypcie decydująca na podstawie `config.py` (`SUMMARY_PROVIDER`), który system LLM zostanie użyty. Prompt jest konstruowany na podstawie wybranego szablonu (`LLM_PROMPT_TEMPLATE_NAME`) lub promptu niestandardowego (`LLM_PROMPT`) oraz języka podsumowania (`SUMMARY_LANGUAGE`).
          * **Ollama (LLM Lokalny)** (`ollama_sum`): Platforma uruchamiająca lokalnie duże modele językowe.
          * **Google Gemini API (LLM Online)** (`google_gemini_sum`): Usługa Google Cloud AI.
  * **Indywidualne Wyniki** (`individual_results`): Transkrypcja i streszczenie generowane dla każdego przetworzonego źródła.
  * **Wynik Końcowy** (`final_output`):
      * **W GUI:** Wyniki dla poszczególnych plików są dostępne do przeglądania w dedykowanej zakładce "Wyniki" poprzez wybór z listy. Logi z całego procesu są dostępne w zakładce "Konsola".
      * **W CLI:** Streszczenia są drukowane do konsoli lub zapisywane do plików (do katalogu, jeśli przetwarzano wiele źródeł i podano opcję `-o`).

-----

## Wymagania Wstępne

  * System operacyjny Windows.
  * Python (zalecany 3.7+).
  * Połączenie z Internetem (do pobrania oprogramowania, materiałów z YouTube oraz opcjonalnie do korzystania z Google Gemini API).
  * Uprawnienia administratora mogą być wymagane do instalacji niektórych programów.
  * Narzędzie do dekompresji archiwów `.7z` (np. [7-Zip](https://www.7-zip.org/)).

-----

## Konfiguracja

Skrypt `transcribe_summarize_working.py` oraz interfejs `gui.py` zarządzają konfiguracją w następujący sposób:

1.  **Plik `config.py` (Zalecane):** Aplikacja w pierwszej kolejności próbuje załadować konfigurację z pliku `config.py`. **Plik `config.py` z domyślnymi ustawieniami jest dołączony do repozytorium.**
      * **Edycja przez GUI:** Możesz wygodnie edytować większość opcji konfiguracyjnych bezpośrednio w zakładce "⚙️ Konfiguracja" w aplikacji GUI. Zmiany są zapisywane do pliku `config.py`.
      * **Edycja Manualna:** Możesz również bezpośrednio edytować plik `config.py`.
2.  **Konfiguracja Domyślna (Fallback):** Jeśli plik `config.py` nie zostanie znaleziony, skrypt CLI i GUI użyją predefiniowanych wartości domyślnych.

**Aby dostosować konfigurację, zaleca się użycie zakładki "Konfiguracja" w GUI lub edycję pliku `config.py`.**

Przykładowa zawartość pliku `config.py` znajduje się w repozytorium.

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

### Krok 4: Instalacja Systemu Podsumowań

Masz dwie opcje generowania podsumowań: lokalnie za pomocą Ollama lub online przez Google Gemini API.

#### Opcja A: Instalacja Ollama i Pobranie Modelu Językowego (Lokalnie)

Jeśli chcesz generować podsumowania lokalnie (zalecane dla prywatności i działania offline):

1.  **Pobierz Ollama:** Przejdź na oficjalną stronę Ollama ([https://ollama.com/](https://ollama.com/)) i pobierz wersję dla Windows.
2.  **Zainstaluj Ollama:** Uruchom instalator.
3.  **Pobierz Model Językowy:** Otwórz terminal PowerShell i wykonaj polecenie, aby pobrać model zdefiniowany w `config.py` (domyślnie `OLLAMA_MODEL="gemma3:4b"`):
    ```powershell
    ollama pull gemma3:4b
    ```
    (Jeśli zmieniłeś `OLLAMA_MODEL` w konfiguracji, użyj tutaj odpowiedniej nazwy modelu).
4.  **Sprawdź Działanie Ollama:** Upewnij się, że Ollama działa w tle (`ollama list`).
5.  **Konfiguracja w `pogadane`:** W pliku `config.py` (lub przez GUI) ustaw `SUMMARY_PROVIDER = "ollama"`.

#### Opcja B: Konfiguracja Google Gemini API (Online)

Jeśli chcesz używać Google Gemini API do generowania podsumowań (wymaga połączenia z internetem i klucza API):

1.  **Uzyskaj Klucz API Google Gemini:**
      * Przejdź do Google AI Studio ([https://aistudio.google.com/](https://aistudio.google.com/)).
      * Zaloguj się kontem Google.
      * Utwórz nowy projekt lub wybierz istniejący.
      * Wygeneruj klucz API ("Get API key"). Skopiuj go i przechowuj w bezpiecznym miejscu.
2.  **Zainstaluj bibliotekę Python:** Otwórz terminal PowerShell i wpisz:
    ```powershell
    pip install google-generativeai
    ```
3.  **Konfiguracja w `pogadane`:**
      * Otwórz plik `config.py` (lub użyj GUI).
      * Ustaw `SUMMARY_PROVIDER = "google"`.
      * Wklej swój klucz API do `GOOGLE_API_KEY = "TWOJ_KLUCZ_API_TUTAJ"`.
      * Możesz również dostosować `GOOGLE_GEMINI_MODEL` (domyślnie "gemini-1.5-flash-latest").

### Krok 5: Instalacja biblioteki GUI (ttkbootstrap)

Aby uruchomić interfejs graficzny, potrzebna jest biblioteka `ttkbootstrap`. Zainstaluj ją używając pip:

1.  Otwórz terminal PowerShell.
2.  Wpisz polecenie:
    ```powershell
    pip install ttkbootstrap
    ```
    Poczekaj na zakończenie instalacji.

-----

## Uruchomienie Aplikacji

1.  **Pobierz/Skopiuj Skrypty:** Upewnij się, że masz najnowsze wersje plików `gui.py`, `transcribe_summarize_working.py` oraz `config.py` z repozytorium. Umieść je wszystkie w jednym katalogu.
2.  **Dostosuj `config.py`:** Upewnij się, że `config.py` jest poprawnie skonfigurowany.

### Uruchomienie Interfejsu Graficznego (GUI) (Wersja Alpha v0.1.8+) (Zalecane)

Interfejs graficzny `gui.py` jest zalecanym sposobem korzystania z aplikacji i obsługuje przetwarzanie wsadowe.

1.  **Otwórz Terminal:** Otwórz terminal PowerShell.
2.  **Przejdź do Katalogu Projektu:** Użyj polecenia `cd`, aby przejść do katalogu, w którym umieściłeś pliki.
    ```powershell
    cd "C:\Sciezka\Do\Twojego\Katalogu\Pogadane"
    ```
3.  **Uruchom GUI:** Wpisz polecenie:
    ```powershell
    python gui.py
    ```
4.  **Korzystanie z GUI:**
      * **Dane Wejściowe:** W polu tekstowym "Pliki audio / URL-e YouTube" wprowadź jedną lub więcej ścieżek do lokalnych plików audio lub URL-i YouTube, **każdą w nowej linii**. Możesz użyć przycisku "➕ Dodaj Pliki Audio" do wybrania i dodania plików.
      * **Kolejka Przetwarzania:** Poniżej pola wejściowego znajduje się tabela "Kolejka Przetwarzania", która wyświetli dodane pliki i ich status podczas przetwarzania.
      * **Konfiguracja:** Przejdź do zakładki "⚙️ Konfiguracja", aby dostosować ustawienia. Pamiętaj, aby kliknąć "💾 Zapisz i Zastosuj". Dostępne są również przyciski "A+" / "A-" do zmiany rozmiaru czcionki w aplikacji. Wiele elementów interfejsu posiada podpowiedzi (tooltips) po najechaniu myszką.
      * **Uruchomienie:** Kliknij przycisk "🚀 Rozpocznij Przetwarzanie Wsadowe". Aplikacja przetworzy każde źródło sekwencyjnie. Postęp ogólny będzie widoczny na pasku postępu.
      * **Wyniki:**
          * **🖥️ Konsola:** Wyświetla szczegółowe logi z całego procesu przetwarzania.
          * **📊 Wyniki (Transkrypcje i Streszczenia):** Ta zakładka zawiera listę rozwijaną "Wybierz przetworzony plik". Po wybraniu pliku z tej listy, jego indywidualna transkrypcja i streszczenie zostaną wyświetlone w odpowiednich polach poniżej.
      * **Zapisywanie:** Przycisk "💾 Zapisz Log" w zakładce "Konsola" pozwala zapisać cały log. Indywidualne transkrypcje i streszczenia można skopiować z pól w zakładce "Wyniki".

### Uruchomienie Skryptu z Linii Komend (CLI) (Wersja Alpha v0.1.8+)

Skrypt `transcribe_summarize_working.py` obsługuje przetwarzanie wsadowe.

1.  **Otwórz Terminal w Odpowiedniej Lokalizacji:** Otwórz terminal PowerShell i przejdź do katalogu ze skryptami.

2.  **Wykonaj Polecenie Uruchomienia Skryptu:**

    **Ogólny wzór:**

    ```powershell
    python transcribe_summarize_working.py [<ścieżka1_LUB_URL1> <ścieżka2_LUB_URL2>...] [-a <plik_wsadowy.txt>] [--diarize | --no-diarize] [-o "<ścieżka_do_katalogu_LUB_pliku_podsumowania>"]
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
    python transcribe_summarize_working.py "C:\Nagrania\spotkanie.mp3" -o "C:\Podsumowania\spotkanie_summary.txt"

    # Przetwarzanie wielu URL-i, zapis podsumowań do katalogu "WynikiYouTube"
    python transcribe_summarize_working.py "URL_YOUTUBE_1" "URL_YOUTUBE_2" -o "C:\MojeDokumenty\WynikiYouTube"

    # Przetwarzanie z pliku wsadowego, podsumowania drukowane do konsoli
    python transcribe_summarize_working.py -a "C:\lista_do_przetworzenia.txt"
    ```

3.  **Monitoruj Proces:** Skrypt wyświetli postęp przetwarzania dla każdego pliku.

-----

## Poprzednie Wersje

Historyczne wersje skryptu są archiwizowane w katalogu `previous_versions` w repozytorium projektu.
