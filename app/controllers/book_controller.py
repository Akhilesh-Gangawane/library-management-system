"""
Book Controller
Handles all book-related business logic including CRUD, search, and filtering.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from app.helpers.response_helper import success_response, error_response, paginated_response
from app.helpers.validation_helper import is_valid_isbn


# ==================== Book Operations ====================

def get_all_books(
    db: Session,
    page: int = 1,
    per_page: int = 12,
    search: str = None,
    category_id: int = None,
    author_id: int = None,
    available_only: bool = False,
) -> dict:
    """
    Retrieve a paginated list of books with optional search and filters.

    Supports filtering by category, author, availability, and a text search
    across title, ISBN, and publisher fields.
    """
    query = db.query(Book).options(
        joinedload(Book.author),
        joinedload(Book.category),
    )

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_term),
                Book.isbn.ilike(search_term),
                Book.publisher.ilike(search_term),
            )
        )

    # Apply category filter
    if category_id:
        query = query.filter(Book.category_id == category_id)

    # Apply author filter
    if author_id:
        query = query.filter(Book.author_id == author_id)

    # Apply availability filter
    if available_only:
        query = query.filter(Book.is_available == True, Book.available_copies > 0)

    # Count total results
    total = query.count()

    # Paginate
    offset = (page - 1) * per_page
    books = query.offset(offset).limit(per_page).all()

    # Serialize
    books_data = []
    for book in books:
        books_data.append({
            "id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "description": book.description,
            "publisher": book.publisher,
            "published_year": book.published_year,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies,
            "is_available": book.is_available,
            "cover_image": book.cover_image,
            "author": {
                "id": book.author.id,
                "name": book.author.name,
            } if book.author else None,
            "category": {
                "id": book.category.id,
                "name": book.category.name,
            } if book.category else None,
            "created_at": str(book.created_at) if book.created_at else None,
        })

    return paginated_response(books_data, total, page, per_page, "Books retrieved successfully")


def get_book_by_id(db: Session, book_id: int) -> dict:
    """
    Retrieve detailed information about a single book.
    """
    book = (
        db.query(Book)
        .options(joinedload(Book.author), joinedload(Book.category))
        .filter(Book.id == book_id)
        .first()
    )

    if not book:
        return error_response("Book not found", 404)

    book_data = {
        "id": book.id,
        "title": book.title,
        "isbn": book.isbn,
        "description": book.description,
        "publisher": book.publisher,
        "published_year": book.published_year,
        "total_copies": book.total_copies,
        "available_copies": book.available_copies,
        "is_available": book.is_available,
        "cover_image": book.cover_image,
        "author": {
            "id": book.author.id,
            "name": book.author.name,
            "bio": book.author.bio,
        } if book.author else None,
        "category": {
            "id": book.category.id,
            "name": book.category.name,
            "description": book.category.description,
        } if book.category else None,
        "created_at": str(book.created_at) if book.created_at else None,
        "updated_at": str(book.updated_at) if book.updated_at else None,
    }

    return success_response(book_data, "Book retrieved successfully")


def create_book(db: Session, book_data: dict) -> dict:
    """
    Create a new book record. Admin only.
    Validates ISBN format and checks for duplicates.
    """
    # Validate ISBN
    if not is_valid_isbn(book_data["isbn"]):
        return error_response("Invalid ISBN format. Must be 10 or 13 digits.", 400)

    # Check for duplicate ISBN
    existing = db.query(Book).filter(Book.isbn == book_data["isbn"]).first()
    if existing:
        return error_response("A book with this ISBN already exists", 409)

    # Resolve or auto-create author
    author_id = book_data.get("author_id")
    new_author_name = book_data.get("new_author_name")
    if new_author_name and new_author_name.strip():
        clean_name = new_author_name.strip()
        author = db.query(Author).filter(Author.name.ilike(clean_name)).first()
        if not author:
            author = Author(name=clean_name)
            db.add(author)
            db.flush()
        author_id = author.id
    elif author_id:
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            return error_response("Author not found", 404)
    else:
        return error_response("Please select or specify an author", 400)

    # Resolve or auto-create category
    category_id = book_data.get("category_id")
    new_category_name = book_data.get("new_category_name")
    if new_category_name and new_category_name.strip():
        clean_cat = new_category_name.strip()
        category = db.query(Category).filter(Category.name.ilike(clean_cat)).first()
        if not category:
            category = Category(name=clean_cat)
            db.add(category)
            db.flush()
        category_id = category.id
    elif category_id:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return error_response("Category not found", 404)
    else:
        return error_response("Please select or specify a category", 400)

    new_book = Book(
        title=book_data["title"].strip(),
        isbn=book_data["isbn"].strip(),
        description=book_data.get("description"),
        publisher=book_data.get("publisher"),
        published_year=book_data.get("published_year"),
        total_copies=book_data.get("total_copies", 1),
        available_copies=book_data.get("total_copies", 1),
        author_id=author_id,
        category_id=category_id,
        cover_image=book_data.get("cover_image"),
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return success_response(
        data={
            "id": new_book.id,
            "title": new_book.title,
            "isbn": new_book.isbn,
        },
        message="Book created successfully",
        status_code=201,
    )


def update_book(db: Session, book_id: int, update_data: dict) -> dict:
    """
    Update an existing book record. Admin only.
    Only non-None fields in update_data are applied.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return error_response("Book not found", 404)

    # Check ISBN uniqueness if being changed
    if update_data.get("isbn") and update_data["isbn"] != book.isbn:
        existing = db.query(Book).filter(Book.isbn == update_data["isbn"]).first()
        if existing:
            return error_response("A book with this ISBN already exists", 409)

    # Handle new author on update if provided
    new_author_name = update_data.get("new_author_name")
    if new_author_name and new_author_name.strip():
        clean_name = new_author_name.strip()
        author = db.query(Author).filter(Author.name.ilike(clean_name)).first()
        if not author:
            author = Author(name=clean_name)
            db.add(author)
            db.flush()
        book.author_id = author.id

    # Handle new category on update if provided
    new_category_name = update_data.get("new_category_name")
    if new_category_name and new_category_name.strip():
        clean_cat = new_category_name.strip()
        category = db.query(Category).filter(Category.name.ilike(clean_cat)).first()
        if not category:
            category = Category(name=clean_cat)
            db.add(category)
            db.flush()
        book.category_id = category.id

    # Apply updates
    updatable_fields = [
        "title", "isbn", "description", "publisher", "published_year",
        "total_copies", "available_copies", "is_available", "author_id",
        "category_id", "cover_image",
    ]

    for field in updatable_fields:
        if field in update_data and update_data[field] is not None:
            setattr(book, field, update_data[field])

    db.commit()
    db.refresh(book)

    return success_response(
        data={"id": book.id, "title": book.title},
        message="Book updated successfully",
    )


def delete_book(db: Session, book_id: int) -> dict:
    """
    Delete a book from the library. Admin only.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return error_response("Book not found", 404)

    db.delete(book)
    db.commit()

    return success_response(message="Book deleted successfully")


# ==================== Author Operations ====================

def get_all_authors(db: Session) -> dict:
    """Retrieve all authors."""
    authors = db.query(Author).all()
    authors_data = [
        {"id": a.id, "name": a.name, "bio": a.bio, "created_at": str(a.created_at) if a.created_at else None}
        for a in authors
    ]
    return success_response(authors_data, "Authors retrieved successfully")


def create_author(db: Session, name: str, bio: str = None) -> dict:
    """Create a new author. Admin only."""
    existing = db.query(Author).filter(Author.name == name.strip()).first()
    if existing:
        return error_response("Author already exists", 409)

    author = Author(name=name.strip(), bio=bio)
    db.add(author)
    db.commit()
    db.refresh(author)

    return success_response(
        data={"id": author.id, "name": author.name},
        message="Author created successfully",
        status_code=201,
    )


# ==================== Category Operations ====================

def get_all_categories(db: Session) -> dict:
    """Retrieve all categories."""
    categories = db.query(Category).all()
    categories_data = [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "created_at": str(c.created_at) if c.created_at else None,
        }
        for c in categories
    ]
    return success_response(categories_data, "Categories retrieved successfully")


def create_category(db: Session, name: str, description: str = None) -> dict:
    """Create a new category. Admin only."""
    existing = db.query(Category).filter(Category.name == name.strip()).first()
    if existing:
        return error_response("Category already exists", 409)

    category = Category(name=name.strip(), description=description)
    db.add(category)
    db.commit()
    db.refresh(category)

    return success_response(
        data={"id": category.id, "name": category.name},
        message="Category created successfully",
        status_code=201,
    )
