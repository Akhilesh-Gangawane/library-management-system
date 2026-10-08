"""
Validation Helper
Provides common validation functions used across the application.
"""

import re
from typing import Optional


def is_valid_email(email: str) -> bool:
    """
    Check whether the given string is a valid email format.

    Args:
        email: The email string to validate.

    Returns:
        True if the email format is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_isbn(isbn: str) -> bool:
    """
    Check whether the given string looks like a valid ISBN
    (10 or 13 digits, hyphens allowed).

    Args:
        isbn: The ISBN string to validate.

    Returns:
        True if the ISBN format is acceptable, False otherwise.
    """
    cleaned = isbn.replace("-", "").replace(" ", "")
    return len(cleaned) in (10, 13) and cleaned.isdigit()


def is_valid_password(password: str) -> tuple:
    """
    Validate password strength. Requires at least 6 characters.

    Args:
        password: The password string to validate.

    Returns:
        A tuple of (is_valid: bool, error_message: Optional[str]).
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, None


def sanitize_string(value: str) -> str:
    """
    Strip leading/trailing whitespace from a string.

    Args:
        value: The string to sanitize.

    Returns:
        The trimmed string.
    """
    if value:
        return value.strip()
    return value


def validate_positive_integer(value: int, field_name: str) -> tuple:
    """
    Ensure the given value is a positive integer.

    Args:
        value: The integer to validate.
        field_name: Name of the field (for error messages).

    Returns:
        A tuple of (is_valid: bool, error_message: Optional[str]).
    """
    if not isinstance(value, int) or value < 1:
        return False, f"{field_name} must be a positive integer"
    return True, None
