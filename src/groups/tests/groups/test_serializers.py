"""Test the Group serializer."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from core.test_helpers import create_test_image
from currency.tests.test_helpers import create_test_currency
from groups.serializers import GroupSerializer


@pytest.mark.django_db
def test_group_valid() -> None:
    """Test that the serializer is valid with correct data."""
    # Arrange
    currency = create_test_currency()

    group = {
        "title": "Miami Summer 2024 Squad",
        "currency": str(currency.id),
    }

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_image_added_valid() -> None:
    """Test that the serializer accepts a valid image."""
    # Arrange
    currency = create_test_currency()

    # Create a test image
    image_file = create_test_image()

    group = {
        "title": "Miami Summer 2024 Squad",
        "currency": str(currency.id),
        "image": image_file,
    }

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_image_optional_valid() -> None:
    """Test that image field is optional."""
    # Arrange
    currency = create_test_currency()

    group = {
        "title": "Miami Summer 2024 Squad",
        "currency": str(currency.id),
    }

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_title_blank_invalid() -> None:
    """Test that the Group title is required."""
    # Arrange
    currency = create_test_currency()

    group = {"title": "", "currency": str(currency.id)}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"title": ["This field may not be blank."]}


@pytest.mark.django_db
def test_title_null_invalid() -> None:
    """Test that the Group title is required."""
    # Arrange
    currency = create_test_currency()

    group = {"title": None, "currency": str(currency.id)}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "title": ["This field may not be null."],
    }


@pytest.mark.django_db
def test_title_required_invalid() -> None:
    """Test that the Group title is required."""
    # Arrange
    currency = create_test_currency()

    group = {"currency": str(currency.id)}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"title": ["This field is required."]}


@pytest.mark.django_db
def test_title_max_length_invalid() -> None:
    """Test that the Group title max length is 255 characters."""
    # Arrange
    currency = create_test_currency()

    group = {"title": "a" * 256, "currency": str(currency.id)}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "title": ["Ensure this field has no more than 255 characters."]
    }


@pytest.mark.django_db
def test_currency_invalid() -> None:
    """Test that the serializer rejects non-existent currency IDs."""
    # Arrange
    currency_id = "fc49ca12-b54b-49e8-94e3-e8c49e894e3e"

    group = {
        "title": "Miami Summer 2024 Squad",
        "description": "Planning our Miami beach vacation!",
        "currency": currency_id,
    }

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "currency": [
            'Invalid pk "fc49ca12-b54b-49e8-94e3-e8c49e894e3e" - object does not exist.'
        ]
    }


@pytest.mark.django_db
def test_currency_required_invalid() -> None:
    """Test that the serializer rejects non-existent currency IDs."""
    # Arrange
    group = {"title": "Miami Summer 2024 Squad"}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"currency": ["This field is required."]}


@pytest.mark.django_db
def test_currency_none_invalid() -> None:
    """Test that the serializer rejects."""
    # Arrange
    group = {"title": "Miami Summer 2024 Squad", "currency": None}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"currency": ["This field may not be null."]}


@pytest.mark.django_db
def test_currency_blank_invalid() -> None:
    """Test that the serializer rejects blank currency IDs."""
    # Arrange
    group = {"title": "Miami Summer 2024 Squad", "currency": ""}

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"currency": ["This field may not be null."]}


@pytest.mark.django_db
def test_image_invalid_format() -> None:
    """Test that the serializer rejects invalid image formats."""
    # Arrange
    currency = create_test_currency()

    # Create an invalid file
    invalid_file = SimpleUploadedFile(
        name="test.txt", content=b"invalid image content", content_type="text/plain"
    )

    group = {
        "title": "Miami Summer 2024 Squad",
        "currency": str(currency.id),
        "image": invalid_file,
    }

    # Act
    serializer = GroupSerializer(data=group)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid

    assert serializer.errors == {
        "image": [
            "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        ]
    }
