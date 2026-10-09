"""
Category Model
Represents book categories/genres in the library system.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    books = relationship("Book", back_populates="category")

    def to_dict(self) -> dict:
        """Serialize category model to a maintainable dictionary / JSON format."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": str(self.created_at) if self.created_at else None,
        }

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
