"""Test the Group model."""

import pytest

from categories.tests.test_helpers import create_emoji_test_category
from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.tests.groups.test_helpers import create_test_group


@pytest.mark.django_db
def test_group_categories() -> None:
    """Test that a group can be associated with multiple categories."""
    # Arrange
    currency = create_test_currency()

    category_1 = create_emoji_test_category(name="Trip", emoji="🛫")
    category_2 = create_emoji_test_category(name="Holiday", emoji="🏖️")

    group = create_test_group(currency=currency)

    # Act
    group.categories.add(category_1, category_2)

    # Assert
    assert group.title == "Miami Summer 2024 Squad 🌴"
    assert group.description == "Planning our Miami beach vacation!"
    assert group.currency == currency
    assert group.created_by
    assert group.updated_by is None
    assert group.created_at
    assert group.updated_at

    assert category_1 in group.categories.all()
    assert category_2 in group.categories.all()

    assert str(group) == group.title


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
