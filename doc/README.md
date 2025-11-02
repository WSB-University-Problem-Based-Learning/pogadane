# Documentation Index

Welcome to the Pogadane documentation! This folder contains detailed technical documentation and reference materials.

## 📚 Documentation Overview

### For Users

| Document | Description | Audience |
|----------|-------------|----------|
| [Quick Start Guide](../QUICK_START.md) | Step-by-step beginner installation guide | 🟢 Beginners |
| [Main README](../README.md) | Complete user manual and reference | 🟡 All users |
| [License Notices](NOTICES.md) | Third-party software licenses | 🟡 All users |

### For Developers

| Document | Description | Audience |
|----------|-------------|----------|
| [Architecture Documentation](ARCHITECTURE.md) | Technical architecture and design | 🔴 Developers |
| [CLI Reference](cli_help/) | Command-line help for external tools | 🔴 Advanced users |

## 📖 Documentation Details

### Quick Start Guide (`QUICK_START.md`)
**Target**: Users with no programming experience  
**Content**:
- Simple installation steps with screenshots
- First-time setup walkthrough
- How to run your first transcription
- Common troubleshooting for beginners

**Start here if**: You're new to Pogadane and want to get running quickly.

---

### Main README (`README.md`)
**Target**: All users - comprehensive reference  
**Content**:
- Complete feature overview
- Detailed installation options
- Configuration reference
- Advanced usage examples
- CLI and GUI documentation

**Use this for**: Complete understanding of all features and options.

---

### Architecture Documentation (`ARCHITECTURE.md`)
**Target**: Developers and technical contributors  
**Content**:
- System architecture diagrams
- Component interactions
- Data flow explanations
- Module structure
- API references
- Security considerations
- Development guidelines

**Use this for**: Understanding the codebase, contributing code, or integrating with Pogadane.

---

### License Notices (`NOTICES.md`)
**Target**: All users (legal/compliance)  
**Content**:
- Third-party component licenses
- OpenAI Whisper license
- SYSTRAN Faster-Whisper license
- Ollama license
- yt-dlp license
- Google Gemma terms (if applicable)

**Use this for**: Understanding legal obligations and license restrictions.

---

### CLI Reference (`cli_help/`)
**Target**: Advanced users and developers  
**Content**:
- `faster-whisper-xxl_help.txt`: Complete command reference for transcription tool
- `ollama_help.txt`: Ollama command reference
- `yt-dlp_help.txt`: YouTube downloader options

**Use this for**: Understanding all available command-line options for external tools.

---

## 🚀 Quick Navigation

**I want to...**

- **Get started quickly** → [Quick Start Guide](../QUICK_START.md)
- **Learn all features** → [Main README](../README.md)
- **Understand the code** → [Architecture Guide](ARCHITECTURE.md)
- **Check licenses** → [License Notices](NOTICES.md)
- **See command options** → [CLI Reference](cli_help/)

---

## 📁 Repository Structure

```
pogadane/
├── README.md                    # Main documentation (start here)
├── QUICK_START.md              # Beginner's installation guide
├── LICENSE                      # Project license
├── doc/                        # This folder - detailed documentation
│   ├── README.md               # This file - documentation index
│   ├── ARCHITECTURE.md         # Technical architecture guide
│   ├── NOTICES.md              # Third-party licenses
│   └── cli_help/               # External tool references
│       ├── faster-whisper-xxl_help.txt
│       ├── ollama_help.txt
│       └── yt-dlp_help.txt
├── .config/
│   └── config.py               # User configuration file
├── src/pogadane/               # Source code
│   ├── gui.py                  # GUI application
│   ├── transcribe_summarize_working.py  # CLI & core logic
│   └── __init__.py
├── tools/
│   └── pogadane_doctor.py     # Setup & maintenance utility
├── samples/                    # Sample audio files
└── res/assets/                 # Project assets (logos, icons)
```

---

## 🆘 Getting Help

### Common Questions

1. **How do I install Pogadane?**
   - Beginners: See [Quick Start Guide](../QUICK_START.md)
   - Advanced: See [Main README Installation Section](../README.md#installation-and-configuration-recommended-use-pogadane_doctorpy)

2. **How do I use the GUI?**
   - See [Main README - GUI Section](../README.md#uruchomienie-interfejsu-graficznego-gui-zalecane)
   <!-- If the heading in README.md is "Uruchomienie interfejsu graficznego (GUI) – zalecane", the correct anchor is likely:
        #uruchomienie-interfejsu-graficznego-gui-zalecane
        If you want to ensure compatibility, remove Polish diacritics and use hyphens:
        [Main README - GUI Section](../README.md#uruchomienie-interfejsu-graficznego-gui-zalecane)
        If the heading is different, update the anchor accordingly.
   - See [Main README - Results Section](../README.md#wyniki)

3. **What's the difference between Ollama and Google Gemini?**
   - See [Architecture - LLM Integration](ARCHITECTURE.md#llm-integration)

4. **Where are my results saved?**
   - See [Main README - Results Section](../README.md#uruchomienie-aplikacji-wersja-alpha-v018)

5. **I'm getting errors, what should I do?**
   - Beginners: See [Quick Start Troubleshooting](../QUICK_START.md#troubleshooting)
   - Advanced: See [Architecture - Error Handling](ARCHITECTURE.md#error-handling)

### Support Channels

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/WSB-University-Problem-Based-Learning/pogadane/discussions)
- 📧 **Direct Contact**: Check the main repository for contact information

---

## 🔄 Documentation Updates

**Last Updated**: 2025-11-02  
**Version**: v0.1.8  

This documentation is actively maintained. If you find errors or have suggestions for improvement:

1. Open an issue on GitHub
2. Submit a pull request with corrections
3. Contact the maintainers

---

## 📝 Contributing to Documentation

We welcome documentation improvements! When contributing:

### Guidelines

- **Keep it simple**: Use clear, beginner-friendly language
- **Be accurate**: Test all instructions before submitting
- **Add examples**: Real-world examples help understanding
- **Update all related docs**: If you change one file, check if others need updates
- **Follow the structure**: Maintain consistency with existing documentation

### Documentation Standards

- Use Markdown format (`.md` files)
- Include code blocks with syntax highlighting
- Add diagrams where helpful (Mermaid or images)
- Keep line length reasonable (80-100 characters)
- Use proper headings hierarchy (H1 → H2 → H3)

---

**Thank you for using Pogadane!** 🎉
