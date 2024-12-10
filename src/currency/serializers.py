"""Currency serializer."""

from rest_framework import serializers

from currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    """Currency serializer."""

    class Meta:
        """Meta class."""

        model = Currency
        fields = ("id", "name", "symbol", "code", "created_at", "updated_at")
