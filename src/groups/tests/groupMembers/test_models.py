"""Test the GroupMember model."""

import pytest
from django.db import IntegrityError

from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import GroupMember, GroupMemberRole
from groups.tests.groupMembers.test_helpers import create_test_group_member
from groups.tests.groups.test_delete_group import create_test_group


@pytest.mark.django_db
def test_group_member_model_default_member() -> None:
    """Test that a group member can be created with the default member role."""
    # Arrange
    user = create_test_user(username="testuser1", email="testuser1@email.com")
    group = create_test_group()

    # Act
    group_member = create_test_group_member(
        user=user, group=group, role=GroupMemberRole.MEMBER
    )

    # Assert
    assert group_member.group == group
    assert group_member.user == user
    assert group_member.role == GroupMemberRole.MEMBER


@pytest.mark.django_db
def test_create_group_member_admin_successful() -> None:
    """Test creating a group member with ADMIN role successfully."""
    # Arrange
    user = create_test_user(username="testuser1", email="testuser1@email.com")
    group = create_test_group()

    # Act
    group_member = create_test_group_member(
        user=user, group=group, role=GroupMemberRole.ADMIN
    )

    # Assert
    assert group_member.group == group
    assert group_member.user == user
    assert group_member.role == GroupMemberRole.ADMIN


@pytest.mark.django_db
def test_create_group_member_owner_successful() -> None:
    """Test creating a group member with OWNER role successfully."""
    # Arrange
    user = create_test_user()
    group = create_test_group()

    # Act
    group_member = create_test_group_member(
        user=user, group=group, role=GroupMemberRole.OWNER
    )

    # Assert
    assert group_member.group == group
    assert group_member.user == user
    assert group_member.role == GroupMemberRole.OWNER


@pytest.mark.django_db
def test_cannot_create_duplicate_group_owner_member() -> None:
    """Test that creating a duplicate group member raises IntegrityError."""
    # Arrange
    user = create_test_user()
    group = create_test_group()

    # Act & Assert
    with pytest.raises(IntegrityError):
        GroupMember.objects.create(group=group, user=user, role=GroupMemberRole.OWNER)


@pytest.mark.django_db
def test_cannot_create_duplicate_group_admin_member() -> None:
    """Test that creating a duplicate group admin member raises IntegrityError."""
    # Arrange
    user = create_test_user(username="testuser1", email="testuser1@email.com")
    group = create_test_group()

    # Act
    create_test_group_member(group=group, user=user, role=GroupMemberRole.ADMIN)

    # Assert
    with pytest.raises(IntegrityError):
        GroupMember.objects.create(group=group, user=user, role=GroupMemberRole.ADMIN)


@pytest.mark.django_db
def test_cannot_create_duplicate_group_member() -> None:
    """Test that creating a duplicate group member raises IntegrityError."""
    # Arrange
    user = create_test_user(username="testuser1", email="testuser1@email.com")
    group = create_test_group()

    # Act
    create_test_group_member(group=group, user=user, role=GroupMemberRole.MEMBER)

    # Assert
    with pytest.raises(IntegrityError):
        GroupMember.objects.create(group=group, user=user, role=GroupMemberRole.MEMBER)


@pytest.mark.django_db
def test_group_member_creation() -> None:
    """Test that creating a group automatically creates an OWNER group member."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = create_test_group(currency=currency, created_by=user)

    # Act
    members = GroupMember.objects.filter(group=group, user=user)

    # Assert
    assert members.count() == 1

    assert members[0].user == user
    assert members[0].group == group
    assert members[0].role == GroupMemberRole.OWNER
    assert members[0].created_at
    assert members[0].updated_at

    assert str(members[0]) == f"{user.username} - {group.title}"


@pytest.mark.django_db
def test_group_member_not_created_on_update() -> None:
    """Test that saving an existing group doesn't create another owner member."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = create_test_group(currency=currency, created_by=user)

    # Assert initial state
    assert GroupMember.objects.filter(group=group).count() == 1  # 1 new member created

    # Act
    group.title = "Updated Title"
    group.save()  # Trigger the post_save signal again

    # Assert
    # Still only 1 member, no new member created during edit
    assert GroupMember.objects.filter(group=group).count() == 1
