"""
Enhanced encoding utilities for reading files from ESL student environments.

This module provides robust encoding detection and fallback mechanisms
to handle files created in various international environments.
"""

import logging
import os
from typing import Tuple, Optional, List

logger = logging.getLogger(__name__)


def try_multiple_encodings(file_path: str, content_type: str = "text") -> Tuple[Optional[str], Optional[str]]:
    """
    Try multiple encodings to read a file, optimized for ESL student environments.
    
    Args:
        file_path: Path to the file to read
        content_type: Type hint for logging (e.g., "text", "code", "markdown", "json")
    
    Returns:
        Tuple of (content, encoding_used) or (None, None) if all attempts fail
    """
    # Common encodings used by ESL students, ordered by likelihood of success
    encodings = _get_encoding_priority_list(content_type)
    
    errors_encountered = []
    
    # First pass: Try strict decoding
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='strict') as file:
                content = file.read()
                if content.strip():  # Only return non-empty content
                    logger.debug(f"Successfully read {file_path} with encoding: {encoding}")
                    return content, encoding
        except UnicodeDecodeError as e:
            errors_encountered.append(f"{encoding}: {str(e)[:100]}")
            continue
        except Exception as e:
            errors_encountered.append(f"{encoding}: {str(e)[:100]}")
            continue
    
    # Second pass: Try with error handling for the most common encodings
    fallback_strategies = [
        ('utf-8', 'ignore'),
        ('latin-1', 'ignore'),
        ('cp1252', 'ignore')
    ]
    
    for encoding, error_strategy in fallback_strategies:
        try:
            with open(file_path, 'r', encoding=encoding, errors=error_strategy) as file:
                content = file.read()
                if content.strip():
                    logger.warning(f"Read {file_path} with {encoding} using '{error_strategy}' error handling - some characters may be lost")
                    return content, f"{encoding} (with errors={error_strategy})"
        except Exception as e:
            errors_encountered.append(f"{encoding} ({error_strategy}): {str(e)[:100]}")
    
    # Log all attempted encodings for debugging
    logger.error(f"Failed to read {file_path} with any encoding. Attempts made:")
    for error in errors_encountered:
        logger.error(f"  - {error}")
    
    return None, None


def _get_encoding_priority_list(content_type: str) -> List[str]:
    """
    Get prioritized encoding list based on content type and ESL student usage patterns.
    
    Args:
        content_type: Type of content being read (text, code, json, markdown, etc.)
    
    Returns:
        List of encodings in priority order
    """
    # Base encodings common across all content types
    base_encodings = [
        'utf-8',           # Most common modern encoding
        'utf-16',          # Windows systems with non-English locales, Office products
        'cp1252',          # Windows-1252: Western European, legacy Windows, regional Office
        'latin-1',         # ISO-8859-1: European systems, older editors, web platforms
        'utf-8-sig',       # UTF-8 with BOM (Byte Order Mark)
    ]
    
    # Additional encodings based on content type
    if content_type in ['json', 'notebook']:
        # JSON/Jupyter notebooks - common in programming environments
        additional = [
            'utf-16le',        # Little-endian UTF-16 (Windows default)
            'utf-16be',        # Big-endian UTF-16
        ]
    elif content_type in ['code', 'python']:
        # Source code files - often saved in various IDE encodings
        additional = [
            'utf-16le',        # Windows IDEs
            'cp1251',          # Cyrillic programming environments
        ]
    else:
        # Text, markdown, and other content
        additional = [
            'utf-16le',        # Little-endian UTF-16 (Windows default)
            'utf-16be',        # Big-endian UTF-16
        ]
    
    # Regional encodings for international ESL students
    regional_encodings = [
        'cp1251',          # Cyrillic (Russian, Bulgarian, etc.)
        'cp1254',          # Turkish
        'cp1250',          # Central European (Polish, Czech, Hungarian)
        'gb2312',          # Simplified Chinese
        'big5',            # Traditional Chinese
        'shift_jis',       # Japanese
        'euc-kr',          # Korean
        'iso-8859-15',     # Latin-9 (includes Euro symbol)
        'iso-8859-2',      # Central European
        'iso-8859-5',      # Cyrillic
        'ascii'            # Last resort
    ]
    
    return base_encodings + additional + regional_encodings


def safe_read_text_file(file_path: str, content_type: str = "text") -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Safely read a text file with comprehensive encoding detection and error reporting.
    
    Args:
        file_path: Path to the file to read
        content_type: Type hint for encoding optimization
    
    Returns:
        Tuple of (content, encoding_used, error_message)
        - If successful: (content, encoding, None)
        - If failed: (None, None, error_message)
    """
    if not os.path.exists(file_path):
        return None, None, f"File not found: {file_path}"
    
    if not os.path.isfile(file_path):
        return None, None, f"Path is not a file: {file_path}"
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return "", "utf-8", None  # Empty file is valid
        
        # Try to read with multiple encodings
        content, encoding_used = try_multiple_encodings(file_path, content_type)
        
        if content is not None:
            return content, encoding_used, None
        else:
            return None, None, f"Could not read file with any supported encoding: {os.path.basename(file_path)}"
    
    except Exception as e:
        return None, None, f"Unexpected error reading file: {str(e)}"


def create_encoding_error_message(file_path: str, content_type: str = "text") -> str:
    """
    Create a standardized error message for encoding failures.
    
    Args:
        file_path: Path to the file that failed
        content_type: Type of content that was being read
    
    Returns:
        Formatted error message for inclusion in extraction results
    """
    return f"[ENCODING ERROR] Could not read {content_type} file with any supported encoding: {os.path.basename(file_path)}"


def get_encoding_info() -> dict:
    """
    Get information about the encoding detection capabilities.
    
    Returns:
        Dictionary with encoding support information
    """
    return {
        'supported_encodings': _get_encoding_priority_list("text"),
        'esl_optimized': True,
        'fallback_strategies': ['ignore', 'replace'],
        'content_type_optimization': True
    }


def detect_encoding(file_path: str) -> Optional[str]:
    """
    Simple wrapper to detect file encoding.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Detected encoding or None if detection fails
    """
    content, encoding = try_multiple_encodings(file_path)
    return encoding