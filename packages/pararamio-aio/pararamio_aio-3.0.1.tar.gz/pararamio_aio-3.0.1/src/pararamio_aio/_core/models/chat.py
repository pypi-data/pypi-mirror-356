"""Core Chat model without lazy loading."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pararamio_aio._core.utils.helpers import parse_iso_datetime

from .base import CoreBaseModel, CoreClientObject

if TYPE_CHECKING:
    from datetime import datetime

    from pararamio_aio._core._types import FormatterT

__all__ = ('CoreChat',)


# Attribute formatters for Chat
CHAT_ATTR_FORMATTERS: FormatterT = {
    'time_edited': parse_iso_datetime,
    'time_updated': parse_iso_datetime,
    'time_created': parse_iso_datetime,
    'user_time_edited': parse_iso_datetime,
}


class CoreChat(CoreBaseModel, CoreClientObject):
    """Core Chat model with common functionality."""

    # Chat attributes (copied from original)
    id: int
    title: str
    history_mode: str
    description: str | None
    posts_count: int
    pm: bool
    e2e: bool
    time_created: datetime
    time_updated: datetime
    time_edited: datetime | None
    author_id: int
    two_step_required: bool
    org_visible: bool
    organization_id: int | None
    posts_live_time: int | None
    allow_api: bool
    read_only: bool
    tnew: bool
    adm_flag: bool
    custom_title: str | None
    is_favorite: bool
    inviter_id: int | None
    tshow: bool
    user_time_edited: datetime
    history_start: int
    pinned: list[int]
    thread_groups: list[int]
    thread_users: list[int]
    thread_admins: list[int]
    thread_users_all: list[int]
    last_msg_author_id: int | None
    last_msg_author: str
    last_msg_bot_name: str
    last_msg_text: str
    last_msg: str
    last_read_post_no: int
    thread_guests: list[int]

    def __init__(self, client: Any, chat_id: int | None = None, **kwargs: Any) -> None:
        # ID processing (as in original)
        if chat_id is None:
            chat_id = kwargs.get('chat_id')
            if chat_id is None:
                chat_id = kwargs['thread_id']

        self.id = int(chat_id)
        self._attr_formatters = CHAT_ATTR_FORMATTERS

        # Call parent constructors
        CoreBaseModel.__init__(self, id=self.id, **kwargs)
        CoreClientObject.__init__(self, client)

    def __str__(self) -> str:
        title = self._data.get('title', '')
        id_ = self.id or ''
        return f'{id_} - {title}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CoreChat):
            return id(other) == id(self)
        return self.id == other.id
