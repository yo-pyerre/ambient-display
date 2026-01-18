"""
Configuration Loader Module
Handles loading and managing application configuration
"""
import json
import os
from typing import Dict, Any

# Default configuration values
DEFAULT_CONFIG = {
    "image_duration": 30,
    "device_ip": "192.168.1.100",
    "paths": {
        "images": "cover art",
        "todos": "todos.txt"
    },
    "time_periods": {
        "day_start": "06:00",
        "night_start": "22:00"
    },
    "presence": {
        "scan_interval": 60,
        "scan_method": "ping"
    },
    "display": {
        "transition_duration": 1000,
        "poll_interval": 5000
    }
}

class ConfigLoader:
    """Manages application configuration."""

    def __init__(self, config_path: str = 'config/config.json'):
        """
        Initialize the configuration loader.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file, falling back to defaults if file doesn't exist.

        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_with_defaults(loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                return DEFAULT_CONFIG.copy()
        else:
            print(f"Config file not found at {self.config_path}. Using defaults.")
            return DEFAULT_CONFIG.copy()

    def _merge_with_defaults(self, loaded_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge loaded configuration with defaults to ensure all keys exist.

        Args:
            loaded_config: Configuration loaded from file

        Returns:
            Merged configuration
        """
        config = DEFAULT_CONFIG.copy()
        for key, value in loaded_config.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                config[key].update(value)
            else:
                config[key] = value
        return config

    def get(self, key: str = None) -> Any:
        """
        Get configuration value(s).

        Args:
            key: Configuration key (supports dot notation, e.g., 'paths.images')
                 If None, returns entire configuration

        Returns:
            Configuration value or entire config if key is None
        """
        if key is None:
            return self.config

        # Support dot notation for nested keys
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
        return value

    def reload(self) -> Dict[str, Any]:
        """
        Reload configuration from file.

        Returns:
            Reloaded configuration
        """
        self.config = self._load_config()
        return self.config

# Global configuration instance
_config_instance = None

def get_config() -> ConfigLoader:
    """
    Get the global configuration instance.

    Returns:
        ConfigLoader instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance
