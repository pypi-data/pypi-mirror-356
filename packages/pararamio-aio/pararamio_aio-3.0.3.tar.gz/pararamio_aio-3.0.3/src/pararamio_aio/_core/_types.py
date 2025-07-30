from __future__ import annotations

from http.cookiejar import CookieJar
from typing import Any, Callable, TypedDict, TypeVar, Union

try:
    from typing import Literal, NotRequired
except ImportError:
    from typing_extensions import Literal, NotRequired


class ProfileTypeT(TypedDict):
    unique_name: str
    id: int
    info: str | None
    find_strict: bool
    name: str
    is_google: bool
    two_step_enabled: bool
    has_password: bool
    phoneconfirmed: bool
    email: str
    phonenumber: NotRequired[str | None]


# noinspection PyUnresolvedReferences
class TextParsedT(TypedDict):
    type: str
    value: str
    name: NotRequired[str]
    id: NotRequired[int]


# noinspection PyUnresolvedReferences
class PostMetaUserT(TypedDict):
    id: int
    name: str
    unique_name: str
    is_bot: NotRequired[bool]


class BotProfileT(TypedDict):
    id: int
    active: bool
    deleted: bool
    email: str | None
    find_strict: bool
    has_password: bool
    info: str | None
    info_parsed: list
    info_chat: int
    is_bot: bool
    is_google: bool
    name: str
    name_trans: str
    unique_name: str
    organizations: list
    phoneconfirmed: bool
    phonenumber: str | None
    time_created: str
    time_updated: str
    two_step_enabled: bool


class PostMetaFileT(TypedDict):
    name: str
    guid: str
    size: int
    mime_type: str
    origin: tuple[int, int]


class MetaReplyT(TypedDict):
    text: str
    user_id: int
    user_name: str
    in_thread_no: int


class PostMetaThreadT(TypedDict):
    title: str


class PostMetaT(TypedDict):
    user: PostMetaUserT
    thread: PostMetaThreadT
    file: PostMetaFileT
    reply: MetaReplyT
    attachments: list[str]


class PostMention(TypedDict):
    id: int
    name: str
    value: str


class BaseEvent(TypedDict):
    type: Literal[
        'GROUP_LEAVED',
        'GROUP_DELETED',
        'ORG_MEMBERS',
        'GROUP_CREATED',
        'GROUP_UPDATED',
        'ENTER_TO_THREAD',
        'CALL',
        'POST_PINNED',
        'NEW_THREAD',
        'EDIT_THREAD',
        'ENTER_TO_THREAD',
        'CHAT_TITLE',
    ]
    data: dict[str, Any]


FormatterT = dict[str, Callable[[dict[str, Any], str], Any]]
CookieJarT = TypeVar('CookieJarT', bound=CookieJar)
QuoteRangeT = dict[str, Union[str, int]]
HeaderLikeT = dict[str, str]
SecondStepFnT = Callable[[CookieJar, dict[str, str], str], tuple[bool, dict[str, str]]]
