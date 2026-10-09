"""
Borrowing Controller
Handles book borrowing, returning, and history retrieval logic.
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session, joinedload
from app.models.borrowing import Borrowing
from app.models.book import Book
from app.models.user import User
from app.helpers.response_helper import success_response, error_response, paginated_response


# Default loan period in days
LOAN_PERIOD_DAYS = 14


def borrow_book(db: Session, user_id: int, book_id: int) -> dict:
    """
    Process a book borrowing request.

    Checks availability, prevents duplicate active borrows,
    decrements the available copies, and creates a borrowing record.
    """
    # Check if book exists
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return error_response("Book not found", 404)

    # Check availability
    if not book.is_available or book.available_copies <= 0:
        return error_response("Book is not available for borrowing", 400)

    # Check if user already has this book borrowed (and not returned)
    active_borrow = (
        db.query(Borrowing)
        .filter(
            Borrowing.user_id == user_id,
            Borrowing.book_id == book_id,
            Borrowing.status == "borrowed",
        )
        .first()
    )
    if active_borrow:
        return error_response("You already have this book borrowed", 400)

    # Create borrowing record
    now = datetime.now(timezone.utc)
    borrowing = Borrowing(
        user_id=user_id,
        book_id=book_id,
        borrow_date=now,
        due_date=now + timedelta(days=LOAN_PERIOD_DAYS),
        status="borrowed",
    )

    # Update book availability
    book.available_copies -= 1
    if book.available_copies == 0:
        book.is_available = False

    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)

    return success_response(
        data={
            "id": borrowing.id,
            "book_id": borrowing.book_id,
            "borrow_date": str(borrowing.borrow_date),
            "due_date": str(borrowing.due_date),
            "status": borrowing.status,
        },
        message="Book borrowed successfully",
        status_code=201,
    )


def return_book(db: Session, user_id: int, borrowing_id: int) -> dict:
    """
    Process a book return.

    Marks the borrowing record as returned, records the return date,
    and increments the book's available copies.
    """
    borrowing = (
        db.query(Borrowing)
        .filter(Borrowing.id == borrowing_id, Borrowing.user_id == user_id)
        .first()
    )

    if not borrowing:
        return error_response("Borrowing record not found", 404)

    if borrowing.status == "returned":
        return error_response("This book has already been returned", 400)

    # Update borrowing record
    borrowing.return_date = datetime.now(timezone.utc)
    borrowing.status = "returned"

    # Update book availability
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if book:
        book.available_copies += 1
        book.is_available = True

    db.commit()
    db.refresh(borrowing)

    return success_response(
        data={
            "id": borrowing.id,
            "return_date": str(borrowing.return_date),
            "status": borrowing.status,
        },
        message="Book returned successfully",
    )


def get_user_borrowings(db: Session, user_id: int, page: int = 1, per_page: int = 10) -> dict:
    """
    Retrieve the borrowing history for a specific user using ORM joins.
    """
    query = (
        db.query(Borrowing)
        .join(Borrowing.book)
        .outerjoin(Book.author)
        .options(joinedload(Borrowing.book).joinedload(Book.author))
        .filter(Borrowing.user_id == user_id)
        .order_by(Borrowing.borrow_date.desc())
    )

    total = query.count()
    offset = (page - 1) * per_page
    borrowings = query.offset(offset).limit(per_page).all()
    borrowings_data = [b.to_dict() for b in borrowings]

    return paginated_response(borrowings_data, total, page, per_page, "Borrowing history retrieved")


def get_all_borrowings(db: Session, page: int = 1, per_page: int = 10, status: str = None) -> dict:
    """
    Retrieve all borrowing records across all users using ORM joins. Admin only.
    Optionally filter by borrowing status.
    """
    query = (
        db.query(Borrowing)
        .join(Borrowing.book)
        .join(Borrowing.user)
        .outerjoin(Book.author)
        .options(
            joinedload(Borrowing.book).joinedload(Book.author),
            joinedload(Borrowing.user),
        )
        .order_by(Borrowing.borrow_date.desc())
    )

    if status:
        query = query.filter(Borrowing.status == status)

    total = query.count()
    offset = (page - 1) * per_page
    borrowings = query.offset(offset).limit(per_page).all()
    borrowings_data = [b.to_dict() for b in borrowings]

    return paginated_response(borrowings_data, total, page, per_page, "All borrowing records retrieved")


def get_all_users(db: Session) -> dict:
    """
    Retrieve all registered users. Admin only.
    """
    users = db.query(User).all()
    users_data = [u.to_dict() for u in users]
    return success_response(users_data, "Users retrieved successfully")
