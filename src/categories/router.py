"""Router for the categories app."""

from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet

router = DefaultRouter()
router.register(r"", CategoryViewSet, basename="categories")
