import ttkbootstrap as ttk
from ttkbootstrap.constants import X, BOTH
from tkinter import filedialog, messagebox
import threading
import queue
import subprocess
import sys
import os
import re
from pathlib import Path
import importlib.util

# --- Load config.py robustly ---
config_path = os.path.join(os.path.dirname(__file__), "config.py")
default_config_values = {
    "FASTER_WHISPER_EXE": "faster-whisper-xxl.exe",
    "YT_DLP_EXE": "yt-dlp.exe",
    "WHISPER_LANGUAGE": "Polish",
    "WHISPER_MODEL": "turbo",
    "ENABLE_SPEAKER_DIARIZATION": False,
    "DIARIZE_METHOD": "pyannote_v3.1",
    "DIARIZE_SPEAKER_PREFIX": "MÓWCA",
    "OLLAMA_MODEL": "gemma3:4b",
    "LLM_PROMPT": "Streść poniższy tekst po polsku, skupiając się na kluczowych wnioskach i decyzjach:\n\n{text}",
    "TRANSCRIPTION_FORMAT": "txt",
    "DOWNLOADED_AUDIO_FILENAME": "downloaded_audio.mp3",
}

config_module = None
try:
    spec = importlib.util.spec_from_file_location("config", config_path)
    if spec and spec.loader:
        config_module = importlib.util.module_from_spec(spec)
        sys.modules['config'] = config_module # Add to sys.modules before exec
        spec.loader.exec_module(config_module)
        print("✅ Konfiguracja GUI załadowana z pliku config.py.")
    else:
        raise ImportError("Nie można utworzyć specyfikacji modułu lub loader jest None.")
except ImportError:
    print("⚠️ Ostrzeżenie GUI: Plik konfiguracyjny config.py nie został znaleziony lub jest błędny.")
    print("   GUI użyje wartości domyślnych.")
    # Create a dummy config module with default values
    class DummyConfig:
        pass
    config_module = DummyConfig()
    for key, value in default_config_values.items():
        setattr(config_module, key, value)
except Exception as e:
    print(f"❌ Błąd podczas ładowania config.py w GUI: {e}")
    print("   GUI użyje wartości domyślnych.")
    class DummyConfig:
        pass
    config_module = DummyConfig()
    for key, value in default_config_values.items():
        setattr(config_module, key, value)


# --- Helpers ---
def strip_ansi(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return re.sub(ansi_escape, "", text)

def insert_with_markdown(widget, text):
    widget.config(state="normal")
    widget.delete("1.0", "end")
    widget.tag_configure("bold", font=("Segoe UI Emoji", 10, "bold"))
    for line in text.splitlines():
        parts = re.split(r"(\*\*.*?\*\*)", line)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                widget.insert("end", part[2:-2], "bold")
            else:
                widget.insert("end", part)
        widget.insert("end", "\n")
    widget.config(state="disabled")

def extract_transcription_and_summary(text):
    transcription = re.search(r"Starting sequential.*?\n(.*?)Transcription speed:", text, re.DOTALL)
    if not transcription: # Fallback for cases where "Starting sequential" might be missing
        transcription = re.search(r"✅ Transcription read successfully\.\n(.*?)(?=\n--- Generated Summary ---|\n✨ Process complete)", text, re.DOTALL)

    summary = re.search(r"--- Generated Summary ---\s*(.*?)\s*-{3,}", text, re.DOTALL)
    return (transcription.group(1).strip() if transcription else ""), (summary.group(1).strip() if summary else "")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event):
        if self.tip:
            return
        bbox = self.widget.bbox("insert") or (0, 0, 0, 0)
        x_bbox, y_bbox, _, _ = bbox # Corrected variable names
        x = self.widget.winfo_rootx() + x_bbox + 20 # Use bbox x
        y = self.widget.winfo_rooty() + y_bbox + 20 # Use bbox y

        self.tip = tw = ttk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 9))
        label.pack(ipadx=1)


    def hide(self, event):
        if self.tip:
            self.tip.destroy()
            self.tip = None

class TranscriberApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("🎧 Pogadane GUI - Transcribe & Summarize")
        self.geometry("700x800") # Increased width for better layout
        self.resizable(True, True)

        # --- Determine base path for resources (like config.py) ---
        if getattr(sys, 'frozen', False): # Running as PyInstaller bundle
            self.base_path = Path(sys._MEIPASS)
        else: # Running as a normal script
            self.base_path = Path(__file__).parent

        self.config_file_path = self.base_path / "config.py"


        # Fixed top input section
        top_frame = ttk.Frame(self)
        top_frame.pack(padx=20, pady=(10, 0), fill=X)

        ttk.Label(top_frame, text="🎙️ Ścieżka pliku audio lub URL YouTube").pack(anchor='w', pady=(0, 5))

        input_row = ttk.Frame(top_frame)
        input_row.pack(fill=X)

        self.input_entry = ttk.Entry(input_row)
        self.input_entry.pack(side="left", fill=X, expand=True)

        browse_btn = ttk.Button(input_row, text="📂", width=3, command=self.browse_file, bootstyle="secondary")
        browse_btn.pack(side="left", padx=(5, 0))

        self.transcribe_button = ttk.Button(top_frame, text="🚀 Transkrybuj i Streść", command=self.run_script)
        self.transcribe_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(top_frame, mode="indeterminate", length=300, bootstyle="info-striped")
        # Progress bar is packed/unpacked in run_script

        # Tabs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(padx=20, pady=(0, 20), fill=BOTH, expand=True)

        # Console Tab
        self.console_tab = ttk.Frame(self.tabs)
        self.console_text = ttk.ScrolledText(self.console_tab, font=("Segoe UI Emoji", 10), wrap="word", state="disabled")
        self.console_text.pack(fill=BOTH, expand=True)
        console_btns = ttk.Frame(self.console_tab)
        console_btns.pack(pady=5, fill=X)
        ttk.Button(console_btns, text="💾 Zapisz Log", command=self.save_console_log).pack(side="left", padx=5)
        ttk.Button(console_btns, text="📁 Zapisz Log Jako...", command=self.save_console_log_as).pack(side="left", padx=5)
        self.tabs.add(self.console_tab, text="🖥️ Konsola")

        # Transcription Tab
        self.transcription_tab = ttk.Frame(self.tabs)
        self.transcription_text = ttk.ScrolledText(self.transcription_tab, font=("Segoe UI Emoji", 10), wrap="word", state="disabled")
        self.transcription_text.pack(fill=BOTH, expand=True)
        btns1 = ttk.Frame(self.transcription_tab)
        btns1.pack(pady=5, fill=X)
        ttk.Button(btns1, text="💾 Zapisz Transkrypcję", command=self.save_transcription).pack(side="left", padx=5)
        ttk.Button(btns1, text="📁 Zapisz Transkrypcję Jako...", command=self.save_transcription_as).pack(side="left", padx=5)
        self.tabs.add(self.transcription_tab, text="📝 Transkrypcja")

        # Summary Tab
        self.summary_tab = ttk.Frame(self.tabs)
        self.summary_text = ttk.ScrolledText(self.summary_tab, font=("Segoe UI Emoji", 10), wrap="word", state="disabled")
        self.summary_text.pack(fill=BOTH, expand=True)
        btns2 = ttk.Frame(self.summary_tab)
        btns2.pack(pady=5, fill=X)
        ttk.Button(btns2, text="💾 Zapisz Streszczenie", command=self.save_summary).pack(side="left", padx=5)
        ttk.Button(btns2, text="📁 Zapisz Streszczenie Jako...", command=self.save_summary_as).pack(side="left", padx=5)
        self.tabs.add(self.summary_tab, text="📌 Streszczenie")

        # --- Config Tab ---
        self.config_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.config_tab, text="⚙️ Konfiguracja")

        config_outer = ttk.Frame(self.config_tab)
        config_outer.pack(fill=BOTH, expand=True)

        canvas = ttk.Canvas(config_outer, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(0,10))

        scrollbar = ttk.Scrollbar(config_outer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_inner = ttk.Frame(canvas) # This is our 'form'
        canvas.create_window((0, 0), window=scrollable_inner, anchor="nw")

        def _on_config_resize(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Make the scrollable_inner frame fill the width of the canvas
            canvas.itemconfig("all_contents_frame", width=event.width)

        canvas.bind("<Configure>", _on_config_resize)
        # Add a name to the window so we can refer to it in _on_config_resize
        canvas.itemconfig(canvas.create_window((0, 0), window=scrollable_inner, anchor="nw", tags="all_contents_frame"), width=canvas.winfo_width())


        scrollable_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_inner.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"), add="+")


        save_button_container = ttk.Frame(self.config_tab) # Should be child of config_tab, not scrollable_inner
        save_button_container.pack(fill="x", pady=(5,15), side="bottom") # Pack at bottom
        ttk.Button(
            save_button_container,
            text="💾 Zapisz i Zastosuj",
            bootstyle="primary",
            width=20, # Adjusted width
            command=self.save_config_to_file
        ).pack(anchor="center") # Center the button

        self.fields = {}
        form = scrollable_inner # Use scrollable_inner as the parent for fields

        def add_field(parent, label, key, tooltip, kind="entry", default_value_key=None):
            if default_value_key is None:
                default_value_key = key

            ttk.Label(parent, text=label).pack(anchor="w", padx=10, pady=(5,0))
            current_value = getattr(config_module, key, default_config_values.get(default_value_key))


            if kind == "entry":
                var = ttk.StringVar(value=str(current_value))
                entry_frame = ttk.Frame(parent)
                entry_frame.pack(fill="x", expand=True, padx=10, pady=(0, 8))

                entry = ttk.Entry(entry_frame, textvariable=var)
                entry.pack(side="left", fill=X, expand=True)

                if key in ["FASTER_WHISPER_EXE", "YT_DLP_EXE"]:
                    def browse_exe(var_ref=var, title_text=f"Wybierz plik dla {label}"): # Capture var and title
                        file_path = filedialog.askopenfilename(title=title_text, filetypes=[("Pliki wykonywalne", "*.exe"), ("Wszystkie pliki", "*.*")])
                        if file_path:
                            var_ref.set(file_path) # Use captured var_ref
                    browse_btn = ttk.Button(entry_frame, text="📂", width=3, command=lambda v=var, l=label: browse_exe(v, f"Wybierz plik dla {l}"))
                    browse_btn.pack(side="right", padx=5)

                ToolTip(entry, tooltip)
                self.fields[key] = var

            elif kind == "bool":
                var = ttk.BooleanVar(value=bool(current_value))
                checkbox = ttk.Checkbutton(parent, text="Włączone", variable=var) # Changed "Enable" to "Włączone"
                checkbox.pack(fill="x", expand=True, padx=10, pady=(0, 8), anchor="w")
                ToolTip(checkbox, tooltip)
                self.fields[key] = var

        # LLM Prompt
        ttk.Label(form, text="Prompt LLM").pack(anchor="w", padx=10, pady=(10,0))
        prompt_frame = ttk.Frame(form)
        prompt_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        prompt_box = ttk.Text(prompt_frame, height=8, wrap="word", font=("Segoe UI", 10))

        current_llm_prompt = getattr(config_module, "LLM_PROMPT", default_config_values.get("LLM_PROMPT"))
        prompt_clean = current_llm_prompt.strip()
        lines = prompt_clean.splitlines()
        lines = [line for line in lines if "from now write only in" not in line.strip().lower() and "{text}" not in line.strip().lower()]
        prompt_clean = "\n".join(lines).strip()

        prompt_box.insert("1.0", prompt_clean)
        prompt_box.pack(fill="both", expand=True)
        ToolTip(prompt_box, "Prompt wysyłany do modelu językowego w celu generowania streszczenia.\nPlaceholdery {text} i instrukcja językowa są dodawane automatycznie.")
        self.fields["LLM_PROMPT"] = prompt_box # Store the Text widget itself

        # Other Fields
        add_field(form, "Język (transkrypcja i streszczenie)", "WHISPER_LANGUAGE", "np. Polish, English. Używane dla transkrypcji i jako instrukcja dla LLM.")
        add_field(form, "Włącz diaryzację mówcy", "ENABLE_SPEAKER_DIARIZATION", "Włącza rozpoznawanie różnych mówców.\nMoże spowolnić proces i wymagać odpowiedniego modelu Whisper.", kind="bool")
        add_field(form, "Prefiks mówcy (diaryzacja)", "DIARIZE_SPEAKER_PREFIX", "Prefiks dla mówców, np. MÓWCA, SPEAKER. FW doda numer.")
        add_field(form, "Model Whisper", "WHISPER_MODEL", "Model Faster Whisper: np. base, small, medium, large-v3, turbo")
        add_field(form, "Metoda diaryzacji", "DIARIZE_METHOD", "Metoda diaryzacji, np. pyannote_v3.1, reverb_v1. Zobacz --diarize w help FW.")
        add_field(form, "Format transkrypcji (wewn.)", "TRANSCRIPTION_FORMAT", "Format pliku transkrypcji, np. txt, srt, vtt. (domyślnie txt)")
        add_field(form, "Model Ollama", "OLLAMA_MODEL", "Model LLM w Ollama, np. gemma3:4b, llama3:8b")
        add_field(form, "Nazwa pobranego pliku audio", "DOWNLOADED_AUDIO_FILENAME", "Nazwa tymczasowego pliku audio pobieranego z YouTube.")
        add_field(form, "Plik wykonywalny yt-dlp", "YT_DLP_EXE", "Ścieżka do yt-dlp.exe. Wymagane do pobierania z YouTube.")
        add_field(form, "Plik wykonywalny Faster Whisper", "FASTER_WHISPER_EXE", "Ścieżka do faster-whisper-xxl.exe.")


        # Default input path
        self.current_input_path = None
        self.output_base_name = None # To store the base name for saving files

        # Show Config tab by default
        self.tabs.select(self.config_tab)

    def browse_file(self):
        path = filedialog.askopenfilename(title="Wybierz plik audio", filetypes=[("Pliki audio", "*.mp3 *.wav *.m4a *.ogg *.flac"), ("Wszystkie pliki", "*.*")])
        if path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, path)

    def _get_save_name_base(self):
        if self.output_base_name:
            return self.output_base_name
        if self.current_input_path:
            # Try to create a more robust base name
            if self.current_input_path.lower().startswith(("http://", "https://")):
                # For URLs, try to derive a name, or use a generic one
                try:
                    # A very basic attempt to get a video ID or meaningful part
                    # This is highly dependent on URL structure and might need improvement
                    parsed_url = Path(self.current_input_path.split("?")[0]).name
                    if parsed_url and parsed_url != ".": # Ensure it's not empty or just a dot
                        return f"youtube_{parsed_url}"
                except Exception:
                    pass # Fallback if parsing fails
                return "youtube_audio" # Generic fallback for URLs
            else:
                return Path(self.current_input_path).stem
        return "wynik" # Default if no input path set

    def save_console_log(self):
        base_name = self._get_save_name_base()
        default_filename = Path(base_name + ".console_log.txt")
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.console_text.get("1.0", "end-1c")) # -1c to avoid extra newline
                messagebox.showinfo("Zapisano", f"Log konsoli zapisany do {file_path}")
            except Exception as e:
                messagebox.showerror("Błąd zapisu", f"Nie można zapisać logu: {e}")

    def save_console_log_as(self): # Effectively same as save_console_log due to asksaveasfilename
        self.save_console_log()

    def save_transcription(self):
        base_name = self._get_save_name_base()
        default_filename = Path(base_name + ".transcription.txt") # Use config for extension later if needed
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt", # or use config.TRANSCRIPTION_FORMAT
            filetypes=[("Pliki tekstowe", "*.txt"), ("Pliki SRT", "*.srt"), ("Pliki VTT", "*.vtt"), ("Wszystkie pliki", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.transcription_text.get("1.0", "end-1c"))
                messagebox.showinfo("Zapisano", f"Transkrypcja zapisana do {file_path}")
            except Exception as e:
                messagebox.showerror("Błąd zapisu", f"Nie można zapisać transkrypcji: {e}")

    def save_transcription_as(self):
        self.save_transcription()

    def save_summary(self):
        base_name = self._get_save_name_base()
        default_filename = Path(base_name + ".summary.txt")
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.summary_text.get("1.0", "end-1c")) # Use the markdown version if needed
                messagebox.showinfo("Zapisano", f"Streszczenie zapisane do {file_path}")
            except Exception as e:
                messagebox.showerror("Błąd zapisu", f"Nie można zapisać streszczenia: {e}")

    def save_summary_as(self):
        self.save_summary()

    def save_config_to_file(self):
        try:
            config_content = ["# config.py - wygenerowany przez Pogadane GUI\n"]
            # Ensure all default keys are present if not in self.fields (e.g. new keys in defaults)
            all_keys = set(self.fields.keys()) | set(default_config_values.keys())

            for key in all_keys:
                if key in self.fields:
                    var = self.fields[key]
                    if key == "LLM_PROMPT":
                        val = var.get("1.0", "end-1c").strip() # -1c to avoid extra newline
                        # Language instruction and {text} are added by the script, no need here
                    elif isinstance(var, ttk.BooleanVar):
                        val = var.get()
                    else: # ttk.StringVar
                        val = var.get()
                else: # Key is in defaults but not in GUI fields (should not happen with current setup)
                    val = default_config_values[key]


                if isinstance(val, bool):
                    config_content.append(f"{key.upper()} = {val}")
                elif isinstance(val, (int, float)):
                    config_content.append(f"{key.upper()} = {val}")
                else: # Strings, paths
                    config_content.append(f"{key.upper()} = {repr(str(val))}") # Ensure it's a string and repr for safety

            with open(self.config_file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(config_content) + "\n")

            messagebox.showinfo("Zapisano", f"Konfiguracja zapisana do {self.config_file_path}.\nZmiany zostaną zastosowane przy następnym uruchomieniu transkrypcji.")
            # Reload config for the current GUI session if needed, or inform user to restart script
            self.reload_config_module()

        except Exception as e:
            messagebox.showerror("Błąd zapisu konfiguracji", str(e))

    def reload_config_module(self):
        global config_module
        try:
            # Invalidate caches for the specific module
            if 'config' in sys.modules:
                importlib.reload(sys.modules['config'])
                config_module = sys.modules['config']
                print("✅ Konfiguracja GUI przeładowana po zapisie.")
            else: # If not in sys.modules, try to load it fresh
                spec = importlib.util.spec_from_file_location("config", self.config_file_path)
                if spec and spec.loader:
                    config_module = importlib.util.module_from_spec(spec)
                    sys.modules['config'] = config_module
                    spec.loader.exec_module(config_module)
                    print("✅ Konfiguracja GUI załadowana (pierwszy raz po zapisie).")
                else:
                     raise ImportError("Nie można utworzyć specyfikacji modułu po zapisie.")

            # Optionally, re-populate fields if you want live update of GUI from reloaded config
            # self.populate_config_fields() # You would need to create this method
        except Exception as e:
            messagebox.showerror("Błąd przeładowania konfiguracji", f"Nie udało się przeładować config.py: {e}\nNiektóre zmiany mogą wymagać ponownego uruchomienia GUI.")
            # Fallback to ensure config_module is not None
            if config_module is None:
                class DummyConfig: pass
                config_module = DummyConfig()
                for key, value in default_config_values.items():
                    setattr(config_module, key, value)


    def run_script(self):
        input_value = self.input_entry.get().strip()
        if not input_value:
            messagebox.showwarning("Brak danych wejściowych", "Podaj ścieżkę do pliku audio lub URL YouTube.")
            return

        self.current_input_path = input_value
        self.output_base_name = self._get_save_name_base() # Set base name for saving files

        self.progress.pack(pady=(5, 10), fill=X, padx=20) # Pack progress bar here
        self.progress.start(10)
        self.transcribe_button.config(state="disabled", text="⏳ Przetwarzanie...")

        # Clear previous results
        for widget in [self.console_text, self.transcription_text, self.summary_text]:
            widget.config(state="normal")
            widget.delete("1.0", "end")
            widget.config(state="disabled")

        self.console_text.config(state="normal") # Enable for output

        self.output_queue = queue.Queue()
        self.script_thread = threading.Thread(target=self._execute_script_streaming, args=(input_value,), daemon=True)
        self.script_thread.start()

        self._poll_output_queue()
        self.tabs.select(self.console_tab) # Switch to console tab

    def _execute_script_streaming(self, input_value):
        # Determine path to transcribe_summarize_working.py
        script_path = self.base_path / "transcribe_summarize_working.py"
        if not script_path.exists():
            self.output_queue.put(f"BŁĄD KRYTYCZNY: Nie znaleziono skryptu transcribe_summarize_working.py w {self.base_path}\n")
            self.output_queue.put(None) # Signal finished
            return

        command = [sys.executable, "-u", str(script_path), input_value]
        # The -o flag for saving summary directly from CLI script is not used here,
        # as GUI will handle saving of summary content.

        # Diarization CLI flags based on GUI config
        # These will override what's in config.py for the script's execution
        if hasattr(config_module, 'ENABLE_SPEAKER_DIARIZATION'):
            if getattr(config_module, 'ENABLE_SPEAKER_DIARIZATION'):
                command.append("--diarize")
            else:
                command.append("--no-diarize")
        
        # Ensure the script runs from the directory containing config.py if it's not bundled
        # For PyInstaller, config.py should be included in the bundle at the top level (base_path)
        cwd_path = str(self.base_path)


        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Capture stderr to stdout pipe
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=cwd_path, # Run script in its directory
                startupinfo=None if os.name != 'nt' else subprocess.STARTUPINFO(dwFlags=subprocess.CREATE_NO_WINDOW) # Hide console window on Windows
            )

            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    self.output_queue.put(strip_ansi(line))
                process.stdout.close()
            
            process.wait() # Wait for the process to complete

        except FileNotFoundError:
            self.output_queue.put(f"BŁĄD: Nie znaleziono interpretera Python ({sys.executable}) lub skryptu/zależności.\n")
        except Exception as e:
            self.output_queue.put(f"BŁĄD wykonania skryptu: {e}\n")
        finally:
            self.output_queue.put(None) # Signal finished

    def _update_output_widgets(self, full_log):
        # This method is called once at the end to populate transcription and summary
        transcription, summary = extract_transcription_and_summary(full_log)

        if transcription:
            self.transcription_text.config(state="normal")
            self.transcription_text.delete("1.0", "end")
            self.transcription_text.insert("end", transcription)
            self.transcription_text.config(state="disabled")
        else: # If no transcription specifically extracted, put the whole log there as fallback
            self.transcription_text.config(state="normal")
            self.transcription_text.delete("1.0", "end")
            self.transcription_text.insert("end", "Nie udało się wyodrębnić transkrypcji z logu.\nPełny log jest w zakładce Konsola.")
            self.transcription_text.config(state="disabled")


        if summary:
            self.summary_text.config(state="normal")
            insert_with_markdown(self.summary_text, summary) # Using the markdown helper
            self.summary_text.config(state="disabled")
        else:
            self.summary_text.config(state="normal")
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("end", "Nie udało się wyodrębnić streszczenia z logu.")
            self.summary_text.config(state="disabled")


    def _poll_output_queue(self):
        try:
            while True: # Process all available lines
                line = self.output_queue.get_nowait()
                if line is None: # End of script signal
                    self._finalize_script_run()
                    return
                else:
                    self.console_text.insert("end", line)
                    self.console_text.see("end") # Autoscroll
        except queue.Empty:
            if self.script_thread.is_alive(): # If script is still running, schedule next poll
                self.after(100, self._poll_output_queue)
            else: # Script finished but None might not have been processed yet
                 self._finalize_script_run() # Try to finalize if thread died unexpectedly

    def _finalize_script_run(self):
        # This ensures that even if None is missed, we finalize if the thread is dead.
        if hasattr(self, '_finalized_run') and self._finalized_run:
            return # Already finalized
        self._finalized_run = True

        full_log_content = self.console_text.get("1.0", "end-1c")
        self._update_output_widgets(full_log_content)

        # Switch to summary tab if summary is found, else transcription, else console
        if self.summary_text.get("1.0", "end-1c").strip() and "Nie udało się wyodrębnić streszczenia" not in self.summary_text.get("1.0", "end-1c"):
            self.tabs.select(self.summary_tab)
        elif self.transcription_text.get("1.0", "end-1c").strip() and "Nie udało się wyodrębnić transkrypcji" not in self.transcription_text.get("1.0", "end-1c"):
            self.tabs.select(self.transcription_tab)
        else:
            self.tabs.select(self.console_tab)

        self.progress.stop()
        self.progress.pack_forget() # Hide progress bar
        self.transcribe_button.config(state="normal", text="🚀 Transkrybuj i Streść")
        self.console_text.config(state="disabled") # Disable console after completion
        
        # Reset flag for next run
        del self._finalized_run


if __name__ == "__main__":
    # Required for PyInstaller --windowed mode on Windows
    # to prevent issues with subprocess and stdio redirection
    if hasattr(sys, 'frozen') and sys.platform == 'win32' and sys.stdout is None:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    app = TranscriberApp()
    app.mainloop()