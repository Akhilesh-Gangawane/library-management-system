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

    def __repr__(self):
        return (
            f"<Borrowing(id={self.id}, user_id={self.user_id}, "
            f"book_id={self.book_id}, status='{self.status}')>"
        )
