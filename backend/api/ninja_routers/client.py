from ninja import Router
from ninja.errors import HttpError
from typing import List

from ..ninja_schemas.client import (
    ClientProfileResponseSchema,
    UpdateClientProfileSchema,
    ClientAppointmentsResponseSchema,
    CreateClientAppointmentSchema,
    ClientReviewsResponseSchema,
    CreateClientReviewSchema,
    UpdateClientReviewSchema,
    MessageResponseSchema,
)
from ..models import User, Client, Appointment, Review, Barber, Service
from ..utils.mixins import (
    GetAppointmentsMixin, 
    GetReviewsMixin,
    AppointmentValidationMixin,
    ReviewValidationMixin,
    UsernameValidationMixin,
    PhoneNumberValidationMixin
)
from ..ninja_auth import JWTAuth

router = Router()
jwt_auth = JWTAuth()


def check_client_permission(request):
    """Helper function to check if user is client"""
    from ..models import Roles
    if not request.auth or request.auth.role != Roles.CLIENT.value:
        raise HttpError(403, "Client access required")
    return request.auth


class ClientProfileHandler(UsernameValidationMixin, PhoneNumberValidationMixin):
    """Handler for client profile operations"""
    
    def get_profile(self, client):
        """Get client profile data"""
        return client.to_dict()
    
    def update_profile(self, client, data):
        """Update client profile"""
        updated = False
        
        # Validate username if provided
        if data.username and data.username != client.username:
            if User.objects.filter(username=data.username).exists():
                raise HttpError(400, f'The username "{data.username}" is already taken.')
            client.username = data.username
            updated = True
            
        # Validate phone number format if provided
        if data.phone_number:
            from ..utils import phone_number_validator
            try:
                phone_number_validator(data.phone_number)
            except:
                raise HttpError(400, "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed (E.164 format).")
            client.phone_number = data.phone_number
            updated = True
            
        # Update other fields
        if data.name:
            client.name = data.name
            updated = True
        if data.surname:
            client.surname = data.surname
            updated = True
            
        if updated:
            client.save()
    
    def delete_profile(self, client):
        """Delete client profile"""
        client.delete()


class ClientAppointmentHandler(GetAppointmentsMixin, AppointmentValidationMixin):
    """Handler for client appointment operations"""
    
    def get_appointments(self, client):
        """Get all appointments for client"""
        return client.appointments
    
    def create_appointment(self, client, barber_id, data):
        """Create new appointment for client"""
        try:
            barber = Barber.objects.get(id=barber_id, is_active=True)
        except Barber.DoesNotExist:
            raise HttpError(404, "Barber not found")
        
        # Validate services belong to barber
        services = Service.objects.filter(id__in=data.service_ids, barber=barber)
        if len(services) != len(data.service_ids):
            raise HttpError(400, "Some services do not belong to this barber")
        
        # Check if client already has ongoing appointment
        from ..models.appointment import AppointmentStatus
        if client.appointments_created.filter(status=AppointmentStatus.ONGOING.value).exists():
            raise HttpError(400, f'Client "{client.username}" already has an ONGOING appointment.')
        
        # Check if appointment already exists for this date
        if client.appointments_created.filter(date=data.date).exists():
            raise HttpError(400, f'Appointment for the date "{data.date}" for the client "{client.username}" already exists.')
        
        # Check if barber is available
        from ..models import Availability
        try:
            availability = Availability.objects.get(barber=barber, date=data.date)
            if data.slot not in availability.slots:
                raise HttpError(400, f'Barber is not available at "{data.slot}" on "{data.date}".')
        except Availability.DoesNotExist:
            raise HttpError(400, f'Barber is not available on "{data.date}".')
        
        # Check if slot is already booked
        if Appointment.objects.filter(barber=barber, date=data.date, slot=data.slot).exists():
            raise HttpError(400, f'Appointment for the date: "{data.date}" in the slot: "{data.slot}" for the barber: "{barber.username}" already exists.')
        
        # Create appointment
        appointment = Appointment.objects.create(
            client=client,
            barber=barber,
            date=data.date,
            slot=data.slot,
            status=AppointmentStatus.ONGOING.value
        )
        appointment.services.set(services)
        appointment.save()
    
    def cancel_appointment(self, client, appointment_id):
        """Cancel client appointment"""
        try:
            appointment = client.appointments_created.get(id=appointment_id)
        except Appointment.DoesNotExist:
            raise HttpError(404, f'Appointment with ID "{appointment_id}" for the client: "{client.username}" does not exist.')
        
        from ..models.appointment import AppointmentStatus
        if appointment.status != AppointmentStatus.ONGOING.value:
            raise HttpError(400, 'Only ONGOING appointments can be cancelled.')
        
        appointment.status = AppointmentStatus.CANCELLED.value
        appointment.save()


class ClientReviewHandler(GetReviewsMixin, ReviewValidationMixin):
    """Handler for client review operations"""
    
    def get_reviews(self, client):
        """Get all reviews for client"""
        return client.reviews
    
    def create_review(self, client, appointment_id, data):
        """Create new review for appointment"""
        try:
            appointment = client.appointments_created.get(id=appointment_id)
        except Appointment.DoesNotExist:
            raise HttpError(404, f'Appointment with ID: "{appointment_id}" for the client: "{client.username}" does not exist.')
        
        from ..models.appointment import AppointmentStatus
        if appointment.status != AppointmentStatus.COMPLETED.value:
            raise HttpError(400, 'Only COMPLETED appointments can be reviewed.')
        
        # Check if review already exists
        if Review.objects.filter(client=client, barber=appointment.barber).exists():
            raise HttpError(400, f'Client: "{client.username}" review for the barber: "{appointment.barber.username}" already exists.')
        
        # Create review
        Review.objects.create(
            client=client,
            barber=appointment.barber,
            appointment=appointment,
            rating=data.rating,
            comment=data.comment
        )
    
    def update_review(self, client, review_id, data):
        """Update client review"""
        try:
            review = client.client_reviews.get(id=review_id)
        except Review.DoesNotExist:
            raise HttpError(404, f'Review with the ID: "{review_id}" for the client: "{client.username}" does not exist.')
        
        if data.rating is not None:
            review.rating = data.rating
        if data.comment is not None:
            review.comment = data.comment
        
        from django.utils import timezone
        review.edited_at = timezone.now()
        review.save()
    
    def delete_review(self, client, review_id):
        """Delete client review"""
        try:
            review = client.client_reviews.get(id=review_id)
        except Review.DoesNotExist:
            raise HttpError(404, f'Review with the ID: "{review_id}" for the client: "{client.username}" does not exist.')
        
        review.delete()


# Initialize handlers
profile_handler = ClientProfileHandler()
appointment_handler = ClientAppointmentHandler()
review_handler = ClientReviewHandler()


@router.get("/profile", response=ClientProfileResponseSchema, auth=jwt_auth)
def get_client_profile(request):
    """
    Client only: Get all related profile information for the authenticated client.
    """
    client = check_client_permission(request)
    return profile_handler.get_profile(client)


@router.patch("/profile", response=MessageResponseSchema, auth=jwt_auth)
def update_client_profile(request, data: UpdateClientProfileSchema):
    """
    Client only: Update general profile information for the authenticated client.
    """
    client = check_client_permission(request)
    profile_handler.update_profile(client, data)
    return {"detail": "Profile info updated successfully."}


@router.delete("/profile", response=MessageResponseSchema, auth=jwt_auth)
def delete_client_profile(request):
    """
    Client only: Delete the account of the authenticated client.
    """
    client = check_client_permission(request)
    profile_handler.delete_profile(client)
    return {"detail": "Profile deleted successfully."}


@router.get("/appointments", response=ClientAppointmentsResponseSchema, auth=jwt_auth)
def get_client_appointments(request):
    """
    Client only: Get all appointments for the authenticated client.
    """
    client = check_client_permission(request)
    appointments = appointment_handler.get_appointments(client)
    return {"appointments": appointments}


@router.post("/appointments/{barber_id}", response=MessageResponseSchema, auth=jwt_auth)
def create_client_appointment(request, barber_id: int, data: CreateClientAppointmentSchema):
    """
    Client only: Create an appointment for the authenticated client.
    """
    client = check_client_permission(request)
    appointment_handler.create_appointment(client, barber_id, data)
    return {"detail": "Appointment added successfully."}


@router.delete("/appointments/{appointment_id}", response=MessageResponseSchema, auth=jwt_auth)
def cancel_client_appointment(request, appointment_id: int):
    """
    Client only: Cancel an ongoing appointment for the authenticated client.
    """
    client = check_client_permission(request)
    appointment_handler.cancel_appointment(client, appointment_id)
    return {"detail": "Appointment cancelled successfully."}


@router.get("/reviews", response=ClientReviewsResponseSchema, auth=jwt_auth)
def get_client_reviews(request):
    """
    Client only: Get all reviews posted by the authenticated client.
    """
    client = check_client_permission(request)
    reviews = review_handler.get_reviews(client)
    return {"reviews": reviews}


@router.post("/reviews/{appointment_id}", response=MessageResponseSchema, auth=jwt_auth)
def create_client_review(request, appointment_id: int, data: CreateClientReviewSchema):
    """
    Client only: Create a review for a completed appointment.
    """
    client = check_client_permission(request)
    review_handler.create_review(client, appointment_id, data)
    return {"detail": "Review created successfully."}


@router.patch("/reviews/{review_id}", response=MessageResponseSchema, auth=jwt_auth)
def update_client_review(request, review_id: int, data: UpdateClientReviewSchema):
    """
    Client only: Update a review by the authenticated client.
    """
    client = check_client_permission(request)
    review_handler.update_review(client, review_id, data)
    return {"detail": "Review updated successfully."}


@router.delete("/reviews/{review_id}", response=MessageResponseSchema, auth=jwt_auth)
def delete_client_review(request, review_id: int):
    """
    Client only: Delete a review by the authenticated client.
    """
    client = check_client_permission(request)
    review_handler.delete_review(client, review_id)
    return {"detail": "Review deleted successfully."} 