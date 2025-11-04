"""
Configuration loading utilities.

This module provides a centralized way to load and manage application configuration
following the Factory pattern for creating configuration objects.
"""

import sys
import json
import importlib.util
from pathlib import Path
from typing import Any, Dict
from .constants import DEFAULT_CONFIG


class ConfigLoader:
    """
    Factory class for loading configuration from file or using defaults.
    
    Implements the Factory pattern to create configuration objects.
    """
    
    @staticmethod
    def resolve_project_root() -> Path:
        """
        Resolve the project root directory.
        
        Returns:
            Path: The project root directory (handles both frozen and development modes)
        """
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parents[2]
    
    @staticmethod
    def load_config(config_path: Path) -> Any:
        """
        Load configuration from file or return default config object.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Configuration module or fallback object with default values
        """
        try:
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
            
            spec = importlib.util.spec_from_file_location("config", config_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules['config'] = module
                spec.loader.exec_module(module)
                print(f"✅ Configuration loaded from {config_path}")
                return module
            
            raise ImportError(f"Cannot create module spec for {config_path}")
            
        except Exception as exc:
            print(f"⚠️ Warning: Using default configuration ({exc})", file=sys.stderr)
            return ConfigLoader._create_fallback_config()
    
    @staticmethod
    def _create_fallback_config() -> Any:
        """
        Create a fallback configuration object with default values.
        
        Returns:
            Object with default configuration attributes
        """
        class FallbackConfig:
            pass
        
        fallback = FallbackConfig()
        for key, value in DEFAULT_CONFIG.items():
            setattr(fallback, key, value)
        
        return fallback
    
    @staticmethod
    def get_config_value(config: Any, key: str, default: Any = None) -> Any:
        """
        Safely get configuration value with fallback.
        
        Args:
            config: Configuration object
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return getattr(config, key, default if default is not None else DEFAULT_CONFIG.get(key))


class ConfigManager:
    """
    Manages configuration state and provides access to configuration values.
    
    Implements Singleton-like behavior for configuration management.
    """
    
    _instance = None
    _config = None
    _config_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, config_path: Path = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to configuration file (defaults to .config/config.py)
        """
        if config_path is None:
            config_path = ConfigLoader.resolve_project_root() / ".config" / "config.py"
        
        self._config_path = config_path
        self._config = ConfigLoader.load_config(config_path)
        
        # Load runtime settings (theme, etc.)
        self.load_runtime_settings()
    
    def reload(self):
        """Reload configuration from file."""
        if self._config_path:
            self._config = ConfigLoader.load_config(self._config_path)
            self.load_runtime_settings()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        if self._config is None:
            self.initialize()
        return ConfigLoader.get_config_value(self._config, key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value (runtime only, not persisted).
        
        Args:
            key: Configuration key
            value: New value
        """
        if self._config is None:
            self.initialize()
        setattr(self._config, key, value)
    
    def save_config_to_file(self, config_obj=None):
        """
        Save runtime configuration preferences to a separate settings file.
        
        This saves UI preferences (like theme mode) to .config/settings.json
        without modifying the main config.py file, preserving user comments.
        
        Args:
            config_obj: Configuration object to save (uses self._config if None)
        """
        if config_obj is None:
            config_obj = self._config
        
        if config_obj is None or self._config_path is None:
            return
        
        # Settings file path (next to config.py)
        settings_file = self._config_path.parent / "settings.json"
        
        # Extract runtime preferences to save
        runtime_settings = {}
        
        # Save theme mode if it exists
        if hasattr(config_obj, 'THEME_MODE'):
            runtime_settings['THEME_MODE'] = config_obj.THEME_MODE
        
        # Save other runtime preferences here as needed
        
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(runtime_settings, f, indent=2)
        except Exception as e:
            # Silent fail - don't break the app if we can't save settings
            print(f"Warning: Could not save settings to {settings_file}: {e}", file=sys.stderr)
    
    def load_runtime_settings(self):
        """
        Load runtime settings from .config/settings.json and apply to config.
        
        This is called during initialization to restore UI preferences.
        """
        if self._config_path is None:
            return
        
        settings_file = self._config_path.parent / "settings.json"
        
        if not settings_file.exists():
            return
        
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Apply runtime settings to config object
            for key, value in settings.items():
                setattr(self._config, key, value)
        except Exception as e:
            print(f"Warning: Could not load settings from {settings_file}: {e}", file=sys.stderr)
    
    @property
    def config(self):
        """Get the raw configuration object."""
        if self._config is None:
            self.initialize()
        return self._config
    
    @property
    def config_path(self):
        """Get the configuration file path."""
        if self._config_path is None:
            self.initialize()
        return self._config_path
