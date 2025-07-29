"""
Helper functions for financial document processing applications.

This module provides various utility functions for common operations.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


def normalize_amount(amount_str: str) -> float:
    """
    Normalize a monetary amount string to a float.
    
    Args:
        amount_str: String representation of a monetary amount
        
    Returns:
        Normalized float value
        
    Examples:
        >>> normalize_amount("1,234.56")
        1234.56
        >>> normalize_amount("1.234,56")
        1234.56
        >>> normalize_amount("1 234,56")
        1234.56
    """
    if not amount_str:
        return 0.0
    
    # Remove currency symbols and whitespace
    amount_str = re.sub(r'[$€£¥]|\s', '', amount_str)
    
    # Handle different decimal/thousand separators
    if ',' in amount_str and '.' in amount_str:
        if amount_str.find(',') < amount_str.find('.'):  # Format: 1,234.56
            amount_str = amount_str.replace(',', '')
        else:  # Format: 1.234,56
            amount_str = amount_str.replace('.', '').replace(',', '.')
    elif ',' in amount_str:
        # Check if comma is used as decimal separator (e.g., 1234,56)
        if re.search(r'\d,\d{2}$', amount_str):
            amount_str = amount_str.replace(',', '.')
        else:
            amount_str = amount_str.replace(',', '')
    
    try:
        return float(amount_str)
    except ValueError:
        return 0.0


def extract_currency(text: str) -> str:
    """
    Extract currency symbol from text.
    
    Args:
        text: Text containing a currency symbol
        
    Returns:
        Currency symbol or empty string if not found
    """
    currency_symbols = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        'zł': 'PLN',
        'PLN': 'PLN',
        'EUR': 'EUR',
        'USD': 'USD',
    }
    
    for symbol, code in currency_symbols.items():
        if symbol in text:
            return code
    
    return ""


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path object for the directory
    """
    path = Path(path)
    os.makedirs(path, exist_ok=True)
    return path


def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Get the extension of a file (lowercase, without the dot).
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension (e.g., "pdf", "json")
    """
    return Path(file_path).suffix.lower().lstrip('.')


def parse_date(
    date_str: str, 
    formats: Optional[List[str]] = None,
    default: Optional[datetime] = None
) -> Optional[datetime]:
    """
    Parse a date string using multiple possible formats.
    
    Args:
        date_str: String representation of a date
        formats: List of date formats to try
        default: Default value to return if parsing fails
        
    Returns:
        Parsed datetime object or default if parsing fails
    """
    if not date_str:
        return default
    
    if formats is None:
        formats = [
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%d.%m.%Y',
            '%Y/%m/%d',
            '%b %d, %Y',
            '%d %b %Y',
            '%d %B %Y',
            '%B %d, %Y',
        ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    return default


def is_valid_amount(amount: float, min_value: float = 0.0, max_value: float = 1e9) -> bool:
    """
    Check if an amount is valid (within reasonable bounds).
    
    Args:
        amount: Amount to check
        min_value: Minimum valid value
        max_value: Maximum valid value
        
    Returns:
        True if the amount is valid, False otherwise
    """
    return min_value <= amount <= max_value and not (amount == 0.0)
