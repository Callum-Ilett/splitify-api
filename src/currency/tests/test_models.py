"""Test the Currency model."""

import pytest

from currency.tests.test_helpers import create_test_currency


@pytest.mark.django_db
def test_group_model() -> None:
    """Test the currency model."""
    # Arrange
    currency = create_test_currency(name="United States Dollar", code="USD", symbol="$")

    # Act

    # Assert
    assert currency.name == "United States Dollar"
    assert currency.symbol == "$"
    assert currency.code == "USD"

    assert currency.created_at
    assert currency.updated_at

    assert str(currency) == f"{currency.name} ({currency.symbol})"
