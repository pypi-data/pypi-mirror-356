"""Async request utilities."""

from __future__ import annotations

from typing import Any

import aiohttp

# Import from core
from pararamio_aio._core import PararamioHTTPRequestException, build_url

# Define BOT_KEY_PARAM locally if not in core
BOT_KEY_PARAM = "key"

__all__ = ("async_api_request", "async_bot_request")


async def async_api_request(
    session: aiohttp.ClientSession,
    url: str,
    method: str = "GET",
    data: dict | None = None,
    headers: dict | None = None,
) -> dict:
    """Make async API request.

    Args:
        session: aiohttp session
        url: API endpoint URL
        method: HTTP method
        data: Request data
        headers: Request headers

    Returns:
        JSON response as dict
    """
    full_url = build_url(url)

    async with session.request(method, full_url, data=data, headers=headers or {}) as response:
        if response.status != 200:
            raise PararamioHTTPRequestException(
                full_url,
                response.status,
                f"HTTP {response.status}",
                dict(response.headers),
                await response.text(),
            )
        return await response.json()


async def async_bot_request(
    url: str,
    key: str,
    method: str = "GET",
    data: dict | None = None,
    headers: dict | None = None,
) -> dict[str, Any]:
    """Make an authenticated bot API request.

    Args:
        url: API endpoint
        key: Bot API key
        method: HTTP method
        data: Request data
        headers: Additional headers

    Returns:
        Response data as dictionary
    """
    # Add bot key to URL
    separator = "&" if "?" in url else "?"
    full_url = f"{url}{separator}{BOT_KEY_PARAM}={key}"

    async with aiohttp.ClientSession() as session:
        return await async_api_request(session, full_url, method, data, headers)
