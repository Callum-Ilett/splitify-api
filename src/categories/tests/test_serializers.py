"""Test the Category serializer."""

import pytest

from categories.serializers import CategorySerializer
from categories.tests.test_helpers import create_test_category
from core.test_helpers import create_test_image


@pytest.mark.django_db
def test_serializer_valid() -> None:
    """Test the Category serializer."""
    # Arrange
    data = {}
    data["name"] = "Entertainment"

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_optional_fields_valid() -> None:
    """Test that the Category optional fields are valid."""
    # Arrange
    icon_file = create_test_image()

    data = {}
    data["name"] = "Entertainment"
    data["emoji"] = "🍿"
    data["parent"] = None
    data["background_color"] = "#000000"
    data["icon"] = icon_file

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_parent_valid() -> None:
    """Test that the Category parent field is valid."""
    # Arrange
    parent_category = create_test_category()

    data = {}
    data["name"] = "Entertainment"
    data["emoji"] = "🍿"
    data["parent"] = str(parent_category.id)

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_non_required_fields_optional_valid() -> None:
    """Test that the Category emoji max length is 2 characters."""
    # Arrange
    data = {}
    data["name"] = "Entertainment"
    data["emoji"] = "🍿"
    data["background_color"] = "#000000"

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_name_empty_required_invalid() -> None:
    """Test that name is required and invalid if it is not provided."""
    # Arrange
    data = {}
    data["name"] = ""

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"name": ["This field may not be blank."]}


@pytest.mark.django_db
def test_name_none_invalid() -> None:
    """Test that name is required and invalid if it is not provided."""
    # Arrange
    data = {}
    data["name"] = None

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"name": ["This field may not be null."]}


@pytest.mark.django_db
def test_name_max_length_invalid() -> None:
    """Test that the Category name max length is 50 characters."""
    # Arrange
    data = {}
    data["name"] = "a" * 51

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "name": ["Ensure this field has no more than 50 characters."]
    }


@pytest.mark.django_db
def test_emoji_max_length_invalid() -> None:
    """Test that the Category emoji max length is 2 characters."""
    # Arrange
    data = {}
    data["name"] = "Entertainment"
    data["emoji"] = "a" * 3

    # Act
    serializer = CategorySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "emoji": ["Ensure this field has no more than 2 characters."]
    }
