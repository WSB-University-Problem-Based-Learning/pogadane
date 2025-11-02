"""
FontManager - Manages font settings and dynamic font scaling for GUI.

This module provides centralized font management for the Pogadane GUI application,
following the Single Responsibility Principle.
"""

from tkinter import font as tkFont
from typing import Dict, Any, Optional
import ttkbootstrap as ttk


class FontManager:
    """
    Manages font settings and dynamic scaling for GUI widgets.
    
    Provides centralized font configuration with support for:
    - Multiple font types (default, label, button, header, etc.)
    - Dynamic font size scaling (zoom in/out)
    - Consistent style application across widgets
    - TTK style integration
    
    Attributes:
        base_font_size (int): Base font size for calculations (default: 10)
        font_settings (Dict[str, tkFont.Font]): Dictionary of configured fonts
    """
    
    def __init__(self, base_font_size: int = 10):
        """
        Initialize FontManager with base font size.
        
        Args:
            base_font_size: Initial base font size (default: 10)
        """
        self.base_font_size = base_font_size
        self.font_settings: Dict[str, tkFont.Font] = {}
        self._initialize_fonts()
    
    def _initialize_fonts(self) -> None:
        """Create all font objects with current base size."""
        self.font_settings = {
            "default": tkFont.Font(family="Segoe UI Emoji", size=self.base_font_size),
            "label": tkFont.Font(family="Segoe UI", size=self.base_font_size),
            "button": tkFont.Font(family="Segoe UI", size=self.base_font_size),
            "scrolledtext": tkFont.Font(family="Segoe UI Emoji", size=self.base_font_size),
            "header": tkFont.Font(family="Segoe UI Emoji", size=self.base_font_size + 2, weight="bold"),
            "tooltip": tkFont.Font(family="Segoe UI", size=max(8, self.base_font_size - 1)),
            "list_header": tkFont.Font(family="Segoe UI", size=self.base_font_size, weight="bold"),
        }
    
    def change_font_size(self, delta: int) -> int:
        """
        Change base font size by delta value.
        
        Args:
            delta: Amount to change font size (positive or negative)
            
        Returns:
            New base font size after change
        """
        self.base_font_size += delta
        # Clamp between 8 and 24
        self.base_font_size = max(8, min(24, self.base_font_size))
        
        # Update all font objects
        for key in self.font_settings:
            new_size = self._calculate_font_size(key)
            self.font_settings[key].config(size=new_size)
        
        return self.base_font_size
    
    def _calculate_font_size(self, font_key: str) -> int:
        """
        Calculate font size for specific font type.
        
        Args:
            font_key: Font type identifier
            
        Returns:
            Calculated font size
        """
        if font_key == "header":
            return self.base_font_size + 2
        elif font_key == "tooltip":
            return max(8, self.base_font_size - 1)
        else:
            return self.base_font_size
    
    def update_ttk_styles(self, style: ttk.Style) -> None:
        """
        Update TTK style configurations with current fonts.
        
        Args:
            style: TTK Style object to configure
        """
        style.configure("TLabel", font=self.font_settings["label"])
        style.configure("TButton", font=self.font_settings["button"])
        style.configure("Outline.TButton", font=self.font_settings["button"])
        style.configure("Success.TButton", font=self.font_settings["button"])
        style.configure("TMenubutton", font=self.font_settings["button"])
        style.configure("TCombobox", font=self.font_settings["default"])
        style.configure("Treeview.Heading", font=self.font_settings["list_header"])
        style.configure(
            "Custom.Treeview",
            font=self.font_settings["default"],
            rowheight=int(self.font_settings["default"].actual("size") * 2.5)
        )
        style.configure("TProgressbar")
        style.configure("TLabelframe.Label", font=self.font_settings["label"])
        style.configure("Custom.TNotebook.Tab", font=self.font_settings["button"])
        style.configure("Switch.TCheckbutton", font=self.font_settings["label"])
    
    def update_widget_fonts(self, widgets: Dict[str, Any], scrolled_widgets: list) -> None:
        """
        Update fonts for specific widget collections.
        
        Args:
            widgets: Dictionary mapping widgets to font keys
            scrolled_widgets: List of ScrolledText widgets to update
        """
        # Update regular widgets
        for widget, font_obj in widgets.items():
            if widget and widget.winfo_exists():
                widget.config(font=font_obj)
        
        # Update ScrolledText widgets (need special handling)
        for scrolled_widget in scrolled_widgets:
            if scrolled_widget and scrolled_widget.winfo_exists():
                scrolled_widget.text.config(font=self.font_settings["scrolledtext"])
    
    def get_font(self, font_key: str) -> Optional[tkFont.Font]:
        """
        Get font object by key.
        
        Args:
            font_key: Font type identifier
            
        Returns:
            Font object or None if not found
        """
        return self.font_settings.get(font_key)
    
    def get_all_fonts(self) -> Dict[str, tkFont.Font]:
        """
        Get all font settings.
        
        Returns:
            Dictionary of all configured fonts
        """
        return self.font_settings.copy()
