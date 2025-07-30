"""Async file operations for Pararamio client."""

from __future__ import annotations

import mimetypes
import os
from io import BytesIO
from typing import TYPE_CHECKING, BinaryIO
from urllib.parse import quote

import aiohttp
from pararamio_aio._core import (
    REQUEST_TIMEOUT,
    UPLOAD_TIMEOUT,
    PararamioHTTPRequestException,
)

# File upload base URL
FILE_UPLOAD_URL = "https://file.pararam.io"

if TYPE_CHECKING:
    pass

__all__ = (
    "async_xupload_file",
    "async_delete_file",
    "async_download_file",
)


async def multipart_encode_async(
    fd: BinaryIO | BytesIO,
    *,
    fields: list[tuple[str, str | None | int]] | None = None,
    boundary: str | None = None,
    form_field_name: str = "data",
    filename: str | None = None,
    content_type: str | None = None,
) -> bytes:
    """
    Async version of multipart encoding for file uploads.

    Args:
        fd: A file-like object opened in binary mode that is to be included in the payload.
        fields: An optional list of tuples representing additional form fields.
        boundary: An optional string used to separate parts of the multipart message.
        form_field_name: The name of the form field for the file being uploaded.
        filename: An optional string representing the filename for the file being uploaded.
        content_type: An optional string representing the content type of the file.

    Returns:
        A bytes object representing the encoded multipart/form-data payload.
    """
    if fields is None:
        fields = []
    if boundary is None:
        boundary = "FORM-BOUNDARY"

    body = BytesIO()

    # Write fields
    if fields:
        for key, value in fields:
            if value is None:
                continue
            body.write(f"--{boundary}\r\n".encode())
            body.write(f'Content-Disposition: form-data; name="{key}"'.encode())
            body.write(f"\r\n\r\n{value}\r\n".encode())

    # Get filename if not provided
    if not filename and hasattr(fd, "name"):
        filename = os.path.basename(fd.name)

    if not content_type and filename:
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    # Write file data
    fd.seek(0)
    body.write(f"--{boundary}\r\n".encode())
    body.write(
        f'Content-Disposition: form-data; name="{form_field_name}"; '
        f'filename="{filename}"\r\n'.encode()
    )
    body.write(f"Content-Type: {content_type}\r\n\r\n".encode())
    body.write(fd.read())
    body.write(f"\r\n--{boundary}--\r\n\r\n".encode())

    return body.getvalue()


async def async_xupload_file(
    session: aiohttp.ClientSession,
    fp: BinaryIO | BytesIO,
    fields: list[tuple[str, str | None | int]],
    *,
    filename: str | None = None,
    content_type: str | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = UPLOAD_TIMEOUT,
) -> dict:
    """
    Async version of xupload_file for uploading files to Pararamio.

    Args:
        session: aiohttp client session
        fp: A binary file-like object to upload
        fields: A list of tuples containing field names and values
        filename: Optional filename for the upload
        content_type: Optional MIME type of the file
        headers: Optional additional headers
        timeout: Timeout in seconds for the upload

    Returns:
        Dictionary with upload response data
    """
    url = f"{FILE_UPLOAD_URL}/upload"
    boundary = "FORM-BOUNDARY"

    # Prepare headers
    _headers = {
        "User-agent": "pararamio-aio",
        "Accept": "application/json",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    if headers:
        _headers.update(headers)

    # Encode multipart data
    data = await multipart_encode_async(
        fp,
        fields=fields,
        filename=filename,
        content_type=content_type,
        boundary=boundary,
    )

    # Make request
    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    async with session.post(url, data=data, headers=_headers, timeout=timeout_obj) as response:
        if response.status == 200:
            return await response.json()
        raise PararamioHTTPRequestException(
            url,
            response.status,
            f"HTTP {response.status}",
            dict(response.headers),
            await response.text(),
        )


async def async_delete_file(
    session: aiohttp.ClientSession,
    guid: str,
    headers: dict[str, str] | None = None,
    timeout: int = REQUEST_TIMEOUT,
) -> dict:
    """
    Async version of delete_file for deleting files from Pararamio.

    Args:
        session: aiohttp client session
        guid: The GUID of the file to delete
        headers: Optional additional headers
        timeout: Timeout in seconds for the request

    Returns:
        Dictionary with deletion response data
    """
    url = f"{FILE_UPLOAD_URL}/delete/{guid}"

    _headers = {
        "User-agent": "pararamio-aio",
        "Accept": "application/json",
    }
    if headers:
        _headers.update(headers)

    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    async with session.delete(url, headers=_headers, timeout=timeout_obj) as response:
        if response.status in (200, 204):
            if response.status == 204:
                return {"success": True}
            return await response.json()
        raise PararamioHTTPRequestException(
            url,
            response.status,
            f"HTTP {response.status}",
            dict(response.headers),
            await response.text(),
        )


async def async_download_file(
    session: aiohttp.ClientSession,
    guid: str,
    filename: str,
    headers: dict[str, str] | None = None,
    timeout: int = REQUEST_TIMEOUT,
) -> BytesIO:
    """
    Async version of download_file for downloading files from Pararamio.

    Args:
        session: aiohttp client session
        guid: The GUID of the file to download
        filename: The filename for the download
        headers: Optional additional headers
        timeout: Timeout in seconds for the request

    Returns:
        BytesIO object containing the downloaded file content
    """
    url = f"{FILE_UPLOAD_URL}/download/{guid}/{quote(filename)}"

    _headers = {
        "User-agent": "pararamio-aio",
    }
    if headers:
        _headers.update(headers)

    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    async with session.get(url, headers=_headers, timeout=timeout_obj) as response:
        if response.status == 200:
            content = await response.read()
            return BytesIO(content)
        raise PararamioHTTPRequestException(
            url,
            response.status,
            f"HTTP {response.status}",
            dict(response.headers),
            await response.text(),
        )
