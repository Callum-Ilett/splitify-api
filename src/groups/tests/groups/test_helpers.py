"""Helper functions for testing groups."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import Group

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

    from currency.models import Currency


def create_test_group(
    title: str = "Miami Summer 2024 Squad 🌴",
    description: str = "Planning our Miami beach vacation!",
    image: str | None = None,
    currency: Currency | None = None,
    created_by: AbstractUser | None = None,
    updated_by: AbstractUser | None = None,
) -> Group:
    """Create a test group."""
    if currency is None:
        currency = create_test_currency()

    if created_by is None:
        created_by = create_test_user()

    return Group.objects.create(
        title=title,
        description=description,
        currency=currency,
        created_by=created_by,
        updated_by=updated_by,
        image=image,
    )
