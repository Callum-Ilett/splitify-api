"""Test the GroupMember model."""

import pytest

from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import GroupMemberRole
from groups.tests.groupMembers.test_helpers import create_test_group_member
from groups.tests.groups.test_delete_group import create_test_group


@pytest.mark.django_db
def test_group_member_model_default_member() -> None:
    """Test that a group member can be created with the default member role."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = create_test_group(currency=currency)

    # Act
    group_member = create_test_group_member(user=user, group=group)

    # Assert
    assert group_member.user == user
    assert group_member.group == group
    assert group_member.role == GroupMemberRole.MEMBER
    assert group_member.created_at
    assert group_member.updated_at

    assert str(group_member) == f"{user.username} - {group.title}"


@pytest.mark.django_db
def test_group_member_model_admin() -> None:
    """Test that a group member can be created with the admin role."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = create_test_group(currency=currency)

    # Act
    group_member = create_test_group_member(
        user=user, group=group, role=GroupMemberRole.ADMIN
    )

    # Assert
    assert group_member.user == user
    assert group_member.group == group
    assert group_member.role == GroupMemberRole.ADMIN
    assert group_member.created_at
    assert group_member.updated_at

    assert str(group_member) == f"{user.username} - {group.title}"
