"""
Pogadane Test Suite

This package contains comprehensive unit and integration tests for the Pogadane
video transcription and summarization application.

Test Modules:
    - test_constants: Tests for application constants and defaults
    - test_text_utils: Tests for text processing utilities
    - test_file_utils: Tests for file operation utilities
    - test_config_loader: Tests for configuration management
    - test_llm_providers: Tests for LLM provider abstraction
    - test_font_manager: Tests for GUI font management
    - test_results_manager: Tests for GUI results storage

Usage:
    Run all tests:
        pytest
    
    Run specific module:
        pytest test/test_constants.py
    
    Run with coverage:
        pytest --cov=src/pogadane --cov-report=term-missing

For more information, see test/README.md
"""

__version__ = "1.0.0"
__all__ = []
