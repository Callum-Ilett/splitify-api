"""Currency views."""

from rest_framework import viewsets

from currency.models import Currency
from currency.serializers import CurrencySerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """Currency view set."""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
