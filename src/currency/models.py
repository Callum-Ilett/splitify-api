"""Models for the currency app."""

import uuid

from django.db import models


class Currency(models.Model):
    """Currency model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=50)

    symbol = models.CharField(max_length=5)

    code = models.CharField(max_length=5, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the string representation of the currency."""
        return f"{self.name} ({self.symbol})"
