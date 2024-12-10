"""Group serializers."""

from rest_framework import serializers

from groups.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""

    DUPLICATE_TITLE_ERROR = "A group with this title already exists for this user."

    def validate_title(self, value: str) -> str:
        """Validate that the title is unique for the current user."""
        request = self.context.get("request")

        if (
            request
            and request.user
            and self.instance is None
            and Group.objects.filter(
                title__iexact=value, created_by=request.user
            ).exists()
        ):
            raise serializers.ValidationError(self.DUPLICATE_TITLE_ERROR)

        return value

    class Meta:
        """Meta class."""

        model = Group

        fields = (
            "id",
            "title",
            "description",
            "currency",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("created_by", "updated_by", "created_at", "updated_at")
