"""
LLM Provider abstraction using Strategy pattern.

This module defines interfaces and implementations for different LLM providers,
allowing easy switching between Ollama (local) and Google Gemini (cloud).
"""

from abc import ABC, abstractmethod
from typing import Optional
import subprocess
import sys
from pathlib import Path


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    Implements the Strategy pattern for summarization providers.
    """
    
    @abstractmethod
    def summarize(self, text: str, prompt: str, language: str, source_name: str = "") -> Optional[str]:
        """
        Generate a summary of the given text.
        
        Args:
            text: Text to summarize
            prompt: Prompt template for summarization
            language: Target language for summary
            source_name: Name of the source file/URL (for logging)
            
        Returns:
            Generated summary text or None on failure
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available and properly configured.
        
        Returns:
            True if provider is ready to use, False otherwise
        """
        pass


class OllamaProvider(LLMProvider):
    """
    Ollama local LLM provider implementation.
    
    Runs LLM models locally using the Ollama CLI.
    """
    
    def __init__(self, model_name: str, debug_mode: bool = False):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model to use
            debug_mode: Enable debug logging
        """
        self.model_name = model_name
        self.debug_mode = debug_mode
    
    def summarize(self, text: str, prompt: str, language: str, source_name: str = "") -> Optional[str]:
        """Generate summary using Ollama."""
        print(f"\n🔄 Summarizing '{source_name}' with Ollama ({self.model_name})")
        
        full_prompt = self._build_prompt(text, prompt, language)
        
        try:
            process = self._run_ollama_command(full_prompt)
            
            if process and process.returncode == 0 and process.stdout:
                summary = process.stdout.strip()
                print(f"✅ Summary OK for '{source_name}' (Ollama).")
                return summary
            else:
                self._handle_error(process, source_name)
                return None
                
        except Exception as e:
            print(f"❌ Ollama error for '{source_name}': {e}", file=sys.stderr)
            return None
    
    def is_available(self) -> bool:
        """Check if Ollama is installed and model is available."""
        try:
            # Check if ollama command exists
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _build_prompt(self, text: str, prompt: str, language: str) -> str:
        """Build the full prompt for Ollama."""
        # Remove placeholder markers from prompt
        prompt_clean = prompt.replace("{text}", "").replace("{Text}", "").strip()
        return f"Please summarize the following text in {language}. {prompt_clean}\n\nText to summarize:\n{text}"
    
    def _run_ollama_command(self, prompt_data: str) -> Optional[subprocess.CompletedProcess]:
        """Execute Ollama command with proper error handling."""
        cmd = ["ollama", "run", self.model_name]
        
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        return subprocess.run(
            cmd,
            input=prompt_data,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
            shell=False,
            startupinfo=startupinfo
        )
    
    def _handle_error(self, process: Optional[subprocess.CompletedProcess], source_name: str):
        """Handle Ollama execution errors."""
        if not process:
            print(f"❌ Summary failed for '{source_name}' (Ollama). Process failed to start.", file=sys.stderr)
        elif process.returncode != 0:
            print(f"❌ Summary failed for '{source_name}' (Ollama). Code: {process.returncode}", file=sys.stderr)
        else:
            print(f"❌ Summary failed for '{source_name}' (Ollama). No output generated.", file=sys.stderr)


class GoogleGeminiProvider(LLMProvider):
    """
    Google Gemini API provider implementation.
    
    Uses Google's Generative AI API for cloud-based summarization.
    """
    
    def __init__(self, api_key: str, model_name: str, debug_mode: bool = False):
        """
        Initialize Google Gemini provider.
        
        Args:
            api_key: Google API key
            model_name: Name of the Gemini model to use
            debug_mode: Enable debug logging
        """
        self.api_key = api_key
        self.model_name = model_name
        self.debug_mode = debug_mode
        self._genai = None
    
    def summarize(self, text: str, prompt: str, language: str, source_name: str = "") -> Optional[str]:
        """Generate summary using Google Gemini."""
        if not self._ensure_library_loaded():
            return None
        
        if not self.api_key:
            print(f"❌ Error: GOOGLE_API_KEY not set for '{source_name}'.", file=sys.stderr)
            return None
        
        print(f"\n🔄 Summarizing '{source_name}' with Google Gemini ({self.model_name})")
        
        try:
            self._genai.configure(api_key=self.api_key)
            model = self._genai.GenerativeModel(self.model_name)
            
            full_prompt = self._build_prompt(text, prompt, language)
            
            print(f"   Sending prompt to Google for '{source_name}'...")
            response = model.generate_content(full_prompt)
            
            if response.parts:
                summary = "".join(p.text for p in response.parts if hasattr(p, 'text')).strip()
                print(f"✅ Summary OK for '{source_name}' (Google).")
                return summary
            elif response.prompt_feedback and response.prompt_feedback.block_reason:
                print(f"❌ Summary blocked by Google for '{source_name}'. Reason: {response.prompt_feedback.block_reason}", file=sys.stderr)
            else:
                print(f"❌ Summary failed for '{source_name}' (Google). No content/unknown error.", file=sys.stderr)
                
            return None
            
        except Exception as e:
            print(f"❌ Google API error for '{source_name}': {e}", file=sys.stderr)
            return None
    
    def is_available(self) -> bool:
        """Check if Google Gemini API is available."""
        return self._ensure_library_loaded() and bool(self.api_key)
    
    def _ensure_library_loaded(self) -> bool:
        """Ensure google-generativeai library is loaded."""
        if self._genai is None:
            try:
                import google.generativeai as genai
                self._genai = genai
                print("✅ Google Generative AI library loaded.")
                return True
            except ImportError:
                print("❌ Error: google-generativeai library not installed.", file=sys.stderr)
                return False
        return True
    
    def _build_prompt(self, text: str, prompt: str, language: str) -> str:
        """Build the full prompt for Google Gemini."""
        prompt_clean = prompt.replace("{text}", "").replace("{Text}", "").strip()
        return f"Please summarize the following text in {language}. {prompt_clean}\n\nText to summarize:\n{text}"


class LLMProviderFactory:
    """
    Factory for creating LLM provider instances.
    
    Implements the Factory pattern for provider creation.
    """
    
    @staticmethod
    def create_provider(
        provider_type: str,
        ollama_model: str = "gemma3:4b",
        google_api_key: str = "",
        google_model: str = "gemini-1.5-flash-latest",
        debug_mode: bool = False
    ) -> Optional[LLMProvider]:
        """
        Create an LLM provider based on type.
        
        Args:
            provider_type: Type of provider ("ollama" or "google")
            ollama_model: Model name for Ollama
            google_api_key: API key for Google Gemini
            google_model: Model name for Google Gemini
            debug_mode: Enable debug logging
            
        Returns:
            LLMProvider instance or None if type is unknown
        """
        provider_type = provider_type.lower().strip()
        
        if provider_type == "ollama":
            return OllamaProvider(ollama_model, debug_mode)
        elif provider_type == "google":
            return GoogleGeminiProvider(google_api_key, google_model, debug_mode)
        else:
            print(f"❌ Error: Unknown provider type '{provider_type}'", file=sys.stderr)
            return None
