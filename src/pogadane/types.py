"""
Type definitions and protocols for Pogadane.

This module contains Protocol definitions for type hints and static type checking.
"""

from typing import Protocol, Dict


class ConfigProtocol(Protocol):
    """
    Protocol defining the configuration object interface.
    
    This protocol allows type-safe access to configuration attributes
    without coupling to a specific configuration class implementation.
    
    Attributes match those found in .config/config.py
    """
    
    # Tool paths (pip-installed commands)
    YT_DLP_PATH: str
    
    # Transcription settings
    TRANSCRIPTION_PROVIDER: str
    WHISPER_LANGUAGE: str
    WHISPER_MODEL: str
    WHISPER_DEVICE: str
    
    # Faster-Whisper library settings
    FASTER_WHISPER_DEVICE: str
    FASTER_WHISPER_COMPUTE_TYPE: str
    FASTER_WHISPER_BATCH_SIZE: int
    FASTER_WHISPER_VAD_FILTER: bool
    
    # Summary/LLM settings
    SUMMARY_PROVIDER: str
    SUMMARY_LANGUAGE: str
    LLM_PROMPT_TEMPLATES: Dict[str, str]
    LLM_PROMPT_TEMPLATE_NAME: str
    LLM_PROMPT: str
    
    # Ollama settings
    OLLAMA_MODEL: str
    
    # Google Gemini settings
    GOOGLE_API_KEY: str
    GOOGLE_GEMINI_MODEL: str
    
    # Transformers settings
    TRANSFORMERS_MODEL: str
    TRANSFORMERS_DEVICE: str
    
    # General settings
    TRANSCRIPTION_FORMAT: str
    DOWNLOADED_AUDIO_FILENAME: str
    DEBUG_MODE: bool
