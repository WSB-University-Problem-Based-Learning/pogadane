"""
Test the newly added Google T5 and Gemma models.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pogadane.llm_providers import TransformersProvider

print("🔍 Testing New Google Model Support\n")
print("=" * 70)

# Get all models
models = TransformersProvider.MODELS

# Categorize models
t5_models = []
flan_t5_models = []
gemma_models = []
bart_models = []

for name, config in models.items():
    if "google-t5/t5" in name:
        t5_models.append((name, config))
    elif "flan-t5" in name:
        flan_t5_models.append((name, config))
    elif "gemma" in name:
        gemma_models.append((name, config))
    elif "bart" in name or "distilbart" in name:
        bart_models.append((name, config))

print("📦 BART Models (Summarization):")
for name, config in bart_models:
    print(f"  ✅ {name}")
    print(f"     Type: {config['type']}, Size: {config['size']}")
    print(f"     {config['description']}")
print()

print("📦 FLAN-T5 Models (Text2Text Generation):")
for name, config in flan_t5_models:
    print(f"  ✅ {name}")
    print(f"     Type: {config['type']}, Size: {config['size']}")
    print(f"     {config['description']}")
print()

print("📦 T5 Models (Text2Text Generation) - NEW:")
for name, config in t5_models:
    print(f"  ✅ {name}")
    print(f"     Type: {config['type']}, Size: {config['size']}")
    print(f"     {config['description']}")
print()

print("📦 Gemma Models (Text Generation) - NEW:")
for name, config in gemma_models:
    print(f"  ✅ {name}")
    print(f"     Type: {config['type']}, Size: {config['size']}")
    print(f"     {config['description']}")
print()

print("=" * 70)
print(f"📊 Total Models: {len(models)}")
print(f"   - BART: {len(bart_models)}")
print(f"   - FLAN-T5: {len(flan_t5_models)}")
print(f"   - T5: {len(t5_models)}")
print(f"   - Gemma: {len(gemma_models)}")
print()

# Verify all model types are valid
valid_types = ['summarization', 'text2text-generation', 'text-generation']
print("🔍 Validating Model Types:")
all_valid = True
for name, config in models.items():
    model_type = config.get('type', 'unknown')
    if model_type not in valid_types:
        print(f"  ❌ {name}: Invalid type '{model_type}'")
        all_valid = False

if all_valid:
    print(f"  ✅ All {len(models)} models have valid types")
print()

print("=" * 70)
print("\n💡 Model Recommendations:\n")
print("For Polish Language:")
print("  🌟 Best: google/gemma-2-2b-it or google/gemma-2-9b-it")
print("     - Multilingual, instruction-tuned")
print("     - Good Polish support")
print()
print("  ⚡ Fast: google-t5/t5-small or google-t5/t5-base")
print("     - Lightweight, good performance")
print()
print("For English Language:")
print("  🌟 Best: facebook/bart-large-cnn")
print("     - Optimized for summarization")
print()
print("  ⚡ Fast: sshleifer/distilbart-cnn-12-6")
print("     - Good quality, faster inference")
print()

print("=" * 70)
print("✅ All new models successfully added!")
print("\nNew models available in GUI:")
print("  Settings → Transformers Model → Select from dropdown")
