"""Currency router."""

from rest_framework import routers

from currency.views import CurrencyViewSet

currency_router = routers.DefaultRouter()

currency_router.register(prefix="", viewset=CurrencyViewSet, basename="currency")
