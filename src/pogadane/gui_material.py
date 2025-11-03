"""
Pogadane GUI - Material Design Version
Modern Material Design interface using CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, StringVar, BooleanVar, END
import threading
import queue
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

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
from .text_utils import strip_ansi, extract_transcription_and_summary
from .config_loader import ConfigManager
from .gui_utils import ResultsManager

# Set appearance mode and color theme
ctk.set_appearance_mode("system")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class MaterialTooltip:
    """Material Design inspired tooltip"""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self._after_id = None
        
        widget.bind("<Enter>", self.schedule_show)
        widget.bind("<Leave>", self.hide)
        widget.bind("<ButtonPress>", self.hide)
    
    def schedule_show(self, event):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
        self._after_id = self.widget.after(self.delay, lambda: self.show())
    
    def show(self):
        if self.tooltip_window or not self.widget.winfo_exists():
            return
        
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_attributes("-topmost", True)
        
        # Material Design shadow effect
        label = ctk.CTkLabel(
            self.tooltip_window,
            text=self.text,
            fg_color=("#2B2B2B", "#E0E0E0"),
            text_color=("#FFFFFF", "#000000"),
            corner_radius=6,
            padx=12,
            pady=8,
            font=("Segoe UI", 11)
        )
        label.pack()
        
        self.tooltip_window.update_idletasks()
        screen_width = self.tooltip_window.winfo_screenwidth()
        tip_width = self.tooltip_window.winfo_width()
        
        if x + tip_width > screen_width:
            x = screen_width - tip_width - 10
        if x < 10:
            x = 10
        
        self.tooltip_window.wm_geometry(f"+{int(x)}+{int(y)}")
    
    def hide(self, event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class PogadaneGUI(ctk.CTk):
    """Main Pogadane GUI Application with Material Design"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("🎧 Pogadane - Transkrybuj & Streść")
        self.geometry("1100x850")
        self.minsize(900, 700)
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        self.config_manager.initialize()
        self.config_module = self.config_manager.config
        
        # Initialize variables
        self.output_queue = queue.Queue()
        self.batch_processing_thread = None
        self.results_manager = ResultsManager()
        self.fields: Dict = {}
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create UI components
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
        # Configure close protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_header(self):
        """Create Material Design header with app title and controls"""
        header_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray13"), corner_radius=0, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # App icon and title
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        app_label = ctk.CTkLabel(
            title_frame,
            text="🎧 Pogadane",
            font=("Segoe UI", 28, "bold"),
            text_color=("#1976D2", "#64B5F6")
        )
        app_label.pack(side="left", padx=(0, 10))
        
        version_label = ctk.CTkLabel(
            title_frame,
            text=f"v{APP_VERSION}",
            font=("Segoe UI", 12),
            text_color=("gray40", "gray60")
        )
        version_label.pack(side="left")
        
        # Theme and font controls
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=1, sticky="e", padx=20, pady=15)
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            controls_frame,
            text="🌙 Tryb Ciemny",
            command=self.toggle_theme,
            font=("Segoe UI", 12)
        )
        self.theme_switch.pack(side="left", padx=10)
        MaterialTooltip(self.theme_switch, "Przełącz między trybem jasnym a ciemnym")
        
        # Font size controls
        font_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        font_frame.pack(side="left", padx=10)
        
        self.font_minus_btn = ctk.CTkButton(
            font_frame,
            text="A-",
            width=40,
            height=32,
            command=lambda: self.change_font_size(-1),
            font=("Segoe UI", 14, "bold")
        )
        self.font_minus_btn.pack(side="left", padx=2)
        MaterialTooltip(self.font_minus_btn, "Zmniejsz rozmiar czcionki")
        
        self.font_plus_btn = ctk.CTkButton(
            font_frame,
            text="A+",
            width=40,
            height=32,
            command=lambda: self.change_font_size(1),
            font=("Segoe UI", 14, "bold")
        )
        self.font_plus_btn.pack(side="left", padx=2)
        MaterialTooltip(self.font_plus_btn, "Zwiększ rozmiar czcionki")
    
    def create_main_content(self):
        """Create main content area with tabs"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        # Input section
        self.create_input_section(main_container)
        
        # Tabview for different sections
        self.tabview = ctk.CTkTabview(main_container, corner_radius=10)
        self.tabview.grid(row=1, column=0, sticky="nsew", pady=(15, 0))
        
        # Add tabs
        self.tab_console = self.tabview.add("🖥️ Konsola")
        self.tab_results = self.tabview.add("📊 Wyniki")
        self.tab_config = self.tabview.add("⚙️ Konfiguracja")
        
        # Configure tabs
        self.create_console_tab()
        self.create_results_tab()
        self.create_config_tab()
    
    def create_input_section(self, parent):
        """Create input section for files and URLs"""
        input_frame = ctk.CTkFrame(parent, corner_radius=10)
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 0))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Label and browse button row
        label_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        label_row.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        label_row.grid_columnconfigure(0, weight=1)
        
        input_label = ctk.CTkLabel(
            label_row,
            text="🎙️ Pliki audio / URL-e YouTube (każdy w nowej linii):",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        )
        input_label.grid(row=0, column=0, sticky="w")
        
        browse_btn = ctk.CTkButton(
            label_row,
            text="➕ Dodaj Pliki",
            width=140,
            height=36,
            command=self.browse_and_add_files,
            font=("Segoe UI", 13),
            corner_radius=8
        )
        browse_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))
        MaterialTooltip(browse_btn, "Wybierz pliki audio z dysku")
        
        # Text input area
        self.input_text = ctk.CTkTextbox(
            input_frame,
            height=100,
            font=("Consolas", 12),
            corner_radius=8,
            border_width=2
        )
        self.input_text.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        MaterialTooltip(self.input_text, "Wklej ścieżki do plików lub URL-e YouTube, każdą w nowej linii")
        
        # Process button and queue
        button_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_row.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        button_row.grid_columnconfigure(0, weight=1)
        
        self.process_btn = ctk.CTkButton(
            button_row,
            text="🚀 Rozpocznij Przetwarzanie Wsadowe",
            height=45,
            command=self.run_batch_script,
            font=("Segoe UI", 15, "bold"),
            fg_color=("#2E7D32", "#66BB6A"),
            hover_color=("#1B5E20", "#81C784"),
            corner_radius=10
        )
        self.process_btn.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        MaterialTooltip(self.process_btn, "Rozpocznij przetwarzanie wszystkich pozycji")
        
        # Queue label
        queue_label = ctk.CTkLabel(
            button_row,
            text="Kolejka Przetwarzania:",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        )
        queue_label.grid(row=1, column=0, sticky="w", pady=(0, 8))
        
        # Queue frame with scrollable text
        queue_frame = ctk.CTkFrame(button_row, corner_radius=8, border_width=2)
        queue_frame.grid(row=2, column=0, sticky="ew")
        queue_frame.grid_columnconfigure(0, weight=1)
        
        # Queue headers
        headers_frame = ctk.CTkFrame(queue_frame, fg_color=("gray85", "gray20"))
        headers_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        headers_frame.grid_columnconfigure(0, weight=3)
        headers_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            headers_frame,
            text="Plik / URL",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=15, pady=8)
        
        ctk.CTkLabel(
            headers_frame,
            text="Status",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        ).grid(row=0, column=1, sticky="w", padx=15, pady=8)
        
        # Queue textbox
        self.queue_text = ctk.CTkTextbox(
            queue_frame,
            height=120,
            font=("Consolas", 11),
            corner_radius=0
        )
        self.queue_text.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.queue_text.configure(state="disabled")
        
        # Progress bar
        progress_frame = ctk.CTkFrame(button_row, fg_color="transparent")
        progress_frame.grid(row=3, column=0, sticky="ew", pady=(15, 0))
        progress_frame.grid_columnconfigure(1, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Postęp: 0/0",
            font=("Segoe UI", 12),
            width=100
        )
        self.progress_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=20,
            corner_radius=10
        )
        self.progress_bar.grid(row=0, column=1, sticky="ew")
        self.progress_bar.set(0)
    
    def create_console_tab(self):
        """Create console output tab"""
        self.tab_console.grid_columnconfigure(0, weight=1)
        self.tab_console.grid_rowconfigure(0, weight=1)
        
        # Console textbox
        self.console_text = ctk.CTkTextbox(
            self.tab_console,
            font=("Consolas", 11),
            corner_radius=8,
            border_width=2
        )
        self.console_text.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 10))
        
        # Console buttons
        btn_frame = ctk.CTkFrame(self.tab_console, fg_color="transparent")
        btn_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        save_log_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Zapisz Log",
            width=140,
            command=self.save_console_log,
            font=("Segoe UI", 13),
            corner_radius=8
        )
        save_log_btn.pack(side="left")
        MaterialTooltip(save_log_btn, "Zapisz logi do pliku")
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Wyczyść",
            width=140,
            command=self.clear_console,
            font=("Segoe UI", 13),
            corner_radius=8,
            fg_color=("gray70", "gray30")
        )
        clear_btn.pack(side="left", padx=(10, 0))
        MaterialTooltip(clear_btn, "Wyczyść konsolę")
    
    def create_results_tab(self):
        """Create results display tab"""
        self.tab_results.grid_columnconfigure(0, weight=1)
        self.tab_results.grid_rowconfigure(1, weight=1)
        
        # File selector
        selector_frame = ctk.CTkFrame(self.tab_results, fg_color="transparent")
        selector_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        selector_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            selector_frame,
            text="Wybierz przetworzony plik:",
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.files_combo = ctk.CTkComboBox(
            selector_frame,
            font=("Segoe UI", 12),
            command=self.display_selected_result,
            state="readonly"
        )
        self.files_combo.grid(row=0, column=1, sticky="ew")
        self.files_combo.set("")
        MaterialTooltip(self.files_combo, "Wybierz plik aby zobaczyć wyniki")
        
        # Results display (split view)
        results_frame = ctk.CTkFrame(self.tab_results, fg_color="transparent")
        results_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_columnconfigure(1, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Transcription frame
        trans_frame = ctk.CTkFrame(results_frame, corner_radius=10)
        trans_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        trans_frame.grid_columnconfigure(0, weight=1)
        trans_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            trans_frame,
            text="📝 Transkrypcja",
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=12)
        
        self.transcription_text = ctk.CTkTextbox(
            trans_frame,
            font=("Consolas", 11),
            corner_radius=8,
            border_width=2
        )
        self.transcription_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Summary frame
        summary_frame = ctk.CTkFrame(results_frame, corner_radius=10)
        summary_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            summary_frame,
            text="📌 Streszczenie",
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=12)
        
        self.summary_text = ctk.CTkTextbox(
            summary_frame,
            font=("Consolas", 11),
            corner_radius=8,
            border_width=2
        )
        self.summary_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
    
    def create_config_tab(self):
        """Create configuration tab"""
        self.tab_config.grid_columnconfigure(0, weight=1)
        self.tab_config.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame
        config_scroll = ctk.CTkScrollableFrame(
            self.tab_config,
            corner_radius=10
        )
        config_scroll.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        config_scroll.grid_columnconfigure(0, weight=1)
        
        # Populate configuration form
        self.populate_config_form(config_scroll)
        
        # Save button
        save_frame = ctk.CTkFrame(self.tab_config, fg_color="transparent")
        save_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        save_btn = ctk.CTkButton(
            save_frame,
            text="💾 Zapisz i Zastosuj",
            height=45,
            command=self.save_config_to_file,
            font=("Segoe UI", 14, "bold"),
            fg_color=("#1976D2", "#64B5F6"),
            hover_color=("#1565C0", "#42A5F5"),
            corner_radius=10
        )
        save_btn.pack(fill="x")
        MaterialTooltip(save_btn, "Zapisz konfigurację i zastosuj zmiany")
    
    def populate_config_form(self, parent):
        """Populate configuration form with settings"""
        row = 0
        
        # Summary Settings
        section_label = ctk.CTkLabel(
            parent,
            text="🤖 Ustawienia Podsumowania",
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        )
        section_label.grid(row=row, column=0, sticky="w", padx=15, pady=(15, 10))
        row += 1
        
        # Summary Provider
        self.add_config_field(
            parent, row, "Dostawca podsumowania", "SUMMARY_PROVIDER",
            "System: 'ollama' (lokalnie), 'transformers' (Python), lub 'google' (API Gemini)",
            kind="combo", options=["ollama", "transformers", "google"]
        )
        row += 1
        
        # Summary Language
        self.add_config_field(
            parent, row, "Język podsumowania", "SUMMARY_LANGUAGE",
            "np. Polish, English"
        )
        row += 1
        
        # Ollama Model
        self.add_config_field(
            parent, row, "Model Ollama", "OLLAMA_MODEL",
            "np. gemma3:4b, llama2:7b"
        )
        row += 1
        
        # Transformers Model
        self.add_config_field(
            parent, row, "Model Transformers", "TRANSFORMERS_MODEL",
            "np. facebook/bart-large-cnn, google/flan-t5-small"
        )
        row += 1
        
        # Google API Key
        self.add_config_field(
            parent, row, "Klucz API Google", "GOOGLE_API_KEY",
            "Twój klucz API Google Gemini", password=True
        )
        row += 1
        
        # Divider
        ctk.CTkFrame(parent, height=2, fg_color=("gray70", "gray30")).grid(
            row=row, column=0, sticky="ew", padx=15, pady=20
        )
        row += 1
        
        # Transcription Settings
        section_label = ctk.CTkLabel(
            parent,
            text="🎙️ Ustawienia Transkrypcji",
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        )
        section_label.grid(row=row, column=0, sticky="w", padx=15, pady=(15, 10))
        row += 1
        
        # Transcription Provider
        self.add_config_field(
            parent, row, "Dostawca transkrypcji", "TRANSCRIPTION_PROVIDER",
            "System: 'faster-whisper' (binarny) lub 'whisper' (Python)",
            kind="combo", options=["faster-whisper", "whisper"]
        )
        row += 1
        
        # Whisper Language
        self.add_config_field(
            parent, row, "Język transkrypcji", "WHISPER_LANGUAGE",
            "np. Polish, English, auto"
        )
        row += 1
        
        # Whisper Model
        self.add_config_field(
            parent, row, "Model Whisper", "WHISPER_MODEL",
            "np. tiny, base, small, medium, large, turbo"
        )
        row += 1
        
        # Faster Whisper EXE Path
        self.add_config_field(
            parent, row, "Plik Faster Whisper", "FASTER_WHISPER_EXE",
            "Ścieżka do faster-whisper-xxl.exe", kind="file"
        )
        row += 1
        
        # YT-DLP Path
        self.add_config_field(
            parent, row, "Plik yt-dlp", "YT_DLP_EXE",
            "Ścieżka do yt-dlp.exe", kind="file"
        )
        row += 1
        
        # Diarization
        self.add_config_field(
            parent, row, "Włącz diaryzację", "ENABLE_SPEAKER_DIARIZATION",
            "Rozpoznawanie różnych mówców", kind="bool"
        )
        row += 1
    
    def add_config_field(self, parent, row, label_text, config_key, tooltip_text, 
                        kind="entry", options=None, password=False):
        """Add a configuration field to the form"""
        # Label
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Segoe UI", 13),
            anchor="w"
        )
        label.grid(row=row, column=0, sticky="w", padx=15, pady=(8, 4))
        MaterialTooltip(label, tooltip_text)
        
        # Get current value from config
        current_value = getattr(self.config_module, config_key, DEFAULT_CONFIG.get(config_key, ""))
        
        # Create appropriate widget
        if kind == "bool":
            var = BooleanVar(value=current_value)
            widget = ctk.CTkSwitch(
                parent,
                text="",
                variable=var,
                font=("Segoe UI", 12)
            )
            self.fields[config_key] = var
        elif kind == "combo":
            var = StringVar(value=str(current_value))
            widget = ctk.CTkComboBox(
                parent,
                values=options or [],
                variable=var,
                font=("Segoe UI", 12),
                state="readonly"
            )
            self.fields[config_key] = var
        elif kind == "file":
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            var = StringVar(value=str(current_value))
            entry = ctk.CTkEntry(
                frame,
                textvariable=var,
                font=("Segoe UI", 12)
            )
            entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
            
            browse_btn = ctk.CTkButton(
                frame,
                text="📂",
                width=40,
                command=lambda: self.browse_file(var),
                font=("Segoe UI", 14)
            )
            browse_btn.pack(side="right")
            widget = frame
            self.fields[config_key] = var
        else:
            var = StringVar(value=str(current_value))
            widget = ctk.CTkEntry(
                parent,
                textvariable=var,
                font=("Segoe UI", 12),
                show="●" if password else ""
            )
            self.fields[config_key] = var
        
        widget.grid(row=row+1, column=0, sticky="ew", padx=15, pady=(0, 12))
        MaterialTooltip(widget, tooltip_text)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray13"), corner_radius=0, height=35)
        status_frame.grid(row=2, column=0, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✅ Gotowy",
            font=("Segoe UI", 11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=15)
        
        self.file_count_label = ctk.CTkLabel(
            status_frame,
            text="Plików: 0",
            font=("Segoe UI", 11),
            anchor="e"
        )
        self.file_count_label.grid(row=0, column=1, sticky="e", padx=15)
    
    # ====================
    # Event Handlers
    # ====================
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "Dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)
    
    def change_font_size(self, delta):
        """Change application font size"""
        # Implement font scaling logic
        print(f"Font size change: {delta}")
        self.update_status("Rozmiar czcionki zmieniony")
    
    def browse_and_add_files(self):
        """Browse for audio files and add to input"""
        files = filedialog.askopenfilenames(
            title="Wybierz pliki audio",
            filetypes=[
                ("Pliki audio", "*.mp3 *.wav *.m4a *.ogg *.flac"),
                ("Wszystkie pliki", "*.*")
            ]
        )
        if files:
            current_text = self.input_text.get("1.0", END).strip()
            new_text = "\n".join(files)
            if current_text:
                self.input_text.insert(END, "\n" + new_text)
            else:
                self.input_text.insert("1.0", new_text)
            self.update_status(f"Dodano {len(files)} plik(ów)")
    
    def browse_file(self, var):
        """Browse for a single file"""
        file = filedialog.askopenfilename()
        if file:
            var.set(file)
    
    def run_batch_script(self):
        """Start batch processing"""
        input_text = self.input_text.get("1.0", END).strip()
        if not input_text:
            messagebox.showwarning("Brak danych", "Proszę wprowadzić pliki lub URL-e")
            return
        
        self.update_status("Rozpoczynam przetwarzanie...")
        self.process_btn.configure(state="disabled")
        
        # Start processing in background thread
        # TODO: Implement actual processing logic
        messagebox.showinfo("Info", "Przetwarzanie zostanie wkrótce zaimplementowane")
        self.process_btn.configure(state="normal")
    
    def save_console_log(self):
        """Save console output to file"""
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(self.console_text.get("1.0", END))
            self.update_status(f"Log zapisany: {file}")
    
    def clear_console(self):
        """Clear console output"""
        self.console_text.delete("1.0", END)
        self.update_status("Konsola wyczyszczona")
    
    def display_selected_result(self, choice):
        """Display selected file results"""
        # TODO: Implement results display logic
        pass
    
    def save_config_to_file(self):
        """Save configuration to file"""
        try:
            config_path = self.config_manager.config_path
            
            # Build config content
            config_lines = ["# Pogadane Configuration\n\n"]
            
            for key, var in self.fields.items():
                value = var.get()
                if isinstance(value, bool):
                    config_lines.append(f"{key} = {value}\n")
                elif isinstance(value, str):
                    config_lines.append(f'{key} = "{value}"\n')
                else:
                    config_lines.append(f"{key} = {value}\n")
            
            # Write to file
            with open(config_path, 'w', encoding='utf-8') as f:
                f.writelines(config_lines)
            
            # Reload config
            self.config_manager.reload()
            self.config_module = self.config_manager.config
            
            messagebox.showinfo("Sukces", "Konfiguracja zapisana pomyślnie!")
            self.update_status("Konfiguracja zapisana")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać konfiguracji:\n{str(e)}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.configure(text=message)
        self.after(3000, lambda: self.status_label.configure(text="✅ Gotowy"))
    
    def on_closing(self):
        """Handle window close event"""
        if self.batch_processing_thread and self.batch_processing_thread.is_alive():
            if messagebox.askyesno("Zakończyć?", 
                                 "Przetwarzanie jest w toku. Czy na pewno chcesz zakończyć?"):
                self.destroy()
        else:
            self.destroy()


def main():
    """Main entry point for the GUI application"""
    app = PogadaneGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
