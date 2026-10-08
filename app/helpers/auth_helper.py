"""
Authentication Helper
Provides utility functions for password hashing and JWT token management.
"""

from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt
from app.config import settings


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        plain_password: The raw password string to hash.

    Returns:
        The hashed password string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: The raw password to check.
        hashed_password: The stored hashed password.

    Returns:
        True if the password matches, False otherwise.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token with the given payload data.

    Args:
        data: Dictionary of claims to encode in the token.
        expires_delta: Optional custom expiration time. Defaults to config value.

    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Args:
        token: The JWT token string to decode.

    Returns:
        Dictionary of decoded claims if valid, None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None
