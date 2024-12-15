"""Serializers for the categories app."""

from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta class for the Category serializer."""

        model = Category
        fields = (
            "id",
            "name",
            "emoji",
            "icon",
            "parent",
            "background_color",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("created_at", "updated_at")
