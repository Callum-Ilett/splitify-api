"""Test the Currency serializer."""

import pytest

from currency.serializers import CurrencySerializer


@pytest.mark.django_db
def test_currency_serializer() -> None:
    """Test the Currency serializer."""
    # Arrange
    data = {}
    data["name"] = "United States Dollar"
    data["symbol"] = "$"
    data["code"] = "USD"

    # Act
    serializer = CurrencySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_name_max_length() -> None:
    """Test that the Currency name max length is 50 characters."""
    # Arrange
    data = {}
    data["name"] = "a" * 51
    data["symbol"] = "$"
    data["code"] = "USD"

    # Act
    serializer = CurrencySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "name": ["Ensure this field has no more than 50 characters."]
    }


@pytest.mark.django_db
def test_symbol_max_length() -> None:
    """Test that the Currency symbol max length is 5 characters."""
    # Arrange
    data = {}
    data["name"] = "United States Dollar"
    data["symbol"] = "a" * 6
    data["code"] = "USD"

    # Act
    serializer = CurrencySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "symbol": ["Ensure this field has no more than 5 characters."]
    }


@pytest.mark.django_db
def test_code_max_length() -> None:
    """Test that the Currency code max length is 5 characters."""
    # Arrange
    data = {}
    data["name"] = "United States Dollar"
    data["symbol"] = "$"
    data["code"] = "a" * 6

    # Act
    serializer = CurrencySerializer(data=data)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {
        "code": ["Ensure this field has no more than 5 characters."]
    }
