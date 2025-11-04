"""
ResultsManager - Manages processed results storage.

This module handles storage and retrieval of processing results
following the Single Responsibility Principle.
"""

from typing import Dict, Any, Optional


class ResultsManager:
    """
    Manages processed results storage.
    
    Handles:
    - Storage of transcription and summary results
    - Results retrieval by source identifier
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

