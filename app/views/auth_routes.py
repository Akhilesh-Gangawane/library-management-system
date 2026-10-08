"""
Auth Routes
API endpoints for user registration, login, and profile management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, UserLogin, UserUpdate
from app.controllers.auth_controller import (
    register_user,
    login_user,
    get_current_user_profile,
    update_user_profile,
)
from app.middlewares.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    return register_user(
        db=db,
        full_name=user_data.full_name,
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone,
    )


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and receive a JWT token."""
    return login_user(db=db, email=user_data.email, password=user_data.password)


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get the current user's profile."""
    return get_current_user_profile(db=db, user_id=current_user.id)


@router.put("/profile")
def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update the current user's profile."""
    return update_user_profile(
        db=db,
        user_id=current_user.id,
        full_name=update_data.full_name,
        phone=update_data.phone,
    )
