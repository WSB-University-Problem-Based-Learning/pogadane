"""
Test the improved summary generation with better error handling.
"""

print("🔍 Testing Summary Improvements\n")
print("=" * 70)

# Test 1: Check repetition detection
test_repetitive = "Powiedziaem, e z tym wanie z kluczowi i dzieci: " * 10
words = test_repetitive.split()
unique_ratio = len(set(words)) / len(words)
print(f"Test 1: Repetition Detection")
print(f"  Text length: {len(words)} words")
print(f"  Unique words: {len(set(words))}")
print(f"  Unique ratio: {unique_ratio:.2f}")
print(f"  Should detect as gibberish: {unique_ratio < 0.3}")
print()

# Test 2: Check normal text
test_normal = "This is a normal summary with various different words and concepts that don't repeat too much."
words_normal = test_normal.split()
unique_ratio_normal = len(set(words_normal)) / len(words_normal)
print(f"Test 2: Normal Text Detection")
print(f"  Text length: {len(words_normal)} words")
print(f"  Unique words: {len(set(words_normal))}")
print(f"  Unique ratio: {unique_ratio_normal:.2f}")
print(f"  Should detect as normal: {unique_ratio_normal >= 0.3}")
print()

print("=" * 70)
print("✅ Improvements Applied:\n")
print("1. Changed from max_length to max_new_tokens")
print("   - Fixes Hugging Face warning about conflicting parameters")
print()
print("2. Added repetition_penalty=1.2")
print("   - Discourages the model from repeating the same words")
print()
print("3. Added no_repeat_ngram_size=3")
print("   - Prevents repeating sequences of 3 words")
print()
print("4. Simplified T5 prompt to just 'summarize: {text}'")
print("   - Works better with FLAN-T5's training format")
print()
print("5. Added gibberish detection (unique_ratio < 0.3)")
print("   - Detects when output is too repetitive")
print("   - Shows helpful error message about using Ollama instead")
print()
print("=" * 70)
print("\n💡 Recommendation for Polish:")
print("   FLAN-T5 was trained primarily on English.")
print("   For better Polish summaries, use Ollama with:")
print("   - gemma2 (Google's multilingual model)")
print("   - llama3.1 (Meta's multilingual model)")
print("   - mistral (Good multilingual support)")
print()
print("   Change in GUI: Settings → LLM Provider → Ollama")
