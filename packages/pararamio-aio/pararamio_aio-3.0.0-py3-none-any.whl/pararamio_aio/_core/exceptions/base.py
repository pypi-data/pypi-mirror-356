from __future__ import annotations

__all__ = (
    'PararamModelNotLoaded',
    'PararamNoNextPost',
    'PararamNoPrevPost',
    'PararamNotFound',
    'PararamioAuthenticationException',
    'PararamioCaptchaAuthenticationException',
    'PararamioException',
    'PararamioHTTPRequestException',
    'PararamioLimitExceededException',
    'PararamioMethodNotAllowed',
    'PararamioPasswordAuthenticationException',
    'PararamioRequestException',
    'PararamioSecondFactorAuthenticationException',
    'PararamioServerResponseException',
    'PararamioValidationException',
    'PararamioXSFRRequestError',
)

import json
from json import JSONDecodeError
from typing import IO
from urllib.error import HTTPError


class PararamioException(Exception):  # noqa: N818
    pass


class PararamioValidationException(PararamioException):
    pass


class PararamModelNotLoaded(PararamioException):
    """Exception raised when trying to access an attribute that hasn't been loaded yet."""


class PararamNotFound(PararamioException):
    pass


class PararamioHTTPRequestException(HTTPError, PararamioException):  # noqa: N818  # pylint: disable=too-many-ancestors
    _response: bytes | None
    fp: IO[bytes]

    def __init__(self, url: str, code: int, msg: str, hdrs: list[tuple[str, str]], fp: IO[bytes]):
        self._response = None
        self.msg = msg
        super().__init__(url, code, msg, hdrs, fp)  # type: ignore

    @property
    def response(self):
        if not self._response and self.fp is not None:
            self._response = self.fp.read()
        return self._response

    @property
    def message(self) -> str | None:
        if self.code in [403, 400]:
            try:
                resp = json.loads(self.response)
                return resp.get('error', None) or resp.get('message', None)
            except JSONDecodeError:
                pass
        return None

    def __str__(self):
        msg = self.message
        if msg:
            return msg
        return str(super(HTTPError, self))


class PararamioRequestException(PararamioException):
    pass


class PararamioServerResponseException(PararamioRequestException):
    response: dict

    def __init__(self, msg: str, response: dict):
        self.msg = msg
        self.response = response

    def __str__(self):
        return f'{self.__class__.__name__}, {self.msg or " has been raised"}'


class PararamioLimitExceededException(PararamioRequestException):
    pass


class PararamioMethodNotAllowed(PararamioException):
    pass


class PararamioAuthenticationException(PararamioException):
    retry_after: int | None = None


class PararamioXSFRRequestError(PararamioAuthenticationException):
    pass


class PararamioPasswordAuthenticationException(PararamioAuthenticationException):
    pass


class PararamioSecondFactorAuthenticationException(PararamioAuthenticationException):
    pass


class PararamioCaptchaAuthenticationException(PararamioAuthenticationException):
    pass


class PararamNoNextPost(PararamioException, StopIteration):
    pass


class PararamNoPrevPost(PararamioException, StopIteration):
    pass
