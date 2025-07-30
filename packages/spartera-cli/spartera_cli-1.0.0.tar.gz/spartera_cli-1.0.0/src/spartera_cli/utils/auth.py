"""
Authentication utilities for Spartera CLI.
"""
import keyring
from typing import Optional

SERVICE_NAME = "spartera-cli"
API_KEY_USERNAME = "api-key"

def save_api_key(api_key: str):
    """Save API key securely."""
    try:
        keyring.set_password(SERVICE_NAME, API_KEY_USERNAME, api_key)
    except Exception:
        # Fallback to config file if keyring fails
        from .config import set_setting
        set_setting("api_key", api_key)

def get_api_key() -> Optional[str]:
    """Get stored API key."""
    try:
        return keyring.get_password(SERVICE_NAME, API_KEY_USERNAME)
    except Exception:
        # Fallback to config file
        from .config import get_setting
        return get_setting("api_key")

def clear_auth():
    """Clear stored authentication."""
    try:
        keyring.delete_password(SERVICE_NAME, API_KEY_USERNAME)
    except Exception:
        pass
    
    # Also clear from config
    from .config import get_config, save_config
    config = get_config()
    config.pop("api_key", None)
    config.pop("company_id", None)
    config.pop("user_id", None)
    config.pop("email", None)
    save_config(config)
