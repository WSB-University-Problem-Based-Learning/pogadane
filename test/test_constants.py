"""
Unit tests for constants module.
Tests that all constants are properly defined and have expected types/values.
"""
import pytest
from pogadane.constants import (
    APP_VERSION,
    DEFAULT_CONFIG,
    MIN_FONT_SIZE,
    MAX_FONT_SIZE,
    DEFAULT_FONT_SIZE,
    FILE_STATUS_PENDING,
    FILE_STATUS_PROCESSING,
    FILE_STATUS_COMPLETED,
    FILE_STATUS_ERROR,
)


class TestConstants:
    """Test suite for constants module."""

    def test_app_version_exists(self):
        """Test that APP_VERSION is defined and is a string."""
        assert isinstance(APP_VERSION, str)
        assert len(APP_VERSION) > 0

    def test_app_version_format(self):
        """Test that APP_VERSION follows semantic versioning."""
        parts = APP_VERSION.split('.')
        assert len(parts) >= 2  # At least major.minor
        assert all(part.isdigit() for part in parts)

    def test_font_size_constants(self):
        """Test font size constants are properly defined."""
        assert isinstance(MIN_FONT_SIZE, int)
        assert isinstance(MAX_FONT_SIZE, int)
        assert isinstance(DEFAULT_FONT_SIZE, int)
        assert MIN_FONT_SIZE < DEFAULT_FONT_SIZE < MAX_FONT_SIZE
        assert MIN_FONT_SIZE > 0
        assert MAX_FONT_SIZE < 100  # Reasonable maximum

    def test_file_status_constants(self):
        """Test file status constants are strings."""
        statuses = [
            FILE_STATUS_PENDING,
            FILE_STATUS_PROCESSING,
            FILE_STATUS_COMPLETED,
            FILE_STATUS_ERROR,
        ]
        for status in statuses:
            assert isinstance(status, str)
            assert len(status) > 0

    def test_file_status_uniqueness(self):
        """Test that all file status constants are unique."""
        statuses = [
            FILE_STATUS_PENDING,
            FILE_STATUS_PROCESSING,
            FILE_STATUS_COMPLETED,
            FILE_STATUS_ERROR,
        ]
        assert len(statuses) == len(set(statuses))

    def test_default_config_is_dict(self):
        """Test that DEFAULT_CONFIG is a dictionary."""
        assert isinstance(DEFAULT_CONFIG, dict)
        assert len(DEFAULT_CONFIG) > 0

    def test_default_config_required_keys(self):
        """Test that DEFAULT_CONFIG has all required keys."""
        required_keys = [
            'TRANSCRIPTION_PROVIDER',
            'YT_DLP_PATH',
            'WHISPER_LANGUAGE',
            'WHISPER_MODEL',
            'SUMMARY_PROVIDER',
            'SUMMARY_LANGUAGE',
            'OLLAMA_MODEL',
            'DEBUG_MODE',
        ]
        for key in required_keys:
            assert key in DEFAULT_CONFIG, f"Missing required key: {key}"

    def test_default_config_types(self):
        """Test that DEFAULT_CONFIG values have expected types."""
        # String values
        string_keys = [
            'TRANSCRIPTION_PROVIDER',
            'YT_DLP_PATH',
            'WHISPER_LANGUAGE',
            'WHISPER_MODEL',
            'SUMMARY_PROVIDER',
            'SUMMARY_LANGUAGE',
            'OLLAMA_MODEL',
            'FASTER_WHISPER_DEVICE',
            'FASTER_WHISPER_COMPUTE_TYPE',
        ]
        for key in string_keys:
            if key in DEFAULT_CONFIG:  # Some keys may be optional
                assert isinstance(DEFAULT_CONFIG[key], str)
                assert len(DEFAULT_CONFIG[key]) > 0

        # Boolean values
        assert isinstance(DEFAULT_CONFIG['DEBUG_MODE'], bool)
        assert isinstance(DEFAULT_CONFIG['FASTER_WHISPER_VAD_FILTER'], bool)

    def test_default_config_whisper_model(self):
        """Test that default Whisper model is valid."""
        valid_models = ['tiny', 'base', 'small', 'medium', 'large', 'turbo']
        assert DEFAULT_CONFIG['WHISPER_MODEL'] in valid_models

    def test_default_config_summary_provider(self):
        """Test that default summary provider is valid."""
        valid_providers = ['ollama', 'google', 'transformers']
        assert DEFAULT_CONFIG['SUMMARY_PROVIDER'] in valid_providers

    def test_default_config_prompt_templates(self):
        """Test that LLM_PROMPT_TEMPLATES exists and is a dict."""
        assert 'LLM_PROMPT_TEMPLATES' in DEFAULT_CONFIG
        assert isinstance(DEFAULT_CONFIG['LLM_PROMPT_TEMPLATES'], dict)
        assert len(DEFAULT_CONFIG['LLM_PROMPT_TEMPLATES']) > 0

    def test_default_config_prompt_template_name(self):
        """Test that default prompt template name exists in templates."""
        template_name = DEFAULT_CONFIG.get('LLM_PROMPT_TEMPLATE_NAME')
        templates = DEFAULT_CONFIG.get('LLM_PROMPT_TEMPLATES', {})
        if template_name:
            assert template_name in templates, \
                f"Default template '{template_name}' not found in templates"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
