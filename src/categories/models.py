"""Models for the categories app."""

import uuid

from colorfield.fields import ColorField
from django.db import models


class Category(models.Model):
    """A category for a group or an expense."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=50)

    emoji = models.CharField(max_length=2, null=True, blank=True)

    icon = models.ImageField(upload_to="categories/icons/", null=True, blank=True)

    background_color = ColorField(null=True, blank=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_main_category(self) -> bool:
        """Return True if this is a main category (has no parent)."""
        return self.parent is None

    @property
    def is_subcategory(self) -> bool:
        """Return True if this is a subcategory (has a parent)."""
        return self.parent is not None

    def __str__(self) -> str:
        """Return the name of the category."""
        return self.name
