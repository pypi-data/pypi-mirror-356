"""
Configuration utilities for financial document processing applications.

This module provides functions for loading and managing configuration from YAML files.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from pydantic import BaseModel


def load_config(
    config_path: Union[str, Path], 
    default_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        default_config: Optional default configuration to use if file doesn't exist
        
    Returns:
        Dictionary containing the configuration
        
    Raises:
        FileNotFoundError: If the config file doesn't exist and no default is provided
        yaml.YAMLError: If the YAML file is invalid
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        if default_config is not None:
            return default_config
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_config(config: Dict[str, Any], config_path: Union[str, Path]) -> None:
    """
    Save configuration to a YAML file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path to save the YAML configuration file
        
    Raises:
        yaml.YAMLError: If the configuration cannot be serialized to YAML
    """
    config_path = Path(config_path)
    
    # Create directory if it doesn't exist
    os.makedirs(config_path.parent, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False)


class ConfigModel(BaseModel):
    """Base class for configuration models with YAML loading/saving capabilities."""
    
    @classmethod
    def from_yaml(cls, config_path: Union[str, Path]):
        """Load configuration from YAML file and create model instance."""
        config = load_config(config_path)
        return cls(**config)
    
    def to_yaml(self, config_path: Union[str, Path]) -> None:
        """Save configuration model to YAML file."""
        save_config(self.model_dump(), config_path)
