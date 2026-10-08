"""
Database Seeder Script
Populates the database with initial admin, regular user, categories, authors, and books.
"""

from app.database import SessionLocal
from app.models.user import User
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.helpers.auth_helper import hash_password
from app.config import settings


def seed_database():
    db = SessionLocal()
    try:
        print("[*] Seeding database...")

        # 1. Seed Admin User
        admin_user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = User(
                full_name="College Administrator",
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                phone="+91-9876543210",
                is_admin=True,
                is_active=True,
            )
            db.add(admin_user)
            print(f"  [+] Admin created: {settings.ADMIN_EMAIL}")
        else:
            print(f"  [-] Admin already exists: {settings.ADMIN_EMAIL}")

        # 2. Seed Default Regular User
        regular_user = db.query(User).filter(User.email == settings.DEFAULT_USER_EMAIL).first()
        if not regular_user:
            regular_user = User(
                full_name="John Doe",
                email=settings.DEFAULT_USER_EMAIL,
                hashed_password=hash_password(settings.DEFAULT_USER_PASSWORD),
                phone="+91-9123456780",
                is_admin=False,
                is_active=True,
            )
            db.add(regular_user)
            print(f"  [+] User created: {settings.DEFAULT_USER_EMAIL}")
        else:
            print(f"  [-] User already exists: {settings.DEFAULT_USER_EMAIL}")

        db.commit()

        # 3. Seed Categories
        categories_data = [
            {"name": "Computer Science", "description": "Software development, algorithms, AI, and systems."},
            {"name": "Data Science", "description": "Machine learning, statistics, data analytics, and big data."},
            {"name": "Mathematics", "description": "Calculus, linear algebra, discrete math, and statistics."},
            {"name": "Literature & Fiction", "description": "Classic literature, modern fiction, and novels."},
            {"name": "Philosophy & Psychology", "description": "Human thought, ethics, reasoning, and behavior."},
        ]

        categories_map = {}
        for cat_info in categories_data:
            cat = db.query(Category).filter(Category.name == cat_info["name"]).first()
            if not cat:
                cat = Category(name=cat_info["name"], description=cat_info["description"])
                db.add(cat)
                db.flush()
                print(f"  [+] Category added: {cat.name}")
            categories_map[cat.name] = cat.id

        db.commit()

        # 4. Seed Authors
        authors_data = [
            {"name": "Robert C. Martin", "bio": "Software engineer and author of Clean Code and Clean Architecture."},
            {"name": "Donald E. Knuth", "bio": "Renowned computer scientist and author of The Art of Computer Programming."},
            {"name": "Martin Fowler", "bio": "Software developer and speaker specializing in enterprise architecture and refactoring."},
            {"name": "Stuart Russell & Peter Norvig", "bio": "Leading researchers in the field of Artificial Intelligence."},
            {"name": "Gilbert Strang", "bio": "Professor of Mathematics at MIT, known for Linear Algebra contributions."},
            {"name": "George Orwell", "bio": "English novelist, essayist, journalist, and critic."},
        ]

        authors_map = {}
        for auth_info in authors_data:
            auth = db.query(Author).filter(Author.name == auth_info["name"]).first()
            if not auth:
                auth = Author(name=auth_info["name"], bio=auth_info["bio"])
                db.add(auth)
                db.flush()
                print(f"  [+] Author added: {auth.name}")
            authors_map[auth.name] = auth.id

        db.commit()

        # 5. Seed Books
        books_data = [
            {
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "isbn": "9780132350884",
                "description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees. Every year, countless hours and significant resources are lost because of poorly written code.",
                "publisher": "Prentice Hall",
                "published_year": 2008,
                "total_copies": 5,
                "available_copies": 5,
                "author_id": authors_map["Robert C. Martin"],
                "category_id": categories_map["Computer Science"],
            },
            {
                "title": "The Art of Computer Programming, Vol. 1",
                "isbn": "9780201896831",
                "description": "The bible of fundamental algorithms and computing concepts. Spans basic data structures and asymptotic analysis.",
                "publisher": "Addison-Wesley Professional",
                "published_year": 1997,
                "total_copies": 3,
                "available_copies": 3,
                "author_id": authors_map["Donald E. Knuth"],
                "category_id": categories_map["Computer Science"],
            },
            {
                "title": "Refactoring: Improving the Design of Existing Code",
                "isbn": "9780134757599",
                "description": "Fully updated for JavaScript, Martin Fowler's guide teaches modern techniques for refactoring legacy software with confidence.",
                "publisher": "Addison-Wesley",
                "published_year": 2018,
                "total_copies": 4,
                "available_copies": 4,
                "author_id": authors_map["Martin Fowler"],
                "category_id": categories_map["Computer Science"],
            },
            {
                "title": "Artificial Intelligence: A Modern Approach",
                "isbn": "9780136042594",
                "description": "The leading textbook in Artificial Intelligence used in over 1,500 universities across the globe.",
                "publisher": "Pearson",
                "published_year": 2020,
                "total_copies": 4,
                "available_copies": 4,
                "author_id": authors_map["Stuart Russell & Peter Norvig"],
                "category_id": categories_map["Data Science"],
            },
            {
                "title": "Introduction to Linear Algebra",
                "isbn": "9780980232776",
                "description": "Comprehensive textbook covering linear equations, vector spaces, eigenvalues, and singular value decomposition.",
                "publisher": "Wellesley-Cambridge Press",
                "published_year": 2016,
                "total_copies": 6,
                "available_copies": 6,
                "author_id": authors_map["Gilbert Strang"],
                "category_id": categories_map["Mathematics"],
            },
            {
                "title": "1984",
                "isbn": "9780451524935",
                "description": "A startling and haunting novel that creates an imaginary world that is completely convincing, from the first sentence to the four finishing words.",
                "publisher": "Signet Classic",
                "published_year": 1949,
                "total_copies": 8,
                "available_copies": 8,
                "author_id": authors_map["George Orwell"],
                "category_id": categories_map["Literature & Fiction"],
            },
        ]

        for book_info in books_data:
            book = db.query(Book).filter(Book.isbn == book_info["isbn"]).first()
            if not book:
                book = Book(**book_info, is_available=True)
                db.add(book)
                print(f"  [+] Book added: {book.title}")

        db.commit()
        print("\n[OK] Database seeding complete!")

    except Exception as e:
        db.rollback()
        print(f"[!] Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
