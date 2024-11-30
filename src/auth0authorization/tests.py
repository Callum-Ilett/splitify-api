"""Tests for the auth0authorization app."""

import json

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import Client
from rest_framework import status


def create_test_user() -> AbstractUser:
    """Create a test user."""
    user_model = get_user_model()
    return user_model.objects.create_user(
        "testuser", "testuser@email.com", "testpassword"
    )


def test_public(client: Client) -> None:
    """Test the public endpoint."""
    # Arrange
    url = "/api/public"

    # Act
    response = client.get(url)
    content = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content["message"] == "This is a public endpoint!"


def test_private_401(client: Client) -> None:
    """Test the private endpoint returns 401 when not authenticated."""
    # Arrange
    url = "/api/private"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_private_200(client: Client) -> None:
    """Test the private endpoint returns 200 when authenticated."""
    # Arrange
    url = "/api/private"

    user = create_test_user()
    client.force_login(user)

    # Act
    response = client.get(url)
    content = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content["message"] == "This is a private endpoint!"
