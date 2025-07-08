from ninja import Schema, File
from ninja.files import UploadedFile
from typing import Optional


# Input schemas
class UploadProfileImageSchema(Schema):
    profile_image: UploadedFile


# Response schemas  
class ImageUploadResponseSchema(Schema):
    detail: str
    image_url: Optional[str] = None


class MessageResponseSchema(Schema):
    detail: str 