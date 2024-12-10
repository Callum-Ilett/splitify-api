"""Test delete group."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser  # noqa: TC002
from django.test import Client  # noqa: TC002
from rest_framework import status

from currency.models import Currency
from groups.models import Group


def create_test_user(
    username: str = "testuser",
    email: str = "testuser@email.com",
) -> AbstractUser:
    """Create a test user."""
    user_model = get_user_model()

    return user_model.objects.create_user(username, email, "testpassword")


def create_test_currency(
    name: str = "USD",
    symbol: str = "$",
    code: str = "USD",
) -> Currency:
    """Create a test currency."""
    currency_model = Currency
    return currency_model.objects.create(name=name, symbol=symbol, code=code)


def create_test_group(
    title: str = "Miami Summer 2024 Squad 🌴",
    description: str = "Planning our Miami beach vacation!",
    currency: Currency | None = None,
    created_by: AbstractUser | None = None,
    updated_by: AbstractUser | None = None,
) -> Group:
    """Create a test group."""
    if currency is None:
        currency = create_test_currency()

    if created_by is None:
        created_by = create_test_user()

    group = Group()
    group.title = title
    group.description = description
    group.currency = currency
    group.created_by = created_by
    group.updated_by = updated_by
    group.save()

    return group


@pytest.mark.django_db
def test_success(client: Client) -> None:
    """Test that a group can be deleted."""
    # Arrange
    user = create_test_user()
    group = create_test_group(created_by=user)

    client.force_login(user)

    # Act & Assert
    assert Group.objects.count() == 1
    response = client.delete(f"/api/groups/{group.id}/")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert Group.objects.count() == 0


@pytest.mark.django_db
def test_unauthenticated_fails(client: Client) -> None:
    """Test that a group cannot be deleted if the user is not authenticated."""
    # Arrange
    user = create_test_user()
    group = create_test_group(created_by=user)

    # Act & Assert
    assert Group.objects.count() == 1
    response = client.delete(f"/api/groups/{group.id}/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert Group.objects.count() == 1


@pytest.mark.django_db
def test_not_found(client: Client) -> None:
    """Test that a group cannot be deleted if it does not exist."""
    # Arrange
    user = create_test_user()

    client.force_login(user)

    # Act & Assert
    assert Group.objects.count() == 0
    response = client.delete("/api/groups/invalid-id/")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert Group.objects.count() == 0
