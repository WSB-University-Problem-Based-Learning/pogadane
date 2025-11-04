"""
Transcription Providers Module

This module implements different transcription backends using the Strategy pattern.
Provides abstraction over various transcription engines:
- FasterWhisperProvider: External faster-whisper-xxl.exe (high quality, requires binary)
- WhisperProvider: Python whisper library (lightweight, pip install only)

Usage:
    provider = TranscriptionProviderFactory.create_provider(config)
    result = provider.transcribe(audio_path, output_dir, original_stem)
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import sys
import subprocess
import shlex
import os


class TranscriptionProvider(ABC):
    """Abstract base class for transcription providers."""
    
    @abstractmethod
    def transcribe(
        self, 
        audio_path: Path, 
        output_dir: Path, 
        original_stem: str,
        language: str = "Polish",
        model: str = "base"
    ) -> Optional[Path]:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            output_dir: Directory to save transcription
            original_stem: Original filename stem
            language: Transcription language
            model: Model size/name
            
        Returns:
            Path to transcription file or None on failure
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this transcription provider is available."""
        pass


class FasterWhisperProvider(TranscriptionProvider):
    """
    Faster-Whisper external executable provider.
    
    Uses the standalone faster-whisper-xxl.exe binary for high-quality
    transcription with GPU acceleration support.
    """
    
    def __init__(self, exe_path: str, debug_mode: bool = False, 
                 enable_diarization: bool = False, diarize_method: str = "pyannote_v3.1",
                 diarize_speaker_prefix: str = "SPEAKER"):
        """
        Initialize Faster-Whisper provider.
        
        Args:
            exe_path: Path to faster-whisper-xxl.exe
            debug_mode: Enable debug logging
            enable_diarization: Enable speaker diarization
            diarize_method: Diarization method to use
            diarize_speaker_prefix: Prefix for speaker labels
        """
        self.exe_path = exe_path
        self.debug_mode = debug_mode
        self.enable_diarization = enable_diarization
        self.diarize_method = diarize_method
        self.diarize_speaker_prefix = diarize_speaker_prefix
    
    def is_available(self) -> bool:
        """Check if faster-whisper executable exists."""
        exe = Path(self.exe_path)
        if exe.is_file():
            return True
        
        # Try to find in PATH
        try:
            result = subprocess.run(
                [self.exe_path, "--help"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def transcribe(
        self,
        audio_path: Path,
        output_dir: Path,
        original_stem: str,
        language: str = "Polish",
        model: str = "turbo"
    ) -> Optional[Path]:
        """Transcribe using faster-whisper executable."""
        if not audio_path.is_file():
            print(f"❌ Error: Audio file not found: '{audio_path}'", file=sys.stderr)
            return None
        
        output_format = "txt"
        expected_output = output_dir / f"{original_stem}_transcription.{output_format}"
        
        print(f"\n🔄 Transcribing with Faster-Whisper: {audio_path}")
        print(f"   Using: {self.exe_path}")
        print(f"   Model: {model}, Language: {language}")
        
        # Build command
        cmd = [
            self.exe_path,
            str(audio_path),
            "--language", language,
            "--model", model,
            "--output_format", output_format,
            "--output_dir", str(output_dir)
        ]
        
        # Add diarization if enabled
        if self.enable_diarization:
            print(f"   Diarization: ENABLED ({self.diarize_method})")
            cmd.extend(["--diarize", self.diarize_method])
            if self.diarize_speaker_prefix:
                cmd.extend(["--speaker", self.diarize_speaker_prefix])
        else:
            print("   Diarization: DISABLED")
        
        # Run command
        process = self._run_command(cmd)
        if process is None or process.returncode != 0:
            print(f"❌ Transcription failed for '{original_stem}'", file=sys.stderr)
            return None
        
        # Find output file
        fw_stem = audio_path.stem
        found_files = list(output_dir.glob(f"{fw_stem}*.{output_format}"))
        
        if not found_files:
            print(f"❌ No transcription file found: '{fw_stem}*.{output_format}' in '{output_dir}'", 
                  file=sys.stderr)
            return None
        
        # Choose appropriate file (prefer diarized if enabled)
        chosen_file = None
        if self.enable_diarization:
            spk_pref_low = self.diarize_speaker_prefix.lower()
            for f in found_files:
                if any(k in f.name.lower() for k in ["speaker", "diarize", spk_pref_low] if spk_pref_low):
                    chosen_file = f
                    break
        
        if not chosen_file:
            chosen_file = output_dir / f"{fw_stem}.{output_format}"
            if chosen_file not in found_files:
                chosen_file = found_files[0]
        
        print(f"ℹ️ Found transcription: {chosen_file}")
        
        # Rename to expected output
        try:
            if chosen_file.resolve() != expected_output.resolve():
                if expected_output.exists():
                    expected_output.unlink()
                final_path = chosen_file.rename(expected_output)
            else:
                final_path = expected_output
            
            print(f"✅ Transcription saved: {final_path}")
            return final_path
        except OSError as e:
            print(f"⚠️ Warning: Rename failed '{chosen_file}' to '{expected_output}': {e}",
                  file=sys.stderr)
            return chosen_file
    
    def _run_command(self, command_list):
        """Execute command with proper Windows handling."""
        from .file_utils import run_subprocess
        return run_subprocess(command_list, debug_mode=self.debug_mode)


class WhisperProvider(TranscriptionProvider):
    """
    OpenAI Whisper Python library provider.
    
    Lightweight transcription using the whisper pip package.
    No external executables needed - pure Python solution.
    
    Install with: pip install openai-whisper
    
    Available models:
    - tiny (~75MB) - Very fast, basic quality
    - base (~150MB) - Fast, good for simple audio
    - small (~500MB) - Balanced speed/quality
    - medium (~1.5GB) - High quality, slower
    - large (~3GB) - Best quality, slowest
    """
    
    def __init__(self, debug_mode: bool = False, device: str = "auto"):
        """
        Initialize Whisper provider.
        
        Args:
            debug_mode: Enable debug logging
            device: Device to use ("cpu", "cuda", or "auto")
        """
        self.debug_mode = debug_mode
        self.device = device
        self._whisper = None
        self._model = None
        self._current_model_name = None
    
    def is_available(self) -> bool:
        """Check if whisper library is installed."""
        try:
            import whisper
            self._whisper = whisper
            return True
        except ImportError:
            if self.debug_mode:
                print("❌ Error: whisper library not installed.", file=sys.stderr)
                print("   Install with: pip install openai-whisper", file=sys.stderr)
            return False
    
    def transcribe(
        self,
        audio_path: Path,
        output_dir: Path,
        original_stem: str,
        language: str = "Polish",
        model: str = "base"
    ) -> Optional[Path]:
        """Transcribe using OpenAI Whisper library."""
        if not self._whisper:
            if not self.is_available():
                return None
        
        if not audio_path.is_file():
            print(f"❌ Error: Audio file not found: '{audio_path}'", file=sys.stderr)
            return None
        
        output_format = "txt"
        output_path = output_dir / f"{original_stem}_transcription.{output_format}"
        
        print(f"\n🔄 Transcribing with Whisper (Python): {audio_path}")
        print(f"   Model: {model}, Language: {language}")
        
        try:
            # Load model if needed
            if self._model is None or self._current_model_name != model:
                print(f"   Loading Whisper model '{model}'...")
                
                # Determine device
                if self.device == "auto":
                    try:
                        import torch
                        device = "cuda" if torch.cuda.is_available() else "cpu"
                    except ImportError:
                        device = "cpu"
                else:
                    device = self.device
                
                print(f"   Using device: {device}")
                
                self._model = self._whisper.load_model(model, device=device)
                self._current_model_name = model
            
            # Map language names to codes
            language_code = self._get_language_code(language)
            
            # Transcribe
            print(f"   Transcribing...")
            result = self._model.transcribe(
                str(audio_path),
                language=language_code,
                verbose=self.debug_mode
            )
            
            # Extract text
            transcription_text = result.get("text", "")
            
            if not transcription_text:
                print(f"❌ Error: Empty transcription result", file=sys.stderr)
                return None
            
            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(transcription_text, encoding='utf-8')
            
            print(f"✅ Transcription saved: {output_path}")
            print(f"   Length: {len(transcription_text)} characters")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Transcription error: {e}", file=sys.stderr)
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return None
    
    def _get_language_code(self, language: str) -> str:
        """Convert language name to Whisper language code."""
        language_map = {
            "polish": "pl",
            "english": "en",
            "german": "de",
            "french": "fr",
            "spanish": "es",
            "italian": "it",
            "portuguese": "pt",
            "russian": "ru",
            "japanese": "ja",
            "chinese": "zh",
            "korean": "ko"
        }
        
        lang_lower = language.lower()
        
        # Check if it's already a code
        if len(lang_lower) == 2:
            return lang_lower
        
        # Try to find in map
        code = language_map.get(lang_lower)
        if code:
            return code
        
        # Default to English
        print(f"⚠️ Warning: Unknown language '{language}', defaulting to English", 
              file=sys.stderr)
        return "en"


class TranscriptionProviderFactory:
    """
    Factory for creating transcription provider instances.
    
    Implements the Factory pattern for provider creation.
    """
    
    @staticmethod
    def create_provider(config: Any) -> Optional[TranscriptionProvider]:
        """
        Create appropriate transcription provider based on configuration.
        
        Args:
            config: Configuration object with TRANSCRIPTION_PROVIDER setting
            
        Returns:
            TranscriptionProvider instance or None
        """
        from .constants import DEFAULT_CONFIG
        
        provider_type = getattr(
            config, 
            'TRANSCRIPTION_PROVIDER', 
            DEFAULT_CONFIG.get('TRANSCRIPTION_PROVIDER', 'faster-whisper')
        ).lower()
        
        debug_mode = getattr(config, 'DEBUG_MODE', DEFAULT_CONFIG.get('DEBUG_MODE', False))
        
        if provider_type == "faster-whisper":
            exe_path = getattr(config, 'FASTER_WHISPER_EXE', DEFAULT_CONFIG.get('FASTER_WHISPER_EXE'))
            enable_diarization = getattr(
                config, 
                'ENABLE_SPEAKER_DIARIZATION', 
                DEFAULT_CONFIG.get('ENABLE_SPEAKER_DIARIZATION', False)
            )
            diarize_method = getattr(
                config,
                'DIARIZE_METHOD',
                DEFAULT_CONFIG.get('DIARIZE_METHOD', 'pyannote_v3.1')
            )
            diarize_speaker_prefix = getattr(
                config,
                'DIARIZE_SPEAKER_PREFIX',
                DEFAULT_CONFIG.get('DIARIZE_SPEAKER_PREFIX', 'SPEAKER')
            )
            
            provider = FasterWhisperProvider(
                exe_path=exe_path,
                debug_mode=debug_mode,
                enable_diarization=enable_diarization,
                diarize_method=diarize_method,
                diarize_speaker_prefix=diarize_speaker_prefix
            )
            
        elif provider_type == "whisper":
            device = getattr(
                config,
                'WHISPER_DEVICE',
                DEFAULT_CONFIG.get('WHISPER_DEVICE', 'auto')
            )
            
            provider = WhisperProvider(
                debug_mode=debug_mode,
                device=device
            )
            
        else:
            print(f"❌ Error: Unknown transcription provider '{provider_type}'", 
                  file=sys.stderr)
            print(f"   Supported providers: 'faster-whisper', 'whisper'", 
                  file=sys.stderr)
            return None
        
        # Check if provider is available
        if not provider.is_available():
            print(f"❌ Error: Transcription provider '{provider_type}' is not available", 
                  file=sys.stderr)
            
            if provider_type == "faster-whisper":
                print(f"   Solution: Ensure faster-whisper-xxl.exe is installed", 
                      file=sys.stderr)
                print(f"   Path: {getattr(config, 'FASTER_WHISPER_EXE', 'Not configured')}", 
                      file=sys.stderr)
            elif provider_type == "whisper":
                print(f"   Solution: Install with 'pip install openai-whisper'", 
                      file=sys.stderr)
            
            return None
        
        return provider
