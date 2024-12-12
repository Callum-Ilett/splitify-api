"""Test update group."""

import pytest
from django.test import Client
from django.test.client import encode_multipart
from rest_framework import status

from core.test_helpers import create_test_image, create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.tests.groups.test_helpers import create_test_group


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
        "description": "Crazy going in the winter! What to wear?",
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
    assert response_data["description"] == "Crazy going in the winter! What to wear?"
    assert response_data["currency"] == str(currency.id)
    assert response_data["created_by"] == user.id  # type: ignore
    assert response_data["updated_by"] == user.id  # type: ignore
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_update_patch_group_image_success(client: Client) -> None:
    """Test that a group can be updated with an image."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    image = create_test_image()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    payload = {
        "image": image,
    }

    client.force_login(user)

    # Act
    response = client.patch(
        f"/api/groups/{group.id}/",
        data=encode_multipart(data=payload, boundary="BoUnDaRyStRiNg"),
        content_type="multipart/form-data; boundary=BoUnDaRyStRiNg",
    )
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert response_data["id"] == str(group.id)
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["image"] is not None
    assert response_data["image"].startswith("http://testserver/media/groups/images/")
    assert response_data["image"].endswith(".png")
    assert response_data["created_by"] == user.id  # type: ignore
    assert response_data["updated_by"] == user.id  # type: ignore
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_update_put_group_image_success(client: Client) -> None:
    """Test that a group can be updated with an image."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    image = create_test_image()

    group = create_test_group(
        currency=currency,
        created_by=user,
    )

    payload = {
        "title": "Miami Winter 2025(edited)🌴",
        "description": "Crazy going in the winter! What to wear?",
        "currency": str(currency.id),
        "image": image,
    }

    client.force_login(user)

    # Act
    response = client.put(
        f"/api/groups/{group.id}/",
        data=encode_multipart(data=payload, boundary="BoUnDaRyStRiNg"),
        content_type="multipart/form-data; boundary=BoUnDaRyStRiNg",
    )
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert response_data["id"] == str(group.id)
    assert response_data["title"] == "Miami Winter 2025(edited)🌴"
    assert response_data["description"] == "Crazy going in the winter! What to wear?"
    assert response_data["currency"] == str(currency.id)
    assert response_data["image"] is not None
    assert response_data["image"].startswith("http://testserver/media/groups/images/")
    assert response_data["image"].endswith(".png")
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
