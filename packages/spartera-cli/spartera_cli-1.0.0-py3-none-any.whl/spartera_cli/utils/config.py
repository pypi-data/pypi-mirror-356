"""
Configuration management for Spartera CLI.
"""
import json
from pathlib import Path
from typing import Dict, Any

def get_config_dir() -> Path:
    """Get CLI configuration directory."""
    config_dir = Path.home() / ".spartera"
    config_dir.mkdir(exist_ok=True)
    return config_dir

def get_config_file() -> Path:
    """Get configuration file path."""
    return get_config_dir() / "config.json"

def get_config() -> Dict[str, Any]:
    """Load configuration from file."""
    config_file = get_config_file()
    
    if not config_file.exists():
        return {}
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_config(config: Dict[str, Any]):
    """Save configuration to file."""
    config_file = get_config_file()
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific setting."""
    config = get_config()
    return config.get(key, default)

def set_setting(key: str, value: Any):
    """Set a specific setting."""
    config = get_config()
    config[key] = value
    save_config(config)
