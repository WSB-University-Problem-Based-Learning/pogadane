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
    
    # Executable paths
    FASTER_WHISPER_EXE: str
    YT_DLP_EXE: str
    
    # Transcription settings
    TRANSCRIPTION_PROVIDER: str
    WHISPER_LANGUAGE: str
    WHISPER_MODEL: str
    WHISPER_DEVICE: str
    
    # Speaker diarization
    ENABLE_SPEAKER_DIARIZATION: bool
    DIARIZE_METHOD: str
    DIARIZE_SPEAKER_PREFIX: str
    
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
