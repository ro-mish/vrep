import os
import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from yaml files"""
        config_dir = Path(__file__).parent
        
        # Load default config
        default_config_path = config_dir / 'default_config.yaml'
        with open(default_config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Load local config if it exists (overrides defaults)
        local_config_path = config_dir / 'local_config.yaml'
        if local_config_path.exists():
            with open(local_config_path, 'r') as f:
                local_config = yaml.safe_load(f)
                self._deep_update(self.config, local_config)

    def _deep_update(self, d: Dict, u: Dict) -> Dict:
        """Recursively update nested dictionaries"""
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._deep_update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def get_network_options(self) -> Dict[str, Any]:
        """Get network initialization options"""
        return self.config['visualization']['network']

    def get_node_config(self) -> Dict[str, Any]:
        """Get node visualization options"""
        return self.config['visualization']['nodes']

    def get_edge_config(self) -> Dict[str, Any]:
        """Get edge visualization options"""
        return self.config['visualization']['edges']

    def get_physics_options(self) -> Dict[str, Any]:
        """Get physics simulation options"""
        return self.config['visualization']['physics']

    def get_interaction_options(self) -> Dict[str, Any]:
        """Get interaction options"""
        return self.config['visualization']['interaction']

    def get_layout_options(self) -> Dict[str, Any]:
        """Get layout options"""
        return self.config['visualization']['layout'] 