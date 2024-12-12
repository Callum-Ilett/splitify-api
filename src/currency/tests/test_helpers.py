"""Helper functions for testing the currency app."""

from currency.models import Currency


def create_test_currency(
    name: str = "United States Dollar", code: str = "USD", symbol: str = "$"
) -> Currency:
    """
    Create a test currency if it doesn't exist, otherwise return existing.
    """
    currency, _ = Currency.objects.get_or_create(name=name, code=code, symbol=symbol)

    return currency
