"""Core User model without lazy loading."""

from __future__ import annotations

from typing import Any

from .base import CoreBaseModel, CoreClientObject

__all__ = ('CoreUser', 'UserInfoParsedItem')


# Types for User
class UserInfoParsedItem(dict[str, Any]):
    """Parsed user info item."""

    type: str
    value: str


class CoreUser(CoreBaseModel, CoreClientObject):
    """Core User model with common functionality."""

    # User attributes (copied from original)
    id: int
    name: str
    name_trans: str
    info: str
    unique_name: str
    deleted: bool
    active: bool
    time_updated: str
    time_created: str
    is_bot: bool
    alias: None | None
    timezone_offset_minutes: int
    owner_id: None | None
    organizations: list[int]
    info_parsed: list[UserInfoParsedItem]

    def __init__(self, client: Any, user_id: int, **kwargs: Any) -> None:
        self.id = user_id
        self._attr_formatters = {}  # User has no special formatters

        # Call parent constructors
        CoreBaseModel.__init__(self, id=user_id, **kwargs)
        CoreClientObject.__init__(self, client)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CoreUser):
            return id(other) == id(self)
        return self.id == other.id

    def __str__(self) -> str:
        return self._data.get('name', '')
