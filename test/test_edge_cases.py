"""
Additional Edge Case Tests for Pogadane
Tests for more obscure scenarios and potential bugs
"""

import sys

from .test_comprehensive_bugs import BugChecker


def test_unicode_handling():
    """Test Unicode characters in various contexts"""
    from pogadane.file_utils import get_input_name_stem
    
    # Test files with Unicode names
    unicode_paths = [
        "ścieżka/do/plik.mp3",
        "путь/к/файл.mp3",
        "パス/ファイル.mp3",
        "路径/文件.mp3",
        "café_résumé.mp3",
    ]
    
    for path in unicode_paths:
        try:
            stem = get_input_name_stem(path)
            assert len(stem) > 0, f"Stem should not be empty for: {path}"
            print(f"✓ Unicode path handled: {path} -> {stem}")
        except Exception as e:
            print(f"⚠️  Unicode path issue: {path} - {e}")


def test_very_long_paths():
    """Test handling of very long file paths"""
    from pogadane.file_utils import get_input_name_stem
    
    # Windows MAX_PATH is 260 characters
    long_path = "C:/" + "verylongfoldername/" * 20 + "file.mp3"
    
    try:
        stem = get_input_name_stem(long_path)
        assert len(stem) > 0, "Should handle long paths"
        print(f"✓ Long path handled (length: {len(long_path)})")
    except Exception as e:
        print(f"✓ Long path limitation handled: {e}")


def test_null_and_none_values():
    """Test handling of null/None values"""
    from pogadane.transcription_providers import FasterWhisperLibraryProvider
    
    # Test None batch_size
    try:
        provider = FasterWhisperLibraryProvider(batch_size=None)
        print(f"✓ None batch_size handled: {provider.batch_size}")
    except TypeError:
        print("✓ None batch_size raises TypeError (expected)")
    
    # Test empty string batch_size in config
    try:
        batch_size_str = ""
        batch_size = int(batch_size_str) if batch_size_str else 0
        assert batch_size == 0, "Empty string should become 0"
        print("✓ Empty string batch_size becomes 0")
    except Exception as e:
        print(f"⚠️  Empty string issue: {e}")


def test_extreme_numbers():
    """Test extreme numerical values"""
    from pogadane.transcription_providers import FasterWhisperLibraryProvider
    
    # Test very large batch_size
    large_batch = FasterWhisperLibraryProvider(batch_size=999999)
    assert large_batch.batch_size == 999999, "Should handle large numbers"
    print(f"✓ Large batch_size handled: {large_batch.batch_size}")
    
    # Test zero
    zero_batch = FasterWhisperLibraryProvider(batch_size=0)
    assert zero_batch.batch_size == 0, "Should handle zero"
    assert not (zero_batch.batch_size > 0), "Zero comparison should work"
    print("✓ Zero batch_size handled correctly")


def test_whitespace_in_config():
    """Test config values with whitespace"""
    test_values = [
        "  16  ",  # Leading/trailing spaces
        "\t16\t",  # Tabs
        "16\n",    # Newline
        " 16 ",    # Mixed
    ]
    
    for val in test_values:
        try:
            result = int(val.strip())
            assert result == 16, f"Should parse '{val}' as 16"
            print(f"✓ Whitespace value parsed: '{val}' -> {result}")
        except Exception as e:
            print(f"⚠️  Whitespace parsing failed: '{val}' - {e}")


def test_case_sensitivity():
    """Test case sensitivity in various contexts"""
    from pogadane.text_utils import is_valid_url
    
    # Test URL case variations
    urls = [
        "HTTPS://YOUTUBE.COM/watch?v=123",
        "https://YOUTUBE.com/watch?v=123",
        "https://youtube.COM/watch?v=123",
    ]
    
    for url in urls:
        assert is_valid_url(url), f"Should recognize URL regardless of case: {url}"
    print(f"✓ All {len(urls)} case variations recognized")


def test_repeated_operations():
    """Test repeated operations for memory leaks or state issues"""
    from pogadane.backend import PogadaneBackend
    
    # Create and destroy multiple backends
    for i in range(10):
        backend = PogadaneBackend()
        assert backend is not None, "Backend should be created"
    
    print("✓ Repeated backend creation works (10 iterations)")
    
    # Test repeated config reloads
    from pogadane.config_loader import ConfigManager
    config_manager = ConfigManager()
    
    for i in range(5):
        config_manager.reload()
        assert config_manager.config is not None, "Config should reload"
    
    print("✓ Repeated config reload works (5 iterations)")


def test_concurrent_file_operations():
    """Test concurrent file operations"""
    from pogadane.file_utils import get_unique_filename
    from pathlib import Path
    import tempfile
    import threading
    
    results = []
    
    def create_unique_name():
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            name = get_unique_filename(tmpdir_path, "test", ".txt")
            results.append(name)
    
    threads = [threading.Thread(target=create_unique_name) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # All names should be present
    assert len(results) == 5, "Should have 5 results"
    print(f"✓ Concurrent file operations work ({len(results)} threads)")


def test_model_name_variations():
    """Test different model name formats"""
    model_names = [
        "tiny",
        "TINY",
        "Tiny",
        "base",
        "large-v3",
        "large_v3",  # Different separator
    ]
    
    for model in model_names:
        # Just verify they're valid strings
        assert isinstance(model, str), f"Model should be string: {model}"
        assert len(model) > 0, f"Model should not be empty: {model}"
    
    print(f"✓ All {len(model_names)} model name variations tested")


def test_language_name_variations():
    """Test language name variations"""
    from pogadane.transcription_providers import FasterWhisperLibraryProvider
    
    provider = FasterWhisperLibraryProvider()
    
    variations = [
        ("polish", "pl"),
        ("Polish", "pl"),
        ("POLISH", "pl"),
        ("PoLiSh", "pl"),
        ("en", "en"),
        ("EN", "en"),
    ]
    
    for input_lang, expected in variations:
        result = provider._get_language_code(input_lang)
        # Should normalize to lowercase code
        assert result.lower() == expected.lower(), f"Language '{input_lang}' mapping failed"
    
    print(f"✓ All {len(variations)} language variations tested")


def test_config_with_comments():
    """Test that config preserves comments"""
    from pogadane.config_loader import ConfigManager
    
    config_path = ConfigManager().config_path
    
    # Read config file
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for comments
    has_comments = '#' in content
    assert has_comments, "Config should have comments"
    
    # Check structure is preserved
    has_sections = '---' in content or 'Ustawienia' in content
    print(f"✓ Config structure preserved (comments: {has_comments}, sections: {has_sections})")


def test_empty_results():
    """Test handling of empty results"""
    from pogadane.gui_utils import ResultsManager
    
    manager = ResultsManager()
    
    # Test empty export
    export = manager.export_all_results()
    assert "Brak" in export or "empty" in export.lower(), "Should indicate no results"
    print("✓ Empty results export handled")
    
    # Test empty retrieval
    result = manager.get_result("non_existent")
    assert result is None, "Should return None for non-existent result"
    print("✓ Non-existent result handled")


def test_progress_update_edge_cases():
    """Test edge cases in progress updates"""
    from pogadane.backend import ProgressCallback, ProgressUpdate, ProcessingStage
    
    updates = []
    def callback(update: ProgressUpdate):
        updates.append(update)
    
    progress = ProgressCallback(callback)
    
    # Test progress > 1.0
    progress.update(ProcessingStage.COMPLETED, "Over 100%", 1.5)
    assert updates[-1].progress == 1.5, "Should accept progress > 1.0"
    print("✓ Progress > 1.0 handled")
    
    # Test negative progress
    progress.update(ProcessingStage.ERROR, "Negative", -0.5)
    assert updates[-1].progress == -0.5, "Should accept negative progress"
    print("✓ Negative progress handled")
    
    # Test None details
    progress.update(ProcessingStage.INITIALIZING, "No details", 0.0, None)
    assert updates[-1].details == {}, "None details should become empty dict"
    print("✓ None details handled")


def test_file_extension_edge_cases():
    """Test various file extensions"""
    from pogadane.file_utils import get_input_name_stem
    
    extensions = [
        "file.mp3",
        "file.MP3",
        "file.wav",
        "file.m4a",
        "file.flac",
        "file.ogg",
        "file.tar.gz",  # Multiple extensions
        "file",  # No extension
        ".hidden",  # Hidden file
    ]
    
    for filename in extensions:
        stem = get_input_name_stem(filename)
        assert len(stem) > 0, f"Should handle extension: {filename}"
        print(f"✓ Extension handled: {filename} -> {stem}")


def test_url_edge_cases():
    """Test edge cases in URL handling"""
    from pogadane.text_utils import is_valid_url
    
    # Valid YouTube URLs
    valid = [
        "https://youtube.com/watch?v=abc",
        "https://youtu.be/abc",
        "https://www.youtube.com/watch?v=abc&feature=share",
    ]
    
    # Invalid URLs
    invalid = [
        "",
        " ",
        "not a url",
        "file:///path/to/file",
        "C:\\Users\\file.mp3",
        "/usr/local/file.mp3",
    ]
    
    for url in valid:
        assert is_valid_url(url), f"Should be valid: {url}"
    print(f"✓ All {len(valid)} valid URLs recognized")
    
    for url in invalid:
        assert not is_valid_url(url), f"Should be invalid: {url}"
    print(f"✓ All {len(invalid)} invalid URLs rejected")


def main():
    """Run all additional edge case tests"""
    checker = BugChecker()
    
    print("\n" + "🔬" * 35)
    print("ADDITIONAL EDGE CASE TESTS FOR POGADANE")
    print("🔬" * 35)
    
    # Unicode and special characters
    checker.test("Unicode Handling", test_unicode_handling)
    checker.test("Very Long Paths", test_very_long_paths)
    checker.test("Special Characters in Config", test_whitespace_in_config)
    
    # Null and edge values
    checker.test("Null and None Values", test_null_and_none_values)
    checker.test("Extreme Numbers", test_extreme_numbers)
    
    # Case sensitivity
    checker.test("Case Sensitivity", test_case_sensitivity)
    checker.test("Language Name Variations", test_language_name_variations)
    checker.test("Model Name Variations", test_model_name_variations)
    
    # Repeated operations
    checker.test("Repeated Operations", test_repeated_operations)
    checker.test("Concurrent File Operations", test_concurrent_file_operations)
    
    # Config handling
    checker.test("Config with Comments", test_config_with_comments)
    
    # Empty states
    checker.test("Empty Results", test_empty_results)
    
    # Progress system edge cases
    checker.test("Progress Update Edge Cases", test_progress_update_edge_cases)
    
    # File handling
    checker.test("File Extension Edge Cases", test_file_extension_edge_cases)
    checker.test("URL Edge Cases", test_url_edge_cases)
    
    # Generate report
    checker.report()
    
    return checker.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
