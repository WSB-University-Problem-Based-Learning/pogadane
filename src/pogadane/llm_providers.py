"""
LLM Provider abstraction using Strategy pattern.

This module defines interfaces and implementations for different LLM providers,
allowing easy switching between:
- Ollama (local, full-featured)
- Google Gemini (cloud, API-based)
- Transformers (local, lightweight, no Ollama needed)
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


class TransformersProvider(LLMProvider):
    """
    Hugging Face Transformers provider implementation.
    
    Uses lightweight transformer models that run locally without Ollama.
    Perfect for users who want local AI without installing Ollama.
    
    Supported models:
    - facebook/bart-large-cnn (default, ~1.6GB, good quality)
    - sshleifer/distilbart-cnn-12-6 (~500MB, faster, lower quality)
    - google/flan-t5-base (~900MB, general purpose)
    - google/flan-t5-small (~300MB, very fast, basic quality)
    """
    
    DEFAULT_MODEL = "facebook/bart-large-cnn"
    
    # Model configurations
    MODELS = {
        "facebook/bart-large-cnn": {
            "max_length": 1024,
            "min_length": 30,
            "type": "summarization",
            "size": "1.6GB",
            "description": "BART Large CNN - High quality summarization (~1.6GB)"
        },
        "sshleifer/distilbart-cnn-12-6": {
            "max_length": 1024,
            "min_length": 30,
            "type": "summarization",
            "size": "500MB",
            "description": "DistilBART - Faster, smaller model (~500MB)"
        },
        "google/flan-t5-base": {
            "max_length": 512,
            "min_length": 30,
            "type": "text2text",
            "size": "900MB",
            "description": "FLAN-T5 Base - General purpose (~900MB)"
        },
        "google/flan-t5-small": {
            "max_length": 512,
            "min_length": 30,
            "type": "text2text",
            "size": "300MB",
            "description": "FLAN-T5 Small - Very fast, basic quality (~300MB)"
        }
    }
    
    def __init__(self, model_name: str = None, debug_mode: bool = False, device: str = "auto"):
        """
        Initialize Transformers provider.
        
        Args:
            model_name: Name of the Hugging Face model (default: facebook/bart-large-cnn)
            debug_mode: Enable debug logging
            device: Device to run on ("cpu", "cuda", or "auto" for automatic)
        """
        self.model_name = model_name or self.DEFAULT_MODEL
        self.debug_mode = debug_mode
        self.device = device
        self._pipeline = None
        self._transformers = None
        
        # Validate model
        if self.model_name not in self.MODELS:
            print(f"⚠️  Warning: Model '{self.model_name}' not in preset list. Will attempt to use anyway.")
    
    def summarize(self, text: str, prompt: str, language: str, source_name: str = "") -> Optional[str]:
        """Generate summary using Transformers."""
        if not self._ensure_pipeline_loaded():
            return None
        
        print(f"\n🔄 Summarizing '{source_name}' with Transformers ({self.model_name})")
        
        try:
            model_config = self.MODELS.get(self.model_name, {})
            model_type = model_config.get("type", "summarization")
            
            # Prepare input text
            # Transformers models work better with shorter inputs (typically max 1024 tokens)
            # Truncate if needed (roughly 4 chars per token)
            max_input_length = 4000  # ~1000 tokens
            if len(text) > max_input_length:
                print(f"   ℹ️  Truncating long text ({len(text)} → {max_input_length} chars)")
                text = text[:max_input_length] + "..."
            
            # Build input based on model type
            if model_type == "text2text":
                # For T5 models, include the instruction
                prompt_clean = prompt.replace("{text}", "").replace("{Text}", "").strip()
                input_text = f"Summarize in {language}: {prompt_clean}\n\n{text}"
            else:
                # For BART models, just use the text
                input_text = text
            
            # Generate summary
            print(f"   Processing with {self.model_name}...")
            
            max_length = model_config.get("max_length", 150)
            min_length = model_config.get("min_length", 30)
            
            result = self._pipeline(
                input_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            
            if result and len(result) > 0:
                summary = result[0]["summary_text"] if "summary_text" in result[0] else result[0].get("generated_text", "")
                
                if summary:
                    print(f"✅ Summary OK for '{source_name}' (Transformers).")
                    
                    # Add language note if not in target language
                    if language.lower() != "english":
                        summary = f"[Note: Summary generated in English - model doesn't support {language}]\n\n{summary}"
                    
                    return summary.strip()
            
            print(f"❌ Summary failed for '{source_name}' (Transformers). No output generated.", file=sys.stderr)
            return None
            
        except Exception as e:
            print(f"❌ Transformers error for '{source_name}': {e}", file=sys.stderr)
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return None
    
    def is_available(self) -> bool:
        """Check if transformers library is available."""
        return self._ensure_library_loaded()
    
    def _ensure_library_loaded(self) -> bool:
        """Ensure transformers library is loaded."""
        if self._transformers is None:
            try:
                import transformers
                self._transformers = transformers
                print("✅ Transformers library loaded.")
                return True
            except ImportError:
                print("❌ Error: transformers library not installed.", file=sys.stderr)
                print("   Install with: pip install transformers torch", file=sys.stderr)
                return False
        return True
    
    def _ensure_pipeline_loaded(self) -> bool:
        """Ensure model pipeline is loaded."""
        if self._pipeline is None:
            if not self._ensure_library_loaded():
                return False
            
            try:
                print(f"   Loading model '{self.model_name}' (first time may take a few minutes)...")
                
                model_config = self.MODELS.get(self.model_name, {})
                model_type = model_config.get("type", "summarization")
                
                # Determine device
                device = -1  # CPU by default
                if self.device == "auto":
                    try:
                        import torch
                        if torch.cuda.is_available():
                            device = 0  # First CUDA device
                            print(f"   ℹ️  Using GPU acceleration")
                        else:
                            print(f"   ℹ️  Using CPU (GPU not available)")
                    except ImportError:
                        print(f"   ℹ️  Using CPU (torch not available)")
                elif self.device == "cuda":
                    device = 0
                
                # Create pipeline
                self._pipeline = self._transformers.pipeline(
                    model_type,
                    model=self.model_name,
                    device=device
                )
                
                print(f"   ✅ Model loaded successfully")
                return True
                
            except Exception as e:
                print(f"❌ Error loading model '{self.model_name}': {e}", file=sys.stderr)
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
                return False
        
        return True
    
    @classmethod
    def list_available_models(cls) -> dict:
        """
        Get information about available preset models.
        
        Returns:
            dict: Dictionary of model configurations with names as keys
        """
        return {
            model_name: {
                'description': config['description'],
                'type': config['type'],
                'max_length': config['max_length'],
                'size': config.get('size', 'Unknown')  # Add size info if available
            }
            for model_name, config in cls.MODELS.items()
        }


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
        transformers_model: str = TransformersProvider.DEFAULT_MODEL,
        transformers_device: str = "auto",
        debug_mode: bool = False
    ) -> Optional[LLMProvider]:
        """
        Create an LLM provider based on type.
        
        Args:
            provider_type: Type of provider ("ollama", "google", or "transformers")
            ollama_model: Model name for Ollama
            google_api_key: API key for Google Gemini
            google_model: Model name for Google Gemini
            transformers_model: Model name for Transformers (default: facebook/bart-large-cnn)
            transformers_device: Device for Transformers ("cpu", "cuda", or "auto")
            debug_mode: Enable debug logging
            
        Returns:
            LLMProvider instance or None if type is unknown
        """
        provider_type = provider_type.lower().strip()
        
        if provider_type == "ollama":
            return OllamaProvider(ollama_model, debug_mode)
        elif provider_type == "google":
            return GoogleGeminiProvider(google_api_key, google_model, debug_mode)
        elif provider_type == "transformers":
            return TransformersProvider(transformers_model, debug_mode, transformers_device)
        else:
            print(f"❌ Error: Unknown provider type '{provider_type}'", file=sys.stderr)
            print(f"   Supported types: ollama, google, transformers", file=sys.stderr)
            return None
