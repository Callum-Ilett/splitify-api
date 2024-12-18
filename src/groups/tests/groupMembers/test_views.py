"""Test group members views."""

import pytest
from django.test import Client
from rest_framework import status

from core.test_helpers import create_test_user
from groups.models import GroupMemberRole
from groups.tests.groupMembers.test_helpers import create_test_group_member
from groups.tests.groups.test_helpers import create_test_group


class TestGroupMembersViewUnauthenticated:
    """Test group members views when the user is not authenticated."""

    @pytest.mark.django_db
    def test_create_group_member_unauthenticated_fails(self, client: Client) -> None:
        """Test that a user cannot create a group member when not authenticated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()

        payload = {
            "group": str(group.id),
            "user": str(user.id),  # type: ignore
        }

        # Act
        response = client.post("/api/group-members/", payload, "application/json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_edit_patch_group_member_unauthenticated_fails(
        self, client: Client
    ) -> None:
        """Test that a user cannot edit a group member when not authenticated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(user=user, group=group)

        payload = {
            "role": "ADMIN",
        }

        # Act
        response = client.patch(
            f"/api/group-members/{group_member.id}/",
            payload,
            "application/json",
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_edit_put_group_member_unauthenticated_fails(self, client: Client) -> None:
        """Test that a user cannot edit a group member when not authenticated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(user=user, group=group)

        payload = {
            "group": str(group.id),
            "user": str(user.id),  # type: ignore
            "role": "ADMIN",
        }

        # Act
        response = client.put(
            f"/api/group-members/{group_member.id}/",
            payload,
            "application/json",
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_delete_group_member_unauthenticated_fails(self, client: Client) -> None:
        """Test that a user cannot delete a group member when not authenticated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(user=user, group=group)

        # Act
        response = client.delete(f"/api/group-members/{group_member.id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_group_members_unauthenticated_fails(self, client: Client) -> None:
        """Test that a user cannot get group members when not authenticated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        create_test_group_member(user=user, group=group)

        # Act
        response = client.get("/api/group-members/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_retrieve_group_members_unauthenticated_fails(self, client: Client) -> None:
        """Test that a user cannot retrieve group members when not authenticated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(user=user, group=group)

        # Act
        response = client.get(f"/api/group-members/{group_member.id}/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCreateGroupMemberView:
    """Test create group member view."""

    @pytest.mark.django_db
    def test_create_group_member_success(self, client: Client) -> None:
        """Test that a group member can be created successfully."""
        # Arrange
        user = create_test_user()
        group = create_test_group()

        payload = {
            "group": str(group.id),
            "user": str(user.pk),
            "role": GroupMemberRole.MEMBER,
        }

        client.force_login(user)

        # Act
        response = client.post("/api/group-members/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        assert response_data["group"] == str(group.id)
        assert response_data["user"] == str(user.pk)
        assert response_data["role"] == GroupMemberRole.MEMBER
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_create_group_member_admin_success(self, client: Client) -> None:
        """Test that a group member can be created with admin role."""
        # Arrange
        user = create_test_user()
        group = create_test_group()

        payload = {
            "group": str(group.id),
            "user": str(user.pk),
            "role": GroupMemberRole.ADMIN,
        }

        client.force_login(user)

        # Act
        response = client.post("/api/group-members/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        assert response_data["group"] == str(group.id)
        assert response_data["user"] == str(user.pk)
        assert response_data["role"] == GroupMemberRole.ADMIN
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_create_group_member_owner_success(self, client: Client) -> None:
        """Test that a group member can be created with owner role."""
        # Arrange
        user = create_test_user()
        group = create_test_group()

        payload = {
            "group": str(group.id),
            "user": str(user.pk),
            "role": GroupMemberRole.OWNER,
        }

        client.force_login(user)

        # Act
        response = client.post("/api/group-members/", payload, "application/json")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        assert response_data["group"] == str(group.id)
        assert response_data["user"] == str(user.pk)
        assert response_data["role"] == GroupMemberRole.OWNER
        assert response_data["created_at"]
        assert response_data["updated_at"]


class TestEditGroupMemberView:
    """Test edit group member view."""

    @pytest.mark.django_db
    def test_edit_group_member_role_success(self, client: Client) -> None:
        """Test that a group member's role can be updated."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(
            user=user, group=group, role=GroupMemberRole.MEMBER
        )

        payload = {
            "role": GroupMemberRole.ADMIN,
        }

        client.force_login(user)

        # Act
        response = client.patch(
            f"/api/group-members/{group_member.id}/",
            payload,
            "application/json",
        )
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["group"] == str(group.id)
        assert response_data["user"] == str(user.pk)
        assert response_data["role"] == GroupMemberRole.ADMIN
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_edit_nonexistent_group_member_fails(self, client: Client) -> None:
        """Test that editing a nonexistent group member fails."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        payload = {
            "role": GroupMemberRole.ADMIN,
        }

        # Act
        response = client.patch(
            "/api/group-members/nonexistent-id/",
            payload,
            "application/json",
        )

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestRetrieveGroupMemberView:
    """Test retrieve group member view."""

    @pytest.mark.django_db
    def test_retrieve_group_member_success(self, client: Client) -> None:
        """Test that a group member can be retrieved."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(user=user, group=group)

        client.force_login(user)

        # Act
        response = client.get(f"/api/group-members/{group_member.id}/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["group"] == str(group.id)
        assert response_data["user"] == str(user.pk)
        assert response_data["role"] == GroupMemberRole.MEMBER
        assert response_data["created_at"]
        assert response_data["updated_at"]

    @pytest.mark.django_db
    def test_retrieve_nonexistent_group_member_fails(self, client: Client) -> None:
        """Test that retrieving a nonexistent group member fails."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        # Act
        response = client.get("/api/group-members/nonexistent-id/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestListGroupMembersView:
    """Test list group members view."""

    @pytest.mark.django_db
    def test_list_group_members_success(self, client: Client) -> None:
        """Test that group members can be listed."""
        # Arrange
        user1 = create_test_user(username="user1", email="user1@test.com")
        user2 = create_test_user(username="user2", email="user2@test.com")
        group = create_test_group()

        create_test_group_member(user=user1, group=group)
        create_test_group_member(user=user2, group=group, role=GroupMemberRole.ADMIN)

        client.force_login(user1)

        # Act
        response = client.get("/api/group-members/")
        response_data = response.json()

        expected_count = 2

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["count"] == expected_count
        assert len(response_data["results"]) == expected_count
        assert response_data["results"][0]["group"] == str(group.id)
        assert response_data["results"][0]["user"] == str(user1.pk)
        assert response_data["results"][0]["role"] == GroupMemberRole.MEMBER
        assert response_data["results"][0]["created_at"]
        assert response_data["results"][0]["updated_at"]

        assert response_data["results"][1]["group"] == str(group.id)
        assert response_data["results"][1]["user"] == str(user2.pk)
        assert response_data["results"][1]["role"] == GroupMemberRole.ADMIN
        assert response_data["results"][1]["created_at"]
        assert response_data["results"][1]["updated_at"]

    @pytest.mark.django_db
    def test_list_empty_group_members_success(self, client: Client) -> None:
        """Test that an empty list is returned when no group members exist."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        # Act
        response = client.get("/api/group-members/")
        response_data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK

        assert response_data["count"] == 0
        assert len(response_data["results"]) == 0


class TestDeleteGroupMemberView:
    """Test delete group member view."""

    @pytest.mark.django_db
    def test_delete_group_member_success(self, client: Client) -> None:
        """Test that a group member can be deleted."""
        # Arrange
        user = create_test_user()
        group = create_test_group()
        group_member = create_test_group_member(user=user, group=group)

        client.force_login(user)

        # Act
        response = client.delete(f"/api/group-members/{group_member.id}/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_delete_nonexistent_group_member_fails(self, client: Client) -> None:
        """Test that deleting a nonexistent group member fails."""
        # Arrange
        user = create_test_user()
        client.force_login(user)

        # Act
        response = client.delete("/api/group-members/nonexistent-id/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
