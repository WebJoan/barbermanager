from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from ..ninja_schemas.admin import (
    AdminProfileResponseSchema,
    BarbersListResponseSchema,
    ClientsListResponseSchema,
    AppointmentsListResponseSchema,
    InviteBarberSchema,
    MessageResponseSchema,
)
from ..models import User, Admin, Barber, Client, Appointment
from ..utils import (
    send_barber_invite_email,
)
from ..ninja_auth import JWTAuth

router = Router()
jwt_auth = JWTAuth()


def check_admin_permission(request):
    """Helper function to check if user is admin"""
    if not request.auth or request.auth.role != 'ADMIN':
        raise HttpError(403, "Admin access required")
    return request.auth


@router.get("/profile", response=AdminProfileResponseSchema, auth=jwt_auth)
def get_admin_profile(request):
    """
    Admin only: Gets all related profile information for authenticated admin.
    """
    admin = check_admin_permission(request)
    return {"profile": admin.to_dict()}


@router.get("/barbers", response=BarbersListResponseSchema, auth=jwt_auth)
def get_all_barbers(request):
    """
    Admin only: Returns all barbers registered and their data.
    """
    check_admin_permission(request)
    barbers = Barber.objects.all()
    return {"barbers": [barber.to_dict() for barber in barbers]}


@router.get("/clients", response=ClientsListResponseSchema, auth=jwt_auth)
def get_all_clients(request):
    """
    Admin only: Returns all clients registered and their data.
    """
    check_admin_permission(request)
    clients = Client.objects.all()
    return {"clients": [client.to_dict() for client in clients]}


@router.get("/appointments", response=AppointmentsListResponseSchema, auth=jwt_auth)
def get_all_appointments(request):
    """
    Admin only: Get all appointments present in the system.
    """
    check_admin_permission(request)
    appointments = Appointment.objects.all()
    return {"appointments": [appointment.to_dict() for appointment in appointments]}


@router.post("/barbers/invite", response=MessageResponseSchema, auth=jwt_auth)
def invite_barber(request, data: InviteBarberSchema):
    """
    Admin only: Invite a barber by email. Sends a link with encoded email (uid).
    """
    check_admin_permission(request)
    
    # Check if user with this email already exists
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "User with this email already exists")
    
    # Create inactive barber
    barber = Barber.objects.create_user(
        email=data.email,
        username=f"barber_{data.email.split('@')[0]}",  # Temporary username
        is_active=False,
        name=data.name,
        surname=data.surname,
        description=data.description,
    )
    
    # Send invitation email
    uid = urlsafe_base64_encode(force_bytes(barber.pk))
    token = default_token_generator.make_token(barber)
    send_barber_invite_email(barber.email, uid, token, settings.FRONTEND_URL)
    
    return {"detail": "Barber invited successfully."}


@router.delete("/barbers/{barber_id}", response=MessageResponseSchema, auth=jwt_auth)
def delete_barber(request, barber_id: int):
    """
    Admin only: Deletes a barber by ID.
    """
    check_admin_permission(request)
    
    try:
        barber = Barber.objects.get(id=barber_id)
        barber.delete()
        return {"detail": "Barber deleted successfully."}
    except Barber.DoesNotExist:
        raise HttpError(404, "Barber not found")


@router.get("/")
def admin_placeholder(request):
    """
    Placeholder for admin endpoints - will be implemented soon
    """
    return {"message": "Admin endpoints under construction"} 