"""
Pogadane Backend - Native Python processing module

This module provides library functions for transcription and summarization
with proper logging and progress callbacks - no console parsing.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional, Tuple, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum
import shutil
import uuid

# Import utility modules
from .config_loader import ConfigManager
from .text_utils import is_valid_url
from .file_utils import get_unique_filename, get_input_name_stem, safe_delete_file
from .constants import (
    DEFAULT_CONFIG,
    TEMP_AUDIO_FOLDER_NAME,
    PROJECT_ROOT
)
from .llm_providers import LLMProviderFactory
from .transcription_providers import TranscriptionProviderFactory


# Configure logging
logger = logging.getLogger(__name__)


class ProcessingStage(Enum):
    """Processing stages for progress tracking"""
    INITIALIZING = "initializing"
    DOWNLOADING = "downloading"
    COPYING = "copying"
    TRANSCRIBING = "transcribing"
    SUMMARIZING = "summarizing"
    CLEANING = "cleaning"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class ProgressUpdate:
    """Progress update data structure"""
    stage: ProcessingStage
    message: str
    progress: float  # 0.0 to 1.0
    details: Optional[Dict[str, Any]] = None
    
    def __str__(self):
        return f"[{self.progress:.0%}] {self.stage.value}: {self.message}"


class ProgressCallback:
    """
    Native Python progress callback handler.
    
    Provides structured progress updates without print statements.
    """
    
    def __init__(self, callback: Optional[Callable[[ProgressUpdate], None]] = None):
        """
        Initialize progress callback.
        
        Args:
            callback: Optional callback function that receives ProgressUpdate objects
        """
        self.callback = callback
        self.current_stage = ProcessingStage.INITIALIZING
        self.current_progress = 0.0
        self.history = []
    
    def update(
        self, 
        stage: ProcessingStage, 
        message: str, 
        progress: float,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Send progress update.
        
        Args:
            stage: Current processing stage
            message: Human-readable message
            progress: Progress value (0.0 to 1.0)
            details: Optional additional details
        """
        self.current_stage = stage
        self.current_progress = progress
        
        update = ProgressUpdate(
            stage=stage,
            message=message,
            progress=progress,
            details=details or {}
        )
        
        self.history.append(update)
        
        # Log the update
        logger.info(str(update))
        
        # Call the callback if provided
        if self.callback:
            try:
                self.callback(update)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")
    
    def log(self, message: str, level: str = "info"):
        """
        Send a log message without changing progress.
        
        Args:
            message: Log message
            level: Log level (info, warning, error)
        """
        log_func = getattr(logger, level, logger.info)
        log_func(message)
        
        # Also send as progress update if callback exists
        if self.callback:
            update = ProgressUpdate(
                stage=self.current_stage,
                message=message,
                progress=self.current_progress,
                details={"log_level": level}
            )
            try:
                self.callback(update)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")


class PogadaneBackend:
    """
    Backend processor for transcription and summarization.
    
    Designed for GUI integration - no CLI arguments, direct function calls.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize backend with configuration.
        
        Args:
            config_path: Optional path to config file (usually not needed - uses singleton)
        """
        # ConfigManager is a singleton - just get the instance
        self.config_manager = ConfigManager()
        
        # Only initialize with specific path if provided AND not already initialized
        if config_path and self.config_manager._config is None:
            self.config_manager.initialize(config_path)
        elif self.config_manager._config is None:
            # Initialize with default path if not already initialized
            self.config_manager.initialize()
        
        self.config = self.config_manager.config
        
        # Setup temp audio directory
        self.temp_audio_dir = PROJECT_ROOT / "src" / "pogadane" / TEMP_AUDIO_FOLDER_NAME
        self.temp_audio_dir.mkdir(parents=True, exist_ok=True)
    
    def process_file(
        self, 
        input_source: str,
        progress_callback: Optional[Callable[[ProgressUpdate], None]] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Process a single file or URL with native progress tracking.
        
        Args:
            input_source: File path or YouTube URL
            progress_callback: Optional callback that receives ProgressUpdate objects
            
        Returns:
            Tuple of (transcription, summary) or (None, None) on error
        """
        # Create progress tracker
        progress = ProgressCallback(progress_callback)
        
        try:
            progress.update(
                ProcessingStage.INITIALIZING,
                f"Processing: {input_source}",
                0.0,
                {"source": input_source}
            )
            
            # Get source name
            source_name = get_input_name_stem(input_source)
            
            # Handle YouTube URLs
            if is_valid_url(input_source):
                progress.update(
                    ProcessingStage.DOWNLOADING,
                    "Downloading from YouTube...",
                    0.1,
                    {"url": input_source}
                )
                audio_file = self._download_youtube_audio(input_source, progress)
                if not audio_file:
                    progress.update(
                        ProcessingStage.ERROR,
                        "Download failed",
                        1.0
                    )
                    return None, None
            else:
                # Local file - copy to temp
                progress.update(
                    ProcessingStage.COPYING,
                    "Copying local file...",
                    0.1,
                    {"file": input_source}
                )
                audio_file = self._copy_to_temp(Path(input_source), progress)
                if not audio_file:
                    progress.update(
                        ProcessingStage.ERROR,
                        "File copy failed",
                        1.0
                    )
                    return None, None
            
            # Transcribe
            progress.update(
                ProcessingStage.TRANSCRIBING,
                "Transcribing audio...",
                0.3,
                {"audio_file": str(audio_file)}
            )
            transcription = self._transcribe_audio(audio_file, source_name, progress)
            
            if not transcription:
                progress.update(
                    ProcessingStage.ERROR,
                    "Transcription failed",
                    1.0
                )
                self._cleanup_temp_files(audio_file, progress)
                return None, None
            
            # Summarize
            progress.update(
                ProcessingStage.SUMMARIZING,
                "Generating summary...",
                0.7,
                {"transcription_length": len(transcription)}
            )
            summary = self._summarize_text(transcription, source_name, progress)
            
            # Cleanup
            progress.update(
                ProcessingStage.CLEANING,
                "Cleaning up...",
                0.9
            )
            self._cleanup_temp_files(audio_file, progress)
            
            progress.update(
                ProcessingStage.COMPLETED,
                "Processing complete!",
                1.0,
                {
                    "transcription_length": len(transcription) if transcription else 0,
                    "summary_length": len(summary) if summary else 0
                }
            )
            
            return transcription, summary
            
        except Exception as e:
            logger.error(f"Error processing {input_source}: {e}", exc_info=True)
            progress.update(
                ProcessingStage.ERROR,
                f"Processing error: {str(e)}",
                1.0,
                {"error": str(e)}
            )
            return None, None
    
    def _download_youtube_audio(self, url: str, progress: ProgressCallback) -> Optional[Path]:
        """Download YouTube audio to temp directory using native logging"""
        try:
            import subprocess
            
            yt_dlp_path = getattr(
                self.config,
                'YT_DLP_PATH',
                DEFAULT_CONFIG.get('YT_DLP_PATH', 'yt-dlp')
            )
            
            # Generate unique filename
            temp_filename = f"youtube_{uuid.uuid4().hex[:8]}.mp3"
            output_path = self.temp_audio_dir / temp_filename
            
            progress.log(f"Downloading: {url}")
            progress.log(f"Output: {output_path}")
            
            cmd = [
                yt_dlp_path,
                "-x",  # Extract audio
                "--audio-format", "mp3",
                "--force-overwrite",
                "-o", str(output_path),
                url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0 and output_path.exists():
                progress.log(f"Downloaded: {output_path}")
                return output_path
            else:
                progress.log(f"Download failed: {result.stderr}", "error")
                return None
                
        except Exception as e:
            progress.log(f"Download error: {e}", "error")
            return None
    
    def _copy_to_temp(self, source_path: Path, progress: ProgressCallback) -> Optional[Path]:
        """Copy local file to temp directory using native logging"""
        try:
            if not source_path.exists():
                progress.log(f"File not found: {source_path}", "error")
                return None
            
            # Generate unique temp filename
            unique_name = get_unique_filename(
                self.temp_audio_dir,
                source_path.stem,
                source_path.suffix
            )
            temp_path = self.temp_audio_dir / unique_name
            
            progress.log(f"Local file: {source_path}")
            progress.log(f"Copied to temp: {temp_path}")
            
            shutil.copy2(source_path, temp_path)
            return temp_path
            
        except Exception as e:
            progress.log(f"Copy error: {e}", "error")
            return None
    
    def _transcribe_audio(
        self,
        audio_path: Path,
        source_name: str,
        progress: ProgressCallback
    ) -> Optional[str]:
        """Transcribe audio file using native logging"""
        try:
            # Get transcription provider
            provider = TranscriptionProviderFactory.create_provider(self.config)
            
            if not provider:
                progress.log("No transcription provider available", "error")
                return None
            
            # Get settings
            language = getattr(
                self.config,
                'WHISPER_LANGUAGE',
                DEFAULT_CONFIG['WHISPER_LANGUAGE']
            )
            model = getattr(
                self.config,
                'WHISPER_MODEL',
                DEFAULT_CONFIG['WHISPER_MODEL']
            )
            
            # Transcribe - provider expects (audio_path, output_dir, original_stem, language, model)
            progress.log(f"Starting transcription for '{source_name}' (model: {model}, language: {language})")
            
            transcription_file = provider.transcribe(
                audio_path=audio_path,
                output_dir=self.temp_audio_dir,
                original_stem=source_name,
                language=language,
                model=model
            )
            
            if transcription_file and transcription_file.exists():
                # Read transcription from file
                transcription = transcription_file.read_text(encoding='utf-8')
                progress.log(f"Transcription complete for '{source_name}' ({len(transcription)} chars)")
                
                # Clean up transcription file
                try:
                    transcription_file.unlink()
                except:
                    pass
            else:
                progress.log(f"Transcription failed for '{source_name}'", "error")
                transcription = None
            
            return transcription
            
        except Exception as e:
            progress.log(f"Transcription error: {e}", "error")
            logger.exception("Transcription exception")
            return None
    
    def _summarize_text(
        self,
        text: str,
        source_name: str,
        progress: ProgressCallback
    ) -> Optional[str]:
        """Summarize transcribed text using native logging"""
        try:
            # Get LLM provider
            provider = LLMProviderFactory.create_provider(self.config)
            
            if not provider:
                progress.log("No LLM provider available", "error")
                return None
            
            # Get settings
            templates = getattr(
                self.config,
                'LLM_PROMPT_TEMPLATES',
                DEFAULT_CONFIG['LLM_PROMPT_TEMPLATES']
            )
            tpl_name = getattr(
                self.config,
                'LLM_PROMPT_TEMPLATE_NAME',
                DEFAULT_CONFIG['LLM_PROMPT_TEMPLATE_NAME']
            )
            prompt = templates.get(tpl_name) or getattr(
                self.config,
                'LLM_PROMPT',
                DEFAULT_CONFIG['LLM_PROMPT']
            )
            
            # Clean prompt
            prompt = prompt.replace("{text}", "").replace("{Text}", "").strip()
            
            language = getattr(
                self.config,
                'SUMMARY_LANGUAGE',
                DEFAULT_CONFIG['SUMMARY_LANGUAGE']
            )
            
            template_info = tpl_name if templates.get(tpl_name) else 'custom LLM_PROMPT'
            progress.log(f"Using template '{template_info}' for '{source_name}'")
            progress.log(f"Starting summarization (text length: {len(text)} chars)")
            
            # Generate summary
            summary = provider.summarize(
                text=text,
                prompt=prompt,
                language=language,
                source_name=source_name
            )
            
            if summary:
                progress.log(f"Summary complete for '{source_name}' ({len(summary)} chars)")
            else:
                progress.log(f"Summary generation failed for '{source_name}'", "error")
            
            return summary
            
        except Exception as e:
            progress.log(f"Summarization error: {e}", "error")
            logger.exception("Summarization exception")
            return None
    
    def _cleanup_temp_files(self, audio_path: Optional[Path], progress: ProgressCallback):
        """Clean up temporary files using native logging"""
        if audio_path and audio_path.exists():
            try:
                progress.log(f"Cleaning up: {audio_path.name}")
                audio_path.unlink()
                progress.log(f"Deleted {audio_path.name}")
            except Exception as e:
                progress.log(f"Cleanup warning: {e}", "warning")
        
        # Clean up empty temp directory
        try:
            if self.temp_audio_dir.exists() and not any(self.temp_audio_dir.iterdir()):
                progress.log(f"Cleaned empty temp dir: {self.temp_audio_dir}")
        except:
            pass


# Compatibility wrapper for subprocess-based calls
def main():
    """
    Legacy CLI entry point for backwards compatibility.
    New code should use PogadaneBackend class directly with progress callbacks.
    """
    import argparse
    
    # Configure basic logging for CLI
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description="Pogadane Audio Processing")
    parser.add_argument("input", help="Audio file or YouTube URL")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize backend
    backend = PogadaneBackend(Path(args.config) if args.config else None)
    
    # Define simple progress callback that prints to console
    def progress_callback(update: ProgressUpdate):
        """Print progress updates to console"""
        icon_map = {
            ProcessingStage.INITIALIZING: "🔧",
            ProcessingStage.DOWNLOADING: "📥",
            ProcessingStage.COPYING: "📄",
            ProcessingStage.TRANSCRIBING: "🎤",
            ProcessingStage.SUMMARIZING: "🤖",
            ProcessingStage.CLEANING: "🧹",
            ProcessingStage.COMPLETED: "✅",
            ProcessingStage.ERROR: "❌"
        }
        icon = icon_map.get(update.stage, "ℹ️")
        print(f"{icon} [{update.progress:.0%}] {update.message}")
    
    # Process
    transcription, summary = backend.process_file(args.input, progress_callback)
    
    # Exit with appropriate code
    sys.exit(0 if (transcription or summary) else 1)


if __name__ == "__main__":
    main()
