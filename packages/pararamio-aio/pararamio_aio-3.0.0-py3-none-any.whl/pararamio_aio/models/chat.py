"""Async Chat model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any
from urllib.parse import quote_plus

# Imports from core
from pararamio_aio._core import (
    POSTS_LIMIT,
    PararamioLimitExceededException,
    PararamioRequestException,
    PararamModelNotLoaded,
    validate_post_load_range,
)
from pararamio_aio._core.utils.helpers import join_ids

from .base import BaseModel
from .post import Post

if TYPE_CHECKING:
    from ..client import AsyncPararamio
    from .file import File

__all__ = ("Chat",)


class Chat(BaseModel):  # pylint: disable=too-many-public-methods,duplicate-code
    """Async Chat model with explicit loading."""

    def __init__(self, client: AsyncPararamio, id: int, title: str | None = None, **kwargs):
        """Initialize async chat.

        Args:
            client: AsyncPararamio client
            id: Chat ID
            title: Optional chat title
            **kwargs: Additional chat data
        """
        # Only pass non-None values to avoid polluting _data
        init_data: dict[str, Any] = {"id": id}
        if title is not None:
            init_data["title"] = title
        init_data.update(kwargs)

        super().__init__(client, **init_data)
        self.id = id

    @property
    def title(self) -> str | None:
        """Get chat title."""
        return self._data.get("title")

    @property
    def description(self) -> str | None:
        """Get chat description."""
        if not self.is_loaded() and "description" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("description")

    @property
    def posts_count(self) -> int:
        """Get total posts count."""
        if "posts_count" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data["posts_count"]

    def is_loaded(self) -> bool:
        """Check if chat data has been loaded.

        Returns:
            True if chat data has been loaded, False otherwise
        """
        # Check for essential fields that are only present after loading
        return "posts_count" in self._data and "time_created" in self._data

    @property
    def is_private(self) -> bool:
        """Check if chat is private message."""
        return self._data.get("pm", False)

    @property
    def time_created(self) -> datetime | None:
        """Get chat creation time."""
        if not self.is_loaded() and "time_created" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("time_created")

    @property
    def time_updated(self) -> datetime | None:
        """Get chat last update time."""
        if not self.is_loaded() and "time_updated" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("time_updated")

    @property
    def author_id(self) -> int | None:
        """Get chat author ID."""
        if not self.is_loaded() and "author_id" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("author_id")

    @property
    def organization_id(self) -> int | None:
        """Get organization ID."""
        if not self.is_loaded() and "organization_id" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("organization_id")

    @property
    def is_favorite(self) -> bool:
        """Check if chat is favorite."""
        if not self.is_loaded() and "is_favorite" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("is_favorite", False)

    @property
    def last_read_post_no(self) -> int:
        """Get last read post number."""
        if not self.is_loaded() and "last_read_post_no" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("last_read_post_no", 0)

    @property
    def thread_users(self) -> list[int]:
        """Get thread user IDs."""
        if not self.is_loaded() and "thread_users" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("thread_users", [])

    @property
    def thread_admins(self) -> list[int]:
        """Get thread admin IDs."""
        if not self.is_loaded() and "thread_admins" not in self._data:
            raise PararamModelNotLoaded(
                "Chat data has not been loaded. Use load() to fetch chat data first."
            )
        return self._data.get("thread_admins", [])

    async def load(self) -> Chat:
        """Load full chat data from API.

        Returns:
            Self with updated data
        """
        # Use the same endpoint as sync version
        url = f"/core/chat?ids={self.id}"
        response = await self.client.api_get(url)
        if response and "chats" in response:
            chats = response.get("chats", [])
            if chats:
                self._data.update(chats[0])
                return self
        raise PararamioRequestException(f"failed to load data for chat id {self.id}")

    async def load_posts(
        self,
        start_post_no: int = -50,
        end_post_no: int = -1,
        limit: int = POSTS_LIMIT,
    ) -> list[Post]:
        """Load posts from chat.

        Args:
            start_post_no: Start post number (negative for from end)
            end_post_no: End post number (negative for from end)
            limit: Maximum posts to load

        Returns:
            List of posts
        """
        validate_post_load_range(start_post_no, end_post_no)

        url = f"/msg/post?chat_id={self.id}&range={start_post_no}x{end_post_no}"

        absolute = abs(end_post_no - start_post_no)
        if start_post_no < 0:
            absolute = 1
        if absolute >= limit:
            raise PararamioLimitExceededException(f"max post load limit is {limit - 1}")

        response = await self.client.api_get(url)
        posts_data = response.get("posts", [])

        if not posts_data:
            return []

        posts = []
        for post_data in posts_data:
            post = Post.from_dict(self.client, self, post_data)
            posts.append(post)

        return posts

    async def get_recent_posts(self, count: int = 50) -> list[Post]:
        """Get recent posts from chat.

        Args:
            count: Number of recent posts to get

        Returns:
            List of recent posts
        """
        return await self.load_posts(start_post_no=-count, end_post_no=-1)

    async def send_message(
        self,
        text: str,
        reply_to_post_no: int | None = None,
        quote: str | None = None,
    ) -> Post:
        """Send a message to this chat.

        Args:
            text: Message text
            reply_to_post_no: Optional post number to reply to
            quote: Optional quote text

        Returns:
            Created post
        """
        url = f"/msg/post/{self.id}"
        data: dict[str, Any] = {
            "uuid": str(uuid.uuid4().hex),
            "text": text,
        }

        if reply_to_post_no:
            data["reply_no"] = reply_to_post_no
        if quote:
            data["quote"] = quote

        response = await self.client.api_post(url, data)
        post_no = response["post_no"]

        # Create post object directly like sync version does

        post = Post(self.client, self, post_no)
        # Load the post data
        await post.load()
        return post

    async def upload_file(
        self,
        file_data: bytes,
        filename: str,
        content_type: str | None = None,
        reply_to_post_no: int | None = None,
    ) -> File:
        """Upload a file to this chat.

        Args:
            file_data: File content as bytes
            filename: File name
            content_type: Optional MIME type
            reply_to_post_no: Optional post number to attach to

        Returns:
            Uploaded file object
        """
        # This is a simplified implementation
        # In reality, you'd need to handle multipart/form-data upload
        raise NotImplementedError("File upload not implemented in this example")

    async def mark_read(self, post_no: int | None = None) -> bool:
        """Mark posts as read.

        Args:
            post_no: Optional specific post number, or None for all

        Returns:
            True if successful
        """
        url = f"/msg/lastread/{self.id}"
        data: dict[str, Any] = {"read_all": True} if post_no is None else {"post_no": post_no}

        response = await self.client.api_post(url, data)

        # Update local data
        if "post_no" in response:
            self._data["last_read_post_no"] = response["post_no"]
        if "posts_count" in response:
            self._data["posts_count"] = response["posts_count"]

        return True

    async def add_users(self, user_ids: list[int]) -> bool:
        """Add users to chat.

        Args:
            user_ids: List of user IDs to add

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/user/{join_ids(user_ids)}"
        response = await self.client.api_post(url)
        return "chat_id" in response

    async def remove_users(self, user_ids: list[int]) -> bool:
        """Remove users from chat.

        Args:
            user_ids: List of user IDs to remove

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/user/{join_ids(user_ids)}"
        response = await self.client.api_delete(url)
        return "chat_id" in response

    async def add_admins(self, user_ids: list[int]) -> bool:
        """Add admins to chat.

        Args:
            user_ids: List of user IDs to make admins

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/admin/{join_ids(user_ids)}"
        response = await self.client.api_post(url)
        return "chat_id" in response

    async def remove_admins(self, user_ids: list[int]) -> bool:
        """Remove admins from chat.

        Args:
            user_ids: List of user IDs to remove admin rights

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/admin/{join_ids(user_ids)}"
        response = await self.client.api_delete(url)
        return "chat_id" in response

    async def update_settings(self, **kwargs) -> bool:
        """Update chat settings.

        Args:
            **kwargs: Settings to update (title, description, etc.)

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}"
        response = await self.client.api_put(url, kwargs)
        return "chat_id" in response

    async def delete(self) -> bool:
        """Delete this chat.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}"
        response = await self.client.api_delete(url)
        return "chat_id" in response

    async def favorite(self) -> bool:
        """Add chat to favorites.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/favorite"
        response = await self.client.api_post(url)
        return "chat_id" in response

    async def unfavorite(self) -> bool:
        """Remove chat from favorites.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/unfavorite"
        response = await self.client.api_post(url)
        return "chat_id" in response

    def __eq__(self, other) -> bool:
        """Check equality with another chat."""
        if not isinstance(other, Chat):
            return False
        return self.id == other.id

    def __str__(self) -> str:
        """String representation."""
        return f"{self.id} - {self.title or 'Untitled'}"

    async def enter(self) -> bool:
        """Enter/join the chat.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/enter"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def quit(self) -> bool:
        """Quit/leave the chat.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/quit"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def hide(self) -> bool:
        """Hide chat from list.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/hide"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def show(self) -> bool:
        """Show hidden chat.

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/show"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def add_groups(self, group_ids: list[int]) -> bool:
        """Add groups to chat.

        Args:
            group_ids: List of group IDs to add

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/group/{join_ids(group_ids)}"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def delete_groups(self, group_ids: list[int]) -> bool:
        """Remove groups from chat.

        Args:
            group_ids: List of group IDs to remove

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/group/{join_ids(group_ids)}"
        response = await self.client.api_delete(url)
        return response.get("result") == "OK"

    async def transfer(self, org_id: int) -> bool:
        """Transfer chat ownership to organization.

        Args:
            org_id: Organization ID

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/transfer/{org_id}"
        response = await self.client.api_post(url)
        return response.get("result") == "OK"

    async def set_custom_title(self, title: str) -> bool:
        """Set custom chat title.

        Args:
            title: New title

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}/custom_title"
        response = await self.client.api_post(url, {"title": title})
        return response.get("result") == "OK"

    async def edit(self, **kwargs) -> bool:
        """Edit chat properties.

        Args:
            **kwargs: Chat properties to update

        Returns:
            True if successful
        """
        url = f"/core/chat/{self.id}"
        response = await self.client.api_put(url, kwargs)
        return response.get("result") == "OK"

    async def read_status(self) -> dict[str, Any]:
        """Get read status info.

        Returns:
            Read status data
        """
        url = f"/core/chat/{self.id}/read_status"
        return await self.client.api_get(url)

    async def sync_chats(self) -> dict[str, Any]:
        """Sync chat data.

        Returns:
            Sync data
        """
        url = "/core/chat/sync"
        return await self.client.api_get(url)

    async def post_search(self, query: str, limit: int = 50) -> list[Post]:
        """Search posts within chat.

        Note: This endpoint is not in the official documentation but works in practice.

        Args:
            query: Search query
            limit: Maximum results (API requires minimum 10)

        Returns:
            List of matching posts
        """

        # API requires limit to be at least 10
        api_limit = max(limit, 10) if limit else None

        url = f"/posts/search?q={quote_plus(query)}&chat_ids={self.id}"
        if api_limit:
            url += f"&limit={api_limit}"

        response = await self.client.api_get(url)

        posts = []
        posts_data = response.get("posts", [])

        # Apply client-side limit if requested limit is less than API minimum (10)
        if limit and limit < 10 and limit < len(posts_data):
            posts_data = posts_data[:limit]
        elif limit and limit < len(posts_data):
            posts_data = posts_data[:limit]

        for post_data in posts_data:
            post_no = post_data.get("post_no")
            if post_no:
                post = Post(self.client, self, post_no)
                posts.append(post)

        return posts

    async def lazy_posts_load(self, start: int = 0, end: int | None = None) -> list[Post]:
        """Load posts lazily (async version of lazy loading).

        Args:
            start: Start index
            end: End index

        Returns:
            List of posts
        """
        # Convert to load_posts parameters
        if end is None:
            end = start + 50  # Default limit
        return await self.load_posts(start_post_no=start, end_post_no=end)

    @classmethod
    async def create_private_chat(cls, client: AsyncPararamio, user_id: int) -> Chat:
        """Create private chat with user.

        Args:
            client: Pararamio client
            user_id: User ID

        Returns:
            Created chat
        """
        url = f"/core/chat/pm/{user_id}"
        response = await client.api_post(url)
        chat_id = response["chat_id"]

        chat = await client.get_chat_by_id(chat_id)
        if chat is None:
            raise ValueError(f"Failed to create or get chat {chat_id}")
        return chat

    @classmethod
    async def search_posts(
        cls,
        client: AsyncPararamio,
        q: str,
        *,
        order_type: str = "time",
        page: int = 1,
        chat_ids: list[int] | None = None,
        limit: int | None = POSTS_LIMIT,
    ) -> tuple[int, list[Post]]:
        """Search for posts across chats.

        Uses chat_ids parameter for chat filtering.
        Note: This endpoint is not in the official documentation but works in practice.

        Args:
            client: AsyncPararamio client
            q: Search query
            order_type: Sort order type (default: 'time')
            page: Page number (default: 1)
            chat_ids: Optional list of chat IDs to search within
            limit: Maximum results (API requires minimum 10)

        Returns:
            Tuple of (total_count, list_of_posts)
        """
        url = cls._build_search_url(q, order_type, page, chat_ids, limit)
        response = await client.api_get(url)

        if "posts" not in response:
            raise PararamioRequestException("failed to perform search")

        posts_data = response["posts"]
        # Apply client-side limit if requested limit is less than API minimum (10)
        if limit and limit < 10 and limit < len(posts_data):
            posts_data = posts_data[:limit]

        posts = cls._create_posts_from_data(client, posts_data)
        return response.get("count", len(posts)), posts

    @classmethod
    def _build_search_url(
        cls,
        q: str,
        order_type: str,
        page: int,
        chat_ids: list[int] | None,
        limit: int | None,
    ) -> str:
        """Build search URL with parameters."""
        url = f"/posts/search?q={quote_plus(q)}"
        if order_type:
            url += f"&order_type={order_type}"
        if page:
            url += f"&page={page}"

        # API requires limit to be at least 10
        api_limit = max(limit or POSTS_LIMIT, 10) if limit else None
        if api_limit:
            url += f"&limit={api_limit}"

        # Handle chat_ids parameter if provided
        if chat_ids is not None:
            url += f"&chat_ids={','.join(map(str, chat_ids))}"

        return url

    @classmethod
    def _create_posts_from_data(
        cls, client: AsyncPararamio, posts_data: list[dict[str, Any]]
    ) -> list[Post]:
        """Create post objects from search results data."""

        created_chats = {}
        posts = []

        for post_data in posts_data:
            chat_id = post_data.get("thread_id")
            post_no = post_data.get("post_no")

            if chat_id and post_no:
                # Create chat object if not already created
                if chat_id not in created_chats:
                    created_chats[chat_id] = cls(client, id=chat_id)

                post = Post(client, created_chats[chat_id], post_no)
                posts.append(post)

        return posts

    async def create_post(self, text: str, **kwargs) -> Post:
        """Create post in chat (alias for send_message).

        Args:
            text: Post text
            **kwargs: Additional parameters

        Returns:
            Created post
        """
        return await self.send_message(text, **kwargs)

    async def post(self, text: str, **kwargs) -> Post:
        """Create post in chat (backward compatibility alias for send_message).

        Args:
            text: Post text
            **kwargs: Additional parameters

        Returns:
            Created post
        """
        return await self.send_message(text, **kwargs)
