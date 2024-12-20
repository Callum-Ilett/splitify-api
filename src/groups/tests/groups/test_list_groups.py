"""Test list groups."""

import pytest
from django.test import Client
from rest_framework import status

from categories.tests.test_helpers import create_emoji_test_category
from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.tests.groups.test_helpers import create_test_group


@pytest.mark.django_db
def test_ascending_order_success(client: Client) -> None:
    """Test that all groups are listed."""
    # Arrange
    user_1 = create_test_user(username="user_1", email="user_1@email.com")
    user_2 = create_test_user(username="user_2", email="user_2@email.com")
    user_3 = create_test_user(username="user_3", email="user_3@email.com")

    currency_usd = create_test_currency(
        name="USD",
        symbol="$",
        code="USD",
    )

    currency_eur = create_test_currency(
        name="EUR",
        symbol="€",
        code="EUR",
    )

    currency_gbp = create_test_currency(
        name="GBP",
        symbol="£",
        code="GBP",
    )

    miami_group = create_test_group(
        title="Miami Summer 2024 Squad 🌴",
        description="Planning our Miami beach vacation!",
        currency=currency_usd,
        created_by=user_1,
    )

    lads_group = create_test_group(
        title="Lads sesh 🍻",
        description="Everyone is invited!",
        currency=currency_eur,
        created_by=user_2,
    )

    christmas_group = create_test_group(
        title="Christmas drinks 2024 🎄",
        description="Planning our Christmas drinks!",
        currency=currency_usd,
        created_by=user_3,
    )

    new_years_group = create_test_group(
        title="New years eve 2025 🎉",
        description="Let's celebrate the new year!",
        currency=currency_gbp,
        created_by=user_1,
    )

    client.force_login(user_1)

    # Act
    response = client.get("/api/groups/")
    response_data = response.json()
    results = response_data["results"]

    # Assert
    expected_group_count = 4
    assert response.status_code == status.HTTP_200_OK

    assert response_data["count"] == expected_group_count
    assert response_data["next"] is None
    assert response_data["previous"] is None

    assert len(results) == expected_group_count

    assert results[0]["id"] == str(christmas_group.id)
    assert results[0]["title"] == "Christmas drinks 2024 🎄"
    assert results[0]["description"] == "Planning our Christmas drinks!"
    assert results[0]["currency"] == str(currency_usd.id)
    assert results[0]["created_by"] == str(user_3.pk)
    assert results[0]["updated_by"] is None
    assert results[0]["created_at"]
    assert results[0]["updated_at"]

    assert results[1]["id"] == str(lads_group.id)
    assert results[1]["title"] == "Lads sesh 🍻"
    assert results[1]["description"] == "Everyone is invited!"
    assert results[1]["currency"] == str(currency_eur.id)
    assert results[1]["created_by"] == str(user_2.pk)
    assert results[1]["updated_by"] is None
    assert results[1]["created_at"]
    assert results[1]["updated_at"]

    assert results[2]["id"] == str(miami_group.id)
    assert results[2]["title"] == "Miami Summer 2024 Squad 🌴"
    assert results[2]["description"] == "Planning our Miami beach vacation!"
    assert results[2]["currency"] == str(currency_usd.id)
    assert results[2]["created_by"] == str(user_1.pk)
    assert results[2]["updated_by"] is None
    assert results[2]["created_at"]
    assert results[2]["updated_at"]

    assert results[3]["id"] == str(new_years_group.id)
    assert results[3]["title"] == "New years eve 2025 🎉"
    assert results[3]["description"] == "Let's celebrate the new year!"
    assert results[3]["currency"] == str(currency_gbp.id)
    assert results[3]["created_by"] == str(user_1.pk)
    assert results[3]["updated_by"] is None
    assert results[3]["created_at"]
    assert results[3]["updated_at"]


@pytest.mark.django_db
def test_pagination_next_page_success(client: Client) -> None:
    """Test that a list of next page of groups can be retrieved successfully."""
    # Arrange
    user_1 = create_test_user(username="user_1", email="user_1@email.com")

    currency_usd = create_test_currency(
        name="USD",
        symbol="$",
        code="USD",
    )

    for i in range(20):
        create_test_group(
            title=f"Group {i}",
            description=f"Description {i}",
            currency=currency_usd,
            created_by=user_1,
            updated_by=None,
        )

    client.force_login(user_1)

    # Act
    response = client.get("/api/groups/?page=1&limit=10")
    response_data = response.json()

    # Assert
    expected_total_groups = 20
    expected_group_count = 10
    expected_next_page_url = (
        f"http://testserver/api/groups/?limit={expected_group_count}&page=2"
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response_data["results"]) == expected_group_count

    assert response_data["count"] == expected_total_groups
    assert response_data["next"] == expected_next_page_url
    assert response_data["previous"] is None


@pytest.mark.django_db
def test_pagination_previous_page_success(client: Client) -> None:
    """Test that a list of previous page of groups can be retrieved successfully."""
    # Arrange
    user_1 = create_test_user(username="user_1", email="user_1@email.com")

    currency_usd = create_test_currency(
        name="USD",
        symbol="$",
        code="USD",
    )

    for i in range(20):
        create_test_group(
            title=f"Group {i}",
            description=f"Description {i}",
            currency=currency_usd,
            created_by=user_1,
            updated_by=None,
        )

    client.force_login(user_1)

    # Act
    response = client.get("/api/groups/?page=2&limit=10")
    response_data = response.json()

    # Assert
    expected_total_groups = 20
    expected_group_count = 10
    expected_previous_page_url = "http://testserver/api/groups/?limit=10"

    assert response.status_code == status.HTTP_200_OK

    assert len(response_data["results"]) == expected_group_count

    assert response_data["count"] == expected_total_groups
    assert response_data["next"] is None
    assert response_data["previous"] == expected_previous_page_url


@pytest.mark.django_db
def test_groups_with_and_without_images_success(client: Client) -> None:
    """Test that groups can have images and some can have None."""
    # Arrange
    user = create_test_user(username="user_1", email="user_1@email.com")
    currency_usd = create_test_currency(name="USD", symbol="$", code="USD")
    image = "image.png"

    create_test_group(
        title="Group with Image",
        description="This group has an image.",
        currency=currency_usd,
        created_by=user,
        image=image,
    )

    create_test_group(
        title="Group without Image",
        description="This group does not have an image.",
        currency=currency_usd,
        created_by=user,
        image=None,
    )

    client.force_login(user)

    # Act
    response = client.get("/api/groups/")
    response_data = response.json()
    results = response_data["results"]

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert results[0]["image"] is not None
    assert results[1]["image"] is None


@pytest.mark.django_db
def test_list_groups_with_categories_success(client: Client) -> None:
    """Test that groups with categories are listed correctly."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    category_1 = create_emoji_test_category(name="Trip", emoji="🛫")
    category_2 = create_emoji_test_category(name="Holiday", emoji="🏖️")

    group = create_test_group(
        title="Miami Summer 2024 Squad 🌴",
        description="Planning our Miami beach vacation!",
        currency=currency,
        created_by=user,
    )

    group.categories.add(category_1, category_2)

    client.force_login(user)

    # Act
    response = client.get("/api/groups/")
    response_data = response.json()
    results = response_data["results"]

    expected_result_count = 1
    expected_category_count = 2
    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert len(results) == expected_result_count

    assert results[0]["id"] == str(group.id)
    assert results[0]["title"] == "Miami Summer 2024 Squad 🌴"
    assert results[0]["description"] == "Planning our Miami beach vacation!"
    assert results[0]["currency"] == str(currency.id)
    assert results[0]["created_by"] == str(user.pk)
    assert len(results[0]["categories"]) == expected_category_count
    assert results[0]["updated_by"] is None
    assert results[0]["created_at"]
    assert results[0]["updated_at"]


@pytest.mark.django_db
def test_list_groups_with_and_without_categories_success(client: Client) -> None:
    """Test that groups both with and without categories are listed correctly."""
    # Arrange
    user = create_test_user()
    currency = create_test_currency()

    category_1 = create_emoji_test_category(name="Trip", emoji="🛫")
    category_2 = create_emoji_test_category(name="Holiday", emoji="🏖️")

    group_with_categories = create_test_group(
        title="Group with categories",
        description="This group has categories",
        currency=currency,
        created_by=user,
    )
    group_with_categories.categories.add(category_1, category_2)

    group_without_categories = create_test_group(
        title="Group without categories",
        description="This group has no categories",
        currency=currency,
        created_by=user,
    )

    client.force_login(user)

    # Act
    response = client.get("/api/groups/")
    response_data = response.json()
    results = response_data["results"]

    expected_result_count = 2
    expected_category_count = 2

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert len(results) == expected_result_count

    # Group with categories
    assert results[0]["id"] == str(group_with_categories.id)
    assert results[0]["title"] == "Group with categories"
    assert results[0]["description"] == "This group has categories"
    assert results[0]["currency"] == str(currency.id)
    assert len(results[0]["categories"]) == expected_category_count
    assert results[0]["created_by"] == str(user.pk)
    assert results[0]["updated_by"] is None
    assert results[0]["created_at"]
    assert results[0]["updated_at"]

    # Group without categories
    assert results[1]["id"] == str(group_without_categories.id)
    assert results[1]["title"] == "Group without categories"
    assert results[1]["description"] == "This group has no categories"
    assert results[1]["currency"] == str(currency.id)
    assert results[1]["categories"] == []
    assert results[1]["created_by"] == str(user.pk)
    assert results[1]["updated_by"] is None
    assert results[1]["created_at"]
    assert results[1]["updated_at"]
