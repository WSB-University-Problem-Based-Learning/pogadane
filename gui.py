import ttkbootstrap as ttk
from ttkbootstrap.constants import X, BOTH, N, S, E, W, VERTICAL
from tkinter import filedialog, messagebox, StringVar, BooleanVar, Text, Canvas, Frame, Scrollbar
import threading
import queue
import subprocess
import sys
import os
import re
from pathlib import Path
import importlib.util

# Wersja Alpha v0.1.7

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
    
    "SUMMARY_PROVIDER": "ollama", # Nowa opcja
    "SUMMARY_LANGUAGE": "Polish",  # Nowa opcja
    
    "OLLAMA_MODEL": "gemma3:4b", # Dla SUMMARY_PROVIDER="ollama"
    
    "GOOGLE_API_KEY": "", # Nowa opcja (dla SUMMARY_PROVIDER="google")
    "GOOGLE_GEMINI_MODEL": "gemini-1.5-flash-latest", # Nowa opcja (dla SUMMARY_PROVIDER="google")

    "LLM_PROMPT": "Streść poniższy tekst, skupiając się na kluczowych wnioskach i decyzjach:", # Zaktualizowany domyślny prompt (rdzeń)
    
    "TRANSCRIPTION_FORMAT": "txt",
    "DOWNLOADED_AUDIO_FILENAME": "downloaded_audio.mp3",
}

config_module = None
try:
    spec = importlib.util.spec_from_file_location("config", config_path)
    if spec and spec.loader:
        config_module = importlib.util.module_from_spec(spec)
        sys.modules['config'] = config_module 
        spec.loader.exec_module(config_module)
        print("✅ Konfiguracja GUI załadowana z pliku config.py.")
    else:
        raise ImportError("Nie można utworzyć specyfikacji modułu lub loader jest None.")
except ImportError:
    print("⚠️ Ostrzeżenie GUI: Plik konfiguracyjny config.py nie został znaleziony lub jest błędny.")
    print("   GUI użyje wartości domyślnych.")
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
    if not transcription: 
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
        x_bbox, y_bbox, _, _ = bbox 
        x = self.widget.winfo_rootx() + x_bbox + 20 
        y = self.widget.winfo_rooty() + y_bbox + 20 

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
        self.geometry("700x850") # Increased height for new fields
        self.resizable(True, True)

        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys._MEIPASS)
        else:
            self.base_path = Path(__file__).parent
        self.config_file_path = self.base_path / "config.py"

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
        self.progress = ttk.Progressbar(top_frame, mode="indeterminate", length=300, bootstyle="info-striped")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(padx=20, pady=(0, 20), fill=BOTH, expand=True)

        self.console_tab = ttk.Frame(self.tabs)
        self.console_text = ttk.ScrolledText(self.console_tab, font=("Segoe UI Emoji", 10), wrap="word", state="disabled")
        self.console_text.pack(fill=BOTH, expand=True)
        console_btns = ttk.Frame(self.console_tab)
        console_btns.pack(pady=5, fill=X)
        ttk.Button(console_btns, text="💾 Zapisz Log", command=self.save_console_log).pack(side="left", padx=5)
        ttk.Button(console_btns, text="📁 Zapisz Log Jako...", command=self.save_console_log_as).pack(side="left", padx=5)
        self.tabs.add(self.console_tab, text="🖥️ Konsola")

        self.transcription_tab = ttk.Frame(self.tabs)
        self.transcription_text = ttk.ScrolledText(self.transcription_tab, font=("Segoe UI Emoji", 10), wrap="word", state="disabled")
        self.transcription_text.pack(fill=BOTH, expand=True)
        btns1 = ttk.Frame(self.transcription_tab)
        btns1.pack(pady=5, fill=X)
        ttk.Button(btns1, text="💾 Zapisz Transkrypcję", command=self.save_transcription).pack(side="left", padx=5)
        ttk.Button(btns1, text="📁 Zapisz Transkrypcję Jako...", command=self.save_transcription_as).pack(side="left", padx=5)
        self.tabs.add(self.transcription_tab, text="📝 Transkrypcja")

        self.summary_tab = ttk.Frame(self.tabs)
        self.summary_text = ttk.ScrolledText(self.summary_tab, font=("Segoe UI Emoji", 10), wrap="word", state="disabled")
        self.summary_text.pack(fill=BOTH, expand=True)
        btns2 = ttk.Frame(self.summary_tab)
        btns2.pack(pady=5, fill=X)
        ttk.Button(btns2, text="💾 Zapisz Streszczenie", command=self.save_summary).pack(side="left", padx=5)
        ttk.Button(btns2, text="📁 Zapisz Streszczenie Jako...", command=self.save_summary_as).pack(side="left", padx=5)
        self.tabs.add(self.summary_tab, text="📌 Streszczenie")

        self.config_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.config_tab, text="⚙️ Konfiguracja")
        config_outer = ttk.Frame(self.config_tab)
        config_outer.pack(fill=BOTH, expand=True)
        canvas = ttk.Canvas(config_outer, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(0,10))
        scrollbar = ttk.Scrollbar(config_outer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_inner = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_inner, anchor="nw", tags="all_contents_frame")
        def _on_config_resize(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig("all_contents_frame", width=event.width)
        canvas.bind("<Configure>", _on_config_resize)
        scrollable_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_inner.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"), add="+")
        save_button_container = ttk.Frame(self.config_tab)
        save_button_container.pack(fill="x", pady=(5,15), side="bottom")
        ttk.Button(save_button_container, text="💾 Zapisz i Zastosuj",bootstyle="primary",width=20,command=self.save_config_to_file).pack(anchor="center")

        self.fields = {}
        form = scrollable_inner

        def add_field(parent, label, key, tooltip, kind="entry", default_value_key=None, options=None):
            if default_value_key is None: default_value_key = key
            ttk.Label(parent, text=label).pack(anchor="w", padx=10, pady=(8,0)) # Increased pady
            current_value = getattr(config_module, key, default_config_values.get(default_value_key))

            if kind == "entry":
                var = StringVar(value=str(current_value))
                entry_frame = ttk.Frame(parent)
                entry_frame.pack(fill="x", expand=True, padx=10, pady=(0, 8))
                entry = ttk.Entry(entry_frame, textvariable=var)
                entry.pack(side="left", fill=X, expand=True)
                if key in ["FASTER_WHISPER_EXE", "YT_DLP_EXE"]:
                    def browse_exe(var_ref=var, title_text=f"Wybierz plik dla {label}"):
                        file_path = filedialog.askopenfilename(title=title_text, filetypes=[("Pliki wykonywalne", "*.exe"), ("Wszystkie pliki", "*.*")])
                        if file_path: var_ref.set(file_path)
                    browse_btn_cfg = ttk.Button(entry_frame, text="📂", width=3, command=lambda v=var, l=label: browse_exe(v, f"Wybierz plik dla {l}"))
                    browse_btn_cfg.pack(side="right", padx=5)
                ToolTip(entry, tooltip)
                self.fields[key] = var
            elif kind == "bool":
                var = BooleanVar(value=bool(current_value))
                checkbox = ttk.Checkbutton(parent, text="Włączone", variable=var)
                checkbox.pack(fill="x", expand=True, padx=10, pady=(0, 8), anchor="w")
                ToolTip(checkbox, tooltip)
                self.fields[key] = var
            elif kind == "combo":
                var = StringVar(value=str(current_value))
                combo = ttk.Combobox(parent, textvariable=var, values=options, state="readonly")
                combo.pack(fill="x", expand=True, padx=10, pady=(0,8))
                ToolTip(combo, tooltip)
                self.fields[key] = var


        # --- Sekcja: Podsumowanie ---
        ttk.Label(form, text="--- Podsumowanie ---", font="-weight bold").pack(anchor="w", padx=10, pady=(15,5))
        add_field(form, "Dostawca podsumowania", "SUMMARY_PROVIDER", "Wybierz system do generowania podsumowań: 'ollama' (lokalnie) lub 'google' (API Gemini).", kind="combo", options=["ollama", "google"])
        add_field(form, "Język podsumowania", "SUMMARY_LANGUAGE", "np. Polish, English. Język, w którym zostanie wygenerowane podsumowanie.")
        
        # LLM Prompt - zmodyfikowane
        ttk.Label(form, text="Prompt dla LLM (Rdzeń instrukcji)").pack(anchor="w", padx=10, pady=(8,0))
        prompt_frame = ttk.Frame(form)
        prompt_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        prompt_box = Text(prompt_frame, height=5, wrap="word", font=("Segoe UI", 10), relief="solid", borderwidth=1) # Standard Tk Text
        current_llm_prompt_from_config = getattr(config_module, "LLM_PROMPT", default_config_values.get("LLM_PROMPT"))
        prompt_box.insert("1.0", current_llm_prompt_from_config) # Wyświetl bez czyszczenia
        prompt_box.pack(fill="both", expand=True)
        ToolTip(prompt_box, "Główna część polecenia dla LLM (np. 'Streść tekst, skupiając się na...').\nInstrukcja językowa i tekst transkrypcji zostaną dodane automatycznie.")
        self.fields["LLM_PROMPT"] = prompt_box

        # --- Sekcja: Ustawienia Ollama (jeśli wybrana) ---
        ttk.Label(form, text="--- Ustawienia Ollama (jeśli dostawcą jest 'ollama') ---", font="-weight bold").pack(anchor="w", padx=10, pady=(15,5))
        add_field(form, "Model Ollama", "OLLAMA_MODEL", "Model LLM w Ollama, np. gemma3:4b, llama3:8b")

        # --- Sekcja: Ustawienia Google Gemini API (jeśli wybrany) ---
        ttk.Label(form, text="--- Ustawienia Google Gemini API (jeśli dostawcą jest 'google') ---", font="-weight bold").pack(anchor="w", padx=10, pady=(15,5))
        add_field(form, "Klucz Google API", "GOOGLE_API_KEY", "Twój klucz API Google Gemini. Wymagane, jeśli używasz Google do podsumowań.")
        add_field(form, "Model Google Gemini", "GOOGLE_GEMINI_MODEL", "Model Google Gemini, np. gemini-1.5-flash-latest")

        # --- Sekcja: Transkrypcja (Whisper) ---
        ttk.Label(form, text="--- Transkrypcja (Faster Whisper) ---", font="-weight bold").pack(anchor="w", padx=10, pady=(15,5))
        add_field(form, "Język transkrypcji (Whisper)", "WHISPER_LANGUAGE", "np. Polish, English. Używane tylko dla transkrypcji przez Whisper.")
        add_field(form, "Model Whisper", "WHISPER_MODEL", "Model Faster Whisper: np. base, small, medium, large-v3, turbo")
        add_field(form, "Włącz diaryzację mówcy", "ENABLE_SPEAKER_DIARIZATION", "Włącza rozpoznawanie różnych mówców.\nMoże spowolnić proces i wymagać odpowiedniego modelu Whisper.", kind="bool")
        add_field(form, "Prefiks mówcy (diaryzacja)", "DIARIZE_SPEAKER_PREFIX", "Prefiks dla mówców, np. MÓWCA, SPEAKER. FW doda numer.")
        add_field(form, "Metoda diaryzacji", "DIARIZE_METHOD", "Metoda diaryzacji, np. pyannote_v3.1, reverb_v1. Zobacz --diarize w help FW.")

        # --- Sekcja: Ogólne Ustawienia Skryptu ---
        ttk.Label(form, text="--- Ogólne Ustawienia Skryptu ---", font="-weight bold").pack(anchor="w", padx=10, pady=(15,5))
        add_field(form, "Format transkrypcji (wewn.)", "TRANSCRIPTION_FORMAT", "Format pliku transkrypcji, np. txt, srt, vtt. (domyślnie txt)")
        add_field(form, "Nazwa pobranego pliku audio", "DOWNLOADED_AUDIO_FILENAME", "Nazwa tymczasowego pliku audio pobieranego z YouTube.")
        add_field(form, "Plik wykonywalny yt-dlp", "YT_DLP_EXE", "Ścieżka do yt-dlp.exe. Wymagane do pobierania z YouTube.")
        add_field(form, "Plik wykonywalny Faster Whisper", "FASTER_WHISPER_EXE", "Ścieżka do faster-whisper-xxl.exe.")

        self.current_input_path = None
        self.output_base_name = None
        self.tabs.select(self.config_tab)

    def browse_file(self):
        path = filedialog.askopenfilename(title="Wybierz plik audio", filetypes=[("Pliki audio", "*.mp3 *.wav *.m4a *.ogg *.flac"), ("Wszystkie pliki", "*.*")])
        if path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, path)

    def _get_save_name_base(self):
        if self.output_base_name: return self.output_base_name
        if self.current_input_path:
            if self.current_input_path.lower().startswith(("http://", "https://")):
                try:
                    parsed_url = Path(self.current_input_path.split("?")[0]).name
                    if parsed_url and parsed_url != ".": return f"youtube_{parsed_url}"
                except Exception: pass
                return "youtube_audio"
            else:
                return Path(self.current_input_path).stem
        return "wynik"

    def save_console_log(self):
        base_name = self._get_save_name_base()
        default_filename = Path(base_name + ".console_log.txt")
        file_path = filedialog.asksaveasfilename(initialfile=default_filename, defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f: f.write(self.console_text.get("1.0", "end-1c"))
                messagebox.showinfo("Zapisano", f"Log konsoli zapisany do {file_path}")
            except Exception as e: messagebox.showerror("Błąd zapisu", f"Nie można zapisać logu: {e}")

    def save_console_log_as(self): self.save_console_log()

    def save_transcription(self):
        base_name = self._get_save_name_base()
        default_filename = Path(base_name + ".transcription.txt")
        file_path = filedialog.asksaveasfilename(initialfile=default_filename, defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt"), ("Pliki SRT", "*.srt"), ("Pliki VTT", "*.vtt"), ("Wszystkie pliki", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f: f.write(self.transcription_text.get("1.0", "end-1c"))
                messagebox.showinfo("Zapisano", f"Transkrypcja zapisana do {file_path}")
            except Exception as e: messagebox.showerror("Błąd zapisu", f"Nie można zapisać transkrypcji: {e}")

    def save_transcription_as(self): self.save_transcription()

    def save_summary(self):
        base_name = self._get_save_name_base()
        default_filename = Path(base_name + ".summary.txt")
        file_path = filedialog.asksaveasfilename(initialfile=default_filename, defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f: f.write(self.summary_text.get("1.0", "end-1c"))
                messagebox.showinfo("Zapisano", f"Streszczenie zapisane do {file_path}")
            except Exception as e: messagebox.showerror("Błąd zapisu", f"Nie można zapisać streszczenia: {e}")

    def save_summary_as(self): self.save_summary()

    def save_config_to_file(self):
        try:
            config_content = ["# config.py - wygenerowany przez Pogadane GUI\n"]
            all_keys = set(self.fields.keys()) | set(default_config_values.keys())
            key_order = [
                "FASTER_WHISPER_EXE", "YT_DLP_EXE", 
                "WHISPER_LANGUAGE", "WHISPER_MODEL", 
                "ENABLE_SPEAKER_DIARIZATION", "DIARIZE_METHOD", "DIARIZE_SPEAKER_PREFIX",
                "SUMMARY_PROVIDER", "SUMMARY_LANGUAGE",
                "OLLAMA_MODEL", 
                "GOOGLE_API_KEY", "GOOGLE_GEMINI_MODEL",
                "LLM_PROMPT", 
                "TRANSCRIPTION_FORMAT", "DOWNLOADED_AUDIO_FILENAME"
            ]
            
            # Dodaj nowe klucze, które mogłyby nie być w key_order, na koniec
            sorted_keys = [k for k in key_order if k in all_keys]
            for k in all_keys:
                if k not in sorted_keys:
                    sorted_keys.append(k)

            for key in sorted_keys:
                if key in self.fields:
                    var = self.fields[key]
                    if key == "LLM_PROMPT": # Specjalna obsługa dla Text widget
                        val = var.get("1.0", "end-1c").strip()
                    elif isinstance(var, BooleanVar):
                        val = var.get()
                    else: # StringVar
                        val = var.get()
                else: # Klucz jest w default_config_values, ale nie ma pola w GUI (np. nowo dodany)
                    val = getattr(config_module, key, default_config_values.get(key))


                if isinstance(val, bool):
                    config_content.append(f"{key.upper()} = {val}")
                elif isinstance(val, (int, float)):
                    config_content.append(f"{key.upper()} = {val}")
                else: 
                    config_content.append(f"{key.upper()} = {repr(str(val))}") 

            with open(self.config_file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(config_content) + "\n")

            messagebox.showinfo("Zapisano", f"Konfiguracja zapisana do {self.config_file_path}.\nZmiany zostaną zastosowane przy następnym uruchomieniu transkrypcji.")
            self.reload_config_module()

        except Exception as e:
            messagebox.showerror("Błąd zapisu konfiguracji", str(e))

    def reload_config_module(self):
        global config_module
        try:
            if 'config' in sys.modules:
                importlib.reload(sys.modules['config'])
                config_module = sys.modules['config']
                print("✅ Konfiguracja GUI przeładowana po zapisie.")
            else: 
                spec = importlib.util.spec_from_file_location("config", self.config_file_path)
                if spec and spec.loader:
                    config_module = importlib.util.module_from_spec(spec)
                    sys.modules['config'] = config_module
                    spec.loader.exec_module(config_module)
                    print("✅ Konfiguracja GUI załadowana (pierwszy raz po zapisie).")
                else:
                     raise ImportError("Nie można utworzyć specyfikacji modułu po zapisie.")
        except Exception as e:
            messagebox.showerror("Błąd przeładowania konfiguracji", f"Nie udało się przeładować config.py: {e}\nNiektóre zmiany mogą wymagać ponownego uruchomienia GUI.")
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
        self.output_base_name = self._get_save_name_base() 

        self.progress.pack(pady=(5, 10), fill=X, padx=20) 
        self.progress.start(10)
        self.transcribe_button.config(state="disabled", text="⏳ Przetwarzanie...")

        for widget in [self.console_text, self.transcription_text, self.summary_text]:
            widget.config(state="normal")
            widget.delete("1.0", "end")
            widget.config(state="disabled")
        self.console_text.config(state="normal")

        self.output_queue = queue.Queue()
        self.script_thread = threading.Thread(target=self._execute_script_streaming, args=(input_value,), daemon=True)
        self.script_thread.start()
        self._poll_output_queue()
        self.tabs.select(self.console_tab) 

    def _execute_script_streaming(self, input_value):
        script_path = self.base_path / "transcribe_summarize_working.py"
        if not script_path.exists():
            self.output_queue.put(f"BŁĄD KRYTYCZNY: Nie znaleziono skryptu transcribe_summarize_working.py w {self.base_path}\n")
            self.output_queue.put(None) 
            return

        command = [sys.executable, "-u", str(script_path), input_value]
        
        # Przekazanie konfiguracji diaryzacji przez flagi CLI, jeśli GUI ją zmodyfikowało
        # Odczytujemy aktualną wartość z (potencjalnie przeładowanego) config_module
        enable_diarization_gui = getattr(config_module, 'ENABLE_SPEAKER_DIARIZATION', default_config_values['ENABLE_SPEAKER_DIARIZATION'])
        if enable_diarization_gui:
            command.append("--diarize")
        else:
            command.append("--no-diarize")
        
        cwd_path = str(self.base_path)
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                encoding="utf-8", errors="replace", cwd=cwd_path, 
                startupinfo=None if os.name != 'nt' else subprocess.STARTUPINFO(dwFlags=subprocess.CREATE_NO_WINDOW)
            )
            if process.stdout:
                for line in iter(process.stdout.readline, ''): self.output_queue.put(strip_ansi(line))
                process.stdout.close()
            process.wait()
        except FileNotFoundError: self.output_queue.put(f"BŁĄD: Nie znaleziono interpretera Python ({sys.executable}) lub skryptu/zależności.\n")
        except Exception as e: self.output_queue.put(f"BŁĄD wykonania skryptu: {e}\n")
        finally: self.output_queue.put(None)

    def _update_output_widgets(self, full_log):
        transcription, summary = extract_transcription_and_summary(full_log)
        if transcription:
            self.transcription_text.config(state="normal")
            self.transcription_text.delete("1.0", "end")
            self.transcription_text.insert("end", transcription)
            self.transcription_text.config(state="disabled")
        else: 
            self.transcription_text.config(state="normal")
            self.transcription_text.delete("1.0", "end")
            self.transcription_text.insert("end", "Nie udało się wyodrębnić transkrypcji z logu.\nPełny log jest w zakładce Konsola.")
            self.transcription_text.config(state="disabled")
        if summary:
            self.summary_text.config(state="normal")
            insert_with_markdown(self.summary_text, summary) 
            self.summary_text.config(state="disabled")
        else:
            self.summary_text.config(state="normal")
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("end", "Nie udało się wyodrębnić streszczenia z logu.")
            self.summary_text.config(state="disabled")

    def _poll_output_queue(self):
        try:
            while True: 
                line = self.output_queue.get_nowait()
                if line is None: 
                    self._finalize_script_run()
                    return
                else:
                    self.console_text.insert("end", line)
                    self.console_text.see("end") 
        except queue.Empty:
            if self.script_thread.is_alive(): 
                self.after(100, self._poll_output_queue)
            else: 
                 self._finalize_script_run() 

    def _finalize_script_run(self):
        if hasattr(self, '_finalized_run') and self._finalized_run: return 
        self._finalized_run = True
        full_log_content = self.console_text.get("1.0", "end-1c")
        self._update_output_widgets(full_log_content)
        if self.summary_text.get("1.0", "end-1c").strip() and "Nie udało się wyodrębnić streszczenia" not in self.summary_text.get("1.0", "end-1c"):
            self.tabs.select(self.summary_tab)
        elif self.transcription_text.get("1.0", "end-1c").strip() and "Nie udało się wyodrębnić transkrypcji" not in self.transcription_text.get("1.0", "end-1c"):
            self.tabs.select(self.transcription_tab)
        else:
            self.tabs.select(self.console_tab)
        self.progress.stop()
        self.progress.pack_forget() 
        self.transcribe_button.config(state="normal", text="🚀 Transkrybuj i Streść")
        self.console_text.config(state="disabled") 
        del self._finalized_run

if __name__ == "__main__":
    if hasattr(sys, 'frozen') and sys.platform == 'win32' and sys.stdout is None:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    app = TranscriberApp()
    app.mainloop()