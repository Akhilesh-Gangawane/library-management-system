"""
Book Schemas
Pydantic models for book, author, and category validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- Author Schemas ----------

class AuthorCreate(BaseModel):
    """Schema for creating an author."""
    name: str
    bio: Optional[str] = None


class AuthorResponse(BaseModel):
    """Schema for author data in responses."""
    id: int
    name: str
    bio: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- Category Schemas ----------

class CategoryCreate(BaseModel):
    """Schema for creating a category."""
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    """Schema for category data in responses."""
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- Book Schemas ----------

class BookCreate(BaseModel):
    """Schema for creating a book."""
    title: str
    isbn: str
    description: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int = 1
    author_id: Optional[int] = None
    new_author_name: Optional[str] = None
    category_id: Optional[int] = None
    new_category_name: Optional[str] = None
    cover_image: Optional[str] = None


class BookUpdate(BaseModel):
    """Schema for updating a book."""
    title: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    is_available: Optional[bool] = None
    author_id: Optional[int] = None
    new_author_name: Optional[str] = None
    category_id: Optional[int] = None
    cover_image: Optional[str] = None


class BookResponse(BaseModel):
    """Schema for book data in responses."""
    id: int
    title: str
    isbn: str
    description: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int
    available_copies: int
    is_available: bool
    cover_image: Optional[str] = None
    author_id: int
    category_id: int
    author: Optional[AuthorResponse] = None
    category: Optional[CategoryResponse] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
