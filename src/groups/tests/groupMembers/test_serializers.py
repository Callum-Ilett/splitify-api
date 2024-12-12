"""Test the GroupMember serializer."""

import pytest

from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import Group, GroupMemberRole
from groups.serializers import GroupMemberSerializer
from groups.tests.groups.test_helpers import create_test_group


@pytest.mark.django_db
def test_group_member_valid() -> None:
    """Test that the serializer is valid with correct data."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = create_test_group(currency=currency)

    group_member = {
        "user": str(user.id),  # type: ignore
        "group": str(group.id),
        "role": GroupMemberRole.MEMBER,
    }

    # Act
    serializer = GroupMemberSerializer(data=group_member)
    is_valid = serializer.is_valid()

    # Assert
    assert is_valid
    assert serializer.errors == {}


@pytest.mark.django_db
def test_user_required_invalid() -> None:
    """Test that the user field is required."""
    # Arrange
    currency = create_test_currency()
    group = create_test_group(currency=currency)

    group_member = {
        "group": str(group.id),
        "role": GroupMemberRole.MEMBER,
    }

    # Act
    serializer = GroupMemberSerializer(data=group_member)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"user": ["This field is required."]}


@pytest.mark.django_db
def test_group_required_invalid() -> None:
    """Test that the group field is required."""
    # Arrange
    user = create_test_user()

    group_member = {
        "user": str(user.id),  # type: ignore
        "role": GroupMemberRole.MEMBER,
    }

    # Act
    serializer = GroupMemberSerializer(data=group_member)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert serializer.errors == {"group": ["This field is required."]}


@pytest.mark.django_db
def test_invalid_user_id() -> None:
    """Test that the serializer rejects non-existent user IDs."""
    # Arrange
    currency = create_test_currency()
    group = create_test_group(currency=currency)

    group_member = {
        "user": "nonexistent-uuid",
        "group": str(group.id),
        "role": GroupMemberRole.MEMBER,
    }

    # Act
    serializer = GroupMemberSerializer(data=group_member)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert "user" in serializer.errors


@pytest.mark.django_db
def test_invalid_group_id() -> None:
    """Test that the serializer rejects non-existent group IDs."""
    # Arrange
    user = create_test_user()

    group_member = {
        "user": str(user.id),  # type: ignore
        "group": "nonexistent-uuid",
        "role": GroupMemberRole.MEMBER,
    }

    # Act
    serializer = GroupMemberSerializer(data=group_member)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert "group" in serializer.errors


@pytest.mark.django_db
def test_invalid_role() -> None:
    """Test that the serializer rejects invalid role values."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = Group.objects.create(title="Test Group", currency=currency)

    group_member = {
        "user": str(user.id),  # type: ignore
        "group": str(group.id),
        "role": "INVALID_ROLE",
    }

    # Act
    serializer = GroupMemberSerializer(data=group_member)
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert "role" in serializer.errors
