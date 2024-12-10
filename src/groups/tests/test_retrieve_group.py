"""Test retrieve group."""

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
def test_retrieve_success(client: Client) -> None:
    """Test that a group can be retrieved successfully."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    client.force_login(user)

    # Act
    response = client.get(f"/api/groups/{group.id}/")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert response_data["id"] == str(group.id)
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["created_by"] == user.id  # type: ignore
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_unauthorized_user_fails(client: Client) -> None:
    """Test that an unauthorized user cannot retrieve a group."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    # Act
    response = client.get(f"/api/groups/{group.id}/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_nonexistent_group_id_fails(client: Client) -> None:
    """Test that a group cannot be retrieved with a nonexistent group ID."""
    # Arrange
    user = create_test_user()
    client.force_login(user)

    # Act
    response = client.get("/api/groups/invalid_group_id/")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
