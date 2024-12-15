"""Views for the categories app."""

from rest_framework import viewsets

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category model."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
