"""
Logging utilities for financial document processing applications.

This module provides standardized logging configuration and helper functions.
"""

import logging
import os
import sys
from typing import Optional, Union


def get_logger(
    name: str, 
    level: Union[int, str] = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: The name of the logger
        level: The logging level (default: INFO)
        log_file: Optional path to log file
        log_format: Optional custom log format
        
    Returns:
        A configured logger instance
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()
    
    # Default format
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
