"""
Configuration loading utilities.

This module provides a centralized way to load and manage application configuration
following the Factory pattern for creating configuration objects.
"""

import sys
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
    
    def reload(self):
        """Reload configuration from file."""
        if self._config_path:
            self._config = ConfigLoader.load_config(self._config_path)
    
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
    
    @property
    def config(self):
        """Get the raw configuration object."""
        if self._config is None:
            self.initialize()
        return self._config
