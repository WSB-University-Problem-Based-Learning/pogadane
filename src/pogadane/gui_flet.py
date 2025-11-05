"""
Pogadane GUI - Material 3 Expressive
Beautiful Material Design 3 interface using Flet (Flutter-based)
100% GUI-based - no CLI dependencies, native Python logging
"""

import flet as ft
import threading
import queue
import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
from .backend import PogadaneBackend, ProgressUpdate, ProcessingStage


# Configure GUI logger
logger = logging.getLogger(__name__)


class PogadaneApp:
    """Main Pogadane Application with Material 3 Expressive Design"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Pogadane"
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Start with light mode
        self.page.padding = 0
        
        # Set base path for locating scripts
        self.base_path = Path(__file__).parent
        
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
        
        # Create spinning progress indicator (hidden by default)
        status_spinner = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            color="#2563EB",
            visible=False,
        )
        
        status_chip = ft.Container(
            content=ft.Row(
                [
                    status_spinner,
                    status_text,
                ],
                spacing=8,
                tight=True,
            ),
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
            "status_spinner": status_spinner,
            "container": container,
            "icon": icon_name,
            "display_name": display_name,
        }

    def _set_queue_item_status(self, index: int, status: str):
        """Update visual status for a queue entry with animated spinner"""

        if index < 0 or index >= len(self.queue_items):
            return

        item = self.queue_items[index]
        status_text: ft.Text = item["status_text"]
        status_chip: ft.Container = item["status_chip"]
        status_spinner: ft.ProgressRing = item.get("status_spinner")
        container: ft.Container = item["container"]

        if status == FILE_STATUS_PROCESSING:
            status_text.value = "Przetwarzanie"
            status_text.color = "#2563EB"
            status_chip.bgcolor = "#DBEAFE"
            if status_spinner:
                status_spinner.visible = True
            # Remove click handler during processing
            container.on_click = None
            container.ink = False
        elif status == FILE_STATUS_COMPLETED:
            status_text.value = "Zakończono → Zobacz wyniki"
            status_text.color = "#047857"
            status_chip.bgcolor = "#D1FAE5"
            if status_spinner:
                status_spinner.visible = False
            # Add click handler for completed items
            source_value = item["value"]
            container.on_click = lambda _, src=source_value: self.view_result_from_queue(src)
            container.ink = True
            container.tooltip = "Kliknij aby zobaczyć wyniki"
        elif status == FILE_STATUS_ERROR:
            status_text.value = "Błąd"
            status_text.color = "#991B1B"
            status_chip.bgcolor = "#FEE2E2"
            if status_spinner:
                status_spinner.visible = False
            # Remove click handler on error
            container.on_click = None
            container.ink = False
        else:
            status_text.value = "Oczekuje"
            status_text.color = "#6B7280"
            status_chip.bgcolor = "#E5E7EB"
            if status_spinner:
                status_spinner.visible = False
            # Remove click handler while pending
            container.on_click = None
            container.ink = False

        item["status"] = status
        status_chip.update()
        status_text.update()
        if status_spinner:
            status_spinner.update()
        container.update()

    def view_result_from_queue(self, source: str):
        """Navigate to results tab and display the selected file"""
        # Switch to Results tab (index 1)
        self.tabs.selected_index = 1
        self.tabs.update()
        
        # Select the file in the dropdown
        self.file_selector.value = source
        self.file_selector.update()
        
        # Display the results
        self.display_selected_result(None)
        
        # Show success message
        self.show_snackbar(f"📄 Wyświetlanie: {os.path.basename(source)}", success=True)

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

        # Only update if element is already added to page
        if self.queue_placeholder and hasattr(self.queue_placeholder, 'page') and self.queue_placeholder.page:
            self.queue_placeholder.bgcolor = queue_placeholder_bg
            self.queue_placeholder.update()

        for item in self.queue_items:
            container: ft.Container = item["container"]
            # Only update if element is already added to page
            if hasattr(container, 'page') and container.page:
                container.bgcolor = queue_card_bg
                container.border = ft.border.all(1, queue_border_color)
                container.update()
    
    def create_console_tab(self):
        """Create modern console output tab with live monitoring"""
        
        # Header with info
        console_header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.TERMINAL_ROUNDED, size=24, color="#7C3AED"),
                    ft.Column(
                        [
                            ft.Text("Monitor Procesów", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Podgląd na żywo przetwarzania audio i generowania podsumowań", size=13, color="#6B7280"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.only(bottom=16),
        )
        
        # Console output with monospace font and better styling
        self.console_output = ft.TextField(
            value="",
            multiline=True,
            read_only=True,
            border_radius=16,
            filled=True,
            text_size=11,
            min_lines=25,
            expand=True,
            bgcolor="#1F2937" if self.page.theme_mode == ft.ThemeMode.DARK else "#F9FAFB",
            color="#E5E7EB" if self.page.theme_mode == ft.ThemeMode.DARK else "#111827",
            border_color="#374151",
            cursor_color="#2563EB",
        )
        
        # Action buttons
        buttons = ft.Row(
            [
                ft.FilledButton(
                    "Zapisz Log",
                    icon=ft.Icons.DOWNLOAD_ROUNDED,
                    on_click=self.save_console_log,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        bgcolor="#2563EB",
                        color="#FFFFFF",
                    ),
                ),
                ft.OutlinedButton(
                    "Wyczyść Konsol ę",
                    icon=ft.Icons.DELETE_SWEEP_ROUNDED,
                    on_click=self.clear_console,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        side=ft.BorderSide(1, "#DC2626"),
                        color="#DC2626",
                    ),
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color="#6B7280"),
                            ft.Text("Automatyczne przewijanie", size=12, color="#6B7280"),
                        ],
                        spacing=6,
                    ),
                ),
            ],
            spacing=12,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    console_header,
                    self.console_output,
                    ft.Container(height=16),
                    buttons,
                ],
                spacing=0,
                expand=True,
            ),
            padding=24,
            expand=True,
        )
    
    def create_results_viewer_tab(self):
        """Create modern results viewer with card-based layout"""

        # Header
        results_header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ANALYTICS_ROUNDED, size=24, color="#34D399"),
                    ft.Column(
                        [
                            ft.Text("Przeglądarka Wyników", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Przeglądaj transkrypcje i podsumowania przetworzonych plików", size=13, color="#6B7280"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.only(bottom=20),
        )

        # File selector with search
        self.file_selector = ft.Dropdown(
            label="📁 Wybierz przetworzony plik",
            hint_text="Wybierz z listy aby zobaczyć wyniki...",
            on_change=self.display_selected_result,
            border_radius=12,
            filled=True,
            border_color="#2563EB",
            focused_border_color="#2563EB",
            width=400,
        )

        # Empty state
        self.results_empty_state = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ARTICLE_OUTLINED, size=64, color="#9CA3AF"),
                    ft.Text(
                        "Brak wyników",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#374151",
                    ),
                    ft.Text(
                        "Przetworz pierwszy plik, aby zobaczyć transkrypcję i podsumowanie.",
                        size=14,
                        color="#6B7280",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=12),
                    ft.FilledButton(
                        "Przejdź do Kolejki",
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        on_click=lambda _: setattr(self.tabs, 'selected_index', 0) or self.tabs.update(),
                        style=ft.ButtonStyle(
                            bgcolor="#7C3AED",
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=16,
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            padding=60,
            alignment=ft.alignment.center,
            expand=True,
        )

        # Transcription card
        self.transcription_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SPEAKER_NOTES_ROUNDED, size=20, color="#2563EB"),
                            ft.Text("Transkrypcja", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.COPY_ROUNDED,
                                tooltip="Kopiuj do schowka",
                                icon_size=18,
                                on_click=lambda _: self.copy_to_clipboard(self.transcription_output.value, "Transkrypcję"),
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=1, color="#E5E7EB"),
                    ft.Container(
                        content=ft.TextField(
                            value="",
                            multiline=True,
                            read_only=True,
                            border=ft.InputBorder.NONE,
                            text_size=13,
                            min_lines=15,
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=16,
            padding=20,
            bgcolor="#FFFFFF" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
            expand=True,
            visible=False,
        )
        self.transcription_output = self.transcription_card.content.controls[2].content

        # Summary card
        self.summary_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, size=20, color="#34D399"),
                            ft.Text("Podsumowanie AI", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.COPY_ROUNDED,
                                tooltip="Kopiuj do schowka",
                                icon_size=18,
                                on_click=lambda _: self.copy_to_clipboard(self.summary_output.value, "Podsumowanie"),
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=1, color="#E5E7EB"),
                    ft.Container(
                        content=ft.TextField(
                            value="",
                            multiline=True,
                            read_only=True,
                            border=ft.InputBorder.NONE,
                            text_size=13,
                            min_lines=15,
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=16,
            padding=20,
            bgcolor="#FFFFFF" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
            expand=True,
            visible=False,
        )
        self.summary_output = self.summary_card.content.controls[2].content

        # Content area with cards
        self.results_content = ft.Column(
            [
                self.results_empty_state,
            ],
            spacing=16,
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    results_header,
                    self.file_selector,
                    ft.Container(height=8),
                    ft.Container(
                        content=self.results_content,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            padding=24,
            expand=True,
        )

    def create_presets_selector(self):
        """Create fancy preset selector with Fast/Medium/Slow options"""
        
        # Preset configurations
        PRESETS = {
            "fast": {
                "name": "⚡ Szybki",
                "description": "Najszybsze przetwarzanie, mniejsze modele",
                "color": "#34D399",
                "icon": ft.Icons.FLASH_ON_ROUNDED,
                "settings": {
                    "TRANSCRIPTION_PROVIDER": "faster-whisper",
                    "WHISPER_MODEL": "base",
                    "FASTER_WHISPER_DEVICE": "auto",
                    "FASTER_WHISPER_COMPUTE_TYPE": "int8",
                    "FASTER_WHISPER_BATCH_SIZE": 16,
                    "SUMMARY_PROVIDER": "transformers",
                    "TRANSFORMERS_MODEL": "google/flan-t5-small",
                }
            },
            "medium": {
                "name": "⚖️ Zrównoważony",
                "description": "Dobra równowaga jakości i szybkości",
                "color": "#2563EB",
                "icon": ft.Icons.BALANCE_ROUNDED,
                "settings": {
                    "TRANSCRIPTION_PROVIDER": "faster-whisper",
                    "WHISPER_MODEL": "turbo",
                    "FASTER_WHISPER_DEVICE": "auto",
                    "FASTER_WHISPER_COMPUTE_TYPE": "auto",
                    "FASTER_WHISPER_BATCH_SIZE": 0,
                    "SUMMARY_PROVIDER": "transformers",
                    "TRANSFORMERS_MODEL": "facebook/bart-large-cnn",
                }
            },
            "slow": {
                "name": "🎯 Precyzyjny",
                "description": "Najlepsza jakość, wolniejsze przetwarzanie",
                "color": "#7C3AED",
                "icon": ft.Icons.HIGH_QUALITY_ROUNDED,
                "settings": {
                    "TRANSCRIPTION_PROVIDER": "faster-whisper",
                    "WHISPER_MODEL": "large-v3",
                    "FASTER_WHISPER_DEVICE": "auto",
                    "FASTER_WHISPER_COMPUTE_TYPE": "float16",
                    "FASTER_WHISPER_BATCH_SIZE": 0,
                    "SUMMARY_PROVIDER": "transformers",
                    "TRANSFORMERS_MODEL": "facebook/bart-large-cnn",
                }
            }
        }
        
        # Determine current preset based on settings
        current_preset = "medium"  # default
        current_model = getattr(self.config_module, "WHISPER_MODEL", "turbo")
        if current_model in ["tiny", "base", "small"]:
            current_preset = "fast"
        elif current_model in ["large-v3", "large-v2", "large"]:
            current_preset = "slow"
        
        # Slider value (0=fast, 1=medium, 2=slow)
        slider_value = {"fast": 0, "medium": 1, "slow": 2}[current_preset]
        
        def apply_preset(e):
            """Apply selected preset to all config fields"""
            slider_val = int(preset_slider.value)
            preset_key = ["fast", "medium", "slow"][slider_val]
            preset = PRESETS[preset_key]
            
            # Update preset indicator
            preset_name.value = preset["name"]
            preset_desc.value = preset["description"]
            preset_icon.name = preset["icon"]
            preset_icon.color = preset["color"]
            preset_card.border = ft.border.all(2, preset["color"])
            
            # Apply settings to config fields
            for key, value in preset["settings"].items():
                if key in self.config_fields:
                    field = self.config_fields[key]
                    if isinstance(field, ft.Switch):
                        field.value = bool(value)
                    elif hasattr(field, 'value'):
                        field.value = str(value)
            
            # Update all fields
            self.page.update()
            
            # Show feedback
            self.show_snackbar(f"Zastosowano preset: {preset['name']}", success=True)
        
        # Create slider
        preset_slider = ft.Slider(
            min=0,
            max=2,
            divisions=2,
            value=slider_value,
            label="{value}",
            on_change=apply_preset,
            active_color="#2563EB",
            inactive_color="#E5E7EB",
            thumb_color="#2563EB",
        )
        
        # Preset indicator
        current = PRESETS[current_preset]
        preset_icon = ft.Icon(current["icon"], size=32, color=current["color"])
        preset_name = ft.Text(current["name"], size=18, weight=ft.FontWeight.BOLD)
        preset_desc = ft.Text(current["description"], size=13, color="#6B7280")
        
        preset_card = ft.Container(
            content=ft.Row(
                [
                    preset_icon,
                    ft.Column(
                        [
                            preset_name,
                            preset_desc,
                        ],
                        spacing=4,
                        expand=True,
                    ),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
            border_radius=12,
            border=ft.border.all(2, current["color"]),
            bgcolor="#FFFFFF" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
        )
        
        # Slider labels
        slider_container = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("⚡ Szybki", size=12, color="#6B7280", expand=True),
                        ft.Text("⚖️ Zrównoważony", size=12, color="#6B7280", expand=True, text_align=ft.TextAlign.CENTER),
                        ft.Text("🎯 Precyzyjny", size=12, color="#6B7280", expand=True, text_align=ft.TextAlign.RIGHT),
                    ],
                ),
                preset_slider,
            ],
            spacing=8,
        )
        
        return ft.Column(
            [
                ft.Text("⚡ Presety Konfiguracji", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Wybierz profil wydajności - ustawienia zostaną automatycznie dostosowane", size=13, color="#6B7280"),
                ft.Container(height=12),
                preset_card,
                ft.Container(height=8),
                slider_container,
            ],
            spacing=0,
        )

    def create_config_section(self, title: str, fields: List[tuple], description: str = None):
        """
        Create a configuration section with fields - Compact & Modern Design
        
        Args:
            title: Section title
            fields: List of tuples (config_key, label, field_type, options, tooltip)
            description: Optional section description
        """
        
        section_fields = []
        
        # Compact section header with better visual hierarchy
        section_header = ft.Column(
            [
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Text(description, size=12, color="#6B7280", italic=True) if description else ft.Container(height=0),
            ],
            spacing=2,
        )
        section_fields.append(section_header)
        section_fields.append(ft.Container(height=12))
        
        # Create fields with compact spacing
        for field_info in fields:
            config_key = field_info[0]
            label = field_info[1]
            field_type = field_info[2]
            options = field_info[3] if len(field_info) > 3 else None
            tooltip = field_info[4] if len(field_info) > 4 else None
            
            current_value = getattr(self.config_module, config_key, DEFAULT_CONFIG.get(config_key, ""))
            
            # Create compact tooltip icon
            tooltip_icon = None
            if tooltip:
                tooltip_icon = ft.IconButton(
                    icon=ft.Icons.INFO_OUTLINE_ROUNDED,
                    icon_size=16,
                    tooltip=tooltip,
                    icon_color="#9CA3AF",
                    on_click=None,
                    style=ft.ButtonStyle(padding=4),
                )
            
            if field_type == "dropdown":
                field = ft.Dropdown(
                    label=label,
                    value=str(current_value),
                    options=[ft.dropdown.Option(opt) for opt in options],
                    border_radius=8,
                    filled=True,
                    expand=True,
                    dense=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    label_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    text_size=13,
                )
                self.config_fields[config_key] = field
                
                if tooltip_icon:
                    field_row = ft.Row([field, tooltip_icon], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    section_fields.append(field_row)
                else:
                    section_fields.append(field)
                
            elif field_type == "checkbox":
                switch = ft.Switch(value=bool(current_value), scale=0.9)
                field = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(label, size=13, weight=ft.FontWeight.W_500),
                            ft.Row([switch, tooltip_icon if tooltip_icon else ft.Container(width=0)], spacing=4),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border=ft.border.all(1, "#E5E7EB"),
                    border_radius=8,
                    bgcolor="#F9FAFB",
                )
                self.config_fields[config_key] = switch
                section_fields.append(field)
                
            elif field_type == "password":
                field = ft.TextField(
                    label=label,
                    value=str(current_value),
                    password=True,
                    can_reveal_password=True,
                    border_radius=8,
                    filled=True,
                    expand=True,
                    dense=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    label_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    text_size=13,
                )
                self.config_fields[config_key] = field
                
                if tooltip_icon:
                    field_row = ft.Row([field, tooltip_icon], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    section_fields.append(field_row)
                else:
                    section_fields.append(field)
                
            elif field_type == "file":
                file_field = ft.TextField(
                    label=label,
                    value=str(current_value),
                    border_radius=8,
                    filled=True,
                    read_only=True,
                    dense=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    label_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    text_size=13,
                )
                browse_btn = ft.IconButton(
                    icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                    icon_size=18,
                    tooltip="Przeglądaj...",
                    on_click=lambda _, f=file_field: self.browse_file(f),
                    style=ft.ButtonStyle(padding=4),
                )
                field = ft.Row(
                    [
                        ft.Container(content=file_field, expand=True),
                        browse_btn,
                        tooltip_icon if tooltip_icon else ft.Container(width=0),
                    ],
                    spacing=4,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                self.config_fields[config_key] = file_field
                section_fields.append(field)
                
            else:  # text
                field = ft.TextField(
                    label=label,
                    value=str(current_value),
                    border_radius=8,
                    filled=True,
                    expand=True,
                    dense=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    label_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    text_size=13,
                )
                self.config_fields[config_key] = field
                
                if tooltip_icon:
                    field_row = ft.Row([field, tooltip_icon], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    section_fields.append(field_row)
                else:
                    section_fields.append(field)
            
            # Reduced spacing between fields
            section_fields.append(ft.Container(height=6))
        
        return ft.Column(section_fields, spacing=0, scroll=ft.ScrollMode.AUTO)
    
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
            
            # ⚡ PRESETS SECTION - Quick configuration
            presets_section = self.create_presets_selector()
            
            # 🎙️ TRANSCRIPTION SETTINGS (Primary feature - shown first)
            transcription_section = self.create_config_section(
                title="🎙️ Transkrypcja Audio",
                description="Ustawienia konwersji mowy na tekst",
                fields=[
                    ("TRANSCRIPTION_PROVIDER", "Silnik transkrypcji", "dropdown", 
                     ["faster-whisper", "whisper"],
                     "faster-whisper: Zalecany, 4x szybszy | whisper: Standardowy OpenAI Whisper"),
                    
                    ("WHISPER_MODEL", "Model AI", "dropdown", 
                     ["tiny", "base", "small", "medium", "large-v3", "turbo"],
                     "turbo: Najszybszy (zalecany) | large-v3: Najdokładniejszy | tiny: Najmniejszy"),
                    
                    ("WHISPER_LANGUAGE", "Język audio", "dropdown",
                     ["Polish", "English", "German", "French", "Spanish", "Italian", "Ukrainian", "Russian"],
                     "Język nagrania do transkrypcji"),
                    
                    ("FASTER_WHISPER_DEVICE", "Akcelerator sprzętowy", "dropdown", 
                     ["auto", "cuda", "cpu"],
                     "auto: Automatyczny (zalecany) | cuda: GPU NVIDIA | cpu: Tylko procesor"),
                ]
            )
            
            # 🤖 SUMMARY SETTINGS
            summary_section = self.create_config_section(
                title="🤖 Generowanie Podsumowań",
                description="Ustawienia AI do tworzenia streszczeń",
                fields=[
                    ("SUMMARY_PROVIDER", "Dostawca AI", "dropdown", 
                     ["transformers", "ollama", "google"],
                     "transformers: Offline, lokalny (ZALECANY) | ollama: Wymaga instalacji Ollama | google: Wymaga klucza API"),
                    
                    ("TRANSFORMERS_MODEL", "Model Transformers", "dropdown",
                     ["facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6", "google/flan-t5-base", "google/flan-t5-small"],
                     "bart-large-cnn: Najlepsza jakość (~1.6GB) | distilbart: Szybszy (~500MB) | flan-t5-small: Najmniejszy (~300MB)"),
                    
                    ("OLLAMA_MODEL", "Model Ollama", "text", None,
                     "Nazwa modelu Ollama (np. gemma3:4b, llama3:8b)"),
                    
                    ("GOOGLE_API_KEY", "Klucz API Google Gemini", "password", None,
                     "Wymagany tylko dla dostawcy 'google'"),
                    
                    ("SUMMARY_LANGUAGE", "Język podsumowania", "dropdown",
                     ["Polish", "English", "German", "French", "Spanish"],
                     "Język wynikowego podsumowania"),
                ]
            )
            
            # ⚙️ ADVANCED SETTINGS (collapsible)
            advanced_section = self.create_config_section(
                title="⚙️ Ustawienia Zaawansowane",
                description="Opcje dla zaawansowanych użytkowników",
                fields=[
                    ("FASTER_WHISPER_BATCH_SIZE", "Batch Size (0 = wyłączone)", "text", None,
                     "Przetwarzanie wsadowe - większe wartości = szybsze, więcej RAM"),
                    
                    ("FASTER_WHISPER_COMPUTE_TYPE", "Typ obliczeń", "dropdown",
                     ["auto", "int8", "float16", "int8_float16"],
                     "auto: Automatyczny | int8: Szybszy, mniej pamięci | float16: Dokładniejszy"),
                    
                    ("FASTER_WHISPER_VAD_FILTER", "Voice Activity Detection", "checkbox", None,
                     "Wykrywanie aktywności głosowej - usuwa ciszę"),
                    
                    ("YT_DLP_PATH", "Ścieżka yt-dlp", "text", None,
                     "Domyślnie: yt-dlp (z PATH). Zmień tylko w razie problemów"),
                ]
            )
            
            # Dialog content with tabs for better organization
            dialog_content = ft.Container(
                content=ft.Column(
                    controls=[
                        # Presets at the top for quick access
                        ft.Container(
                            content=presets_section,
                            padding=ft.padding.symmetric(horizontal=20, vertical=16),
                            bgcolor="#F9FAFB" if self.page.theme_mode == ft.ThemeMode.LIGHT else "#1F2937",
                            border_radius=16,
                        ),
                        ft.Divider(height=1, color="#E5E7EB"),
                        # Tabs for detailed settings
                        ft.Tabs(
                            selected_index=0,
                            animation_duration=300,
                            tabs=[
                                ft.Tab(
                                    text="Transkrypcja",
                                    icon=ft.Icons.MIC_ROUNDED,
                                    content=ft.Container(
                                        content=transcription_section,
                                        padding=ft.padding.all(20),
                                    ),
                                ),
                                ft.Tab(
                                    text="Podsumowanie",
                                    icon=ft.Icons.AUTO_AWESOME_ROUNDED,
                                    content=ft.Container(
                                        content=summary_section,
                                        padding=ft.padding.all(20),
                                    ),
                                ),
                                ft.Tab(
                                    text="Zaawansowane",
                                    icon=ft.Icons.TUNE_ROUNDED,
                                    content=ft.Container(
                                        content=advanced_section,
                                        padding=ft.padding.all(20),
                                    ),
                                ),
                            ],
                            expand=1,
                        ),
                    ],
                    spacing=0,
                ),
                height=600,
                width=750,
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
                    # Left side: Reset button
                    ft.Container(
                        content=ft.OutlinedButton(
                            "Przywróć Domyślne",
                            icon=ft.Icons.RESTORE_ROUNDED,
                            on_click=lambda _: self.reset_to_defaults(settings_dialog),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                color="#DC2626",
                                side=ft.BorderSide(2, "#DC2626"),
                            ),
                        ),
                        expand=True,
                    ),
                    # Right side: Cancel and Save buttons
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
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
    
    def reset_to_defaults(self, settings_dialog):
        """Reset all configuration to default values with confirmation"""
        
        # Create confirmation dialog
        def confirm_reset(e):
            confirm_dialog.open = False
            self.page.update()
            
            # Show resetting indicator
            reset_dialog = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        ft.ProgressRing(width=50, height=50, color="#DC2626"),
                        ft.Text("Przywracanie domyślnych...", size=16, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    width=250,
                    height=120,
                ),
                modal=True,
            )
            
            self.page.overlay.append(reset_dialog)
            reset_dialog.open = True
            self.page.update()
            
            try:
                # Update all fields to default values
                for key, field in self.config_fields.items():
                    default_value = DEFAULT_CONFIG.get(key, "")
                    
                    if isinstance(field, ft.Switch):
                        field.value = bool(default_value)
                    elif hasattr(field, 'value'):
                        field.value = str(default_value)
                
                # Update the fields visually
                self.page.update()
                
                # Small delay to show the animation
                import time
                time.sleep(0.3)
                
                # Close reset dialog
                reset_dialog.open = False
                self.page.update()
                
                self.show_snackbar("Przywrócono domyślne ustawienia. Kliknij 'Zapisz i Zastosuj' aby zachować.", success=True)
                
            except Exception as ex:
                reset_dialog.open = False
                self.page.update()
                self.show_snackbar(f"Błąd przywracania domyślnych: {str(ex)}", error=True)
        
        def cancel_reset(e):
            confirm_dialog.open = False
            self.page.update()
        
        # Confirmation dialog
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING_ROUNDED, size=28, color="#FBBF24"),
                ft.Text("Przywrócić Domyślne?", size=20, weight=ft.FontWeight.BOLD),
            ], spacing=12),
            content=ft.Text(
                "Czy na pewno chcesz przywrócić wszystkie ustawienia do wartości domyślnych?\n\n"
                "Ta operacja zastąpi bieżące wartości, ale nie zapisze ich automatycznie. "
                "Będziesz musiał kliknąć 'Zapisz i Zastosuj' aby zachować zmiany.",
                size=14,
            ),
            actions=[
                ft.TextButton(
                    "Anuluj",
                    on_click=cancel_reset,
                ),
                ft.FilledButton(
                    "Przywróć Domyślne",
                    icon=ft.Icons.RESTORE_ROUNDED,
                    on_click=confirm_reset,
                    style=ft.ButtonStyle(
                        bgcolor="#DC2626",
                        color="#FFFFFF",
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
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
        """Execute batch processing using native progress callbacks - no stdout capture"""
        
        # Initialize backend (will use the same ConfigManager singleton as GUI)
        backend = PogadaneBackend()
        
        # Set environment variables for better compatibility
        os.environ['TQDM_DISABLE'] = '1'  # Disable tqdm progress bars
        os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'  # Disable HuggingFace progress bars
        
        for i, input_src in enumerate(input_sources):
            # Update queue status to PROCESSING
            self.output_queue.put(("update_status", str(i), FILE_STATUS_PROCESSING))
            
            try:
                # Define progress callback for this file
                def progress_callback(update: ProgressUpdate):
                    """Handle progress updates from backend"""
                    # Map stages to icons
                    icon_map = {
                        ProcessingStage.INITIALIZING: "🔧",
                        ProcessingStage.DOWNLOADING: "📥",
                        ProcessingStage.COPYING: "📄",
                        ProcessingStage.TRANSCRIBING: "🎤",
                        ProcessingStage.SUMMARIZING: "🤖",
                        ProcessingStage.CLEANING: "🧹",
                        ProcessingStage.COMPLETED: "✅",
                        ProcessingStage.ERROR: "❌"
                    }
                    icon = icon_map.get(update.stage, "ℹ️")
                    
                    # Format message with icon and progress
                    log_message = f"{icon} [{update.progress:.0%}] {update.message}\n"
                    
                    # Send to console
                    self.output_queue.put(("log", log_message, "", ""))
                
                # Process file using backend with native callbacks
                transcription, summary = backend.process_file(
                    input_src,
                    progress_callback=progress_callback
                )
                
                # Check results
                if transcription or summary:
                    self.output_queue.put(("result", input_src, transcription or "", summary or ""))
                    self.output_queue.put(("update_status", str(i), FILE_STATUS_COMPLETED))
                else:
                    self.output_queue.put(("error", f"⚠️ Nie znaleziono wyników dla: {input_src}", "", ""))
                    self.output_queue.put(("update_status", str(i), FILE_STATUS_ERROR))
                    
            except Exception as ex:
                logger.error(f"Error processing {input_src}: {ex}", exc_info=True)
                self.output_queue.put(("error", f"❌ Błąd podczas przetwarzania {input_src}: {ex}", "", ""))
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
        """Display selected file results in card-based layout"""
        if not self.file_selector.value:
            return
        
        # Get the selected file's source key
        source = self.file_selector.value
        
        # Retrieve results from manager
        result = self.results_manager.get_result(source)
        
        if result:
            # Update transcription
            transcription_text = result.get("transcription", "")
            self.transcription_output.value = transcription_text if transcription_text else "⚠️ Brak transkrypcji."
            
            # Update summary
            summary_text = result.get("summary", "")
            self.summary_output.value = summary_text if summary_text else "⚠️ Brak podsumowania."
            
            # Show cards, hide empty state
            self.results_empty_state.visible = False
            self.transcription_card.visible = True
            self.summary_card.visible = True
            
            # Update results content
            self.results_content.controls = [
                ft.Row(
                    [
                        self.transcription_card,
                        self.summary_card,
                    ],
                    spacing=16,
                    expand=True,
                )
            ]
            
            self.results_content.update()
            self.update_status(f"📄 Wyświetlanie: {os.path.basename(source)}")
        else:
            # Show empty state if no results
            self.results_empty_state.visible = True
            self.transcription_card.visible = False
            self.summary_card.visible = False
            self.results_content.controls = [self.results_empty_state]
            self.results_content.update()
    
    def copy_to_clipboard(self, text: str, content_type: str):
        """Copy text to clipboard with feedback"""
        if not text or text.startswith("⚠️"):
            self.show_snackbar(f"Brak treści do skopiowania", warning=True)
            return
        
        try:
            self.page.set_clipboard(text)
            self.show_snackbar(f"✅ {content_type} skopiowano do schowka!", success=True)
        except Exception as ex:
            self.show_snackbar(f"❌ Błąd kopiowania: {str(ex)}", error=True)
    
    def save_config(self, e):
        """Save configuration to file - preserves comments and structure"""
        try:
            config_path = self.config_manager.config_path
            
            # Read existing config file to preserve comments and structure
            with open(config_path, 'r', encoding='utf-8') as f:
                config_lines = f.readlines()
            
            # Build a mapping of values to update
            updates = {}
            for key, field in self.config_fields.items():
                if isinstance(field, ft.Switch):
                    updates[key] = field.value
                elif hasattr(field, 'value'):
                    value = field.value
                    
                    # Special type conversions for known integer fields
                    if key == "FASTER_WHISPER_BATCH_SIZE":
                        try:
                            value = int(value) if value else 0
                        except (ValueError, TypeError):
                            logger.warning(f"Invalid batch_size value '{value}', using 0")
                            value = 0
                    
                    updates[key] = value
            
            # Update lines in place, preserving comments and structure
            new_lines = []
            for line in config_lines:
                stripped = line.strip()
                
                # Skip empty lines and comments
                if not stripped or stripped.startswith('#'):
                    new_lines.append(line)
                    continue
                
                # Check if this line is a config assignment
                if '=' in line:
                    # Extract the variable name (before =)
                    var_name = line.split('=')[0].strip()
                    
                    # If this variable is in our updates, replace it
                    if var_name in updates:
                        value = updates[var_name]
                        
                        # Preserve inline comments if they exist
                        inline_comment = ""
                        if '#' in line:
                            comment_start = line.index('#')
                            inline_comment = " " + line[comment_start:]
                        
                        # Format the new value
                        if isinstance(value, bool):
                            new_line = f"{var_name} = {value}{inline_comment}"
                        elif isinstance(value, str):
                            new_line = f'{var_name} = "{value}"{inline_comment}'
                        elif isinstance(value, (int, float)):
                            new_line = f"{var_name} = {value}{inline_comment}"
                        else:
                            new_line = f'{var_name} = "{value}"{inline_comment}'
                        
                        new_lines.append(new_line if new_line.endswith('\n') else new_line + '\n')
                    else:
                        # Keep the line as-is if not in our updates
                        new_lines.append(line)
                else:
                    # Keep non-assignment lines as-is
                    new_lines.append(line)
            
            # Write updated config back to file
            with open(config_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            # Reload config
            self.config_manager.reload()
            self.config_module = self.config_manager.config
            
            self.show_snackbar("Konfiguracja zapisana pomyślnie!", success=True)
            self.update_status("Konfiguracja zapisana")
        except Exception as ex:
            self.show_snackbar(f"Błąd zapisu konfiguracji: {str(ex)}", error=True)
            import traceback
            traceback.print_exc()
    
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
    """Main entry point for Flet app with native Python logging"""
    # Configure logging for GUI
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pogadane.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger.info("Starting Pogadane GUI")
    PogadaneApp(page)


if __name__ == "__main__":
    ft.app(target=main)
