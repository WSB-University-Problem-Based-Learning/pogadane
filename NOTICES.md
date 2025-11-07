# Third-Party License Notices

Pogadane uses the following third-party components, libraries, frameworks, models, and datasets. Review their license terms if you plan to redistribute the software or build derivative work.

## Table of Contents

- [Python Libraries & Frameworks](#python-libraries--frameworks)
- [AI/ML Models](#aiml-models)
- [Datasets](#datasets)
- [External Tools](#external-tools)
- [Full License Texts](#full-license-texts)

- [Full License Texts](#full-license-texts)

---

## Python Libraries & Frameworks

### Core Dependencies

#### Flet
- **License:** Apache License 2.0
- **Copyright:** 2022 Appveyor Systems Inc.
- **Purpose:** Cross-platform GUI framework (Material Design 3)
- **Version:** ≥0.24.0
- **License text:** https://github.com/flet-dev/flet/blob/main/LICENSE
- **Homepage:** https://flet.dev

#### Google Generative AI (google-generativeai)
- **License:** Apache License 2.0
- **Copyright:** Google LLC
- **Purpose:** Google Gemini API client for AI summarization
- **Version:** ≥0.3.0
- **License text:** https://github.com/google/generative-ai-python/blob/main/LICENSE
- **Homepage:** https://ai.google.dev

#### yt-dlp
- **License:** The Unlicense (Public Domain)
- **Purpose:** Download audio/video from YouTube and other platforms
- **Version:** ≥2023.0.0
- **License text:** https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE
- **Homepage:** https://github.com/yt-dlp/yt-dlp

#### py7zr
- **License:** GNU Lesser General Public License v2.1 or later
- **Copyright:** 2019 Hiroshi Miura
- **Purpose:** 7-Zip archive extraction
- **Version:** ≥0.20.0
- **License text:** https://github.com/miurahr/py7zr/blob/master/LICENSE
- **Homepage:** https://github.com/miurahr/py7zr

### Transcription Engines

#### OpenAI Whisper (openai-whisper)
- **License:** MIT License
- **Copyright:** 2022 OpenAI
- **Purpose:** Automatic speech recognition (ASR) model
- **Version:** ≥20231117
- **License text:** https://github.com/openai/whisper/blob/main/LICENSE
- **Homepage:** https://github.com/openai/whisper
- **Paper:** Radford et al., "Robust Speech Recognition via Large-Scale Weak Supervision" (2022)

#### SYSTRAN faster-whisper
- **License:** MIT License
- **Copyright:** 2023 SYSTRAN
- **Purpose:** Optimized Whisper implementation using CTranslate2 (4x faster)
- **Version:** ≥1.0.0
- **License text:** https://github.com/SYSTRAN/faster-whisper/blob/master/LICENSE
- **Homepage:** https://github.com/SYSTRAN/faster-whisper
- **Based on:** OpenAI Whisper, CTranslate2

### AI Summarization Libraries

#### Hugging Face Transformers

#### Hugging Face Transformers
- **License:** Apache License 2.0
- **Copyright:** 2018 The Hugging Face team
- **Purpose:** State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX
- **Version:** ≥4.30.0
- **License text:** https://github.com/huggingface/transformers/blob/main/LICENSE
- **Homepage:** https://huggingface.co/transformers

#### PyTorch
- **License:** BSD-3-Clause License
- **Copyright:** Facebook, Inc. and its affiliates
- **Purpose:** Deep learning framework (required by Transformers)
- **Version:** ≥2.0.0
- **License text:** https://github.com/pytorch/pytorch/blob/main/LICENSE
- **Homepage:** https://pytorch.org

#### llama-cpp-python
- **License:** MIT License
- **Copyright:** 2023 Andrei Betlen
- **Purpose:** Python bindings for llama.cpp (GGUF model inference)
- **Version:** Optional dependency for GGUF models
- **License text:** https://github.com/abetlen/llama-cpp-python/blob/main/LICENSE.md
- **Homepage:** https://github.com/abetlen/llama-cpp-python
- **Based on:** llama.cpp by Georgi Gerganov

---

## AI/ML Models

Pogadane supports various AI models. Models are NOT distributed with Pogadane - users download them separately. Model usage is subject to their respective licenses.

### Whisper Models (Speech Recognition)

#### OpenAI Whisper Models
- **License:** MIT License
- **Copyright:** 2022 OpenAI
- **Available models:** tiny, base, small, medium, large, large-v2, large-v3, turbo
- **Purpose:** Automatic speech recognition trained on 680,000 hours of multilingual data
- **License text:** https://github.com/openai/whisper/blob/main/LICENSE
- **Model card:** https://github.com/openai/whisper/blob/main/model-card.md
- **Training data:** Weakly supervised from the internet (multilingual)

### Summarization Models (Transformers)

#### Facebook BART
- **License:** Apache License 2.0 / MIT License
- **Copyright:** Facebook AI Research
- **Models supported:**
  - `facebook/bart-large-cnn` (~1.6GB) - CNN/DailyMail fine-tuned
  - `sshleifer/distilbart-cnn-12-6` (~500MB) - Distilled version
- **Purpose:** Text summarization
- **License text:** https://github.com/facebookresearch/fairseq/blob/main/LICENSE
- **Paper:** Lewis et al., "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension" (2020)
- **Model card:** https://huggingface.co/facebook/bart-large-cnn

#### Google T5 / FLAN-T5
- **License:** Apache License 2.0
- **Copyright:** Google Research
- **Models supported:**
  - `google/flan-t5-small` (~300MB)
  - `google/flan-t5-base` (~900MB)
  - `google-t5/t5-small` (~240MB)
  - `google-t5/t5-base` (~850MB)
  - `google-t5/t5-large` (~2.7GB)
- **Purpose:** Text-to-text generation (summarization, translation, Q&A)
- **License text:** https://github.com/google-research/text-to-text-transfer-transformer/blob/main/LICENSE
- **Paper:** Raffel et al., "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer" (2020)
- **FLAN paper:** Chung et al., "Scaling Instruction-Finetuned Language Models" (2022)
- **Model card:** https://huggingface.co/google/flan-t5-base

#### Google Gemma Models
- **License:** Gemma Terms of Use (see below)
- **Copyright:** Google LLC
- **Models supported via Transformers:**
  - `google/gemma-2-2b-it` (~5GB) - Instruction-tuned 2B parameters
  - `google/gemma-2-9b-it` (~18GB) - Instruction-tuned 9B parameters
  - `google/gemma-3-4b-it` (~8GB) - Latest instruction-tuned 4B parameters
- **Purpose:** General-purpose language model (summarization, chat, generation)
- **Terms:** https://ai.google.dev/gemma/terms
- **Prohibited use policy:** https://ai.google.dev/gemma/prohibited_use_policy
- **Model card:** https://huggingface.co/google/gemma-2-2b-it
- **Paper (Gemma 3):** Gemma Team, "Gemma 3" (2025) - https://goo.gle/Gemma3Report
- **Citation:**
  ```bibtex
  @article{gemma_2025,
      title={Gemma 3},
      url={https://goo.gle/Gemma3Report},
      publisher={Kaggle},
      author={Gemma Team},
      year={2025}
  }
  ```

**Note:** Gemma models require accepting Google's terms before download. Some models are gated and require HuggingFace authentication.

### GGUF Quantized Models (llama.cpp)

#### Supported Model Families
- **Gemma** (Google) - Instruction-tuned models via llama.cpp
- **Llama** (Meta) - General-purpose language models
- **Mistral** (Mistral AI) - High-performance open models
- **Other GGUF-compatible models**

**Format:** GGUF (GPT-Generated Unified Format)
**Quantization:** Q4_K_M, Q5_K_M, Q8_0, etc.
**Purpose:** Efficient inference on CPU/GPU with reduced memory usage
**License:** Varies by model (check individual model licenses)
**Homepage:** https://github.com/ggerganov/llama.cpp

**Example model used in documentation:**
- `gemma-3-4b-it-Q4_K_M.gguf` - Quantized Gemma 3 4B (subject to Gemma Terms of Use)

### Ollama Models (Local LLM)

#### Ollama
- **License:** MIT License
- **Copyright:** Ollama
- **Purpose:** Run large language models locally
- **Version:** Optional external dependency
- **License text:** https://github.com/ollama/ollama/blob/main/LICENSE
- **Homepage:** https://ollama.com

**Supported models via Ollama** (examples):
- `llama3.2:1b` - Meta Llama 3.2 1B
- `gemma2:2b` - Google Gemma 2 2B
- `mistral:7b` - Mistral 7B
- Many others from https://ollama.com/library

**Note:** Each model has its own license. Check model pages before use.

---

## Datasets

### Common Voice Corpus

#### Mozilla Common Voice 19.0
- **License:** CC0 1.0 Universal (Public Domain Dedication)
- **Copyright:** Mozilla Foundation and contributors
- **Purpose:** Training data for Whisper models (not included in Pogadane)
- **Version:** 19.0
- **Dataset card:** https://huggingface.co/datasets/mozilla-foundation/common_voice_19_0
- **Homepage:** https://commonvoice.mozilla.org/
- **Citation:**
  ```bibtex
  @inproceedings{commonvoice:2020,
    author = {Ardila, R. and Branson, M. and Davis, K. and Henretty, M. and Kohler, M. and Meyer, J. and Morais, R. and Saunders, L. and Tyers, F. M. and Weber, G.},
    title = {Common Voice: A Massively-Multilingual Speech Corpus},
    booktitle = {Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020)},
    pages = {4211--4215},
    year = 2020
  }
  ```

**Note:** This dataset was used to train some Whisper models. Pogadane does not distribute this dataset.

### Other Training Data

- **Whisper training data:** 680,000 hours of multilingual audio from the internet (proprietary to OpenAI, not publicly available)
- **BART training data:** BookCorpus + English Wikipedia (approx. 16GB of text)
- **T5 training data:** C4 (Colossal Clean Crawled Corpus) - 750GB of web text
- **Gemma training data:** Proprietary Google training corpus (details in model paper)

---

## External Tools

### FFmpeg (Implicit Dependency)
- **License:** GNU Lesser General Public License (LGPL) version 2.1 or later / GNU General Public License (GPL) version 2 or later
- **Purpose:** Audio/video processing (required by Whisper and yt-dlp)
- **Homepage:** https://ffmpeg.org/
- **License:** https://ffmpeg.org/legal.html

**Note:** FFmpeg is NOT distributed with Pogadane. Users must install it separately:
- Windows: Included with `openai-whisper` or download from ffmpeg.org
- macOS: `brew install ffmpeg`
- Linux: `apt install ffmpeg` or `yum install ffmpeg`

---

## Sample Audio Files

The `samples/` directory contains audio files used for testing and demonstration purposes. These files are sourced from YouTube and are subject to their respective licenses.

### Serial 1670 - Scena "Powrót do alkoholizmu"
- **File:** `samples/serial1670-Powrót_do_alkoholizmu.mp3`
- **Source:** https://www.youtube.com/watch?v=StBTOpmUEjw
- **Channel:** Kurse.pl - https://www.youtube.com/@KursePl
- **Published:** April 21, 2013
- **Views:** 9,576,891 (as of inclusion date)
- **Purpose:** Testing and demonstration of transcription functionality
- **License:** Subject to YouTube's Terms of Service and channel's copyright
- **Note:** This sample is used for educational/testing purposes only

### Additional Sample Files
- **File:** `samples/Styrta_się_pali.mp3`
- **Source:** YouTube (specific video details to be documented)
- **Purpose:** Testing and demonstration of transcription functionality
- **License:** Subject to YouTube's Terms of Service and original creator's copyright
- **Note:** This sample is used for educational/testing purposes only

**Important Notice for Sample Files:**
1. Sample files in the `samples/` directory are NOT included in source distributions
2. These files are used for local testing and demonstration only
3. Users should not redistribute these files without permission from original copyright holders
4. When using Pogadane with YouTube URLs, users must comply with YouTube's Terms of Service
5. Downloaded content is subject to the original creator's copyright and licensing terms

**YouTube Terms of Service:** https://www.youtube.com/static?template=terms

---

## Full License Texts

### MIT License (OpenAI Whisper, SYSTRAN faster-whisper, Ollama, llama-cpp-python)

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Apache License 2.0 (Flet, Google Generative AI, Transformers, BART, T5, FLAN-T5)

```
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

Full text: https://www.apache.org/licenses/LICENSE-2.0

### The Unlicense (yt-dlp)

```
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
```

### BSD-3-Clause License (PyTorch)

```
BSD 3-Clause License

Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### GNU LGPL v2.1 (py7zr)

```
GNU Lesser General Public License v2.1

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.
```

Full text: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html

### CC0 1.0 Universal (Common Voice Dataset)

```
Creative Commons CC0 1.0 Universal (CC0 1.0)
Public Domain Dedication

The person who associated a work with this deed has dedicated the work to
the public domain by waiving all of his or her rights to the work worldwide
under copyright law, including all related and neighboring rights, to the
extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial
purposes, all without asking permission.
```

Full text: https://creativecommons.org/publicdomain/zero/1.0/

### Google Gemma Terms of Use

**IMPORTANT:** If you use Gemma models (via Transformers, Ollama, or GGUF format), you must comply with Google's terms:

- **Gemma Terms of Use:** https://ai.google.dev/gemma/terms
- **Gemma Prohibited Use Policy:** https://ai.google.dev/gemma/prohibited_use_policy

**Gemma models are NOT distributed with Pogadane.** Users download them separately from:
- HuggingFace (Transformers): https://huggingface.co/google
- Ollama: https://ollama.com/library
- GGUF quantized versions from community sources

**Full Gemma Terms:** See `doc/gemma_terms.md` for the complete text of Gemma Terms of Use and Prohibited Use Policy.

---

## Summary

### Components Distributed with Pogadane

Pogadane distributes the following under the MIT License:
- Source code (MIT License - see LICENSE file)
- Python libraries installed via pip (see respective licenses above)

### Components NOT Distributed

Users must download separately:
- **AI Models:** Whisper, BART, T5, Gemma, Llama, Mistral (check individual licenses)
- **External tools:** Ollama, FFmpeg
- **Datasets:** Common Voice (not needed for normal use)
- **Sample audio files:** Files in `samples/` directory are for testing only and subject to original creators' copyrights

### License Compliance

When using Pogadane:
1. ✅ **Core application:** MIT License (permissive)
2. ✅ **Python dependencies:** Mostly MIT/Apache 2.0 (permissive)
3. ⚠️ **Gemma models:** Requires accepting Google's Terms of Use
4. ⚠️ **FFmpeg:** LGPL/GPL (usually dynamically linked, no distribution issues)
5. ⚠️ **py7zr:** LGPL 2.1 (library dependency, acceptable for applications)
6. ⚠️ **Sample files:** NOT for redistribution - subject to original creators' copyright and YouTube ToS

**For commercial use:** Review individual model licenses. Most Whisper, BART, and T5 models are permissively licensed. Gemma has usage restrictions.

**For redistribution:** Include this NOTICES.md file and comply with all upstream licenses. Do NOT redistribute sample audio files from `samples/` directory.

---

## Updates

This notice file was last updated: **November 7, 2025**

If you find missing attributions or license information, please file an issue at:
https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues

