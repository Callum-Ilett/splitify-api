"""App configuration for the currency app."""

from django.apps import AppConfig


class CurrencyConfig(AppConfig):
    """App configuration for the currency app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "currency"
