"""Async authentication utilities."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

# Import from core
from pararamio_aio._core import (
    AUTH_INIT_URL,
    AUTH_LOGIN_URL,
    AUTH_NEXT_URL,
    AUTH_TOTP_URL,
    XSRF_HEADER_NAME,
    AuthenticationFlow,
    InvalidCredentialsException,
    PararamioAuthenticationException,
    PararamioHTTPRequestException,
    PararamioSecondFactorAuthenticationException,
    RateLimitException,
    RateLimitHandler,
    TwoFactorFailedException,
    build_url,
    generate_otp,
    prepare_headers,
)

__all__ = (
    "async_authenticate",
    "get_async_xsrf_token",
    "async_do_second_step",
    "async_do_second_step_with_code",
)


async def get_async_xsrf_token(session: aiohttp.ClientSession) -> str:
    """Get XSRF token from /auth/init endpoint.

    Args:
        session: aiohttp session

    Returns:
        XSRF token string

    Raises:
        PararamioAuthenticationException: If failed to get token
    """
    url = build_url(AUTH_INIT_URL)
    async with session.get(url) as response:
        if response.status == 200:
            xsrf_token = response.headers.get("X-Xsrftoken")
            if xsrf_token:
                return xsrf_token

    raise PararamioAuthenticationException("Failed to get XSRF token")


async def _make_auth_request(
    session: aiohttp.ClientSession,
    url: str,
    method: str = "GET",
    data: dict | None = None,
    headers: dict | None = None,
    rate_limit_handler: RateLimitHandler = None,
    wait_auth_limit: bool = False,
) -> tuple[bool, dict]:
    """Make authentication request with error handling.

    Returns:
        Tuple of (success, response_data)
    """
    full_url = build_url(url)

    try:
        if method == "POST" and data:
            async with session.post(full_url, json=data, headers=headers) as response:
                if response.status == 429 and rate_limit_handler:
                    # Handle rate limiting
                    retry_after = rate_limit_handler.handle_rate_limit(dict(response.headers))
                    if wait_auth_limit:
                        await asyncio.sleep(retry_after)
                        # Retry the request after waiting
                        return await _make_auth_request(
                            session, url, method, data, headers, rate_limit_handler, wait_auth_limit
                        )
                    raise RateLimitException(
                        f"Rate limit exceeded. Retry after {retry_after} seconds",
                        retry_after=retry_after,
                    )

                return await _handle_auth_response(response, full_url)
        else:  # GET
            async with session.get(full_url, headers=headers) as response:
                return await _handle_auth_response(response, full_url)

    except aiohttp.ClientError as e:
        raise PararamioAuthenticationException(f"Request failed: {e}") from e


async def _handle_auth_response(
    response: aiohttp.ClientResponse,
    full_url: str,
) -> tuple[bool, dict[str, Any]]:
    """Handle authentication response with common logic."""
    if response.status == 200:
        return True, await response.json()
    if response.status < 500:
        return False, await response.json()
    raise PararamioHTTPRequestException(
        full_url,
        response.status,
        f"HTTP {response.status}",
        dict(response.headers),
        await response.text(),
    )


async def async_do_second_step(
    session: aiohttp.ClientSession,
    headers: dict[str, str],
    key: str,
    rate_limit_handler: RateLimitHandler,
    wait_auth_limit: bool = False,
) -> tuple[bool, dict[str, str]]:
    """
    Do second step authentication with TOTP key asynchronously.

    Args:
        session: aiohttp session
        headers: Headers to send
        key: TOTP key to generate one time code
        rate_limit_handler: Rate limit handler instance
        wait_auth_limit: Wait for rate limit instead of raising exception

    Returns:
        Tuple of (success, response_data)

    Raises:
        PararamioSecondFactorAuthenticationException: If 2FA fails
    """
    if not key:
        raise PararamioSecondFactorAuthenticationException("key can not be empty")

    try:
        code = generate_otp(key)
    except Exception as e:
        raise PararamioSecondFactorAuthenticationException("Invalid second step key") from e

    return await async_do_second_step_with_code(
        session, headers, code, rate_limit_handler, wait_auth_limit
    )


async def async_do_second_step_with_code(
    session: aiohttp.ClientSession,
    headers: dict[str, str],
    code: str,
    rate_limit_handler: RateLimitHandler,
    wait_auth_limit: bool = False,
) -> tuple[bool, dict[str, str]]:
    """
    Do second step authentication with TOTP code asynchronously.

    Args:
        session: aiohttp session
        headers: Headers to send
        code: 6 digits code
        rate_limit_handler: Rate limit handler instance
        wait_auth_limit: Wait for rate limit instead of raising exception

    Returns:
        Tuple of (success, response_data)

    Raises:
        PararamioSecondFactorAuthenticationException: If 2FA fails
    """
    if not code:
        raise PararamioSecondFactorAuthenticationException("code can not be empty")
    if len(code) != 6:
        raise PararamioSecondFactorAuthenticationException("code must be 6 digits len")

    totp_data = AuthenticationFlow.prepare_totp_data(code)
    return await _make_auth_request(
        session,
        AUTH_TOTP_URL,
        "POST",
        totp_data,
        headers,
        rate_limit_handler,
        wait_auth_limit,
    )


async def async_authenticate(
    session: aiohttp.ClientSession,
    login: str,
    password: str,
    key: str | None = None,
    wait_auth_limit: bool = False,
    second_step_fn: Any = None,
    second_step_arg: str | None = None,
) -> tuple[bool, str]:
    """Authenticate with Pararamio API asynchronously.

    Follows the unified authentication flow from core.

    Args:
        session: aiohttp session
        login: User login
        password: User password
        key: Authentication key (for automatic TOTP generation)
        wait_auth_limit: Wait for rate limit instead of raising exception
        second_step_fn: Optional async function for second step authentication
        second_step_arg: Argument for second step function (key or code)

    Returns:
        Tuple of (success, xsrf_token)

    Raises:
        Various authentication exceptions
    """
    rate_limit_handler = RateLimitHandler()

    # Check rate limiting
    await _check_rate_limit(rate_limit_handler, wait_auth_limit)

    try:
        # Step 1: Get XSRF token and login
        xsrf_token, headers = await _perform_login(
            session, login, password, rate_limit_handler, wait_auth_limit
        )

        # Step 2: Handle second step authentication
        await _handle_second_step(
            session,
            headers,
            key,
            second_step_fn,
            second_step_arg,
            rate_limit_handler,
            wait_auth_limit,
        )

        # Step 3: Complete auth flow
        await _complete_auth_flow(session, headers, rate_limit_handler, wait_auth_limit)

        # Clear rate limit on success
        rate_limit_handler.clear()

        return True, xsrf_token

    except RateLimitException:
        # Let rate limit exceptions bubble up
        raise
    except Exception as e:
        if not isinstance(e, (InvalidCredentialsException, TwoFactorFailedException)):
            raise PararamioAuthenticationException(f"Authentication failed: {e}") from e
        raise


async def _check_rate_limit(rate_limit_handler: RateLimitHandler, wait_auth_limit: bool) -> None:
    """Check and handle rate limiting."""
    should_wait, wait_seconds = rate_limit_handler.should_wait()
    if should_wait:
        if wait_auth_limit:
            await asyncio.sleep(wait_seconds)
        else:
            raise RateLimitException(
                f"Rate limit exceeded. Retry after {wait_seconds} seconds", retry_after=wait_seconds
            )


async def _perform_login(
    session: aiohttp.ClientSession,
    login: str,
    password: str,
    rate_limit_handler: RateLimitHandler,
    wait_auth_limit: bool,
) -> tuple[str, dict[str, str]]:
    """Perform login and handle XSRF retry if needed."""
    xsrf_token = await get_async_xsrf_token(session)
    headers = prepare_headers(xsrf_token=xsrf_token)

    login_data = AuthenticationFlow.prepare_login_data(login, password)

    success, resp = await _make_auth_request(
        session,
        AUTH_LOGIN_URL,
        "POST",
        login_data,
        headers,
        rate_limit_handler,
        wait_auth_limit,
    )

    if not success:
        # Parse error and check if we need new XSRF
        error_type, error_msg = AuthenticationFlow.parse_error_response(resp)

        if AuthenticationFlow.should_retry_with_new_xsrf(error_type, error_msg):
            # Retry with new XSRF token
            xsrf_token = await get_async_xsrf_token(session)
            headers[XSRF_HEADER_NAME] = xsrf_token

            success, _ = await _make_auth_request(
                session,
                AUTH_LOGIN_URL,
                "POST",
                login_data,
                headers,
                rate_limit_handler,
                wait_auth_limit,
            )

            if not success:
                raise InvalidCredentialsException("Login failed after XSRF retry")
        else:
            raise InvalidCredentialsException(f"Login failed: {error_msg}")

    return xsrf_token, headers


async def _handle_second_step(
    session: aiohttp.ClientSession,
    headers: dict[str, str],
    key: str | None,
    second_step_fn: Any,
    second_step_arg: str | None,
    rate_limit_handler: RateLimitHandler,
    wait_auth_limit: bool,
) -> None:
    """Handle second step authentication (TOTP or custom)."""
    if second_step_fn is not None and second_step_arg:
        # Use provided second step function
        success, _ = await second_step_fn(
            session, headers, second_step_arg, rate_limit_handler, wait_auth_limit
        )
        if not success:
            raise TwoFactorFailedException("Second factor authentication failed")
    elif key:
        # Use default TOTP with key
        try:
            code = generate_otp(key)
        except Exception as e:
            raise TwoFactorFailedException("Invalid TOTP key") from e

        totp_data = AuthenticationFlow.prepare_totp_data(code)
        success, _ = await _make_auth_request(
            session,
            AUTH_TOTP_URL,
            "POST",
            totp_data,
            headers,
            rate_limit_handler,
            wait_auth_limit,
        )

        if not success:
            raise TwoFactorFailedException("TOTP authentication failed")


async def _complete_auth_flow(
    session: aiohttp.ClientSession,
    headers: dict[str, str],
    rate_limit_handler: RateLimitHandler,
    wait_auth_limit: bool,
) -> None:
    """Complete the authentication flow."""
    success, _ = await _make_auth_request(
        session, AUTH_NEXT_URL, "GET", {}, headers, rate_limit_handler, wait_auth_limit
    )

    if not success:
        raise PararamioAuthenticationException("Failed to complete auth flow")

    success, _ = await _make_auth_request(
        session, AUTH_INIT_URL, "GET", {}, headers, rate_limit_handler, wait_auth_limit
    )

    if not success:
        raise PararamioAuthenticationException("Failed to initialize session")
