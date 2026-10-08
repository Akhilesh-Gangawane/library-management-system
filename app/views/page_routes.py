"""
Page Routes
Serves the HTML pages for the frontend. Separates API routes from page rendering.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="app/views/templates")


@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    """Serve the home / landing page."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Serve the registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/books", response_class=HTMLResponse)
def books_page(request: Request):
    """Serve the books browsing page."""
    return templates.TemplateResponse("books.html", {"request": request})


@router.get("/books/{book_id}", response_class=HTMLResponse)
def book_detail_page(request: Request, book_id: int):
    """Serve the book detail page."""
    return templates.TemplateResponse("book_detail.html", {"request": request, "book_id": book_id})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    """Serve the user dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/my-history", response_class=HTMLResponse)
def history_page(request: Request):
    """Serve the borrowing history page."""
    return templates.TemplateResponse("history.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    """Serve the user profile page."""
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard_page(request: Request):
    """Serve the admin dashboard page."""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/admin/books", response_class=HTMLResponse)
def admin_books_page(request: Request):
    """Serve the admin books management page."""
    return templates.TemplateResponse("admin/books.html", {"request": request})


@router.get("/admin/users", response_class=HTMLResponse)
def admin_users_page(request: Request):
    """Serve the admin users page."""
    return templates.TemplateResponse("admin/users.html", {"request": request})


@router.get("/admin/borrowings", response_class=HTMLResponse)
def admin_borrowings_page(request: Request):
    """Serve the admin borrowings page."""
    return templates.TemplateResponse("admin/borrowings.html", {"request": request})
