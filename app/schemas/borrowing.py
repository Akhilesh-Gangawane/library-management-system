"""
Borrowing Schemas
Pydantic models for borrowing record validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.book import BookResponse


class BorrowingCreate(BaseModel):
    """Schema for creating a borrowing record."""
    book_id: int


class BorrowingResponse(BaseModel):
    """Schema for borrowing data in responses."""
    id: int
    user_id: int
    book_id: int
    borrow_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: str
    user: Optional[UserResponse] = None
    book: Optional[BookResponse] = None

    class Config:
        from_attributes = True
