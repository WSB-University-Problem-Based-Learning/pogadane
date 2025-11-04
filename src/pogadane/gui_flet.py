"""
Pogadane GUI - Material 3 Expressive
Beautiful Material Design 3 interface using Flet (Flutter-based)
"""

import flet as ft
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


class PogadaneApp:
    """Main Pogadane Application with Material 3 Expressive Design"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Pogadane"
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Start with light mode
        self.page.padding = 0
        self.page.window_width = 1200
        self.page.window_height = 1000  # Increased from 900 to prevent cropping
        self.page.window_min_width = 900
        self.page.window_min_height = 800  # Increased from 700
        
        # Set custom icon (window icon and favicon)
        icon_path = Path(__file__).parent.parent.parent / "res" / "assets" / "pogadane-icon.ico"
        if icon_path.exists():
            self.page.window_icon = str(icon_path)
            # For web version, set as favicon
            self.page.web_icon = str(icon_path)
        
        # Pogadane Brand Color Palette - Material 3 Expressive
        # Light Theme
        light_theme = ft.ColorScheme(
            # Primary - Brand Blue (trust, primary actions)
            primary="#2563EB",
            on_primary="#FFFFFF",
            primary_container="#DBEAFE",
            on_primary_container="#1E3A8A",
            
            # Secondary - Brand Purple (innovation, secondary actions)
            secondary="#7C3AED",
            on_secondary="#FFFFFF",
            secondary_container="#EDE9FE",
            on_secondary_container="#5B21B6",
            
            # Tertiary - Brand Green (success, confirmation, CTAs)
            tertiary="#34D399",
            on_tertiary="#FFFFFF",
            tertiary_container="#D1FAE5",
            on_tertiary_container="#047857",
            
            # Error
            error="#DC2626",
            on_error="#FFFFFF",
            error_container="#FEE2E2",
            on_error_container="#991B1B",
            
            # Background & Surface
            background="#F3F4F6",
            on_background="#111827",
            surface="#FFFFFF",
            on_surface="#111827",
            
            # Surface Variants
            surface_variant="#F9FAFB",
            on_surface_variant="#374151",
            
            # Outline & Borders
            outline="#9CA3AF",
            outline_variant="#D1D5DB",
            
            # Shadow & Overlay
            shadow="#000000",
            scrim="#000000",
            
            # Inverse
            inverse_surface="#1F2937",
            on_inverse_surface="#F9FAFB",
            inverse_primary="#60A5FA",
        )
        
        # Dark Theme - Adapted Pogadane Brand Colors
        dark_theme = ft.ColorScheme(
            # Primary - Brighter blue for dark mode
            primary="#60A5FA",
            on_primary="#1E3A8A",
            primary_container="#1E40AF",
            on_primary_container="#DBEAFE",
            
            # Secondary - Brighter purple for dark mode
            secondary="#A78BFA",
            on_secondary="#5B21B6",
            secondary_container="#6D28D9",
            on_secondary_container="#EDE9FE",
            
            # Tertiary - Adjusted green for dark mode
            tertiary="#6EE7B7",
            on_tertiary="#047857",
            tertiary_container="#059669",
            on_tertiary_container="#D1FAE5",
            
            # Error
            error="#F87171",
            on_error="#991B1B",
            error_container="#B91C1C",
            on_error_container="#FEE2E2",
            
            # Background & Surface - Dark mode
            background="#111827",
            on_background="#F9FAFB",
            surface="#1F2937",
            on_surface="#F9FAFB",
            
            # Surface Variants
            surface_variant="#374151",
            on_surface_variant="#E5E7EB",
            
            # Outline & Borders
            outline="#6B7280",
            outline_variant="#4B5563",
            
            # Shadow & Overlay
            shadow="#000000",
            scrim="#000000",
            
            # Inverse
            inverse_surface="#F3F4F6",
            on_inverse_surface="#111827",
            inverse_primary="#2563EB",
        )
        
        # Set themes
        self.page.theme = ft.Theme(
            use_material3=True,
            color_scheme=light_theme,
        )
        self.page.dark_theme = ft.Theme(
            use_material3=True,
            color_scheme=dark_theme,
        )
        
        # Brand accent colors (for special use cases)
        self.brand_colors = {
            "highlight_yellow": "#FBBF24",  # Warnings, offline status
            "accent_green": "#6EE7B7",      # Bright positive feedback
            "success": "#34D399",            # Success states
            "warning": "#FBBF24",            # Warning states
        }
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        self.config_manager.initialize()
        self.config_module = self.config_manager.config
        
        # Initialize variables
        self.output_queue = queue.Queue()
        self.batch_processing_thread = None
        self.results_manager = ResultsManager()
        self.config_fields: Dict = {}
        self.current_font_scale = 1.0  # Track font size scaling
        
        # UI Components
        self.input_field = None
        self.queue_list = None
        self.progress_bar = None
        self.progress_text = None
        self.console_output = None
        self.transcription_output = None
        self.summary_output = None
        self.file_selector = None
        self.status_bar = None
        self.tabs = None
        self.theme_toggle_button = None  # Reference to theme toggle button
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the complete Material 3 UI"""
        
        # App Bar (Top)
        app_bar = self.create_app_bar()
        
        # Main Content with Tabs
        main_content = self.create_main_content()
        
        # Status Bar (Bottom)
        status_bar = self.create_status_bar()
        
        # Add to page
        self.page.add(
            ft.Column(
                [
                    app_bar,
                    ft.Divider(height=1),
                    main_content,
                    ft.Divider(height=1),
                    status_bar,
                ],
                spacing=0,
                expand=True,
            )
        )
    
    def create_app_bar(self):
        """Create Material 3 App Bar with Expressive design"""
        return ft.Container(
            content=ft.Row(
                [
                    # App Logo and Title
                    ft.Row(
                        [
                            ft.Image(
                                src=str(Path(__file__).parent.parent.parent / "res" / "assets" / "pogadane-icon.ico"),
                                width=120,
                                height=45,
                                fit=ft.ImageFit.CONTAIN,
                            ) if (Path(__file__).parent.parent.parent / "res" / "assets" / "pogadane-icon.ico").exists() 
                            else ft.Row([
                                ft.Icon(
                                    ft.Icons.HEADSET_ROUNDED,
                                    size=40,
                                    color="#2563EB",
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Pogadane",
                                            size=28,
                                            weight=ft.FontWeight.BOLD,
                                            color="#2563EB",
                                        ),
                                        ft.Text(
                                            f"v{APP_VERSION}",
                                            size=12,
                                            color="#6B7280",
                                        ),
                                    ],
                                    spacing=0,
                                ),
                            ], spacing=12),
                        ],
                        spacing=12,
                    ),
                    
                    # Spacer
                    ft.Container(expand=True),
                    
                    # Theme Toggle
                    ft.IconButton(
                        ref=lambda ref: setattr(self, 'theme_toggle_button', ref),
                        icon=ft.Icons.DARK_MODE_ROUNDED,
                        icon_size=24,
                        tooltip="Przełącz na tryb ciemny",
                        on_click=self.toggle_theme,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            animation_duration=300,
                        ),
                    ),
                    
                    # Font Size Controls
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.TEXT_DECREASE_ROUNDED,
                                    icon_size=20,
                                    tooltip="Zmniejsz czcionkę (A-)",
                                    on_click=lambda _: self.change_font_size(-1),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.TEXT_INCREASE_ROUNDED,
                                    icon_size=20,
                                    tooltip="Zwiększ czcionkę (A+)",
                                    on_click=lambda _: self.change_font_size(1),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                    ),
                                ),
                            ],
                            spacing=4,
                        ),
                        border_radius=12,
                        padding=4,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            animate=250,  # Animation duration in ms
        )
    
    def create_main_content(self):
        """Create main content area with tabs"""
        # Input Section
        input_section = self.create_input_section()
        
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Konsola",
                    icon=ft.Icons.TERMINAL_ROUNDED,
                    content=self.create_console_tab(),
                ),
                ft.Tab(
                    text="Wyniki",
                    icon=ft.Icons.ASSESSMENT_ROUNDED,
                    content=self.create_results_tab(),
                ),
                ft.Tab(
                    text="Konfiguracja",
                    icon=ft.Icons.SETTINGS_ROUNDED,
                    content=self.create_config_tab(),
                ),
            ],
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    input_section,
                    ft.Divider(height=1),
                    self.tabs,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )
    
    def create_input_section(self):
        """Create Material 3 input section with cards"""
        
        # File input field
        self.input_field = ft.TextField(
            label="Pliki audio / URL-e YouTube",
            hint_text="Wklej ścieżki do plików lub URL-e YouTube, każdą w nowej linii...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=16,
            filled=True,
            text_size=13,
            helper_text="Obsługiwane formaty: MP3, WAV, M4A, OGG, FLAC oraz YouTube",
        )
        
        # Buttons row
        buttons_row = ft.Row(
            [
                ft.FilledButton(
                    "Dodaj Pliki",
                    icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                    on_click=self.browse_files,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=16,
                        bgcolor="#7C3AED",  # Brand Purple for secondary actions
                        color="#FFFFFF",
                        animation_duration=200,
                    ),
                ),
                ft.Container(expand=True),
                ft.FilledButton(
                    "Rozpocznij Przetwarzanie",
                    icon=ft.Icons.PLAY_ARROW_ROUNDED,
                    on_click=self.start_batch_processing,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=24, vertical=16),
                        bgcolor="#34D399",  # Brand Green for key CTAs
                        color="#FFFFFF",
                        animation_duration=200,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Queue section
        queue_header = ft.Row(
            [
                ft.Icon(ft.Icons.QUEUE_MUSIC_ROUNDED, size=20, color="#7C3AED"),  # Brand Purple
                ft.Text("Kolejka Przetwarzania", size=16, weight=ft.FontWeight.W_600, color="#111827"),
            ],
            spacing=8,
        )
        
        # Queue list
        self.queue_list = ft.ListView(
            spacing=4,
            height=150,
        )
        
        queue_container = ft.Container(
            content=ft.Column(
                [
                    queue_header,
                    ft.Divider(height=1, color="#E5E7EB"),
                    self.queue_list,
                ],
                spacing=12,
            ),
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=16,
            padding=16,
            bgcolor="#F9FAFB",  # Light surface
            animate=300,  # Animation duration in ms
        )
        
        # Progress bar
        self.progress_text = ft.Text("Postęp: 0/0", size=13, color="#374151")
        self.progress_bar = ft.ProgressBar(
            value=0,
            height=8,
            border_radius=4,
            color="#34D399",  # Brand Green for progress
            bgcolor="#E5E7EB",
            tooltip="Postęp przetwarzania",
        )
        
        progress_container = ft.Column(
            [
                self.progress_text,
                self.progress_bar,
            ],
            spacing=8,
        )
        
        # Main input card
        return ft.Container(
            content=ft.Column(
                [
                    self.input_field,
                    buttons_row,
                    queue_container,
                    progress_container,
                ],
                spacing=16,
            ),
            padding=24,
            animate=300,  # Animation duration in ms
        )
    
    def create_console_tab(self):
        """Create console output tab with Material 3 design"""
        
        self.console_output = ft.TextField(
            value="",
            multiline=True,
            read_only=True,
            border_radius=16,
            filled=True,
            text_size=12,
            min_lines=20,
            expand=True,
        )
        
        buttons = ft.Row(
            [
                ft.FilledTonalButton(
                    "Zapisz Log",
                    icon=ft.Icons.SAVE_ROUNDED,
                    on_click=self.save_console_log,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=16,
                        bgcolor="#EDE9FE",  # Light purple tonal
                        color="#5B21B6",
                        animation_duration=200,
                    ),
                ),
                ft.OutlinedButton(
                    "Wyczyść",
                    icon=ft.Icons.CLEAR_ROUNDED,
                    on_click=self.clear_console,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=16,
                        side=ft.BorderSide(1, "#9CA3AF"),
                        color="#374151",
                        animation_duration=200,
                    ),
                ),
            ],
            spacing=12,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    self.console_output,
                    buttons,
                ],
                spacing=16,
                expand=True,
            ),
            padding=24,
        )
    
    def create_results_tab(self):
        """Create results display tab with split view"""
        
        # File selector
        self.file_selector = ft.Dropdown(
            label="Wybierz przetworzony plik",
            hint_text="Wybierz plik z listy...",
            on_change=self.display_selected_result,
            border_radius=12,
            filled=True,
        )
        
        # Transcription output
        self.transcription_output = ft.TextField(
            label="📝 Transkrypcja",
            multiline=True,
            read_only=True,
            border_radius=16,
            filled=True,
            text_size=12,
            min_lines=15,
            expand=True,
        )
        
        # Summary output
        self.summary_output = ft.TextField(
            label="📌 Streszczenie",
            multiline=True,
            read_only=True,
            border_radius=16,
            filled=True,
            text_size=12,
            min_lines=15,
            expand=True,
        )
        
        # Split view
        split_view = ft.Row(
            [
                ft.Container(content=self.transcription_output, expand=True),
                ft.Container(content=self.summary_output, expand=True),
            ],
            spacing=16,
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    self.file_selector,
                    split_view,
                ],
                spacing=16,
                expand=True,
            ),
            padding=24,
        )
    
    def create_config_tab(self):
        """Create configuration tab with organized sections"""
        
        # Summary Settings Section
        summary_section = self.create_config_section(
            title="🤖 Ustawienia Podsumowania",
            fields=[
                ("SUMMARY_PROVIDER", "Dostawca podsumowania", "dropdown", ["ollama", "transformers", "google"]),
                ("SUMMARY_LANGUAGE", "Język podsumowania", "text", None),
                ("OLLAMA_MODEL", "Model Ollama", "text", None),
                ("TRANSFORMERS_MODEL", "Model Transformers", "text", None),
                ("GOOGLE_API_KEY", "Klucz API Google", "password", None),
            ]
        )
        
        # Transcription Settings Section
        transcription_section = self.create_config_section(
            title="🎙️ Ustawienia Transkrypcji",
            fields=[
                ("TRANSCRIPTION_PROVIDER", "Dostawca transkrypcji", "dropdown", ["faster-whisper", "whisper"]),
                ("WHISPER_LANGUAGE", "Język transkrypcji", "text", None),
                ("WHISPER_MODEL", "Model Whisper", "dropdown", ["tiny", "base", "small", "medium", "large", "turbo"]),
                ("FASTER_WHISPER_EXE", "Plik Faster Whisper", "file", None),
                ("YT_DLP_EXE", "Plik yt-dlp", "file", None),
                ("ENABLE_SPEAKER_DIARIZATION", "Włącz diaryzację", "switch", None),
            ]
        )
        
        # Save button
        save_button = ft.FilledButton(
            "Zapisz i Zastosuj",
            icon=ft.Icons.SAVE_ROUNDED,
            on_click=self.save_config,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.padding.symmetric(horizontal=32, vertical=20),
                bgcolor="#2563EB",  # Brand Blue for primary save action
                color="#FFFFFF",
                animation_duration=200,
            ),
        )
        
        # Scrollable container
        config_content = ft.ListView(
            controls=[
                summary_section,
                ft.Divider(height=32),
                transcription_section,
                ft.Container(height=16),
                save_button,
            ],
            spacing=0,
            expand=True,
        )
        
        return ft.Container(
            content=config_content,
            padding=24,
        )
    
    def create_config_section(self, title: str, fields: List[tuple]):
        """Create a configuration section with fields"""
        
        section_fields = []
        
        # Section title
        section_header = ft.Row(
            [
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            ],
        )
        section_fields.append(section_header)
        section_fields.append(ft.Container(height=16))
        
        # Create fields
        for field_info in fields:
            config_key = field_info[0]
            label = field_info[1]
            field_type = field_info[2]
            options = field_info[3] if len(field_info) > 3 else None
            
            current_value = getattr(self.config_module, config_key, DEFAULT_CONFIG.get(config_key, ""))
            
            if field_type == "dropdown":
                field = ft.Dropdown(
                    label=label,
                    value=str(current_value),
                    options=[ft.dropdown.Option(opt) for opt in options],
                    border_radius=12,
                    filled=True,
                )
                self.config_fields[config_key] = field
                section_fields.append(field)
                
            elif field_type == "switch":
                field = ft.Row(
                    [
                        ft.Text(label, size=14),
                        ft.Switch(value=bool(current_value)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
                self.config_fields[config_key] = field.controls[1]
                section_fields.append(field)
                
            elif field_type == "password":
                field = ft.TextField(
                    label=label,
                    value=str(current_value),
                    password=True,
                    can_reveal_password=True,
                    border_radius=12,
                    filled=True,
                )
                self.config_fields[config_key] = field
                section_fields.append(field)
                
            elif field_type == "file":
                file_field = ft.TextField(
                    label=label,
                    value=str(current_value),
                    border_radius=12,
                    filled=True,
                    read_only=True,
                )
                browse_btn = ft.IconButton(
                    icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                    tooltip="Przeglądaj...",
                    on_click=lambda _, f=file_field: self.browse_file(f),
                )
                field = ft.Row(
                    [
                        ft.Container(content=file_field, expand=True),
                        browse_btn,
                    ],
                    spacing=8,
                )
                self.config_fields[config_key] = file_field
                section_fields.append(field)
                
            else:  # text
                field = ft.TextField(
                    label=label,
                    value=str(current_value),
                    border_radius=12,
                    filled=True,
                )
                self.config_fields[config_key] = field
                section_fields.append(field)
            
            section_fields.append(ft.Container(height=8))
        
        return ft.Container(
            content=ft.Column(section_fields, spacing=0),
            border=ft.border.all(1),
            border_radius=16,
            padding=20,
        )
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        
        self.status_bar = ft.Row(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=16, color="#34D399"),  # Brand Green for success
                ft.Text("Gotowy", size=13, color="#111827"),
                ft.Container(expand=True),
                ft.Text("Plików: 0", size=13, color="#6B7280"),
            ],
            spacing=8,
        )
        
        return ft.Container(
            content=self.status_bar,
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            bgcolor="#F9FAFB",  # Light surface
            border=ft.border.only(top=ft.BorderSide(1, "#E5E7EB")),
            animate=200,  # Animation duration in ms
        )
    
    # Event Handlers
    
    def toggle_theme(self, e):
        """Toggle between light and dark theme with animation"""
        # Toggle theme mode
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            theme_name = "ciemny"
            # Update icon button
            if e and hasattr(e.control, 'icon'):
                e.control.icon = ft.Icons.LIGHT_MODE_ROUNDED
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            theme_name = "jasny"
            # Update icon button
            if e and hasattr(e.control, 'icon'):
                e.control.icon = ft.Icons.DARK_MODE_ROUNDED
        
        # Animate the transition
        self.page.update()
        self.update_status(f"Motyw zmieniony na {theme_name}")
        self.show_snackbar(f"✨ Motyw {theme_name} aktywny", success=True)
    
    def change_font_size(self, delta: int):
        """Change font size"""
        # Implement font scaling
        self.update_status(f"Rozmiar czcionki {'zwiększony' if delta > 0 else 'zmniejszony'}")
    
    def browse_files(self, e):
        """Browse for audio files"""
        file_picker = ft.FilePicker(on_result=self.on_files_selected)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        file_picker.pick_files(
            dialog_title="Wybierz pliki audio",
            allowed_extensions=["mp3", "wav", "m4a", "ogg", "flac"],
            allow_multiple=True,
        )
    
    def on_files_selected(self, e: ft.FilePickerResultEvent):
        """Handle selected files"""
        if e.files:
            current_text = self.input_field.value or ""
            new_files = "\n".join([f.path for f in e.files])
            
            if current_text.strip():
                self.input_field.value = f"{current_text}\n{new_files}"
            else:
                self.input_field.value = new_files
            
            self.input_field.update()
            self.update_status(f"Dodano {len(e.files)} plik(ów)")
    
    def browse_file(self, text_field: ft.TextField):
        """Browse for a single file"""
        file_picker = ft.FilePicker(
            on_result=lambda e: self.on_file_selected(e, text_field)
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        
        file_picker.pick_files(
            dialog_title="Wybierz plik",
            allow_multiple=False,
        )
    
    def on_file_selected(self, e: ft.FilePickerResultEvent, text_field: ft.TextField):
        """Handle single file selection"""
        if e.files:
            text_field.value = e.files[0].path
            text_field.update()
    
    def start_batch_processing(self, e):
        """Start batch processing with visual feedback"""
        input_text = self.input_field.value
        if not input_text or not input_text.strip():
            self.show_snackbar("Proszę wprowadzić pliki lub URL-e", error=True)
            return
        
        # Animate progress bar
        self.progress_bar.value = 0
        self.progress_text.value = "Postęp: Przygotowywanie..."
        self.progress_bar.update()
        self.progress_text.update()
        
        self.update_status("Rozpoczynam przetwarzanie...")
        self.show_snackbar("🚀 Rozpoczęto przetwarzanie", success=True)
        # TODO: Implement actual batch processing
    
    def save_console_log(self, e):
        """Save console output to file"""
        file_picker = ft.FilePicker(on_result=self.on_save_log)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        file_picker.save_file(
            dialog_title="Zapisz log",
            file_name="pogadane_log.txt",
            allowed_extensions=["txt"],
        )
    
    def on_save_log(self, e: ft.FilePickerResultEvent):
        """Handle log save"""
        if e.path:
            try:
                with open(e.path, 'w', encoding='utf-8') as f:
                    f.write(self.console_output.value or "")
                self.show_snackbar(f"Log zapisany: {e.path}")
            except Exception as ex:
                self.show_snackbar(f"Błąd zapisu: {str(ex)}", error=True)
    
    def clear_console(self, e):
        """Clear console output"""
        self.console_output.value = ""
        self.console_output.update()
        self.update_status("Konsola wyczyszczona")
    
    def display_selected_result(self, e):
        """Display selected file results"""
        # TODO: Implement results display
        pass
    
    def save_config(self, e):
        """Save configuration to file"""
        try:
            config_path = self.config_manager.config_path
            
            # Build config content
            config_lines = ["# Pogadane Configuration\n\n"]
            
            for key, field in self.config_fields.items():
                if isinstance(field, ft.Switch):
                    value = field.value
                    config_lines.append(f"{key} = {value}\n")
                elif hasattr(field, 'value'):
                    value = field.value
                    if isinstance(value, str):
                        config_lines.append(f'{key} = "{value}"\n')
                    else:
                        config_lines.append(f"{key} = {value}\n")
            
            # Write to file
            with open(config_path, 'w', encoding='utf-8') as f:
                f.writelines(config_lines)
            
            # Reload config
            self.config_manager.reload()
            self.config_module = self.config_manager.config
            
            self.show_snackbar("Konfiguracja zapisana pomyślnie!", success=True)
            self.update_status("Konfiguracja zapisana")
        except Exception as ex:
            self.show_snackbar(f"Błąd zapisu konfiguracji: {str(ex)}", error=True)
    
    def update_status(self, message: str):
        """Update status bar message"""
        if self.status_bar:
            self.status_bar.controls[1].value = message
            self.status_bar.update()
    
    def show_snackbar(self, message: str, error: bool = False, warning: bool = False, success: bool = False):
        """Show Material 3 snackbar notification with brand colors and animation"""
        # Determine background color based on type
        if error:
            bg_color = "#DC2626"  # Red for errors
            icon = ft.Icons.ERROR_ROUNDED
        elif warning:
            bg_color = "#FBBF24"  # Brand Yellow for warnings
            icon = ft.Icons.WARNING_ROUNDED
        elif success:
            bg_color = "#34D399"  # Brand Green for success
            icon = ft.Icons.CHECK_CIRCLE_ROUNDED
        else:
            bg_color = "#2563EB"  # Brand Blue for info
            icon = ft.Icons.INFO_ROUNDED
        
        snackbar = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(icon, color="#FFFFFF", size=20),
                    ft.Text(message, color="#FFFFFF", size=14),
                ],
                spacing=12,
            ),
            bgcolor=bg_color,
            action="OK",
            action_color="#FFFFFF",
            duration=3000,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=16,
            padding=16,
            show_close_icon=True,
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()


def main(page: ft.Page):
    """Main entry point for Flet app"""
    PogadaneApp(page)


if __name__ == "__main__":
    ft.app(target=main)
