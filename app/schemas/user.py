"""
User Schemas
Pydantic models for user data validation and serialization.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration."""
    full_name: str
    email: str
    password: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: str
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses."""
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    is_admin: bool
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    phone: Optional[str] = None


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
