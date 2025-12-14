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
import logging
from pathlib import Path


# Configure logger
logger = logging.getLogger(__name__)


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
        from .file_utils import run_subprocess
        
        cmd = ["ollama", "run", self.model_name]
        return run_subprocess(cmd, input_data=prompt_data, debug_mode=self.debug_mode)
    
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
            "type": "text2text-generation",
            "size": "900MB",
            "description": "FLAN-T5 Base - General purpose (~900MB)"
        },
        "google/flan-t5-small": {
            "max_length": 512,
            "min_length": 30,
            "type": "text2text-generation",
            "size": "300MB",
            "description": "FLAN-T5 Small - Very fast, basic quality (~300MB)"
        },
        "google-t5/t5-small": {
            "max_length": 512,
            "min_length": 30,
            "type": "text2text-generation",
            "size": "240MB",
            "description": "T5 Small - Compact, fast (~240MB)"
        },
        "google-t5/t5-base": {
            "max_length": 512,
            "min_length": 30,
            "type": "text2text-generation",
            "size": "850MB",
            "description": "T5 Base - Balanced performance (~850MB)"
        },
        "google-t5/t5-large": {
            "max_length": 512,
            "min_length": 30,
            "type": "text2text-generation",
            "size": "2.7GB",
            "description": "T5 Large - High quality, slower (~2.7GB)"
        },
        "google/gemma-2-2b-it": {
            "max_length": 2048,
            "min_length": 50,
            "type": "text-generation",
            "size": "5GB",
            "description": "Gemma 2 2B Instruct - Lightweight instruction-tuned (~5GB)"
        },
        "google/gemma-2-9b-it": {
            "max_length": 2048,
            "min_length": 50,
            "type": "text-generation",
            "size": "18GB",
            "description": "Gemma 2 9B Instruct - Powerful instruction-tuned (~18GB)"
        },
        "google/gemma-3-4b-it": {
            "max_length": 2048,
            "min_length": 50,
            "type": "text-generation",
            "size": "8GB",
            "description": "Gemma 3 4B Instruct - Latest Google model (~8GB)",
            "gated": True  # Requires HuggingFace authentication
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
            # Clean the text first - remove excessive whitespace and newlines
            text = ' '.join(text.split())
            
            # Try different chunk sizes if needed
            chunk_sizes = [3500, 2500, 1500, 1000]  # Progressive fallback
            
            for max_input_length in chunk_sizes:
                try:
                    # Truncate if needed
                    if len(text) > max_input_length:
                        if max_input_length == chunk_sizes[0]:  # Only print once
                            print(f"   ℹ️  Truncating long text ({len(text)} → {max_input_length} chars)")
                        working_text = text[:max_input_length]
                    else:
                        working_text = text
                    
                    # Build input based on model type
                    if model_type == "text2text-generation":
                        # For T5 models, use a clearer prompt
                        # T5 models work better with task-specific prefixes
                        if language.lower() == "polish":
                            # Try to get Polish output by being explicit
                            input_text = f"summarize: {working_text}"
                        else:
                            input_text = f"summarize: {working_text}"
                    elif model_type == "text-generation":
                        # For Gemma and other instruction-tuned models
                        # Use a conversational prompt format
                        if language.lower() == "polish":
                            input_text = f"Proszę podsumuj poniższy tekst w języku polskim:\n\n{working_text}\n\nPodsumowanie:"
                        else:
                            input_text = f"Please summarize the following text:\n\n{working_text}\n\nSummary:"
                    else:
                        # For BART models, just use the text
                        input_text = working_text
                    
                    # Generate summary
                    if max_input_length == chunk_sizes[0]:
                        print(f"   Processing with {self.model_name}...")
                    
                    max_length = model_config.get("max_length", 150)
                    min_length = model_config.get("min_length", 30)
                    
                    # Use max_new_tokens instead of max_length to avoid warning
                    # Calculate max_new_tokens (roughly 75% of max_length to account for input)
                    max_new_tokens = int(max_length * 0.5)  # Generate up to half of max_length as new tokens
                    
                    # Prepare generation parameters based on model type
                    gen_params = {
                        "max_new_tokens": max_new_tokens,
                        "do_sample": False,
                        "truncation": True,
                        "clean_up_tokenization_spaces": True,
                        "repetition_penalty": 1.2,  # Prevent repetition
                        "no_repeat_ngram_size": 3,  # Prevent repeating 3-grams
                    }
                    
                    # For text-generation models, don't use min_length (not supported)
                    if model_type != "text-generation":
                        gen_params["min_length"] = min_length
                    
                    # Use more conservative settings to avoid errors
                    result = self._pipeline(input_text, **gen_params)
                    
                    if result and len(result) > 0:
                        summary = result[0]["summary_text"] if "summary_text" in result[0] else result[0].get("generated_text", "")
                        
                        if summary:
                            # Check for repetitive gibberish (common with multilingual issues)
                            # If the same phrase appears more than 3 times, it's likely broken
                            words = summary.split()
                            if len(words) > 10:
                                # Check for excessive repetition
                                unique_ratio = len(set(words)) / len(words)
                                if unique_ratio < 0.3:  # Less than 30% unique words = repetitive gibberish
                                    print(f"⚠️  Detected repetitive output (unique ratio: {unique_ratio:.2f})")
                                    print(f"   This usually means the model doesn't support {language} well.")
                                    summary = f"[⚠️ Model limitation: FLAN-T5 doesn't support Polish well. Consider using Ollama with a Polish-capable model like 'gemma2' or 'llama3.1']\n\n[Original attempt - may be low quality]:\n{summary[:200]}..."
                            
                            print(f"✅ Summary OK for '{source_name}' (Transformers).")
                            
                            return summary.strip()
                    
                    # If we get here, no summary was generated
                    break
                    
                except Exception as chunk_error:
                    # If this isn't the last chunk size, try smaller
                    if max_input_length != chunk_sizes[-1]:
                        print(f"   ⚠️  Retrying with smaller chunk ({max_input_length} → {chunk_sizes[chunk_sizes.index(max_input_length) + 1]})")
                        continue
                    else:
                        # Last attempt failed, re-raise
                        raise chunk_error
            
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
                from .constants import MODELS_DIR
                import os
                
                # Set cache directory to local dep/models
                cache_dir = str(MODELS_DIR)
                os.environ['TRANSFORMERS_CACHE'] = cache_dir
                os.environ['HF_HOME'] = cache_dir
                
                print(f"   Loading model '{self.model_name}' from {cache_dir}")
                print(f"   (First time may take a few minutes to download...)")
                
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
                
                # Create pipeline - cache location set via environment variables above
                self._pipeline = self._transformers.pipeline(
                    model_type,
                    model=self.model_name,
                    device=device
                )
                
                print(f"   ✅ Model loaded successfully")
                return True
                
            except Exception as e:
                error_message = str(e)
                print(f"❌ Error loading model '{self.model_name}': {error_message}", file=sys.stderr)
                
                # Check if this is a gated model authentication error
                if "gated" in error_message.lower() or "401" in error_message or "authenticate" in error_message.lower():
                    model_config = self.MODELS.get(self.model_name, {})
                    if model_config.get("gated", False):
                        print(f"\n🔒 Model '{self.model_name}' requires HuggingFace authentication:", file=sys.stderr)
                        print(f"   1. Create account at: https://huggingface.co/join", file=sys.stderr)
                        print(f"   2. Request access at: https://huggingface.co/{self.model_name}", file=sys.stderr)
                        print(f"   3. Generate token at: https://huggingface.co/settings/tokens", file=sys.stderr)
                        print(f"   4. Run: huggingface-cli login", file=sys.stderr)
                        print(f"   5. Enter your token when prompted\n", file=sys.stderr)
                
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


class LlamaCppProvider(LLMProvider):
    """
    Llama.cpp GGUF model provider implementation.
    
    Uses llama-cpp-python to run quantized GGUF models locally.
    Perfect for running large models efficiently on CPU or GPU.
    
    Supported formats:
    - GGUF quantized models (Q4_K_M, Q5_K_M, Q8_0, etc.)
    - Works with Gemma, Llama, Mistral, and other GGUF models
    """
    
    def __init__(self, model_path: str, debug_mode: bool = False, n_ctx: int = 4096, n_gpu_layers: int = 0):
        """
        Initialize Llama.cpp provider.
        
        Args:
            model_path: Path to the GGUF model file
            debug_mode: Enable debug logging
            n_ctx: Context window size (default: 4096)
            n_gpu_layers: Number of layers to offload to GPU (0 = CPU only)
        """
        self.model_path = model_path
        self.debug_mode = debug_mode
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self._llm = None
        self._llama_cpp = None
    
    def summarize(self, text: str, prompt: str, language: str, source_name: str = "") -> Optional[str]:
        """Generate summary using Llama.cpp GGUF model."""
        if not self._ensure_model_loaded():
            return None
        
        print(f"\n🔄 Summarizing '{source_name}' with GGUF model ({Path(self.model_path).name})")
        
        try:
            # Build the full prompt
            full_prompt = self._build_prompt(text, prompt, language)
            
            print(f"   Generating summary...")
            
            # Generate summary with llama.cpp
            response = self._llm(
                full_prompt,
                max_tokens=512,  # Maximum tokens to generate
                temperature=0.7,
                top_p=0.9,
                repeat_penalty=1.1,
                stop=["</s>", "\n\n\n"],  # Stop sequences
                echo=False  # Don't echo the prompt
            )
            
            if response and 'choices' in response and len(response['choices']) > 0:
                summary = response['choices'][0]['text'].strip()
                
                if summary:
                    print(f"✅ Summary OK for '{source_name}' (GGUF).")
                    return summary
            
            print(f"❌ Summary failed for '{source_name}' (GGUF). No output generated.", file=sys.stderr)
            return None
            
        except Exception as e:
            print(f"❌ GGUF model error for '{source_name}': {e}", file=sys.stderr)
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return None
    
    def is_available(self) -> bool:
        """Check if llama-cpp-python is available and model exists."""
        if not self._ensure_library_loaded():
            return False
        
        # Check if model file exists
        model_file = Path(self.model_path)
        if not model_file.exists():
            print(f"❌ Error: GGUF model file not found: {self.model_path}", file=sys.stderr)
            return False
        
        return True
    
    def _ensure_library_loaded(self) -> bool:
        """Ensure llama-cpp-python library is loaded."""
        if self._llama_cpp is None:
            try:
                from llama_cpp import Llama
                self._llama_cpp = Llama
                print("✅ llama-cpp-python library loaded.")
                return True
            except ImportError:
                print("❌ Error: llama-cpp-python library not installed.", file=sys.stderr)
                print("   Install with: pip install llama-cpp-python", file=sys.stderr)
                return False
        return True
    
    def _ensure_model_loaded(self) -> bool:
        """Ensure GGUF model is loaded."""
        if self._llm is None:
            if not self._ensure_library_loaded():
                return False
            
            try:
                model_file = Path(self.model_path)
                if not model_file.exists():
                    print(f"❌ Error: GGUF model file not found: {self.model_path}", file=sys.stderr)
                    return False
                
                print(f"   Loading GGUF model: {model_file.name}")
                print(f"   Context size: {self.n_ctx}, GPU layers: {self.n_gpu_layers}")
                
                # Load the model
                self._llm = self._llama_cpp(
                    model_path=str(model_file),
                    n_ctx=self.n_ctx,
                    n_gpu_layers=self.n_gpu_layers,
                    verbose=self.debug_mode
                )
                
                print(f"   ✅ GGUF model loaded successfully")
                return True
                
            except Exception as e:
                print(f"❌ Error loading GGUF model '{self.model_path}': {e}", file=sys.stderr)
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
                return False
        
        return True
    
    def _build_prompt(self, text: str, prompt: str, language: str) -> str:
        """Build the full prompt for GGUF model."""
        # For Gemma models, use Gemma chat template
        if "gemma" in self.model_path.lower():
            # Gemma chat template format
            system_msg = f"You are a helpful AI assistant that creates summaries in {language}."
            user_msg = f"{prompt}\n\nText to summarize:\n{text[:2000]}"  # Limit text length
            
            return f"<start_of_turn>user\n{user_msg}<end_of_turn>\n<start_of_turn>model\n"
        else:
            # Generic format for other models
            prompt_clean = prompt.replace("{text}", "").replace("{Text}", "").strip()
            return f"### Instruction:\n{prompt_clean} Please respond in {language}.\n\n### Input:\n{text[:2000]}\n\n### Response:\n"


class LLMProviderFactory:
    """
    Factory for creating LLM provider instances.
    
    Implements the Factory pattern for provider creation.
    """
    
    @staticmethod
    def create_provider(config, debug_mode: bool = False) -> Optional[LLMProvider]:
        """
        Create an LLM provider based on config.
        
        Args:
            config: Configuration object with provider settings (ConfigProtocol)
            debug_mode: Enable debug logging (optional, overrides config.DEBUG_MODE if provided)
            
        Returns:
            LLMProvider instance or None if type is unknown
            
        Example:
            >>> from types import SimpleNamespace
            >>> config = SimpleNamespace(
            ...     SUMMARY_PROVIDER='ollama',
            ...     OLLAMA_MODEL='gemma3:4b',
            ...     DEBUG_MODE=False
            ... )
            >>> provider = LLMProviderFactory.create_provider(config)
        """
        # Support both attribute access (config.SUMMARY_PROVIDER) 
        # and dict-like access (config.get('SUMMARY_PROVIDER'))
        if hasattr(config, 'get'):
            # Dict-like config object (used in tests)
            provider_type = config.get('SUMMARY_PROVIDER', 'ollama')
            ollama_model = config.get('OLLAMA_MODEL', 'gemma3:4b')
            google_api_key = config.get('GOOGLE_API_KEY', '')
            google_model = config.get('GOOGLE_GEMINI_MODEL', 'gemini-1.5-flash-latest')
            transformers_model = config.get('TRANSFORMERS_MODEL', TransformersProvider.DEFAULT_MODEL)
            transformers_device = config.get('TRANSFORMERS_DEVICE', 'auto')
            gguf_model_path = config.get('GGUF_MODEL_PATH', '')
            gguf_n_gpu_layers = int(config.get('GGUF_N_GPU_LAYERS', 0))
            use_debug = config.get('DEBUG_MODE', False) if not debug_mode else debug_mode
        else:
            # Attribute-based config object (standard usage)
            provider_type = getattr(config, 'SUMMARY_PROVIDER', 'ollama')
            ollama_model = getattr(config, 'OLLAMA_MODEL', 'gemma3:4b')
            google_api_key = getattr(config, 'GOOGLE_API_KEY', '')
            google_model = getattr(config, 'GOOGLE_GEMINI_MODEL', 'gemini-1.5-flash-latest')
            transformers_model = getattr(config, 'TRANSFORMERS_MODEL', TransformersProvider.DEFAULT_MODEL)
            transformers_device = getattr(config, 'TRANSFORMERS_DEVICE', 'auto')
            gguf_model_path = getattr(config, 'GGUF_MODEL_PATH', '')
            gguf_n_gpu_layers = int(getattr(config, 'GGUF_N_GPU_LAYERS', 0))
            use_debug = getattr(config, 'DEBUG_MODE', False) if not debug_mode else debug_mode
        
        # Ensure provider_type is a string
        if not isinstance(provider_type, str):
            print(f"❌ Error: SUMMARY_PROVIDER must be a string, got {type(provider_type).__name__}", file=sys.stderr)
            provider_type = 'ollama'  # Fallback to default
        
        provider_type = provider_type.lower().strip()
        
        if provider_type == "ollama":
            return OllamaProvider(ollama_model, use_debug)
        elif provider_type == "google":
            return GoogleGeminiProvider(google_api_key, google_model, use_debug)
        elif provider_type == "transformers":
            return TransformersProvider(transformers_model, use_debug, transformers_device)
        elif provider_type == "gguf" or provider_type == "llama-cpp":
            return LlamaCppProvider(gguf_model_path, use_debug, n_gpu_layers=gguf_n_gpu_layers)
        else:
            print(f"❌ Error: Unknown provider type '{provider_type}'", file=sys.stderr)
            print(f"   Supported types: ollama, google, transformers, gguf", file=sys.stderr)
            return None
