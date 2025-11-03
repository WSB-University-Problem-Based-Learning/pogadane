# Contributing to Pogadane

Thank you for your interest in contributing to Pogadane! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 **Bug Reports** - Report issues you encounter
- ✨ **Feature Requests** - Suggest new features
- 📝 **Documentation** - Improve or translate documentation
- 💻 **Code Contributions** - Submit bug fixes or new features
- 🧪 **Testing** - Test new releases and provide feedback

## 📋 Before You Start

1. **Check existing issues** - Someone might already be working on it
2. **Read the documentation** - Familiarize yourself with the project
3. **Review the code** - Understand the architecture and patterns

## 🐛 Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or screenshots

## ✨ Suggesting Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md) and describe:

- The problem your feature would solve
- Your proposed solution
- Alternative approaches considered
- Any implementation ideas

## 💻 Code Contributions

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pogadane.git
   cd pogadane
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # Unix:
   source .venv/bin/activate
   ```

3. **Install in development mode:**
   ```bash
   python install.py --dev
   ```

4. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

### Code Standards

#### Python Style

- **PEP 8** compliance (use `black` for formatting)
- **Type hints** where appropriate
- **Docstrings** for all public functions/classes
- **Comments** for complex logic

```python
def transcribe_audio(audio_path: str, model: str = "base") -> str:
    """
    Transcribe audio file to text.
    
    Args:
        audio_path: Path to audio file
        model: Whisper model size (tiny/base/small/medium/large)
    
    Returns:
        Transcribed text
    
    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
    # Implementation
```

#### Code Organization

- Follow **SOLID principles**
- Use **design patterns** where appropriate (Strategy, Factory, Singleton)
- Keep functions **focused and small** (< 50 lines ideally)
- **Avoid duplication** - use utility modules

#### Testing

- Write **unit tests** for new functionality
- Maintain **test coverage** above 80%
- Run tests before submitting PR:

```bash
pytest
pytest --cov=src/pogadane --cov-report=html
```

### Commit Messages

Follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `style`: Code style changes

**Examples:**
```bash
feat(transcription): add Whisper Python provider

Implemented WhisperProvider class using openai-whisper library.
This provides a lightweight alternative to Faster-Whisper.

Closes #123

---

fix(gui): correct font scaling on high DPI displays

Fixed issue where font sizes were too small on 4K displays.

Fixes #456

---

docs: update installation guide for cross-platform support

Updated INSTALL.md with macOS and Linux instructions.
Added troubleshooting section for common issues.
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Run all tests** and ensure they pass
4. **Update CHANGELOG.md** with your changes
5. **Create pull request** with clear description

### Pull Request Template

When creating a PR, the template will guide you through:
- Description of changes
- Type of change (bug fix, feature, etc.)
- Testing performed
- Checklist of requirements

See [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)

## 📚 Documentation

### Writing Documentation

- Use **clear, simple language**
- Include **code examples**
- Add **screenshots** for UI changes
- Test **all instructions** before submitting

### Documentation Structure

```
docs/
├── README.md          # Main docs (user-facing)
├── INSTALL.md         # Installation guide
├── QUICK_START.md     # Beginner tutorial
└── doc/
    ├── ARCHITECTURE.md   # Technical architecture
    ├── REFACTORING.md    # Refactoring guide
    └── NOTICES.md        # Third-party licenses
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest test/test_llm_providers.py

# Run with coverage
pytest --cov=src/pogadane

# Run with verbose output
pytest -v
```

### Writing Tests

```python
import pytest
from pogadane.llm_providers import OllamaProvider

def test_ollama_provider_initialization():
    """Test OllamaProvider initializes correctly."""
    provider = OllamaProvider(model="gemma3:4b")
    assert provider.model == "gemma3:4b"
    
def test_ollama_provider_summarize_with_mock(mocker):
    """Test summarization with mocked Ollama."""
    mock_ollama = mocker.patch('ollama.generate')
    mock_ollama.return_value = {"response": "Test summary"}
    
    provider = OllamaProvider()
    result = provider.summarize("Test text", "Summarize:", "English")
    
    assert result == "Test summary"
    mock_ollama.assert_called_once()
```

## 🎨 Design Patterns Used

Pogadane follows these patterns - maintain consistency:

- **Strategy Pattern** - LLM and transcription providers
- **Factory Pattern** - Provider creation
- **Singleton Pattern** - Configuration management
- **Observer Pattern** - GUI updates (where applicable)

## 📖 Resources

- **Architecture Guide** - [doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)
- **Refactoring Guide** - [doc/REFACTORING.md](doc/REFACTORING.md)
- **Test Guide** - [test/README.md](test/README.md)
- **Code Style** - [PEP 8](https://pep8.org/)

## ❓ Questions?

- **General questions** - Open a [GitHub Discussion](https://github.com/WSB-University-Problem-Based-Learning/pogadane/discussions)
- **Bug reports** - Use [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- **Feature ideas** - Use [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)

## 🙏 Thank You!

Every contribution helps make Pogadane better. We appreciate your time and effort!

---

**Happy Coding! 🚀**
