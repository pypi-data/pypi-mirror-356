"""
Configuration loader for the Packet Capture Module.
"""
import os
import yaml
from typing import Dict, Any


class ConfigLoader:
    """Load and provide access to configuration settings."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the config loader.
        
        Args:
            config_path: Path to the YAML config file
        """
        self.config: Dict[str, Any] = {}
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "config", 
            "config.yaml"
        )
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = yaml.safe_load(config_file)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}")
            self.config = {}
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            self.config = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: The configuration key (can use dot notation for nested keys)
            default: Default value if key is not found
            
        Returns:
            The configuration value or default
        """
        parts = key.split('.')
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def get_multicast_config(self) -> Dict[str, Any]:
        """Get multicast-specific configuration."""
        return self.config.get("multicast", {})
    
    def get_filter_config(self) -> Dict[str, Any]:
        """Get filter-specific configuration."""
        return self.config.get("filter", {})
    
    def get_buffer_config(self) -> Dict[str, Any]:
        """Get buffer-specific configuration."""
        return self.config.get("buffer", {})


# Singleton instance
config = ConfigLoader()