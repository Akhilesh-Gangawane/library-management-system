"""
Author Model
Represents book authors in the library system.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    books = relationship("Book", back_populates="author")

    def to_dict(self) -> dict:
        """Serialize author model to a maintainable dictionary / JSON format."""
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "created_at": str(self.created_at) if self.created_at else None,
        }

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"
