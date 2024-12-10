"""Test update group."""

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
def test_patch_success(client: Client) -> None:
    """Test that a group can be updated successfully."""
    # Arrange
    user = create_test_user()

    group = create_test_group(
        title="Miami Summer 2024 Squad 🌴",
        description="Planning our Miami beach vacation!",
        created_by=user,
    )

    payload = {
        "title": "Miami Summer 2024 Squad(edited)🌴",
    }

    client.force_login(user)

    # Act
    response = client.patch(f"/api/groups/{group.id}/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == str(group.id)
    assert response_data["title"] == "Miami Summer 2024 Squad(edited)🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(group.currency.id)
    assert response_data["created_by"] == user.id  # type: ignore
    assert response_data["updated_by"] == user.id  # type: ignore
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_put_success(client: Client) -> None:
    """Test that a group can be edited successfully."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    payload = {
        "title": "Miami Winter 2025(edited)🌴",
        "description": "Crazyness going in the winter! What to wear?",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.put(
        f"/api/groups/{group.id}/",
        payload,
        "application/json",
    )
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert response_data["id"] == str(group.id)
    assert response_data["title"] == "Miami Winter 2025(edited)🌴"
    assert (
        response_data["description"] == "Crazyness going in the winter! What to wear?"
    )
    assert response_data["currency"] == str(currency.id)
    assert response_data["created_by"] == user.id  # type: ignore
    assert response_data["updated_by"] == user.id  # type: ignore
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_unauthenticated_fails(client: Client) -> None:
    """Test that an unauthenticated user cannot edit a group."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    payload = {
        "title": "Miami Summer 2024 Squad(edited)🌴",
    }

    # Act
    response = client.patch(f"/api/groups/{group.id}/", payload, "application/json")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_empty_title_fails(client: Client) -> None:
    """Test that a group cannot be edited without a title."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    payload = {
        "title": "",
    }

    client.force_login(user)

    # Act
    response = client.patch(
        f"/api/groups/{group.id}/",
        payload,
        "application/json",
    )
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["title"][0] == "This field may not be blank."


@pytest.mark.django_db
def test_invalid_currency_fails(client: Client) -> None:
    """Test that a group cannot be edited with an invalid currency."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    payload = {
        "currency": "invalid_currency_id",
    }

    client.force_login(user)

    # Act
    response = client.patch(
        f"/api/groups/{group.id}/",
        payload,
        "application/json",
    )
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["currency"][0] == "“invalid_currency_id” is not a valid UUID."


@pytest.mark.django_db
def test_nonexistent_group_id_fails(client: Client) -> None:
    """Test that a group cannot be edited with a nonexistent group ID."""
    # Arrange
    user = create_test_user()

    payload = {
        "title": "Miami Summer 2024 Squad (edited)🌴",
    }

    client.force_login(user)

    # Act
    response = client.patch(
        "/api/groups/invalid_group_id/",
        payload,
        "application/json",
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
