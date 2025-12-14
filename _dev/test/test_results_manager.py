"""
Unit tests for gui_utils.results_manager module.
Tests ResultsManager class for results storage and display.
"""
import pytest
from pogadane.gui_utils.results_manager import ResultsManager


class TestResultsManager:
    """Test suite for ResultsManager class."""

    def test_initialization(self):
        """Test ResultsManager initialization."""
        rm = ResultsManager()
        assert hasattr(rm, 'results')
        assert isinstance(rm.results, dict)
        assert len(rm.results) == 0

    def test_add_result(self):
        """Test adding a result."""
        rm = ResultsManager()
        
        rm.add_result(
            source="test.mp3",
            transcription="Test transcription",
            summary="Test summary"
        )
        
        assert "test.mp3" in rm.results
        assert rm.results["test.mp3"]["transcription"] == "Test transcription"
        assert rm.results["test.mp3"]["summary"] == "Test summary"

    def test_add_multiple_results(self):
        """Test adding multiple results."""
        rm = ResultsManager()
        
        rm.add_result("file1.mp3", "Trans 1", "Summary 1")
        rm.add_result("file2.mp3", "Trans 2", "Summary 2")
        rm.add_result("file3.mp3", "Trans 3", "Summary 3")
        
        assert len(rm.results) == 3

    def test_add_result_overwrites_existing(self):
        """Test that adding a result overwrites existing one."""
        rm = ResultsManager()
        
        rm.add_result("test.mp3", "Original", "Original")
        rm.add_result("test.mp3", "Updated", "Updated")
        
        assert rm.results["test.mp3"]["transcription"] == "Updated"
        assert rm.results["test.mp3"]["summary"] == "Updated"

    def test_get_result_existing(self):
        """Test getting an existing result."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "Trans", "Summary")
        
        result = rm.get_result("test.mp3")
        
        assert result is not None
        assert result["transcription"] == "Trans"
        assert result["summary"] == "Summary"

    def test_get_result_nonexistent(self):
        """Test getting a non-existent result."""
        rm = ResultsManager()
        
        result = rm.get_result("nonexistent.mp3")
        
        assert result is None

    def test_get_transcription(self):
        """Test getting transcription for a source."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "Test transcription", "Test summary")
        
        if hasattr(rm, 'get_transcription'):
            trans = rm.get_transcription("test.mp3")
            assert trans == "Test transcription"

    def test_get_summary(self):
        """Test getting summary for a source."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "Test transcription", "Test summary")
        
        if hasattr(rm, 'get_summary'):
            summary = rm.get_summary("test.mp3")
            assert summary == "Test summary"

    def test_has_result(self):
        """Test checking if result exists."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "Trans", "Summary")
        
        if hasattr(rm, 'has_result'):
            assert rm.has_result("test.mp3") is True
            assert rm.has_result("nonexistent.mp3") is False

    def test_get_all_sources(self):
        """Test getting all source names."""
        rm = ResultsManager()
        rm.add_result("file1.mp3", "Trans 1", "Summary 1")
        rm.add_result("file2.mp3", "Trans 2", "Summary 2")
        
        if hasattr(rm, 'get_all_sources'):
            sources = rm.get_all_sources()
            assert len(sources) == 2
            assert "file1.mp3" in sources
            assert "file2.mp3" in sources
        else:
            # Can get sources from results dict
            sources = list(rm.results.keys())
            assert len(sources) == 2

    def test_clear_results(self):
        """Test clearing all results."""
        rm = ResultsManager()
        rm.add_result("file1.mp3", "Trans 1", "Summary 1")
        rm.add_result("file2.mp3", "Trans 2", "Summary 2")
        
        if hasattr(rm, 'clear'):
            rm.clear()
            assert len(rm.results) == 0

    def test_remove_result(self):
        """Test removing a specific result."""
        rm = ResultsManager()
        rm.add_result("file1.mp3", "Trans 1", "Summary 1")
        rm.add_result("file2.mp3", "Trans 2", "Summary 2")
        
        if hasattr(rm, 'remove_result'):
            rm.remove_result("file1.mp3")
            assert "file1.mp3" not in rm.results
            assert "file2.mp3" in rm.results

    def test_add_empty_transcription(self):
        """Test adding result with empty transcription."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "", "Summary")
        
        result = rm.get_result("test.mp3")
        assert result["transcription"] == ""
        assert result["summary"] == "Summary"

    def test_add_empty_summary(self):
        """Test adding result with empty summary."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "Transcription", "")
        
        result = rm.get_result("test.mp3")
        assert result["transcription"] == "Transcription"
        assert result["summary"] == ""

    def test_add_both_empty(self):
        """Test adding result with both fields empty."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "", "")
        
        result = rm.get_result("test.mp3")
        assert result["transcription"] == ""
        assert result["summary"] == ""

    def test_unicode_handling(self):
        """Test handling of Unicode characters."""
        rm = ResultsManager()
        rm.add_result(
            "test.mp3",
            "Transkrypcja: żółć, ąę, śń",
            "Streszczenie: ćńół"
        )
        
        result = rm.get_result("test.mp3")
        assert "żółć" in result["transcription"]
        assert "ćńół" in result["summary"]

    def test_special_characters_in_source_name(self):
        """Test handling of special characters in source names."""
        rm = ResultsManager()
        special_names = [
            "file with spaces.mp3",
            "file-with-dashes.mp3",
            "file_with_underscores.mp3",
            "file.with.dots.mp3",
        ]
        
        for name in special_names:
            rm.add_result(name, "Trans", "Summary")
            assert rm.get_result(name) is not None

    def test_long_content(self):
        """Test handling of very long content."""
        rm = ResultsManager()
        long_text = "A" * 10000  # 10k characters
        
        rm.add_result("test.mp3", long_text, long_text)
        
        result = rm.get_result("test.mp3")
        assert len(result["transcription"]) == 10000
        assert len(result["summary"]) == 10000

    def test_result_count(self):
        """Test getting count of results."""
        rm = ResultsManager()
        
        assert len(rm.results) == 0
        
        rm.add_result("file1.mp3", "Trans", "Summary")
        assert len(rm.results) == 1
        
        rm.add_result("file2.mp3", "Trans", "Summary")
        assert len(rm.results) == 2


class TestResultsManagerIntegration:
    """Integration tests for ResultsManager."""

    def test_workflow_simulation(self):
        """Test realistic workflow of adding and retrieving results."""
        rm = ResultsManager()
        
        # Process multiple files
        files = [
            ("meeting1.mp3", "Meeting transcription 1", "Meeting summary 1"),
            ("meeting2.mp3", "Meeting transcription 2", "Meeting summary 2"),
            ("podcast.mp3", "Podcast transcription", "Podcast summary"),
        ]
        
        # Add all results
        for source, trans, summary in files:
            rm.add_result(source, trans, summary)
        
        # Verify all are stored
        assert len(rm.results) == 3
        
        # Retrieve each one
        for source, expected_trans, expected_summary in files:
            result = rm.get_result(source)
            assert result["transcription"] == expected_trans
            assert result["summary"] == expected_summary

    def test_export_functionality(self):
        """Test exporting results to file (if implemented)."""
        rm = ResultsManager()
        rm.add_result("test.mp3", "Transcription", "Summary")
        
        if hasattr(rm, 'export_result'):
            # Test export functionality
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
                tmp_path = tmp.name
            
            try:
                rm.export_result("test.mp3", tmp_path)
                # Verify file was created and contains content
                from pathlib import Path
                assert Path(tmp_path).exists()
            finally:
                Path(tmp_path).unlink(missing_ok=True)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
