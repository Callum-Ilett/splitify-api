"""Test the Category views."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test.client import encode_multipart
from rest_framework import status

from categories.tests.test_helpers import create_emoji_test_category
from core.test_helpers import create_test_image, create_test_user


class TestCategoryViewsUnauthenticated:
    """Test the Category views when the user is not authenticated."""

    @pytest.mark.django_db
    def test_list_categories_unauthenticated_fails(self, client: Client) -> None:
        """Test that a list of categories is not accessible to unauthenticated users."""
        # Arrange

        # Act
        response = client.get("/api/categories/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_retrieve_category_unauthenticated_fails(self, client: Client) -> None:
        """Test that retrieving a category is not accessible to unauthenticated users."""
        # Arrange
        category_id = 1

        # Act
        response = client.get(f"/api/categories/{category_id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_category_unauthenticated_fails(self, client: Client) -> None:
        """Test that updating a category is not accessible to unauthenticated users."""
        # Arrange
        category_id = 1
        data = {"name": "Updated Category"}

        # Act
        response = client.put(f"/api/categories/{category_id}/", data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_partial_update_category_unauthenticated_fails(
        self, client: Client
    ) -> None:
        """Test that updating a category is not accessible to unauthenticated users."""
        # Arrange
        category_id = 1
        data = {"name": "Partially Updated Category"}

        # Act
        response = client.patch(f"/api/categories/{category_id}/", data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_delete_category_unauthenticated_fails(self, client: Client) -> None:
        """Test that deleting a category is not accessible to unauthenticated users."""
        # Arrange
        category_id = 1

        # Act
        response = client.delete(f"/api/categories/{category_id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCreateCategoryView:
    """Test the CreateCategoryView."""

    @pytest.mark.django_db
    def test_create_category_success(self, client: Client) -> None:
        """Test that creating a category succeeds."""
        # Arrange
        user = create_test_user()
        icon = create_test_image()

        data = {
            "name": "Entertainment",
            "emoji": "🎥",
            "icon": icon,
            "background_color": "#FF0000",
        }

        client.force_login(user)

        # Act
        response = client.post("/api/categories/", data, format="multipart/form-data")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        assert response_data["id"]
        assert response_data["name"] == "Entertainment"
        assert response_data["emoji"] == "🎥"
        assert response_data["icon"]
        assert response_data["background_color"] == "#FF0000"
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_create_category_name_empty_fails(self, client: Client) -> None:
        """Test that creating a category fails when name is empty."""
        # Arrange
        user = create_test_user()
        data = {
            "name": "",
            "emoji": "🎥",
            "background_color": "#FF0000",
        }

        client.force_login(user)

        # Act
        response = client.post("/api/categories/", data, format="multipart/form-data")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["name"][0] == "This field may not be blank."

    @pytest.mark.django_db
    def test_create_category_name_too_long_fails(self, client: Client) -> None:
        """Test that creating a category fails when name exceeds max length."""
        # Arrange
        user = create_test_user()
        data = {
            "name": "a" * 51,  # Max length is 50 based on serializer tests
            "emoji": "🎥",
            "background_color": "#FF0000",
        }

        client.force_login(user)

        # Act
        response = client.post("/api/categories/", data, format="multipart/form-data")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response_data["name"][0]
            == "Ensure this field has no more than 50 characters."
        )

    @pytest.mark.django_db
    def test_create_category_invalid_emoji_fails(self, client: Client) -> None:
        """Test that creating a category fails when emoji exceeds max length."""
        # Arrange
        user = create_test_user()
        data = {
            "name": "Entertainment",
            "emoji": "🎥🎬🎭",  # Max length is 2 based on serializer tests
            "background_color": "#FF0000",
        }

        client.force_login(user)

        # Act
        response = client.post("/api/categories/", data, format="multipart/form-data")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response_data["emoji"][0]
            == "Ensure this field has no more than 2 characters."
        )

    @pytest.mark.django_db
    def test_create_category_invalid_image_format_fails(self, client: Client) -> None:
        """Test that creating a category fails when image format is invalid."""
        # Arrange
        user = create_test_user()
        invalid_file = SimpleUploadedFile(
            name="test.txt", content=b"invalid image content", content_type="text/plain"
        )

        data = {
            "name": "Entertainment",
            "emoji": "🎥",
            "icon": invalid_file,
            "background_color": "#FF0000",
        }

        client.force_login(user)

        # Act
        response = client.post("/api/categories/", data, format="multipart/form-data")
        response_data = response.json()

        expected_error = "Upload a valid image. The file you uploaded was either not an image or a corrupted image."

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["icon"][0] == expected_error


class TestUpdateCategoryView:
    """Test the UpdateCategoryView."""

    @pytest.mark.django_db
    def test_update_category_success(self, client: Client) -> None:
        """Test that updating a category succeeds."""
        # Arrange
        user = create_test_user()
        icon = create_test_image()

        category = create_emoji_test_category(
            name="Entertainment",
            emoji="🎥",
            background_color="#FF0000",
            icon="icon.png",
        )

        data = {
            "name": "Movies & TV",
            "emoji": "🍿",
            "background_color": "#00FF00",
            "icon": icon,
        }

        client.force_login(user)

        # Act
        response = client.put(
            f"/api/categories/{category.id}/",
            data=encode_multipart(data=data, boundary="BoUnDaRyStRiNg"),
            content_type="multipart/form-data; boundary=BoUnDaRyStRiNg",
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["id"]
        assert response_data["name"] == "Movies & TV"
        assert response_data["emoji"] == "🍿"
        assert response_data["icon"]
        assert response_data["background_color"] == "#00FF00"
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_partial_update_category_success(self, client: Client) -> None:
        """Test that partial updating a category succeeds."""
        # Arrange
        user = create_test_user()
        category = create_emoji_test_category(
            name="Entertainment",
            emoji="🎥",
            background_color="#FF0000",
            icon="icon.png",
        )

        data = {
            "name": "Movies & Shows",
            "emoji": "🍿",
        }

        client.force_login(user)

        # Act
        response = client.patch(
            f"/api/categories/{category.id}/",
            data=encode_multipart(data=data, boundary="BoUnDaRyStRiNg"),
            content_type="multipart/form-data; boundary=BoUnDaRyStRiNg",
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["id"]
        assert response_data["name"] == "Movies & Shows"
        assert response_data["emoji"] == "🍿"
        assert response_data["icon"]
        assert response_data["background_color"] == "#FF0000"
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_update_category_name_empty_fails(self, client: Client) -> None:
        """Test that updating a category fails when name is empty."""
        # Arrange
        user = create_test_user()
        category = create_emoji_test_category(
            name="Entertainment", emoji="🎥", background_color="#FF0000"
        )

        data = {
            "name": "",
            "emoji": "🍿",
            "background_color": "#00FF00",
            "icon": "",
        }

        client.force_login(user)

        # Act
        response = client.put(
            f"/api/categories/{category.id}/",
            data=encode_multipart(data=data, boundary="BoUnDaRyStRiNg"),
            content_type="multipart/form-data; boundary=BoUnDaRyStRiNg",
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["name"][0] == "This field may not be blank."


class TestListCategoryView:
    """Test the ListCategoryView."""

    @pytest.mark.django_db
    def test_list_categories_success(self, client: Client) -> None:
        """Test that categories can be listed successfully."""
        # Arrange
        user = create_test_user()

        create_emoji_test_category(
            name="Entertainment",
            emoji="🎬",
            background_color="#FF0000",
            icon="icon1.png",
        )
        create_emoji_test_category(
            name="Food",
            emoji="🍕",
            background_color="#00FF00",
            icon="icon2.png",
        )

        client.force_login(user)

        # Act
        response = client.get("/api/categories/")
        response_data = response.json()

        expected_count = 2

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert len(response_data) == expected_count

        assert response_data[0]["id"]
        assert response_data[0]["name"] == "Entertainment"
        assert response_data[0]["emoji"] == "🎬"
        assert response_data[0]["icon"]
        assert response_data[0]["background_color"] == "#FF0000"
        assert response_data[0]["created_at"]
        assert response_data[0]["updated_at"]

        assert response_data[1]["id"]
        assert response_data[1]["name"] == "Food"
        assert response_data[1]["emoji"] == "🍕"
        assert response_data[1]["icon"]
        assert response_data[1]["background_color"] == "#00FF00"
        assert response_data[1]["created_at"]
        assert response_data[1]["updated_at"]

    @pytest.mark.django_db
    def test_list_categories_empty_success(self, client: Client) -> None:
        """Test that an empty list is returned when no categories exist."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        # Act
        response = client.get("/api/categories/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert len(response_data) == 0


class TestRetrieveCategoryView:
    """Test the RetrieveCategoryView."""

    @pytest.mark.django_db
    def test_retrieve_category_success(self, client: Client) -> None:
        """Test that a category can be retrieved successfully."""
        # Arrange
        user = create_test_user()
        category = create_emoji_test_category(
            name="Entertainment",
            emoji="🎥",
            background_color="#FF0000",
            icon="icon.png",
        )

        client.force_login(user)

        # Act
        response = client.get(f"/api/categories/{category.id}/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["id"]
        assert response_data["name"] == "Entertainment"
        assert response_data["emoji"] == "🎥"
        assert response_data["icon"]
        assert response_data["background_color"] == "#FF0000"
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_retrieve_category_not_found(self, client: Client) -> None:
        """Test that retrieving a non-existent category returns 404."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        # Act
        response = client.get("/api/categories/nonexistent-id/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteCategoryView:
    """Test the DeleteCategoryView."""

    @pytest.mark.django_db
    def test_delete_category_success(self, client: Client) -> None:
        """Test that a category can be deleted successfully."""
        # Arrange
        user = create_test_user()
        category = create_emoji_test_category(
            name="Entertainment",
            emoji="🎥",
            background_color="#FF0000",
            icon="icon.png",
        )

        client.force_login(user)

        # Act
        response = client.delete(f"/api/categories/{category.id}/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_delete_category_not_found(self, client: Client) -> None:
        """Test that deleting a non-existent category returns 404."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        # Act
        response = client.delete("/api/categories/nonexistent-id/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
