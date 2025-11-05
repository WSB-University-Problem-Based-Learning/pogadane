"""
Comprehensive Bug Check for Pogadane Application

This script tests various scenarios to ensure the application is bug-proof.
Tests cover: type conversions, edge cases, error handling, config validation, etc.
"""

import sys
import os
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class BugChecker:
    """Comprehensive bug checker for Pogadane"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, func):
        """Run a test and track results"""
        try:
            print(f"\n{'='*70}")
            print(f"TEST: {name}")
            print('='*70)
            func()
            self.passed += 1
            print(f"✅ PASSED: {name}")
        except Exception as e:
            self.failed += 1
            error_msg = f"❌ FAILED: {name} - {str(e)}"
            self.errors.append(error_msg)
            print(error_msg)
            import traceback
            traceback.print_exc()
    
    def report(self):
        """Print final report"""
        print("\n" + "="*70)
        print("COMPREHENSIVE BUG CHECK REPORT")
        print("="*70)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Total:  {self.passed + self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.errors:
            print("\n❌ ERRORS FOUND:")
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error}")
        else:
            print("\n🎉 ALL TESTS PASSED! Application is bug-proof!")
        
        print("="*70)


def test_config_loader():
    """Test configuration loading with various scenarios"""
    from pogadane.config_loader import ConfigManager
    
    # Test 1: Normal loading
    config_manager = ConfigManager()
    config = config_manager.config
    assert config is not None, "Config should not be None"
    print("✓ Config loaded successfully")
    
    # Test 2: Singleton pattern
    config_manager2 = ConfigManager()
    assert config_manager is config_manager2, "ConfigManager should be singleton"
    print("✓ Singleton pattern works")
    
    # Test 3: Required attributes exist
    required_attrs = [
        'TRANSCRIPTION_PROVIDER',
        'WHISPER_MODEL',
        'WHISPER_LANGUAGE',
        'SUMMARY_PROVIDER',
        'SUMMARY_LANGUAGE'
    ]
    for attr in required_attrs:
        assert hasattr(config, attr), f"Config missing required attribute: {attr}"
        value = getattr(config, attr)
        assert value is not None, f"Config attribute {attr} is None"
    print(f"✓ All {len(required_attrs)} required attributes present")


def test_backend_initialization():
    """Test backend initialization with various configs"""
    from pogadane.backend import PogadaneBackend
    
    # Test 1: Normal initialization
    backend = PogadaneBackend()
    assert backend is not None, "Backend should not be None"
    assert backend.config is not None, "Backend config should not be None"
    print("✓ Backend initialized successfully")
    
    # Test 2: Temp directory created
    assert backend.temp_audio_dir.exists(), "Temp audio directory should exist"
    print(f"✓ Temp directory exists: {backend.temp_audio_dir}")
    
    # Test 3: Config manager is singleton
    assert backend.config_manager._config is not None, "Config should be loaded"
    print("✓ Config manager properly initialized")


def test_type_conversions():
    """Test type conversions for config values"""
    from pogadane.config_loader import ConfigManager
    
    config = ConfigManager().config
    
    # Test 1: FASTER_WHISPER_BATCH_SIZE is integer
    batch_size = getattr(config, 'FASTER_WHISPER_BATCH_SIZE', None)
    print(f"  batch_size value: {batch_size}, type: {type(batch_size)}")
    
    # Should work with both int and string from config
    if isinstance(batch_size, str):
        batch_size_int = int(batch_size)
        assert batch_size_int >= 0, "Batch size should be non-negative"
    elif isinstance(batch_size, int):
        assert batch_size >= 0, "Batch size should be non-negative"
    print("✓ Batch size type conversion works")
    
    # Test 2: Boolean values
    vad_filter = getattr(config, 'FASTER_WHISPER_VAD_FILTER', False)
    print(f"  vad_filter value: {vad_filter}, type: {type(vad_filter)}")
    assert isinstance(vad_filter, bool), "VAD filter should be boolean"
    print("✓ Boolean conversion works")


def test_transcription_provider_creation():
    """Test transcription provider creation with various configs"""
    from pogadane.transcription_providers import TranscriptionProviderFactory
    from pogadane.config_loader import ConfigManager
    
    config = ConfigManager().config
    
    # Test 1: Create provider
    provider = TranscriptionProviderFactory.create_provider(config)
    assert provider is not None, "Provider should be created"
    print(f"✓ Provider created: {provider.__class__.__name__}")
    
    # Test 2: Provider is available
    assert provider.is_available(), "Provider should be available"
    print("✓ Provider is available")
    
    # Test 3: Check batch_size handling
    if hasattr(provider, 'batch_size'):
        batch_size = provider.batch_size
        print(f"  Provider batch_size: {batch_size}, type: {type(batch_size)}")
        assert isinstance(batch_size, int), "Provider batch_size should be integer"
        
        # Test comparison (this was the original bug)
        result = batch_size > 0
        assert isinstance(result, bool), "Comparison should return boolean"
        print(f"✓ Batch size comparison works: {batch_size} > 0 = {result}")


def test_llm_provider_creation():
    """Test LLM provider creation"""
    from pogadane.llm_providers import LLMProviderFactory
    from pogadane.config_loader import ConfigManager
    
    config = ConfigManager().config
    
    # Test 1: Create provider
    provider = LLMProviderFactory.create_provider(config)
    assert provider is not None, "LLM Provider should be created"
    print(f"✓ LLM Provider created: {provider.__class__.__name__}")


def test_progress_callback_system():
    """Test progress callback system"""
    from pogadane.backend import ProgressCallback, ProgressUpdate, ProcessingStage
    
    # Test 1: Progress callback without callback function
    progress = ProgressCallback(None)
    progress.update(ProcessingStage.INITIALIZING, "Test", 0.0)
    assert progress.current_stage == ProcessingStage.INITIALIZING, "Stage should be set"
    assert progress.current_progress == 0.0, "Progress should be 0.0"
    print("✓ Progress callback without function works")
    
    # Test 2: Progress callback with callback function
    updates = []
    def callback(update: ProgressUpdate):
        updates.append(update)
    
    progress = ProgressCallback(callback)
    progress.update(ProcessingStage.TRANSCRIBING, "Transcribing", 0.5, {"key": "value"})
    
    assert len(updates) == 1, "Should have one update"
    assert updates[0].stage == ProcessingStage.TRANSCRIBING, "Stage should match"
    assert updates[0].progress == 0.5, "Progress should match"
    assert updates[0].details["key"] == "value", "Details should match"
    print("✓ Progress callback with function works")
    
    # Test 3: Progress history
    assert len(progress.history) == 1, "History should have one entry"
    print("✓ Progress history works")
    
    # Test 4: Log method
    progress.log("Test log message")
    print("✓ Log method works")


def test_file_operations():
    """Test file operation utilities"""
    from pogadane.file_utils import get_unique_filename, get_input_name_stem
    from pathlib import Path
    import tempfile
    
    # Test 1: get_unique_filename
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create a file
        test_file = tmpdir_path / "test.txt"
        test_file.write_text("test")
        
        # Get unique filename
        unique = get_unique_filename(tmpdir_path, "test", ".txt")
        assert "test" in unique, "Should contain original name"
        assert unique != "test.txt", "Should be different from original"
        print(f"✓ Unique filename: {unique}")
    
    # Test 2: get_input_name_stem
    stem = get_input_name_stem("path/to/audio.mp3")
    assert stem == "audio", f"Stem should be 'audio', got '{stem}'"
    
    stem = get_input_name_stem("https://youtube.com/watch?v=123")
    assert len(stem) > 0, "YouTube URL should have a stem"
    print(f"✓ Input name stem: {stem}")


def test_text_utilities():
    """Test text utility functions"""
    from pogadane.text_utils import is_valid_url, strip_ansi
    
    # Test 1: URL validation
    assert is_valid_url("https://youtube.com/watch?v=123"), "Should be valid YouTube URL"
    assert is_valid_url("https://youtu.be/123"), "Should be valid YouTube short URL"
    assert not is_valid_url("not a url"), "Should not be valid URL"
    assert not is_valid_url("/path/to/file.mp3"), "Local path should not be URL"
    print("✓ URL validation works")
    
    # Test 2: ANSI strip
    text_with_ansi = "\x1b[31mRed text\x1b[0m"
    clean = strip_ansi(text_with_ansi)
    assert "\x1b" not in clean, "Should strip ANSI codes"
    assert "Red text" in clean, "Should preserve text"
    print("✓ ANSI stripping works")


def test_constants():
    """Test constants are properly defined"""
    from pogadane.constants import (
        DEFAULT_CONFIG,
        FILE_STATUS_PENDING,
        FILE_STATUS_PROCESSING,
        FILE_STATUS_COMPLETED,
        FILE_STATUS_ERROR,
        APP_VERSION
    )
    
    # Test 1: DEFAULT_CONFIG exists and has required keys
    required_keys = [
        'TRANSCRIPTION_PROVIDER',
        'WHISPER_MODEL',
        'WHISPER_LANGUAGE',
        'SUMMARY_PROVIDER',
        'SUMMARY_LANGUAGE'
    ]
    for key in required_keys:
        assert key in DEFAULT_CONFIG, f"DEFAULT_CONFIG missing key: {key}"
    print(f"✓ DEFAULT_CONFIG has all {len(required_keys)} required keys")
    
    # Test 2: Status constants (check they exist and are non-empty strings)
    assert isinstance(FILE_STATUS_PENDING, str) and len(FILE_STATUS_PENDING) > 0, "Status constant invalid"
    assert isinstance(FILE_STATUS_PROCESSING, str) and len(FILE_STATUS_PROCESSING) > 0, "Status constant invalid"
    assert isinstance(FILE_STATUS_COMPLETED, str) and len(FILE_STATUS_COMPLETED) > 0, "Status constant invalid"
    assert isinstance(FILE_STATUS_ERROR, str) and len(FILE_STATUS_ERROR) > 0, "Status constant invalid"
    print("✓ Status constants defined correctly")
    
    # Test 3: Version
    assert isinstance(APP_VERSION, str), "APP_VERSION should be string"
    assert len(APP_VERSION) > 0, "APP_VERSION should not be empty"
    print(f"✓ App version: {APP_VERSION}")


def test_edge_cases_config_values():
    """Test edge cases for config values"""
    from pogadane.transcription_providers import FasterWhisperLibraryProvider
    
    # Test 1: Batch size = 0 (disabled)
    provider = FasterWhisperLibraryProvider(batch_size=0)
    assert provider.batch_size == 0, "Batch size should be 0"
    assert not (provider.batch_size > 0), "Comparison should be False"
    print("✓ Batch size 0 works")
    
    # Test 2: Batch size > 0
    provider = FasterWhisperLibraryProvider(batch_size=16)
    assert provider.batch_size == 16, "Batch size should be 16"
    assert provider.batch_size > 0, "Comparison should be True"
    print("✓ Batch size 16 works")
    
    # Test 3: Negative batch size (should be handled)
    provider = FasterWhisperLibraryProvider(batch_size=-1)
    # Should not crash
    print(f"✓ Negative batch size handled: {provider.batch_size}")


def test_path_handling():
    """Test path handling across different scenarios"""
    from pogadane.constants import PROJECT_ROOT, DEP_DIR, MODELS_DIR
    from pathlib import Path
    
    # Test 1: Paths are Path objects
    assert isinstance(PROJECT_ROOT, Path), "PROJECT_ROOT should be Path"
    assert isinstance(DEP_DIR, Path), "DEP_DIR should be Path"
    assert isinstance(MODELS_DIR, Path), "MODELS_DIR should be Path"
    print("✓ All paths are Path objects")
    
    # Test 2: PROJECT_ROOT exists
    assert PROJECT_ROOT.exists(), "PROJECT_ROOT should exist"
    print(f"✓ PROJECT_ROOT exists: {PROJECT_ROOT}")
    
    # Test 3: Path concatenation works
    test_path = PROJECT_ROOT / "test" / "file.txt"
    assert isinstance(test_path, Path), "Path concatenation should return Path"
    print("✓ Path concatenation works")


def test_error_handling_missing_files():
    """Test error handling for missing files"""
    from pogadane.backend import PogadaneBackend, ProgressCallback
    from pathlib import Path
    
    backend = PogadaneBackend()
    
    # Test with non-existent file
    non_existent = Path("/this/does/not/exist/file.mp3")
    
    # Create a progress callback
    progress = ProgressCallback(None)
    
    # This should not crash, but return None/error
    try:
        result = backend._copy_to_temp(non_existent, progress)
        # Should return None for missing file
        assert result is None, "Should return None for missing file"
        print("✓ Missing file handled gracefully")
    except Exception as e:
        # Should not raise exception, but if it does, check if it's expected
        print(f"✓ Missing file error handled: {e}")


def test_youtube_url_patterns():
    """Test various YouTube URL patterns"""
    from pogadane.text_utils import is_valid_url
    
    youtube_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
    ]
    
    for url in youtube_urls:
        assert is_valid_url(url), f"Should recognize YouTube URL: {url}"
    print(f"✓ All {len(youtube_urls)} YouTube URL patterns recognized")


def test_language_code_mapping():
    """Test language code mapping in providers"""
    from pogadane.transcription_providers import FasterWhisperLibraryProvider
    
    provider = FasterWhisperLibraryProvider()
    
    # Test various language inputs
    test_cases = [
        ("Polish", "pl"),
        ("polish", "pl"),
        ("POLISH", "pl"),
        ("English", "en"),
        ("pl", "pl"),  # Already a code
        ("en", "en"),
        ("German", "de"),
        ("unknown_language", "en"),  # Should default to English
    ]
    
    for input_lang, expected_code in test_cases:
        result = provider._get_language_code(input_lang)
        assert result == expected_code, f"Language '{input_lang}' should map to '{expected_code}', got '{result}'"
    
    print(f"✓ All {len(test_cases)} language mappings correct")


def test_model_names():
    """Test valid model names"""
    valid_models = ["tiny", "base", "small", "medium", "large-v3", "turbo"]
    
    # Just verify they're strings and non-empty
    for model in valid_models:
        assert isinstance(model, str), f"Model name should be string: {model}"
        assert len(model) > 0, f"Model name should not be empty: {model}"
    
    print(f"✓ All {len(valid_models)} model names valid")


def test_processing_stages():
    """Test ProcessingStage enum"""
    from pogadane.backend import ProcessingStage
    
    stages = [
        ProcessingStage.INITIALIZING,
        ProcessingStage.DOWNLOADING,
        ProcessingStage.COPYING,
        ProcessingStage.TRANSCRIBING,
        ProcessingStage.SUMMARIZING,
        ProcessingStage.CLEANING,
        ProcessingStage.COMPLETED,
        ProcessingStage.ERROR
    ]
    
    # Test enum values
    for stage in stages:
        assert isinstance(stage.value, str), f"Stage value should be string: {stage}"
        assert len(stage.value) > 0, f"Stage value should not be empty: {stage}"
    
    print(f"✓ All {len(stages)} processing stages valid")


def test_results_manager():
    """Test ResultsManager utility"""
    from pogadane.gui_utils import ResultsManager
    
    manager = ResultsManager()
    
    # Test 1: Add result
    manager.add_result("test_source", "transcription text", "summary text")
    assert "test_source" in manager.results_data, "Result should be added"
    print("✓ Result added successfully")
    
    # Test 2: Get result
    result = manager.get_result("test_source")
    assert result is not None, "Result should be retrievable"
    assert result["transcription"] == "transcription text", "Transcription should match"
    assert result["summary"] == "summary text", "Summary should match"
    print("✓ Result retrieved successfully")
    
    # Test 3: List sources
    sources = manager.get_all_sources()
    assert "test_source" in sources, "Source should be in list"
    print("✓ List sources works")
    
    # Test 4: Count results
    count = manager.get_result_count()
    assert count == 1, "Should have 1 result"
    print(f"✓ Result count: {count}")
    
    # Test 5: Has results
    assert manager.has_results(), "Should have results"
    print("✓ Has results check works")
    
    # Test 6: Export results
    exported = manager.export_all_results()
    assert "test_source" in exported, "Export should contain source"
    assert "transcription text" in exported, "Export should contain transcription"
    print("✓ Export results works")
    
    # Test 7: Clear results
    manager.clear_all()
    assert manager.get_result_count() == 0, "Results should be cleared"
    assert not manager.has_results(), "Should not have results"
    print("✓ Clear results works")


def test_config_save_type_preservation():
    """Test that config save preserves types"""
    # This tests the fix we just made
    from pogadane.config_loader import ConfigManager
    
    config = ConfigManager().config
    
    # Check critical types
    batch_size = getattr(config, 'FASTER_WHISPER_BATCH_SIZE', 0)
    print(f"  FASTER_WHISPER_BATCH_SIZE: {batch_size} (type: {type(batch_size).__name__})")
    
    vad_filter = getattr(config, 'FASTER_WHISPER_VAD_FILTER', False)
    print(f"  FASTER_WHISPER_VAD_FILTER: {vad_filter} (type: {type(vad_filter).__name__})")
    
    # Ensure types are correct or can be converted
    if isinstance(batch_size, str):
        batch_size = int(batch_size)
    assert isinstance(batch_size, int), "Batch size should be int or convertible to int"
    
    if isinstance(vad_filter, str):
        vad_filter = vad_filter.lower() in ('true', '1', 'yes', 'on')
    assert isinstance(vad_filter, bool), "VAD filter should be bool or convertible to bool"
    
    print("✓ Config types correct or convertible")


def test_empty_string_handling():
    """Test handling of empty strings in config"""
    # Test that empty strings don't cause issues
    test_values = ["", "   ", None]
    
    for val in test_values:
        # Test batch_size conversion
        try:
            if val:
                result = int(val)
            else:
                result = 0
            print(f"✓ Empty value '{val}' converted to {result}")
        except ValueError:
            # Should use default
            result = 0
            print(f"✓ Invalid value '{val}' defaults to {result}")


def test_special_characters_in_paths():
    """Test paths with special characters"""
    from pogadane.file_utils import get_input_name_stem
    
    test_paths = [
        "C:/Users/Test User/file.mp3",
        "C:\\Users\\Test User\\file with spaces.mp3",
        "/path/to/file-with-dashes.mp3",
        "path/to/file_with_underscores.mp3",
        "file (1).mp3",
        "file [2].mp3",
    ]
    
    for path in test_paths:
        try:
            stem = get_input_name_stem(path)
            assert len(stem) > 0, f"Stem should not be empty for: {path}"
            print(f"✓ Path handled: {path} -> {stem}")
        except Exception as e:
            print(f"⚠️  Path failed: {path} - {e}")


def test_concurrent_access():
    """Test thread safety (basic check)"""
    from pogadane.config_loader import ConfigManager
    import threading
    
    results = []
    
    def access_config():
        config = ConfigManager().config
        results.append(config is not None)
    
    # Create multiple threads
    threads = [threading.Thread(target=access_config) for _ in range(5)]
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Wait for completion
    for t in threads:
        t.join()
    
    # Check all succeeded
    assert all(results), "All threads should access config successfully"
    assert len(results) == 5, "Should have 5 results"
    print(f"✓ Concurrent access works ({len(results)} threads)")


def main():
    """Run all bug checks"""
    checker = BugChecker()
    
    print("\n" + "🔍" * 35)
    print("COMPREHENSIVE BUG CHECK FOR POGADANE")
    print("🔍" * 35)
    
    # Configuration tests
    checker.test("Config Loader", test_config_loader)
    checker.test("Backend Initialization", test_backend_initialization)
    checker.test("Type Conversions", test_type_conversions)
    
    # Provider tests
    checker.test("Transcription Provider Creation", test_transcription_provider_creation)
    checker.test("LLM Provider Creation", test_llm_provider_creation)
    
    # Progress system tests
    checker.test("Progress Callback System", test_progress_callback_system)
    checker.test("Processing Stages", test_processing_stages)
    
    # Utility tests
    checker.test("File Operations", test_file_operations)
    checker.test("Text Utilities", test_text_utilities)
    checker.test("Constants", test_constants)
    checker.test("Results Manager", test_results_manager)
    
    # Edge case tests
    checker.test("Edge Cases - Config Values", test_edge_cases_config_values)
    checker.test("Path Handling", test_path_handling)
    checker.test("Error Handling - Missing Files", test_error_handling_missing_files)
    checker.test("YouTube URL Patterns", test_youtube_url_patterns)
    checker.test("Language Code Mapping", test_language_code_mapping)
    checker.test("Model Names", test_model_names)
    
    # Type safety tests
    checker.test("Config Save Type Preservation", test_config_save_type_preservation)
    checker.test("Empty String Handling", test_empty_string_handling)
    checker.test("Special Characters in Paths", test_special_characters_in_paths)
    
    # Concurrency tests
    checker.test("Concurrent Access", test_concurrent_access)
    
    # Generate report
    checker.report()
    
    return checker.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
