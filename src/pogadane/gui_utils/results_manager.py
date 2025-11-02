"""
ResultsManager - Manages processed results storage and display.

This module handles storage, retrieval, and display of processing results
following the Single Responsibility Principle.
"""

from typing import Dict, Any, Optional, Tuple
from ttkbootstrap.widgets.scrolled import ScrolledText
import ttkbootstrap as ttk
from tkinter import END, DISABLED, NORMAL


class ResultsManager:
    """
    Manages processed results storage and display.
    
    Handles:
    - Storage of transcription and summary results
    - Results retrieval by source identifier
    - Display of results in GUI widgets
    - Results metadata tracking
    
    Attributes:
        results_data (Dict[str, Dict[str, str]]): Stored results indexed by source
    """
    
    def __init__(self):
        """Initialize ResultsManager with empty storage."""
        self.results_data: Dict[str, Dict[str, str]] = {}
    
    def add_result(self, source: str, transcription: str, summary: str) -> None:
        """
        Add or update processing result.
        
        Args:
            source: Source identifier (file path or URL)
            transcription: Transcription text
            summary: Summary text
        """
        self.results_data[source] = {
            "transcription": transcription,
            "summary": summary
        }
    
    def get_result(self, source: str) -> Optional[Dict[str, str]]:
        """
        Retrieve result by source identifier.
        
        Args:
            source: Source identifier
            
        Returns:
            Dictionary with transcription and summary, or None if not found
        """
        return self.results_data.get(source)
    
    def get_all_sources(self) -> list:
        """
        Get list of all processed sources.
        
        Returns:
            List of source identifiers
        """
        return list(self.results_data.keys())
    
    def clear_all(self) -> None:
        """Clear all stored results."""
        self.results_data.clear()
    
    def has_results(self) -> bool:
        """
        Check if any results are stored.
        
        Returns:
            True if results exist, False otherwise
        """
        return bool(self.results_data)
    
    def get_result_count(self) -> int:
        """
        Get total number of stored results.
        
        Returns:
            Number of results
        """
        return len(self.results_data)
    
    def display_result(
        self,
        source: str,
        transcription_widget: ScrolledText,
        summary_widget: ScrolledText,
        insert_markdown_func: callable = None
    ) -> bool:
        """
        Display result in GUI widgets.
        
        Args:
            source: Source identifier
            transcription_widget: ScrolledText widget for transcription
            summary_widget: ScrolledText widget for summary
            insert_markdown_func: Optional function to render markdown in summary
            
        Returns:
            True if result was displayed, False if source not found
        """
        result = self.get_result(source)
        
        if result:
            # Display transcription (plain text)
            self._update_scrolled_text(
                transcription_widget,
                result.get("transcription", "Brak transkrypcji.")
            )
            
            # Display summary (with markdown if function provided)
            summary_text = result.get("summary", "Brak podsumowania.")
            if insert_markdown_func:
                insert_markdown_func(summary_widget, summary_text)
            else:
                self._update_scrolled_text(summary_widget, summary_text)
            
            return True
        else:
            # Clear both widgets if source not found
            self._clear_scrolled_text(transcription_widget)
            self._clear_scrolled_text(summary_widget)
            return False
    
    def _update_scrolled_text(self, widget: ScrolledText, content: str) -> None:
        """
        Update ScrolledText widget content.
        
        Args:
            widget: ScrolledText widget to update
            content: Text content to display
        """
        widget.text.config(state=NORMAL)
        widget.text.delete("1.0", END)
        widget.text.insert("1.0", content)
        widget.text.config(state=DISABLED)
    
    def _clear_scrolled_text(self, widget: ScrolledText) -> None:
        """
        Clear ScrolledText widget content.
        
        Args:
            widget: ScrolledText widget to clear
        """
        widget.text.config(state=NORMAL)
        widget.text.delete("1.0", END)
        widget.text.config(state=DISABLED)
    
    def export_all_results(self) -> str:
        """
        Export all results as formatted text.
        
        Returns:
            Formatted text containing all results
        """
        if not self.results_data:
            return "Brak wyników do eksportu."
        
        lines = []
        for i, (source, data) in enumerate(self.results_data.items(), 1):
            lines.append(f"{'=' * 80}")
            lines.append(f"WYNIK #{i}: {source}")
            lines.append(f"{'=' * 80}")
            lines.append("")
            lines.append("--- TRANSKRYPCJA ---")
            lines.append(data.get("transcription", "Brak transkrypcji."))
            lines.append("")
            lines.append("--- STRESZCZENIE ---")
            lines.append(data.get("summary", "Brak streszczenia."))
            lines.append("")
        
        return "\n".join(lines)
