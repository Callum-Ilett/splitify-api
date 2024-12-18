"""Test cases for creating a group."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from rest_framework import status

from categories.tests.test_helpers import create_emoji_test_category
from core.test_helpers import create_test_image, create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.tests.groups.test_delete_group import create_test_group


@pytest.mark.django_db
def test_create_group_success(client: Client) -> None:
    """Test that a group can be created successfully."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED

    assert response_data["id"]
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["created_by"] == str(user.pk)
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_create_group_with_categories_success(client: Client) -> None:
    """Test that a group can be created with categories successfully."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    category_1 = create_emoji_test_category(name="Trip", emoji="🛫")
    category_2 = create_emoji_test_category(name="Holiday", emoji="🏖️")

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
        "categories": [str(category_1.id), str(category_2.id)],
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED

    assert response_data["id"]
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["categories"] == [str(category_1.id), str(category_2.id)]
    assert response_data["created_by"] == str(user.pk)
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_image_multipart_form_data_success(client: Client) -> None:
    """Test that a group can be created with an image using multipart form data."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    image = create_test_image()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
        "image": image,
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, format="multipart/form-data")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED

    assert response_data["id"]
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["image"] is not None
    assert response_data["image"] == "http://testserver/media/groups/images/test.png"
    assert response_data["created_by"] == str(user.pk)
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_invalid_image_format_fails(client: Client) -> None:
    """Test that uploading an invalid image format fails."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    # Create an invalid file
    invalid_file = SimpleUploadedFile(
        name="test.txt", content=b"invalid image content", content_type="text/plain"
    )

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
        "image": invalid_file,
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, format="multipart")
    response_data = response.json()

    expected_error = "Upload a valid image. The file you uploaded was either not an image or a corrupted image."

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["image"][0] == expected_error


@pytest.mark.django_db
def test_unauthenticated_fails(client: Client) -> None:
    """Test that an unauthenticated user cannot create a group."""
    # Arrange
    currency = create_test_currency()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    # Act
    response = client.post("/api/groups/", payload, "application/json")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_existing_title_other_user_success(client: Client) -> None:
    """Test that duplicate group titles from different users are allowed."""
    # Arrange
    user_1 = create_test_user(username="user_1", email="user_1@email.com")
    user_2 = create_test_user(username="user_2", email="user_2@email.com")

    currency = create_test_currency()

    create_test_group(
        title="Miami Summer 2024 Squad 🌴",
        currency=currency,
        created_by=user_1,
    )

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user_2)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED

    assert response_data["id"]
    assert response_data["title"] == "Miami Summer 2024 Squad 🌴"
    assert response_data["description"] == "Planning our Miami beach vacation!"
    assert response_data["currency"] == str(currency.id)
    assert response_data["created_by"] == str(user_2.pk)
    assert response_data["updated_by"] is None
    assert response_data["created_at"]
    assert response_data["updated_at"]


@pytest.mark.django_db
def test_existing_title_fails(client: Client) -> None:
    """Test that duplicate group titles from same user are not allowed."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    create_test_group(
        title="Miami Summer 2024 Squad 🌴", created_by=user, currency=currency
    )

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    expected_error = "A group with this title already exists for this user."

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data["title"][0] == expected_error


@pytest.mark.django_db
def test_existing_title_case_insensitive_fails(client: Client) -> None:
    """Test that duplicate group titles from same user are not allowed."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    create_test_group(
        title="Miami Summer 2024 Squad 🌴", created_by=user, currency=currency
    )

    payload = {
        "title": "MIAMI SuMMer 2024 sQuAd 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    expected_error = "A group with this title already exists for this user."
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data["title"][0] == expected_error


@pytest.mark.django_db
def test_required_fields_fails(client: Client) -> None:
    """Test that a group cannot be created without title and currency."""
    # Arrange
    user = create_test_user()

    payload = {"description": "Planning our Miami beach vacation!"}

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["title"][0] == "This field is required."
    assert response_data["currency"][0] == "This field is required."


@pytest.mark.django_db
def test_title_empty_fails(client: Client) -> None:
    """Test that a group cannot be created with an empty title."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    payload = {
        "title": "",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["title"][0] == "This field may not be blank."


@pytest.mark.django_db
def test_title_none_fails(client: Client) -> None:
    """Test that a group cannot be created with a title of None."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    payload = {
        "title": None,
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["title"][0] == "This field may not be null."


@pytest.mark.django_db
def test_title_too_long_fails(client: Client) -> None:
    """Test that a group cannot be created with a title that exceeds 255 characters."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    payload = {
        "title": "a" * 256,
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    expected_error = "Ensure this field has no more than 255 characters."

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["title"][0] == expected_error


@pytest.mark.django_db
def test_currency_empty_fails(client: Client) -> None:
    """Test that a group cannot be created without a currency."""
    # Arrange
    user = create_test_user()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": "",
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["currency"][0] == "This field may not be null."


@pytest.mark.django_db
def test_currency_none_fails(client: Client) -> None:
    """Test that a group cannot be created without a currency."""
    # Arrange
    user = create_test_user()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": None,
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["currency"][0] == "This field may not be null."


@pytest.mark.django_db
def test_currency_undefined_fails(client: Client) -> None:
    """Test that a group cannot be created without a currency."""
    # Arrange
    user = create_test_user()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["currency"][0] == "This field is required."


@pytest.mark.django_db
def test_create_group_with_json_and_image_fails(client: Client) -> None:
    """Test that a group cannot be created with an image using JSON content type."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
        "image": "some_base64_image_data",  # This should fail
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert (
        response_data["image"][0]
        == "The submitted data was not a file. Check the encoding type on the form."
    )


@pytest.mark.django_db
def test_create_group_with_invalid_category_fails(client: Client) -> None:
    """Test that a group cannot be created with a non-existent category."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    invalid_category_id = "12345678-1234-5678-1234-567812345678"

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
        "categories": [invalid_category_id],
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response_data["categories"][0]
        == 'Invalid pk "12345678-1234-5678-1234-567812345678" - object does not exist.'
    )


@pytest.mark.django_db
def test_create_group_with_invalid_category_format_fails(client: Client) -> None:
    """Test that a group cannot be created with malformed category IDs."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    payload = {
        "title": "Miami Summer 2024 Squad 🌴",
        "description": "Planning our Miami beach vacation!",
        "currency": str(currency.id),
        "categories": ["not-a-uuid"],
    }

    client.force_login(user)

    # Act
    response = client.post("/api/groups/", payload, "application/json")
    response_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data["categories"][0] == "“not-a-uuid” is not a valid UUID."
