from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import PermissionDenied

from ..ninja_schemas.auth import (
    RegisterClientSchema,
    RegisterBarberSchema,
    LoginSchema,
    LoginResponseSchema,
    LogoutSchema,
    RequestPasswordResetSchema,
    ConfirmPasswordResetSchema,
    RefreshTokenSchema,
    RefreshTokenResponseSchema,
    MessageResponseSchema,
    EmailResponseSchema,
    CurrentUserResponseSchema,
)
from ..models import User, Client
from ..utils import (
    send_client_verify_email,
    send_password_reset_email,
)
from django.contrib.auth import authenticate

router = Router()


from ..ninja_auth import JWTAuth

jwt_auth = JWTAuth()

@router.get("/me", response=CurrentUserResponseSchema, auth=jwt_auth)
def get_current_user(request):
    """
    Returns the current authenticated user's information.
    """
    return {"me": request.auth.to_dict()}


@router.post("/register", response=MessageResponseSchema)
def register_client(request, data: RegisterClientSchema):
    """
    Client self registration. Creates inactive client and sends confirmation email.
    """
    # Validate email uniqueness
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "User with this email already exists")
    
    # Validate username uniqueness
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "User with this username already exists")
    
    # Create client
    client = Client(
        email=data.email,
        username=data.username,
        name=data.name,
        surname=data.surname,
        is_active=False
    )
    
    if data.phone_number:
        client.phone_number = data.phone_number
    
    client.set_password(data.password)
    client.save()
    
    # Send verification email
    uid = urlsafe_base64_encode(force_bytes(client.pk))
    token = default_token_generator.make_token(client)
    send_client_verify_email(client.email, uid, token, settings.FRONTEND_URL)
    
    return {"detail": "Client registered, check your email to verify."}


@router.post("/register/{uidb64}/{token}", response=MessageResponseSchema)
def register_barber(request, uidb64: str, token: str, data: RegisterBarberSchema):
    """
    Barber completes registration via invite link by setting username and password.
    """
    # Validate UID and token
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise HttpError(400, "Invalid or expired confirmation link")
    
    if not default_token_generator.check_token(user, token):
        raise HttpError(400, "Invalid or expired confirmation link")
    
    if user.is_active:
        raise HttpError(400, "Account already registered")
    
    # Validate username uniqueness
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "User with this username already exists")
    
    # Update barber
    user.username = data.username
    user.name = data.name
    user.surname = data.surname
    user.is_active = True
    
    if data.description:
        user.description = data.description
    
    user.set_password(data.password)
    user.save()
    
    return {"detail": "Barber registered and account activated."}


@router.get("/email/{uidb64}/{token}", response=EmailResponseSchema)
def get_email_from_token(request, uidb64: str, token: str):
    """
    Returns the email associated to the user from a valid given uid64 and token
    """
    # Validate UID and token
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise HttpError(400, "Invalid or expired confirmation link")
    
    if not default_token_generator.check_token(user, token):
        raise HttpError(400, "Invalid or expired confirmation link")
    
    return {"email": user.email}


@router.get("/verify/{uidb64}/{token}", response=MessageResponseSchema)
def verify_client(request, uidb64: str, token: str):
    """
    Verifies client account from confirmation email link.
    """
    # Validate UID and token
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise HttpError(400, "Invalid or expired confirmation link")
    
    if not default_token_generator.check_token(user, token):
        raise HttpError(400, "Invalid or expired confirmation link")
    
    if user.is_active:
        raise HttpError(400, "Account already verified")
    
    user.is_active = True
    user.save()
    
    return {"detail": "Email verified successfully."}


@router.post("/login", response=LoginResponseSchema)
def login_user(request, data: LoginSchema):
    """
    Login with email OR username + password.
    """
    if not data.email and not data.username:
        raise HttpError(400, "You must provide either an email or username")
    
    if data.email and data.username:
        raise HttpError(400, "Provide only one of email or username, not both")
    
    identifier = data.username or data.email
    user = authenticate(username=identifier, password=data.password)
    
    if not user:
        raise HttpError(403, "Invalid credentials")
    
    if not user.is_active:
        raise HttpError(403, "Account inactive. Please verify your email")
    
    refresh = RefreshToken.for_user(user)
    
    return {
        "user": user.to_dict(),
        "token": {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "expires_in": int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
            "refresh_expires_in": int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
            "token_type": "Bearer"
        }
    }


@router.post("/logout", response=MessageResponseSchema, auth=jwt_auth)
def logout_user(request, data: LogoutSchema):
    """
    Logout by blacklisting the refresh token.
    """
    try:
        token = RefreshToken(data.refresh_token)
        token.blacklist()
    except TokenError:
        raise HttpError(400, "Invalid or expired refresh token")
    
    return {"detail": "Logout successful."}


@router.post("/reset-password", response=MessageResponseSchema)
def request_password_reset(request, data: RequestPasswordResetSchema):
    """
    Request password reset by email - sends reset email with token.
    """
    try:
        user = User.objects.get(email=data.email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        send_password_reset_email(user.email, uid, token, settings.FRONTEND_URL)
    except User.DoesNotExist:
        pass  # Don't reveal if email exists
    
    return {"detail": "If this email is registered, a password reset email has been sent."}


@router.post("/reset-password/{uidb64}/{token}", response=MessageResponseSchema)
def confirm_password_reset(request, uidb64: str, token: str, data: ConfirmPasswordResetSchema):
    """
    Confirm password reset by setting new password using token from email.
    """
    # Validate UID and token
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise HttpError(400, "Invalid or expired reset link")
    
    if not default_token_generator.check_token(user, token):
        raise HttpError(400, "Invalid or expired reset link")
    
    user.set_password(data.password)
    user.save()
    
    return {"detail": "Password has been reset successfully."}


@router.post("/refresh-token", response=RefreshTokenResponseSchema)
def refresh_token(request, data: RefreshTokenSchema):
    """
    Refresh the access token using a refresh token.
    """
    try:
        refresh = RefreshToken(data.refresh_token)
        return {
            "access_token": str(refresh.access_token),
            "expires_in": int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
            "token_type": "Bearer"
        }
    except TokenError:
        raise HttpError(400, "Invalid or expired refresh token") 