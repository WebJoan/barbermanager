from ninja import Schema
from typing import Optional
from datetime import datetime


class UserSchema(Schema):
    """User basic information schema"""
    id: int
    username: str
    email: str
    name: str
    surname: str
    phone_number: Optional[str]
    is_active: bool
    user_type: str
    created_at: datetime


class TokenSchema(Schema):
    """JWT token information schema"""
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str = "Bearer"


class LoginResponseSchema(Schema):
    """Login response schema"""
    user: dict  # Will contain user.to_dict() response
    token: TokenSchema


class RegisterClientSchema(Schema):
    """Client registration input schema"""
    email: str
    password: str
    username: str
    name: str
    surname: str
    phone_number: Optional[str] = None


class RegisterBarberSchema(Schema):
    """Barber registration input schema"""
    username: str
    password: str
    name: str
    surname: str
    description: Optional[str] = None


class LoginSchema(Schema):
    """Login input schema"""
    email: Optional[str] = None
    username: Optional[str] = None
    password: str


class LogoutSchema(Schema):
    """Logout input schema"""
    refresh_token: str


class RequestPasswordResetSchema(Schema):
    """Password reset request schema"""
    email: str


class ConfirmPasswordResetSchema(Schema):
    """Password reset confirmation schema"""
    password: str


class RefreshTokenSchema(Schema):
    """Token refresh input schema"""
    refresh_token: str


class RefreshTokenResponseSchema(Schema):
    """Token refresh response schema"""
    access_token: str
    expires_in: int
    token_type: str = "Bearer"


class MessageResponseSchema(Schema):
    """Generic message response schema"""
    detail: str


class EmailResponseSchema(Schema):
    """Email response schema"""
    email: str


class CurrentUserResponseSchema(Schema):
    """Current user response schema"""
    me: dict  # Will contain user.to_dict() response 