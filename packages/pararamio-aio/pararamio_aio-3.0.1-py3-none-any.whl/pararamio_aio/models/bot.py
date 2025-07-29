"""Async Bot model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

# Imports from core
from pararamio_aio._core.utils.helpers import join_ids, unescape_dict

from ..utils import async_bot_request

__all__ = ("AsyncPararamioBot",)


class AsyncPararamioBot:
    """Async bot client for Pararamio API."""

    def __init__(self, key: str):
        """Initialize bot with API key.

        Args:
            key: Bot API key
        """
        if len(key) > 50:
            key = key[20:]
        self.key = key

    async def request(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        """Send an authenticated HTTP request.

        Args:
            url: API endpoint
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request payload for POST/PUT
            headers: Additional headers

        Returns:
            Response data as dictionary
        """
        return await async_bot_request(url, self.key, method=method, data=data, headers=headers)

    async def get_profile(self) -> dict[str, Any]:
        """Get bot profile information.

        Returns:
            Bot profile data with unescaped name fields
        """
        url = "/user/me"
        response = await self.request(url)
        return unescape_dict(response, keys=["name"])

    async def post_message(
        self, chat_id: int, text: str, reply_no: int | None = None
    ) -> dict[str, str | int]:
        """Send a message to a chat.

        Args:
            chat_id: Target chat ID
            text: Message text
            reply_no: Optional message number to reply to

        Returns:
            Response data with post information
        """
        url = "/bot/message"
        return await self.request(
            url,
            method="POST",
            data={"chat_id": chat_id, "text": text, "reply_no": reply_no},
        )

    async def post_private_message_by_user_id(
        self,
        user_id: int,
        text: str,
    ) -> dict[str, str | int]:
        """Send a private message to a user by ID.

        Args:
            user_id: Target user ID
            text: Message text

        Returns:
            Response data with message information
        """
        url = "/msg/post/private"
        return await self.request(url, method="POST", data={"text": text, "user_id": user_id})

    async def post_private_message_by_user_email(
        self, email: str, text: str
    ) -> dict[str, str | int]:
        """Send a private message to a user by email.

        Args:
            email: Target user email
            text: Message text

        Returns:
            Response data with message information
        """
        url = "/msg/post/private"
        return await self.request(url, method="POST", data={"text": text, "user_email": email})

    async def post_private_message_by_user_unique_name(
        self, unique_name: str, text: str
    ) -> dict[str, str | int]:
        """Send a private message to a user by unique name.

        Args:
            unique_name: Target user unique name
            text: Message text

        Returns:
            Response data with message information
        """
        url = "/msg/post/private"
        return await self.request(
            url, method="POST", data={"text": text, "user_unique_name": unique_name}
        )

    async def get_tasks(self) -> dict[str, Any]:
        """Get bot tasks.

        Returns:
            Tasks data
        """
        url = "/msg/task"
        return await self.request(url)

    async def set_task_status(self, chat_id: int, post_no: int, state: str) -> dict:
        """Set task status.

        Args:
            chat_id: Chat ID where task is located
            post_no: Post number of the task
            state: New state ('open', 'done', or 'close')

        Returns:
            Response data

        Raises:
            ValueError: If state is invalid
        """
        if str.lower(state) not in ("open", "done", "close"):
            raise ValueError(f"unknown state {state}")

        url = f"/msg/task/{chat_id}/{post_no}"
        data = {"state": state}
        return await self.request(url, method="POST", data=data)

    async def get_chat(self, chat_id: int) -> dict[str, Any]:
        """Get chat by ID.

        Args:
            chat_id: Chat ID

        Returns:
            Chat data

        Raises:
            ValueError: If chat not found
        """
        url = f"/core/chat?ids={chat_id}"
        response = await self.request(url)
        chats = response.get("chats", [])

        if not chats:
            raise ValueError(f"chat with id {chat_id} is not found")

        return chats[0]

    async def get_chats(self) -> list[dict[str, Any]]:
        """Get all bot chats.

        Returns:
            List of chat data dictionaries
        """
        url = "/core/chat/sync"
        response = await self.request(url)
        chat_ids = response.get("chats", [])

        if not chat_ids:
            return []

        # Load chats in batches
        all_chats = []
        batch_size = 50

        for i in range(0, len(chat_ids), batch_size):
            batch_ids = chat_ids[i : i + batch_size]
            url = f"/core/chat?ids={join_ids(batch_ids)}"
            batch_response = await self.request(url)
            all_chats.extend(batch_response.get("chats", []))

        return all_chats

    async def get_users(self, user_ids: list[int]) -> list[dict[str, Any]]:
        """Get users by IDs.

        Args:
            user_ids: List of user IDs

        Returns:
            List of user data with unescaped names
        """
        if not user_ids:
            return []

        url = f"/core/user?ids={join_ids(user_ids)}"
        response = await self.request(url)
        return [unescape_dict(u, keys=["name"]) for u in response.get("users", [])]

    async def get_user_by_id(self, user_id: int) -> dict[str, Any]:
        """Get a single user by ID.

        Args:
            user_id: User ID

        Returns:
            User data

        Raises:
            ValueError: If user not found
        """
        users = await self.get_users([user_id])
        if not users:
            raise ValueError(f"user with id {user_id} is not found")
        return users[0]

    async def get_user_activity(
        self,
        user_id: int,
        start: datetime,
        end: datetime,
        actions: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Get user activity within date range.

        Args:
            user_id: User ID
            start: Start datetime
            end: End datetime
            actions: Optional list of activity actions to filter

        Returns:
            List of activity data

        Note:
            This is a simplified version. The sync version uses Activity model
            which is not yet implemented in async.
        """
        # Simplified implementation - just fetch first page
        # In full implementation, would need to handle pagination and Activity model
        action_str = ",".join(actions) if actions else ""
        url = f"/activity?user_id={user_id}&action={action_str}&page=1"
        response = await self.request(url)

        activities = response.get("activities", [])

        # Filter by date range
        filtered = []
        for activity in activities:
            activity_time = activity.get("time_created")
            if activity_time and start <= activity_time <= end:
                filtered.append(activity)

        return filtered
