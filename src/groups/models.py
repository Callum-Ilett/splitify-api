"""Group model."""

import uuid

from django.contrib.auth import get_user_model
from django.db import models

from currency.models import Currency


class Group(models.Model):
    """
    Model representing a group.

    - id: UUID field representing the group's unique identifier.
    - title: CharField representing the group's title.
    - description: TextField representing the group's description.
    - created_at: DateTimeField representing the group's creation date and time.
    - updated_at: DateTimeField representing the group's last update date and time.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)

    description = models.TextField(null=True, blank=True)

    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, related_name="groups"
    )

    image = models.ImageField(upload_to="groups/images/", null=True, blank=True)

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_groups",
    )

    updated_by = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_groups",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the string representation of the group."""
        return self.title
