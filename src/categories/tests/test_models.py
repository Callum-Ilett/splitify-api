"""Test the Category model."""

import pytest

from categories.tests.test_helpers import create_emoji_test_category


@pytest.mark.django_db
def test_category_model() -> None:
    """Test the category model."""
    # Arrange
    category = create_emoji_test_category(
        name="Movies", emoji="🎥", background_color="#000000", icon="icon.png"
    )

    # Act

    # Assert
    assert category.name == "Movies"
    assert category.emoji == "🎥"
    assert category.background_color == "#000000"
    assert category.icon == "icon.png"
    assert category.created_at
    assert category.updated_at
    assert category.is_main_category is True

    assert str(category) == category.name


@pytest.mark.django_db
def test_category_model_parent() -> None:
    """Test the category model with a parent."""
    # Arrange
    main_category = create_emoji_test_category(
        name="Entertainment", emoji="🍿", background_color="#000000", icon="icon.png"
    )

    subcategory_1 = create_emoji_test_category(
        name="Movies", emoji="🎥", background_color="#000000", icon="icon.png"
    )

    subcategory_2 = create_emoji_test_category(
        name="Games", emoji="🎮", background_color="#000000", icon="icon.png"
    )

    subcategory_1.parent = main_category  # type: ignore  # noqa: PGH003
    subcategory_1.save()

    subcategory_2.parent = main_category  # type: ignore  # noqa: PGH003
    subcategory_2.save()

    # Act

    # Assert
    assert main_category.name == "Entertainment"
    assert main_category.emoji == "🍿"
    assert main_category.background_color == "#000000"
    assert main_category.icon == "icon.png"
    assert main_category.created_at
    assert main_category.updated_at
    assert main_category.is_main_category is True

    assert subcategory_1.parent == main_category
    assert subcategory_1.name == "Movies"
    assert subcategory_1.emoji == "🎥"
    assert subcategory_1.background_color == "#000000"
    assert subcategory_1.icon == "icon.png"
    assert subcategory_1.created_at
    assert subcategory_1.updated_at
    assert subcategory_1.is_main_category is False

    assert subcategory_2.parent == main_category
    assert subcategory_2.name == "Games"
    assert subcategory_2.emoji == "🎮"
    assert subcategory_2.background_color == "#000000"
    assert subcategory_2.icon == "icon.png"
    assert subcategory_2.created_at
    assert subcategory_2.updated_at
    assert subcategory_2.is_main_category is False
    assert str(main_category) == main_category.name
