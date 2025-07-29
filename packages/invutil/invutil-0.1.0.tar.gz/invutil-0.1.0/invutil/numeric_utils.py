"""
Numeric utility functions for financial document processing.

This module provides specialized numeric parsing and formatting functions
commonly needed when processing financial documents.
"""

import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple, Union


def parse_amount(amount_str: str) -> Optional[float]:
    """
    Parse a monetary amount from a string, handling various formats.
    
    Args:
        amount_str: String representation of a monetary amount
        
    Returns:
        Parsed float value or None if parsing fails
        
    Examples:
        >>> parse_amount("$1,234.56")
        1234.56
        >>> parse_amount("1.234,56 €")
        1234.56
        >>> parse_amount("1 234,56 zł")
        1234.56
    """
    if not amount_str:
        return None
    
    # Clean the string
    amount_str = amount_str.strip()
    
    # Remove currency symbols
    amount_str = re.sub(r'[$€£¥zł]', '', amount_str)
    
    # Remove whitespace
    amount_str = re.sub(r'\s', '', amount_str)
    
    # Handle different decimal/thousand separators
    if ',' in amount_str and '.' in amount_str:
        if amount_str.find(',') < amount_str.find('.'):  # Format: 1,234.56
            amount_str = amount_str.replace(',', '')
        else:  # Format: 1.234,56
            amount_str = amount_str.replace('.', '').replace(',', '.')
    elif ',' in amount_str:
        # Check if comma is used as decimal separator (e.g., 1234,56)
        if re.search(r'\d,\d{1,2}$', amount_str):
            amount_str = amount_str.replace(',', '.')
        else:
            amount_str = amount_str.replace(',', '')
    
    try:
        return float(amount_str)
    except ValueError:
        return None


def extract_currency(text: str) -> str:
    """
    Extract currency symbol or code from text.
    
    Args:
        text: Text containing a currency symbol or code
        
    Returns:
        Currency code (e.g., "USD", "EUR") or empty string if not found
    """
    # Map of currency symbols/codes to standardized codes
    currency_map = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        'zł': 'PLN',
        'PLN': 'PLN',
        'EUR': 'EUR',
        'USD': 'USD',
        'GBP': 'GBP',
        'JPY': 'JPY',
    }
    
    # Try to find currency symbols first (more specific)
    for symbol, code in currency_map.items():
        if symbol in text:
            return code
    
    return ""


def round_amount(amount: float, precision: int = 2) -> float:
    """
    Round a monetary amount to the specified precision using banker's rounding.
    
    Args:
        amount: Amount to round
        precision: Number of decimal places
        
    Returns:
        Rounded amount
    """
    if amount is None:
        return 0.0
    
    # Use Decimal for precise rounding
    decimal_amount = Decimal(str(amount))
    rounded = decimal_amount.quantize(Decimal('0.' + '0' * precision), rounding=ROUND_HALF_UP)
    return float(rounded)


def format_amount(
    amount: float,
    currency: Optional[str] = None,
    precision: int = 2,
    thousands_separator: str = ',',
    decimal_separator: str = '.'
) -> str:
    """
    Format a monetary amount with appropriate separators and currency symbol.
    
    Args:
        amount: Amount to format
        currency: Optional currency code
        precision: Number of decimal places
        thousands_separator: Character to use as thousands separator
        decimal_separator: Character to use as decimal separator
        
    Returns:
        Formatted amount string
    """
    if amount is None:
        return ""
    
    # Round the amount
    amount = round_amount(amount, precision)
    
    # Format the integer part with thousands separator
    integer_part = int(amount)
    integer_str = ""
    
    if integer_part == 0:
        integer_str = "0"
    else:
        while integer_part > 0:
            if integer_str:
                chunk = f"{integer_part % 1000:03d}"
                integer_str = chunk + thousands_separator + integer_str
            else:
                integer_str = f"{integer_part % 1000}"
            integer_part //= 1000
    
    # Format the decimal part
    decimal_part = int(round((amount - int(amount)) * (10 ** precision)))
    decimal_str = f"{decimal_part:0{precision}d}" if precision > 0 else ""
    
    # Combine parts
    result = integer_str
    if decimal_str:
        result += decimal_separator + decimal_str
    
    # Add currency symbol if provided
    currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'PLN': 'zł',
    }
    
    if currency:
        symbol = currency_symbols.get(currency, currency)
        if symbol in ['$', '£', '¥']:
            result = symbol + result
        else:
            result = result + ' ' + symbol
    
    return result


def calculate_percentage(
    part: float,
    total: float,
    default: float = 0.0
) -> float:
    """
    Calculate percentage of part relative to total.
    
    Args:
        part: The part value
        total: The total value
        default: Default value to return if calculation is not possible
        
    Returns:
        Percentage value (0-100)
    """
    if total == 0:
        return default
    
    return (part / total) * 100.0


def is_amount_within_tolerance(
    amount1: float,
    amount2: float,
    tolerance: float = 0.01,
    relative: bool = True
) -> bool:
    """
    Check if two amounts are within a specified tolerance of each other.
    
    Args:
        amount1: First amount
        amount2: Second amount
        tolerance: Tolerance value (default: 0.01)
        relative: If True, tolerance is relative to the larger amount
                 If False, tolerance is absolute
        
    Returns:
        True if amounts are within tolerance, False otherwise
    """
    if amount1 == amount2:
        return True
    
    if relative:
        base = max(abs(amount1), abs(amount2))
        if base == 0:
            return True
        relative_diff = abs(amount1 - amount2) / base
        return relative_diff <= tolerance
    else:
        return abs(amount1 - amount2) <= tolerance
