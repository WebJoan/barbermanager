from ninja import NinjaAPI
from .ninja_auth import JWTAuth
from .ninja_routers import auth_router, admin_router, barber_router, client_router, public_router, image_router


# Create the main API instance
api = NinjaAPI(
    title="Barber Manager API",
    description="Manage barbershop scheduling, reviews, and users.",
    version="1.0.0",
    docs_url="/docs/",
)

# JWT Auth instance
jwt_auth = JWTAuth()

# Add routers
api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/admin", admin_router, tags=["Admin"], auth=jwt_auth)
api.add_router("/barber", barber_router, tags=["Barber"], auth=jwt_auth)
api.add_router("/client", client_router, tags=["Client"], auth=jwt_auth)
api.add_router("/public", public_router, tags=["Public"])
api.add_router("/image", image_router, tags=["Images"], auth=jwt_auth) 