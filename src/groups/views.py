"""Groups views."""

from rest_framework import viewsets

from groups.models import Group
from groups.serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """Group view set."""

    queryset = Group.objects.all().order_by("title")
    serializer_class = GroupSerializer

    def perform_create(self, serializer: GroupSerializer) -> None:
        """Perform the create action."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer: GroupSerializer) -> None:
        """Perform the update action."""
        serializer.save(updated_by=self.request.user)
