"""
Admin Routes
API endpoints restricted to admin users for managing the library system.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookCreate, BookUpdate, AuthorCreate, CategoryCreate
from app.controllers.book_controller import (
    create_book,
    update_book,
    delete_book,
    create_author,
    create_category,
)
from app.controllers.borrowing_controller import get_all_borrowings, get_all_users
from app.middlewares.auth_middleware import require_admin
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ---------- Book Management ----------

@router.post("/books")
def add_book(
    book_data: BookCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Add a new book to the library. Admin only."""
    return create_book(db=db, book_data=book_data.model_dump())


@router.put("/books/{book_id}")
def edit_book(
    book_id: int,
    book_data: BookUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update an existing book. Admin only."""
    return update_book(db=db, book_id=book_id, update_data=book_data.model_dump(exclude_none=True))


@router.delete("/books/{book_id}")
def remove_book(
    book_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a book from the library. Admin only."""
    return delete_book(db=db, book_id=book_id)


# ---------- Author Management ----------

@router.post("/authors")
def add_author(
    author_data: AuthorCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Add a new author. Admin only."""
    return create_author(db=db, name=author_data.name, bio=author_data.bio)


# ---------- Category Management ----------

@router.post("/categories")
def add_category(
    category_data: CategoryCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Add a new category. Admin only."""
    return create_category(db=db, name=category_data.name, description=category_data.description)


# ---------- User Management ----------

@router.get("/users")
def list_users(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all registered users. Admin only."""
    return get_all_users(db=db)


# ---------- Borrowing Records ----------

@router.get("/borrowings")
def list_all_borrowings(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    status: str = Query(None),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """View all borrowing records across users. Admin only."""
    return get_all_borrowings(db=db, page=page, per_page=per_page, status=status)
