"""
Library Management System - Main Application Entry Point
Configures the FastAPI app, mounts static files, and registers all routes.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.views.auth_routes import router as auth_router
from app.views.book_routes import router as book_router
from app.views.borrowing_routes import router as borrowing_router
from app.views.admin_routes import router as admin_router
from app.views.page_routes import router as page_router

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A library management system with user and admin features.",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register API routes
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(borrowing_router)
app.include_router(admin_router)

# Register page routes (must be last to avoid conflicts with API routes)
app.include_router(page_router)
