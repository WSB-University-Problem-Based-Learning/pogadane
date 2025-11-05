"""
Test faster-whisper library integration
"""
import sys
from pathlib import Path

def test_provider_creation():
    """Test that the faster-whisper library provider can be created"""
    try:
        from pogadane.transcription_providers import FasterWhisperLibraryProvider
        
        provider = FasterWhisperLibraryProvider(
            debug_mode=True,
            device="cpu",  # Use CPU for testing
            compute_type="int8",
            batch_size=0,
            vad_filter=False
        )
        
        print("✅ FasterWhisperLibraryProvider created successfully")
        
        # Check if library is available
        is_available = provider.is_available()
        
        if is_available:
            print("✅ faster-whisper library is installed and available")
            return True
        else:
            print("⚠️  faster-whisper library not installed")
            print("   Install with: pip install faster-whisper")
            return False
            
    except Exception as e:
        print(f"❌ Error creating provider: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_factory_auto_selection():
    """Test that the factory can auto-select providers"""
    try:
        from pogadane.transcription_providers import TranscriptionProviderFactory
        from pogadane.config_loader import ConfigManager
        
        # Create config
        config = ConfigManager()
        
        # Create provider (should auto-select library if available)
        provider = TranscriptionProviderFactory.create_provider(config)
        
        if provider:
            provider_type = type(provider).__name__
            print(f"✅ Factory created provider: {provider_type}")
            return True
        else:
            print("⚠️  No provider available")
            return False
            
    except Exception as e:
        print(f"❌ Error in factory: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test that configuration options are available"""
    try:
        from pogadane.constants import DEFAULT_CONFIG
        
        required_keys = [
            "TRANSCRIPTION_PROVIDER",
            "FASTER_WHISPER_DEVICE",
            "FASTER_WHISPER_COMPUTE_TYPE",
            "FASTER_WHISPER_BATCH_SIZE",
            "FASTER_WHISPER_VAD_FILTER"
        ]
        
        missing = [key for key in required_keys if key not in DEFAULT_CONFIG]
        
        if missing:
            print(f"❌ Missing configuration keys: {missing}")
            return False
        else:
            print("✅ All configuration keys present")
            print(f"   TRANSCRIPTION_PROVIDER: {DEFAULT_CONFIG['TRANSCRIPTION_PROVIDER']}")
            print(f"   FASTER_WHISPER_DEVICE: {DEFAULT_CONFIG['FASTER_WHISPER_DEVICE']}")
            print(f"   FASTER_WHISPER_COMPUTE_TYPE: {DEFAULT_CONFIG['FASTER_WHISPER_COMPUTE_TYPE']}")
            print(f"   FASTER_WHISPER_BATCH_SIZE: {DEFAULT_CONFIG['FASTER_WHISPER_BATCH_SIZE']}")
            print(f"   FASTER_WHISPER_VAD_FILTER: {DEFAULT_CONFIG['FASTER_WHISPER_VAD_FILTER']}")
            print(f"   YT_DLP_PATH: {DEFAULT_CONFIG.get('YT_DLP_PATH', 'N/A')}")
            return True
            
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Faster-Whisper Library Integration")
    print("=" * 60)
    print()
    
    tests = [
        ("Configuration", test_configuration),
        ("Provider Creation", test_provider_creation),
        ("Factory Auto-Selection", test_factory_auto_selection),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'=' * 60}")
        print(f"Test: {name}")
        print(f"{'=' * 60}")
        result = test_func()
        results.append((name, result))
        print()
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed or library not installed")
        print()
        print("To install faster-whisper:")
        print("  pip install faster-whisper")
        sys.exit(1)
