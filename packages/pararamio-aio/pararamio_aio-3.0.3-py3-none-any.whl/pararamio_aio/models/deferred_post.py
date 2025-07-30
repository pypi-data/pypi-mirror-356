"""Async DeferredPost model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio_aio._core import PararamNotFound
from pararamio_aio._core.utils.helpers import format_datetime

from .base import BaseModel

if TYPE_CHECKING:
    from ..client import AsyncPararamio

__all__ = ("DeferredPost",)


class DeferredPost(BaseModel):
    """Async DeferredPost model for scheduled posts."""

    _data: dict[str, Any]  # Type hint for mypy

    def __init__(self, client: AsyncPararamio, id: int, **kwargs):
        """Initialize async deferred post.

        Args:
            client: AsyncPararamio client
            id: Deferred post ID
            **kwargs: Additional post data
        """
        super().__init__(client, id=id, **kwargs)
        self.id = id

    @property
    def user_id(self) -> int:
        """Get post author user ID."""
        return self._data.get("user_id", 0)

    @property
    def chat_id(self) -> int:
        """Get target chat ID."""
        return self._data.get("chat_id", 0)

    @property
    def text(self) -> str:
        """Get post text."""
        # Check both top-level and nested data
        text = self._data.get("text")
        if text is None and "data" in self._data:
            text = self._data["data"].get("text")
        return text or ""

    @property
    def reply_no(self) -> int | None:
        """Get reply post number if any."""
        reply_no = self._data.get("reply_no")
        if reply_no is None and "data" in self._data:
            reply_no = self._data["data"].get("reply_no")
        return reply_no

    @property
    def time_created(self) -> datetime | None:
        """Get creation time."""
        return self._data.get("time_created")

    @property
    def time_sending(self) -> datetime | None:
        """Get scheduled sending time."""
        return self._data.get("time_sending")

    @property
    def data(self) -> dict[str, Any]:
        """Get additional post data."""
        return self._data.get("data", {})

    async def load(self) -> DeferredPost:
        """Load full deferred post data from API.

        Returns:
            Self with updated data

        Raises:
            PararamNotFound: If post not found
        """
        posts = await self.get_deferred_posts(self.client)

        for post in posts:
            if post.id == self.id:
                self._data = post._data
                return self

        raise PararamNotFound(f"Deferred post with id {self.id} not found")

    async def delete(self) -> bool:
        """Delete this deferred post.

        Returns:
            True if successful
        """
        url = f"/msg/deferred/{self.id}"
        await self.client.api_delete(url)
        return True

    @classmethod
    async def create(
        cls,
        client: AsyncPararamio,
        chat_id: int,
        text: str,
        *,
        time_sending: datetime,
        reply_no: int | None = None,
        quote_range: tuple[int, int] | None = None,
    ) -> DeferredPost:
        """Create a new deferred (scheduled) post.

        Args:
            client: AsyncPararamio client
            chat_id: Target chat ID
            text: Post text
            time_sending: When to send the post
            reply_no: Optional post number to reply to
            quote_range: Optional quote range as (start, end) tuple

        Returns:
            Created DeferredPost object
        """
        url = "/msg/deferred"
        data = {
            "chat_id": chat_id,
            "text": text,
            "time_sending": format_datetime(time_sending),
            "reply_no": reply_no,
            "quote_range": quote_range,
        }

        response = await client.api_post(url, data)

        return cls(
            client,
            id=int(response["deferred_post_id"]),
            chat_id=chat_id,
            data=data,
            time_sending=time_sending,
            **response,
        )

    @classmethod
    async def get_deferred_posts(cls, client: AsyncPararamio) -> list[DeferredPost]:
        """Get all deferred posts for the current user.

        Args:
            client: AsyncPararamio client

        Returns:
            List of DeferredPost objects
        """
        url = "/msg/deferred"
        response = await client.api_get(url)
        posts_data = response.get("posts", [])

        return [cls(client, **post_data) for post_data in posts_data]

    def __str__(self) -> str:
        """String representation."""
        return self.text or f"DeferredPost({self.id})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, DeferredPost):
            return False
        return self.id == other.id
