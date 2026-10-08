"""
Library Management System - Database Configuration
Handles SQLAlchemy engine, session, and base model setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Ensures the session is closed after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
