"""
Book Routes
API endpoints for book browsing, searching, and filtering (public + authenticated).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.book_controller import (
    get_all_books,
    get_book_by_id,
    get_all_authors,
    get_all_categories,
)

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.get("")
def list_books(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=100),
    search: str = Query(None),
    category_id: int = Query(None),
    author_id: int = Query(None),
    available_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    """
    List all books with pagination, search, and filtering options.
    This endpoint is publicly accessible.
    """
    return get_all_books(
        db=db,
        page=page,
        per_page=per_page,
        search=search,
        category_id=category_id,
        author_id=author_id,
        available_only=available_only,
    )


@router.get("/authors")
def list_authors(db: Session = Depends(get_db)):
    """List all authors."""
    return get_all_authors(db)


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    """List all categories."""
    return get_all_categories(db)


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific book."""
    return get_book_by_id(db=db, book_id=book_id)
