"""Groups permissions."""

from rest_framework import permissions, viewsets
from rest_framework.request import Request

from groups.models import Group, GroupMember, GroupMemberRole


class IsGroupOwner(permissions.BasePermission):
    """Permission to check if the user is the owner of a group."""

    def has_object_permission(  # noqa: ANN201, PGH003 # type: ignore
        self,
        request: Request,
        view: viewsets.ModelViewSet,  # noqa: ARG002
        obj: Group,
    ):
        """Check if the user is the owner of the group."""
        member = GroupMember.objects.get(group=obj, user=request.user)
        return member.role == GroupMemberRole.OWNER


class IsGroupAdmin(permissions.BasePermission):
    """Permission to check if the user is an admin of a group."""

    def has_object_permission(  # noqa: ANN201, PGH003 # type: ignore
        self,
        request: Request,
        view: viewsets.ModelViewSet,  # noqa: ARG002
        obj: Group,
    ):
        """Check if the user is an admin Member of the group."""
        member = GroupMember.objects.get(group=obj, user=request.user)

        return member.role == GroupMemberRole.ADMIN


class IsGroupAdminOrOwner(permissions.BasePermission):
    """Permission to check if the user is an admin or owner of a group."""

    def has_object_permission(  # noqa: ANN201, PGH003 # type: ignore
        self, request: Request, view: viewsets.ModelViewSet, obj: Group
    ):
        """Check if the user is an admin or owner of the group."""
        return IsGroupAdmin().has_object_permission(
            request, view, obj
        ) or IsGroupOwner().has_object_permission(request, view, obj)
