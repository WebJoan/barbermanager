from ninja import Schema
from typing import List, Optional, Dict, Any
from datetime import date, time


class AdminProfileResponseSchema(Schema):
    profile: Dict[str, Any]


class BarberProfileSchema(Schema):
    id: int
    role: str
    is_active: bool
    username: str
    email: Optional[str]
    profile_image: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    description: Optional[str]
    total_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    ongoing_appointments: int
    total_revenue: float
    total_reviews: int
    average_rating: float


class BarbersListResponseSchema(Schema):
    barbers: List[BarberProfileSchema]


class ClientProfileSchema(Schema):
    id: int
    role: str
    is_active: bool
    username: str
    email: Optional[str]
    profile_image: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    phone_number: Optional[str]
    total_appointments: int
    completed_appointments: int
    ongoing_appointments: int
    total_revenue: float
    total_reviews: int
    next_appointment: Optional[Dict[str, Any]]


class ClientsListResponseSchema(Schema):
    clients: List[ClientProfileSchema]


class AppointmentSchema(Schema):
    id: int
    date: date
    slot: time
    status: str
    client: Dict[str, Any]
    barber: Dict[str, Any]
    services: List[Dict[str, Any]]
    service_ids: List[int]
    total_price: float
    created_at: str
    edited_at: str
    reminder_email_sent: bool


class AppointmentsListResponseSchema(Schema):
    appointments: List[AppointmentSchema]


class InviteBarberSchema(Schema):
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    description: Optional[str] = None


class MessageResponseSchema(Schema):
    detail: str 