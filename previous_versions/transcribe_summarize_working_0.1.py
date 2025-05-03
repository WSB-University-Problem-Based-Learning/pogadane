import subprocess
import sys
import os
import argparse
from pathlib import Path
import shlex # Used for safer command construction if needed, though list format is preferred
# Wersja Alpha v0.1.0
# --- Configuration ---
# Option 1: Assume faster-whisper-xxl.exe is in the current directory or PATH
FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
# Option 2: Specify the full path if needed (use raw string r"..." for Windows paths)
# FASTER_WHISPER_EXE = r"C:\path\to\your\faster-whisper-xxl.exe"

WHISPER_LANGUAGE = "Polish"
WHISPER_MODEL = "turbo"
OLLAMA_MODEL = "gemma3:4b"
TRANSCRIPTION_FORMAT = "txt" # Use 'txt' for easy reading by the script
# --- End Configuration ---

def run_command(command_list, input_data=None, capture_output=True, text_encoding='utf-8'):
    """Runs an external command safely."""
    print(f"\n▶️ Running command: {' '.join(command_list)}")
    try:
        # Pass input_data directly as string if text=True is used
        process = subprocess.run(
            command_list,
            input=input_data if input_data else None, # CORRECTED LINE: Removed .encode()
            capture_output=capture_output,
            text=True,  # Expects input as string, decodes stdout/stderr as text
            encoding=text_encoding, # Specify encoding for text mode
            check=False, # Don't raise exception on non-zero exit; we'll check manually
            shell=False # Recommended for security and cross-platform compatibility
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
    except TypeError as e: # Specifically catch the TypeError we saw
        print(f"❌ TypeError during subprocess interaction: {e}", file=sys.stderr)
        print("   This might indicate an issue with text=True vs input data type.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred while running the command: {e}", file=sys.stderr)
        return None

def transcribe_audio(audio_path_str):
    """Transcribes the audio file using Faster Whisper."""
    audio_path = Path(audio_path_str)
    if not audio_path.is_file():
        print(f"❌ Error: Audio file not found at '{audio_path}'", file=sys.stderr)
        return None

    # Determine expected transcription output path
    transcription_output_path = audio_path.with_suffix(f'.{TRANSCRIPTION_FORMAT}')

    print(f"\n🔄 Starting Transcription for: {audio_path}")
    print(f"   Expected output: {transcription_output_path}")

    # Construct the command arguments as a list
    command = [
        FASTER_WHISPER_EXE,
        str(audio_path), # Ensure path is a string
        "--language", WHISPER_LANGUAGE, # Użycie stałej
        "--model", WHISPER_MODEL, # Using 'turbo' as specified
        "--output_format", TRANSCRIPTION_FORMAT, # Użycie stałej
        # Add '--output_dir', '.' if you want output in the current dir instead of audio dir
    ]

    process = run_command(command, capture_output=True) # Capture output to check stderr

    # --- MODIFICATION START ---
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
        # Optionally add a check here for file size > 0 if needed
        # if transcription_output_path.stat().st_size > 0:
        #    return transcription_output_path
        # else:
        #    print(f"❌ Error: Transcription file exists but is empty.", file=sys.stderr)
        #    return None
        return transcription_output_path # Return path if file exists, regardless of exit code
    else:
        print(f"❌ Transcription failed. Output file not found.", file=sys.stderr)
        return None
    # --- MODIFICATION END ---
def summarize_text(text_to_summarize):
    """Summarizes the given text using Ollama."""
    if not text_to_summarize:
        print("⚠️ Warning: No text provided for summarization.", file=sys.stderr)
        return None

    print(f"\n🔄 Starting Summarization using Ollama ({OLLAMA_MODEL})")

    # Prepare the prompt for Ollama
    # Important: Ensure Ollama understands the instruction format.
    # This might need adjustment based on how gemma3:4b best handles instructions.
    prompt = f"Streść poniższy tekst po polsku:\n\n{text_to_summarize}"

    command = ["ollama", "run", OLLAMA_MODEL]

    process = run_command(command, input_data=prompt, capture_output=True)

    if process and process.returncode == 0:
        summary = process.stdout.strip()
        print("✅ Summarization successful.")
        return summary
    else:
        print(f"❌ Summarization failed. Exit code: {process.returncode if process else 'N/A'}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio and summarize the text.")
    parser.add_argument("audio_file", help="Path to the input audio file (e.g., MP3, WAV).")
    parser.add_argument("-o", "--output", help="Optional path to save the summary text file.", default=None)
    # Add argument for whisper executable path if needed
    # parser.add_argument("--whisper-exe", help="Path to faster-whisper-xxl.exe", default=FASTER_WHISPER_EXE)

    args = parser.parse_args()

    # --- Step 1: Transcribe ---
    transcription_file_path = transcribe_audio(args.audio_file)

    if not transcription_file_path:
        sys.exit(1) # Exit if transcription failed

    # --- Step 2: Read Transcription ---
    print(f"\n📖 Reading transcription file: {transcription_file_path}")
    try:
        with open(transcription_file_path, 'r', encoding='utf-8') as f:
            transcribed_text = f.read()
        print("✅ Transcription read successfully.")
    except FileNotFoundError:
        print(f"❌ Error: Transcription file '{transcription_file_path}' disappeared!", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading transcription file: {e}", file=sys.stderr)
        sys.exit(1)

    # Optional: Delete transcription file after reading if desired
    # print(f"   Deleting intermediate transcription file: {transcription_file_path}")
    # try:
    #     os.remove(transcription_file_path)
    # except OSError as e:
    #     print(f"⚠️ Warning: Could not delete transcription file {transcription_file_path}: {e}", file=sys.stderr)


    # --- Step 3: Summarize ---
    summary = summarize_text(transcribed_text)

    # --- Step 4: Output/Save Summary ---
    if summary:
        print("\n--- Generated Summary ---")
        print(summary)
        print("-----------------------")

        if args.output:
            summary_output_path = Path(args.output)
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
             # Determine a default summary filename based on audio input
            audio_path = Path(args.audio_file)
            default_summary_path = audio_path.with_suffix('.summary.txt')
            print(f"\n💡 Tip: You can save the summary by using the -o flag.")
            print(f"   Example: python your_script_name.py \"{args.audio_file}\" -o \"{default_summary_path}\"")

    else:
        print("\n❌ Summary generation failed or produced no output.", file=sys.stderr)
        sys.exit(1)

    print("\n✨ Process complete.")

if __name__ == "__main__":
    main()