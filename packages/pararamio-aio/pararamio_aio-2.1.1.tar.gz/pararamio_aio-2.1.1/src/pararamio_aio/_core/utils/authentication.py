from __future__ import annotations

import binascii
import json
import logging
import time
from typing import TYPE_CHECKING, Any
from urllib.error import HTTPError

from pararamio_aio._core import exceptions as ex
from pararamio_aio._core.constants import XSRF_HEADER_NAME
from pararamio_aio._core.exceptions import RateLimitException
from pararamio_aio._core.utils.http_client import RateLimitHandler

from .auth_flow import generate_otp
from .requests import api_request, raw_api_request

if TYPE_CHECKING:
    from http.cookiejar import CookieJar

    from pararamio_aio._core._types import HeaderLikeT, SecondStepFnT

__all__ = (
    'authenticate',
    'do_second_step',
    'do_second_step_with_code',
    'get_xsrf_token',
)

XSFR_URL = INIT_URL = '/auth/init'
LOGIN_URL = '/auth/login/password'
TWO_STEP_URL = '/auth/totp'
AUTH_URL = '/auth/next'
log = logging.getLogger('pararamio')


def get_xsrf_token(cookie_jar: CookieJar) -> str:
    _, headers = raw_api_request(XSFR_URL, cookie_jar=cookie_jar)
    for key, value in headers:
        if key.lower() == 'x-xsrftoken':
            return value
    msg = f'XSFR Header was not found in {XSFR_URL} url'
    raise ex.PararamioXSFRRequestError(msg)


def do_init(cookie_jar: CookieJar, headers: dict) -> tuple[bool, dict]:
    try:
        return True, api_request(
            INIT_URL,
            method='GET',
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_login(login: str, password: str, cookie_jar: CookieJar, headers: dict) -> tuple[bool, dict]:
    try:
        return True, api_request(
            LOGIN_URL,
            method='POST',
            data={'email': login, 'password': password},
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_taking_secret(cookie_jar: CookieJar, headers: dict) -> tuple[bool, dict]:
    try:
        return True, api_request(
            AUTH_URL,
            method='GET',
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_second_step(cookie_jar: CookieJar, headers: dict, key: str) -> tuple[bool, dict[str, str]]:
    """
    do second step pararam login with TFA key or raise Exception
    :param cookie_jar: cookie container
    :param headers: headers to send
    :param key: key to generate one time code
    :return: True if login success
    """
    if not key:
        msg = 'key can not be empty'
        raise ex.PararamioSecondFactorAuthenticationException(msg)
    try:
        key = generate_otp(key)
    except binascii.Error as e:
        msg = 'Invalid second step key'
        raise ex.PararamioSecondFactorAuthenticationException(msg) from e
    try:
        resp = api_request(
            TWO_STEP_URL,
            method='POST',
            data={'code': key},
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise
    return True, resp


def do_second_step_with_code(
    cookie_jar: CookieJar, headers: dict[str, str], code: str
) -> tuple[bool, dict[str, str]]:
    """
    do second step pararam login with TFA code or raise Exception
    :param cookie_jar: cookie container
    :param headers: headers to send
    :param code: 6 digits code
    :return:  True if login success
    """
    if not code:
        msg = 'code can not be empty'
        raise ex.PararamioSecondFactorAuthenticationException(msg)
    if len(code) != 6:
        msg = 'code must be 6 digits len'
        raise ex.PararamioSecondFactorAuthenticationException(msg)
    try:
        resp = api_request(
            TWO_STEP_URL,
            method='POST',
            data={'code': code},
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise
    return True, resp


def _handle_rate_limit(wait_auth_limit: bool) -> None:
    """Handle rate limiting before authentication."""
    rate_limit_handler = RateLimitHandler()
    should_wait, wait_seconds = rate_limit_handler.should_wait()
    if should_wait:
        if wait_auth_limit:
            time.sleep(wait_seconds)
        else:
            msg = f'Rate limit exceeded. Retry after {wait_seconds} seconds'
            raise RateLimitException(msg, retry_after=wait_seconds)


def _handle_captcha(
    login: str, password: str, cookie_jar: CookieJar, headers: dict[str, Any], resp: dict[str, Any]
) -> tuple[bool, tuple[bool, dict[str, Any]]]:
    """Handle captcha requirement during authentication.

    Returns:
        Tuple of (was_captcha_required, (success, response))
    """
    if resp.get('codes', {}).get('non_field', '') != 'captcha_required':
        return False, (False, resp)

    try:
        from pararamio_aio._core.utils.captcha import (  # pylint: disable=import-outside-toplevel
            show_captcha,
        )

        success = show_captcha(f'login:{login}', headers, cookie_jar)
        if not success:
            msg = 'Captcha required'
            raise ex.PararamioCaptchaAuthenticationException(msg)
        return True, do_login(login, password, cookie_jar, headers)
    except ImportError as e:
        msg = 'Captcha required, but exception when show it'
        raise ex.PararamioCaptchaAuthenticationException(msg) from e


def authenticate(
    login: str,
    password: str,
    cookie_jar: CookieJar,
    headers: HeaderLikeT | None = None,
    second_step_fn: SecondStepFnT | None = do_second_step,
    second_step_arg: str | None = None,
    wait_auth_limit: bool = False,
) -> tuple[bool, dict[str, Any], str]:
    # Handle rate limiting
    _handle_rate_limit(wait_auth_limit)

    if not headers or XSRF_HEADER_NAME not in headers:
        if headers is None:
            headers = {}
        headers[XSRF_HEADER_NAME] = get_xsrf_token(cookie_jar)

    success, resp = do_login(login, password, cookie_jar, headers)

    # Handle captcha if required
    captcha_handled, captcha_result = _handle_captcha(login, password, cookie_jar, headers, resp)
    if captcha_handled:
        success, resp = captcha_result

    if not success and resp.get('error', 'xsrf'):
        log.debug('invalid xsrf trying to get new one')
        headers[XSRF_HEADER_NAME] = get_xsrf_token(cookie_jar)
        success, resp = do_login(login, password, cookie_jar, headers)

    if not success:
        log.error('authentication failed: %s', resp.get('error', ''))
        msg = 'Login, password authentication failed'
        raise ex.PararamioPasswordAuthenticationException(msg)

    if second_step_fn is not None and second_step_arg:
        success, resp = second_step_fn(cookie_jar, headers, second_step_arg)
        if not success:
            msg = 'Second factor authentication failed'
            raise ex.PararamioSecondFactorAuthenticationException(msg)

    success, resp = do_taking_secret(cookie_jar, headers)
    if not success:
        msg = 'Taking secret failed'
        raise ex.PararamioAuthenticationException(msg)

    success, resp = do_init(cookie_jar, headers)
    return True, {'user_id': resp.get('user_id')}, headers[XSRF_HEADER_NAME]
