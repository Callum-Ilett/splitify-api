"""Group model."""

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from currency.models import Currency


class GroupMemberRole(models.TextChoices):
    """Group member role choices."""

    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"
    OWNER = "owner", "Owner"


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
        Currency, on_delete=models.PROTECT, related_name="associated_groups"
    )

    image = models.ImageField(upload_to="groups/images/", null=True, blank=True)

    members = models.ManyToManyField(
        get_user_model(), through="GroupMember", related_name="joined_groups"
    )

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


class GroupMember(models.Model):
    """Model representing a group member."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="group_members"
    )

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_members"
    )

    role = models.CharField(
        max_length=50, choices=GroupMemberRole.choices, default=GroupMemberRole.MEMBER
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the string representation of the group member."""
        return f"{self.user.username} - {self.group.title}"


@receiver(post_save, sender=Group)
def create_group_member(sender, instance, created, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """
    Create an owner group member when a new group is created.

    This signal handler automatically creates a GroupMember instance with the owner role
    for the user who created the group, but only if the group is newly created.
    """
    if created and instance.members.count() == 0:
        GroupMember.objects.create(
            group=instance, user=instance.created_by, role=GroupMemberRole.OWNER
        )
