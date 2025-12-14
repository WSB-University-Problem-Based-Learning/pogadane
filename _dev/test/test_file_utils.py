"""
Unit tests for file_utils module.
Tests file operations: unique filename generation, file deletion,
directory creation, and file finding.
"""
import pytest
from pathlib import Path
import tempfile
import shutil
from pogadane.file_utils import (
    get_unique_filename,
    get_input_name_stem,
    safe_delete_file,
    safe_create_directory,
    cleanup_temp_directory,
    find_output_file,
)


class TestGetUniqueFilename:
    """Test suite for get_unique_filename function."""

    def test_youtube_url_short_form(self):
        """Test YouTube short URL format."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        filename = get_unique_filename(url)
        assert "dQw4w9WgXcQ" in filename
        assert filename.endswith(".mp3")

    def test_youtube_url_long_form(self):
        """Test YouTube standard URL format."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        filename = get_unique_filename(url)
        assert "dQw4w9WgXcQ" in filename
        assert filename.endswith(".mp3")

    def test_youtube_url_with_params(self):
        """Test YouTube URL with additional parameters."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s"
        filename = get_unique_filename(url)
        assert "dQw4w9WgXcQ" in filename
        assert filename.endswith(".mp3")

    def test_file_path(self):
        """Test with file path."""
        path = "C:\\Users\\test\\meeting.mp3"
        filename = get_unique_filename(path)
        assert "meeting" in filename
        assert filename.endswith(".mp3")

    def test_file_path_without_extension(self):
        """Test file path without extension."""
        path = "/home/user/audio_file"
        filename = get_unique_filename(path)
        assert "audio_file" in filename

    def test_timestamp_added(self):
        """Test that timestamp is added to filename."""
        url = "https://youtu.be/test123"
        filename1 = get_unique_filename(url)
        import time
        time.sleep(0.01)  # Small delay
        filename2 = get_unique_filename(url)
        # Filenames should be different due to timestamp
        assert filename1 != filename2


class TestGetInputNameStem:
    """Test suite for get_input_name_stem function."""

    def test_simple_filename(self):
        """Test simple filename extraction."""
        stem = get_input_name_stem("meeting.mp3")
        assert stem == "meeting"

    def test_path_with_extension(self):
        """Test full path with extension."""
        stem = get_input_name_stem("/path/to/audio_file.wav")
        assert stem == "audio_file"

    def test_windows_path(self):
        """Test Windows path."""
        stem = get_input_name_stem("C:\\Users\\test\\recording.m4a")
        assert stem == "recording"

    def test_no_extension(self):
        """Test file without extension."""
        stem = get_input_name_stem("audiofile")
        assert stem == "audiofile"

    def test_multiple_dots(self):
        """Test filename with multiple dots."""
        stem = get_input_name_stem("my.audio.file.mp3")
        assert stem == "my.audio.file"

    def test_youtube_url(self):
        """Test YouTube URL."""
        stem = get_input_name_stem("https://www.youtube.com/watch?v=abc123")
        assert "abc123" in stem or "watch" in stem


class TestSafeDeleteFile:
    """Test suite for safe_delete_file function."""

    def test_delete_existing_file(self):
        """Test deleting an existing file."""
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        # Delete it
        result = safe_delete_file(tmp_path, "test file")
        assert result is True
        assert not Path(tmp_path).exists()

    def test_delete_nonexistent_file(self):
        """Test deleting a file that doesn't exist."""
        result = safe_delete_file("/nonexistent/file.txt", "test file")
        # Should return False or handle gracefully
        assert result is False or result is None

    def test_delete_with_path_object(self):
        """Test deleting with Path object."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        result = safe_delete_file(tmp_path, "test file")
        assert result is True
        assert not tmp_path.exists()


class TestSafeCreateDirectory:
    """Test suite for safe_create_directory function."""

    def test_create_new_directory(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / "test_subdir"
            result = safe_create_directory(new_dir, "test directory")
            assert result is True
            assert new_dir.exists()
            assert new_dir.is_dir()

    def test_create_existing_directory(self):
        """Test creating a directory that already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = safe_create_directory(tmpdir, "existing directory")
            assert result is True  # Should succeed (already exists)
            assert Path(tmpdir).is_dir()

    def test_create_nested_directories(self):
        """Test creating nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested = Path(tmpdir) / "level1" / "level2" / "level3"
            result = safe_create_directory(nested, "nested directory")
            assert result is True
            assert nested.exists()


class TestCleanupTempDirectory:
    """Test suite for cleanup_temp_directory function."""

    def test_cleanup_empty_directory(self):
        """Test cleanup of empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "temp_dir"
            temp_path.mkdir()
            
            cleanup_temp_directory(temp_path)
            # Should remove empty directory
            # Behavior may vary, check implementation

    def test_cleanup_with_files(self):
        """Test cleanup doesn't remove directory with files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "temp_dir"
            temp_path.mkdir()
            (temp_path / "file.txt").write_text("content")
            
            cleanup_temp_directory(temp_path)
            # Should not remove directory with files
            assert temp_path.exists()

    def test_cleanup_nonexistent_directory(self):
        """Test cleanup of nonexistent directory."""
        # Should not raise error
        cleanup_temp_directory("/nonexistent/directory")


class TestFindOutputFile:
    """Test suite for find_output_file function."""

    def test_find_existing_file(self):
        """Test finding an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "output"
            test_file = Path(tmpdir) / "output.txt"
            test_file.write_text("content")
            
            found = find_output_file(base_path, [".txt", ".log"])
            assert found is not None
            assert found.name == "output.txt"

    def test_find_with_multiple_extensions(self):
        """Test finding file with multiple possible extensions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "output"
            test_file = Path(tmpdir) / "output.srt"
            test_file.write_text("content")
            
            found = find_output_file(base_path, [".txt", ".srt", ".vtt"])
            assert found is not None
            assert found.suffix == ".srt"

    def test_find_nonexistent_file(self):
        """Test when no file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "nonexistent"
            
            found = find_output_file(base_path, [".txt", ".log"])
            assert found is None

    def test_find_first_match(self):
        """Test that first matching extension is returned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "output"
            (Path(tmpdir) / "output.txt").write_text("txt content")
            (Path(tmpdir) / "output.log").write_text("log content")
            
            found = find_output_file(base_path, [".txt", ".log"])
            # Should return .txt (first in list)
            assert found.suffix == ".txt"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
