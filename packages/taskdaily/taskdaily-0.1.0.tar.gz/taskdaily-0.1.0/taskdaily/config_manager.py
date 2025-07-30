import os
import yaml
from pathlib import Path
from typing import Dict, Any
import shutil

DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent / "templates"
USER_CONFIG_DIR = Path.home() / ".config" / "daily-task"
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.yaml"
USER_TEMPLATE_FILE = USER_CONFIG_DIR / "daily_template.md"

def ensure_user_config_exists():
    """Ensure user config directory exists and has necessary files."""
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copy default config if user config doesn't exist
    if not USER_CONFIG_FILE.exists():
        shutil.copy2(DEFAULT_CONFIG_DIR / "config.yaml", USER_CONFIG_FILE)
    
    # Copy default template if user template doesn't exist
    if not USER_TEMPLATE_FILE.exists():
        shutil.copy2(DEFAULT_CONFIG_DIR / "daily_template.md", USER_TEMPLATE_FILE)

def load_default_config() -> Dict[str, Any]:
    """Load default configuration from package."""
    with open(DEFAULT_CONFIG_DIR / "config.yaml", 'r') as f:
        return yaml.safe_load(f)

def load_user_config() -> Dict[str, Any]:
    """Load user configuration, create if doesn't exist."""
    ensure_user_config_exists()
    with open(USER_CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def merge_configs(default_config: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge configurations, with user config taking precedence."""
    merged = default_config.copy()
    
    for key, value in user_config.items():
        if (
            key in merged and 
            isinstance(merged[key], dict) and 
            isinstance(value, dict)
        ):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged

def get_config() -> Dict[str, Any]:
    """Get merged configuration with user preferences."""
    default_config = load_default_config()
    user_config = load_user_config()
    return merge_configs(default_config, user_config)

def get_template_path() -> Path:
    """Get path to the template file, preferring user template."""
    ensure_user_config_exists()
    return USER_TEMPLATE_FILE

def update_user_config(config: Dict[str, Any]) -> None:
    """Update user configuration file."""
    ensure_user_config_exists()
    with open(USER_CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

def reset_to_defaults() -> None:
    """Reset user configuration to package defaults."""
    ensure_user_config_exists()
    shutil.copy2(DEFAULT_CONFIG_DIR / "config.yaml", USER_CONFIG_FILE)
    shutil.copy2(DEFAULT_CONFIG_DIR / "daily_template.md", USER_TEMPLATE_FILE) 