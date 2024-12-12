"""
Test views for currency app.
"""

import pytest
from django.test import Client
from rest_framework import status

from core.test_helpers import create_test_user
from currency.models import Currency
from currency.tests.test_helpers import create_test_currency


class TestUnauthenticatedCurrencyView:
    """
    Test views for currency app when the user is not authenticated.
    """

    @pytest.mark.django_db
    def test_list_currencies_unauthenticated_fails(self, client: Client) -> None:
        """
        Test that a user cannot list currencies if they are not logged in.
        """
        # Arrange

        # Act
        response = client.get("/api/currency/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_retrieve_currency_unauthenticated_fails(self, client: Client) -> None:
        """
        Test that a user cannot retrieve a currency if they are not logged in.
        """
        # Arrange
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        # Act
        response = client.get(f"/api/currency/{currency.id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_currency_unauthenticated_fails(self, client: Client) -> None:
        """
        Test that a user cannot create a currency if they are not logged in.
        """
        # Arrange
        payload = {
            "name": "US Dollar",
            "code": "USD",
            "symbol": "$",
        }

        # Act
        response = client.post("/api/currency/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_put_currency_unauthenticated_fails(self, client: Client) -> None:
        """
        Test that a user cannot update a currency if they are not logged in.
        """
        # Arrange
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        payload = {
            "name": "UK Pound",
            "code": "GBP",
            "symbol": "£",
        }

        # Act
        response = client.put(
            f"/api/currency/{currency.id}/", payload, "application/json"
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_patch_currency_unauthenticated_fails(self, client: Client) -> None:
        """
        Test that a user cannot update a currency if they are not logged in.
        """
        # Arrange
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        payload = {
            "name": "UK Pound",
        }

        # Act
        response = client.patch(
            f"/api/currency/{currency.id}/", payload, "application/json"
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_delete_currency_unauthenticated_fails(self, client: Client) -> None:
        """
        Test that a user cannot delete a currency if they are not logged in.
        """
        # Arrange
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        # Act
        response = client.delete(f"/api/currency/{currency.id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCreateCurrencyView:
    """
    Test views for currency app.
    """

    @pytest.mark.django_db
    def test_create_currency_success(self, client: Client) -> None:
        """
        Test that a currency can be created successfully.
        """
        # Arrange
        user = create_test_user()

        payload = {
            "name": "US Dollar",
            "code": "USD",
            "symbol": "$",
        }

        client.force_login(user)

        # Act
        response = client.post("/api/currency/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        assert response_data["name"] == "US Dollar"
        assert response_data["code"] == "USD"
        assert response_data["symbol"] == "$"

    @pytest.mark.django_db
    def test_create_currency_required_fields_fails(self, client: Client) -> None:
        """
        Test that a user cannot create a currency without required fields.
        """
        # Arrange
        user = create_test_user()

        payload = {}

        client.force_login(user)

        # Act
        response = client.post("/api/currency/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response_data["name"] == ["This field is required."]
        assert response_data["code"] == ["This field is required."]
        assert response_data["symbol"] == ["This field is required."]


class TestRetrieveCurrencyView:
    """
    Test views for retrieving a currency by id.
    """

    @pytest.mark.django_db
    def test_retrieve_currency_success(self, client: Client) -> None:
        """
        Test that a currency can be retrieved by id successfully.
        """
        # Arrange
        user = create_test_user()
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        client.force_login(user)

        # Act
        response = client.get(f"/api/currency/{currency.id}/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["name"] == "US Dollar"
        assert response_data["code"] == "USD"
        assert response_data["symbol"] == "$"

    @pytest.mark.django_db
    def test_retrieve_currency_not_found_fails(self, client: Client) -> None:
        """
        Test that a currency that does not exist cannot be retrieved.
        """
        # Arrange
        user = create_test_user()

        client.force_login(user)

        # Act
        response = client.get("/api/currency/999/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestListCurrencyView:
    """
    Test views for listing currencies.
    """

    @pytest.mark.django_db
    def test_list_currencies_success(self, client: Client) -> None:
        """
        Test that a list of currencies can be retrieved successfully.
        """
        # Arrange
        user = create_test_user()

        create_test_currency(name="US Dollar", code="USD", symbol="$")
        create_test_currency(name="UK Pound", code="GBP", symbol="£")
        create_test_currency(name="Euro", code="EUR", symbol="€")

        client.force_login(user)

        # Act
        response = client.get("/api/currency/")
        response_data = response.json()

        expected_count = 3

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["count"] == expected_count
        assert response_data["next"] is None
        assert response_data["previous"] is None

        assert len(response_data["results"]) == expected_count

        assert response_data["results"][0]["name"] == "US Dollar"
        assert response_data["results"][0]["code"] == "USD"
        assert response_data["results"][0]["symbol"] == "$"

        assert response_data["results"][1]["name"] == "UK Pound"
        assert response_data["results"][1]["code"] == "GBP"
        assert response_data["results"][1]["symbol"] == "£"

        assert response_data["results"][2]["name"] == "Euro"
        assert response_data["results"][2]["code"] == "EUR"
        assert response_data["results"][2]["symbol"] == "€"

    @pytest.mark.django_db
    def test_list_currency_empty_success(self, client: Client) -> None:
        """
        Test that an empty list of currencies can be retrieved successfully.
        """
        # Arrange
        user = create_test_user()

        client.force_login(user)

        # Act
        response = client.get("/api/currency/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["count"] == 0
        assert response_data["next"] is None
        assert response_data["previous"] is None

        assert len(response_data["results"]) == 0


class TestUpdateCurrencyView:
    """
    Test views for editing a currency.
    """

    @pytest.mark.django_db
    def test_update_put_currency_success(self, client: Client) -> None:
        """
        Test that a currency can be updated successfully.
        """
        # Arrange
        user = create_test_user()
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        payload = {
            "name": "UK Pound",
            "code": "GBP",
            "symbol": "£",
        }

        client.force_login(user)

        # Act
        response = client.put(
            f"/api/currency/{currency.id}/", payload, "application/json"
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["name"] == "UK Pound"
        assert response_data["code"] == "GBP"
        assert response_data["symbol"] == "£"

    @pytest.mark.django_db
    def test_update_patch_currency_success(self, client: Client) -> None:
        """
        Test that a currency can be updated successfully.
        """
        # Arrange
        user = create_test_user()
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        payload = {
            "name": "USA Dollar",
            "code": "USD",
            "symbol": "$",
        }

        client.force_login(user)

        # Act
        response = client.patch(
            f"/api/currency/{currency.id}/", payload, "application/json"
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["name"] == "USA Dollar"
        assert response_data["code"] == "USD"
        assert response_data["symbol"] == "$"

    @pytest.mark.django_db
    def test_update_currency_with_empty_strings_fails(self, client: Client) -> None:
        """
        Test that updating with empty strings is handled properly.
        """
        # Arrange
        user = create_test_user()
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        payload = {
            "name": "",
            "code": "",
            "symbol": "",
        }
        client.force_login(user)

        # Act
        response = client.put(
            f"/api/currency/{currency.id}/", payload, "application/json"
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response_data["name"] == ["This field may not be blank."]
        assert response_data["code"] == ["This field may not be blank."]
        assert response_data["symbol"] == ["This field may not be blank."]


class TestDeleteCurrencyView:
    """
    Test views for deleting a currency.
    """

    @pytest.mark.django_db
    def test_delete_currency_success(self, client: Client) -> None:
        """
        Test that a currency can be deleted successfully.
        """
        # Arrange
        user = create_test_user()
        currency = create_test_currency(name="US Dollar", code="USD", symbol="$")

        client.force_login(user)

        # Act
        assert Currency.objects.count() == 1
        response = client.delete(f"/api/currency/{currency.id}/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Currency.objects.count() == 0

    @pytest.mark.django_db
    def test_delete_currency_not_found_fails(self, client: Client) -> None:
        """
        Test that a user cannot delete a currency that does not exist.
        """
        # Arrange
        user = create_test_user()
        create_test_currency(name="US Dollar", code="USD", symbol="$")

        client.force_login(user)

        # Act
        response = client.delete("/api/currency/999/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
