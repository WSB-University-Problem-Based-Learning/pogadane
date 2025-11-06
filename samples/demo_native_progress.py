"""
Demo script showing the new native Python progress callback system.

Run this to see how the refactored backend provides structured progress updates
without any console parsing or stdout capture.
"""

from src.pogadane.backend import PogadaneBackend, ProgressUpdate, ProcessingStage
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def demo_progress_callback(update: ProgressUpdate):
    """
    Example progress callback that receives structured updates.
    
    This demonstrates how to use the new progress system.
    """
    # Map stages to icons for pretty printing
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
    
    # Print formatted progress
    print(f"{icon} [{update.progress:>5.1%}] {update.stage.value.upper()}: {update.message}")
    
    # Show details if available
    if update.details:
        for key, value in update.details.items():
            print(f"     └─ {key}: {value}")


def main():
    """Demo the new progress system"""
    print("=" * 70)
    print("Pogadane Backend - Native Python Progress Demonstration")
    print("=" * 70)
    print()
    print("This demo shows the new structured progress callback system.")
    print("No stdout capture, no console parsing - pure Python!")
    print()
    print("=" * 70)
    print()
    
    # Initialize backend
    backend = PogadaneBackend()
    
    # Example: Process a file with progress tracking
    print("📝 Note: To test with a real file, replace 'test.mp3' with an actual audio file path.")
    print()
    
    # Simulate what happens during processing
    print("Example progress updates you would see:")
    print()
    
    # Simulate progress updates
    demo_progress_callback(ProgressUpdate(
        stage=ProcessingStage.INITIALIZING,
        message="Processing: audio_sample.mp3",
        progress=0.0,
        details={"source": "audio_sample.mp3"}
    ))
    
    demo_progress_callback(ProgressUpdate(
        stage=ProcessingStage.COPYING,
        message="Copying local file...",
        progress=0.1,
        details={"file": "audio_sample.mp3"}
    ))
    
    demo_progress_callback(ProgressUpdate(
        stage=ProcessingStage.TRANSCRIBING,
        message="Transcribing audio...",
        progress=0.3,
        details={"audio_file": "temp_audio/audio_sample.mp3", "model": "turbo"}
    ))
    
    demo_progress_callback(ProgressUpdate(
        stage=ProcessingStage.SUMMARIZING,
        message="Generating summary...",
        progress=0.7,
        details={"transcription_length": 1234}
    ))
    
    demo_progress_callback(ProgressUpdate(
        stage=ProcessingStage.CLEANING,
        message="Cleaning up...",
        progress=0.9,
        details={}
    ))
    
    demo_progress_callback(ProgressUpdate(
        stage=ProcessingStage.COMPLETED,
        message="Processing complete!",
        progress=1.0,
        details={"transcription_length": 1234, "summary_length": 345}
    ))
    
    print()
    print("=" * 70)
    print()
    print("✨ Benefits of the new system:")
    print("  • Structured data with ProgressUpdate dataclass")
    print("  • Clear processing stages with enum")
    print("  • Type-safe callbacks")
    print("  • No stdout/stderr capture needed")
    print("  • Full logging to pogadane.log file")
    print("  • Progress history available")
    print("  • Easy to integrate with any UI")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
