"""
String utility functions for text processing and validation.

This module provides utility functions for common string operations
including digit extraction, character equality checking, and text cleaning.
"""

import re
import unicodedata
from typing import Sequence


def digits_only(raw_number: str) -> str:
    """
    Extract only digits from a string.

    Removes all non-digit characters from the input string, leaving
    only numeric characters (0-9).

    Args:
        raw_number: Input string that may contain digits and other characters

    Returns:
        String containing only the digit characters from the input

    Examples:
        >>> digits_only("123-456-789")
        "123456789"
        >>> digits_only("ABC123DEF")
        "123"
    """
    return re.sub(r"[^0-9]", "", raw_number)


def is_equal(words: Sequence[str]) -> bool:
    """
    Check if all characters in a sequence are equal.

    Determines whether all characters in the given sequence are identical.
    This is useful for validating strings that should not have all the
    same character (like CPF/CNPJ validation).

    Args:
        words: Sequence of characters to check for equality

    Returns:
        True if all characters are the same, False otherwise

    Examples:
        >>> is_equal("111111")
        True
        >>> is_equal("123456")
        False
    """
    return all(c == words[i - 1] for i, c in enumerate(words) if i > 0)


def remove_special_characters(text: str) -> str:
    """
    Remove special characters and accents from text.

    Cleans the input text by removing special characters (keeping only
    alphanumeric characters and whitespace) and then removes accents
    from the remaining characters.

    Args:
        text: Input text to clean

    Returns:
        Cleaned text with special characters and accents removed

    Examples:
        >>> remove_special_characters("Olá, mundo!")
        "Ola mundo"
        >>> remove_special_characters("Test@123#")
        "Test123"
    """
    cleaned_text = re.sub(r"([^\s\w]|_)+", "", text.strip())
    return remove_accents(cleaned_text)


def remove_accents(text: str) -> str:
    """
    Remove accents and diacritical marks from text.

    Uses Unicode normalization to decompose characters with accents
    and then removes the combining diacritical marks, leaving only
    the base characters.

    Args:
        text: Input text that may contain accented characters

    Returns:
        Text with accents and diacritical marks removed

    Examples:
        >>> remove_accents("café")
        "cafe"
        >>> remove_accents("naïve")
        "naive"
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
