"""
Borrowing Model
Tracks book borrowing and return records.
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="borrowed")  # borrowed, returned, overdue

    # Relationships
    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")

    def to_dict(self, include_relations: bool = True) -> dict:
        """
        Serialize borrowing mapper record to a maintainable dictionary / JSON format.
        Includes mapped book and user relations.
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "borrow_date": str(self.borrow_date) if self.borrow_date else None,
            "due_date": str(self.due_date) if self.due_date else None,
            "return_date": str(self.return_date) if self.return_date else None,
            "status": self.status,
        }
        if include_relations:
            if self.book:
                data["book"] = {
                    "id": self.book.id,
                    "title": self.book.title,
                    "isbn": self.book.isbn,
                    "author": self.book.author.name if self.book.author else None,
                }
            else:
                data["book"] = None

            if self.user:
                data["user"] = {
                    "id": self.user.id,
                    "full_name": self.user.full_name,
                    "email": self.user.email,
                }
            else:
                data["user"] = None
        return data

    def __repr__(self):
        return (
            f"<Borrowing(id={self.id}, user_id={self.user_id}, "
            f"book_id={self.book_id}, status='{self.status}')>"
        )
