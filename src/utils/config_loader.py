import os
import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / 'config'
        self._config_cache = {}

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load and parse a YAML file"""
        if filename in self._config_cache:
            return self._config_cache[filename]

        file_path = self.config_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file {filename} not found")

        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            self._config_cache[filename] = config
            return config

    def get_prompts_config(self) -> Dict[str, Any]:
        """Get prompts configuration"""
        return self._load_yaml('prompts.yaml')

# Create a singleton instance
config_loader = ConfigLoader() 