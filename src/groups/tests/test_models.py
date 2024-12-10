"""Test the Group model."""

import pytest
from django.contrib.auth import get_user_model

from currency.models import Currency
from groups.models import Group


@pytest.mark.django_db
def test_group_currency() -> None:
    """Test that a group can be associated with a currency."""
    # Arrange
    currency = Currency()
    currency.code = "USD"
    currency.name = "United States Dollar"
    currency.symbol = "$"

    group = Group()
    group.title = "Miami Summer 2024 Squad 🌴"
    group.description = "Planning our Miami beach vacation!"
    group.currency = currency

    # Act
    currency.save()
    group.save()

    # Assert
    assert group.title == "Miami Summer 2024 Squad 🌴"
    assert group.description == "Planning our Miami beach vacation!"
    assert group.currency == currency
    assert group.created_by is None
    assert group.updated_by is None
    assert group.created_at
    assert group.updated_at

    assert str(group) == group.title


@pytest.mark.django_db
def test_group_model_audit() -> None:
    """Test that a group tracks the user who created and last updated it."""
    # Arrange

    # Create a currency
    currency = Currency()
    currency.code = "USD"
    currency.name = "United States Dollar"
    currency.symbol = "$"

    # Create a user
    user = get_user_model().objects.create()
    user.username = "testuser"
    user.email = "testuser@example.com"
    user.password = "testpassword"
    user.save()

    # Create a group
    group = Group()
    group.title = "Miami Summer 2024 Squad 🌴"
    group.description = "Planning our Miami beach vacation!"
    group.currency = currency
    group.created_by = user
    group.updated_by = user

    # Act
    currency.save()
    group.save()

    # Assert
    assert group.title == "Miami Summer 2024 Squad 🌴"
    assert group.description == "Planning our Miami beach vacation!"
    assert group.created_by == user
    assert group.updated_by == user

    assert group.created_at
    assert group.updated_at

    assert str(group) == group.title
