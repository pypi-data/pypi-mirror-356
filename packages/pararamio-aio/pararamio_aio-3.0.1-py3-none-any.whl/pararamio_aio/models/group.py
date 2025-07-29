"""Async Group model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

# Imports from core
from pararamio_aio._core import (
    PararamioRequestException,
    PararamioValidationException,
    PararamNotFound,
)
from pararamio_aio._core.utils.helpers import join_ids

from .base import BaseModel

if TYPE_CHECKING:
    from ..client import AsyncPararamio

__all__ = ("Group",)


class Group(BaseModel):
    """Async Group model with explicit loading."""

    def __init__(self, client: AsyncPararamio, id: int, name: str | None = None, **kwargs):
        """Initialize async group.

        Args:
            client: AsyncPararamio client
            id: Group ID
            name: Optional group name
            **kwargs: Additional group data
        """
        super().__init__(client, id=id, name=name, **kwargs)
        self.id = id

    @property
    def name(self) -> str | None:
        """Get group name."""
        return self._data.get("name")

    @property
    def unique_name(self) -> str | None:
        """Get group unique name."""
        return self._data.get("unique_name")

    @property
    def description(self) -> str | None:
        """Get group description."""
        return self._data.get("description")

    @property
    def email_domain(self) -> str | None:
        """Get group email domain."""
        return self._data.get("email_domain")

    @property
    def time_created(self) -> datetime | None:
        """Get group creation time."""
        return self._data.get("time_created")

    @property
    def time_updated(self) -> datetime | None:
        """Get group last update time."""
        return self._data.get("time_updated")

    @property
    def is_active(self) -> bool:
        """Check if group is active."""
        return self._data.get("active", True)

    @property
    def members_count(self) -> int:
        """Get group members count."""
        return self._data.get("members_count", 0)

    async def load(self) -> Group:
        """Load full group data from API.

        Returns:
            Self with updated data
        """
        groups = await self.client.get_groups_by_ids([self.id])
        if not groups:
            raise PararamNotFound(f"Group {self.id} not found")

        # Update our data with loaded data
        self._data.update(groups[0]._data)
        return self

    async def get_members(self) -> list[int]:
        """Get group member user IDs.

        Returns:
            List of user IDs
        """
        url = f"/group/{self.id}/members"
        response = await self.client.api_get(url)
        return response.get("members", [])

    async def add_members(self, user_ids: list[int]) -> bool:
        """Add members to group.

        Args:
            user_ids: List of user IDs to add

        Returns:
            True if successful
        """
        url = f"/group/{self.id}/members"
        data = {"user_ids": user_ids}
        response = await self.client.api_post(url, data)
        return response.get("success", False)

    async def add_member(self, user_id: int, reload: bool = True) -> None:
        """Add a single member to group.

        Args:
            user_id: User ID to add
            reload: Whether to reload group data after operation

        Raises:
            PararamioRequestException: If operation fails
        """
        url = f"/core/group/{self.id}/users/{user_id}"
        response = await self.client.api_post(url)

        if response.get("result") == "OK":
            # Update local cache if we have users data
            if "users" in self._data:
                if user_id not in self._data["users"]:
                    self._data["users"].append(user_id)

            if reload:
                await self.load()
        else:
            raise PararamioRequestException(f"Failed to add user {user_id} to group {self.id}")

    async def remove_members(self, user_ids: list[int]) -> bool:
        """Remove members from group.

        Args:
            user_ids: List of user IDs to remove

        Returns:
            True if successful
        """
        # Use DELETE with query parameters instead of request body
        url = f"/group/{self.id}/members?user_ids={join_ids(user_ids)}"
        response = await self.client.api_delete(url)
        return response.get("success", False)

    async def remove_member(self, user_id: int, reload: bool = True) -> None:
        """Remove a single member from group.

        Args:
            user_id: User ID to remove
            reload: Whether to reload group data after operation

        Raises:
            PararamioRequestException: If operation fails
        """
        url = f"/core/group/{self.id}/users/{user_id}"
        response = await self.client.api_delete(url)

        if response.get("result") == "OK":
            # Update local cache if we have users data
            if "users" in self._data and user_id in self._data["users"]:
                self._data["users"].remove(user_id)

            # Also remove from admins if present
            if "admins" in self._data and user_id in self._data["admins"]:
                self._data["admins"].remove(user_id)

            if reload:
                await self.load()
        else:
            raise PararamioRequestException(f"Failed to remove user {user_id} from group {self.id}")

    async def add_admins(self, admin_ids: list[int]) -> bool:
        """Add admin users to the group.

        Args:
            admin_ids: List of user IDs to make admins

        Returns:
            True if successful
        """
        url = f"/core/group/{self.id}/admins/{join_ids(admin_ids)}"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def update_settings(self, **kwargs) -> bool:
        """Update group settings.

        Args:
            **kwargs: Settings to update (name, description, etc.)

        Returns:
            True if successful
        """
        # Filter allowed fields
        allowed_fields = {"unique_name", "name", "description", "email_domain"}
        data = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not data:
            return False

        url = f"/group/{self.id}"
        response = await self.client.api_put(url, data)

        # Update local data
        if response.get("success"):
            self._data.update(data)
            return True

        return False

    async def edit(self, changes: dict[str, str | None], reload: bool = True) -> None:
        """Edit group settings.

        Args:
            changes: Dictionary of fields to change
            reload: Whether to reload group data after operation

        Raises:
            PararamioValidationException: If invalid fields provided
        """
        # Define editable fields
        editable_fields = ["unique_name", "name", "description", "email_domain"]

        # Validate fields
        invalid_fields = set(changes.keys()) - set(editable_fields)
        if invalid_fields:
            raise PararamioValidationException(
                f"Invalid fields: {invalid_fields}. Valid fields are: {editable_fields}"
            )

        # Ensure we have current data
        if not self._data.get("name"):
            await self.load()

        url = f"/core/group/{self.id}"
        response = await self.client.api_put(url, changes)

        if response.get("result") == "OK":
            # Update local data
            self._data.update(changes)

            if reload:
                await self.load()

    async def delete(self) -> bool:
        """Delete this group.

        Returns:
            True if successful
        """
        url = f"/group/{self.id}"
        response = await self.client.api_delete(url)
        return response.get("success", False)

    # @classmethod
    # async def search(cls, client: AsyncPararamio, query: str) -> list[Group]:
    #     """Search for groups.
    #
    #     DEPRECATED: Group search is not available in the API.
    #     Groups might be returned as part of user search results.
    #
    #     Args:
    #         client: AsyncPararamio client
    #         query: Search query
    #
    #     Returns:
    #         List of found groups
    #     """
    #     from urllib.parse import quote
    #     # Use the same endpoint as user search (they seem to be combined)
    #     url = f"/user/search?flt={quote(query)}"
    #     response = await client.api_get(url)
    #
    #     groups = []
    #     for group_data in response.get("groups", []):
    #         group = cls.from_dict(client, group_data)
    #         groups.append(group)
    #
    #     return groups

    @classmethod
    async def create(
        cls,
        client: AsyncPararamio,
        name: str,
        unique_name: str,
        description: str = "",
        email_domain: str | None = None,
    ) -> Group:
        """Create a new group.

        Args:
            client: AsyncPararamio client
            name: Group display name
            unique_name: Group unique identifier
            description: Group description
            email_domain: Optional email domain

        Returns:
            Created group object
        """
        data = {
            "name": name,
            "unique_name": unique_name,
            "description": description,
        }

        if email_domain:
            data["email_domain"] = email_domain

        response = await client.api_post("/group", data)
        group_id = response["group_id"]

        group = await client.get_group_by_id(group_id)
        if group is None:
            raise ValueError(f"Failed to retrieve created group with id {group_id}")
        return group

    def __eq__(self, other) -> bool:
        """Check equality with another group."""
        if not isinstance(other, Group):
            return False
        return self.id == other.id

    def __str__(self) -> str:
        """String representation."""
        return self.name or f"Group({self.id})"

    @classmethod
    async def search(cls, client: AsyncPararamio, search_string: str) -> list[Group]:
        """Search for groups.

        Note: This uses the user search endpoint which also returns groups.

        Args:
            client: AsyncPararamio client
            search_string: Search query

        Returns:
            List of matching groups
        """
        from urllib.parse import quote  # pylint: disable=import-outside-toplevel

        # Use the same endpoint as user search (they seem to be combined)
        url = f"/user/search?flt={quote(search_string)}&self=false"
        response = await client.api_get(url)
        groups = []
        for group_data in response.get("groups", []):
            group = cls.from_dict(client, group_data)
            groups.append(group)
        return groups
