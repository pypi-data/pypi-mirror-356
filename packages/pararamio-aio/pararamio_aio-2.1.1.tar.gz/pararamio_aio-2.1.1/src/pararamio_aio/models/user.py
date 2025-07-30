"""Async User model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio_aio._core import PararamNotFound

from .activity import Activity, ActivityAction
from .base import BaseModel

if TYPE_CHECKING:
    from ..client import AsyncPararamio
    from .chat import Chat
    from .post import Post

__all__ = ("User", "UserSearchResult")


@dataclass
class UserSearchResult:
    """User search result with explicit data."""

    id: int
    avatar: str | None
    name: str
    unique_name: str
    custom_name: str | None
    time_created: str
    time_updated: str
    other_blocked: bool
    pm_thread_id: int | None
    is_bot: bool
    client: AsyncPararamio

    @property
    def has_pm(self) -> bool:
        """Check if user has PM thread."""
        return self.pm_thread_id is not None

    async def get_pm_thread(self) -> Chat:
        """Get PM thread for this user.

        Returns:
            Chat object for PM
        """
        if self.pm_thread_id:
            chat = await self.client.get_chat_by_id(self.pm_thread_id)
            if chat is None:
                raise ValueError(f"Chat with id {self.pm_thread_id} not found")
            return chat
        # Create new PM thread
        return await self.create_pm_thread()

    async def create_pm_thread(self) -> Chat:
        """Create a new PM thread with this user.

        Returns:
            New chat object
        """

        url = f"/core/chat/pm/{self.id}"
        response = await self.client.api_post(url)
        chat_id = response["chat_id"]
        chat = await self.client.get_chat_by_id(chat_id)
        if chat is None:
            raise ValueError(f"Failed to create or retrieve chat with id {chat_id}")
        return chat

    async def send_message(self, text: str) -> Post:
        """Send a private message to this user.

        Args:
            text: Message text

        Returns:
            Created post
        """
        chat = await self.get_pm_thread()
        return await chat.send_message(text)


class User(BaseModel):
    """Async User model with explicit loading."""

    def __init__(self, client: AsyncPararamio, id: int, name: str | None = None, **kwargs):
        """Initialize async user.

        Args:
            client: AsyncPararamio client
            id: User ID
            name: Optional user name
            **kwargs: Additional user data
        """
        super().__init__(client, id=id, name=name, **kwargs)
        self.id = id

    @property
    def name(self) -> str | None:
        """Get user name."""
        return self._data.get("name")

    @property
    def unique_name(self) -> str | None:
        """Get user unique name."""
        return self._data.get("unique_name")

    @property
    def is_bot(self) -> bool:
        """Check if user is a bot."""
        return self._data.get("is_bot", False)

    @property
    def time_created(self) -> datetime | None:
        """Get user creation time."""
        return self._data.get("time_created")

    @property
    def time_updated(self) -> datetime | None:
        """Get user last update time."""
        return self._data.get("time_updated")

    @property
    def info(self) -> str | None:
        """Get user info."""
        return self._data.get("info")

    @property
    def organizations(self) -> list[int]:
        """Get user organization IDs."""
        return self._data.get("organizations", [])

    async def load(self) -> User:
        """Load full user data from API.

        Returns:
            Self with updated data
        """
        users = await self.client.get_users_by_ids([self.id])
        if not users:
            raise PararamNotFound(f"User {self.id} not found")

        # Update our data with loaded data
        self._data.update(users[0]._data)
        return self

    async def send_private_message(self, text: str) -> Post:
        """Send a private message to this user.

        Args:
            text: Message text

        Returns:
            Created post
        """
        url = "/msg/post/private"
        response = await self.client.api_post(url, {"text": text, "user_id": self.id})

        # Load the created post
        post = await self.client.get_post(response["chat_id"], response["post_no"])
        if post is None:
            raise ValueError(
                f"Failed to retrieve post {response['post_no']} from chat {response['chat_id']}"
            )
        return post

    async def _activity_page_loader(
        self, action: ActivityAction | None = None, page: int = 1
    ) -> dict[str, Any]:
        """Load activity page from API.

        Args:
            action: Optional action type to filter
            page: Page number

        Returns:
            API response dict
        """
        url = f"/activity?user_id={self.id}&page={page}"
        if action:
            url += f"&action={action.value}"

        return await self.client.api_get(url)

    async def get_activity(
        self, start: datetime, end: datetime, actions: list[ActivityAction] | None = None
    ) -> list[Activity]:
        """Get user activity within date range.

        Args:
            start: Start datetime
            end: End datetime
            actions: Optional list of ActivityAction types to filter

        Returns:
            List of Activity objects sorted by time
        """

        # Create async page loader
        async def page_loader(
            action: ActivityAction | None = None, page: int = 1
        ) -> dict[str, Any]:
            return await self._activity_page_loader(action, page)

        return await Activity.get_activity(page_loader, start, end, actions)

    @classmethod
    async def search(cls, client: AsyncPararamio, query: str) -> list[UserSearchResult]:
        """Search for users.

        Args:
            client: AsyncPararamio client
            query: Search query

        Returns:
            List of search results
        """
        url = f"/users?flt={query}"
        response = await client.api_get(url)

        results = []
        for data in response.get("users", []):
            result = UserSearchResult(client=client, **data)
            results.append(result)

        return results

    def __eq__(self, other) -> bool:
        """Check equality with another user."""
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __str__(self) -> str:
        """String representation."""
        return self.name or f"User({self.id})"
