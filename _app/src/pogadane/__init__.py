"""
Pogadane - Audio transcription and summarization application.

This package provides tools for transcribing audio files and generating
AI-powered summaries using local or cloud-based LLM providers.
"""

__version__ = "0.1.8"
__author__ = "WSB University - Problem Based Learning"

# Export main modules
from . import constants
from . import config_loader
from . import llm_providers
from . import text_utils
from . import file_utils

__all__ = [
    'constants',
    'config_loader',
    'llm_providers',
    'text_utils',
    'file_utils',
]
