from ninja import Schema
from typing import List, Optional
from datetime import datetime, date, time


# Barber schemas
class PublicBarberSchema(Schema):
    id: int
    username: str
    name: str
    surname: str
    description: Optional[str]
    profile_image: Optional[str]
    average_rating: float
    completed_appointments: int
    total_revenue: float


class BarbersListResponseSchema(Schema):
    barbers: List[PublicBarberSchema]


class BarberProfilePublicResponseSchema(Schema):
    id: int
    username: str
    name: str
    surname: str
    description: Optional[str]
    profile_image: Optional[str]
    services: List[dict]
    availabilities: List[dict]
    reviews: List[dict]
    average_rating: float
    completed_appointments: int
    total_revenue: float


# Client schemas
class PublicClientSchema(Schema):
    id: int
    username: str
    profile_image: Optional[str]
    completed_appointments: int


class ClientProfilePublicResponseSchema(Schema):
    id: int
    username: str
    profile_image: Optional[str]
    completed_appointments: int
    reviews: List[dict]


# Service schemas
class ServiceSchema(Schema):
    id: int
    name: str
    description: Optional[str]
    price: float
    duration: int


class BarberServicesResponseSchema(Schema):
    services: List[ServiceSchema]


# Availability schemas
class AvailabilitySchema(Schema):
    id: int
    date: date
    slots: List[time]


class BarberAvailabilitiesResponseSchema(Schema):
    availabilities: List[AvailabilitySchema] 