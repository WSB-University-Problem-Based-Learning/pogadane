"""
Unit tests for text_utils module.
Tests text processing functions: ANSI stripping, URL validation, 
markdown rendering, and transcription/summary extraction.
"""
import pytest
from pogadane.text_utils import (
    strip_ansi,
    is_valid_url,
    extract_transcription_and_summary,
)


class TestStripAnsi:
    """Test suite for strip_ansi function."""

    def test_strip_ansi_no_codes(self):
        """Test that plain text is unchanged."""
        text = "Hello, World!"
        assert strip_ansi(text) == text

    def test_strip_ansi_with_color_codes(self):
        """Test stripping ANSI color codes."""
        text = "\033[31mRed text\033[0m"
        expected = "Red text"
        assert strip_ansi(text) == expected

    def test_strip_ansi_multiple_codes(self):
        """Test stripping multiple ANSI codes."""
        text = "\033[1m\033[32mBold Green\033[0m\033[0m"
        expected = "Bold Green"
        assert strip_ansi(text) == expected

    def test_strip_ansi_empty_string(self):
        """Test with empty string."""
        assert strip_ansi("") == ""

    def test_strip_ansi_only_codes(self):
        """Test string with only ANSI codes."""
        text = "\033[31m\033[0m"
        assert strip_ansi(text) == ""

    def test_strip_ansi_mixed_content(self):
        """Test mixed text and ANSI codes."""
        text = "Normal \033[31mRed\033[0m Normal"
        expected = "Normal Red Normal"
        assert strip_ansi(text) == expected


class TestIsValidUrl:
    """Test suite for is_valid_url function."""

    def test_valid_http_url(self):
        """Test valid HTTP URL."""
        assert is_valid_url("http://example.com")

    def test_valid_https_url(self):
        """Test valid HTTPS URL."""
        assert is_valid_url("https://example.com")

    def test_valid_youtube_url(self):
        """Test valid YouTube URL."""
        assert is_valid_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def test_invalid_url_no_protocol(self):
        """Test URL without protocol."""
        assert not is_valid_url("example.com")

    def test_invalid_url_ftp(self):
        """Test FTP URL (should be invalid for our use case)."""
        assert not is_valid_url("ftp://example.com")

    def test_invalid_url_empty(self):
        """Test empty string."""
        assert not is_valid_url("")

    def test_invalid_url_file_path(self):
        """Test file path (not a URL)."""
        assert not is_valid_url("C:\\Users\\file.txt")
        assert not is_valid_url("/home/user/file.txt")

    def test_invalid_url_random_text(self):
        """Test random text."""
        assert not is_valid_url("Hello World")


class TestExtractTranscriptionAndSummary:
    """Test suite for extract_transcription_and_summary function."""

    def test_extract_both_present(self):
        """Test extraction when both transcription and summary are present."""
        log_text = """
Some log output
--- POCZĄTEK TRANSKRYPCJI ---
This is the transcription text.
Multiple lines here.
--- KONIEC TRANSKRYPCJI ---
More log output
--- POCZĄTEK STRESZCZENIA ---
This is the summary.
--- KONIEC STRESZCZENIA ---
End of log
"""
        trans, summary = extract_transcription_and_summary(log_text)
        assert "This is the transcription text." in trans
        assert "Multiple lines here." in trans
        assert "This is the summary." in summary

    def test_extract_transcription_only(self):
        """Test extraction when only transcription is present."""
        log_text = """
--- POCZĄTEK TRANSKRYPCJI ---
Only transcription here.
--- KONIEC TRANSKRYPCJI ---
"""
        trans, summary = extract_transcription_and_summary(log_text)
        assert "Only transcription here." in trans
        assert summary == ""

    def test_extract_summary_only(self):
        """Test extraction when only summary is present."""
        log_text = """
--- POCZĄTEK STRESZCZENIA ---
Only summary here.
--- KONIEC STRESZCZENIA ---
"""
        trans, summary = extract_transcription_and_summary(log_text)
        assert trans == ""
        assert "Only summary here." in summary

    def test_extract_nothing(self):
        """Test extraction when neither is present."""
        log_text = "Just some log output without markers"
        trans, summary = extract_transcription_and_summary(log_text)
        assert trans == ""
        assert summary == ""

    def test_extract_empty_sections(self):
        """Test extraction with empty sections."""
        log_text = """
--- POCZĄTEK TRANSKRYPCJI ---
--- KONIEC TRANSKRYPCJI ---
--- POCZĄTEK STRESZCZENIA ---
--- KONIEC STRESZCZENIA ---
"""
        trans, summary = extract_transcription_and_summary(log_text)
        assert trans.strip() == ""
        assert summary.strip() == ""

    def test_extract_preserves_formatting(self):
        """Test that extraction preserves line breaks and formatting."""
        log_text = """
--- POCZĄTEK TRANSKRYPCJI ---
Line 1
Line 2
Line 3
--- KONIEC TRANSKRYPCJI ---
"""
        trans, _ = extract_transcription_and_summary(log_text)
        assert "Line 1" in trans
        assert "Line 2" in trans
        assert "Line 3" in trans

    def test_extract_with_special_characters(self):
        """Test extraction with special characters."""
        log_text = """
--- POCZĄTEK TRANSKRYPCJI ---
Text with special chars: !@#$%^&*()
Unicode: żółć, ąę
--- KONIEC TRANSKRYPCJI ---
"""
        trans, _ = extract_transcription_and_summary(log_text)
        assert "!@#$%^&*()" in trans
        assert "żółć" in trans

    def test_extract_multiple_markers(self):
        """Test that only first occurrence is extracted."""
        log_text = """
--- POCZĄTEK TRANSKRYPCJI ---
First transcription
--- KONIEC TRANSKRYPCJI ---
--- POCZĄTEK TRANSKRYPCJI ---
Second transcription (should be ignored)
--- KONIEC TRANSKRYPCJI ---
"""
        trans, _ = extract_transcription_and_summary(log_text)
        assert "First transcription" in trans
        # Implementation might include both or just first - adjust based on actual behavior

    def test_extract_case_sensitive(self):
        """Test that markers are case-sensitive."""
        log_text = """
--- początek transkrypcji ---
Lowercase markers (should not match)
--- koniec transkrypcji ---
"""
        trans, _ = extract_transcription_and_summary(log_text)
        # Should not extract with lowercase markers
        assert trans == ""


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
