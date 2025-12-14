"""
Unit tests for llm_providers module.
Tests LLMProvider abstract class, concrete implementations,
and LLMProviderFactory.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pogadane.llm_providers import (
    LLMProvider,
    OllamaProvider,
    GoogleGeminiProvider,
    LLMProviderFactory,
)


class TestLLMProviderInterface:
    """Test suite for LLMProvider abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that LLMProvider cannot be instantiated directly."""
        with pytest.raises(TypeError):
            LLMProvider()

    def test_subclass_must_implement_summarize(self):
        """Test that subclasses must implement summarize method."""
        class IncompleteProvider(LLMProvider):
            def is_available(self):
                return True
        
        with pytest.raises(TypeError):
            IncompleteProvider()

    def test_subclass_must_implement_is_available(self):
        """Test that subclasses must implement is_available method."""
        class IncompleteProvider(LLMProvider):
            def summarize(self, text, prompt, language, source_name=""):
                return "summary"
        
        with pytest.raises(TypeError):
            IncompleteProvider()


class TestOllamaProvider:
    """Test suite for OllamaProvider."""

    def test_initialization(self):
        """Test OllamaProvider initialization."""
        provider = OllamaProvider(
            model="gemma3:4b",
            debug_mode=False
        )
        assert provider.model == "gemma3:4b"
        assert provider.debug_mode is False

    def test_initialization_with_defaults(self):
        """Test initialization with default parameters."""
        provider = OllamaProvider()
        assert provider.model is not None
        assert isinstance(provider.debug_mode, bool)

    @patch('subprocess.run')
    def test_is_available_success(self, mock_run):
        """Test is_available returns True when Ollama is running."""
        mock_run.return_value = Mock(returncode=0)
        
        provider = OllamaProvider()
        assert provider.is_available() is True

    @patch('subprocess.run')
    def test_is_available_failure(self, mock_run):
        """Test is_available returns False when Ollama is not running."""
        mock_run.side_effect = FileNotFoundError()
        
        provider = OllamaProvider()
        assert provider.is_available() is False

    @patch('subprocess.run')
    def test_summarize_success(self, mock_run):
        """Test successful summarization."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="This is a test summary.",
            stderr=""
        )
        
        provider = OllamaProvider(model="gemma3:4b")
        result = provider.summarize(
            text="Long text to summarize",
            prompt="Summarize this",
            language="English",
            source_name="test.mp3"
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    @patch('subprocess.run')
    def test_summarize_with_debug_mode(self, mock_run):
        """Test summarization with debug mode enabled."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Summary output",
            stderr="Debug info"
        )
        
        provider = OllamaProvider(model="gemma3:4b", debug_mode=True)
        result = provider.summarize(
            text="Text",
            prompt="Prompt",
            language="English"
        )
        
        assert result is not None

    @patch('subprocess.run')
    def test_summarize_handles_errors(self, mock_run):
        """Test that summarize handles subprocess errors gracefully."""
        mock_run.side_effect = Exception("Ollama error")
        
        provider = OllamaProvider()
        result = provider.summarize(
            text="Text",
            prompt="Prompt",
            language="English"
        )
        
        # Should handle error gracefully (return None or error message)
        assert result is None or "error" in result.lower()


class TestGoogleGeminiProvider:
    """Test suite for GoogleGeminiProvider."""

    def test_initialization(self):
        """Test GoogleGeminiProvider initialization."""
        provider = GoogleGeminiProvider(
            api_key="test_api_key",
            model="gemini-pro",
            debug_mode=False
        )
        assert provider.api_key == "test_api_key"
        assert provider.model == "gemini-pro"
        assert provider.debug_mode is False

    def test_initialization_with_defaults(self):
        """Test initialization with default parameters."""
        provider = GoogleGeminiProvider(api_key="test_key")
        assert provider.model is not None
        assert isinstance(provider.debug_mode, bool)

    def test_is_available_with_api_key(self):
        """Test is_available returns True with valid API key."""
        provider = GoogleGeminiProvider(api_key="test_api_key_123")
        # Should return True if API key is present
        assert provider.is_available() is True

    def test_is_available_without_api_key(self):
        """Test is_available returns False without API key."""
        provider = GoogleGeminiProvider(api_key="")
        assert provider.is_available() is False

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_summarize_success(self, mock_model_class, mock_configure):
        """Test successful summarization with Google Gemini."""
        # Mock the model and response
        mock_response = Mock()
        mock_response.text = "This is a Gemini summary."
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        provider = GoogleGeminiProvider(api_key="test_key")
        result = provider.summarize(
            text="Long text",
            prompt="Summarize",
            language="English",
            source_name="test.mp3"
        )
        
        assert result == "This is a Gemini summary."
        mock_configure.assert_called_once_with(api_key="test_key")

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_summarize_handles_api_errors(self, mock_model_class, mock_configure):
        """Test that summarize handles API errors gracefully."""
        mock_model_class.side_effect = Exception("API error")
        
        provider = GoogleGeminiProvider(api_key="test_key")
        result = provider.summarize(
            text="Text",
            prompt="Prompt",
            language="English"
        )
        
        # Should handle error gracefully
        assert result is None or "error" in result.lower()


class TestLLMProviderFactory:
    """Test suite for LLMProviderFactory."""

    def test_create_ollama_provider(self):
        """Test creating Ollama provider."""
        mock_config = Mock()
        mock_config.get.side_effect = lambda key, default=None: {
            'SUMMARY_PROVIDER': 'ollama',
            'OLLAMA_MODEL': 'gemma3:4b',
            'DEBUG_MODE': False
        }.get(key, default)
        
        provider = LLMProviderFactory.create_provider(mock_config)
        
        assert isinstance(provider, OllamaProvider)
        assert provider.model == 'gemma3:4b'

    def test_create_google_provider(self):
        """Test creating Google Gemini provider."""
        mock_config = Mock()
        mock_config.get.side_effect = lambda key, default=None: {
            'SUMMARY_PROVIDER': 'google',
            'GOOGLE_API_KEY': 'test_api_key',
            'GOOGLE_GEMINI_MODEL': 'gemini-pro',
            'DEBUG_MODE': False
        }.get(key, default)
        
        provider = LLMProviderFactory.create_provider(mock_config)
        
        assert isinstance(provider, GoogleGeminiProvider)
        assert provider.api_key == 'test_api_key'

    def test_create_provider_defaults_to_ollama(self):
        """Test that factory defaults to Ollama for unknown provider."""
        mock_config = Mock()
        mock_config.get.side_effect = lambda key, default=None: {
            'SUMMARY_PROVIDER': 'unknown_provider',
            'OLLAMA_MODEL': 'gemma3:4b',
            'DEBUG_MODE': False
        }.get(key, default)
        
        provider = LLMProviderFactory.create_provider(mock_config)
        
        # Should default to Ollama
        assert isinstance(provider, OllamaProvider)

    def test_create_provider_with_debug_mode(self):
        """Test creating provider with debug mode enabled."""
        mock_config = Mock()
        mock_config.get.side_effect = lambda key, default=None: {
            'SUMMARY_PROVIDER': 'ollama',
            'OLLAMA_MODEL': 'gemma3:4b',
            'DEBUG_MODE': True
        }.get(key, default)
        
        provider = LLMProviderFactory.create_provider(mock_config)
        
        assert provider.debug_mode is True

    def test_create_provider_handles_missing_config(self):
        """Test factory handles missing config values gracefully."""
        mock_config = Mock()
        mock_config.get.side_effect = lambda key, default=None: default
        
        # Should not raise error, use defaults
        provider = LLMProviderFactory.create_provider(mock_config)
        assert provider is not None


class TestProviderIntegration:
    """Integration tests for LLM providers."""

    def test_provider_interface_consistency(self):
        """Test that all providers follow the same interface."""
        providers = [
            OllamaProvider(model="test"),
            GoogleGeminiProvider(api_key="test"),
        ]
        
        for provider in providers:
            # All should have these methods
            assert hasattr(provider, 'summarize')
            assert hasattr(provider, 'is_available')
            assert callable(provider.summarize)
            assert callable(provider.is_available)

    def test_summarize_signature_consistency(self):
        """Test that summarize method signature is consistent."""
        providers = [
            OllamaProvider(model="test"),
            GoogleGeminiProvider(api_key="test"),
        ]
        
        for provider in providers:
            # Should accept these parameters
            import inspect
            sig = inspect.signature(provider.summarize)
            params = list(sig.parameters.keys())
            assert 'text' in params
            assert 'prompt' in params
            assert 'language' in params
            assert 'source_name' in params


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
