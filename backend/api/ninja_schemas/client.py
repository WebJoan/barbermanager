from ninja import Schema
from typing import List, Optional
from datetime import datetime, date, time


# Response schemas
class ClientProfileResponseSchema(Schema):
    id: int
    role: str
    is_active: bool
    username: str
    email: str
    profile_image: Optional[str]
    name: str
    surname: str
    phone_number: Optional[str]
    appointments: List[dict]
    completed_appointments: int
    next_appointment: Optional[dict]
    reviews: List[dict]


class ClientAppointmentSchema(Schema):
    id: int
    barber_id: int
    client_id: int
    date: date
    slot: time
    status: str
    services: List[dict]
    created_at: datetime
    edited_at: Optional[datetime]


class ClientAppointmentsResponseSchema(Schema):
    appointments: List[ClientAppointmentSchema]


class ClientReviewSchema(Schema):
    id: int
    client_id: int
    barber_id: int
    appointment_id: int
    rating: int
    comment: str
    created_at: datetime
    edited_at: Optional[datetime]


class ClientReviewsResponseSchema(Schema):
    reviews: List[ClientReviewSchema]


# Input schemas
class UpdateClientProfileSchema(Schema):
    username: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    phone_number: Optional[str] = None


class CreateClientAppointmentSchema(Schema):
    date: date
    slot: time
    service_ids: List[int]


class CreateClientReviewSchema(Schema):
    rating: int
    comment: str


class UpdateClientReviewSchema(Schema):
    rating: Optional[int] = None
    comment: Optional[str] = None


# Common response schema
class MessageResponseSchema(Schema):
    detail: str 