"""Helper functions for testing group members."""

from django.contrib.auth.models import AbstractUser

from groups.models import Group, GroupMember, GroupMemberRole


def create_test_group_member(
    user: AbstractUser,
    group: Group,
    role: GroupMemberRole = GroupMemberRole.MEMBER,
) -> GroupMember:
    """Create a test group member if it doesn't exist, otherwise return existing group member."""
    group_member, _ = GroupMember.objects.get_or_create(
        user=user, group=group, role=role
    )

    return group_member
