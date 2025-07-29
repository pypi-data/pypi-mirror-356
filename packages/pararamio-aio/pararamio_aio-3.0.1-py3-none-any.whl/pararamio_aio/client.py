"""Async client for Pararamio API."""

from __future__ import annotations

import datetime
import json
import logging
import os
from http.cookiejar import Cookie
from http.cookies import SimpleCookie
from io import BytesIO
from typing import (
    Any,
    BinaryIO,
    Dict,
    Sequence,
)
from urllib.parse import quote, quote_plus

import aiofiles
import aiohttp

# Import from core
from pararamio_aio._core import (
    XSRF_HEADER_NAME,
    AsyncCookieManager,
    AsyncInMemoryCookieManager,
    PararamioAuthenticationException,
    PararamioHTTPRequestException,
    PararamioValidationException,
)
from yarl import URL

from .file_operations import async_delete_file, async_download_file, async_xupload_file
from .models import Chat, File, Group, Post, User
from .utils import async_authenticate, async_do_second_step_with_code, get_async_xsrf_token

ProfileTypeT = Dict[str, Any]

__all__ = ("AsyncPararamio",)

log = logging.getLogger("pararamio_aio.client")


class AsyncPararamio:
    """Async Pararamio client class.

    This class provides an async client interface for interacting with the Pararamio API.
    Unlike the sync version, this client uses explicit loading instead of lazy loading.
    """

    def __init__(
        self,
        login: str | None = None,
        password: str | None = None,
        key: str | None = None,
        cookie_manager: AsyncCookieManager | None = None,
        session: aiohttp.ClientSession | None = None,
        wait_auth_limit: bool = False,
    ):
        """Initialize async Pararamio client.

        Args:
            login: Optional string for the login name
            password: Optional string for the password
            key: Optional string for an authentication key
            cookie_manager: Optional AsyncCookieManager instance for cookie persistence
            session: Optional aiohttp.ClientSession to use
            wait_auth_limit: Boolean flag to wait for rate limits instead of raising
                exception (default False)
        """
        self._login = login
        self._password = password
        self._key = key
        self._wait_auth_limit = wait_auth_limit
        self._authenticated = False
        self._session = session
        self._cookie_jar = aiohttp.CookieJar()
        self._cookie_manager = (
            cookie_manager if cookie_manager is not None else AsyncInMemoryCookieManager()
        )
        self._headers: dict[str, str] = {}
        self._profile: ProfileTypeT | None = None

    def _create_simple_cookie(self, cookie) -> tuple[SimpleCookie, URL]:
        """Create SimpleCookie from cookie object.

        Returns:
            Tuple of (SimpleCookie, URL for the cookie domain)
        """
        # Create proper URL for the cookie domain
        domain = cookie.domain
        # Remove leading dot for URL creation
        if domain.startswith("."):
            url_domain = domain[1:]
        else:
            url_domain = domain
        if not url_domain.startswith("http"):
            url_domain = f"https://{url_domain}"
        url = URL(url_domain).with_path(cookie.path)

        # Create SimpleCookie with all attributes preserved
        simple_cookie = SimpleCookie()
        # Remove quotes from cookie value if present
        cookie_value = cookie.value
        if cookie_value.startswith('"') and cookie_value.endswith('"'):
            cookie_value = cookie_value[1:-1]
        simple_cookie[cookie.name] = cookie_value

        # Set all cookie attributes
        if cookie.domain:
            simple_cookie[cookie.name]["domain"] = cookie.domain
        if cookie.path:
            simple_cookie[cookie.name]["path"] = cookie.path
        if cookie.secure:
            simple_cookie[cookie.name]["secure"] = True
        if cookie.expires is not None:
            # Convert expires timestamp to formatted string
            expires_dt = datetime.datetime.fromtimestamp(cookie.expires, tz=datetime.timezone.utc)
            simple_cookie[cookie.name]["expires"] = expires_dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return simple_cookie, url

    async def _load_cookies_to_session(self) -> None:
        """Load cookies from cookie manager to session."""
        cookies = self._cookie_manager.get_all_cookies()
        if not cookies:
            # Try to load if no cookies yet
            await self._cookie_manager.load_cookies()
            cookies = self._cookie_manager.get_all_cookies()

        if cookies:
            # Convert cookies to aiohttp format
            for cookie in cookies:
                # Skip cookies with empty or None value
                if not cookie.value:
                    continue

                simple_cookie, url = self._create_simple_cookie(cookie)

                # Update session cookies
                if self._session:
                    self._session.cookie_jar.update_cookies(simple_cookie, url)

    async def _ensure_session(self) -> None:
        """Ensure session is created."""
        if self._session is None:
            connector = aiohttp.TCPConnector(limit=30, limit_per_host=10)
            self._session = aiohttp.ClientSession(
                connector=connector,
                cookie_jar=self._cookie_jar,
                timeout=aiohttp.ClientTimeout(total=30),
            )

    async def _check_xsrf_token(self) -> None:
        """Check for XSRF token in cookies and set authentication status."""
        cookies = self._cookie_manager.get_all_cookies()
        for cookie in cookies:
            if cookie.name == "_xsrf":
                self._headers[XSRF_HEADER_NAME] = cookie.value
                self._authenticated = True
                break

    async def __aenter__(self):
        """Async context manager entry."""
        # Create session with cookie jar
        await self._ensure_session()

        # Load cookies from cookie manager to session
        await self._load_cookies_to_session()

        # Check for XSRF token in cookies
        await self._check_xsrf_token()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Save cookies if we have a cookie manager
        await self._save_cookies_to_manager()

        if self._session:
            await self._session.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get the aiohttp session."""
        if self._session is None:
            raise RuntimeError("Client session not initialized. Use async context manager.")
        return self._session

    async def _save_cookies_to_manager(self) -> None:
        """Save cookies from aiohttp cookie jar to cookie manager."""
        if self._cookie_manager and self._cookie_jar:
            # Convert aiohttp cookies to standard Cookie objects
            for aiohttp_cookie in self._cookie_jar:
                expires = aiohttp_cookie.get("expires")
                if expires == "":
                    expires = None
                elif expires is not None:
                    try:
                        expires = int(float(expires))
                    except (ValueError, TypeError):
                        expires = None

                # Remove quotes from cookie value before saving
                cookie_value = aiohttp_cookie.value
                if cookie_value.startswith('"') and cookie_value.endswith('"'):
                    cookie_value = cookie_value[1:-1]

                cookie = Cookie(
                    version=0,
                    name=aiohttp_cookie.key,
                    value=cookie_value,
                    port=None,
                    port_specified=False,
                    domain=aiohttp_cookie["domain"],
                    domain_specified=bool(aiohttp_cookie["domain"]),
                    domain_initial_dot=aiohttp_cookie["domain"].startswith("."),
                    path=aiohttp_cookie["path"],
                    path_specified=bool(aiohttp_cookie["path"]),
                    secure=aiohttp_cookie.get("secure", False),
                    expires=expires,
                    discard=False,
                    comment=None,
                    comment_url=None,
                    rest={},
                    rfc2109=False,
                )
                self._cookie_manager.add_cookie(cookie)
            await self._cookie_manager.save_cookies()

    async def authenticate(
        self,
        login: str | None = None,
        password: str | None = None,
        key: str | None = None,
    ) -> bool:
        """Authenticate with the Pararamio API.

        Args:
            login: Optional login override
            password: Optional password override
            key: Optional key override

        Returns:
            True if authentication successful
        """
        login = login or self._login or ""
        password = password or self._password or ""
        key = key or self._key or ""

        if not key:
            raise PararamioAuthenticationException("key must be set and not empty")

        self._authenticated, xsrf_token = await async_authenticate(
            self.session, login, password, key, self._wait_auth_limit
        )

        if self._authenticated:
            self._headers[XSRF_HEADER_NAME] = xsrf_token
            # Save cookies through cookie manager
            await self._save_cookies_to_manager()

        return self._authenticated

    async def authenticate_with_code(
        self,
        code: str,
        login: str | None = None,
        password: str | None = None,
    ) -> bool:
        """Authenticate with a TOTP code directly.

        Args:
            code: The 6-digit authentication code. Must be set and not empty.
            login: Optional login override
            password: Optional password override

        Returns:
            True if authentication successful

        Raises:
            PararamioAuthenticationException: If the code is not provided or is empty.
        """
        login = login or self._login or ""
        password = password or self._password or ""

        if not code:
            raise PararamioAuthenticationException("code must be set and not empty")

        self._authenticated, xsrf_token = await async_authenticate(
            self.session,
            login,
            password,
            key=None,
            wait_auth_limit=self._wait_auth_limit,
            second_step_fn=async_do_second_step_with_code,
            second_step_arg=code,
        )

        if self._authenticated:
            self._headers[XSRF_HEADER_NAME] = xsrf_token
            # Save cookies through cookie manager
            await self._save_cookies_to_manager()

        return self._authenticated

    async def _ensure_authenticated(self):
        """Ensure the client is authenticated."""
        if not self._authenticated:
            success = await self.authenticate()
            if not success:
                raise PararamioAuthenticationException("Failed to authenticate")

    async def _api_request_with_retry(self, method: str, url: str, **kwargs) -> dict[str, Any]:
        """Make API request with automatic retry on auth errors."""
        try:
            return await self._api_request(method, url, **kwargs)
        except PararamioHTTPRequestException as e:
            if e.code == 401:
                # Check if it's an XSRF token error by examining the response
                try:
                    if e.fp and hasattr(e.fp, "read"):
                        response_text = e.fp.read()
                        if isinstance(response_text, bytes):
                            response_text = response_text.decode("utf-8")
                    elif e.response:
                        response_text = e.response
                        if isinstance(response_text, bytes):
                            response_text = response_text.decode("utf-8")
                    else:
                        response_text = ""

                    # Check if it's an XSRF error
                    if response_text and "xsrf" in response_text.lower():
                        log.info(
                            "XSRF token is expired, invalid or was not set, trying to get new one"
                        )
                        self._headers[XSRF_HEADER_NAME] = ""
                        return await self._api_request(method, url, **kwargs)

                except (json.JSONDecodeError, ValueError) as parse_error:
                    log.debug("Failed to parse error response: %s", parse_error)

                # Regular authentication error - use cookie manager only if we have credentials
                if self._cookie_manager and self._key:

                    async def retry():
                        self._authenticated = False
                        await self.authenticate()
                        return await self._api_request(method, url, **kwargs)

                    return await self._cookie_manager.handle_auth_error(retry)
            raise

    async def _api_request(self, method: str, url: str, **kwargs) -> dict[str, Any]:
        """Make raw API request."""
        await self._ensure_authenticated()

        # Ensure XSRF token is present in headers
        if not self._headers.get(XSRF_HEADER_NAME):
            try:
                xsrf_token = await get_async_xsrf_token(self.session)
                self._headers[XSRF_HEADER_NAME] = xsrf_token
                # Save cookies after getting new XSRF token
                await self._save_cookies_to_manager()
            except (aiohttp.ClientError, ValueError) as e:
                log.warning("Failed to get XSRF token: %s", e)

        full_url = f"https://api.pararam.io{url}"
        async with self.session.request(
            method, full_url, headers=self._headers, **kwargs
        ) as response:
            if response.status != 200:
                # Read response body for error details
                try:
                    error_body = await response.text()
                except aiohttp.ClientError:
                    error_body = ""

                # Create a BytesIO object for the error body to match expected interface
                # BytesIO already imported at top of file
                error_fp = BytesIO(error_body.encode("utf-8") if error_body else b"")

                raise PararamioHTTPRequestException(
                    full_url,
                    response.status,
                    f"HTTP {response.status}",
                    list(response.headers.items()),
                    error_fp,
                )
            return await response.json()

    async def api_get(self, url: str) -> dict[str, Any]:
        """Make an authenticated GET request.

        Args:
            url: API endpoint URL

        Returns:
            JSON response as dict
        """
        return await self._api_request_with_retry("GET", url)

    async def api_post(self, url: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make an authenticated POST request.

        Args:
            url: API endpoint URL
            data: Optional data payload

        Returns:
            JSON response as dict
        """
        return await self._api_request_with_retry("POST", url, json=data)

    async def api_put(self, url: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make an authenticated PUT request.

        Args:
            url: API endpoint URL
            data: Optional data payload

        Returns:
            JSON response as dict
        """
        return await self._api_request_with_retry("PUT", url, json=data)

    async def api_delete(self, url: str) -> dict[str, Any]:
        """Make an authenticated DELETE request.

        Args:
            url: API endpoint URL

        Returns:
            JSON response as dict
        """
        return await self._api_request_with_retry("DELETE", url)

    async def get_profile(self) -> ProfileTypeT:
        """Get user profile.

        Returns:
            User profile data
        """
        if not self._profile:
            response = await self.api_get("/user/me")
            self._profile = response
        return self._profile

    def get_cookies(self) -> aiohttp.CookieJar | None:
        """Get current cookie jar.

        Note: Unlike sync version, this doesn't trigger authentication.
        Use authenticate() explicitly if needed.

        Returns:
            Current aiohttp CookieJar or None
        """
        return self._cookie_jar

    def get_headers(self) -> dict[str, str]:
        """Get current request headers.

        Note: Unlike sync version, this doesn't trigger authentication.
        Use authenticate() explicitly if needed.

        Returns:
            Copy of current headers dict
        """
        return self._headers.copy()

    async def search_users(self, query: str, include_self: bool = False) -> list[User]:
        """Search for users.

        Args:
            query: Search query string
            include_self: Whether to include current user in results. Default is False.

        Returns:
            List of found users
        """
        url = f"/user/search?flt={quote(query)}"
        if not include_self:
            url += "&self=false"
        response = await self.api_get(url)
        users = []
        for user_data in response.get("users", []):
            user = User.from_dict(self, user_data)
            users.append(user)
        return users

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None if not found
        """
        try:
            users = await self.get_users_by_ids([user_id])
            return users[0] if users else None
        except (aiohttp.ClientError, IndexError, KeyError):
            return None

    async def get_users_by_ids(self, ids: Sequence[int]) -> list[User]:
        """Get multiple users by IDs.

        Args:
            ids: Sequence of user IDs

        Returns:
            List of user objects
        """
        if not ids:
            return []
        if len(ids) > 100:
            raise PararamioValidationException("too many ids, max 100")

        url = "/user/list?ids=" + ",".join(map(str, ids))
        response = await self.api_get(url)
        users = []
        for user_data in response.get("users", []):
            user = User.from_dict(self, user_data)
            users.append(user)
        return users

    async def get_chat_by_id(self, chat_id: int) -> Chat | None:
        """Get chat by ID.

        Args:
            chat_id: Chat ID

        Returns:
            Chat object or None if not found
        """
        try:
            chats = await self.get_chats_by_ids([chat_id])
            return chats[0] if chats else None
        except (aiohttp.ClientError, IndexError, KeyError):
            return None

    async def get_chats_by_ids(self, ids: Sequence[int]) -> list[Chat]:
        """Get multiple chats by IDs.

        Args:
            ids: Sequence of chat IDs

        Returns:
            List of chat objects
        """
        if not ids:
            return []

        url = f"/core/chat?ids={','.join(map(str, ids))}"
        response = await self.api_get(url)
        chats = []
        for chat_data in response.get("chats", []):
            chat = Chat.from_dict(self, chat_data)
            chats.append(chat)
        return chats

    async def list_chats(self) -> list[Chat]:
        """List all user chats.

        Returns:
            List of chat objects
        """
        url = "/core/chat/sync"
        response = await self.api_get(url)
        chat_ids = response.get("chats", [])
        return await self.get_chats_by_ids(chat_ids)

    async def create_chat(
        self,
        title: str,
        description: str = "",
        users: list[int] | None = None,
        groups: list[int] | None = None,
        **kwargs,
    ) -> Chat:
        """Create a new chat.

        Args:
            title: Chat title
            description: Chat description
            users: List of user IDs to add
            groups: List of group IDs to add
            **kwargs: Additional chat parameters

        Returns:
            Created chat object
        """
        data = {
            "title": title,
            "description": description,
            "users": users or [],
            "groups": groups or [],
            **kwargs,
        }

        response = await self.api_post("/core/chat", data)
        chat_id = response["chat_id"]
        chat = await self.get_chat_by_id(chat_id)
        if not chat:
            raise PararamioValidationException(f"Failed to create chat with ID {chat_id}")
        return chat

    async def search_groups(self, query: str) -> list[Group]:
        """Search for groups.

        Note: This uses the user search endpoint which also returns groups.

        Args:
            query: Search query string

        Returns:
            List of found groups
        """
        return await Group.search(self, query)

    async def get_group_by_id(self, group_id: int) -> Group | None:
        """Get group by ID.

        Args:
            group_id: Group ID

        Returns:
            Group object or None if not found
        """
        try:
            groups = await self.get_groups_by_ids([group_id])
            return groups[0] if groups else None
        except (aiohttp.ClientError, IndexError, KeyError):
            return None

    async def get_groups_by_ids(self, ids: Sequence[int]) -> list[Group]:
        """Get multiple groups by IDs.

        Args:
            ids: Sequence of group IDs

        Returns:
            List of group objects
        """
        if not ids:
            return []
        if len(ids) > 100:
            raise PararamioValidationException("too many ids, max 100")

        url = "/core/group?ids=" + ",".join(map(str, ids))
        response = await self.api_get(url)
        groups = []
        for group_data in response.get("groups", []):
            group = Group.from_dict(self, group_data)
            groups.append(group)
        return groups

    async def search_posts(
        self,
        query: str,
        order_type: str = "time",
        page: int = 1,
        chat_ids: list[int] | None = None,
        limit: int | None = None,
    ) -> tuple[int, list[Post]]:
        """Search for posts.

        Note: This endpoint is not in the official documentation but works in practice.

        Args:
            query: Search query
            order_type: Order type ('time', 'relevance')
            page: Page number
            chat_ids: Optional list of chat IDs to search within
            limit: Optional result limit

        Returns:
            Tuple of (total_count, posts_list)
        """
        url = self._build_search_url(query, order_type, page, chat_ids, limit)
        response = await self.api_get(url)
        total_count = response.get("count", 0)

        posts_data = response.get("posts", [])
        # Apply client-side limit if requested limit is less than API minimum (10)
        if limit and limit < 10 and limit < len(posts_data):
            posts_data = posts_data[:limit]

        posts = await self._load_posts_from_data(posts_data)
        return total_count, posts

    def _build_search_url(
        self,
        query: str,
        order_type: str,
        page: int,
        chat_ids: list[int] | None,
        limit: int | None,
    ) -> str:
        """Build search URL with parameters."""
        url = f"/posts/search?q={quote_plus(query)}"
        if order_type:
            url += f"&order_type={order_type}"
        if page:
            url += f"&page={page}"

        # API requires limit to be at least 10
        api_limit = max(limit or 100, 10) if limit else None
        if api_limit:
            url += f"&limit={api_limit}"

        # Handle chat_ids parameter if provided
        if chat_ids:
            url += f"&chat_ids={','.join(map(str, chat_ids))}"

        return url

    async def _load_posts_from_data(self, posts_data: list[dict[str, Any]]) -> list[Post]:
        """Load full post objects from search results data."""
        posts = []
        for post_data in posts_data:
            thread_id = post_data.get("thread_id")
            post_no = post_data.get("post_no")
            if thread_id and post_no:
                # Load the full post data
                post = await self.get_post(thread_id, post_no)
                if post:
                    posts.append(post)
        return posts

    async def get_post(self, chat_id: int, post_no: int) -> Post | None:
        """Get a specific post by chat ID and post number.

        Args:
            chat_id: Chat ID
            post_no: Post number

        Returns:
            Post object or None if not found
        """
        try:
            # Simple encoding for now - in real implementation would use core utils
            url = f"/msg/post?ids={chat_id}-{post_no}"
            response = await self.api_get(url)
            posts_data = response.get("posts", [])
            if posts_data:
                chat = await self.get_chat_by_id(chat_id)
                if chat:
                    return Post.from_dict(self, chat, posts_data[0])
            return None
        except (aiohttp.ClientError, IndexError, KeyError):
            return None

    async def _upload_file(
        self,
        file: BinaryIO | BytesIO,
        chat_id: int,
        *,
        filename: str | None = None,
        type_: str | None = None,
        organization_id: int | None = None,
        reply_no: int | None = None,
        quote_range: str | None = None,
    ) -> tuple[dict, dict]:
        """
        Internal method for uploading a file to a specified chat or organization.

        Args:
            file: A binary stream of the file to be uploaded.
            chat_id: The ID of the chat where the file will be uploaded.
            filename: An optional parameter that specifies the name of the file.
            type_: An optional parameter that specifies the type of file being uploaded.
                   If not provided, it will be inferred from the filename.
            organization_id: An optional parameter that specifies the ID of the organization
                             if the file is an organization avatar.
            reply_no: An optional parameter that specifies the reply number
                      associated with the file.
            quote_range: An optional parameter that specifies the range
                         of quotes associated with the file.

        Returns:
            A tuple containing a dictionary with the response from the xupload_file function
            and a dictionary of the fields used during the upload.

        Raises:
            PararamioValidationException: If filename is not set when type is None,
            or if organization_id is not set when type is organization_avatar,
            or if chat_id is not set when type is chat_avatar.
        """
        if type_ is None and not filename:
            raise PararamioValidationException("filename must be set when type is None")

        await self._ensure_authenticated()

        if type_ == "organization_avatar" and organization_id is None:
            raise PararamioValidationException(
                "organization_id must be set when type is organization_avatar"
            )
        if type_ == "chat_avatar" and chat_id is None:
            raise PararamioValidationException("chat_id must be set when type is chat_avatar")

        content_type = None
        if type_ not in ("organization_avatar", "chat_avatar"):
            content_type = type_

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0, 0)

        fields: list[tuple[str, str | int | None]] = [
            ("type", type_),
            ("filename", filename),
            ("size", file_size),
            ("chat_id", chat_id),
            ("organization_id", organization_id),
            ("reply_no", reply_no),
            ("quote_range", quote_range),
        ]

        result = await async_xupload_file(
            self.session,
            fp=file,
            fields=fields,
            filename=filename,
            content_type=content_type,
            headers=self._headers,
        )

        return result, dict(fields)

    async def upload_file(
        self,
        file: str | BytesIO | BinaryIO | os.PathLike,
        chat_id: int,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        reply_no: int | None = None,
        quote_range: str | None = None,
    ) -> File:
        """
        Upload a file to a specified chat.

        Args:
            file: The file to be uploaded. It can be a file path,
                  a BytesIO object, or an os.PathLike object.
            chat_id: The ID of the chat where the file should be uploaded.
            filename: The name of the file.
                      If not specified and the file is a path, the basename of the file
                      path will be used.
            content_type: The MIME type of the file.
            reply_no: The reply number in the chat to which this file is in response.
            quote_range: The range of messages being quoted.

        Returns:
            File: An instance of the File class representing the uploaded file.
        """
        if isinstance(file, (str, os.PathLike)):
            filename = filename or os.path.basename(str(file))
            async with aiofiles.open(file, "rb") as f:
                content = await f.read()
                bio = BytesIO(content)
                res, extra = await self._upload_file(
                    bio,
                    chat_id,
                    filename=filename,
                    type_=content_type,
                    reply_no=reply_no,
                    quote_range=quote_range,
                )
        else:
            res, extra = await self._upload_file(
                file,
                chat_id,
                filename=filename,
                type_=content_type,
                reply_no=reply_no,
                quote_range=quote_range,
            )

        return File(self, guid=res["guid"], mime_type=extra.get("type"), **extra)

    async def delete_file(self, guid: str) -> dict:
        """
        Delete a file identified by the provided GUID.

        Args:
            guid: The globally unique identifier of the file to be deleted.

        Returns:
            dict: The result of the deletion operation.
        """
        return await async_delete_file(self.session, guid, headers=self._headers)

    async def download_file(self, guid: str, filename: str) -> BytesIO:
        """
        Download and return a file as a BytesIO object given its unique identifier and filename.

        Args:
            guid: The unique identifier of the file to be downloaded.
            filename: The name of the file to be downloaded.

        Returns:
            BytesIO: A BytesIO object containing the downloaded file content.
        """
        return await async_download_file(self.session, guid, filename, headers=self._headers)

    async def post_private_message_by_user_email(self, email: str, text: str) -> Post:
        """Post a private message to a user identified by their email address.

        Args:
            email: The email address of the user to whom the message will be sent.
            text: The content of the message to be posted.

        Returns:
            A Post object representing the posted message.
        """
        url = "/msg/post/private"
        resp = await self.api_post(url, data={"text": text, "user_email": email})

        # Get the created post
        post = await self.get_post(resp["chat_id"], resp["post_no"])
        if post is None:
            raise ValueError(
                f"Failed to retrieve created post {resp['post_no']} from chat {resp['chat_id']}"
            )
        return post

    async def post_private_message_by_user_id(self, user_id: int, text: str) -> Post:
        """Send a private message to a specific user.

        Args:
            user_id: The ID of the user to whom the message will be sent.
            text: The content of the message to be sent.

        Returns:
            The Post object containing information about the sent message.
        """
        url = "/msg/post/private"
        resp = await self.api_post(url, data={"text": text, "user_id": user_id})

        # Get the created post
        post = await self.get_post(resp["chat_id"], resp["post_no"])
        if post is None:
            raise ValueError(
                f"Failed to retrieve created post {resp['post_no']} from chat {resp['chat_id']}"
            )
        return post

    async def post_private_message_by_user_unique_name(self, unique_name: str, text: str) -> Post:
        """Post a private message to a user identified by their unique name.

        Args:
            unique_name: The unique name of the user to whom the private message is to be sent.
            text: The content of the private message.

        Returns:
            An instance of the Post class representing the posted message.
        """
        url = "/msg/post/private"
        resp = await self.api_post(url, data={"text": text, "user_unique_name": unique_name})

        # Get the created post
        post = await self.get_post(resp["chat_id"], resp["post_no"])
        if post is None:
            raise ValueError(
                f"Failed to retrieve created post {resp['post_no']} from chat {resp['chat_id']}"
            )
        return post

    async def mark_all_messages_as_read(self, org_id: int | None = None) -> bool:
        """Mark all messages as read for the organization or everywhere if org_id is None.

        Args:
            org_id: The ID of the organization. This parameter is optional.

        Returns:
            True if the operation was successful, False otherwise.
        """
        url = "/msg/lastread/all"
        data = {}
        if org_id is not None:
            data["org_id"] = org_id
        response = await self.api_post(url, data=data)
        return response.get("result", None) == "OK"
