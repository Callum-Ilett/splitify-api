"""User models."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self) -> str:
        """Return the user's id."""
        return str(self.id)
