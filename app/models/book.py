"""
Book Model
Represents books in the library with availability tracking.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    publisher = Column(String(150), nullable=True)
    published_year = Column(Integer, nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    is_available = Column(Boolean, default=True)
    cover_image = Column(String(255), nullable=True)

    # Foreign Keys
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")
    borrowings = relationship("Borrowing", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"
