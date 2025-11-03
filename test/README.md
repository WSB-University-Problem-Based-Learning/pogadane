# Testing Guide for Pogadane

This directory contains comprehensive unit tests for the Pogadane project.

## Test Structure

```
test/
├── test_constants.py          # Tests for constants module
├── test_text_utils.py          # Tests for text utilities
├── test_file_utils.py          # Tests for file utilities
├── test_config_loader.py       # Tests for configuration system
├── test_llm_providers.py       # Tests for LLM providers
├── test_font_manager.py        # Tests for font management
└── test_results_manager.py     # Tests for results management
```

## Installation

### 1. Install Test Dependencies

```powershell
pip install -r requirements-test.txt
```

Or install individually:
```powershell
pip install pytest pytest-cov pytest-mock coverage
```

### 2. Verify Installation

```powershell
pytest --version
```

## Running Tests

### Run All Tests

```powershell
pytest
```

### Run Specific Test File

```powershell
pytest test/test_constants.py
```

### Run Specific Test Class

```powershell
pytest test/test_config_loader.py::TestConfigManager
```

### Run Specific Test Method

```powershell
pytest test/test_config_loader.py::TestConfigManager::test_singleton_pattern
```

### Run with Verbose Output

```powershell
pytest -v
```

### Run with Coverage Report

```powershell
pytest --cov=src/pogadane --cov-report=term-missing
```

### Run with HTML Coverage Report

```powershell
pytest --cov=src/pogadane --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Test Markers

Tests are organized with markers for selective running:

### Run Only Unit Tests

```powershell
pytest -m unit
```

### Run Only Integration Tests

```powershell
pytest -m integration
```

### Skip Slow Tests

```powershell
pytest -m "not slow"
```

## Coverage Goals

We aim for:
- **80%+ overall code coverage**
- **90%+ for utility modules**
- **100% for critical functions** (config, providers)

### Check Current Coverage

```powershell
pytest --cov=src/pogadane --cov-report=term-missing
```

## Writing New Tests

### Test File Naming

- Test files must start with `test_`
- Mirror the module structure: `test_<module_name>.py`

### Test Class Naming

```python
class TestModuleName:
    """Test suite for ModuleName."""
    pass
```

### Test Method Naming

```python
def test_feature_description(self):
    """Test that feature does something specific."""
    # Arrange
    # Act
    # Assert
    pass
```

### Example Test

```python
import pytest
from pogadane.text_utils import strip_ansi

class TestStripAnsi:
    def test_removes_color_codes(self):
        """Test that ANSI color codes are removed."""
        text = "\033[31mRed text\033[0m"
        result = strip_ansi(text)
        assert result == "Red text"
```

## Best Practices

### 1. Arrange-Act-Assert Pattern

```python
def test_something(self):
    # Arrange: Set up test data
    manager = ConfigManager()
    
    # Act: Execute the function
    result = manager.get('KEY')
    
    # Assert: Verify the result
    assert result == expected_value
```

### 2. Use Descriptive Names

```python
# Good
def test_config_manager_returns_default_when_key_missing(self):
    pass

# Bad
def test_config(self):
    pass
```

### 3. Test One Thing at a Time

```python
# Good - separate tests
def test_add_result(self):
    rm.add_result("file", "trans", "summary")
    assert "file" in rm.results

def test_get_result(self):
    rm.add_result("file", "trans", "summary")
    result = rm.get_result("file")
    assert result is not None

# Bad - testing multiple things
def test_results_manager(self):
    rm.add_result("file", "trans", "summary")
    assert "file" in rm.results
    result = rm.get_result("file")
    assert result is not None
    rm.remove_result("file")
    assert "file" not in rm.results
```

### 4. Use Fixtures for Common Setup

```python
@pytest.fixture
def config_manager():
    """Provide a configured ConfigManager instance."""
    manager = ConfigManager()
    manager.initialize()
    return manager

def test_with_fixture(config_manager):
    value = config_manager.get('WHISPER_MODEL')
    assert value is not None
```

### 5. Use Mocking for External Dependencies

```python
from unittest.mock import Mock, patch

@patch('subprocess.run')
def test_ollama_provider(mock_run):
    mock_run.return_value = Mock(returncode=0, stdout="Summary")
    provider = OllamaProvider()
    result = provider.summarize("text", "prompt", "en")
    assert result is not None
```

## Continuous Integration

Tests should be run automatically in CI/CD:

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-test.txt
      - run: pytest --cov=src/pogadane --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Troubleshooting

### Import Errors

If you see "ModuleNotFoundError", ensure you're running pytest from the project root:

```powershell
cd C:\Users\...\pogadane
pytest
```

### Coverage Not Working

Ensure coverage is installed:

```powershell
pip install pytest-cov
```

### Tests Not Found

Check that test files start with `test_` and are in the `test/` directory.

## Test Coverage Report

After running tests with coverage:

```powershell
pytest --cov=src/pogadane --cov-report=html
```

Open `htmlcov/index.html` to see detailed coverage report with line-by-line coverage.

## Excluded from Coverage

The following are excluded from coverage requirements:
- GUI main window code (`gui.py` - requires display)
- `__repr__` methods
- Abstract methods
- `if __name__ == '__main__':` blocks

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov`
4. Aim for 80%+ coverage for new code
5. Update this README if adding new test categories

## Questions?

See the main project README.md or open an issue on GitHub.

---

**Happy Testing! 🧪**
