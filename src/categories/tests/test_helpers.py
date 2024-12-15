"""Test helpers for the categories app."""

from __future__ import annotations

from categories.models import Category


def create_emoji_test_category(
    name: str = "Movies",
    emoji: str = "🎥",
    background_color: str | None = None,
    icon: str | None = None,
) -> Category:
    """Create a test category with an emoji."""
    return Category.objects.create(
        name=name,
        emoji=emoji,
        background_color=background_color,
        icon=icon,
    )


def create_test_category(
    name: str = "Games",
    background_color: str | None = None,
    icon: str | None = None,
) -> Category:
    """Create a test category."""
    return Category.objects.create(
        name=name, background_color=background_color, icon=icon
    )
