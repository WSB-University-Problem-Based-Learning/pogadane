import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import subprocess
import sys
import os
import argparse
from pathlib import Path
import shlex
import re
import importlib.util

# Wersja Alpha v0.1.8

class DefaultConfig:
    FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"
    YT_DLP_EXE = "yt-dlp.exe"
    WHISPER_LANGUAGE = "Polish"
    WHISPER_MODEL = "turbo"
    ENABLE_SPEAKER_DIARIZATION = False
    DIARIZE_METHOD = "pyannote_v3.1"
    DIARIZE_SPEAKER_PREFIX = "MÓWCA"
    SUMMARY_PROVIDER = "ollama"
    SUMMARY_LANGUAGE = "Polish"
    LLM_PROMPT_TEMPLATES = {
        "Standardowy": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:",
        "Elementy Akcji": "Przeanalizuj poniższy tekst i wypisz wyłącznie listę zadań do wykonania (action items), przypisanych osób (jeśli wspomniano) i terminów (jeśli wspomniano) w formie punktów.",
        "Główne Tematy": "Wylistuj główne tematy poruszone w poniższej dyskusji.",
        "Kluczowe Pytania": "Na podstawie poniższej dyskusji, sformułuj listę kluczowych pytań, które pozostały bez odpowiedzi lub wymagają dalszej analizy.",
        "ELI5": "Wyjaśnij główne tezy i wnioski z poniższego tekstu w maksymalnie prosty sposób, unikając skomplikowanego słownictwa."
    }
    LLM_PROMPT_TEMPLATE_NAME = "Standardowy"
    LLM_PROMPT = "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:"
    OLLAMA_MODEL = "gemma3:4b"
    GOOGLE_API_KEY = ""
    GOOGLE_GEMINI_MODEL = "gemini-1.5-flash-latest"
    TRANSCRIPTION_FORMAT = "txt"
    DOWNLOADED_AUDIO_FILENAME = "downloaded_audio.mp3"
    DEBUG_MODE = False

class DummyConfigCli:
    pass

def _resolve_project_root():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]

CONFIG_PATH = _resolve_project_root() / ".config" / "config.py"

def _iter_default_config_items():
    for attr, value in vars(DefaultConfig).items():
        if not attr.startswith("__"):
            yield attr, value

def _load_config_module():
    try:
        if not CONFIG_PATH.exists():
            raise FileNotFoundError(CONFIG_PATH)
        spec = importlib.util.spec_from_file_location("config", CONFIG_PATH)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules['config'] = module
            spec.loader.exec_module(module)
            print("✅ Konfiguracja CLI załadowana z .config/config.py.")
            return module
        raise ImportError(f"Nie można utworzyć specyfikacji modułu dla {CONFIG_PATH}")
    except Exception as exc:
        print(f"⚠️ Ostrzeżenie CLI: Używam wartości domyślnych konfiguracji ({exc}).", file=sys.stderr)
        fallback = DummyConfigCli()
        for key, value in _iter_default_config_items():
            setattr(fallback, key, value)
        return fallback

config = _load_config_module()

genai = None

def ensure_google_ai_available():
    global genai
    if genai is None:
        try: import google.generativeai as google_genai; genai = google_genai; print("✅ Biblioteka google-generativeai załadowana.")
        except ImportError: print("❌ Błąd: Biblioteka google.generativeai nie jest zainstalowana.", file=sys.stderr); return False
    return True

def run_command(command_list, input_data=None, capture_output=True, text_encoding='utf-8'):
    debug_mode = getattr(config, 'DEBUG_MODE', DefaultConfig.DEBUG_MODE)
    cmd_str = ' '.join(shlex.quote(str(s)) for s in command_list)
    if debug_mode: print(f"🐞 DEBUG: Running command: {cmd_str}\n🐞 DEBUG: Input (100char): {input_data[:100]}..." if input_data else "🐞 DEBUG: No input data")
    else: print(f"\n▶️ Running command: {cmd_str}")
    startupinfo = None
    if os.name == 'nt': startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW; startupinfo.wShowWindow = subprocess.SW_HIDE
    try:
        process = subprocess.run(command_list, input=input_data, capture_output=capture_output, text=True, encoding=text_encoding, check=False, shell=False, startupinfo=startupinfo)
        if debug_mode:
            print(f"☑️ CMD exit code: {process.returncode}")
            if process.stdout: print(f"--- stdout ---\n{process.stdout.strip()}\n--------------")
            if process.stderr: print(f"--- stderr ---\n{process.stderr.strip()}\n--------------", file=sys.stderr)
        else:
            if process.returncode == 0: print(f"☑️ CMD finished successfully (code: {process.returncode})")
            else: print(f"⚠️ CMD Warning: Exited with {process.returncode}.", file=sys.stderr); print(f"--- stderr for error ---\n{process.stderr.strip()}\n------------------------", file=sys.stderr) if process.stderr else None
        return process
    except FileNotFoundError: print(f"❌ Error: CMD not found: {command_list[0]}", file=sys.stderr); return None
    except Exception as e: print(f"❌ Unexpected CMD error '{command_list[0]}': {e}", file=sys.stderr); return None

def get_unique_download_filename(url):
    base_name = getattr(config, 'DOWNLOADED_AUDIO_FILENAME', DefaultConfig.DOWNLOADED_AUDIO_FILENAME)
    base_stem, base_suffix = Path(base_name).stem, Path(base_name).suffix or ".mp3"
    try:
        url_part_match = re.search(r"v=([^&]+)", url)
        unique_id = url_part_match.group(1) if url_part_match else (Path(url.split("?")[0]).name or os.urandom(4).hex())
        return f"{base_stem}_{re.sub(r'[\\/*?:\"<>|]', '', unique_id)}{base_suffix}"
    except: return f"{base_stem}_{os.urandom(4).hex()}{base_suffix}"

def download_youtube_audio(url, target_dir_path):
    print(f"\n🔄 Downloading YouTube Audio: {url}")
    yt_dlp_exe = getattr(config, 'YT_DLP_EXE', DefaultConfig.YT_DLP_EXE)
    temp_audio_filename = get_unique_download_filename(url)
    download_path = target_dir_path / temp_audio_filename
    print(f"   Using yt-dlp: {yt_dlp_exe}, Output: {download_path}")
    command = [yt_dlp_exe, "-x", "--audio-format", "mp3", "--force-overwrite", "-o", str(download_path), url]
    process = run_command(command, capture_output=True)
    dl_ok = download_path.is_file() and download_path.stat().st_size > 0
    if process and process.returncode == 0 and dl_ok: print(f"✅ Download successful: {download_path}"); return download_path
    elif process and process.returncode != 0 and dl_ok: print(f"⚠️ yt-dlp warning (code {process.returncode}), but file created: {download_path}. Proceeding.", file=sys.stderr); return download_path
    else:
        print(f"❌ Download failed for {url}. Code: {process.returncode if process else 'N/A'}", file=sys.stderr)
        if download_path.exists() and not dl_ok: print(f"   Output '{download_path}' empty/invalid.", file=sys.stderr)
        elif not download_path.exists(): print(f"   Output '{download_path}' not created.", file=sys.stderr)
        if download_path.exists():
            try: os.remove(download_path); print(f"   Removed temp file: {download_path}")
            except OSError as e: print(f"   Warning: Could not remove temp file {download_path}: {e}", file=sys.stderr)
        return None

def transcribe_audio(audio_path_str, original_input_name_stem):
    audio_path = Path(audio_path_str)
    if not audio_path.is_file(): print(f"❌ Error: Audio file not found: '{audio_path}' for '{original_input_name_stem}'", file=sys.stderr); return None
    fmt = getattr(config, 'TRANSCRIPTION_FORMAT', DefaultConfig.TRANSCRIPTION_FORMAT)
    trans_out_path = audio_path.parent / f"{original_input_name_stem}_transcription.{fmt}"
    print(f"\n🔄 Transcribing: {audio_path} (Original: {original_input_name_stem})")
    fw_exe = getattr(config, 'FASTER_WHISPER_EXE', DefaultConfig.FASTER_WHISPER_EXE)
    print(f"   Using FW: {fw_exe}, Expected output: {trans_out_path.name} in {audio_path.parent}")
    cmd = [fw_exe, str(audio_path), "--language", getattr(config, 'WHISPER_LANGUAGE', DefaultConfig.WHISPER_LANGUAGE), "--model", getattr(config, 'WHISPER_MODEL', DefaultConfig.WHISPER_MODEL), "--output_format", fmt, "--output_dir", str(audio_path.parent)]
    use_diarize = getattr(config, 'ENABLE_SPEAKER_DIARIZATION', DefaultConfig.ENABLE_SPEAKER_DIARIZATION)
    if use_diarize:
        print("   Diarization: ENABLED"); cmd.extend(["--diarize", getattr(config, 'DIARIZE_METHOD', DefaultConfig.DIARIZE_METHOD)])
        prefix = getattr(config, 'DIARIZE_SPEAKER_PREFIX', DefaultConfig.DIARIZE_SPEAKER_PREFIX)
        if prefix: cmd.extend(["--speaker", prefix])
    else: print("   Diarization: DISABLED")
    process = run_command(cmd, capture_output=True)
    fw_stem = audio_path.stem; found_files = list(audio_path.parent.glob(f"{fw_stem}*.{fmt}"))
    if not found_files: print(f"❌ Transcription failed for '{original_input_name_stem}'. No file like '{fw_stem}*.{fmt}' in '{audio_path.parent}'.", file=sys.stderr); return None
    chosen_file = None
    if use_diarize:
        spk_pref_low = getattr(config, 'DIARIZE_SPEAKER_PREFIX', "").lower()
        for f in found_files:
            if any(k in f.name.lower() for k in ["speaker", "diarize", spk_pref_low] if spk_pref_low): chosen_file = f; break
    if not chosen_file: chosen_file = audio_path.parent / f"{fw_stem}.{fmt}" if (audio_path.parent / f"{fw_stem}.{fmt}") in found_files else found_files[0]
    print(f"ℹ️ FW output: {chosen_file}")
    try:
        if chosen_file.resolve() != trans_out_path.resolve():
            if trans_out_path.exists(): trans_out_path.unlink()
            final_path = chosen_file.rename(trans_out_path)
        else: final_path = trans_out_path
        print(f"✅ Transcription finalized: {final_path}"); return final_path
    except OSError as e: print(f"⚠️ Warn: Rename failed '{chosen_file}' to '{trans_out_path}': {e}. Using original.", file=sys.stderr); return chosen_file

def summarize_text(text_to_summarize, original_input_name_stem=""):
    if not text_to_summarize: print(f"⚠️ Warn: No text for summarization (Input: {original_input_name_stem}).", file=sys.stderr); return None
    provider = getattr(config, 'SUMMARY_PROVIDER', DefaultConfig.SUMMARY_PROVIDER).lower()
    templates = getattr(config, 'LLM_PROMPT_TEMPLATES', DefaultConfig.LLM_PROMPT_TEMPLATES)
    tpl_name = getattr(config, 'LLM_PROMPT_TEMPLATE_NAME', DefaultConfig.LLM_PROMPT_TEMPLATE_NAME)
    prompt_core = templates.get(tpl_name) or getattr(config, 'LLM_PROMPT', DefaultConfig.LLM_PROMPT)
    print(f"ℹ️ Using template '{tpl_name if templates.get(tpl_name) else 'custom LLM_PROMPT'}' for '{original_input_name_stem}'.")
    prompt_core = prompt_core.replace("{text}", "").replace("{Text}", "").strip()
    lang = getattr(config, 'SUMMARY_LANGUAGE', DefaultConfig.SUMMARY_LANGUAGE)
    summary_result = None; print("--- POCZĄTEK STRESZCZENIA ---") # Znacznik dla GUI
    if provider == "ollama":
        model = getattr(config, 'OLLAMA_MODEL', DefaultConfig.OLLAMA_MODEL)
        print(f"\n🔄 Summarizing '{original_input_name_stem}' with Ollama ({model})")
        prompt_data = f"Please summarize the following text in {lang}. {prompt_core}\n\nText to summarize:\n{text_to_summarize}"
        cmd = ["ollama", "run", model]; proc = run_command(cmd, input_data=prompt_data, capture_output=True)
        if proc and proc.returncode == 0 and proc.stdout: summary_result = proc.stdout.strip(); print(f"✅ Summary OK for '{original_input_name_stem}' (Ollama).")
        else: print(f"❌ Summary failed for '{original_input_name_stem}' (Ollama). Code: {proc.returncode if proc else 'N/A'}", file=sys.stderr); print(f"   Reason: Ollama gave no output.{' Code 0.' if proc and proc.returncode==0 else ''}", file=sys.stderr) if proc and not proc.stdout else None
    elif provider == "google":
        if ensure_google_ai_available():
            api_key = getattr(config, 'GOOGLE_API_KEY', DefaultConfig.GOOGLE_API_KEY)
            model_name = getattr(config, 'GOOGLE_GEMINI_MODEL', DefaultConfig.GOOGLE_GEMINI_MODEL)
            if not api_key: print(f"❌ Error: GOOGLE_API_KEY not set for '{original_input_name_stem}'.", file=sys.stderr)
            else:
                print(f"\n🔄 Summarizing '{original_input_name_stem}' with Google Gemini ({model_name})")
                try:
                    genai.configure(api_key=api_key); model_obj = genai.GenerativeModel(model_name)
                    prompt_data = f"Please summarize the following text in {lang}. {prompt_core}\n\nText to summarize:\n{text_to_summarize}"
                    print(f"   Sending prompt to Google for '{original_input_name_stem}'...")
                    resp = model_obj.generate_content(prompt_data)
                    if resp.parts: summary_result = "".join(p.text for p in resp.parts if hasattr(p, 'text')).strip(); print(f"✅ Summary OK for '{original_input_name_stem}' (Google).")
                    elif resp.prompt_feedback and resp.prompt_feedback.block_reason: print(f"❌ Summary blocked by Google for '{original_input_name_stem}'. Reason: {resp.prompt_feedback.block_reason}", file=sys.stderr)
                    else: print(f"❌ Summary failed for '{original_input_name_stem}' (Google). No content/unknown error.", file=sys.stderr)
                except Exception as e: print(f"❌ Google API error for '{original_input_name_stem}': {e}", file=sys.stderr)
    else: print(f"❌ Error: Unknown provider '{provider}' for '{original_input_name_stem}'.", file=sys.stderr)
    if summary_result: print(summary_result) # Drukuj streszczenie do konsoli (dla GUI)
    print("--- KONIEC STRESZCZENIA ---") # Znacznik dla GUI
    return summary_result

def is_valid_url(text): return re.match(r'^https?://', text) is not None
def get_input_name_stem(src_str):
    if is_valid_url(src_str):
        try:
            yt_match = re.search(r"(?:v=|\/embed\/|\/watch\?v=|\.be\/)([a-zA-Z0-9_-]{11})", src_str)
            if yt_match: return f"youtube_{yt_match.group(1)}"
            safe_name = re.sub(r'[\\/*?:"<>|]', "", Path(src_str.split("?")[0]).name)
            return safe_name if safe_name else f"url_{os.urandom(4).hex()}"
        except: return f"url_{os.urandom(4).hex()}"
    else: return Path(src_str).stem

def _try_cleanup_temp_files(audio_file, trans_file):
    if audio_file and audio_file.exists():
        print(f"\n🧹 Cleaning up temp audio: {audio_file.name}")
        try: os.remove(audio_file); print(f"✅ Deleted {audio_file.name}")
        except OSError as e: print(f"⚠️ Warn: Could not delete {audio_file.name}: {e}", file=sys.stderr)
    if trans_file and trans_file.exists():
        print(f"🧹 Cleaning up temp transcript: {trans_file.name}")
        try: os.remove(trans_file); print(f"✅ Deleted {trans_file.name}")
        except OSError as e: print(f"⚠️ Warn: Could not delete {trans_file.name}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Transcribe & Summarize audio/YouTube.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_sources", nargs='*', default=[], help="File(s) or URL(s). Omit if using --batch-file.")
    parser.add_argument("-o", "--output", help="Summary output. File if 1 input & not dir. Else, DIR for summaries.", default=None)
    parser.add_argument("-a", "--batch-file", help="File with input sources (one per line).", default=None)
    diar_grp = parser.add_mutually_exclusive_group()
    diar_grp.add_argument("--diarize", action='store_true', help="Enable diarization.")
    diar_grp.add_argument("--no-diarize", action='store_true', help="Disable diarization.")
    args = parser.parse_args()
    
    sources = []
    if args.batch_file:
        print(f"ℹ️ Reading from batch: {args.batch_file}")
        try:
            with open(args.batch_file, 'r', encoding='utf-8') as f: sources.extend(l.strip() for l in f if l.strip() and not l.startswith('#'))
            if not sources: print(f"⚠️ Batch file '{args.batch_file}' empty/all comments.", file=sys.stderr)
        except FileNotFoundError: print(f"❌ Error: Batch file not found: {args.batch_file}", file=sys.stderr); sys.exit(1)
        except Exception as e: print(f"❌ Error reading batch '{args.batch_file}': {e}", file=sys.stderr); sys.exit(1)
    sources.extend(args.input_sources)
    if not sources: print("❌ Error: No input sources.", file=sys.stderr); parser.print_help(); sys.exit(1)

    diar_base = getattr(config, 'ENABLE_SPEAKER_DIARIZATION', DefaultConfig.ENABLE_SPEAKER_DIARIZATION)
    diar_src = "config" if hasattr(config, 'ENABLE_SPEAKER_DIARIZATION') else "default"
    if args.diarize: setattr(config, 'ENABLE_SPEAKER_DIARIZATION', True); print("ℹ️ Diarization: ENABLED (CLI).")
    elif args.no_diarize: setattr(config, 'ENABLE_SPEAKER_DIARIZATION', False); print("ℹ️ Diarization: DISABLED (CLI).")
    else: setattr(config, 'ENABLE_SPEAKER_DIARIZATION', diar_base); print(f"ℹ️ Diarization from {diar_src}: {'ENABLED' if config.ENABLE_SPEAKER_DIARIZATION else 'DISABLED'}.")
    if config.ENABLE_SPEAKER_DIARIZATION:
        for k, v_def in [('DIARIZE_METHOD', DefaultConfig.DIARIZE_METHOD), ('DIARIZE_SPEAKER_PREFIX', DefaultConfig.DIARIZE_SPEAKER_PREFIX)]:
            if not hasattr(config, k): setattr(config, k, v_def)
    
    out_dir_sum, single_out_file_sum = None, None
    # Poprawka UnboundLocalError: zdefiniuj scr_dir przed użyciem
    scr_dir = Path(__file__).parent.resolve()
    temp_dir = scr_dir / "pogadane_temp_audio"
    try: temp_dir.mkdir(parents=True, exist_ok=True); print(f"ℹ️ Temp audio in: {temp_dir}")
    except OSError as e: print(f"❌ Error creating temp dir '{temp_dir}': {e}. Exiting.", file=sys.stderr); sys.exit(1)

    if args.output:
        out_path = Path(args.output)
        # Jeśli jest więcej niż jedno źródło LUB jeśli ścieżka -o jest katalogiem LUB jeśli ścieżka -o nie ma rozszerzenia (traktujemy jak katalog)
        if len(sources) > 1 or out_path.is_dir() or (not out_path.suffix and not out_path.exists()): # Dodano warunek not out_path.exists() dla nowych katalogów
            out_dir_sum = out_path
        else: # W przeciwnym razie to pojedynczy plik wyjściowy
            single_out_file_sum = out_path
            
        if out_dir_sum:
            try: out_dir_sum.mkdir(parents=True, exist_ok=True); print(f"ℹ️ Summaries to dir: {out_dir_sum.resolve()}")
            except OSError as e: print(f"❌ Error creating output dir '{out_dir_sum}': {e}", file=sys.stderr); sys.exit(1)
        elif single_out_file_sum:
            try: single_out_file_sum.parent.mkdir(parents=True, exist_ok=True); print(f"ℹ️ Summary to file: {single_out_file_sum.resolve()}")
            except OSError as e: print(f"❌ Error creating parent for '{single_out_file_sum}': {e}", file=sys.stderr); sys.exit(1)

    for idx, src_str in enumerate(sources):
        print(f"\n--- Processing {idx + 1}/{len(sources)}: {src_str} ---")
        stem = get_input_name_stem(src_str)
        audio_to_trans, temp_file_to_del = None, None
        if is_valid_url(src_str):
            print(f"✅ URL: {src_str}"); dl_path = download_youtube_audio(src_str, temp_dir)
            if dl_path: audio_to_trans, temp_file_to_del = dl_path, dl_path
            else: print(f"❌ Download failed for {src_str}. Skipping.", file=sys.stderr); continue
        else:
            print(f"✅ Local file: {src_str}"); loc_path = Path(src_str)
            if not loc_path.is_file(): print(f"❌ File not found: '{loc_path}'. Skipping.", file=sys.stderr); continue
            try:
                temp_cp_path = temp_dir / f"{stem}_{os.urandom(4).hex()}{loc_path.suffix}"
                import shutil; shutil.copy2(loc_path, temp_cp_path)
                audio_to_trans, temp_file_to_del = temp_cp_path, temp_cp_path
                print(f"   Copied to temp: {audio_to_trans}")
            except Exception as e: print(f"❌ Error copying '{loc_path}' to temp: {e}. Skipping.", file=sys.stderr); continue
        if not audio_to_trans: print(f"❌ No valid audio for '{src_str}'. Skipping.", file=sys.stderr); continue
        
        trans_path = transcribe_audio(str(audio_to_trans), stem)
        if not trans_path: print(f"❌ Transcription failed for '{src_str}'. Skipping.", file=sys.stderr); _try_cleanup_temp_files(temp_file_to_del, None); continue
        
        print("--- POCZĄTEK TRANSKRYPCJI ---") # Znacznik dla GUI
        txt = ""
        try:
            with open(trans_path, 'r', encoding='utf-8') as f: txt = f.read()
            print(txt) # Drukuj transkrypcję (dla logu i GUI)
            print(f"✅ Transcript read for '{stem}'.")
        except FileNotFoundError:
            print(f"❌ Transcript '{trans_path}' disappeared! Skipping.", file=sys.stderr)
            _try_cleanup_temp_files(temp_file_to_del, trans_path)
            print("--- KONIEC TRANSKRYPCJI ---") # Zamknij znacznik mimo błędu
            continue
        except Exception as e:
            print(f"❌ Error reading '{trans_path}': {e}. Skipping.", file=sys.stderr)
            _try_cleanup_temp_files(temp_file_to_del, trans_path)
            print("--- KONIEC TRANSKRYPCJI ---") # Zamknij znacznik mimo błędu
            continue
        print("--- KONIEC TRANSKRYPCJI ---") # Znacznik dla GUI
        
        summary_text = summarize_text(txt, stem) # Ta funkcja drukuje własne znaczniki i zawartość
        
        if summary_text: # Jeśli summarize_text zwróciło coś (a nie None)
            # Zapisywanie do pliku, jeśli użytkownik podał -o
            sum_out_path = None
            if out_dir_sum: sum_out_path = out_dir_sum / f"{stem}.summary.txt"
            elif single_out_file_sum: sum_out_path = single_out_file_sum
            if sum_out_path:
                print(f"\n💾 Saving summary for '{stem}' to: {sum_out_path}")
                try:
                    sum_out_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(sum_out_path, 'w', encoding='utf-8') as f: f.write(summary_text) # Zapisz tylko tekst streszczenia
                    print(f"✅ Summary saved: {sum_out_path}")
                except Exception as e: print(f"❌ Error saving summary for '{stem}' to '{sum_out_path}': {e}", file=sys.stderr)
        else: print(f"\n❌ Summary generation failed or produced no output for '{stem}'.", file=sys.stderr)
        
        _try_cleanup_temp_files(temp_file_to_del, trans_path)

    try:
        if temp_dir.exists() and not any(temp_dir.iterdir()): temp_dir.rmdir(); print(f"ℹ️ Cleaned empty temp dir: {temp_dir}")
    except OSError as e: print(f"⚠️ Warn: Could not remove temp dir {temp_dir}: {e}", file=sys.stderr)
    print("\n✨ All processing complete.")

if __name__ == "__main__":
    main()