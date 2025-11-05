"""
Pogadane Backend - GUI-focused processing module

This module provides library functions for transcription and summarization
designed to be called directly from the GUI without subprocess overhead.
"""

import sys
import os
from pathlib import Path
from typing import Optional, Tuple, Callable
import shutil
import uuid

# Import utility modules
from .config_loader import ConfigManager
from .text_utils import is_valid_url
from .file_utils import get_unique_filename, get_input_name_stem, safe_delete_file
from .constants import (
    DEFAULT_CONFIG,
    TRANSCRIPTION_START_MARKER,
    TRANSCRIPTION_END_MARKER,
    SUMMARY_START_MARKER,
    SUMMARY_END_MARKER,
    TEMP_AUDIO_FOLDER_NAME,
    PROJECT_ROOT
)
from .llm_providers import LLMProviderFactory
from .transcription_providers import TranscriptionProviderFactory


class ProgressCallback:
    """Simple progress callback handler"""
    def __init__(self):
        self.current_step = ""
        self.progress = 0.0
    
    def update(self, message: str, progress: float = None):
        """Update progress"""
        self.current_step = message
        if progress is not None:
            self.progress = progress
        print(message)


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
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Process a single file or URL.
        
        Args:
            input_source: File path or YouTube URL
            progress_callback: Optional callback for progress updates
            
        Returns:
            Tuple of (transcription, summary) or (None, None) on error
        """
        if progress_callback is None:
            progress_callback = lambda msg, prog=None: print(msg)
        
        progress_callback(f"📂 Processing: {input_source}", 0.0)
        
        # Get source name
        source_name = get_input_name_stem(input_source)
        
        # Handle YouTube URLs
        if is_valid_url(input_source):
            progress_callback(f"📥 Downloading from YouTube...", 0.1)
            audio_file = self._download_youtube_audio(input_source)
            if not audio_file:
                return None, None
        else:
            # Local file - copy to temp
            progress_callback(f"📄 Copying local file...", 0.1)
            audio_file = self._copy_to_temp(Path(input_source))
            if not audio_file:
                return None, None
        
        # Transcribe
        progress_callback(f"🎤 Transcribing audio...", 0.3)
        transcription = self._transcribe_audio(audio_file, source_name, progress_callback)
        
        if not transcription:
            progress_callback(f"❌ Transcription failed", 1.0)
            self._cleanup_temp_files(audio_file)
            return None, None
        
        # Summarize
        progress_callback(f"🤖 Generating summary...", 0.7)
        summary = self._summarize_text(transcription, source_name, progress_callback)
        
        # Cleanup
        progress_callback(f"🧹 Cleaning up...", 0.9)
        self._cleanup_temp_files(audio_file)
        
        progress_callback(f"✅ Processing complete!", 1.0)
        return transcription, summary
    
    def _download_youtube_audio(self, url: str) -> Optional[Path]:
        """Download YouTube audio to temp directory"""
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
            
            print(f"🔄 Downloading: {url}")
            print(f"   Output: {output_path}")
            
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
                print(f"✅ Downloaded: {output_path}")
                return output_path
            else:
                print(f"❌ Download failed: {result.stderr}", file=sys.stderr)
                return None
                
        except Exception as e:
            print(f"❌ Download error: {e}", file=sys.stderr)
            return None
    
    def _copy_to_temp(self, source_path: Path) -> Optional[Path]:
        """Copy local file to temp directory"""
        try:
            if not source_path.exists():
                print(f"❌ File not found: {source_path}", file=sys.stderr)
                return None
            
            # Generate unique temp filename
            unique_name = get_unique_filename(
                self.temp_audio_dir,
                source_path.stem,
                source_path.suffix
            )
            temp_path = self.temp_audio_dir / unique_name
            
            print(f"✅ Local file: {source_path}")
            print(f"   Copied to temp: {temp_path}")
            
            shutil.copy2(source_path, temp_path)
            return temp_path
            
        except Exception as e:
            print(f"❌ Copy error: {e}", file=sys.stderr)
            return None
    
    def _transcribe_audio(
        self,
        audio_path: Path,
        source_name: str,
        progress_callback: Callable
    ) -> Optional[str]:
        """Transcribe audio file"""
        try:
            # Get transcription provider
            provider = TranscriptionProviderFactory.create_provider(self.config)
            
            if not provider:
                print(f"❌ No transcription provider available", file=sys.stderr)
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
            print(f"{TRANSCRIPTION_START_MARKER}")
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
                print(f"✅ Transcript OK for '{source_name}'.")
                print(transcription)
                
                # Clean up transcription file
                try:
                    transcription_file.unlink()
                except:
                    pass
            else:
                print(f"❌ Transcription failed for '{source_name}'.", file=sys.stderr)
                transcription = None
            
            print(f"{TRANSCRIPTION_END_MARKER}")
            return transcription
            
        except Exception as e:
            print(f"❌ Transcription error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return None
    
    def _summarize_text(
        self,
        text: str,
        source_name: str,
        progress_callback: Callable
    ) -> Optional[str]:
        """Summarize transcribed text"""
        try:
            # Get LLM provider
            provider = LLMProviderFactory.create_provider(self.config)
            
            if not provider:
                print(f"❌ No LLM provider available", file=sys.stderr)
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
            
            print(f"ℹ️ Using template '{tpl_name if templates.get(tpl_name) else 'custom LLM_PROMPT'}' for '{source_name}'.")
            print(f"{SUMMARY_START_MARKER}")
            
            # Generate summary
            summary = provider.summarize(
                text=text,
                prompt=prompt,
                language=language,
                source_name=source_name
            )
            
            if summary:
                print(f"✅ Summary OK for '{source_name}'.")
                print(summary)
            else:
                print(f"❌ Summary generation failed for '{source_name}'.", file=sys.stderr)
            
            print(f"{SUMMARY_END_MARKER}")
            return summary
            
        except Exception as e:
            print(f"❌ Summarization error: {e}", file=sys.stderr)
            return None
    
    def _cleanup_temp_files(self, audio_path: Optional[Path]):
        """Clean up temporary files"""
        if audio_path and audio_path.exists():
            try:
                print(f"🧹 Cleaning up: {audio_path.name}")
                audio_path.unlink()
                print(f"✅ Deleted {audio_path.name}")
            except Exception as e:
                print(f"⚠️ Cleanup warning: {e}", file=sys.stderr)
        
        # Clean up empty temp directory
        try:
            if self.temp_audio_dir.exists() and not any(self.temp_audio_dir.iterdir()):
                print(f"ℹ️ Cleaned empty temp dir: {self.temp_audio_dir}")
        except:
            pass


# Compatibility wrapper for subprocess-based calls
def main():
    """
    Legacy CLI entry point for backwards compatibility.
    New code should use PogadaneBackend class directly.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Pogadane Audio Processing (Legacy CLI)")
    parser.add_argument("input", help="Audio file or YouTube URL")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    # Initialize backend
    backend = PogadaneBackend(Path(args.config) if args.config else None)
    
    # Process
    transcription, summary = backend.process_file(args.input)
    
    # Exit with appropriate code
    sys.exit(0 if (transcription or summary) else 1)


if __name__ == "__main__":
    main()
