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
import shlex
import wave
import struct
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random

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
        
        # Set window size properties
        self.page.window.width = 1200
        self.page.window.height = 1000
        self.page.window.min_width = 900
        self.page.window.min_height = 800
        
        # Set custom icon (window icon and favicon)
        icon_path = Path(__file__).parent.parent.parent / "res" / "assets" / "pogadane-icon.ico"
        if icon_path.exists():
            self.page.window.icon = str(icon_path)
            # Note: web_icon is not a valid property in Flet, icon is used for both
        
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
        
        # Material 3 Expressive Design Tokens
        # Based on Google's M3 guidelines for spacing, elevation, and motion
        self.design_tokens = {
            # Spacing Scale (8px base unit - M3 standard)
            "spacing": {
                "xs": 4,      # Extra small - tight spacing
                "sm": 8,      # Small - compact layouts
                "md": 16,     # Medium - default spacing
                "lg": 24,     # Large - generous spacing
                "xl": 32,     # Extra large - section separation
                "xxl": 48,    # Double extra large - major sections
            },
            
            # Border Radius (M3 Expressive - more pronounced curves)
            "radius": {
                "none": 0,
                "sm": 8,      # Small components
                "md": 12,     # Standard components
                "lg": 16,     # Cards, containers
                "xl": 20,     # Large cards
                "xxl": 28,    # Hero elements
                "full": 9999, # Pills, circular
            },
            
            # Elevation (shadows for depth)
            "elevation": {
                "0": "none",
                "1": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                "2": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
                "3": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
                "4": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
                "5": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
            },
            
            # Typography Scale (M3 Expressive typography)
            "typography": {
                "display_large": {"size": 57, "weight": ft.FontWeight.W_400, "line_height": 64},
                "display_medium": {"size": 45, "weight": ft.FontWeight.W_400, "line_height": 52},
                "display_small": {"size": 36, "weight": ft.FontWeight.W_400, "line_height": 44},
                "headline_large": {"size": 32, "weight": ft.FontWeight.W_400, "line_height": 40},
                "headline_medium": {"size": 28, "weight": ft.FontWeight.W_400, "line_height": 36},
                "headline_small": {"size": 24, "weight": ft.FontWeight.W_400, "line_height": 32},
                "title_large": {"size": 22, "weight": ft.FontWeight.W_400, "line_height": 28},
                "title_medium": {"size": 16, "weight": ft.FontWeight.W_500, "line_height": 24},
                "title_small": {"size": 14, "weight": ft.FontWeight.W_500, "line_height": 20},
                "body_large": {"size": 16, "weight": ft.FontWeight.W_400, "line_height": 24},
                "body_medium": {"size": 14, "weight": ft.FontWeight.W_400, "line_height": 20},
                "body_small": {"size": 12, "weight": ft.FontWeight.W_400, "line_height": 16},
                "label_large": {"size": 14, "weight": ft.FontWeight.W_500, "line_height": 20},
                "label_medium": {"size": 12, "weight": ft.FontWeight.W_500, "line_height": 16},
                "label_small": {"size": 11, "weight": ft.FontWeight.W_500, "line_height": 16},
            },
            
            # Animation durations (M3 motion system)
            "motion": {
                "instant": 0,
                "fast": 100,
                "medium": 200,
                "slow": 300,
                "slower": 500,
            },
            
            # Icon sizes
            "icon_size": {
                "sm": 16,
                "md": 20,
                "lg": 24,
                "xl": 32,
                "xxl": 48,
            },
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
        
        # Audio visualization variables
        self.current_audio_file = None
        self.audio_duration = 0
        self.audio_sample_rate = 0
        self.waveform_data = []
        self.topic_segments = []
        self.playback_position = 0.0
        self.is_playing = False
        
        # UI Components
        self.queue_list = None
        self.queue_items: List[Dict[str, object]] = []
        self.queue_placeholder = None
        self.progress_bar = None
        self.progress_text = None
        self.console_output = None
        self.transcription_output = None
        self.summary_output = None
        self.file_selector = None
        self.status_bar = None
        self.status_message_text = None
        self.status_icon = None
        self.file_count_text = None
        self.tabs = None
        self.theme_toggle_button = None  # Reference to theme toggle button

        # Queue processing state
        self.total_items = 0
        self.completed_items = 0
        self.error_items = 0
        
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
        """Create Material 3 Expressive App Bar with enhanced visual hierarchy"""
        
        # Prepare logo path
        icon_path = Path(__file__).parent.parent.parent / "res" / "assets" / "pogadane-icon.ico"
        
        # Helper method to create text with design tokens
        def get_text(text, style_key, **kwargs):
            style = self.design_tokens["typography"][style_key]
            return ft.Text(
                text,
                size=style["size"],
                weight=style["weight"],
                **kwargs
            )
        
        return ft.Container(
            content=ft.Row(
                [
                    # App Logo and Title - Enhanced with M3 spacing
                    ft.Row(
                        [
                            # Icon with subtle scale animation
                            ft.Container(
                                content=ft.Image(
                                    src=str(icon_path),
                                    width=self.design_tokens["icon_size"]["xxl"],
                                    height=self.design_tokens["icon_size"]["xxl"],
                                    fit=ft.ImageFit.CONTAIN,
                                ) if icon_path.exists() else ft.Icon(
                                    ft.Icons.HEADSET_ROUNDED,
                                    size=self.design_tokens["icon_size"]["xxl"],
                                    color="#2563EB",
                                ),
                                animate_scale=self.design_tokens["motion"]["medium"],
                            ),
                            # Title and version with M3 typography
                            ft.Column(
                                [
                                    get_text(
                                        "Pogadane",
                                        "headline_medium",
                                        color="#2563EB",
                                    ),
                                    get_text(
                                        f"v{APP_VERSION}",
                                        "label_small",
                                        color="#6B7280",
                                    ),
                                ],
                                spacing=self.design_tokens["spacing"]["xs"],
                            ),
                        ],
                        spacing=self.design_tokens["spacing"]["md"],
                    ),
                    
                    # Spacer
                    ft.Container(expand=True),
                    
                    # Settings Button - M3 Expressive with hover state
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.SETTINGS_ROUNDED,
                            icon_size=self.design_tokens["icon_size"]["lg"],
                            tooltip="Ustawienia",
                            on_click=self.open_settings_dialog,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=self.design_tokens["radius"]["md"]),
                                animation_duration=self.design_tokens["motion"]["fast"],
                            ),
                        ),
                        animate_scale=self.design_tokens["motion"]["fast"],
                    ),
                    
                    # Theme Toggle - Enhanced with M3 state layers
                    ft.Container(
                        content=ft.IconButton(
                            ref=lambda ref: setattr(self, 'theme_toggle_button', ref),
                            icon=ft.Icons.DARK_MODE_ROUNDED,
                            icon_size=self.design_tokens["icon_size"]["lg"],
                            tooltip="Przełącz na tryb ciemny",
                            on_click=self.toggle_theme,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=self.design_tokens["radius"]["md"]),
                                animation_duration=self.design_tokens["motion"]["medium"],
                            ),
                        ),
                        animate_scale=self.design_tokens["motion"]["fast"],
                    ),
                    
                    # Font Size Controls - Grouped with M3 spacing
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.TEXT_DECREASE_ROUNDED,
                                    icon_size=self.design_tokens["icon_size"]["md"],
                                    tooltip="Zmniejsz czcionkę (A-)",
                                    on_click=lambda _: self.change_font_size(-1),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=self.design_tokens["radius"]["sm"]),
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.TEXT_INCREASE_ROUNDED,
                                    icon_size=self.design_tokens["icon_size"]["md"],
                                    tooltip="Zwiększ czcionkę (A+)",
                                    on_click=lambda _: self.change_font_size(1),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=self.design_tokens["radius"]["sm"]),
                                    ),
                                ),
                            ],
                            spacing=self.design_tokens["spacing"]["xs"],
                        ),
                        border_radius=self.design_tokens["radius"]["md"],
                        padding=self.design_tokens["spacing"]["xs"],
                        bgcolor="#F3F4F6" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#374151",
                        animate=self.design_tokens["motion"]["medium"],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(
                horizontal=self.design_tokens["spacing"]["lg"],
                vertical=self.design_tokens["spacing"]["md"],
            ),
            bgcolor=ft.Colors.SURFACE,
            animate=self.design_tokens["motion"]["medium"],
        )
    
    def create_main_content(self):
        """Create main content area with tabs"""
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Kolejka",
                    icon=ft.Icons.LIST_ALT_ROUNDED,
                    content=self.create_queue_tab(),
                ),
                ft.Tab(
                    text="Przeglądarka Wyników",
                    icon=ft.Icons.ANALYTICS_ROUNDED,
                    content=self.create_results_viewer_tab(),
                ),
                ft.Tab(
                    text="Konsola",
                    icon=ft.Icons.TERMINAL_ROUNDED,
                    content=self.create_console_tab(),
                ),
            ],
            expand=True,
        )
        
        return ft.Container(
            content=self.tabs,
            expand=True,
        )
    
    def create_queue_tab(self):
        """Create Material 3 queue management tab"""

        queue_intro = ft.Column(
            [
                ft.Text(
                    "Kolejka zadań",
                    size=18,
                    weight=ft.FontWeight.W_700,
                ),
                ft.Text(
                    "Dodaj pliki audio lub adresy URL, aby przygotować partię do przetworzenia.",
                    size=13,
                    color="#6B7280",
                ),
            ],
            spacing=4,
        )

        queue_actions = ft.Row(
            [
                ft.FilledButton(
                    "Dodaj plik(i)",
                    icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                    on_click=self.browse_files,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=16,
                        bgcolor="#7C3AED",
                        color="#FFFFFF",
                        animation_duration=200,
                    ),
                ),
                ft.OutlinedButton(
                    "Dodaj URL",
                    icon=ft.Icons.LINK_ROUNDED,
                    on_click=self.open_add_url_dialog,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=16,
                        side=ft.BorderSide(1, "#7C3AED"),
                        color="#7C3AED",
                        animation_duration=200,
                    ),
                ),
                ft.Container(expand=True),
                ft.FilledButton(
                    "Rozpocznij przetwarzanie",
                    icon=ft.Icons.PLAY_ARROW_ROUNDED,
                    on_click=self.start_batch_processing,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=24, vertical=16),
                        bgcolor="#34D399",
                        color="#FFFFFF",
                        animation_duration=200,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        queue_header = ft.Row(
            [
                ft.Icon(ft.Icons.QUEUE_MUSIC_ROUNDED, size=20, color="#7C3AED"),
                ft.Text(
                    "Elementy w kolejce",
                    size=16,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            spacing=8,
        )

        self.queue_placeholder = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.INBOX_ROUNDED, size=48, color="#9CA3AF"),
                    ft.Text(
                        "Kolejka jest pusta. Dodaj pierwszy element, aby rozpocząć.",
                        size=13,
                        color="#6B7280",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=40,
            bgcolor="#F9FAFB" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
            border_radius=12,
        )

        self.queue_list = ft.ListView(
            spacing=8,
            expand=True,
            auto_scroll=False,
            controls=[self.queue_placeholder],
        )

        queue_container = ft.Container(
            content=ft.Column(
                [
                    queue_header,
                    ft.Divider(height=1),
                    ft.Container(
                        content=self.queue_list,
                        expand=True,
                    ),
                ],
                spacing=12,
                expand=True,
            ),
            border=ft.border.all(1),
            border_radius=16,
            padding=16,
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    queue_intro,
                    queue_actions,
                    queue_container,
                ],
                spacing=16,
                expand=True,
            ),
            padding=24,
            expand=True,
        )

    def open_add_url_dialog(self, e):
        """Prompt user for a URL and add it to the processing queue"""

        url_field = ft.TextField(
            label="Adres URL",
            hint_text="Wklej adres URL źródła audio...",
            autofocus=True,
            border_radius=12,
            filled=True,
        )

        def close_dialog(_=None):
            dialog.open = False
            self.page.update()
            if dialog in self.page.overlay:
                self.page.overlay.remove(dialog)

        def confirm_add(_=None):
            url_value = (url_field.value or "").strip()
            if url_value:
                added = self.add_queue_entries([url_value])
                if added:
                    self.update_status("Dodano URL do kolejki")
                    self.show_snackbar("🔗 Dodano URL do kolejki", success=True)
                else:
                    self.show_snackbar("ℹ️ URL znajduje się już w kolejce", warning=True)
            close_dialog()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Dodaj URL", size=20, weight=ft.FontWeight.BOLD),
            content=url_field,
            actions=[
                ft.TextButton("Anuluj", on_click=close_dialog),
                ft.FilledButton(
                    "Dodaj",
                    icon=ft.Icons.ADD_LINK_ROUNDED,
                    on_click=confirm_add,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        bgcolor="#2563EB",
                        color="#FFFFFF",
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def add_queue_entries(self, entries: List[str]) -> int:
        """Add new items to the processing queue"""

        if not entries or not self.queue_list:
            return 0

        added = 0
        existing_values = {item["value"] for item in self.queue_items}

        for entry in entries:
            normalized = entry.strip()
            if not normalized or normalized in existing_values:
                continue

            queue_item = self._create_queue_item(normalized)
            self.queue_items.append(queue_item)
            self.queue_list.controls.append(queue_item["container"])
            existing_values.add(normalized)
            added += 1

        if added == 0:
            return 0

        if self.queue_placeholder and self.queue_placeholder in self.queue_list.controls:
            self.queue_list.controls.remove(self.queue_placeholder)

        self.queue_list.update()
        self.update_queue_count()

        return added

    def remove_queue_item(self, entry_value: str):
        """Remove a queue entry by its value"""

        target = None
        for item in self.queue_items:
            if item["value"] == entry_value:
                target = item
                break

        if not target:
            return

        if target["container"] in self.queue_list.controls:
            self.queue_list.controls.remove(target["container"])

        self.queue_items.remove(target)

        if not self.queue_items and self.queue_placeholder:
            self.queue_list.controls.append(self.queue_placeholder)

        self.queue_list.update()
        self.update_queue_count()

    def update_queue_count(self):
        """Update queue counter in status bar"""

        if self.file_count_text:
            self.file_count_text.value = f"Kolejka: {len(self.queue_items)}"
            self.file_count_text.update()

    def _create_queue_item(self, entry: str) -> Dict[str, object]:
        """Create UI representation for a queue entry"""

        is_url = entry.lower().startswith("http")
        icon_name = ft.Icons.LINK_ROUNDED if is_url else ft.Icons.AUDIO_FILE_ROUNDED
        display_name = entry if is_url else os.path.basename(entry) or entry

        status_text = ft.Text("Oczekuje", size=12, weight=ft.FontWeight.W_600, color="#6B7280")
        status_chip = ft.Container(
            content=status_text,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=999,
            bgcolor="#E5E7EB",
        )

        remove_button = ft.IconButton(
            icon=ft.Icons.CLOSE_ROUNDED,
            tooltip="Usuń z kolejki",
            icon_size=18,
            on_click=lambda _, value=entry: self.remove_queue_item(value),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=self.design_tokens["radius"]["full"]),
                padding=8,
            ),
        )

        content = ft.Row(
            [
                ft.Icon(icon_name, size=22, color="#2563EB" if not is_url else "#7C3AED"),
                ft.Column(
                    [
                        ft.Text(display_name, size=14, weight=ft.FontWeight.W_600),
                        ft.Text(entry, size=12, color="#6B7280"),
                    ],
                    spacing=4,
                    expand=True,
                ),
                status_chip,
                remove_button,
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        container = ft.Container(
            content=content,
            border_radius=12,
            padding=16,
            border=ft.border.all(1, "#E5E7EB"),
            bgcolor="#FFFFFF" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#111827",
        )

        return {
            "value": entry,
            "status": FILE_STATUS_PENDING,
            "status_text": status_text,
            "status_chip": status_chip,
            "container": container,
        }

    def _set_queue_item_status(self, index: int, status: str):
        """Update visual status for a queue entry"""

        if index < 0 or index >= len(self.queue_items):
            return

        item = self.queue_items[index]
        status_text: ft.Text = item["status_text"]
        status_chip: ft.Container = item["status_chip"]

        if status == FILE_STATUS_PROCESSING:
            status_text.value = "Przetwarzanie"
            status_text.color = "#2563EB"
            status_chip.bgcolor = "#DBEAFE"
        elif status == FILE_STATUS_COMPLETED:
            status_text.value = "Zakończono"
            status_text.color = "#047857"
            status_chip.bgcolor = "#D1FAE5"
        elif status == FILE_STATUS_ERROR:
            status_text.value = "Błąd"
            status_text.color = "#991B1B"
            status_chip.bgcolor = "#FEE2E2"
        else:
            status_text.value = "Oczekuje"
            status_text.color = "#6B7280"
            status_chip.bgcolor = "#E5E7EB"

        item["status"] = status
        status_chip.update()
        status_text.update()

    def _update_progress(self, processed: int, message: Optional[str] = None):
        """Update global progress bar and text"""

        if self.progress_bar:
            progress_value = (processed / self.total_items) if self.total_items else 0
            self.progress_bar.value = min(max(progress_value, 0), 1)
            self.progress_bar.update()

        if self.progress_text:
            if message:
                self.progress_text.value = message
            else:
                if self.total_items:
                    self.progress_text.value = f"Postęp: {processed}/{self.total_items}"
                else:
                    self.progress_text.value = "Postęp: 0/0"
            self.progress_text.update()

    def refresh_theme_sensitive_elements(self):
        """Update UI elements that depend on the active theme"""

        is_light = self.page.theme_mode == ft.ThemeMode.LIGHT
        queue_card_bg = "#FFFFFF" if is_light else "#111827"
        queue_border_color = "#E5E7EB" if is_light else "#374151"
        queue_placeholder_bg = "#F9FAFB" if is_light else "#1F2937"

        if self.queue_placeholder:
            self.queue_placeholder.bgcolor = queue_placeholder_bg
            self.queue_placeholder.update()

        for item in self.queue_items:
            container: ft.Container = item["container"]
            container.bgcolor = queue_card_bg
            container.border = ft.border.all(1, queue_border_color)
            container.update()

        if hasattr(self, "waveform_canvas") and self.waveform_canvas:
            self.waveform_canvas.bgcolor = "#F9FAFB" if is_light else "#1F2937"
            self.waveform_canvas.update()

        if hasattr(self, "topic_timeline") and self.topic_timeline:
            self.topic_timeline.bgcolor = "#F9FAFB" if is_light else "#1F2937"
            self.topic_timeline.update()
    
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
    
    def create_results_viewer_tab(self):
        """Create merged results and visualization workspace"""

        # File selector
        self.file_selector = ft.Dropdown(
            label="Wynik",
            hint_text="Wybierz przetworzony plik z listy...",
            on_change=self.display_selected_result,
            border_radius=12,
            filled=True,
        )

        visualization_section = self.create_visualization_section()

        # Transcription output
        self.transcription_output = ft.TextField(
            label="Transkrypcja",
            multiline=True,
            read_only=True,
            border_radius=16,
            filled=True,
            text_size=12,
            min_lines=12,
            expand=True,
        )

        # Summary output
        self.summary_output = ft.TextField(
            label="Streszczenie",
            multiline=True,
            read_only=True,
            border_radius=16,
            filled=True,
            text_size=12,
            min_lines=12,
            expand=True,
        )

        text_outputs = ft.Tabs(
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Transkrypcja",
                    icon=ft.Icons.SPEAKER_NOTES_ROUNDED,
                    content=ft.Container(
                        content=self.transcription_output,
                        padding=ft.padding.only(top=12),
                        expand=True,
                    ),
                ),
                ft.Tab(
                    text="Streszczenie",
                    icon=ft.Icons.DESCRIPTION_ROUNDED,
                    content=ft.Container(
                        content=self.summary_output,
                        padding=ft.padding.only(top=12),
                        expand=True,
                    ),
                ),
            ],
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    self.file_selector,
                    ft.Container(height=16),
                    visualization_section,
                    ft.Container(height=16),
                    text_outputs,
                ],
                spacing=0,
                expand=True,
            ),
            padding=24,
            expand=True,
        )

    def create_visualization_section(self):
        """Create audio visualization section with waveform and timeline"""

        # Audio file info
        self.viz_file_info = ft.Text(
            "Nie wybrano pliku audio",
            size=14,
            color="#6B7280",
            weight=ft.FontWeight.W_500,
        )

        # Waveform visualization
        self.waveform_canvas = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.GRAPHIC_EQ_ROUNDED, size=40, color="#2563EB"),
                            ft.Text("Wizualizacja fali dźwiękowej", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=16),
                    self.create_waveform_placeholder(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=24,
            border_radius=16,
            border=ft.border.all(1, "#E5E7EB"),
            bgcolor="#F9FAFB" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
        )

        # Topic timeline
        self.topic_timeline = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.TIMELINE_ROUNDED, size=40, color="#7C3AED"),
                            ft.Text("Oś czasu tematów", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=16),
                    self.create_topic_timeline_placeholder(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=24,
            border_radius=16,
            border=ft.border.all(1, "#E5E7EB"),
            bgcolor="#F9FAFB" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
        )

        # Control buttons
        control_buttons = ft.Row(
            controls=[
                ft.FilledButton(
                    "Generuj wizualizację",
                    icon=ft.Icons.AUTO_GRAPH_ROUNDED,
                    on_click=self.generate_visualization,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        bgcolor="#2563EB",
                        color="#FFFFFF",
                    ),
                ),
                ft.OutlinedButton(
                    "Eksportuj do PNG",
                    icon=ft.Icons.DOWNLOAD_ROUNDED,
                    on_click=self.export_visualization,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                ),
            ],
            spacing=12,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    self.viz_file_info,
                    ft.Container(height=8),
                    control_buttons,
                    ft.Container(height=16),
                    self.waveform_canvas,
                    ft.Container(height=16),
                    self.topic_timeline,
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            border_radius=16,
            border=ft.border.all(1, "#E5E7EB"),
            padding=24,
            expand=True,
        )
    
    def create_waveform_placeholder(self):
        """Create waveform placeholder visualization with animated bars"""
        # Create animated waveform bars that pulse
        bars = []
        
        for i in range(100):
            # Vary heights to create wave pattern
            base_height = 50
            variation = random.randint(-30, 70)
            height = max(20, min(120, base_height + variation))
            
            # Create bar with pulsing animation
            bar = ft.Container(
                width=6,
                height=height,
                bgcolor="#2563EB" if i % 3 == 0 else "#60A5FA",
                border_radius=3,
                opacity=0.8,
                animate=500 if i % 5 == 0 else None,
                tooltip=f"Pozycja: {i}s",
            )
            bars.append(bar)
        
        # Wrap in scrollable container
        return ft.Container(
            content=ft.Row(
                controls=bars,
                spacing=2,
                alignment=ft.MainAxisAlignment.START,
                scroll=ft.ScrollMode.AUTO,
            ),
            height=150,
            border_radius=12,
            padding=12,
            bgcolor="#F3F4F6" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#111827",
        )
    
    def create_topic_timeline_placeholder(self):
        """Create interactive topic timeline with hover effects"""
        # Sample topics with timestamps (will be replaced with real data)
        sample_topics = [
            {"time": "0:00", "end": "2:30", "duration": "2:30", "topic": "Wprowadzenie", "desc": "Przedstawienie tematu i kontekstu", "color": "#34D399"},
            {"time": "2:30", "end": "7:45", "duration": "5:15", "topic": "Problem główny", "desc": "Analiza kluczowych wyzwań", "color": "#F59E0B"},
            {"time": "7:45", "end": "11:05", "duration": "3:20", "topic": "Rozwiązanie", "desc": "Propozycje i rekomendacje", "color": "#2563EB"},
            {"time": "11:05", "end": "12:50", "duration": "1:45", "topic": "Podsumowanie", "desc": "Wnioski i następne kroki", "color": "#7C3AED"},
        ]
        
        timeline_items = []
        
        for idx, topic in enumerate(sample_topics):
            # Create expandable topic card
            topic_card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                # Time marker
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                topic["time"],
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color="#FFFFFF",
                                            ),
                                            ft.Icon(ft.Icons.ARROW_DOWNWARD, size=12, color="#FFFFFF"),
                                            ft.Text(
                                                topic["end"],
                                                size=11,
                                                color="#FFFFFF",
                                                opacity=0.8,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=2,
                                    ),
                                    bgcolor=topic["color"],
                                    padding=10,
                                    border_radius=12,
                                    width=70,
                                ),
                                # Topic info
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.CIRCLE, size=12, color=topic["color"]),
                                                    ft.Text(topic["topic"], size=16, weight=ft.FontWeight.BOLD),
                                                    ft.Container(expand=True),
                                                    ft.IconButton(
                                                        icon=ft.Icons.PLAY_CIRCLE_OUTLINE_ROUNDED,
                                                        icon_size=24,
                                                        icon_color=topic["color"],
                                                        tooltip="Odtwórz od tego momentu",
                                                        on_click=lambda e, t=topic["time"]: self.jump_to_time(t),
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Text(
                                                topic["desc"],
                                                size=13,
                                                color="#6B7280",
                                                italic=True,
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.TIMER_OUTLINED, size=14, color="#9CA3AF"),
                                                    ft.Text(f"Długość: {topic['duration']}", size=12, color="#9CA3AF"),
                                                ],
                                                spacing=4,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                    bgcolor=topic["color"] + "15",  # Very light background
                                    padding=16,
                                    border_radius=12,
                                    border=ft.border.all(2, topic["color"]),
                                    expand=True,
                                    animate=300,
                                ),
                            ],
                            spacing=16,
                        ),
                    ],
                ),
                margin=ft.margin.only(bottom=16),
                animate_opacity=300,
                animate_scale=300,
                on_hover=lambda e: self.on_topic_hover(e),
            )
            timeline_items.append(topic_card)
        
        # Add playback position indicator
        playback_indicator = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=20, color="#2563EB"),
                    ft.ProgressBar(value=0.3, height=6, color="#2563EB", bgcolor="#E5E7EB", border_radius=3),
                    ft.Text("3:45 / 12:50", size=12, weight=ft.FontWeight.W_500),
                ],
                spacing=12,
            ),
            padding=12,
            border_radius=12,
            bgcolor="#EFF6FF" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1E3A8A",
            margin=ft.margin.only(bottom=20),
        )
        
        return ft.Column(
            controls=[playback_indicator] + timeline_items,
            spacing=0,
        )
    
    def on_topic_hover(self, e):
        """Handle topic hover effect"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.02
        else:  # Mouse leave
            e.control.scale = 1.0
        e.control.update()
    
    def jump_to_time(self, timestamp):
        """Jump to specific time in audio"""
        # Convert timestamp to seconds
        time_parts = timestamp.split(":")
        seconds = int(time_parts[0]) * 60 + int(time_parts[1])
        
        self.playback_position = seconds
        self.update_playback_position()
        self.show_snackbar(f"⏩ Przeskakiwanie do {timestamp}", success=True)
    
    def analyze_audio_file(self, file_path):
        """Analyze audio file and extract waveform data"""
        try:
            # Try using wave library first (built-in, no dependencies)
            import wave
            
            with wave.open(str(file_path), 'rb') as wav_file:
                # Get audio properties
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                
                # Calculate duration
                duration = n_frames / float(framerate)
                
                # Read audio data
                audio_data = wav_file.readframes(n_frames)
                
                # Convert to amplitude values
                import struct
                if sample_width == 2:  # 16-bit audio
                    fmt = f'{n_frames * n_channels}h'
                    samples = struct.unpack(fmt, audio_data)
                else:
                    samples = [0] * 100  # Fallback
                
                # Downsample to ~100 points for visualization
                step = max(1, len(samples) // 100)
                waveform = [abs(samples[i]) for i in range(0, len(samples), step)][:100]
                
                # Normalize to 0-120 range for display
                if waveform:
                    max_val = max(waveform)
                    if max_val > 0:
                        waveform = [int(20 + (v / max_val) * 100) for v in waveform]
                
                return {
                    'duration': duration,
                    'sample_rate': framerate,
                    'channels': n_channels,
                    'waveform': waveform if waveform else [50] * 100,
                }
        except ImportError:
            print("⚠️ wave library not available, using placeholder data")
        except Exception as e:
            print(f"⚠️ Could not analyze audio: {e}")
        
        # Return placeholder data if analysis fails
        return {
            'duration': 0,
            'sample_rate': 44100,
            'channels': 2,
            'waveform': [random.randint(20, 120) for _ in range(100)],
        }
    
    def parse_transcription_topics(self, transcription_text, summary_text):
        """Parse transcription and summary to extract topic segments with timestamps"""
        topics = []
        
        # Simple heuristic: look for time markers in transcription
        # Format: [00:00:00] or (0:00) or similar
        import re
        
        # Try to find timestamp patterns in transcription
        timestamp_pattern = r'\[?(\d{1,2}):(\d{2})(?::(\d{2}))?\]?'
        matches = re.finditer(timestamp_pattern, transcription_text)
        
        timestamps = []
        for match in matches:
            hours = 0
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            if match.group(3):
                hours = minutes
                minutes = seconds
                seconds = int(match.group(3))
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            timestamps.append(total_seconds)
        
        # If we found timestamps, use them to segment topics
        if timestamps and len(timestamps) >= 2:
            colors = ["#34D399", "#F59E0B", "#2563EB", "#7C3AED", "#EC4899"]
            
            for i, start_time in enumerate(timestamps[:-1]):
                end_time = timestamps[i + 1]
                duration = end_time - start_time
                
                topic = {
                    'time': self.seconds_to_timestamp(start_time),
                    'end': self.seconds_to_timestamp(end_time),
                    'duration': self.seconds_to_timestamp(duration),
                    'topic': f'Segment {i + 1}',
                    'desc': 'Automatycznie wykryty segment',
                    'color': colors[i % len(colors)],
                }
                topics.append(topic)
        else:
            # Use default segments if no timestamps found
            topics = [
                {"time": "0:00", "end": "2:30", "duration": "2:30", "topic": "Wprowadzenie", "desc": "Przedstawienie tematu", "color": "#34D399"},
                {"time": "2:30", "end": "7:45", "duration": "5:15", "topic": "Treść główna", "desc": "Główna część nagrania", "color": "#2563EB"},
                {"time": "7:45", "end": "10:00", "duration": "2:15", "topic": "Podsumowanie", "desc": "Wnioski końcowe", "color": "#7C3AED"},
            ]
        
        return topics
    
    def seconds_to_timestamp(self, seconds):
        """Convert seconds to MM:SS or HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def generate_visualization(self, e):
        """Generate audio waveform and topic timeline from actual audio file"""
        # Determine audio source
        audio_source: Optional[str] = None

        if self.file_selector and self.file_selector.value:
            audio_source = self.file_selector.value
        else:
            for item in self.queue_items:
                candidate = item["value"]
                if not candidate.lower().startswith("http"):
                    audio_source = candidate
                    break

        if not audio_source:
            self.show_snackbar("⚠️ Proszę wybrać plik audio z wyników lub kolejki", error=True)
            return

        audio_path = Path(audio_source)
        if not audio_path.exists():
            self.show_snackbar(f"⚠️ Plik nie istnieje: {audio_source}", error=True)
            return
        
        # Show loading animation
        loading_dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(width=50, height=50, color="#2563EB"),
                    ft.Text("Generowanie wizualizacji...", size=16, text_align=ft.TextAlign.CENTER),
                    ft.Text("Analizowanie pliku audio", size=12, color="#6B7280"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                width=250,
                height=150,
            ),
            modal=True,
        )
        
        self.page.overlay.append(loading_dialog)
        loading_dialog.open = True
        self.page.update()
        
        # Process in background thread
        import threading
        
        def process_visualization():
            try:
                # Analyze audio file
                audio_info = self.analyze_audio_file(audio_path)
                
                self.current_audio_file = str(audio_path)
                self.audio_duration = audio_info['duration']
                self.audio_sample_rate = audio_info['sample_rate']
                self.waveform_data = audio_info['waveform']
                
                # Try to get transcription/summary if available
                transcription = self.transcription_output.value if self.transcription_output else ""
                summary = self.summary_output.value if self.summary_output else ""
                
                # Parse topics from transcription
                self.topic_segments = self.parse_transcription_topics(transcription, summary)
                
                # Close loading dialog
                loading_dialog.open = False
                self.page.update()
                
                # Update visualization with real data
                self.update_visualization_with_data()
                
                # Update file info
                duration_str = self.seconds_to_timestamp(self.audio_duration) if self.audio_duration > 0 else "N/A"
                self.viz_file_info.value = f"🎵 Audio: {audio_path.name} | Długość: {duration_str} | Próbkowanie: {self.audio_sample_rate}Hz"
                self.viz_file_info.update()
                
                # Show success
                self.show_snackbar("✅ Wizualizacja wygenerowana z prawdziwych danych audio!", success=True)
                
            except Exception as ex:
                loading_dialog.open = False
                self.page.update()
                print(f"❌ Error generating visualization: {ex}")
                import traceback
                traceback.print_exc()
                self.show_snackbar(f"❌ Błąd: {str(ex)}", error=True)
        
        threading.Thread(target=process_visualization, daemon=True).start()
    
    def update_visualization_with_data(self):
        """Update waveform and timeline with analyzed data"""
        # Rebuild waveform with real data
        if hasattr(self, 'waveform_canvas') and self.waveform_data:
            bars = []
            for i, height in enumerate(self.waveform_data):
                time_pos = (i / len(self.waveform_data)) * self.audio_duration if self.audio_duration > 0 else i
                bar = ft.Container(
                    width=6,
                    height=height,
                    bgcolor="#2563EB" if i % 3 == 0 else "#60A5FA",
                    border_radius=3,
                    opacity=0.8,
                    animate=500 if i % 5 == 0 else None,
                    tooltip=f"Pozycja: {self.seconds_to_timestamp(time_pos)}",
                    on_click=lambda e, pos=time_pos: self.jump_to_time(self.seconds_to_timestamp(pos)),
                )
                bars.append(bar)
            
            # Update waveform display
            new_waveform = ft.Container(
                content=ft.Row(
                    controls=bars,
                    spacing=2,
                    alignment=ft.MainAxisAlignment.START,
                    scroll=ft.ScrollMode.AUTO,
                ),
                height=150,
                border_radius=12,
                padding=12,
                bgcolor="#F3F4F6" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#111827",
            )
            
            # Find and update waveform in canvas
            if self.waveform_canvas.content.controls:
                self.waveform_canvas.content.controls[2] = new_waveform
                self.waveform_canvas.update()
        
        # Update topic timeline with parsed data
        if hasattr(self, 'topic_timeline') and self.topic_segments:
            self.rebuild_topic_timeline()
    
    def rebuild_topic_timeline(self):
        """Rebuild topic timeline with actual topic data"""
        timeline_items = []
        
        for idx, topic in enumerate(self.topic_segments):
            topic_card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                # Time marker
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                topic["time"],
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color="#FFFFFF",
                                            ),
                                            ft.Icon(ft.Icons.ARROW_DOWNWARD, size=12, color="#FFFFFF"),
                                            ft.Text(
                                                topic["end"],
                                                size=11,
                                                color="#FFFFFF",
                                                opacity=0.8,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=2,
                                    ),
                                    bgcolor=topic["color"],
                                    padding=10,
                                    border_radius=12,
                                    width=70,
                                ),
                                # Topic info
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.CIRCLE, size=12, color=topic["color"]),
                                                    ft.Text(topic["topic"], size=16, weight=ft.FontWeight.BOLD),
                                                    ft.Container(expand=True),
                                                    ft.IconButton(
                                                        icon=ft.Icons.PLAY_CIRCLE_OUTLINE_ROUNDED,
                                                        icon_size=24,
                                                        icon_color=topic["color"],
                                                        tooltip="Odtwórz od tego momentu",
                                                        on_click=lambda e, t=topic["time"]: self.jump_to_time(t),
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Text(
                                                topic["desc"],
                                                size=13,
                                                color="#6B7280",
                                                italic=True,
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.TIMER_OUTLINED, size=14, color="#9CA3AF"),
                                                    ft.Text(f"Długość: {topic['duration']}", size=12, color="#9CA3AF"),
                                                ],
                                                spacing=4,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                    bgcolor=topic["color"] + "15",
                                    padding=16,
                                    border_radius=12,
                                    border=ft.border.all(2, topic["color"]),
                                    expand=True,
                                    animate=300,
                                ),
                            ],
                            spacing=16,
                        ),
                    ],
                ),
                margin=ft.margin.only(bottom=16),
                animate_opacity=300,
                animate_scale=300,
                on_hover=lambda e: self.on_topic_hover(e),
            )
            timeline_items.append(topic_card)
        
        # Add playback controls
        playback_controls = self.create_playback_controls()
        
        # Update timeline
        if self.topic_timeline.content:
            self.topic_timeline.content.controls = [playback_controls] + timeline_items
            self.topic_timeline.update()
    
    def create_playback_controls(self):
        """Create audio playback controls"""
        # Playback progress
        progress = self.playback_position / self.audio_duration if self.audio_duration > 0 else 0
        current_time = self.seconds_to_timestamp(self.playback_position)
        total_time = self.seconds_to_timestamp(self.audio_duration) if self.audio_duration > 0 else "0:00"
        
        self.playback_progress = ft.ProgressBar(
            value=progress,
            height=6,
            color="#2563EB",
            bgcolor="#E5E7EB",
            border_radius=3,
        )
        
        self.playback_time_text = ft.Text(
            f"{current_time} / {total_time}",
            size=12,
            weight=ft.FontWeight.W_500,
        )
        
        self.play_pause_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW_ROUNDED if not self.is_playing else ft.Icons.PAUSE_ROUNDED,
            icon_size=24,
            icon_color="#2563EB",
            tooltip="Odtwórz/Pauza",
            on_click=self.toggle_playback,
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.play_pause_button,
                    ft.Container(content=self.playback_progress, expand=True),
                    self.playback_time_text,
                ],
                spacing=12,
            ),
            padding=12,
            border_radius=12,
            bgcolor="#EFF6FF" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1E3A8A",
            margin=ft.margin.only(bottom=20),
        )
    
    def toggle_playback(self, e):
        """Toggle audio playback"""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_pause_button.icon = ft.Icons.PAUSE_ROUNDED
            self.show_snackbar("▶️ Odtwarzanie...", success=True)
            # TODO: Implement actual audio playback
        else:
            self.play_pause_button.icon = ft.Icons.PLAY_ARROW_ROUNDED
            self.show_snackbar("⏸️ Pauza", success=True)
        
        self.play_pause_button.update()
    
    def update_playback_position(self):
        """Update playback position UI"""
        if hasattr(self, 'playback_progress') and hasattr(self, 'playback_time_text'):
            progress = self.playback_position / self.audio_duration if self.audio_duration > 0 else 0
            self.playback_progress.value = progress
            self.playback_progress.update()
            
            current_time = self.seconds_to_timestamp(self.playback_position)
            total_time = self.seconds_to_timestamp(self.audio_duration) if self.audio_duration > 0 else "0:00"
            self.playback_time_text.value = f"{current_time} / {total_time}"
            self.playback_time_text.update()
    
    def export_visualization(self, e):
        """Export visualization to PNG"""
        self.show_snackbar("🖼️ Eksport wizualizacji w przygotowaniu...", success=True)
        # TODO: Implement PNG export
    
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
        
        self.status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=16, color="#34D399")
        self.status_message_text = ft.Text("Gotowy", size=13)
        status_message = ft.Row(
            [
                self.status_icon,
                self.status_message_text,
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.progress_text = ft.Text("Postęp: 0/0", size=12, color="#6B7280")
        self.progress_bar = ft.ProgressBar(
            value=0,
            height=6,
            border_radius=3,
            color="#34D399",
            bgcolor="#E5E7EB",
        )

        progress_column = ft.Column(
            [
                self.progress_text,
                ft.Container(content=self.progress_bar, expand=True),
            ],
            spacing=6,
            expand=True,
        )

        self.file_count_text = ft.Text("Kolejka: 0", size=13)

        self.status_bar = ft.Row(
            [
                status_message,
                ft.Container(width=16),
                progress_column,
                ft.Container(width=16),
                self.file_count_text,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        return ft.Container(
            content=self.status_bar,
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            border=ft.border.only(top=ft.BorderSide(1)),
            animate=200,
        )
    
    # Event Handlers
    
    def open_settings_dialog(self, e):
        """Open settings dialog window with loading animation"""
        # Show loading indicator
        loading_dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(width=50, height=50),
                    ft.Text("Ładowanie ustawień...", size=16, text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                width=200,
                height=120,
            ),
            modal=True,
        )
        
        self.page.overlay.append(loading_dialog)
        loading_dialog.open = True
        self.page.update()
        
        try:
            # Clear previous config fields
            self.config_fields.clear()
            
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
            
            # Dialog content with scrollable column
            dialog_content = ft.Container(
                content=ft.Column(
                    controls=[
                        summary_section,
                        ft.Divider(height=32),
                        transcription_section,
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                height=500,
                width=600,
            )
            
            # Create dialog with fade-in animation
            settings_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row([
                    ft.Icon(ft.Icons.SETTINGS_ROUNDED, size=28, color="#2563EB"),
                    ft.Text("Ustawienia", size=24, weight=ft.FontWeight.BOLD),
                ], spacing=12),
                content=dialog_content,
                actions=[
                    ft.TextButton(
                        "Anuluj",
                        on_click=lambda _: self.close_dialog(settings_dialog),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                    ),
                    ft.FilledButton(
                        "Zapisz i Zastosuj",
                        icon=ft.Icons.SAVE_ROUNDED,
                        on_click=lambda _: self.save_config_from_dialog(settings_dialog),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            bgcolor="#2563EB",
                            color="#FFFFFF",
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            # Close loading dialog and show settings dialog with animation
            loading_dialog.open = False
            self.page.update()
            
            # Small delay for smooth transition
            import time
            time.sleep(0.1)
            
            # Show settings dialog
            self.page.overlay.append(settings_dialog)
            settings_dialog.open = True
            self.page.update()
            
        except Exception as ex:
            # Close loading dialog on error
            loading_dialog.open = False
            self.page.update()
            
            print(f"❌ Error opening settings dialog: {ex}")
            import traceback
            traceback.print_exc()
            self.show_snackbar(f"Błąd otwierania ustawień: {str(ex)}", error=True)
    
    def close_dialog(self, dialog):
        """Close the settings dialog"""
        dialog.open = False
        self.page.update()
    
    def save_config_from_dialog(self, dialog):
        """Save configuration from dialog with loading animation and close it"""
        # Show saving indicator
        saving_dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(width=50, height=50, color="#2563EB"),
                    ft.Text("Zapisywanie...", size=16, text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                width=200,
                height=120,
            ),
            modal=True,
        )
        
        self.page.overlay.append(saving_dialog)
        saving_dialog.open = True
        self.page.update()
        
        try:
            # Save configuration
            self.save_config(None)
            
            # Small delay to show the saving animation
            import time
            time.sleep(0.3)
            
            # Close saving dialog
            saving_dialog.open = False
            self.page.update()
            
            # Close settings dialog
            self.close_dialog(dialog)
            
            # Show success with animated snackbar
            self.show_snackbar("✅ Ustawienia zapisane pomyślnie!", success=True)
            
        except Exception as ex:
            # Close saving dialog on error
            saving_dialog.open = False
            self.page.update()
            
            print(f"❌ Error saving config: {ex}")
            self.show_snackbar(f"❌ Błąd zapisu: {str(ex)}", error=True)
    
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
        self.refresh_theme_sensitive_elements()
        self.update_status(f"Motyw zmieniony na {theme_name}")
        self.show_snackbar(f"✨ Motyw {theme_name} aktywny", success=True)
    
    def change_font_size(self, delta: int):
        """Change font size dynamically"""
        # Update font scale
        self.current_font_scale += delta * 0.1
        self.current_font_scale = max(0.7, min(1.5, self.current_font_scale))  # Clamp between 0.7 and 1.5
        
        # Update text fields font sizes
        if self.console_output:
            self.console_output.text_size = int(12 * self.current_font_scale)
            self.console_output.update()
        
        if self.transcription_output:
            self.transcription_output.text_size = int(12 * self.current_font_scale)
            self.transcription_output.update()
        
        if self.summary_output:
            self.summary_output.text_size = int(12 * self.current_font_scale)
            self.summary_output.update()
        
        scale_percent = int(self.current_font_scale * 100)
        self.update_status(f"Rozmiar czcionki: {scale_percent}%")
        self.show_snackbar(f"📝 Czcionka: {scale_percent}%", success=True)
    
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
        """Handle selected files with animated feedback"""
        if e.files:
            # Show loading animation for file processing
            loading_snackbar = ft.SnackBar(
                content=ft.Row([
                    ft.ProgressRing(width=20, height=20, stroke_width=3),
                    ft.Text(f"Dodawanie {len(e.files)} plik(ów)..."),
                ], spacing=10),
                duration=1000,
            )
            self.page.overlay.append(loading_snackbar)
            loading_snackbar.open = True
            self.page.update()
            
            new_files = [f.path for f in e.files if f.path]
            added = self.add_queue_entries(new_files)
            
            # Close loading and show success
            loading_snackbar.open = False
            self.page.update()
            
            if added:
                self.update_status(f"Dodano {added} plik(ów) do kolejki")
                self.show_snackbar(f"📁 Dodano {added} plik(ów)", success=True)
            else:
                self.show_snackbar("ℹ️ Wszystkie pliki są już w kolejce", warning=True)
    
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
        """Start real batch processing with backend integration"""
        if not self.queue_items:
            self.show_snackbar("⚠️ Kolejka jest pusta", error=True)
            return
        
        input_sources = [item["value"] for item in self.queue_items]
        self.total_items = len(input_sources)
        self.completed_items = 0
        self.error_items = 0
        self._update_progress(0)

        for idx in range(self.total_items):
            self._set_queue_item_status(idx, FILE_STATUS_PENDING)
        
        if self.status_icon:
            self.status_icon.color = "#2563EB"
            self.status_icon.update()
        
        self.update_status("🚀 Rozpoczynam przetwarzanie...")
        self.show_snackbar("🚀 Rozpoczęto przetwarzanie", success=True)
        
        # Start real backend processing in background thread
        threading.Thread(
            target=self._execute_batch_processing_logic,
            args=(input_sources,),
            daemon=True
        ).start()
        
        # Start queue poller
        threading.Thread(
            target=self._poll_output_queue_for_batch,
            daemon=True
        ).start()
    
    def _execute_batch_processing_logic(self, input_sources):
        """Execute batch processing for all input sources (real backend logic)"""
        script_path = self.base_path / "transcribe_summarize_working.py"
        
        for i, input_src in enumerate(input_sources):
            # Update queue status to PROCESSING
            self.output_queue.put(("update_status", str(i), FILE_STATUS_PROCESSING))
            
            # Build command
            cmd = [sys.executable, "-u", str(script_path), input_src]
            
            # Add config file if selected
            if hasattr(self, 'config_path') and self.config_path:
                cmd.extend(["--config", str(self.config_path)])
            
            try:
                # Start subprocess
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )
                
                # Read output line by line
                for line in proc.stdout:
                    clean_line = strip_ansi(line)
                    self.output_queue.put(("log", clean_line, "", ""))
                
                # Wait for completion
                proc.wait()
                
                # Check return code
                if proc.returncode == 0:
                    # Try to extract transcription and summary from results
                    trans, summ = extract_transcription_and_summary(input_src, self.base_path)
                    
                    if trans or summ:
                        self.output_queue.put(("result", input_src, trans, summ))
                        self.output_queue.put(("update_status", str(i), FILE_STATUS_COMPLETED))
                    else:
                        self.output_queue.put(("error", f"⚠️ Nie znaleziono wyników dla: {input_src}", "", ""))
                        self.output_queue.put(("update_status", str(i), FILE_STATUS_ERROR))
                else:
                    self.output_queue.put(("error", f"❌ Błąd przetwarzania: {input_src} (kod {proc.returncode})", "", ""))
                    self.output_queue.put(("update_status", str(i), FILE_STATUS_ERROR))
                    
            except Exception as ex:
                self.output_queue.put(("error", f"❌ Wyjątek podczas przetwarzania {input_src}: {ex}", "", ""))
                self.output_queue.put(("update_status", str(i), FILE_STATUS_ERROR))
        
        # Signal completion
        self.output_queue.put(("finished_all", "", "", ""))
    
    def _poll_output_queue_for_batch(self):
        """Poll output queue and update UI (adapted for Flet)"""
        while True:
            try:
                msg = self.output_queue.get(timeout=0.1)
                msg_type = msg[0]
                
                if msg_type == "log":
                    # Update console output
                    data = msg[1]
                    self.console_output.value += data
                    self.console_output.update()
                    
                elif msg_type == "error":
                    # Show error in console
                    data = msg[1]
                    self.console_output.value += f"\n❌ {data}\n"
                    self.console_output.update()
                    self.show_snackbar(f"❌ {data}", error=True)
                    
                elif msg_type == "update_status":
                    # Update queue item status
                    item_index = int(msg[1])
                    status = msg[2]

                    self._set_queue_item_status(item_index, status)

                    if status == FILE_STATUS_PROCESSING:
                        self._update_progress(
                            self.completed_items,
                            f"Postęp: Przetwarzanie {item_index + 1}/{self.total_items}",
                        )
                    elif status == FILE_STATUS_COMPLETED:
                        self.completed_items += 1
                        self._update_progress(self.completed_items)
                    elif status == FILE_STATUS_ERROR:
                        self.error_items += 1
                        self.completed_items += 1
                        self._update_progress(
                            self.completed_items,
                            f"Postęp: Błąd w pliku {item_index + 1}",
                        )
                        if self.status_icon:
                            self.status_icon.color = "#DC2626"
                            self.status_icon.update()
                    
                elif msg_type == "result":
                    # Add result to results manager
                    source = msg[1]
                    transcription = msg[2]
                    summary = msg[3]
                    
                    self.results_manager.add_result(source, transcription, summary)
                    
                    # Update file selector dropdown
                    self.file_selector.options.append(
                        ft.dropdown.Option(text=os.path.basename(source), key=source)
                    )
                    self.file_selector.update()
                    
                    self.show_snackbar(f"✅ Zakończono: {os.path.basename(source)}", success=True)
                    
                elif msg_type == "finished_all":
                    # All processing complete
                    self._update_progress(self.total_items, "Postęp: Zakończono wszystkie pliki")
                    
                    if self.status_icon:
                        self.status_icon.color = "#34D399" if self.error_items == 0 else "#FBBF24"
                        self.status_icon.update()
                    
                    if self.error_items:
                        self.update_status(f"⚠️ Zakończono z błędami ({self.error_items})")
                        self.show_snackbar("⚠️ Przetwarzanie zakończone z błędami", warning=True)
                    else:
                        self.update_status("✅ Przetwarzanie zakończone!")
                        self.show_snackbar("✅ Przetwarzanie zakończone!", success=True)
                    
                    # Exit polling loop
                    break
                    
            except queue.Empty:
                # No messages, continue polling
                continue
            except Exception as ex:
                # Log any polling errors
                print(f"Error in queue poller: {ex}")
                continue

    
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
        """Handle log save with animated feedback"""
        if e.path:
            # Show saving animation
            saving_snackbar = ft.SnackBar(
                content=ft.Row([
                    ft.ProgressRing(width=20, height=20, stroke_width=3, color="#2563EB"),
                    ft.Text("Zapisywanie logu..."),
                ], spacing=10),
                duration=1000,
            )
            self.page.overlay.append(saving_snackbar)
            saving_snackbar.open = True
            self.page.update()
            
            try:
                with open(e.path, 'w', encoding='utf-8') as f:
                    f.write(self.console_output.value or "")
                
                # Close saving animation
                import time
                time.sleep(0.3)
                saving_snackbar.open = False
                self.page.update()
                
                # Show success
                self.show_snackbar(f"💾 Log zapisany: {e.path}", success=True)
            except Exception as ex:
                saving_snackbar.open = False
                self.page.update()
                self.show_snackbar(f"❌ Błąd zapisu: {str(ex)}", error=True)
    
    def clear_console(self, e):
        """Clear console output with animation"""
        # Fade out animation
        if self.console_output.value:
            self.console_output.opacity = 0.3
            self.console_output.update()
            
            import time
            time.sleep(0.2)
            
            # Clear content
            self.console_output.value = ""
            
            # Fade back in
            self.console_output.opacity = 1.0
            self.console_output.update()
            
            self.update_status("🗑️ Konsola wyczyszczona")
            self.show_snackbar("🗑️ Konsola wyczyszczona", success=True)
        else:
            self.show_snackbar("ℹ️ Konsola jest już pusta", success=True)
    
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
        if self.status_message_text:
            self.status_message_text.value = message
            self.status_message_text.update()
    
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
