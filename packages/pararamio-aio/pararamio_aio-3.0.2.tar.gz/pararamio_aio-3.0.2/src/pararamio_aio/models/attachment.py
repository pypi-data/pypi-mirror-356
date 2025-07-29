"""Async Attachment model."""

from __future__ import annotations

import mimetypes
import os
from dataclasses import dataclass
from io import BufferedReader, BytesIO
from os import PathLike
from os.path import basename
from typing import BinaryIO

import aiofiles

__all__ = ("Attachment",)


def guess_mime_type(filename: str | PathLike) -> str:
    """Guess MIME type from filename.

    Args:
        filename: File name or path

    Returns:
        MIME type string
    """
    if not mimetypes.inited:
        mimetypes.init(files=os.environ.get("PARARAMIO_MIME_TYPES_PATH", None))
    return mimetypes.guess_type(str(filename))[0] or "application/octet-stream"


@dataclass
class Attachment:
    """File attachment representation.

    This is a utility class for handling file attachments before upload.
    It can handle various file input types and provides helpers for
    filename and content type detection.
    """

    file: str | bytes | PathLike | BytesIO | BinaryIO
    filename: str | None = None
    content_type: str | None = None

    @property
    def guess_filename(self) -> str:
        """Guess filename from file object.

        Returns:
            Guessed filename or 'unknown'
        """
        if self.filename:
            return self.filename

        if isinstance(self.file, (str, PathLike)):
            return basename(str(self.file))

        if isinstance(self.file, (BytesIO, BinaryIO, BufferedReader)):
            try:
                name = getattr(self.file, "name", None)
                if name:
                    return basename(name)
            except AttributeError:
                pass

        return "unknown"

    @property
    def guess_content_type(self) -> str:
        """Guess content type from file.

        Returns:
            MIME type string
        """
        if self.content_type:
            return self.content_type

        if isinstance(self.file, (str, PathLike)):
            return guess_mime_type(self.file)

        if isinstance(self.file, (BinaryIO, BufferedReader)):
            name = getattr(self.file, "name", None)
            if name:
                return guess_mime_type(name)

        return "application/octet-stream"

    async def get_fp(self) -> BytesIO | BinaryIO:
        """Get file pointer asynchronously.

        This method handles async file reading for path-based files.

        Returns:
            File-like object (BytesIO or BinaryIO)

        Raises:
            TypeError: If file type is not supported
        """
        if isinstance(self.file, bytes):
            return BytesIO(self.file)

        if isinstance(self.file, (str, PathLike)):
            # Read file asynchronously
            async with aiofiles.open(self.file, "rb") as f:
                content = await f.read()
                return BytesIO(content)

        if isinstance(self.file, (BytesIO, BinaryIO, BufferedReader)):
            return self.file

        raise TypeError(f"Unsupported type {type(self.file)}")

    @property
    def fp(self) -> BytesIO | BinaryIO:
        """Get file pointer.

        Note: This is a sync property. For async file reading,
        use get_fp() method instead.

        Returns:
            File-like object

        Raises:
            TypeError: If file type is not supported
        """
        if isinstance(self.file, bytes):
            return BytesIO(self.file)

        if isinstance(self.file, (str, PathLike)):
            # Sync file read - not recommended in async context
            with open(self.file, "rb") as f:
                return BytesIO(f.read())

        if isinstance(self.file, (BytesIO, BinaryIO, BufferedReader)):
            return self.file

        raise TypeError(f"Unsupported type {type(self.file)}")

    def __str__(self) -> str:
        """String representation."""
        return f"Attachment({self.guess_filename})"
