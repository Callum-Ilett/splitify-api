"""Groups router."""

from rest_framework import routers

from .views import GroupViewSet

groups_router = routers.DefaultRouter()
groups_router.register(prefix="", viewset=GroupViewSet, basename="group")
