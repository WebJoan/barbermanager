from ninja import Router
from ninja.errors import HttpError
from typing import List

from ..ninja_schemas.public import (
    BarbersListResponseSchema,
    BarberProfilePublicResponseSchema,
    ClientProfilePublicResponseSchema,
    BarberServicesResponseSchema,
    BarberAvailabilitiesResponseSchema,
    PublicBarberSchema,
    PublicClientSchema,
    ServiceSchema,
    AvailabilitySchema,
)
from ..models import Barber, Client, Service, Availability
from ..utils.mixins import (
    GetBarbersMixin,
    GetClientsMixin,
    GetServicesMixin,
    GetAvailabilitiesMixin,
)

router = Router()


class PublicBarberHandler(GetBarbersMixin):
    """Handler for public barber operations"""
    
    def get_all_barbers(self):
        """Get all active barbers with public data"""
        return self.get_barbers_public()
    
    def get_barber_profile(self, barber_id):
        """Get public barber profile"""
        try:
            barber = Barber.objects.get(id=barber_id, is_active=True)
        except Barber.DoesNotExist:
            raise HttpError(404, "Barber not found")
        
        # Get public data but keep all fields for profile view
        return barber.to_dict()


class PublicClientHandler(GetClientsMixin):
    """Handler for public client operations"""
    
    def get_client_profile(self, client_id):
        """Get public client profile"""
        try:
            client = Client.objects.get(id=client_id, is_active=True)
        except Client.DoesNotExist:
            raise HttpError(404, "Client not found")
        
        return self.get_client_public(client)


class PublicServiceHandler(GetServicesMixin):
    """Handler for public service operations"""
    
    def get_barber_services(self, barber_id):
        """Get all services for a barber"""
        try:
            barber = Barber.objects.get(id=barber_id, is_active=True)
        except Barber.DoesNotExist:
            raise HttpError(404, "Barber not found")
        
        return self.get_services_public(barber_id)


class PublicAvailabilityHandler(GetAvailabilitiesMixin):
    """Handler for public availability operations"""
    
    def get_barber_availabilities(self, barber_id):
        """Get all availabilities for a barber"""
        try:
            barber = Barber.objects.get(id=barber_id, is_active=True)
        except Barber.DoesNotExist:
            raise HttpError(404, "Barber not found")
        
        return self.get_availabilities_public(barber_id)


# Initialize handlers
barber_handler = PublicBarberHandler()
client_handler = PublicClientHandler()
service_handler = PublicServiceHandler()
availability_handler = PublicAvailabilityHandler()


@router.get("/barbers", response=BarbersListResponseSchema)
def get_barbers_public(request):
    """
    Return a list of all active barbers.
    """
    barbers = barber_handler.get_all_barbers()
    return {"barbers": barbers}


@router.get("/barbers/{barber_id}", response=BarberProfilePublicResponseSchema)
def get_barber_profile_public(request, barber_id: int):
    """
    Get all public profile information for a barber. (Public)
    """
    barber_data = barber_handler.get_barber_profile(barber_id)
    return barber_data


@router.get("/clients/{client_id}", response=ClientProfilePublicResponseSchema)
def get_client_profile_public(request, client_id: int):
    """
    Get all public profile information for a client. (Public)
    """
    client_data = client_handler.get_client_profile(client_id)
    return client_data


@router.get("/barbers/{barber_id}/services", response=BarberServicesResponseSchema)
def get_barber_services_public(request, barber_id: int):
    """
    Get all services for the given barber. (Public)
    """
    services = service_handler.get_barber_services(barber_id)
    return {"services": services}


@router.get("/barbers/{barber_id}/availabilities", response=BarberAvailabilitiesResponseSchema)
def get_barber_availabilities_public(request, barber_id: int):
    """
    Get all availabilities for a specific barber. (Public)
    """
    availabilities = availability_handler.get_barber_availabilities(barber_id)
    return {"availabilities": availabilities} 