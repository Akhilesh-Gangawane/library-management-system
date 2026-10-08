"""
Auth Controller
Handles user registration, login, and token management business logic.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.helpers.auth_helper import hash_password, verify_password, create_access_token
from app.helpers.validation_helper import is_valid_email, is_valid_password
from app.helpers.response_helper import success_response, error_response


def register_user(db: Session, full_name: str, email: str, password: str, phone: str = None) -> dict:
    """
    Register a new user account.

    Validates email format and password strength, checks for duplicate emails,
    then creates the user record with a hashed password.
    """
    # Validate email format
    if not is_valid_email(email):
        return error_response("Invalid email format", 400)

    # Validate password strength
    is_valid, pwd_error = is_valid_password(password)
    if not is_valid:
        return error_response(pwd_error, 400)

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return error_response("Email already registered", 409)

    # Create new user
    new_user = User(
        full_name=full_name.strip(),
        email=email.strip().lower(),
        hashed_password=hash_password(password),
        phone=phone,
        is_admin=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate token for auto-login after registration
    token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email, "is_admin": False}
    )

    return success_response(
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email,
                "phone": new_user.phone,
                "is_admin": new_user.is_admin,
            },
        },
        message="Registration successful",
        status_code=201,
    )


def login_user(db: Session, email: str, password: str) -> dict:
    """
    Authenticate a user and issue a JWT token.

    Looks up the user by email, verifies the password, and returns
    an access token on success.
    """
    # Find user by email
    user = db.query(User).filter(User.email == email.strip().lower()).first()

    if not user:
        return error_response("Invalid email or password", 401)

    # Verify password
    if not verify_password(password, user.hashed_password):
        return error_response("Invalid email or password", 401)

    # Check if account is active
    if not user.is_active:
        return error_response("Account is deactivated", 403)

    # Generate JWT token
    token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "is_admin": user.is_admin,
        }
    )

    return success_response(
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "is_admin": user.is_admin,
            },
        },
        message="Login successful",
    )


def get_current_user_profile(db: Session, user_id: int) -> dict:
    """
    Retrieve the profile of the currently authenticated user.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return error_response("User not found", 404)

    return success_response(
        data={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "created_at": str(user.created_at) if user.created_at else None,
        },
        message="Profile retrieved successfully",
    )


def update_user_profile(db: Session, user_id: int, full_name: str = None, phone: str = None) -> dict:
    """
    Update the profile fields for the authenticated user.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return error_response("User not found", 404)

    if full_name:
        user.full_name = full_name.strip()
    if phone is not None:
        user.phone = phone

    db.commit()
    db.refresh(user)

    return success_response(
        data={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin,
        },
        message="Profile updated successfully",
    )
