import ttkbootstrap as ttk
from ttkbootstrap.constants import X, Y, BOTH, LEFT, RIGHT, TOP, BOTTOM, DISABLED, NORMAL, HORIZONTAL, VERTICAL, END, W, E, NW, YES, NO, SUNKEN, RAISED, CURRENT
from ttkbootstrap.widgets.scrolled import ScrolledText
from tkinter import filedialog, messagebox, StringVar, BooleanVar, Text, Canvas, Frame, Scrollbar
from tkinter import font as tkFont
import threading
import queue
import subprocess
import sys
import os
from pathlib import Path

# Import utility modules
from .constants import (
    APP_VERSION,
    CUSTOM_PROMPT_OPTION_TEXT,
    FILE_STATUS_PENDING,
    FILE_STATUS_PROCESSING,
    FILE_STATUS_COMPLETED,
    FILE_STATUS_ERROR,
    DEFAULT_CONFIG
)
from .text_utils import strip_ansi, extract_transcription_and_summary, insert_with_markdown
from .config_loader import ConfigManager
from .gui_utils import FontManager, ResultsManager

# Wersja Alpha v0.1.8

# Initialize configuration manager
config_manager = ConfigManager()
config_manager.initialize()
config_module = config_manager.config

# Poprawka: Definicja klasy ToolTip tylko raz.
class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.tip = None
        self.delay = delay
        self._after_id = None
        widget.bind("<Enter>", self.schedule_show)
        widget.bind("<Leave>", self.hide)
        widget.bind("<ButtonPress>", self.hide) # Hide on click

    def schedule_show(self, event):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
        app_instance = self.widget.winfo_toplevel()
        if isinstance(app_instance, TranscriberApp) and hasattr(app_instance, 'font_settings') and "tooltip" in app_instance.font_settings:
            self._after_id = self.widget.after(self.delay, lambda e=event: self.show(e))
        else:
            self._after_id = self.widget.after(self.delay, lambda e=event: self.show(e)) # Show even if font not fully ready

    def show(self, event):
        if self.tip or not self.widget.winfo_exists():
            return
        if hasattr(self.widget, 'bbox') and callable(self.widget.bbox):
            try: bbox_val = self.widget.bbox("insert" if isinstance(self.widget, (Text, ttk.Entry)) else CURRENT)
            except Exception: bbox_val = None
            x_bbox, y_bbox, _, _ = bbox_val if bbox_val else (0,0,0,0)
        else: x_bbox, y_bbox = 0,0
        x = self.widget.winfo_rootx() + x_bbox + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip = tw = ttk.Toplevel(self.widget); tw.wm_overrideredirect(True); tw.wm_attributes("-topmost", True)
        tooltip_font = ("Segoe UI", 9)
        app_instance = self.widget.winfo_toplevel()
        if isinstance(app_instance, TranscriberApp) and hasattr(app_instance, 'font_settings') and "tooltip" in app_instance.font_settings:
            tooltip_font = app_instance.font_settings["tooltip"]
        label = ttk.Label(tw, text=self.text, background="#FFFFE0", relief=SUNKEN, borderwidth=1, font=tooltip_font, wraplength=350, justify=LEFT, padding=(5,3))
        label.pack(ipadx=2, ipady=2)
        tw.update_idletasks(); screen_width = tw.winfo_screenwidth(); tip_width = tw.winfo_width()
        if x + tip_width > screen_width: x = screen_width - tip_width - 5
        if x < 0 : x = 5
        tw.wm_geometry(f"+{int(x)}+{int(y)}")

    def hide(self, event=None):
        if self._after_id: self.widget.after_cancel(self._after_id); self._after_id = None
        if self.tip: self.tip.destroy(); self.tip = None

class TranscriberApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("🎧 Pogadane GUI - Transkrybuj & Streść (v0.1.8)")
        self.geometry("950x800")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.app_style = ttk.Style()

        # Initialize FontManager
        self.font_manager = FontManager(base_font_size=10)
        self.font_settings = self.font_manager.get_all_fonts()
        self.font_manager.update_ttk_styles(self.app_style)

        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys._MEIPASS)
        else:
            self.base_path = Path(__file__).resolve().parent
        self.config_file_path = config_manager.config_path

        top_controls_frame = ttk.Frame(self)
        top_controls_frame.pack(padx=10, pady=10, fill=X)
        font_controls_frame = ttk.Frame(top_controls_frame)
        font_controls_frame.pack(side=RIGHT, padx=(0, 5))
        btn_font_plus = ttk.Button(font_controls_frame, text="A+", command=lambda: self.change_font_size(1), width=3)
        btn_font_plus.pack(side=LEFT, padx=2)
        ToolTip(btn_font_plus, "Zwiększ rozmiar czcionki.")
        btn_font_minus = ttk.Button(font_controls_frame, text="A-", command=lambda: self.change_font_size(-1), width=3)
        btn_font_minus.pack(side=LEFT)
        ToolTip(btn_font_minus, "Zmniejsz rozmiar czcionki.")

        input_label_frame = ttk.Frame(top_controls_frame)
        input_label_frame.pack(fill=X, pady=(0, 5))
        ttk.Label(
            input_label_frame,
            text="🎙️ Pliki audio / URL-e YouTube (każdy w nowej linii):",
            font=self.font_settings["label"],
        ).pack(side=LEFT, anchor=W)
        browse_btn = ttk.Button(
            input_label_frame,
            text="➕ Dodaj Pliki Audio",
            command=self.browse_and_add_files,
            bootstyle="info-outline",
            style="Outline.TButton",
        )
        browse_btn.pack(side=RIGHT, padx=(10, 0))
        ToolTip(browse_btn, "Kliknij, aby wybrać jeden lub więcej plików audio.")

        input_text_frame = ttk.Frame(top_controls_frame)
        input_text_frame.pack(fill=X, expand=YES, pady=(0, 5))
        self.input_text_area = Text(
            input_text_frame,
            height=4,
            font=self.font_settings["scrolledtext"],
            wrap="none",
            relief=SUNKEN,
            borderwidth=1,
        )
        sb_y_input = ttk.Scrollbar(input_text_frame, orient=VERTICAL, command=self.input_text_area.yview)
        sb_x_input = ttk.Scrollbar(input_text_frame, orient=HORIZONTAL, command=self.input_text_area.xview)
        self.input_text_area["yscrollcommand"] = sb_y_input.set
        self.input_text_area["xscrollcommand"] = sb_x_input.set
        sb_y_input.pack(side=RIGHT, fill=Y)
        sb_x_input.pack(side=BOTTOM, fill=X)
        self.input_text_area.pack(side=LEFT, fill=BOTH, expand=YES)
        ToolTip(self.input_text_area, "Wklej ścieżki do plików lub URL-e, każdą w nowej linii.")

        self.transcribe_button = ttk.Button(
            top_controls_frame,
            text="🚀 Rozpocznij Przetwarzanie Wsadowe",
            command=self.run_batch_script,
            style="Success.TButton",
        )
        self.transcribe_button.pack(pady=(5, 10), fill=X)
        ToolTip(self.transcribe_button, "Rozpoczyna przetwarzanie wszystkich pozycji z listy.")

        queue_progress_frame = ttk.Frame(self)
        queue_progress_frame.pack(padx=10, pady=5, fill=BOTH, expand=YES)
        ttk.Label(queue_progress_frame, text="Kolejka Przetwarzania:", font=self.font_settings["header"]).pack(anchor=W, pady=(0, 5))

        tree_frame = ttk.Frame(queue_progress_frame)
        tree_frame.pack(side=TOP, fill=BOTH, expand=YES)
        self.files_queue_tree = ttk.Treeview(
            tree_frame,
            columns=("source", "status"),
            show="headings",
            height=5,
            style="Custom.Treeview",
        )
        self.files_queue_tree.heading("source", text="Plik / URL")
        self.files_queue_tree.heading("status", text="Status")
        self.files_queue_tree.column("source", width=450, anchor=W, stretch=YES)
        self.files_queue_tree.column("status", width=150, anchor=W, stretch=NO)
        self.files_queue_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        tree_sb = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.files_queue_tree.yview)
        self.files_queue_tree.configure(yscrollcommand=tree_sb.set)
        tree_sb.pack(side=RIGHT, fill=Y)
        ToolTip(self.files_queue_tree, "Lista plików/URL-i do przetworzenia i ich status.")

        progress_bar_frame = ttk.Frame(queue_progress_frame)
        progress_bar_frame.pack(fill=X, pady=(5, 5), side=BOTTOM)
        self.overall_progress_label = ttk.Label(
            progress_bar_frame,
            text="Postęp: 0/0",
            font=self.font_settings["label"],
        )
        self.overall_progress_label.pack(side=LEFT, padx=(0, 10))
        self.overall_progress = ttk.Progressbar(
            progress_bar_frame,
            mode="determinate",
            length=300,
            bootstyle="primary-striped",
        )
        self.overall_progress.pack(side=LEFT, fill=X, expand=YES)
        ToolTip(self.overall_progress, "Ogólny postęp przetwarzania.")

        self.tabs = ttk.Notebook(self, style="Custom.TNotebook")
        self.tabs.pack(padx=10, pady=10, fill=BOTH, expand=YES)

        self.console_tab = ttk.Frame(self.tabs)
        self.console_text = ScrolledText(
            self.console_tab,
            font=self.font_settings["scrolledtext"],
            wrap="word",
            state=DISABLED,
        )
        self.console_text.pack(fill=BOTH, expand=YES)
        console_btns = ttk.Frame(self.console_tab)
        console_btns.pack(pady=5, fill=X)
        btn_save_log = ttk.Button(
            console_btns,
            text="💾 Zapisz Log",
            command=self.save_console_log,
            style="Outline.TButton",
        )
        btn_save_log.pack(side=LEFT, padx=5)
        ToolTip(btn_save_log, "Zapisuje cały log z konsoli do pliku.")
        self.tabs.add(self.console_tab, text="🖥️ Konsola")

        self.results_manager_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.results_manager_frame, text="📊 Wyniki")
        results_controls_frame = ttk.Frame(self.results_manager_frame)
        results_controls_frame.pack(fill=X, pady=5, padx=5)
        ttk.Label(
            results_controls_frame,
            text="Wybierz przetworzony plik:",
            font=self.font_settings["label"],
        ).pack(side=LEFT, padx=(0, 5))
        self.processed_files_combo = ttk.Combobox(
            results_controls_frame,
            state="readonly",
            font=self.font_settings["default"],
            width=40,
        )
        self.processed_files_combo.pack(side=LEFT, fill=X, expand=YES)
        self.processed_files_combo.bind("<<ComboboxSelected>>", self.display_selected_result)
        ToolTip(self.processed_files_combo, "Wybierz plik, aby zobaczyć jego wyniki.")

        results_display_pane = ttk.Panedwindow(
            self.results_manager_frame,
            orient=HORIZONTAL,
        )
        results_display_pane.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        trans_frame = ttk.Labelframe(results_display_pane, text="📝 Transkrypcja", padding=5)
        self.current_transcription_text = ScrolledText(
            trans_frame,
            font=self.font_settings["scrolledtext"],
            wrap="word",
            state=DISABLED,
            height=10,
        )
        self.current_transcription_text.pack(fill=BOTH, expand=YES)
        results_display_pane.add(trans_frame, weight=1)
        summary_frame = ttk.Labelframe(results_display_pane, text="📌 Streszczenie", padding=5)
        self.current_summary_text = ScrolledText(
            summary_frame,
            font=self.font_settings["scrolledtext"],
            wrap="word",
            state=DISABLED,
            height=10,
        )
        self.current_summary_text.pack(fill=BOTH, expand=YES)
        results_display_pane.add(summary_frame, weight=1)

        self.config_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.config_tab, text="⚙️ Konfiguracja")
        config_outer = ttk.Frame(self.config_tab)
        config_outer.pack(fill=BOTH, expand=YES)
        canvas = ttk.Canvas(config_outer, highlightthickness=0); canvas.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0,10))
        scrollbar = ttk.Scrollbar(config_outer, orient=VERTICAL, command=canvas.yview); scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_inner_config_form = ttk.Frame(canvas)
        canvas.create_window((0,0), window=self.scrollable_inner_config_form, anchor=NW, tags="all_contents_frame_cfg")
        def _on_cfg_resize(event): canvas.configure(scrollregion=canvas.bbox("all")); canvas.itemconfig("all_contents_frame_cfg", width=event.width)
        canvas.bind("<Configure>", _on_cfg_resize)
        self.scrollable_inner_config_form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        save_btn_cfg_cont = ttk.Frame(self.config_tab); save_btn_cfg_cont.pack(fill=X, pady=(5,15), side=BOTTOM)
        btn_save_cfg = ttk.Button(save_btn_cfg_cont, text="💾 Zapisz i Zastosuj",bootstyle="primary",width=20,command=self.save_config_to_file, style="Success.TButton")
        btn_save_cfg.pack(anchor="center"); ToolTip(btn_save_cfg, "Zapisuje konfigurację i stosuje ją.")

        self.fields = {}; self.llm_prompt_template_var = StringVar(); self.custom_llm_prompt_text_widget = None
        self.populate_config_form()

        self.output_queue = queue.Queue()
        self.batch_processing_thread = None
        
        # Initialize ResultsManager
        self.results_manager = ResultsManager()
        
        self.update_widget_fonts()
        self.tabs.select(self.results_manager_frame)


    def update_font_styles(self):
        """Update TTK styles - delegates to FontManager."""
        self.font_manager.update_ttk_styles(self.app_style)


    def update_widget_fonts(self):
        """Update widget fonts - delegates to FontManager."""
        widgets_to_update_map = {
            self.input_text_area: self.font_settings["scrolledtext"],
        }
        if self.custom_llm_prompt_text_widget:
             widgets_to_update_map[self.custom_llm_prompt_text_widget] = self.font_settings["scrolledtext"]
        
        scrolled_widgets = [
            self.console_text,
            self.current_transcription_text,
            self.current_summary_text,
        ]
        
        self.font_manager.update_widget_fonts(widgets_to_update_map, scrolled_widgets)

    def change_font_size(self, delta):
        """Change font size - delegates to FontManager."""
        new_size = self.font_manager.change_font_size(delta)
        self.font_settings = self.font_manager.get_all_fonts()
        self.update_font_styles()
        self.update_widget_fonts()
        if hasattr(self, 'scrollable_inner_config_form'): self.populate_config_form()
        print(f"Rozmiar czcionki zmieniony na bazowy: {new_size}")

    def on_closing(self):
        if self.batch_processing_thread and self.batch_processing_thread.is_alive():
            if messagebox.askyesno("Zakończyć?", "Przetwarzanie jest w toku. Czy na pewno chcesz zakończyć?"): self.destroy()
            else: return
        self.destroy()

    def populate_config_form(self):
        form = self.scrollable_inner_config_form
        for widget in form.winfo_children(): widget.destroy()
        self.fields = {}
        ttk.Label(form, text="--- Podsumowanie ---", font=self.font_settings["header"]).pack(anchor=W, padx=10, pady=(15,5))
        self.add_config_field(form, "Dostawca podsumowania", "SUMMARY_PROVIDER", "System: 'ollama' (lokalnie) lub 'google' (API Gemini).", kind="combo", options=["ollama", "google"])
        self.add_config_field(form, "Język podsumowania", "SUMMARY_LANGUAGE", "np. Polish, English.")
        ttk.Label(form, text="Szablon Promptu LLM", font=self.font_settings["label"]).pack(anchor=W, padx=10, pady=(8,0))
        tpl_cfg = getattr(config_module, "LLM_PROMPT_TEMPLATES", DEFAULT_CONFIG["LLM_PROMPT_TEMPLATES"])
        tpl_names = list(tpl_cfg.keys()) + [CUSTOM_PROMPT_OPTION_TEXT]
        curr_tpl_name = getattr(config_module, "LLM_PROMPT_TEMPLATE_NAME", DEFAULT_CONFIG["LLM_PROMPT_TEMPLATE_NAME"])
        if not curr_tpl_name and getattr(config_module, "LLM_PROMPT", DEFAULT_CONFIG["LLM_PROMPT"]): self.llm_prompt_template_var.set(CUSTOM_PROMPT_OPTION_TEXT)
        elif curr_tpl_name in tpl_names: self.llm_prompt_template_var.set(curr_tpl_name)
        else: self.llm_prompt_template_var.set(tpl_names[0] if tpl_names and tpl_names[0] != CUSTOM_PROMPT_OPTION_TEXT else CUSTOM_PROMPT_OPTION_TEXT)
        self.prompt_template_combo = ttk.Combobox(form, textvariable=self.llm_prompt_template_var, values=tpl_names, state="readonly", font=self.font_settings["default"])
        self.prompt_template_combo.pack(fill=X, expand=True, padx=10, pady=(0,8)); self.prompt_template_combo.bind("<<ComboboxSelected>>", self.on_prompt_template_change)
        ToolTip(self.prompt_template_combo, "Wybierz szablon promptu lub opcję własnego."); self.fields["LLM_PROMPT_TEMPLATE_NAME"] = self.llm_prompt_template_var
        ttk.Label(form, text="Prompt Niestandardowy (dla opcji powyżej)", font=self.font_settings["label"]).pack(anchor=W, padx=10, pady=(8,0))
        cust_prompt_fr = ttk.Frame(form); cust_prompt_fr.pack(fill=BOTH, expand=True, padx=10, pady=(0,8))
        self.custom_llm_prompt_text_widget = Text(cust_prompt_fr, height=5, wrap="word", font=self.font_settings["scrolledtext"], relief=SUNKEN, borderwidth=1)
        self.custom_llm_prompt_text_widget.insert("1.0", getattr(config_module, "LLM_PROMPT", DEFAULT_CONFIG.get("LLM_PROMPT")))
        self.custom_llm_prompt_text_widget.pack(fill=BOTH, expand=True)
        ToolTip(self.custom_llm_prompt_text_widget, "Wpisz własny prompt. Język i tekst dodane automatycznie."); self.fields["LLM_PROMPT"] = self.custom_llm_prompt_text_widget
        self.on_prompt_template_change()
        ttk.Label(form, text="--- Ustawienia Ollama (dla 'ollama') ---", font=self.font_settings["header"]).pack(anchor=W, padx=10, pady=(15,5))
        self.add_config_field(form, "Model Ollama", "OLLAMA_MODEL", "Model LLM w Ollama.")
        ttk.Label(form, text="--- Ustawienia Google Gemini (dla 'google') ---", font=self.font_settings["header"]).pack(anchor=W, padx=10, pady=(15,5))
        self.add_config_field(form, "Klucz Google API", "GOOGLE_API_KEY", "Klucz API Google Gemini.")
        self.add_config_field(form, "Model Google Gemini", "GOOGLE_GEMINI_MODEL", "Model Google Gemini.")
        ttk.Label(form, text="--- Transkrypcja (Faster Whisper) ---", font=self.font_settings["header"]).pack(anchor=W, padx=10, pady=(15,5))
        self.add_config_field(form, "Język transkrypcji", "WHISPER_LANGUAGE", "np. Polish, English.")
        self.add_config_field(form, "Model Whisper", "WHISPER_MODEL", "Model Faster Whisper.")
        self.add_config_field(form, "Włącz diaryzację", "ENABLE_SPEAKER_DIARIZATION", "Rozpoznawanie mówców.", kind="bool")
        self.add_config_field(form, "Prefiks mówcy", "DIARIZE_SPEAKER_PREFIX", "Prefiks dla mówców, np. MÓWCA.")
        self.add_config_field(form, "Metoda diaryzacji", "DIARIZE_METHOD", "Metoda diaryzacji, np. pyannote_v3.1.")
        ttk.Label(form, text="--- Ogólne Ustawienia Skryptu ---", font=self.font_settings["header"]).pack(anchor=W, padx=10, pady=(15,5))
        self.add_config_field(form, "Format transkrypcji (wewn.)", "TRANSCRIPTION_FORMAT", "Format pliku transkrypcji (txt, srt, etc).")
        self.add_config_field(form, "Bazowa nazwa pobranego audio", "DOWNLOADED_AUDIO_FILENAME", "Nazwa tymczasowego pliku audio z YouTube.")
        self.add_config_field(form, "Plik yt-dlp", "YT_DLP_EXE", "Ścieżka do yt-dlp.exe.")
        self.add_config_field(form, "Plik Faster Whisper", "FASTER_WHISPER_EXE", "Ścieżka do faster-whisper-xxl.exe.")
        self.add_config_field(form, "Tryb Debugowania", "DEBUG_MODE", "Włącza szczegółowe logowanie.", kind="bool")

    def on_prompt_template_change(self, event=None):
        is_custom = self.llm_prompt_template_var.get() == CUSTOM_PROMPT_OPTION_TEXT
        self.custom_llm_prompt_text_widget.config(state=NORMAL if is_custom else DISABLED, relief="solid" if is_custom else "flat", background="white" if is_custom else "#f0f0f0")
        if not is_custom:
            selected_key = self.llm_prompt_template_var.get(); templates = getattr(config_module, "LLM_PROMPT_TEMPLATES", DEFAULT_CONFIG["LLM_PROMPT_TEMPLATES"])
            if selected_key in templates:
                self.custom_llm_prompt_text_widget.config(state=NORMAL); self.custom_llm_prompt_text_widget.delete("1.0", END)
                self.custom_llm_prompt_text_widget.insert("1.0", templates[selected_key]); self.custom_llm_prompt_text_widget.config(state=DISABLED, relief="flat", background="#f0f0f0")

    def add_config_field(self, parent, label, key, tooltip, kind="entry", default_value_key=None, options=None):
        if default_value_key is None: default_value_key = key
        ttk.Label(parent, text=label, font=self.font_settings["label"]).pack(anchor=W, padx=10, pady=(8,0))
        current_value = getattr(config_module, key, DEFAULT_CONFIG.get(default_value_key))
        if kind == "entry":
            var = StringVar(value=str(current_value)); entry_frame = ttk.Frame(parent); entry_frame.pack(fill=X, expand=True, padx=10, pady=(0,8))
            entry = ttk.Entry(entry_frame, textvariable=var, font=self.font_settings["default"]); entry.pack(side=LEFT, fill=X, expand=True)
            if key in ["FASTER_WHISPER_EXE", "YT_DLP_EXE"]:
                def browse_exe(v=var, t=f"Wybierz {label}"):
                    file_path = filedialog.askopenfilename(title=t, filetypes=[("Pliki EXE", "*.exe"),("Wszystkie", "*.*")])
                    if file_path: v.set(file_path) # Check if a file was selected
                ttk.Button(entry_frame, text="📂", width=3, command=browse_exe, style="Outline.TButton").pack(side=RIGHT, padx=5)
            ToolTip(entry, tooltip); self.fields[key] = var
        elif kind == "bool":
            var = BooleanVar(value=bool(current_value)); cb = ttk.Checkbutton(parent, text="Włączone", variable=var, style="Switch.TCheckbutton")
            cb.pack(fill=X, expand=True, padx=10, pady=(0,8), anchor=W); ToolTip(cb, tooltip); self.fields[key] = var
        elif kind == "combo":
            var = StringVar(value=str(current_value)); combo = ttk.Combobox(parent, textvariable=var, values=options or [], state="readonly", font=self.font_settings["default"])
            combo.pack(fill=X, expand=True, padx=10, pady=(0,8)); ToolTip(combo, tooltip); self.fields[key] = var

    def browse_and_add_files(self):
        paths = filedialog.askopenfilenames(title="Wybierz pliki audio", filetypes=[("Audio", "*.mp3 *.wav *.m4a *.ogg *.flac"), ("All", "*.*")])
        if paths:
            current_text = self.input_text_area.get("1.0", END).strip()
            new_lines = "\n".join(paths)
            if current_text: self.input_text_area.insert(END, "\n" + new_lines + "\n")
            else: self.input_text_area.insert("1.0", new_lines + "\n")

    def _get_save_name_base(self): return "pogadane_batch_results"
    def _save_file_dialog(self, getter, suffix, title, f_desc):
        fp = filedialog.asksaveasfilename(initialfile=self._get_save_name_base()+suffix, defaultextension=suffix.split('.')[-1], filetypes=[(f_desc, f"*{suffix}"), ("All", "*.*")])
        if fp:
            try:
                with open(fp, "w", encoding="utf-8") as f: f.write(getter())
                messagebox.showinfo("Zapisano", f"{title} zapisany do {fp}")
            except Exception as e: messagebox.showerror("Błąd zapisu", f"Nie można zapisać {title.lower()}: {e}")
    def save_console_log(self): self._save_file_dialog(lambda: self.console_text.get("1.0", "end-1c"), ".console_log.txt", "Log konsoli", "Pliki tekstowe")

    def save_config_to_file(self):
        try:
            content = ["# config.py - wygenerowany przez Pogadane GUI\n"]; order = ["FASTER_WHISPER_EXE", "YT_DLP_EXE", "WHISPER_LANGUAGE", "WHISPER_MODEL", "ENABLE_SPEAKER_DIARIZATION", "DIARIZE_METHOD", "DIARIZE_SPEAKER_PREFIX", "SUMMARY_PROVIDER", "SUMMARY_LANGUAGE", "LLM_PROMPT_TEMPLATES", "LLM_PROMPT_TEMPLATE_NAME", "LLM_PROMPT", "OLLAMA_MODEL", "GOOGLE_API_KEY", "GOOGLE_GEMINI_MODEL", "TRANSCRIPTION_FORMAT", "DOWNLOADED_AUDIO_FILENAME", "DEBUG_MODE"]
            cfg_dict = {}
            for k in order:
                if k == "LLM_PROMPT_TEMPLATES": cfg_dict[k] = getattr(config_module, k, DEFAULT_CONFIG.get(k)); continue
                if k in self.fields: var = self.fields[k]; cfg_dict[k] = var.get("1.0", "end-1c").strip() if isinstance(var, Text) else (var.get() if isinstance(var, BooleanVar) else var.get())
                else: cfg_dict[k] = getattr(config_module, k, DEFAULT_CONFIG.get(k))
            if cfg_dict.get("LLM_PROMPT_TEMPLATE_NAME") == CUSTOM_PROMPT_OPTION_TEXT: cfg_dict["LLM_PROMPT_TEMPLATE_NAME"] = ""
            for k in order:
                val = cfg_dict.get(k, DEFAULT_CONFIG.get(k))
                if k == "LLM_PROMPT_TEMPLATES": content.append(f"{k.upper()} = {repr(val)}")
                elif isinstance(val, bool): content.append(f"{k.upper()} = {val}")
                elif isinstance(val, (int, float)) and not isinstance(val, bool): content.append(f"{k.upper()} = {val}")
                else: content.append(f"{k.upper()} = {repr(str(val))}")
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file_path, "w", encoding="utf-8") as f: f.write("\n".join(content) + "\n")
            messagebox.showinfo("Zapisano", f"Konfiguracja zapisana do {self.config_file_path}.\nZmiany zostaną zastosowane.")
            config_manager.reload(); self.populate_config_form()
        except Exception as e: messagebox.showerror("Błąd zapisu konfiguracji", str(e))


    def run_batch_script(self):
        sources = [l.strip() for l in self.input_text_area.get("1.0", END).strip().splitlines() if l.strip()]
        if not sources: messagebox.showwarning("Brak danych", "Wprowadź źródła."); return
        self.total_to_process = len(sources); self.current_processed_count = 0
        self.results_manager.clear_all(); self.processed_files_combo['values'] = []; self.processed_files_combo.set('')
        for w in [self.current_transcription_text, self.current_summary_text]: w.text.config(state=NORMAL); w.text.delete("1.0", END); w.text.config(state=DISABLED)
        [self.files_queue_tree.delete(i) for i in self.files_queue_tree.get_children()]
        for i,s_val in enumerate(sources): # Zmiana nazwy zmiennej src na s_val
            display_name = Path(s_val).name if len(s_val) < 60 else s_val[:57]+"..."
            self.files_queue_tree.insert("", END, iid=str(i), values=(display_name, FILE_STATUS_PENDING))

        self.overall_progress['value'] = 0; self.overall_progress_label.config(text=f"Postęp: 0/{self.total_to_process}")
        self.transcribe_button.config(state=DISABLED, text="⏳ Przetwarzanie..."); self.console_text.config(state=NORMAL); self.console_text.delete("1.0", END); self.tabs.select(self.console_tab)
        self.batch_processing_thread = threading.Thread(target=self._execute_batch_processing_logic, args=(sources,), daemon=True); self.batch_processing_thread.start()
        self._poll_output_queue_for_batch()

    def _execute_batch_processing_logic(self, input_sources):
        script_path = self.base_path / "transcribe_summarize_working.py"
        if not script_path.exists(): self.output_queue.put(("error", f"BŁĄD: Nie znaleziono {script_path}\n", "")); self.output_queue.put(("finished_all", "", "")); return
        for i, input_src in enumerate(input_sources):
            self.output_queue.put(("update_status", str(i), FILE_STATUS_PROCESSING))
            self.output_queue.put(("log", f"\n--- ({i+1}/{self.total_to_process}) START: {input_src} ---\n", input_src))
            stdout_lines = []
            cmd = [sys.executable, "-u", str(script_path), input_src] # Przekaż jedno źródło
            cmd.append("--diarize" if getattr(config_module, 'ENABLE_SPEAKER_DIARIZATION', False) else "--no-diarize")
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", cwd=str(self.base_path), startupinfo=None if os.name!='nt' else subprocess.STARTUPINFO(dwFlags=subprocess.CREATE_NO_WINDOW))
                if proc.stdout:
                    for line in iter(proc.stdout.readline, ''): clean = strip_ansi(line); stdout_lines.append(clean); self.output_queue.put(("log", clean, input_src))
                    proc.stdout.close()
                proc.wait()
                log_for_file = "".join(stdout_lines); trans, summ = extract_transcription_and_summary(log_for_file)
                if proc.returncode == 0: self.output_queue.put(("update_status", str(i), FILE_STATUS_COMPLETED)); self.output_queue.put(("result", input_src, trans, summ)); self.output_queue.put(("log", f"--- ({i+1}/{self.total_to_process}) OK: {input_src} ---\n", input_src))
                else: self.output_queue.put(("update_status", str(i), FILE_STATUS_ERROR)); self.output_queue.put(("error", f"Błąd {input_src} (kod: {proc.returncode})\nLog w konsoli.\n", input_src)); self.output_queue.put(("log", f"--- ({i+1}/{self.total_to_process}) BŁĄD: {input_src} (kod: {proc.returncode}) ---\n", input_src))
            except Exception as e: self.output_queue.put(("update_status", str(i), FILE_STATUS_ERROR)); self.output_queue.put(("error", f"Krytyczny błąd dla {input_src}: {e}\n", input_src))
        self.output_queue.put(("finished_all", "", ""))

    def _poll_output_queue_for_batch(self):
        try:
            while True:
                message = self.output_queue.get_nowait()
                # Safely unpack message - handle variable length tuples
                msg_type = message[0] if len(message) > 0 else None
                data1 = message[1] if len(message) > 1 else ""
                data2 = message[2] if len(message) > 2 else ""
                summary_data = message[3] if len(message) > 3 else ""

                if msg_type == "log": self.console_text.config(state=NORMAL); self.console_text.insert(END, data1); self.console_text.see(END); self.console_text.config(state=DISABLED)
                elif msg_type == "error": self.console_text.config(state=NORMAL); self.console_text.insert(END, data1, "error_tag"); self.console_text.see(END); self.console_text.tag_configure("error_tag", foreground="red", font=self.font_settings["scrolledtext"]); self.console_text.config(state=DISABLED)
                elif msg_type == "update_status": item_id = data1; status_text = data2; (self.files_queue_tree.exists(item_id) and self.files_queue_tree.set(item_id, "status", status_text))
                elif msg_type == "result":
                    src_name, trans, summ = data1, data2, summary_data # summary_data to teraz poprawnie summ
                    self.results_manager.add_result(src_name, trans, summ)
                    combo_vals = list(self.processed_files_combo['values']); (src_name not in combo_vals and self.processed_files_combo.config(values=combo_vals + [src_name]))
                    (not self.processed_files_combo.get() and (self.processed_files_combo.set(src_name), self.display_selected_result()))
                    self.current_processed_count +=1; self.overall_progress['value'] = (self.current_processed_count / self.total_to_process) * 100
                    self.overall_progress_label.config(text=f"Postęp: {self.current_processed_count}/{self.total_to_process}")
                elif msg_type == "finished_all": self._finalize_batch_run(); return
        except queue.Empty:
            if self.batch_processing_thread and self.batch_processing_thread.is_alive(): self.after(100, self._poll_output_queue_for_batch)
            else: self._finalize_batch_run()

    def display_selected_result(self, event=None):
        """Display selected result using ResultsManager."""
        selected_src = self.processed_files_combo.get()
        self.results_manager.display_result(
            selected_src,
            self.current_transcription_text,
            self.current_summary_text,
            insert_with_markdown
        )

    def _finalize_batch_run(self):
        self.overall_progress_label.config(text=f"Ukończono: {self.current_processed_count}/{self.total_to_process}")
        if self.current_processed_count == self.total_to_process : self.overall_progress['value'] = 100
        self.transcribe_button.config(state=NORMAL, text="🚀 Rozpocznij Przetwarzanie Wsadowe")
        self.console_text.config(state=DISABLED)
        if self.processed_files_combo['values']:
            self.tabs.select(self.results_manager_frame)
            if not self.processed_files_combo.get(): self.processed_files_combo.current(0)
            self.display_selected_result()
        else: self.tabs.select(self.console_tab)
        messagebox.showinfo("Zakończono", f"Przetwarzanie wsadowe {self.total_to_process} źródeł zakończone.")
        self.batch_processing_thread = None

if __name__ == "__main__":
    if hasattr(sys, 'frozen') and sys.platform == 'win32' and sys.stdout is None: sys.stdout = open(os.devnull, 'w'); sys.stderr = open(os.devnull, 'w')
    app = TranscriberApp()
    app.mainloop()