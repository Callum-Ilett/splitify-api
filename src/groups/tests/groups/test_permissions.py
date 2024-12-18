"""Test group permissions."""

import pytest
from django.test import Client
from rest_framework import status

from core.test_helpers import create_test_user
from currency.tests.test_helpers import create_test_currency
from groups.models import GroupMemberRole
from groups.tests.groupMembers.test_helpers import create_test_group_member
from groups.tests.groups.test_helpers import create_test_group


class TestCreateGroupPermissions:
    """Test create group permissions."""

    @pytest.mark.django_db
    def test_unauthenticated_fails(self, client: Client) -> None:
        """Test that an unauthenticated user cannot create a group."""
        # Arrange
        currency = create_test_currency()

        payload = {
            "title": "Miami Summer 2024 Squad 🌴",
            "description": "Planning our Miami beach vacation!",
            "currency": str(currency.id),
        }

        # Act
        response = client.post("/api/groups/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestListGroupPermissions:
    """Test list group permissions."""

    @pytest.mark.django_db
    def test_list_group_unauthenticated_fails(self, client: Client) -> None:
        """Test that an unauthenticated user cannot list groups."""
        # Act
        response = client.get("/api/groups/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRetrieveGroupPermissions:
    """Test retrieve group permissions."""

    @pytest.mark.django_db
    def test_retrieve_group_unauthenticated_fails(self, client: Client) -> None:
        """Test that an unauthenticated user cannot retrieve a group."""
        # Arrange
        group = create_test_group()

        # Act
        response = client.get(f"/api/groups/{group.id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestPatchUpdatePermissions:
    """Test patch update permissions."""

    @pytest.mark.django_db
    def test_update_group_owner_success(self, client: Client) -> None:
        """Test that an owner of a group can update it."""
        # Arrange
        user = create_test_user()
        group = create_test_group(created_by=user)

        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
        }

        client.force_login(user)

        # Act
        response = client.patch(f"/api/groups/{group.id}/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_group_admin_success(self, client: Client) -> None:
        """Test that an admin of a group can update it."""
        # Arrange
        user = create_test_user()
        user_2 = create_test_user(username="user_2", email="user_2@email.com")

        group = create_test_group(created_by=user)
        create_test_group_member(user=user_2, group=group, role=GroupMemberRole.ADMIN)

        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
        }

        client.force_login(user_2)

        # Act
        response = client.patch(f"/api/groups/{group.id}/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_group_member_fails(self, client: Client) -> None:
        """Test that a member of a group cannot update it."""
        # Arrange
        user = create_test_user()
        user_2 = create_test_user(username="user_2", email="user_2@email.com")

        group = create_test_group(created_by=user)
        create_test_group_member(user=user_2, group=group, role=GroupMemberRole.MEMBER)

        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
        }

        client.force_login(user_2)

        # Act
        response = client.patch(f"/api/groups/{group.id}/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert (
            response_data["detail"]
            == "You do not have permission to perform this action."
        )

    @pytest.mark.django_db
    def test_update_group_unauthenticated_fails(self, client: Client) -> None:
        """Test that an unauthenticated user cannot update a group."""
        # Arrange
        group = create_test_group()
        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
        }

        # Act
        response = client.patch(f"/api/groups/{group.id}/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestPutUpdatePermissions:
    """Test put update permissions."""

    @pytest.mark.django_db
    def test_update_group_owner_success(self, client: Client) -> None:
        """Test that an owner of a group can update it."""
        # Arrange
        user = create_test_user()
        group = create_test_group(created_by=user)

        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
            "description": "Planning our Miami beach vacation!",
            "currency": str(group.currency.id),
        }

        client.force_login(user)

        # Act
        response = client.put(f"/api/groups/{group.id}/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_group_admin_success(self, client: Client) -> None:
        """Test that an admin of a group can update it."""
        # Arrange
        user = create_test_user()
        user_2 = create_test_user(username="user_2", email="user_2@email.com")

        group = create_test_group(created_by=user)
        create_test_group_member(user=user_2, group=group, role=GroupMemberRole.ADMIN)

        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
            "description": "Planning our Miami beach vacation!",
            "currency": str(group.currency.id),
        }

        client.force_login(user_2)

        # Act
        response = client.put(f"/api/groups/{group.id}/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_group_member_fails(self, client: Client) -> None:
        """Test that a member of a group cannot update it."""
        # Arrange
        user = create_test_user()
        user_2 = create_test_user(username="user_2", email="user_2@email.com")

        group = create_test_group(created_by=user)
        create_test_group_member(user=user_2, group=group, role=GroupMemberRole.MEMBER)

        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
            "description": "Planning our Miami beach vacation!",
            "currency": str(group.currency.id),
        }

        client.force_login(user_2)

        # Act
        response = client.put(f"/api/groups/{group.id}/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert (
            response_data["detail"]
            == "You do not have permission to perform this action."
        )

    @pytest.mark.django_db
    def test_update_group_unauthenticated_fails(self, client: Client) -> None:
        """Test that an unauthenticated user cannot update a group."""
        # Arrange
        group = create_test_group()
        payload = {
            "title": "Miami Summer 2024 Squad(edited)🌴",
            "description": "Planning our Miami beach vacation!",
            "currency": str(group.currency.id),
        }

        # Act
        response = client.put(f"/api/groups/{group.id}/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeletePermissions:
    """Test delete permissions."""

    @pytest.mark.django_db
    def test_delete_group_owner_success(self, client: Client) -> None:
        """Test that an admin of a group cannot delete it."""
        # Arrange
        user = create_test_user()
        group = create_test_group(created_by=user)
        client.force_login(user)

        # Act
        response = client.delete(f"/api/groups/{group.id}/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_delete_group_admin_fails(self, client: Client) -> None:
        """Test that an admin of a group cannot delete it."""
        # Arrange
        user = create_test_user()
        user_2 = create_test_user(username="user_2", email="user_2@email.com")

        group = create_test_group(created_by=user)
        create_test_group_member(user=user_2, group=group, role=GroupMemberRole.ADMIN)

        client.force_login(user_2)

        # Act
        response = client.delete(f"/api/groups/{group.id}/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert (
            response_data["detail"]
            == "You do not have permission to perform this action."
        )

    @pytest.mark.django_db
    def test_delete_group_member_fails(self, client: Client) -> None:
        """Test that a member of a group cannot delete it."""
        # Arrange
        user = create_test_user()
        user_2 = create_test_user(username="user_2", email="user_2@email.com")

        group = create_test_group(created_by=user)
        create_test_group_member(user=user_2, group=group, role=GroupMemberRole.MEMBER)

        client.force_login(user_2)

        # Act
        response = client.delete(f"/api/groups/{group.id}/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert (
            response_data["detail"]
            == "You do not have permission to perform this action."
        )

    @pytest.mark.django_db
    def test_delete_group_unauthenticated_fails(self, client: Client) -> None:
        """Test that an unauthenticated user cannot delete a group."""
        # Arrange
        group = create_test_group()

        # Act
        response = client.delete(f"/api/groups/{group.id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
