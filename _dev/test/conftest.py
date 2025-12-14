"""
Pytest configuration and shared fixtures for the Pogadane test suite.

This module provides common test fixtures and configuration for all test modules.
Fixtures defined here are automatically available to all test files.
"""

import sys
import pytest
import tempfile
from pathlib import Path

# Add _app/src to Python path so tests can import pogadane
_app_src = Path(__file__).parent.parent.parent / "_app" / "src"
if str(_app_src) not in sys.path:
    sys.path.insert(0, str(_app_src))


@pytest.fixture
def temp_dir():
    """
    Provide a temporary directory that is automatically cleaned up after the test.
    
    Yields:
        Path: Path to a temporary directory.
        
    Example:
        def test_file_creation(temp_dir):
            file_path = temp_dir / "test.txt"
            file_path.write_text("content")
            assert file_path.exists()
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_config_file(temp_dir):
    """
    Provide a temporary config.py file for testing configuration loading.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Yields:
        Path: Path to a temporary config.py file.
        
    Example:
        def test_config_loading(temp_config_file):
            # temp_config_file contains a valid config.py
            loader = ConfigLoader()
            config = loader.load_config(str(temp_config_file))
            assert config is not None
    """
    config_file = temp_dir / "config.py"
    config_content = """
# Test configuration file
WHISPER_MODEL = "base"
OLLAMA_MODEL = "test-model"
GEMINI_MODEL = "gemini-test"
LLM_PROVIDER = "ollama"
SUMMARY_LANGUAGE = "en"
PROMPT_TEMPLATE = "Test prompt"
"""
    config_file.write_text(config_content, encoding='utf-8')
    yield config_file


@pytest.fixture
def sample_text():
    """
    Provide sample text for testing text processing functions.
    
    Returns:
        str: Sample text with various formatting.
        
    Example:
        def test_text_processing(sample_text):
            result = process_text(sample_text)
            assert len(result) > 0
    """
    return """
    This is sample text for testing.
    
    It includes multiple lines.
    
    Some special characters: ąćęłńóśźż
    
    ANSI codes: \033[31mRed\033[0m
    """


@pytest.fixture
def sample_urls():
    """
    Provide sample URLs for testing URL validation.
    
    Returns:
        dict: Dictionary with 'valid' and 'invalid' URL lists.
        
    Example:
        def test_url_validation(sample_urls):
            for url in sample_urls['valid']:
                assert is_valid_url(url)
    """
    return {
        'valid': [
            'https://www.example.com',
            'http://example.com',
            'https://example.com/path?query=value',
            'https://subdomain.example.com:8080/path',
        ],
        'invalid': [
            'not-a-url',
            'ftp://example.com',
            'https://',
            'example.com',  # Missing protocol
            '',
            None,
        ]
    }


@pytest.fixture
def sample_transcription():
    """
    Provide a sample transcription with markers for testing extraction.
    
    Returns:
        str: Sample transcription with TRANSCRIPTION and SUMMARY markers.
        
    Example:
        def test_extraction(sample_transcription):
            trans, summary = extract_transcription_and_summary(sample_transcription)
            assert trans and summary
    """
    return """
=== TRANSCRIPTION START ===
This is the transcription content.
It has multiple lines.
=== TRANSCRIPTION END ===

=== SUMMARY START ===
This is the summary content.
Brief and concise.
=== SUMMARY END ===
"""


@pytest.fixture
def mock_config():
    """
    Provide a mock configuration dictionary for testing.
    
    Returns:
        dict: Configuration dictionary with all required keys.
        
    Example:
        def test_with_config(mock_config):
            assert mock_config['WHISPER_MODEL'] == 'base'
    """
    return {
        'WHISPER_MODEL': 'base',
        'OLLAMA_MODEL': 'llama3.2:3b',
        'GEMINI_MODEL': 'gemini-1.5-flash',
        'LLM_PROVIDER': 'ollama',
        'SUMMARY_LANGUAGE': 'en',
        'PROMPT_TEMPLATE': 'Summarize this text: {text}',
        'GEMINI_API_KEY': None,
    }


@pytest.fixture(autouse=True)
def reset_singletons():
    """
    Automatically reset singleton instances before each test.
    
    This fixture ensures that singleton classes (like ConfigManager) are
    reset between tests to avoid state pollution.
    
    This fixture runs automatically before each test (autouse=True).
    """
    # Import here to avoid circular dependencies
    from pogadane.config_loader import ConfigManager
    
    # Reset ConfigManager singleton
    ConfigManager._instance = None
    ConfigManager._initialized = False
    
    yield
    
    # Clean up after test
    ConfigManager._instance = None
    ConfigManager._initialized = False


# Pytest configuration hooks

def pytest_configure(config):
    """
    Pytest configuration hook - runs once at the start of the test session.
    
    Registers custom markers for test categorization.
    """
    config.addinivalue_line(
        "markers", "unit: Unit tests that test individual functions/methods"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that test multiple components"
    )
    config.addinivalue_line(
        "markers", "gui: Tests that require GUI components"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to run"
    )


def pytest_collection_modifyitems(config, items):
    """
    Pytest hook to modify test collection.
    
    Automatically adds markers to tests based on their names or modules.
    """
    for item in items:
        # Add 'unit' marker to all tests by default
        if not any(marker in item.keywords for marker in ['integration', 'gui', 'slow']):
            item.add_marker(pytest.mark.unit)
        
        # Add 'integration' marker to TestXXXIntegration classes
        if 'Integration' in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Add 'gui' marker to GUI-related tests
        if 'gui' in item.nodeid.lower() or 'font_manager' in item.nodeid or 'results_manager' in item.nodeid:
            item.add_marker(pytest.mark.gui)


# Custom pytest assertions (optional)

def pytest_assertrepr_compare(op, left, right):
    """
    Provide custom assertion messages for better test output.
    
    This hook is called for all assertions and can provide more readable
    failure messages.
    """
    if isinstance(left, dict) and isinstance(right, dict) and op == "==":
        return [
            "Dictionary comparison failed:",
            f"Left keys: {set(left.keys())}",
            f"Right keys: {set(right.keys())}",
            f"Common keys: {set(left.keys()) & set(right.keys())}",
            f"Differing values: {[(k, left.get(k), right.get(k)) for k in set(left.keys()) & set(right.keys()) if left.get(k) != right.get(k)]}",
        ]
