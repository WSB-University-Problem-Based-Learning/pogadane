import subprocess
import sys
import os
import argparse
from pathlib import Path
import shlex # Used for safer command construction if needed, though list format is preferred
import re # Import regular expressions for URL validation (basic)

# Wersja Alpha v0.1.4

# Próba załadowania konfiguracji z pliku config.py
try:
    import config
    print("✅ Konfiguracja załadowana z pliku config.py.")
except ImportError:
    print("⚠️ Ostrzeżenie: Plik konfiguracyjny config.py nie został znaleziony.", file=sys.stderr)
    print("   Używam domyślnych wartości konfiguracyjnych.", file=sys.stderr)
    print("   Aby dostosować ustawienia, utwórz plik config.py (szablon w README.md).", file=sys.stderr)

    # Definicja domyślnej konfiguracji jako obiektu zastępczego
    class DefaultConfig:
        # --- Default Configuration ---
        # Ścieżki do plików wykonywalnych
        FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
        YT_DLP_EXE = "yt-dlp.exe"

        # Ustawienia Whisper
        WHISPER_LANGUAGE = "Polish"
        WHISPER_MODEL = "turbo"

        # Ustawienia Ollama
        OLLAMA_MODEL = "gemma3:4b"

        # Prompt dla modelu językowego (Ollama)
        LLM_PROMPT = "Streść poniższy tekst po polsku, skupiając się na kluczowych wnioskach i decyzjach:\n\n{text}"

        # Ustawienia Ogólne Skryptu
        TRANSCRIPTION_FORMAT = "txt"
        DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"
        # --- End Default Configuration ---

    config = DefaultConfig() # Użyj domyślnej konfiguracji

def run_command(command_list, input_data=None, capture_output=True, text_encoding='utf-8'):
    """Runs an external command safely."""
    print(f"\n▶️ Running command: {' '.join(command_list)}")
    try:
        process = subprocess.run(
            command_list,
            input=input_data if input_data else None,
            capture_output=capture_output,
            text=True,
            encoding=text_encoding,
            check=False,
            shell=False
        )
        print(f"☑️ Command finished with exit code: {process.returncode}")
        if process.stdout:
            print("--- stdout ---")
            print(process.stdout.strip())
            print("--------------")
        if process.stderr:
            print("--- stderr ---", file=sys.stderr)
            print(process.stderr.strip(), file=sys.stderr)
            print("--------------", file=sys.stderr)

        if process.returncode != 0:
            print(f"⚠️ Warning: Command exited with non-zero status {process.returncode}.", file=sys.stderr)

        return process

    except FileNotFoundError:
        print(f"❌ Error: Command not found: {command_list[0]}", file=sys.stderr)
        print("Ensure the executable is in your PATH or the correct directory, as specified in config.py or default settings.", file=sys.stderr)
        return None
    except TypeError as e:
        print(f"❌ TypeError during subprocess interaction: {e}", file=sys.stderr)
        print("   This might indicate an issue with text=True vs input data type.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred while running the command: {e}", file=sys.stderr)
        return None

def download_youtube_audio(url):
    """Downloads audio from a YouTube URL using yt-dlp."""
    print(f"\n🔄 Starting YouTube Audio Download for: {url}")
    print(f"   Using yt-dlp: {config.YT_DLP_EXE}")
    print(f"   Outputting to temporary file: {config.DOWNLOADED_AUDIO_FILENAME}")

    command = [
        config.YT_DLP_EXE,
        "-x",
        "--audio-format", "mp3",
        "--force-overwrite",
        "-o", config.DOWNLOADED_AUDIO_FILENAME,
        url
    ]

    process = run_command(command, capture_output=True)

    download_path = Path(config.DOWNLOADED_AUDIO_FILENAME)
    download_successful = download_path.is_file() and download_path.stat().st_size > 0

    if process and process.returncode == 0 and download_successful:
        print(f"✅ YouTube audio downloaded successfully: {download_path}")
        return download_path
    elif process and process.returncode != 0 and download_successful:
         print(f"⚠️ Warning: yt-dlp exited with code {process.returncode}, but the audio file was created.", file=sys.stderr)
         print(f"   Proceeding with downloaded file: {download_path}", file=sys.stderr)
         return download_path
    else:
        print(f"❌ YouTube audio download failed. Exit code: {process.returncode if process else 'N/A'}", file=sys.stderr)
        if not download_successful and download_path.exists():
             print(f"   The output file '{download_path}' exists but might be empty or invalid.", file=sys.stderr)
        elif not download_path.exists():
             print(f"   The output file '{download_path}' was not created.", file=sys.stderr)
        if download_path.exists():
            try:
                os.remove(download_path)
                print(f"   Removed potentially incomplete file: {download_path}")
            except OSError as e:
                print(f"   Warning: Could not remove incomplete file {download_path}: {e}", file=sys.stderr)
        return None

def transcribe_audio(audio_path_str):
    """Transcribes the audio file using Faster Whisper."""
    audio_path = Path(audio_path_str)
    if not audio_path.is_file():
        print(f"❌ Error: Audio file not found at '{audio_path}'", file=sys.stderr)
        return None

    base_name = audio_path.stem
    transcription_output_path = audio_path.with_name(f"{base_name}_transcription").with_suffix(f'.{config.TRANSCRIPTION_FORMAT}')

    print(f"\n🔄 Starting Transcription for: {audio_path}")
    print(f"   Using Faster Whisper: {config.FASTER_WHISPER_EXE}")
    print(f"   Expected output: {transcription_output_path}")

    command = [
        config.FASTER_WHISPER_EXE,
        str(audio_path),
        "--language", config.WHISPER_LANGUAGE,
        "--model", config.WHISPER_MODEL,
        "--output_format", config.TRANSCRIPTION_FORMAT,
        "--output_dir", str(transcription_output_path.parent),
    ]

    process = run_command(command, capture_output=True)

    transcription_file_exists = transcription_output_path.is_file()

    if process and process.returncode != 0:
        print(f"⚠️ Warning: faster-whisper-xxl.exe exited with code {process.returncode}.", file=sys.stderr)
        if transcription_file_exists:
            print(f"   However, output file '{transcription_output_path}' was found. Attempting to proceed.", file=sys.stderr)
        else:
             print(f"   Output file '{transcription_output_path}' was *not* found. Transcription likely failed.", file=sys.stderr)

    if transcription_file_exists:
        print(f"✅ Transcription file found: {transcription_output_path}")
        return transcription_output_path
    else:
        fallback_transcription_path = audio_path.with_suffix(f'.{config.TRANSCRIPTION_FORMAT}')
        if fallback_transcription_path.is_file():
             print(f"ℹ️ Info: Transcription file found in source directory instead: {fallback_transcription_path}")
             return fallback_transcription_path
        else:
            print(f"❌ Transcription failed. Output file not found at expected location or source directory.", file=sys.stderr)
            return None

def summarize_text(text_to_summarize):
    """Summarizes the given text using Ollama."""
    if not text_to_summarize:
        print("⚠️ Warning: No text provided for summarization.", file=sys.stderr)
        return None

    print(f"\n🔄 Starting Summarization using Ollama ({config.OLLAMA_MODEL})")

    try:
        prompt = config.LLM_PROMPT.format(text=text_to_summarize)
    except KeyError:
        prompt_source = "config.py" if 'config' in sys.modules and hasattr(sys.modules['config'], 'LLM_PROMPT') else "domyślnych ustawień skryptu"
        current_prompt_value = config.LLM_PROMPT if hasattr(config, 'LLM_PROMPT') else "[Nie zdefiniowano LLM_PROMPT]"

        print(f"❌ Error: LLM_PROMPT w konfiguracji ({prompt_source}) nie zawiera wymaganego placeholdera '{{text}}'.", file=sys.stderr)
        print(f"   Aktualna wartość LLM_PROMPT: \"{current_prompt_value}\"", file=sys.stderr)
        print("   Proszę edytować odpowiednią konfigurację i dodać '{text}' w miejscu, gdzie ma być wstawiony transkrybowany tekst.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error formatting LLM prompt: {e}", file=sys.stderr)
        return None

    command = ["ollama", "run", config.OLLAMA_MODEL]

    process = run_command(command, input_data=prompt, capture_output=True)

    if process and process.returncode == 0 and process.stdout:
        summary = process.stdout.strip()
        print("✅ Summarization successful.")
        return summary
    else:
        print(f"❌ Summarization failed. Exit code: {process.returncode if process else 'N/A'}", file=sys.stderr)
        if process and not process.stdout:
             print("   Reason: Ollama produced no output (stdout was empty).", file=sys.stderr)
        return None

def is_valid_url(text):
    """Basic check if a string looks like a URL."""
    return re.match(r'^https?://', text) is not None

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio (from file or YouTube URL) and summarize the text.",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument(
        "input_source",
        help="Path to the local input audio file (e.g., MP3, WAV)\n"
             "OR a YouTube video URL (e.g., 'https://www.youtube.com/watch?v=...')")
    parser.add_argument(
        "-o", "--output",
        help="Optional path to save the final summary text file.\n"
             "If not provided, a default name based on the input will be suggested.",
        default=None)

    args = parser.parse_args()
    input_value = args.input_source
    audio_path_to_transcribe = None
    downloaded_file_to_delete = None

    if is_valid_url(input_value):
        print(f"✅ Detected URL: {input_value}")
        downloaded_path = download_youtube_audio(input_value)
        if downloaded_path:
            audio_path_to_transcribe = downloaded_path
            downloaded_file_to_delete = downloaded_path
        else:
            print("❌ Error: Failed to download audio from the provided URL.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"✅ Treating input as local file path: {input_value}")
        local_path = Path(input_value)
        if not local_path.is_file():
            print(f"❌ Error: Input file not found at '{local_path}'", file=sys.stderr)
            sys.exit(1)
        audio_path_to_transcribe = local_path

    if not audio_path_to_transcribe:
         print("❌ Error: Could not determine a valid audio source.", file=sys.stderr)
         sys.exit(1)

    transcription_file_path = transcribe_audio(str(audio_path_to_transcribe))

    if downloaded_file_to_delete:
        print(f"\n🧹 Cleaning up temporary downloaded audio: {downloaded_file_to_delete}")
        try:
            os.remove(downloaded_file_to_delete)
            print(f"✅ Successfully deleted {downloaded_file_to_delete}")
        except OSError as e:
            print(f"⚠️ Warning: Could not delete temporary file {downloaded_file_to_delete}: {e}", file=sys.stderr)

    if not transcription_file_path:
        print("❌ Error: Transcription step failed. Exiting.", file=sys.stderr)
        sys.exit(1)

    print(f"\n📖 Reading transcription file: {transcription_file_path}")
    transcribed_text = ""
    try:
        with open(transcription_file_path, 'r', encoding='utf-8') as f:
            transcribed_text = f.read()
        print("✅ Transcription read successfully.")
    except FileNotFoundError:
        print(f"❌ Error: Transcription file '{transcription_file_path}' not found after supposedly being created!", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading transcription file: {e}", file=sys.stderr)
        sys.exit(1)

    summary = summarize_text(transcribed_text)

    if summary:
        print("\n--- Generated Summary ---")
        print(summary)
        print("-----------------------")

        output_path_provided = args.output
        summary_output_path = None

        if output_path_provided:
             summary_output_path = Path(output_path_provided)
        else:
             input_base_name = Path(input_value).stem if not is_valid_url(input_value) else transcription_file_path.stem.replace('_transcription', '')
             default_summary_path = Path(f"{input_base_name}.summary.txt")
             print(f"\n💡 Tip: Summary not saved automatically.")
             print(f"   To save, use the -o flag, e.g.: -o \"{default_summary_path}\"")

        if summary_output_path:
            print(f"\n💾 Saving summary to: {summary_output_path}")
            try:
                summary_output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(summary_output_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f"✅ Summary saved successfully to {summary_output_path}")
            except Exception as e:
                print(f"❌ Error saving summary file: {e}", file=sys.stderr)
    else:
        print("\n❌ Summary generation failed or produced no output.", file=sys.stderr)

    print("\n✨ Process complete.")

if __name__ == "__main__":
    main()