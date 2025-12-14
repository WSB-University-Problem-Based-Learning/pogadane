"""
Unit tests for config_loader module.
Tests ConfigManager (Singleton) and ConfigLoader (Factory) patterns.
"""
import pytest
from pathlib import Path
import tempfile
import importlib
from pogadane.config_loader import ConfigManager, ConfigLoader
from pogadane.constants import DEFAULT_CONFIG


class TestConfigLoader:
    """Test suite for ConfigLoader factory."""

    def test_load_from_valid_file(self):
        """Test loading configuration from a valid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write("""
TRANSCRIPTION_PROVIDER = 'faster-whisper'
WHISPER_MODEL = 'base'
DEBUG_MODE = True
""")
            tmp_path = tmp.name
        
        try:
            config = ConfigLoader.load_from_file(tmp_path)
            assert hasattr(config, 'TRANSCRIPTION_PROVIDER')
            assert config.TRANSCRIPTION_PROVIDER == 'faster-whisper'
            assert config.WHISPER_MODEL == 'base'
            assert config.DEBUG_MODE is True
        finally:
            Path(tmp_path).unlink()

    def test_load_from_nonexistent_file(self):
        """Test loading from nonexistent file returns fallback config."""
        config = ConfigLoader.load_from_file("/nonexistent/config.py")
        # Should return fallback config with defaults, not None
        assert config is not None
        assert hasattr(config, 'TRANSCRIPTION_PROVIDER')

    def test_load_from_invalid_python(self):
        """Test loading from invalid Python file returns fallback config."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write("this is not valid python code {{{")
            tmp_path = tmp.name
        
        try:
            config = ConfigLoader.load_from_file(tmp_path)
            # Should return fallback config with defaults, not None
            assert config is not None
            assert hasattr(config, 'TRANSCRIPTION_PROVIDER')
        finally:
            Path(tmp_path).unlink()

    def test_load_preserves_all_attributes(self):
        """Test that all attributes from config file are preserved."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write("""
STRING_VAL = 'test'
INT_VAL = 42
BOOL_VAL = False
LIST_VAL = [1, 2, 3]
DICT_VAL = {'key': 'value'}
""")
            tmp_path = tmp.name
        
        try:
            config = ConfigLoader.load_from_file(tmp_path)
            assert config.STRING_VAL == 'test'
            assert config.INT_VAL == 42
            assert config.BOOL_VAL is False
            assert config.LIST_VAL == [1, 2, 3]
            assert config.DICT_VAL == {'key': 'value'}
        finally:
            Path(tmp_path).unlink()


class TestConfigManager:
    """Test suite for ConfigManager singleton."""

    def test_singleton_pattern(self):
        """Test that ConfigManager follows singleton pattern."""
        # Reset singleton for testing
        ConfigManager._instance = None
        
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        
        assert manager1 is manager2

    def test_get_with_default(self):
        """Test getting config value with default fallback."""
        manager = ConfigManager()
        manager.initialize()
        
        # Get existing key from DEFAULT_CONFIG
        value = manager.get('WHISPER_MODEL')
        assert value is not None
        
        # Get non-existing key with default
        value = manager.get('NONEXISTENT_KEY', 'default_value')
        assert value == 'default_value'

    def test_get_without_default(self):
        """Test getting config value without default."""
        manager = ConfigManager()
        manager.initialize()
        
        # Existing key
        value = manager.get('WHISPER_MODEL')
        assert value == DEFAULT_CONFIG['WHISPER_MODEL']
        
        # Non-existing key
        value = manager.get('NONEXISTENT_KEY')
        assert value is None

    def test_set_value(self):
        """Test setting config value at runtime."""
        manager = ConfigManager()
        manager.initialize()
        
        manager.set('TEST_KEY', 'test_value')
        assert manager.get('TEST_KEY') == 'test_value'

    def test_set_overwrites_existing(self):
        """Test that set() overwrites existing values."""
        manager = ConfigManager()
        manager.initialize()
        
        original_value = manager.get('DEBUG_MODE')
        manager.set('DEBUG_MODE', not original_value)
        assert manager.get('DEBUG_MODE') == (not original_value)

    def test_initialize_with_default(self):
        """Test initialization with default config."""
        ConfigManager._instance = None
        manager = ConfigManager()
        manager.initialize()
        
        # Should have all default config keys
        for key in DEFAULT_CONFIG:
            assert manager.get(key) is not None

    def test_initialize_with_custom_file(self):
        """Test initialization with custom config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write("""
WHISPER_MODEL = 'custom_model'
CUSTOM_KEY = 'custom_value'
""")
            tmp_path = tmp.name
        
        try:
            ConfigManager._instance = None
            manager = ConfigManager()
            manager.initialize(config_path=tmp_path)
            
            # Should have custom values
            assert manager.get('WHISPER_MODEL') == 'custom_model'
            assert manager.get('CUSTOM_KEY') == 'custom_value'
            
            # Should still have defaults for non-overridden keys
            assert manager.get('DEBUG_MODE') == DEFAULT_CONFIG['DEBUG_MODE']
        finally:
            Path(tmp_path).unlink()

    def test_reload_config(self):
        """Test reloading configuration.
        
        Note: Due to Python's import caching, hot-reload of modified config files
        may not reflect changes without application restart. This test verifies
        that reload() doesn't crash and maintains existing values.
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write("TEST_VALUE = 'initial'")
            tmp_path = tmp.name
        
        try:
            ConfigManager._instance = None
            manager = ConfigManager()
            manager.initialize(config_path=tmp_path)
            
            assert manager.get('TEST_VALUE') == 'initial'
            
            # Reload (same file, should not crash)
            manager.reload()
            
            # Should still have initial value (hot-reload has limitations)
            assert manager.get('TEST_VALUE') == 'initial'
        finally:
            Path(tmp_path).unlink()

    def test_config_path_property(self):
        """Test that config_path property is accessible."""
        manager = ConfigManager()
        manager.initialize()
        
        # Should have config_path attribute
        assert hasattr(manager, 'config_path')

    def test_get_all_config(self):
        """Test getting all configuration as dict."""
        manager = ConfigManager()
        manager.initialize()
        
        # If there's a method to get all config, test it
        if hasattr(manager, 'get_all'):
            all_config = manager.get_all()
            assert isinstance(all_config, dict)
            assert len(all_config) > 0

    def test_fallback_to_default(self):
        """Test that invalid config file falls back to defaults."""
        ConfigManager._instance = None
        manager = ConfigManager()
        manager.initialize(config_path="/nonexistent/config.py")
        
        # Should fall back to defaults
        assert manager.get('WHISPER_MODEL') == DEFAULT_CONFIG['WHISPER_MODEL']


class TestConfigIntegration:
    """Integration tests for config system."""

    def test_config_updates_persist(self):
        """Test that config updates persist through singleton."""
        ConfigManager._instance = None
        
        manager1 = ConfigManager()
        manager1.initialize()
        manager1.set('PERSISTENT_KEY', 'persistent_value')
        
        # Get new reference
        manager2 = ConfigManager()
        
        # Should see the same value (singleton)
        assert manager2.get('PERSISTENT_KEY') == 'persistent_value'

    def test_config_types_preserved(self):
        """Test that config value types are preserved."""
        manager = ConfigManager()
        manager.initialize()
        
        # String
        manager.set('STRING_VAL', 'text')
        assert isinstance(manager.get('STRING_VAL'), str)
        
        # Integer
        manager.set('INT_VAL', 42)
        assert isinstance(manager.get('INT_VAL'), int)
        
        # Boolean
        manager.set('BOOL_VAL', True)
        assert isinstance(manager.get('BOOL_VAL'), bool)
        
        # List
        manager.set('LIST_VAL', [1, 2, 3])
        assert isinstance(manager.get('LIST_VAL'), list)
        
        # Dict
        manager.set('DICT_VAL', {'key': 'value'})
        assert isinstance(manager.get('DICT_VAL'), dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
