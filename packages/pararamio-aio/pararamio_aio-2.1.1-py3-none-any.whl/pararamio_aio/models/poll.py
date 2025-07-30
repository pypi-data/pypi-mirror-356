"""Async Poll model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio_aio._core import (
    PararamioRequestException,
    PararamioServerResponseException,
    PararamioValidationException,
)

from .base import BaseModel

if TYPE_CHECKING:
    from ..client import AsyncPararamio
    from .chat import Chat

__all__ = ("PollOption", "Poll")


class PollOption:
    """Represents a poll option object."""

    def __init__(self, id: int, text: str, count: int, vote_users: list[int]) -> None:
        """Initialize poll option.

        Args:
            id: Option ID
            text: Option text
            count: Vote count
            vote_users: List of user IDs who voted
        """
        self.id = id
        self.text = text
        self.count = count
        self.vote_users = vote_users

    @classmethod
    def from_response_data(cls, data: dict[str, Any]) -> PollOption:
        """Create PollOption from API response data.

        Args:
            data: Response data containing poll option information

        Returns:
            PollOption instance

        Raises:
            PararamioServerResponseException: If required fields are missing
        """
        required_fields = ["id", "text", "count", "vote_users"]
        for field in required_fields:
            if field not in data:
                raise PararamioServerResponseException(
                    f"invalid server vote option response, missing {field}",
                    data,
                )
        return cls(**data)

    def __str__(self) -> str:
        """String representation."""
        return f"{self.text} ({self.count} votes)"


class Poll(BaseModel):
    """Async Poll model with explicit loading."""

    def __init__(
        self,
        client: AsyncPararamio,
        vote_uid: str,
        **kwargs: Any,
    ) -> None:
        """Initialize async poll.

        Args:
            client: AsyncPararamio client
            vote_uid: Poll unique ID
            **kwargs: Additional poll data
        """
        super().__init__(client, vote_uid=vote_uid, **kwargs)
        self.vote_uid = vote_uid

    @property
    def chat_id(self) -> int:
        """Get chat ID where poll is posted."""
        value = self._data.get("chat_id", 0)
        return int(value) if not isinstance(value, list) else 0

    @property
    def anonymous(self) -> bool:
        """Check if poll is anonymous."""
        return bool(self._data.get("anonymous", False))

    @property
    def mode(self) -> str:
        """Get poll mode ('one' for single choice, 'more' for multiple)."""
        return str(self._data.get("mode", "one"))

    @property
    def options(self) -> list[PollOption]:
        """Get poll options."""
        raw_options = self._data.get("options", [])
        if raw_options and isinstance(raw_options[0], dict):
            return [PollOption.from_response_data(opt) for opt in raw_options]
        return raw_options if isinstance(raw_options, list) else []

    @property
    def question(self) -> str:
        """Get poll question."""
        return str(self._data.get("question", ""))

    @property
    def total_user(self) -> int:
        """Get total number of users who voted."""
        value = self._data.get("total_user", 0)
        return int(value) if not isinstance(value, list) else 0

    @property
    def total_answer(self) -> int:
        """Get total number of answers."""
        value = self._data.get("total_answer", 0)
        return int(value) if not isinstance(value, list) else 0

    @property
    def user_id(self) -> int:
        """Get poll creator user ID."""
        value = self._data.get("user_id", 0)
        return int(value) if not isinstance(value, list) else 0

    async def load(self) -> Poll:
        """Load full poll data from API.

        Returns:
            Self with updated data
        """
        response = await self.client.api_get(f"/msg/vote/{self.vote_uid}")
        return self._update(response)

    def _update(self, response: dict[str, Any]) -> Poll:
        """Update the Poll object with response data.

        Args:
            response: API response data

        Returns:
            Updated Poll object

        Raises:
            PararamioServerResponseException: If response is invalid
        """
        if "vote" not in response:
            raise PararamioServerResponseException(
                f"failed to load data for vote {self.vote_uid} in chat {self.chat_id}",
                response,
            )

        # Process response data
        vote_data = response["vote"]
        self._data = {
            k: v if k != "options" else [PollOption.from_response_data(opt) for opt in v]
            for k, v in vote_data.items()
        }
        return self

    @classmethod
    async def create(
        cls, chat: Chat, question: str, *, mode: str, anonymous: bool, options: list[str]
    ) -> Poll:
        """Create a new poll in the specified chat.

        Args:
            chat: The chat where the poll will be created
            question: The poll question
            mode: Options select mode ('one' for single, 'more' for multiple)
            anonymous: Whether the poll should be anonymous
            options: List of option texts

        Returns:
            Created Poll object

        Raises:
            PararamioRequestException: If poll creation fails
        """
        response = await chat.client.api_post(
            "/msg/vote",
            {
                "chat_id": chat.id,
                "question": question,
                "options": options,
                "mode": mode,
                "anonymous": anonymous,
            },
        )

        if not response:
            raise PararamioRequestException("Failed to create poll")

        poll = cls(chat.client, response["vote_uid"])
        await poll.load()
        return poll

    async def _vote(self, option_ids: list[int]) -> Poll:
        """Vote on the poll with selected option IDs.

        Args:
            option_ids: List of option IDs to vote for

        Returns:
            Updated Poll object

        Raises:
            PararamioValidationException: If option IDs are invalid
        """
        valid_ids = [opt.id for opt in self.options]
        if not all(opt_id in valid_ids for opt_id in option_ids):
            raise PararamioValidationException("incorrect option")

        response = await self.client.api_put(
            f"/msg/vote/{self.vote_uid}",
            {"variants": option_ids},
        )
        return self._update(response)

    async def vote(self, option_id: int) -> Poll:
        """Vote for a single option.

        Args:
            option_id: The option ID to vote for

        Returns:
            Updated Poll object

        Raises:
            PararamioValidationException: If option_id is invalid
        """
        return await self._vote([option_id])

    async def vote_multi(self, option_ids: list[int]) -> Poll:
        """Vote for multiple options.

        Args:
            option_ids: List of option IDs to vote for

        Returns:
            Updated Poll object

        Raises:
            PararamioValidationException: If poll mode is not 'more' or option IDs are invalid
        """
        if self.mode != "more":
            raise PararamioValidationException(
                f"incorrect poll mode ({self.mode}) for multi voting"
            )
        return await self._vote(option_ids)

    async def retract(self) -> Poll:
        """Retract vote from the poll.

        Returns:
            Updated Poll object
        """
        return await self._vote([])

    def __str__(self) -> str:
        """String representation."""
        return self.question

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Poll):
            return False
        return self.vote_uid == other.vote_uid
