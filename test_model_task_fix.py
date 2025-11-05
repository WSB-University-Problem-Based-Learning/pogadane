"""
Test to verify the Transformers model task name fix.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pogadane.llm_providers import TransformersProvider

def test_model_task_names():
    """Test that all model configurations have valid task names."""
    print("🔍 Testing Transformers Model Task Names\n")
    print("=" * 70)
    
    # Check all model configurations
    models = TransformersProvider.MODELS
    valid_tasks = [
        'summarization', 
        'text2text-generation',
        'translation',
        'text-generation'
    ]
    
    all_valid = True
    
    for model_name, config in models.items():
        task_type = config.get("type", "unknown")
        is_valid = task_type in valid_tasks
        
        status = "✅" if is_valid else "❌"
        print(f"{status} {model_name}")
        print(f"   Task type: {task_type}")
        print(f"   Valid: {is_valid}")
        
        if not is_valid:
            print(f"   ⚠️  Invalid task! Should be one of: {valid_tasks}")
            all_valid = False
        print()
    
    print("=" * 70)
    if all_valid:
        print("✅ All model task names are VALID!")
        print("\nThe fix is working correctly:")
        print("  - 'text2text' changed to 'text2text-generation'")
        print("  - All models now use recognized Hugging Face tasks")
        return True
    else:
        print("❌ Some model task names are INVALID!")
        return False

if __name__ == "__main__":
    success = test_model_task_names()
    sys.exit(0 if success else 1)
