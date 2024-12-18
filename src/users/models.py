"""User models."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User model.

    Attributes:
        - id: UUID field representing the user's unique identifier
        - password: CharField representing the user's password
        - last_login: DateTimeField representing when the user was last logged in
        - is_active: BooleanField representing whether the user is active
        - is_staff: BooleanField representing whether the user is a staff member
        - is_superuser: BooleanField representing whether the user is a superuser
        - first_name: CharField representing the user's first name
        - last_name: CharField representing the user's last name
        - email: EmailField representing the user's email address
        - groups: ManyToManyField to the user's groups
        - user_permissions: ManyToManyField to the user's user permissions
        - date_joined: DateTimeField representing when the user was created

    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self) -> str:
        """Return the user's id."""
        return str(self.id)
