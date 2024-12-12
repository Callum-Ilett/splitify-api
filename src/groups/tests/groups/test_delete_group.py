"""Test delete group."""

from __future__ import annotations

import pytest
from django.test import Client  # noqa: TC002
from rest_framework import status

from core.test_helpers import create_test_image, create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import Group
from groups.tests.groups.test_helpers import create_test_group


@pytest.mark.django_db
def test_delete_group_success(client: Client) -> None:
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
def test_delete_group_with_image_success(client: Client) -> None:
    """Test that a group with an image can be deleted."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    image = create_test_image()

    group = Group.objects.create(
        title="Miami Summer 2024 Squad 🌴",
        description="Planning our Miami beach vacation!",
        currency=currency,
        created_by=user,
        image=image,
    )

    client.force_login(user)

    # Act
    response = client.delete(f"/api/groups/{group.id}/")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Group.objects.filter(id=group.id).exists()


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
def test_not_found_fails(client: Client) -> None:
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
