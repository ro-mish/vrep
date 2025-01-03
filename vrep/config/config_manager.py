import os
from pathlib import Path
import yaml

class ConfigManager:
    def __init__(self, config_path: str = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path (str, optional): Path to custom configuration file
        """
        self.config_path = config_path
        self.default_config_path = os.path.join(
            os.path.dirname(__file__), 
            'default_config.yaml'
        )

    def get_config(self) -> dict:
        """
        Load and return configuration, merging default and custom configs if needed.
        
        Returns:
            dict: Configuration dictionary
        """
        # Load default config
        with open(self.default_config_path, 'r') as f:
            config = yaml.safe_load(f)

        # If custom config provided, merge it with default
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                custom_config = yaml.safe_load(f)
                config.update(custom_config)

        return config 