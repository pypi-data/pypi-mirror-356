"""Async Team model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio_aio._core import PararamioRequestException

from .base import BaseModel
from .group import Group
from .user import User

if TYPE_CHECKING:
    from ..client import AsyncPararamio

__all__ = ("TeamMemberStatus", "TeamMember", "Team")


class TeamCommonMixin:
    """Mixin for common team/member properties."""

    _data: dict[str, Any]  # This will be provided by BaseModel

    @property
    def state(self) -> str:
        """Get state."""
        return self._data.get("state", "")

    @property
    def time_created(self) -> datetime | None:
        """Get creation time."""
        return self._data.get("time_created")

    @property
    def time_updated(self) -> datetime | None:
        """Get last update time."""
        return self._data.get("time_updated")


class TeamMemberStatus(BaseModel):
    """Team member status model."""

    def __init__(self, client: AsyncPararamio, id: int, **kwargs):
        """Initialize team member status.

        Args:
            client: AsyncPararamio client
            id: Status ID
            **kwargs: Additional status data
        """
        super().__init__(client, id=id, **kwargs)
        self.id = id

    @property
    def user_id(self) -> int:
        """Get user ID."""
        return self._data.get("user_id", 0)

    @property
    def setter_id(self) -> int:
        """Get setter user ID."""
        return self._data.get("setter_id", 0)

    @property
    def org_id(self) -> int:
        """Get organization ID."""
        return self._data.get("org_id", 0)

    @property
    def time_created(self) -> datetime | None:
        """Get creation time."""
        return self._data.get("time_created")

    @property
    def status(self) -> str:
        """Get status text."""
        return self._data.get("status", "")


class TeamMember(TeamCommonMixin, BaseModel):
    """Team member model."""

    def __init__(self, client: AsyncPararamio, id: int, org_id: int, **kwargs):
        """Initialize team member.

        Args:
            client: AsyncPararamio client
            id: Member ID
            org_id: Organization ID
            **kwargs: Additional member data
        """
        super().__init__(client, id=id, org_id=org_id, **kwargs)
        self.id = id
        self.org_id = org_id

    @property
    def email(self) -> str:
        """Get member email."""
        return self._data.get("email", "")

    @property
    def chats(self) -> list[int]:
        """Get member chat IDs."""
        return self._data.get("chats", [])

    @property
    def groups(self) -> list[int]:
        """Get member group IDs."""
        return self._data.get("groups", [])

    @property
    def is_admin(self) -> bool:
        """Check if member is admin."""
        return self._data.get("is_admin", False)

    @property
    def is_member(self) -> bool:
        """Check if user is active member."""
        return self._data.get("is_member", True)

    @property
    def last_activity(self) -> datetime | None:
        """Get last activity time."""
        return self._data.get("last_activity")

    @property
    def phonenumber(self) -> str | None:
        """Get phone number."""
        return self._data.get("phonenumber")

    @property
    def two_step_enabled(self) -> bool:
        """Check if two-step verification is enabled."""
        return self._data.get("two_step_enabled", False)

    @property
    def inviter_id(self) -> int | None:
        """Get inviter user ID."""
        return self._data.get("inviter_id")

    async def get_user(self) -> User | None:
        """Get associated User object.

        Returns:
            User object or None
        """
        return await self.client.get_user_by_id(self.id)

    async def get_last_status(self) -> TeamMemberStatus | None:
        """Get last status for this member.

        Returns:
            TeamMemberStatus or None if no status
        """
        url = f"/core/org/status?user_ids={self.id}"
        response = await self.client.api_get(url)
        data = response.get("data", [])

        if not data:
            return None

        return TeamMemberStatus(self.client, **data[0])

    async def add_status(self, status: str) -> bool:
        """Add status for this member.

        Args:
            status: Status text

        Returns:
            True if successful
        """
        url = "/core/org/status"
        data = {
            "org_id": self.org_id,
            "status": status,
            "user_id": self.id,
        }
        response = await self.client.api_post(url, data=data)
        return bool(response) and response.get("result") == "OK"

    def __str__(self) -> str:
        """String representation."""
        return self.email or str(self.id)

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, (TeamMember, User)):
            return False
        return self.id == other.id


class Team(TeamCommonMixin, BaseModel):
    """Async Team model with explicit loading."""

    def __init__(self, client: AsyncPararamio, id: int, **kwargs):
        """Initialize async team.

        Args:
            client: AsyncPararamio client
            id: Team ID
            **kwargs: Additional team data
        """
        super().__init__(client, id=id, **kwargs)
        self.id = id

    @property
    def title(self) -> str:
        """Get team title."""
        return self._data.get("title", "")

    @property
    def slug(self) -> str:
        """Get team slug."""
        return self._data.get("slug", "")

    @property
    def description(self) -> str | None:
        """Get team description."""
        return self._data.get("description")

    @property
    def email_domain(self) -> str | None:
        """Get email domain."""
        return self._data.get("email_domain")

    @property
    def is_active(self) -> bool:
        """Check if team is active."""
        return self._data.get("is_active", True)

    @property
    def two_step_required(self) -> bool:
        """Check if two-step verification is required."""
        return self._data.get("two_step_required", False)

    @property
    def default_thread_id(self) -> int:
        """Get default thread ID."""
        return self._data.get("default_thread_id", 0)

    @property
    def guest_thread_id(self) -> int | None:
        """Get guest thread ID."""
        return self._data.get("guest_thread_id")

    @property
    def inviter_id(self) -> int | None:
        """Get inviter user ID."""
        return self._data.get("inviter_id")

    @property
    def users(self) -> list[int]:
        """Get team user IDs."""
        return self._data.get("users", [])

    @property
    def admins(self) -> list[int]:
        """Get team admin IDs."""
        return self._data.get("admins", [])

    @property
    def groups(self) -> list[int]:
        """Get team group IDs."""
        return self._data.get("groups", [])

    @property
    def guests(self) -> list[int]:
        """Get team guest IDs."""
        return self._data.get("guests", [])

    async def load(self) -> Team:
        """Load full team data from API.

        Returns:
            Self with updated data
        """
        url = f"/core/org?ids={self.id}"
        response = await self.client.api_get(url)

        if "orgs" in response and response["orgs"]:
            self._data.update(response["orgs"][0])
        else:
            self._data.update(response)

        return self

    async def create_role(self, name: str, description: str | None = None) -> Group:
        """Create a new role (group) in this team.

        Args:
            name: Role name
            description: Role description

        Returns:
            Created Group object
        """
        return await Group.create(
            self.client,
            name=name,
            unique_name=name,  # Async version requires unique_name
            description=description or "",
            # Note: organization_id parameter not supported in async Group.create
        )

    async def get_member_info(self, user_id: int) -> TeamMember:
        """Get information about a specific member.

        Args:
            user_id: User ID

        Returns:
            TeamMember object

        Raises:
            PararamioRequestException: If member not found
        """
        url = f"/core/org/{self.id}/member_info/{user_id}"
        response = await self.client.api_get(url)

        if not response:
            raise PararamioRequestException(f"empty response for user {user_id}")

        return TeamMember(self.client, org_id=self.id, **response)

    async def get_members_info(self) -> list[TeamMember]:
        """Get information about all team members.

        Returns:
            List of TeamMember objects
        """
        url = f"/core/org/{self.id}/member_info"
        response = await self.client.api_get(url)

        if response:
            return [
                TeamMember(self.client, org_id=self.id, **member_data)
                for member_data in response.get("data", [])
            ]
        return []

    async def mark_all_messages_as_read(self) -> bool:
        """Mark all messages in this team as read.

        Returns:
            True if successful
        """
        return await self.client.mark_all_messages_as_read(self.id)

    @classmethod
    async def get_my_team_ids(cls, client: AsyncPararamio) -> list[int]:
        """Get IDs of teams the current user belongs to.

        Args:
            client: AsyncPararamio client

        Returns:
            List of team IDs
        """
        url = "/core/org/sync"
        response = await client.api_get(url)
        return response.get("ids", [])

    @classmethod
    async def load_teams(cls, client: AsyncPararamio) -> list[Team]:
        """Load all teams for the current user.

        Args:
            client: AsyncPararamio client

        Returns:
            List of Team objects
        """
        ids = await cls.get_my_team_ids(client)

        if not ids:
            return []

        url = "/core/org?ids=" + ",".join(map(str, ids))
        response = await client.api_get(url)

        if response:
            return [cls(client, **team_data) for team_data in response.get("orgs", [])]

        return []

    def __contains__(self, item) -> bool:
        """Check if user is in team."""
        if not isinstance(item, (TeamMember, User)):
            return False
        return item.id in self.users

    def __str__(self) -> str:
        """String representation."""
        return self.title or f"Team({self.id})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Team):
            return False
        return self.id == other.id
