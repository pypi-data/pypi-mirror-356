"""
Date utility functions for financial document processing.

This module provides specialized date parsing and formatting functions
commonly needed when processing financial documents.
"""

import re
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Union

# Common date formats by locale
DATE_FORMATS = {
    "en": ["%m/%d/%Y", "%m-%d-%Y", "%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y"],
    "de": ["%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y"],
    "fr": ["%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%d %b %Y"],
    "pl": ["%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y"],
    "es": ["%d/%m/%Y", "%d-%m-%Y", "%d de %B de %Y"],
}

# Month names in different languages
MONTH_NAMES = {
    "en": {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
    },
    "de": {
        "jan": 1, "feb": 2, "mär": 3, "apr": 4, "mai": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dez": 12,
        "januar": 1, "februar": 2, "märz": 3, "april": 4, "mai": 5, "juni": 6,
        "juli": 7, "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12
    },
    "fr": {
        "janv": 1, "févr": 2, "mars": 3, "avr": 4, "mai": 5, "juin": 6,
        "juil": 7, "août": 8, "sept": 9, "oct": 10, "nov": 11, "déc": 12,
        "janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
        "juillet": 7, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12
    },
    "pl": {
        "sty": 1, "lut": 2, "mar": 3, "kwi": 4, "maj": 5, "cze": 6,
        "lip": 7, "sie": 8, "wrz": 9, "paź": 10, "lis": 11, "gru": 12,
        "styczeń": 1, "luty": 2, "marzec": 3, "kwiecień": 4, "maj": 5, "czerwiec": 6,
        "lipiec": 7, "sierpień": 8, "wrzesień": 9, "październik": 10, "listopad": 11, "grudzień": 12
    },
    "es": {
        "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
        "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12,
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
}


def parse_date_multilingual(
    date_str: str, 
    languages: Optional[List[str]] = None,
    default: Optional[datetime] = None
) -> Optional[datetime]:
    """
    Parse a date string using formats from multiple languages.
    
    Args:
        date_str: String representation of a date
        languages: List of language codes to try (default: ["en", "de", "fr", "pl", "es"])
        default: Default value to return if parsing fails
        
    Returns:
        Parsed datetime object or default if parsing fails
    """
    if not date_str:
        return default
    
    if languages is None:
        languages = ["en", "de", "fr", "pl", "es"]
    
    # Try standard formats for each language
    formats = []
    for lang in languages:
        if lang in DATE_FORMATS:
            formats.extend(DATE_FORMATS[lang])
    
    # Add ISO format which is language-independent
    formats.append("%Y-%m-%d")
    
    # Try each format
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    # Try custom parsing for text dates
    result = parse_text_date(date_str, languages)
    if result:
        return result
    
    return default


def parse_text_date(date_str: str, languages: List[str]) -> Optional[datetime]:
    """
    Parse a date that might be in text format (e.g., "12 January 2023").
    
    Args:
        date_str: String representation of a date
        languages: List of language codes to try
        
    Returns:
        Parsed datetime object or None if parsing fails
    """
    date_str = date_str.lower()
    
    # Extract potential day, month, year
    day_match = re.search(r'\b(\d{1,2})\b', date_str)
    year_match = re.search(r'\b(20\d{2}|19\d{2})\b', date_str)
    
    if not (day_match and year_match):
        return None
    
    day = int(day_match.group(1))
    year = int(year_match.group(1))
    
    # Find month name in different languages
    for lang in languages:
        if lang not in MONTH_NAMES:
            continue
            
        for month_name, month_num in MONTH_NAMES[lang].items():
            if month_name in date_str.lower():
                # Validate date components
                if 1 <= day <= 31 and 1 <= month_num <= 12:
                    try:
                        return datetime(year, month_num, day)
                    except ValueError:
                        # Invalid date (e.g., February 30)
                        continue
    
    return None


def format_date(
    dt: Union[datetime, date], 
    fmt: str = "%Y-%m-%d",
    locale: str = "en"
) -> str:
    """
    Format a date according to the specified format and locale.
    
    Args:
        dt: Date or datetime object
        fmt: Format string (default: ISO format)
        locale: Locale code (default: "en")
        
    Returns:
        Formatted date string
    """
    if isinstance(dt, datetime):
        return dt.strftime(fmt)
    elif isinstance(dt, date):
        return dt.strftime(fmt)
    return ""


def is_valid_date(
    dt: Union[datetime, date],
    min_date: Optional[Union[datetime, date]] = None,
    max_date: Optional[Union[datetime, date]] = None
) -> bool:
    """
    Check if a date is valid (within reasonable bounds).
    
    Args:
        dt: Date to check
        min_date: Minimum valid date
        max_date: Maximum valid date
        
    Returns:
        True if the date is valid, False otherwise
    """
    if min_date is None:
        min_date = datetime(1900, 1, 1)
    
    if max_date is None:
        max_date = datetime.now()
    
    if isinstance(dt, date) and not isinstance(dt, datetime):
        if isinstance(min_date, datetime):
            min_date = min_date.date()
        if isinstance(max_date, datetime):
            max_date = max_date.date()
    
    return min_date <= dt <= max_date
