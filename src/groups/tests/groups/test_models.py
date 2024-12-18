"""Test the Group model."""

import pytest

from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import GroupMember, GroupMemberRole
from groups.tests.groups.test_helpers import create_test_group


@pytest.mark.django_db
def test_group_currency() -> None:
    """Test that a group can be associated with a currency."""
    # Arrange
    currency = create_test_currency()
    group = create_test_group(currency=currency)

    # Act

    # Assert
    assert group.title == "Miami Summer 2024 Squad 🌴"
    assert group.description == "Planning our Miami beach vacation!"
    assert group.currency == currency
    assert group.created_by
    assert group.updated_by is None
    assert group.created_at
    assert group.updated_at

    assert str(group) == group.title


@pytest.mark.django_db
def test_group_image() -> None:
    """Test that a group can have an image."""
    # Arrange
    currency = create_test_currency()
    group = create_test_group(currency=currency, image="test.png")

    # Act

    # Assert
    assert group.title == "Miami Summer 2024 Squad 🌴"
    assert group.description == "Planning our Miami beach vacation!"
    assert group.currency == currency
    assert group.created_by
    assert group.updated_by is None
    assert group.created_at
    assert group.updated_at

    assert str(group) == group.title


@pytest.mark.django_db
def test_group_model_audit() -> None:
    """Test that a group tracks the user who created and last updated it."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()
    group = create_test_group(currency=currency, created_by=user)

    # Act

    # Assert
    assert group.title == "Miami Summer 2024 Squad 🌴"
    assert group.description == "Planning our Miami beach vacation!"
    assert group.created_by == user
    assert group.updated_by is None

    assert group.created_at
    assert group.updated_at

    assert str(group) == group.title


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
