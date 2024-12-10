"""Test the Group serializer."""

import pytest

from currency.models import Currency
from groups.serializers import GroupSerializer


@pytest.mark.django_db
def test_group_valid() -> None:
    """Test that the serializer is valid with correct data."""
    # Arrange
    currency = Currency()
    currency.name = "United States Dollar"
    currency.symbol = "$"
    currency.code = "USD"
    currency.save()

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
    currency = Currency()
    currency.name = "United States Dollar"
    currency.symbol = "$"
    currency.code = "USD"
    currency.save()

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
    currency = Currency()
    currency.name = "United States Dollar"
    currency.symbol = "$"
    currency.code = "USD"
    currency.save()

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
    currency = Currency()
    currency.name = "United States Dollar"
    currency.symbol = "$"
    currency.code = "USD"
    currency.save()

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
    currency = Currency()
    currency.name = "United States Dollar"
    currency.symbol = "$"
    currency.code = "USD"
    currency.save()

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
