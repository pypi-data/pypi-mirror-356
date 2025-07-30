"""
MarkMate Configuration Settings

Default configuration and settings management.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "processing": {
        "max_file_size_mb": 100,
        "supported_encodings": [
            "utf-8", "utf-16", "utf-16-le", "utf-16-be",
            "cp1252", "latin-1", "ascii",
            "cp1251", "cp1254", "iso-8859-1", "iso-8859-2",
            "gb2312", "big5", "shift_jis", "euc-kr"
        ],
        "mac_system_files": [
            ".DS_Store", "._", "__MACOSX", ".Spotlight-V100",
            ".Trashes", ".TemporaryItems", ".fseventsd"
        ]
    },
    "extraction": {
        "timeout_seconds": 300,
        "github_clone_timeout": 120,
        "max_commit_analysis": 100
    },
    "grading": {
        "claude_model": "claude-3-5-sonnet-20241022",
        "openai_model": "gpt-4o",
        "temperature": 0.1,
        "max_tokens": 2000,
        "timeout_seconds": 60
    },
    "cli": {
        "default_output_dir": "processed_submissions",
        "default_extracted_file": "extracted_content.json",
        "default_grading_file": "grading_results.json",
        "default_github_urls_file": "github_urls.txt"
    }
}


class Config:
    """Configuration manager for MarkMate."""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config_dict: Custom configuration dictionary
        """
        self._config = DEFAULT_CONFIG.copy()
        if config_dict:
            self._merge_config(config_dict)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated key path.
        
        Args:
            key_path: Dot-separated path (e.g., "processing.max_file_size_mb")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split(".")
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value by dot-separated key path.
        
        Args:
            key_path: Dot-separated path
            value: Value to set
        """
        keys = key_path.split(".")
        config = self._config
        
        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
    
    def _merge_config(self, custom_config: Dict[str, Any]) -> None:
        """Merge custom configuration with default."""
        def merge_dict(base: Dict, custom: Dict) -> Dict:
            for key, value in custom.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
            return base
        
        merge_dict(self._config, custom_config)
    
    @property
    def processing(self) -> Dict[str, Any]:
        """Get processing configuration."""
        return self._config["processing"]
    
    @property
    def extraction(self) -> Dict[str, Any]:
        """Get extraction configuration."""
        return self._config["extraction"]
    
    @property
    def grading(self) -> Dict[str, Any]:
        """Get grading configuration."""
        return self._config["grading"]
    
    @property
    def cli(self) -> Dict[str, Any]:
        """Get CLI configuration."""
        return self._config["cli"]


# Global configuration instance
config = Config()


def load_config_file(config_path: str) -> Config:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to configuration file (JSON or YAML)
        
    Returns:
        Config instance
    """
    import json
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.suffix.lower() in ['.yml', '.yaml']:
            try:
                import yaml
                custom_config = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML required for YAML configuration files")
        else:
            custom_config = json.load(f)
    
    return Config(custom_config)


def get_api_keys() -> Dict[str, Optional[str]]:
    """
    Get API keys from environment variables.
    
    Returns:
        Dictionary of API keys
    """
    return {
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY")
    }


def validate_api_keys(required_providers: list) -> Dict[str, bool]:
    """
    Validate that required API keys are available.
    
    Args:
        required_providers: List of required providers
        
    Returns:
        Dictionary indicating which providers are available
    """
    api_keys = get_api_keys()
    
    availability = {}
    for provider in required_providers:
        if provider == "claude":
            availability["claude"] = bool(api_keys["anthropic"])
        elif provider == "openai":
            availability["openai"] = bool(api_keys["openai"])
        else:
            availability[provider] = False
    
    return availability