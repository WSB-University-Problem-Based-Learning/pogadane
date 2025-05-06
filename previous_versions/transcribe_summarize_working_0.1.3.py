import subprocess
import sys
import os
import argparse
from pathlib import Path
import shlex # Used for safer command construction if needed, though list format is preferred
import re # Import regular expressions for URL validation (basic)

# Wersja Alpha v0.1.3 # <<< ZAKTUALIZOWANA WERSJA
# --- Configuration ---
# Option 1: Assume executables are in the current directory or PATH
FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
YT_DLP_EXE = "yt-dlp.exe" # Added for YouTube downloads
# Option 2: Specify the full path if needed (use raw string r"..." for Windows paths)
# FASTER_WHISPER_EXE = r"C:\path\to\your\faster-whisper-xxl.exe"
# YT_DLP_EXE = r"C:\path\to\your\yt-dlp.exe"

WHISPER_LANGUAGE = "Polish"
WHISPER_MODEL = "turbo"
OLLAMA_MODEL = "gemma3:4b"
# --- NEW CONSTANT START ---
# Prompt dla modelu językowego (Ollama). Musi zawierać placeholder {text}.
LLM_PROMPT = "Streść poniższy tekst po polsku, skupiając się na kluczowych wnioskach i decyzjach:\n\n{text}"
# --- NEW CONSTANT END ---
TRANSCRIPTION_FORMAT = "txt" # Use 'txt' for easy reading by the script
DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3" # Temporary filename for downloads
# --- End Configuration ---

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
        print("Ensure the executable is in your PATH or the correct directory.", file=sys.stderr)
        return None
    except TypeError as e:
        print(f"❌ TypeError during subprocess interaction: {e}", file=sys.stderr)
        print("   This might indicate an issue with text=True vs input data type.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred while running the command: {e}", file=sys.stderr)
        return None

# --- NEW FUNCTION START ---
def download_youtube_audio(url):
    """Downloads audio from a YouTube URL using yt-dlp."""
    print(f"\n🔄 Starting YouTube Audio Download for: {url}")
    print(f"   Using yt-dlp: {YT_DLP_EXE}")
    print(f"   Outputting to temporary file: {DOWNLOADED_AUDIO_FILENAME}")

    # Construct the command for yt-dlp
    # -x: Extract audio
    # --audio-format mp3: Convert to mp3
    # --force-overwrite: Overwrite the temp file if it exists
    # -o: Specify output filename template (using our constant)
    command = [
        YT_DLP_EXE,
        "-x", # Extract audio
        "--audio-format", "mp3",
        "--force-overwrite", # Overwrite temp file if needed
        "-o", DOWNLOADED_AUDIO_FILENAME, # Output to our defined temp file
        url # The YouTube URL to download
    ]

    process = run_command(command, capture_output=True)

    # Check if the command ran and if the output file exists
    download_path = Path(DOWNLOADED_AUDIO_FILENAME)
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
        # Attempt to clean up potentially empty file
        if download_path.exists():
            try:
                os.remove(download_path)
                print(f"   Removed potentially incomplete file: {download_path}")
            except OSError as e:
                print(f"   Warning: Could not remove incomplete file {download_path}: {e}", file=sys.stderr)
        return None
# --- NEW FUNCTION END ---


def transcribe_audio(audio_path_str):
    """Transcribes the audio file using Faster Whisper."""
    audio_path = Path(audio_path_str)
    if not audio_path.is_file():
        print(f"❌ Error: Audio file not found at '{audio_path}'", file=sys.stderr)
        return None

    # Determine expected transcription output path
    # Ensure output has a unique name based on the input, avoiding clashes if input is always 'downloaded_audio.mp3'
    base_name = audio_path.stem # Get filename without extension (e.g., 'downloaded_audio' or 'spotkanie')
    transcription_output_path = audio_path.with_name(f"{base_name}_transcription").with_suffix(f'.{TRANSCRIPTION_FORMAT}')


    print(f"\n🔄 Starting Transcription for: {audio_path}")
    print(f"   Using Faster Whisper: {FASTER_WHISPER_EXE}")
    print(f"   Expected output: {transcription_output_path}")

    # Construct the command arguments as a list
    command = [
        FASTER_WHISPER_EXE,
        str(audio_path),
        "--language", WHISPER_LANGUAGE,
        "--model", WHISPER_MODEL,
        "--output_format", TRANSCRIPTION_FORMAT,
        # Specify output directory and filename base to match our calculated path
        "--output_dir", str(transcription_output_path.parent),
        # Whisper adds the format suffix automatically, so we provide the base name
        # However, faster-whisper-xxl might just take the dir. Let's test with just dir.
        # If it outputs to the source dir, we'll need to adjust.
        # Update: Let's explicitly control the output dir, Whisper usually names the file based on input.
        # We will check for the existence of the calculated `transcription_output_path`.
    ]

    process = run_command(command, capture_output=True)

    # Check if the output file exists, even if there was an error code
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
        # Let's double-check if Whisper created the file in the *source* audio directory instead
        fallback_transcription_path = audio_path.with_suffix(f'.{TRANSCRIPTION_FORMAT}')
        if fallback_transcription_path.is_file():
             print(f"ℹ️ Info: Transcription file found in source directory instead: {fallback_transcription_path}")
             # Optionally move it to the desired location or just use this path
             # For simplicity, let's use it directly if found here.
             # Consider renaming it to match the expected pattern if needed later.
             return fallback_transcription_path
        else:
            print(f"❌ Transcription failed. Output file not found at expected location or source directory.", file=sys.stderr)
            return None

def summarize_text(text_to_summarize):
    """Summarizes the given text using Ollama."""
    if not text_to_summarize:
        print("⚠️ Warning: No text provided for summarization.", file=sys.stderr)
        return None

    print(f"\n🔄 Starting Summarization using Ollama ({OLLAMA_MODEL})")

    # --- MODIFICATION START ---
    # Use the configured LLM_PROMPT constant.
    # Use .format() to insert the transcription into the prompt template.
    try:
        prompt = LLM_PROMPT.format(text=text_to_summarize)
    except KeyError:
        # Fallback or error if the placeholder is missing in the constant
        print(f"❌ Error: LLM_PROMPT constant in the script configuration is missing the required '{{text}}' placeholder.", file=sys.stderr)
        print(f"   Current LLM_PROMPT value: \"{LLM_PROMPT}\"", file=sys.stderr)
        print("   Please edit the script and add '{text}' where the transcribed text should be inserted.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error formatting LLM prompt: {e}", file=sys.stderr)
        return None
    # --- MODIFICATION END ---

    command = ["ollama", "run", OLLAMA_MODEL]

    process = run_command(command, input_data=prompt, capture_output=True)

    if process and process.returncode == 0 and process.stdout: # Check stdout has content
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
    # Simple check for common URL patterns. Can be made more robust.
    return re.match(r'^https?://', text) is not None

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio (from file or YouTube URL) and summarize the text.",
        formatter_class=argparse.RawTextHelpFormatter # Nicer help text formatting
        )
    # --- ARGUMENT PARSING MODIFICATION ---
    parser.add_argument(
        "input_source",
        help="Path to the local input audio file (e.g., MP3, WAV)\n"
             "OR a YouTube video URL (e.g., 'https://www.youtube.com/watch?v=...')")
    parser.add_argument(
        "-o", "--output",
        help="Optional path to save the final summary text file.\n"
             "If not provided, a default name based on the input will be suggested.",
        default=None)
    # --- END ARGUMENT PARSING MODIFICATION ---

    args = parser.parse_args()
    input_value = args.input_source
    audio_path_to_transcribe = None
    downloaded_file_to_delete = None # Keep track if we downloaded a file

    # --- INPUT HANDLING LOGIC ---
    if is_valid_url(input_value):
        print(f"✅ Detected URL: {input_value}")
        # Attempt to download audio from URL
        downloaded_path = download_youtube_audio(input_value)
        if downloaded_path:
            audio_path_to_transcribe = downloaded_path
            downloaded_file_to_delete = downloaded_path # Mark for deletion later
        else:
            print("❌ Error: Failed to download audio from the provided URL.", file=sys.stderr)
            sys.exit(1) # Exit if download failed
    else:
        # Assume it's a local file path
        print(f"✅ Treating input as local file path: {input_value}")
        local_path = Path(input_value)
        if not local_path.is_file():
            print(f"❌ Error: Input file not found at '{local_path}'", file=sys.stderr)
            sys.exit(1) # Exit if local file not found
        audio_path_to_transcribe = local_path
    # --- END INPUT HANDLING LOGIC ---


    # Proceed only if we have a valid audio path (either downloaded or local)
    if not audio_path_to_transcribe:
         print("❌ Error: Could not determine a valid audio source.", file=sys.stderr)
         sys.exit(1)


    # --- Step 1: Transcribe ---
    # Pass the determined audio path (could be original or downloaded)
    transcription_file_path = transcribe_audio(str(audio_path_to_transcribe))


    # --- Cleanup Downloaded File (if any) ---
    # Delete the temporary audio file *after* transcription attempt (success or fail)
    if downloaded_file_to_delete:
        print(f"\n🧹 Cleaning up temporary downloaded audio: {downloaded_file_to_delete}")
        try:
            os.remove(downloaded_file_to_delete)
            print(f"✅ Successfully deleted {downloaded_file_to_delete}")
        except OSError as e:
            print(f"⚠️ Warning: Could not delete temporary file {downloaded_file_to_delete}: {e}", file=sys.stderr)
    # --- End Cleanup ---

    # Exit if transcription failed
    if not transcription_file_path:
        print("❌ Error: Transcription step failed. Exiting.", file=sys.stderr)
        sys.exit(1)

    # --- Step 2: Read Transcription ---
    print(f"\n📖 Reading transcription file: {transcription_file_path}")
    transcribed_text = "" # Initialize
    try:
        with open(transcription_file_path, 'r', encoding='utf-8') as f:
            transcribed_text = f.read()
        print("✅ Transcription read successfully.")
        # Optional: Delete transcription file now if no longer needed
        # print(f"   Deleting intermediate transcription file: {transcription_file_path}")
        # try:
        #     os.remove(transcription_file_path)
        # except OSError as e:
        #     print(f"⚠️ Warning: Could not delete transcription file {transcription_file_path}: {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"❌ Error: Transcription file '{transcription_file_path}' not found after supposedly being created!", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading transcription file: {e}", file=sys.stderr)
        sys.exit(1)


    # --- Step 3: Summarize ---
    summary = summarize_text(transcribed_text)

    # --- Step 4: Output/Save Summary ---
    if summary:
        print("\n--- Generated Summary ---")
        print(summary)
        print("-----------------------")

        output_path_provided = args.output
        summary_output_path = None

        if output_path_provided:
             summary_output_path = Path(output_path_provided)
        else:
            # Determine a default summary filename based on audio input
            # Use the *original* input name's stem if possible, or the transcription file's base
             input_base_name = Path(input_value).stem if not is_valid_url(input_value) else transcription_file_path.stem.replace('_transcription', '')
             default_summary_path = Path(f"{input_base_name}.summary.txt") # Place in current dir by default
             print(f"\n💡 Tip: Summary not saved automatically.")
             print(f"   To save, use the -o flag, e.g.: -o \"{default_summary_path}\"")
             # We don't save automatically if -o is not used

        if summary_output_path:
            print(f"\n💾 Saving summary to: {summary_output_path}")
            try:
                # Ensure parent directory exists
                summary_output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(summary_output_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f"✅ Summary saved successfully to {summary_output_path}")
            except Exception as e:
                print(f"❌ Error saving summary file: {e}", file=sys.stderr)

    else:
        print("\n❌ Summary generation failed or produced no output.", file=sys.stderr)
        # Decide if this should be a critical error
        # sys.exit(1) # Uncomment if summarization failure should stop the script with error status

    print("\n✨ Process complete.")

if __name__ == "__main__":
    main()