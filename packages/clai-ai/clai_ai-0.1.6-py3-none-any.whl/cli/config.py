import os
import json
from pathlib import Path
from typing import Dict, Optional

class ConfigManager:
    """Manages Clay configuration (API keys, settings, etc.)"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".clai"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(exist_ok=True)
        
        # Set proper permissions (readable only by user)
        os.chmod(self.config_dir, 0o700)
    
    def get_config(self) -> Dict:
        """Get current configuration"""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def save_config(self, config: Dict):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set proper permissions (readable only by user)
        os.chmod(self.config_file, 0o600)
    
    def get_api_key(self) -> Optional[str]:
        """Get Gemini API key"""
        config = self.get_config()
        return config.get('api_key')
    
    def set_api_key(self, api_key: str):
        """Set Gemini API key"""
        config = self.get_config()
        config['api_key'] = api_key.strip()
        self.save_config(config)
    
    def get_setting(self, key: str, default=None):
        """Get a specific setting"""
        config = self.get_config()
        return config.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set a specific setting"""
        config = self.get_config()
        config[key] = value
        self.save_config(config)
