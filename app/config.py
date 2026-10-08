"""
Library Management System - Application Configuration
Loads environment variables and provides app-wide settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME: str = os.getenv("APP_NAME", "Library Management System")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./library.db")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Admin defaults
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@college.edu")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin@123")

    # Default user
    DEFAULT_USER_EMAIL: str = os.getenv("DEFAULT_USER_EMAIL", "user@email.com")
    DEFAULT_USER_PASSWORD: str = os.getenv("DEFAULT_USER_PASSWORD", "user@123")

    # CORS
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "http://localhost:8000"
    ).split(",")


settings = Settings()
