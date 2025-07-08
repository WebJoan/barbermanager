from ninja import Router, File
from ninja.errors import HttpError
from ninja.files import UploadedFile

from ..ninja_schemas.image import (
    ImageUploadResponseSchema,
    MessageResponseSchema,
)
from ..ninja_auth import JWTAuth

router = Router()
jwt_auth = JWTAuth()


class ImageHandler:
    """Handler for image operations"""
    
    def upload_profile_image(self, user, image_file):
        """Upload profile image for user"""
        # Validate file type
        if not image_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise HttpError(400, "Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed.")
        
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if image_file.size > max_size:
            raise HttpError(400, "File size too large. Maximum size is 5MB.")
        
        # Delete old profile image if exists
        if user.profile_image:
            user.profile_image.delete(save=False)
        
        # Save new profile image
        user.profile_image = image_file
        user.save()
        
        return user.profile_image.url if user.profile_image else None
    
    def delete_profile_image(self, user):
        """Delete profile image for user"""
        if not user.profile_image:
            raise HttpError(400, "No profile image to delete.")
        
        # Delete the image file
        user.profile_image.delete(save=False)
        user.profile_image = None
        user.save()


# Initialize handler
image_handler = ImageHandler()


@router.post("/profile", response=ImageUploadResponseSchema, auth=jwt_auth)
def upload_profile_image(request, profile_image: UploadedFile = File(...)):
    """
    Uploads a profile image to the profile of the authenticated user.
    """
    user = request.auth
    if not user:
        raise HttpError(401, "Authentication required")
    
    image_url = image_handler.upload_profile_image(user, profile_image)
    
    return {
        "detail": "Profile picture uploaded successfully.",
        "image_url": image_url
    }


@router.delete("/profile", response=MessageResponseSchema, auth=jwt_auth)
def delete_profile_image(request):
    """
    Deletes the profile picture of the authenticated user.
    """
    user = request.auth
    if not user:
        raise HttpError(401, "Authentication required")
    
    image_handler.delete_profile_image(user)
    
    return {"detail": "Profile picture deleted successfully."} 