"""Helper functions for testing."""

import io

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def create_test_user(
    username: str = "testuser",
    email: str = "testuser@email.com",
) -> AbstractUser:
    """Create a test user if it doesn't exist, otherwise return existing user."""
    user_model = get_user_model()

    user, _ = user_model.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "password": "testpassword",
        },
    )

    return user


def create_test_image() -> SimpleUploadedFile:
    """Create a test image file."""
    image = Image.new("RGB", (100, 100), color="red")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    return SimpleUploadedFile(
        name="test.png", content=img_byte_arr, content_type="image/png"
    )
