"""Test retrieve group."""

import pytest
from django.test import Client
from rest_framework import status

from categories.tests.test_helpers import create_emoji_test_category
from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.tests.groups.test_helpers import create_test_group


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
    assert response_data["created_by"] == str(user.pk)
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_retrieve_image_success(client: Client) -> None:
    """Test that a group with an image can be retrieved successfully."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    image = "test.png"

    group = create_test_group(
        currency=currency,
        image=image,
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
    assert "image" in response_data
    assert response_data["image"] is not None
    assert response_data["created_by"] == str(user.pk)
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_retrieve_group_with_categories_success(client: Client) -> None:
    """Test that a group with categories can be retrieved successfully."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    category_1 = create_emoji_test_category(name="Trip", emoji="🛫")
    category_2 = create_emoji_test_category(name="Holiday", emoji="🏖️")

    group = create_test_group(
        title="Miami Summer 2024 Squad 🌴",
        description="Planning our Miami beach vacation!",
        currency=currency,
        created_by=user,
    )

    group.categories.add(category_1, category_2)

    client.force_login(user)

    # Act
    response = client.get(f"/api/groups/{group.id}/")
    response_data = response.json()

    expected_category_count = 2

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert response_data["id"] == str(group.id)
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["created_by"] == str(user.pk)
    assert len(response_data["categories"]) == expected_category_count
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


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
