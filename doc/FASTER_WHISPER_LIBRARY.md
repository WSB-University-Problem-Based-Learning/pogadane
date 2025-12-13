# Faster-Whisper Library Integration

Pogadane now supports **SYSTRAN faster-whisper** Python library as the recommended transcription backend!

## What is faster-whisper?

[faster-whisper](https://github.com/SYSTRAN/faster-whisper) is a reimplementation of OpenAI's Whisper model using CTranslate2, which provides:

- ⚡ **4x faster** than openai-whisper with same accuracy
- 💾 **Less memory usage** than original Whisper
- 🎯 **GPU acceleration** (CUDA) and CPU optimization (INT8 quantization)
- 📦 **Pure Python** - no external executables needed
- 🚀 **Batched transcription** for even better performance
- 🎤 **VAD filtering** (Voice Activity Detection)
- ⏱️ **Word-level timestamps**
- 🗣️ **Multiple model sizes**: tiny, base, small, medium, large-v3, turbo, distil-large-v3

## Installation

### Quick Install

```bash
# Install faster-whisper library
pip install -r requirements-faster-whisper.txt

# Or install directly
pip install faster-whisper
```

### GPU Support (Optional)

For GPU acceleration, you need:
- NVIDIA GPU with CUDA support
- CUDA 12 and cuDNN 9

**Installation guides:**
- Windows/Linux: https://github.com/SYSTRAN/faster-whisper#gpu
- For CUDA 11: `pip install --force-reinstall ctranslate2==3.24.0`
- For CUDA 12 + cuDNN 8: `pip install --force-reinstall ctranslate2==4.4.0`

## Configuration

### Using Library (Default)

The library is tried first by default. No configuration needed!

```python
# In .config/config.py
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_USE_LIBRARY = True  # Default: try library first
```

### Advanced Settings

```python
# In .config/config.py

# Device selection
FASTER_WHISPER_DEVICE = "auto"  # "cuda", "cpu", or "auto"

# Quantization/compute type
FASTER_WHISPER_COMPUTE_TYPE = "auto"  # "float16", "int8", "int8_float16", or "auto"
# Note: auto uses float16 on GPU, int8 on CPU

# Batched transcription (faster!)
FASTER_WHISPER_BATCH_SIZE = 0  # 0=no batching, 8-16=recommended for speed
# Higher batch_size = faster but more memory

# Voice Activity Detection
FASTER_WHISPER_VAD_FILTER = False  # True to remove silence

# Model selection
WHISPER_MODEL = "turbo"  # Options: tiny, base, small, medium, large-v3, turbo, distil-large-v3
WHISPER_LANGUAGE = "Polish"  # or "en", "de", "fr", etc.
```

### Provider Selection

Three ways to use transcription:

#### 1. Auto (Recommended)
```python
TRANSCRIPTION_PROVIDER = "faster-whisper"
```

#### 2. Library Only
```python
TRANSCRIPTION_PROVIDER = "faster-whisper-library"
```

## Performance Comparison

### Large-v3 Model on GPU (NVIDIA RTX 3070 Ti)
| Implementation | Precision | Beam Size | Speed | Memory |
|----------------|-----------|-----------|-------|--------|
| openai/whisper | fp16 | 5 | 2m23s | 4708MB |
| faster-whisper | fp16 | 5 | 1m03s | 4525MB |
| **faster-whisper (batch=8)** | fp16 | 5 | **17s** | 6090MB |
| faster-whisper | int8 | 5 | 59s | 2926MB |

### Small Model on CPU (Intel i7-12700K, 8 threads)
| Implementation | Precision | Beam Size | Speed | Memory |
|----------------|-----------|-----------|-------|--------|
| openai/whisper | fp32 | 5 | 6m58s | 2335MB |
| faster-whisper | fp32 | 5 | 2m37s | 2257MB |
| **faster-whisper (batch=8)** | fp32 | 5 | **1m06s** | 4230MB |
| faster-whisper | int8 | 5 | 1m42s | 1477MB |

Source: [SYSTRAN/faster-whisper benchmarks](https://github.com/SYSTRAN/faster-whisper#benchmark)

## Model Sizes

| Model | Size | Quality | Speed | Use Case |
|-------|------|---------|-------|----------|
| tiny | ~75MB | Basic | Very Fast | Quick drafts |
| base | ~150MB | Good | Fast | Simple audio |
| small | ~500MB | Better | Moderate | Balanced |
| medium | ~1.5GB | High | Slower | Quality focus |
| large-v3 | ~3GB | Best | Slowest | Maximum quality |
| **turbo** | ~1.5GB | Excellent | **Fast** | **Recommended** |
| distil-large-v3 | ~1.5GB | Excellent | Fast | Optimized |

## Usage Examples

### Basic Transcription

```python
from pogadane.transcription_providers import TranscriptionProviderFactory
from pogadane.config_loader import ConfigManager

# Load config
config = ConfigManager()

# Create provider (auto-selects faster-whisper library)
provider = TranscriptionProviderFactory.create_provider(config)

# Transcribe
result = provider.transcribe(
    audio_path=Path("audio.mp3"),
    output_dir=Path("output"),
    original_stem="audio",
    language="Polish",
    model="turbo"
)

print(f"Transcription saved to: {result}")
```

### Batched Transcription (Faster!)

```python
# In .config/config.py
FASTER_WHISPER_BATCH_SIZE = 16  # Process 16 segments at once
FASTER_WHISPER_DEVICE = "cuda"  # Use GPU
FASTER_WHISPER_COMPUTE_TYPE = "float16"  # Best GPU performance
```

### CPU Optimization

```python
# In .config/config.py
FASTER_WHISPER_DEVICE = "cpu"
FASTER_WHISPER_COMPUTE_TYPE = "int8"  # Faster on CPU with less memory
FASTER_WHISPER_BATCH_SIZE = 8  # Moderate batching
```

## Migration Guide

### From openai-whisper

**Before:**
```python
TRANSCRIPTION_PROVIDER = "whisper"
WHISPER_DEVICE = "cuda"
```

**After:**
```python
TRANSCRIPTION_PROVIDER = "faster-whisper"
FASTER_WHISPER_DEVICE = "cuda"
FASTER_WHISPER_COMPUTE_TYPE = "float16"
FASTER_WHISPER_BATCH_SIZE = 8  # Enable batching for speed boost!
```

## Troubleshooting

### Library Not Found

```
❌ Error: faster-whisper library not installed.
   Install with: pip install faster-whisper
```

**Solution:**
```bash
pip install faster-whisper
```

### GPU Not Detected

**Issue:** Using CPU despite having NVIDIA GPU

**Solution:**
1. Install CUDA 12: https://developer.nvidia.com/cuda-downloads
2. Install cuDNN 9: https://developer.nvidia.com/cudnn
3. Verify: `python -c "import torch; print(torch.cuda.is_available())"`

### Out of Memory (GPU)

**Issue:** GPU runs out of memory during transcription

**Solution:**
```python
# Reduce batch size or use int8 quantization
FASTER_WHISPER_BATCH_SIZE = 4  # Lower batch size
FASTER_WHISPER_COMPUTE_TYPE = "int8_float16"  # Less memory
```

### Slow CPU Performance

**Issue:** CPU transcription is very slow

**Solution:**
```python
# Use INT8 quantization and batching
FASTER_WHISPER_COMPUTE_TYPE = "int8"
FASTER_WHISPER_BATCH_SIZE = 8
WHISPER_MODEL = "small"  # Use smaller model
```

## Benefits Summary

✅ **No external binaries** - Pure Python installation  
✅ **4x faster** than openai-whisper  
✅ **Less memory** usage  
✅ **GPU acceleration** with CUDA  
✅ **CPU optimization** with INT8  
✅ **Batched transcription** for speed  
✅ **VAD filtering** to skip silence  
✅ **Word-level timestamps**  
✅ **Same accuracy** as original Whisper  
✅ **Multiple model sizes** including optimized turbo and distil models  

## References

- **GitHub:** https://github.com/SYSTRAN/faster-whisper
- **PyPI:** https://pypi.org/project/faster-whisper/
- **Benchmarks:** https://github.com/SYSTRAN/faster-whisper#benchmark
- **CTranslate2:** https://github.com/OpenNMT/CTranslate2/

## License

faster-whisper is licensed under MIT License by SYSTRAN.
