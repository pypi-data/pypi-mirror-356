from __future__ import annotations

import asyncio
import json
import logging
import mimetypes
from io import BytesIO
from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO
from urllib.parse import quote

import aiohttp
from aiohttp import FormData

from ..constants import (
    BASE_API_URL,
    FILE_UPLOAD_URL,
    UPLOAD_TIMEOUT,
    VERSION,
)
from ..constants import (
    REQUEST_TIMEOUT as TIMEOUT,
)
from ..exceptions import PararamioHTTPRequestException

if TYPE_CHECKING:
    from .._types import HeaderLikeT

__all__ = (
    'api_request',
    'bot_request',
    'delete_file',
    'download_file',
    'raw_api_request',
    'upload_file',
    'xupload_file',
)
log = logging.getLogger('pararamio')
UA_HEADER = f'pararamio lib version {VERSION}'
DEFAULT_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'User-agent': UA_HEADER,
}


async def bot_request(
    session: aiohttp.ClientSession,
    url: str,
    key: str,
    method: str = 'GET',
    data: dict | None = None,
    headers: dict | None = None,
    timeout: int = TIMEOUT,
):
    """
    Sends an async request to a bot API endpoint with the specified parameters.

    Parameters:
    session (aiohttp.ClientSession): The aiohttp session to use for the request.
    url (str): The endpoint URL of the bot API.
    key (str): The API token for authentication.
    method (str): The HTTP method to use for the request. Defaults to 'GET'.
    data (Optional[dict]): The data payload for the request. Defaults to None.
    headers (Optional[dict]): Additional headers to include in the request. Defaults to None.
    timeout (int): The timeout setting for the request. Defaults to TIMEOUT.

    Returns:
    Response object from the API request.
    """
    _headers = {'X-APIToken': key, **DEFAULT_HEADERS}
    if headers:
        _headers = {**_headers, **headers}
    return await api_request(
        session=session, url=url, method=method, data=data, headers=_headers, timeout=timeout
    )


async def _base_request(
    session: aiohttp.ClientSession,
    url: str,
    method: str = 'GET',
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: int = TIMEOUT,
) -> aiohttp.ClientResponse:
    """
    Sends an async HTTP request and returns a ClientResponse object.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        url (str): The URL endpoint to which the request is sent.
        method (str): The HTTP method to use for the request (default is 'GET').
        data (Optional[bytes]): The payload to include in the request body (default is None).
        headers (Optional[dict]): A dictionary of headers to include in the request
                                  (default is None).
        timeout (int): The timeout for the request in seconds (TIMEOUT defines default).

    Returns:
        aiohttp.ClientResponse: The response object containing the server's response to the HTTP
            request.

    Raises:
        PararamioHTTPRequestException: An exception is raised if there is
                                       an issue with the HTTP request.
    """
    _url = f'{BASE_API_URL}{url}'
    _headers = DEFAULT_HEADERS.copy()
    if headers:
        _headers.update(headers)

    return await _make_request(session, _url, method, data, _headers, timeout)


async def _base_file_request(
    session: aiohttp.ClientSession,
    url: str,
    method='GET',
    data: bytes | FormData | None = None,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> aiohttp.ClientResponse:
    """
    Performs an async file request to the specified URL with the given parameters.

    Arguments:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        url (str): The URL endpoint to send the request to.
        method (str, optional): The HTTP method to use for the request (default is 'GET').
        data (Optional[Union[bytes, FormData]], optional): The data to send in the request body
            (default is None).
        headers (Optional[HeaderLikeT], optional): The headers to include in the request
                                                   (default is None).
        timeout (int, optional): The timeout duration for the request (default value is TIMEOUT).

    Returns:
        aiohttp.ClientResponse: The response object from the file request.

    Raises:
        PararamioHTTPRequestException: If the request fails with an HTTP error code.
    """
    _url = f'{FILE_UPLOAD_URL}{url}'
    _headers = headers or {}

    return await _make_request(session, _url, method, data, _headers, timeout)


async def _read_json_response(response: aiohttp.ClientResponse) -> dict:
    """Read response content and parse as JSON."""
    content = await response.read()
    return json.loads(content)


async def _upload_with_form_data(
    session: aiohttp.ClientSession,
    url: str,
    data: FormData,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> dict:
    """Upload form data and return JSON response."""
    _headers = {
        'User-agent': UA_HEADER,
        'Accept': 'application/json',
        **(headers or {}),
    }

    response = await _base_file_request(
        session,
        url,
        method='POST',
        data=data,
        headers=_headers,
        timeout=timeout,
    )

    return await _read_json_response(response)


async def upload_file(
    session: aiohttp.ClientSession,
    fp: BinaryIO,
    perm: str,
    filename: str | None = None,
    file_type=None,
    headers: HeaderLikeT | None = None,
    timeout: int = UPLOAD_TIMEOUT,
):
    """
    Upload a file to a pararam server asynchronously with specified permissions and optional
    parameters.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        fp (BinaryIO): A file-like object to be uploaded.
        perm (str): The permission level for the uploaded file.
        filename (Optional[str], optional): Optional filename used during upload. Defaults to None.
        file_type (optional): Optional MIME type of the file. Defaults to None.
        headers (Optional[HeaderLikeT], optional): Optional headers to include in the request.
        Defaults to None.
        timeout (int, optional): Timeout duration for the upload request.
        Defaults to UPLOAD_TIMEOUT.

    Returns:
        dict: A dictionary containing the server's response to the file upload.
    """
    url = f'/upload/{perm}'

    if not filename:
        filename = Path(getattr(fp, 'name', 'file')).name
    if not file_type:
        file_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    data = FormData()
    fp.seek(0)
    data.add_field('file', fp, filename=filename, content_type=file_type)

    return await _upload_with_form_data(session, url, data, headers, timeout)


async def xupload_file(
    session: aiohttp.ClientSession,
    fp: BinaryIO,
    fields: list[tuple[str, str | None | int]],
    filename: str | None = None,
    content_type: str | None = None,
    headers: HeaderLikeT | None = None,
    timeout: int = UPLOAD_TIMEOUT,
) -> dict:
    """
    Uploads a file asynchronously to a predefined URL using a multipart/form-data request.

    Arguments:
    - session: The aiohttp session to use for the request.
    - fp: A binary file-like object to upload.
    - fields: A list of tuples where each tuple contains a field name and a value which can be
    a string, None, or an integer.
    - filename: Optional; The name of the file being uploaded.
                If not provided, it defaults to None.
    - content_type: Optional; The MIME type of the file being uploaded.
                    If not provided, it defaults to None.
    - headers: Optional; Additional headers to include in the upload request.
               If not provided, defaults to None.
    - timeout: Optional; The timeout in seconds for the request.
               Defaults to UPLOAD_TIMEOUT.

    Returns:
    - A dictionary parsed from the JSON response of the upload request.
    """
    url = '/upload'

    if not filename:
        filename = Path(getattr(fp, 'name', 'file')).name
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    data = FormData()

    # Add form fields
    for key, value in fields:
        if value is not None:
            data.add_field(key, str(value))

    # Add file
    fp.seek(0)
    data.add_field('data', fp, filename=filename, content_type=content_type)

    return await _upload_with_form_data(session, url, data, headers, timeout)


async def delete_file(
    session: aiohttp.ClientSession,
    guid: str,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> dict:
    url = f'/delete/{guid}'
    response = await _base_file_request(
        session, url, method='DELETE', headers=headers, timeout=timeout
    )
    return await _read_json_response(response)


async def download_file(
    session: aiohttp.ClientSession,
    guid: str,
    filename: str,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> BytesIO:
    url = f'/download/{guid}/{quote(filename)}'
    response = await file_request(session, url, method='GET', headers=headers, timeout=timeout)
    content = await response.read()
    return BytesIO(content)


async def file_request(
    session: aiohttp.ClientSession,
    url: str,
    method='GET',
    data: bytes | None = None,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> aiohttp.ClientResponse:
    _headers = DEFAULT_HEADERS.copy()
    if headers:
        _headers.update(headers)
    return await _base_file_request(
        session,
        url,
        method=method,
        data=data,
        headers=_headers,
        timeout=timeout,
    )


async def _make_request(
    session: aiohttp.ClientSession,
    url: str,
    method: str = 'GET',
    data: Any = None,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> aiohttp.ClientResponse:
    """
    Common request handler for both API and file requests.

    Args:
        session: The aiohttp session to use for the request
        url: The full URL to send the request to
        method: The HTTP method to use
        data: The data to send in the request body
        headers: Headers to include in the request
        timeout: Request timeout in seconds

    Returns:
        The response object from the request

    Raises:
        PararamioHTTPRequestException: If the request fails
    """
    log.debug('%s - %s - %s - %s', url, method, data, headers)

    try:
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        async with session.request(
            method, url, data=data, headers=headers or {}, timeout=timeout_obj
        ) as response:
            if response.status >= 400:
                content = await response.read()
                headers_list = list(response.headers.items())
                raise PararamioHTTPRequestException(
                    url,
                    response.status,
                    response.reason or 'Unknown error',
                    headers_list,
                    BytesIO(content),
                )
            return response
    except asyncio.TimeoutError as e:
        log.exception('%s - %s - timeout', url, method)
        raise PararamioHTTPRequestException(url, 408, 'Request Timeout', [], BytesIO()) from e
    except aiohttp.ClientError as e:
        log.exception('%s - %s', url, method)
        raise PararamioHTTPRequestException(url, 0, str(e), [], BytesIO()) from e


async def raw_api_request(
    session: aiohttp.ClientSession,
    url: str,
    method: str = 'GET',
    data: bytes | None = None,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> tuple[dict, list]:
    response = await _base_request(session, url, method, data, headers, timeout)
    if 200 <= response.status < 300:
        content = await response.read()
        headers_list = list(response.headers.items())
        return json.loads(content), headers_list
    return {}, []


async def api_request(
    session: aiohttp.ClientSession,
    url: str,
    method: str = 'GET',
    data: dict | None = None,
    headers: HeaderLikeT | None = None,
    timeout: int = TIMEOUT,
) -> dict:
    _data = None
    if data is not None:
        _data = json.dumps(data).encode('utf-8')

    response = await _base_request(session, url, method, _data, headers, timeout)

    if response.status == 204:
        return {}

    if 200 <= response.status < 500:
        content = await response.read()
        try:
            return json.loads(content)
        except JSONDecodeError as e:
            log.exception('%s - %s', url, method)
            headers_list = list(response.headers.items())
            raise PararamioHTTPRequestException(
                url,
                response.status,
                'JSONDecodeError',
                headers_list,
                BytesIO(content),
            ) from e
    return {}
