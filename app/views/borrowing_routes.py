"""
Borrowing Routes
API endpoints for borrowing and returning books (authenticated users).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.borrowing import BorrowingCreate
from app.controllers.borrowing_controller import (
    borrow_book,
    return_book,
    get_user_borrowings,
)
from app.middlewares.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/borrowings", tags=["Borrowings"])


@router.post("")
def borrow(
    data: BorrowingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Borrow a book. Requires authentication."""
    return borrow_book(db=db, user_id=current_user.id, book_id=data.book_id)


@router.put("/{borrowing_id}/return")
def return_borrowed_book(
    borrowing_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a borrowed book. Requires authentication."""
    return return_book(db=db, user_id=current_user.id, borrowing_id=borrowing_id)


@router.get("/my-history")
def my_borrowing_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the current user's borrowing history."""
    return get_user_borrowings(db=db, user_id=current_user.id, page=page, per_page=per_page)
