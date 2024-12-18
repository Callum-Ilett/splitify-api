"""Groups router."""

from rest_framework import routers

from .views import GroupMemberViewSet, GroupViewSet

groups_router = routers.DefaultRouter()
groups_router.register(prefix="groups", viewset=GroupViewSet, basename="group")

group_members_router = routers.DefaultRouter()
group_members_router.register(
    prefix="group-members", viewset=GroupMemberViewSet, basename="group-member"
)
