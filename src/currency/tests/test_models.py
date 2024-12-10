"""Test the Currency model."""

import pytest

from currency.models import Currency


@pytest.mark.django_db
def test_group_model() -> None:
    """Test the currency model."""
    # Arrange
    currency = Currency()
    currency.name = "United States Dollar"
    currency.symbol = "$"
    currency.code = "USD"

    # Act
    currency.save()

    # Assert
    assert currency.name == "United States Dollar"
    assert currency.symbol == "$"
    assert currency.code == "USD"

    assert currency.created_at
    assert currency.updated_at

    assert str(currency) == f"{currency.name} ({currency.symbol})"
