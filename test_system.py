"""
End-to-End System Tests
Tests all endpoints: Auth, Books, Borrowings, Admin Operations, and HTML Page delivery.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def run_tests():
    print("========================================")
    print("RUNNING LIBRARY MANAGEMENT SYSTEM TESTS")
    print("========================================")

    # 1. Test HTML Page Deliveries
    pages = ["/", "/login", "/register", "/books", "/books/1", "/dashboard", "/my-history", "/profile", "/admin", "/admin/books", "/admin/users", "/admin/borrowings"]
    for path in pages:
        res = client.get(path)
        assert res.status_code == 200, f"Page {path} returned {res.status_code}"
        print(f"  [+] Page OK: {path}")

    # 2. Test User Login (user@email.com / user@123)
    res = client.post("/api/auth/login", json={"email": "user@email.com", "password": "user@123"})
    assert res.status_code == 200
    user_data = res.json()
    assert user_data["success"] is True
    user_token = user_data["data"]["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    print("  [+] User login OK: user@email.com")

    # 3. Test Admin Login (admin@college.edu / admin@123)
    res = client.post("/api/auth/login", json={"email": "admin@college.edu", "password": "admin@123"})
    assert res.status_code == 200
    admin_data = res.json()
    assert admin_data["success"] is True
    assert admin_data["data"]["user"]["is_admin"] is True
    admin_token = admin_data["data"]["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("  [+] Admin login OK: admin@college.edu")

    # 4. Test User Profile
    res = client.get("/api/auth/profile", headers=user_headers)
    assert res.status_code == 200
    assert res.json()["data"]["email"] == "user@email.com"
    print("  [+] Get profile OK")

    res = client.put("/api/auth/profile", headers=user_headers, json={"full_name": "John Doe Updated", "phone": "9999888877"})
    assert res.status_code == 200
    assert res.json()["data"]["full_name"] == "John Doe Updated"
    print("  [+] Update profile OK")

    # 5. Test Public Book Listing, Search & Filters
    res = client.get("/api/books")
    assert res.status_code == 200
    books = res.json()["data"]
    assert len(books) > 0
    print(f"  [+] List books OK (found {len(books)} books)")

    res = client.get("/api/books?search=Clean")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 1
    print("  [+] Search books OK")

    res = client.get("/api/books?category_id=1")
    assert res.status_code == 200
    print("  [+] Filter books by category OK")

    res = client.get("/api/books?available_only=true")
    assert res.status_code == 200
    print("  [+] Filter books by availability OK")

    res = client.get("/api/books/1")
    assert res.status_code == 200
    assert res.json()["data"]["id"] == 1
    print("  [+] Get book details OK")

    # 6. Test Book Borrowing & Return Flow
    # Borrow book id=2
    res = client.post("/api/borrowings", headers=user_headers, json={"book_id": 2})
    assert res.status_code in (200, 201), f"Borrow failed: {res.text}"
    borrow_id = res.json()["data"]["id"]
    print(f"  [+] Borrow book OK (borrowing_id={borrow_id})")

    # Cannot borrow duplicate book
    res = client.post("/api/borrowings", headers=user_headers, json={"book_id": 2})
    assert res.status_code == 400
    print("  [+] Duplicate borrow prevention OK")

    # View my history
    res = client.get("/api/borrowings/my-history", headers=user_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 1
    print("  [+] View user borrowing history OK")

    # Return book
    res = client.put(f"/api/borrowings/{borrow_id}/return", headers=user_headers)
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "returned"
    print("  [+] Return book OK")

    # 7. Test Admin Operations
    # Add Author
    res = client.post("/api/admin/authors", headers=admin_headers, json={"name": "Andrew S. Tanenbaum", "bio": "Author of Modern Operating Systems"})
    assert res.status_code in (200, 201)
    author_id = res.json()["data"]["id"]
    print(f"  [+] Admin add author OK (author_id={author_id})")

    # Add Category
    res = client.post("/api/admin/categories", headers=admin_headers, json={"name": "Operating Systems", "description": "OS kernel and design"})
    assert res.status_code in (200, 201)
    category_id = res.json()["data"]["id"]
    print(f"  [+] Admin add category OK (category_id={category_id})")

    # Add Book
    res = client.post("/api/admin/books", headers=admin_headers, json={
        "title": "Modern Operating Systems",
        "isbn": "9780133591620",
        "description": "Comprehensive OS textbook",
        "publisher": "Pearson",
        "published_year": 2014,
        "total_copies": 4,
        "author_id": author_id,
        "category_id": category_id,
    })
    assert res.status_code in (200, 201)
    new_book_id = res.json()["data"]["id"]
    print(f"  [+] Admin add book OK (book_id={new_book_id})")

    # Update Book (and manage availability)
    res = client.put(f"/api/admin/books/{new_book_id}", headers=admin_headers, json={
        "total_copies": 7,
        "available_copies": 7,
        "is_available": True,
    })
    assert res.status_code == 200
    print("  [+] Admin update book & availability OK")

    # View Users
    res = client.get("/api/admin/users", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2
    print(f"  [+] Admin view users OK (found {len(res.json()['data'])} users)")

    # View All Borrowing Records
    res = client.get("/api/admin/borrowings", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 1
    print("  [+] Admin view all borrowings OK")

    # Delete Book
    res = client.delete(f"/api/admin/books/{new_book_id}", headers=admin_headers)
    assert res.status_code == 200
    print("  [+] Admin delete book OK")

    # Non-admin forbidden from admin endpoints
    res = client.get("/api/admin/users", headers=user_headers)
    assert res.status_code == 403
    print("  [+] Non-admin forbidden (403) from admin endpoints OK")

    print("\n========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("========================================")


if __name__ == "__main__":
    run_tests()
