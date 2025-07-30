"""Async Activity model."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Coroutine

# Imports from core
from pararamio_aio._core.utils.helpers import parse_iso_datetime

__all__ = ("ActivityAction", "Activity")


class ActivityAction(Enum):
    """Activity action types."""

    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    READ = "thread-read"
    POST = "thread-post"
    CALL = "calling"
    CALL_END = "endcall"


class Activity:
    """User activity record."""

    def __init__(self, action: ActivityAction, time: datetime):
        """Initialize activity.

        Args:
            action: Activity action type
            time: Activity timestamp
        """
        self.action = action
        self.time = time

    @classmethod
    def from_api_data(cls, data: dict[str, str]) -> Activity:
        """Create Activity from API response data.

        Args:
            data: API response data

        Returns:
            Activity instance

        Raises:
            ValueError: If time format is invalid
        """
        time = parse_iso_datetime(data, "datetime")
        if time is None:
            raise ValueError("Invalid time format")

        return cls(
            action=ActivityAction(data["action"]),
            time=time,
        )

    @classmethod
    async def get_activity(
        cls,
        page_loader: Callable[..., Coroutine[Any, Any, dict[str, Any]]],
        start: datetime,
        end: datetime,
        actions: list[ActivityAction] | None = None,
    ) -> list[Activity]:
        """Get user activity within date range.

        Args:
            page_loader: Async function to load activity pages
            start: Start datetime
            end: End datetime
            actions: Optional list of actions to filter

        Returns:
            List of Activity objects sorted by time
        """
        results = []
        actions_to_check: list[ActivityAction | None] = [None]

        if actions:
            actions_to_check = actions  # type: ignore[assignment]

        for action in actions_to_check:
            page = 1
            is_last_page = False

            while not is_last_page:
                # Call async page loader
                response = await page_loader(action, page=page)
                data = response.get("data", [])

                if not data:
                    break

                for activity_data in data:
                    activity = cls.from_api_data(activity_data)

                    if activity.time > end:
                        continue

                    if activity.time < start:
                        is_last_page = True
                        break

                    results.append(activity)

                page += 1

        return sorted(results, key=lambda x: x.time)

    def __str__(self) -> str:
        """String representation."""
        return f"Activity({self.time}, {self.action.value})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<Activity(action={self.action}, time={self.time})>"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Activity):
            return False
        return self.action == other.action and self.time == other.time
