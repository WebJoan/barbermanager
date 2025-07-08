from .auth import router as auth_router
from .admin import router as admin_router
from .barber import router as barber_router
from .client import router as client_router
from .public import router as public_router
from .image import router as image_router

__all__ = [
    'auth_router',
    'admin_router', 
    'barber_router',
    'client_router',
    'public_router',
    'image_router',
] 