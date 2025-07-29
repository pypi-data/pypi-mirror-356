"""Async Post model."""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast
from uuid import uuid4

# Imports from core
from pararamio_aio._core import PararamioRequestException, PararamModelNotLoaded
from pararamio_aio._core.utils.helpers import encode_digit

from .base import BaseModel
from .file import File

if TYPE_CHECKING:
    from ..client import AsyncPararamio
    from .chat import Chat
    from .user import User

__all__ = ("Post", "get_post_mention")


def get_post_mention(data: dict[str, Any]) -> dict[str, Any] | None:
    """Extract mention data from parsed text item.

    Args:
        data: Parsed text item data

    Returns:
        PostMention dict or None if not a mention
    """
    id_val = data.get("id")
    name = data.get("name")
    value = data.get("value")

    if id_val is None and name is None and value is None:
        return None

    return cast(dict[str, Any], {"id": id_val, "name": name, "value": value})


class Post(BaseModel):  # pylint: disable=too-many-public-methods
    """Async Post model with explicit loading."""

    def __init__(self, client: AsyncPararamio, chat: Chat, post_no: int, **kwargs):
        """Initialize async post.

        Args:
            client: AsyncPararamio client
            chat: Parent chat object
            post_no: Post number
            **kwargs: Additional post data
        """
        super().__init__(client, post_no=post_no, **kwargs)
        self._chat = chat
        self.post_no = post_no

    @property
    def chat(self) -> Chat:
        """Get parent chat."""
        return self._chat

    @property
    def chat_id(self) -> int:
        """Get chat ID."""
        return self._chat.id

    def is_loaded(self) -> bool:
        """Check if post data has been loaded.

        Returns:
            True if post data has been loaded, False otherwise
        """
        # Check for essential fields that are only present after loading
        return "text" in self._data and "user_id" in self._data and "time_created" in self._data

    @property
    def text(self) -> str:
        """Get post text."""
        if not self.is_loaded() and "text" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("text", "")

    @property
    def user_id(self) -> int | None:
        """Get post author user ID."""
        if not self.is_loaded() and "user_id" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("user_id")

    @property
    def time_created(self) -> datetime | None:
        """Get post creation time."""
        if not self.is_loaded() and "time_created" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("time_created")

    @property
    def time_edited(self) -> datetime | None:
        """Get post edit time."""
        if not self.is_loaded() and "time_edited" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("time_edited")

    @property
    def reply_no(self) -> int | None:
        """Get reply post number if this is a reply."""
        if not self.is_loaded() and "reply_no" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("reply_no")

    @property
    def is_reply(self) -> bool:
        """Check if this post is a reply."""
        return self.reply_no is not None

    @property
    def is_deleted(self) -> bool:
        """Check if post is deleted."""
        if not self.is_loaded() and "is_deleted" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("is_deleted", False)

    @property
    def meta(self) -> dict[str, Any]:
        """Get post metadata."""
        if not self.is_loaded() and "meta" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("meta", {})

    @property
    def event(self) -> dict[str, Any] | None:
        """Get post event data."""
        if not self.is_loaded() and "event" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("event")

    @property
    def is_event(self) -> bool:
        """Check if this is an event post."""
        return bool(self.event)

    @property
    def uuid(self) -> str | None:
        """Get post UUID."""
        if not self.is_loaded() and "uuid" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("uuid")

    @property
    def text_parsed(self) -> list[dict[str, Any]]:
        """Get parsed text data."""
        if not self.is_loaded() and "text_parsed" not in self._data:
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("text_parsed", [])

    @property
    def mentions(self) -> list[dict[str, Any]]:
        """Get post mentions."""
        mentions = []
        for item in self.text_parsed:
            if item.get("type") == "mention":
                mentions.append(
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "value": item.get("value"),
                    }
                )
        return mentions

    @property
    def user_links(self) -> list[dict[str, Any]]:
        """Get user links in post."""
        links = []
        for item in self.text_parsed:
            if item.get("type") == "user_link":
                links.append(
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "value": item.get("value"),
                    }
                )
        return links

    async def get_author(self) -> User | None:
        """Get post author.

        Returns:
            User object or None if not found
        """
        if not self.user_id:
            return None

        return await self.client.get_user_by_id(self.user_id)

    async def load(self) -> Post:
        """Load full post data from API.

        Returns:
            Self with updated data
        """
        url = f"/msg/post?ids={encode_digit(self.chat_id)}-{encode_digit(self.post_no)}"
        response = await self.client.api_get(url)
        posts_data = response.get("posts", [])

        if len(posts_data) != 1:
            raise PararamioRequestException(
                f"Failed to load data for post_no {self.post_no} in chat {self.chat_id}"
            )

        # Update our data with loaded data
        self._data.update(posts_data[0])
        return self

    async def get_replies(self) -> list[int]:
        """Get list of reply post numbers.

        Returns:
            List of post numbers that reply to this post
        """
        url = f"/msg/post/{self.chat_id}/{self.post_no}/replies"
        response = await self.client.api_get(url)
        return response.get("data", [])

    async def load_reply_posts(self) -> list[Post]:
        """Load all posts that reply to this post.

        Returns:
            List of reply posts
        """
        reply_numbers = await self.get_replies()

        posts = []
        for post_no in reply_numbers:
            post = await self.client.get_post(self.chat_id, post_no)
            if post:
                posts.append(post)

        return posts

    async def get_reply_to_post(self) -> Post | None:
        """Get the post this post replies to.

        Returns:
            Parent post or None if not a reply
        """
        if not self.is_reply or self.reply_no is None:
            return None

        return await self.client.get_post(self.chat_id, self.reply_no)

    async def reply(self, text: str, quote: str | None = None) -> Post:
        """Reply to this post.

        Args:
            text: Reply text
            quote: Optional quote text

        Returns:
            Created reply post
        """
        url = f"/msg/post/{self.chat_id}"
        data = {
            "uuid": str(uuid4().hex),
            "text": text,
            "reply_no": self.post_no,
        }

        if quote:
            data["quote"] = quote

        response = await self.client.api_post(url, data)
        post_no = response["post_no"]

        post = await self.client.get_post(self.chat_id, post_no)
        if post is None:
            raise ValueError(f"Failed to retrieve reply post {post_no} from chat {self.chat_id}")
        return post

    async def edit(self, text: str, quote: str | None = None, reply_no: int | None = None) -> bool:
        """Edit this post.

        Args:
            text: New post text
            quote: Optional new quote
            reply_no: Optional new reply number

        Returns:
            True if successful
        """
        url = f"/msg/post/{self.chat_id}/{self.post_no}"
        data: dict[str, Any] = {
            "uuid": self.uuid or str(uuid4().hex),
            "text": text,
        }

        if quote is not None:
            data["quote"] = quote
        if reply_no is not None:
            data["reply_no"] = reply_no

        response = await self.client.api_put(url, data)

        if response.get("ver"):
            # Reload the post data
            await self.load()
            return True

        return False

    async def delete(self) -> bool:
        """Delete this post.

        Returns:
            True if successful
        """
        url = f"/msg/post/{self.chat_id}/{self.post_no}"
        response = await self.client.api_delete(url)

        if response.get("ver"):
            # Update local data to reflect deletion
            self._data["is_deleted"] = True
            return True

        return False

    async def who_read(self) -> list[int]:
        """Get list of user IDs who read this post.

        Returns:
            List of user IDs
        """
        url = f"/activity/who-read?thread_id={self.chat_id}&post_no={self.post_no}"
        response = await self.client.api_get(url)
        return response.get("users", [])

    async def mark_read(self) -> bool:
        """Mark this post as read.

        Returns:
            True if successful
        """
        return await self.chat.mark_read(self.post_no)

    async def get_file(self) -> File | None:
        """Get attached file if any.

        Returns:
            File object or None if no file
        """
        file_data = self.meta.get("file")
        if not file_data:
            return None

        return File.from_dict(self.client, file_data)

    async def load_attachments(self) -> list[File]:
        """Load all file attachments for this post.

        Returns:
            List of attached files
        """
        attachment_uuids = self.meta.get("attachments", [])
        if not attachment_uuids:
            return []

        # This is a simplified implementation
        # In reality, you'd need to search through nearby posts to find the files
        files = []
        main_file = await self.get_file()
        if main_file:
            files.append(main_file)

        return files

    @classmethod
    def from_dict(  # type: ignore[override]  # pylint: disable=arguments-renamed
        cls,
        client: AsyncPararamio,
        chat_or_data: Chat | dict[str, Any],
        data: dict[str, Any] | None = None,
    ) -> Post:
        """Create post from dict data.

        Args:
            client: AsyncPararamio client
            chat_or_data: Parent chat object or data dict (for base class compatibility)
            data: Raw post data (when chat is provided)

        Returns:
            Post instance
        """
        if isinstance(chat_or_data, dict):
            # Called with base signature: from_dict(client, data)
            raise NotImplementedError("Post.from_dict requires a Chat object")

        chat = chat_or_data
        if data is None:
            raise ValueError("data parameter is required when chat is provided")

        post_no = data.pop("post_no", None) or data.pop("in_thread_no", None)
        return cls(client, chat, post_no, **data)

    def __eq__(self, other) -> bool:
        """Check equality with another post."""
        if not isinstance(other, Post):
            return False
        return self.chat_id == other.chat_id and self.post_no == other.post_no

    @property
    def is_bot(self) -> bool:
        """Check if post is from a bot.

        Returns:
            True if post is from bot
        """
        if not self.is_loaded():
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return self._data.get("meta", {}).get("user", {}).get("is_bot", False)

    @property
    def is_file(self) -> bool:
        """Check if post contains file attachment.

        Returns:
            True if post has file
        """
        if not self.is_loaded():
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        return "file" in self._data.get("meta", {})

    @property
    def is_mention(self) -> bool:
        """Check if post contains mentions.

        Returns:
            True if post has mentions
        """
        if not self.is_loaded():
            raise PararamModelNotLoaded(
                "Post data has not been loaded. Use load() to fetch post data first."
            )
        text_parsed = self._data.get("text_parsed", [])
        if not text_parsed:
            return False

        for item in text_parsed:
            if isinstance(item, dict) and item.get("type") == "mention":
                return True
        return False

    async def next(self) -> Post | None:
        """Get next post in thread.

        Returns:
            Next post or None
        """
        try:
            # Get posts after this one
            posts = await self.chat.load_posts(
                start_post_no=self.post_no + 1, end_post_no=self.post_no + 2, limit=1
            )
            return posts[0] if posts else None
        except (IndexError, KeyError, AttributeError):
            return None

    async def prev(self) -> Post | None:
        """Get previous post in thread.

        Returns:
            Previous post or None
        """
        try:
            # Get posts before this one
            if self.post_no <= 1:
                return None
            posts = await self.chat.load_posts(
                start_post_no=self.post_no - 1, end_post_no=self.post_no, limit=1
            )
            return posts[0] if posts else None
        except (IndexError, KeyError, AttributeError):
            return None

    def attachments(self) -> list[dict[str, Any]]:
        """Get post attachments.

        Returns:
            List of attachment data
        """
        return self._data.get("attachments", [])

    def file(self) -> dict[str, Any] | None:
        """Get file attachment data.

        Returns:
            File data or None
        """
        return self._data.get("meta", {}).get("file")

    def in_thread_no(self) -> int | None:
        """Get thread number if post is in a thread.

        Returns:
            Thread number or None
        """
        return self._data.get("in_thread_no")

    def __str__(self) -> str:
        """String representation."""
        return self.text

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"<Post(client={hex(id(self.client))}, chat_id={self.chat_id}, post_no={self.post_no})>"
        )

    async def rerere(self) -> list[Post]:
        """Get all replies in a thread recursively.

        Returns:
            List of all posts in the reply chain
        """
        url = f"/msg/post/{self.chat_id}/{self.post_no}/rerere"
        response = await self.client.api_get(url)

        posts = []
        for post_no in response.get("data", []):
            post = Post(self.client, self._chat, post_no)
            await post.load()
            posts.append(post)

        return posts

    async def get_tree(self, load_limit: int = 1000) -> OrderedDict[int, Post]:
        """Get post hierarchy as an ordered dictionary.

        Args:
            load_limit: Maximum number of posts to load between first and current

        Returns:
            OrderedDict mapping post numbers to Post objects
        """
        posts: dict[int, Post] = {self.post_no: self}

        # Get all replies recursively
        for post in await self.rerere():
            posts[post.post_no] = post

        # Find the first post in thread
        first = posts[min(posts.keys())]
        tree = OrderedDict(sorted(posts.items()))

        # Calculate load range
        load_start = first.post_no + 1
        if self.post_no - first.post_no > load_limit:
            load_start = self.post_no - load_limit

        # Load posts in range if needed
        if load_start < self.post_no - 1:
            loaded_posts = await self._chat.load_posts(
                start_post_no=load_start, end_post_no=self.post_no - 1
            )
            for post in loaded_posts:
                posts[post.post_no] = post

        # Build final tree with only connected posts
        for post in sorted(posts.values(), key=lambda p: p.post_no):
            if post.reply_no is None or post.reply_no not in tree:
                continue
            tree[post.post_no] = post

        return OrderedDict(sorted(tree.items()))

    @classmethod
    async def create(
        cls,
        chat: Chat,
        text: str,
        *,
        reply_no: int | None = None,
        quote: str | None = None,
        uuid: str | None = None,
        attachments: list[str] | None = None,
    ) -> Post:
        """Create a new post.

        Args:
            chat: Parent chat
            text: Post text
            reply_no: Optional post number to reply to
            quote: Optional quote text
            uuid: Optional UUID (generated if not provided)
            attachments: Optional list of attachment UUIDs

        Returns:
            Created Post object
        """
        url = f"/msg/post/{chat.id}"
        data: dict[str, Any] = {
            "uuid": uuid or str(uuid4().hex),
            "text": text,
            "quote": quote,
            "reply_no": reply_no,
        }
        if attachments:
            data["attachments"] = attachments

        response = await chat._client.api_post(url, data)
        if not response:
            raise PararamioRequestException("Failed to create post")

        post = cls(chat._client, chat, post_no=response["post_no"])
        await post.load()
        return post
