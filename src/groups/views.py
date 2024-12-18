"""Groups views."""

from typing import ClassVar

from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from groups.models import Group, GroupMember
from groups.permissions import IsGroupAdminOrOwner, IsGroupOwner
from groups.serializers import GroupMemberSerializer, GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """Group view set."""

    queryset = Group.objects.all().order_by("title")
    serializer_class = GroupSerializer
    permission_classes: ClassVar = [IsAuthenticated]

    def get_permissions(self) -> list[permissions.BasePermission]:
        """Get the permissions for the view."""
        if self.action == "destroy":
            return [IsAuthenticated(), IsGroupOwner()]

        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsGroupAdminOrOwner()]

        return super().get_permissions()

    def perform_create(self, serializer: GroupSerializer) -> None:
        """Perform the create action."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer: GroupSerializer) -> None:
        """Perform the update action."""
        serializer.save(updated_by=self.request.user)


class GroupMemberViewSet(viewsets.ModelViewSet):
    """Group member view set."""

    queryset = GroupMember.objects.all()

    serializer_class = GroupMemberSerializer
