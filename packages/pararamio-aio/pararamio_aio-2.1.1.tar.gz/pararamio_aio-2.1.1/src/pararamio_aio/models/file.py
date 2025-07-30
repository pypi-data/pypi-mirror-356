"""Async File model."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from .base import BaseModel

if TYPE_CHECKING:
    from ..client import AsyncPararamio

__all__ = ("File",)


class File(BaseModel):
    """Async File model with explicit loading."""

    def __init__(self, client: AsyncPararamio, guid: str, name: str | None = None, **kwargs):
        """Initialize async file.

        Args:
            client: AsyncPararamio client
            guid: File GUID
            name: Optional file name
            **kwargs: Additional file data
        """
        super().__init__(client, guid=guid, name=name, **kwargs)
        self.guid = guid

    @property
    def name(self) -> str | None:
        """Get file name."""
        return self._data.get("name") or self._data.get("filename")

    @property
    def mime_type(self) -> str | None:
        """Get file MIME type."""
        return self._data.get("mime_type") or self._data.get("type")

    @property
    def size(self) -> int | None:
        """Get file size in bytes."""
        return self._data.get("size")

    @property
    def chat_id(self) -> int | None:
        """Get associated chat ID."""
        return self._data.get("chat_id")

    @property
    def organization_id(self) -> int | None:
        """Get associated organization ID."""
        return self._data.get("organization_id")

    @property
    def reply_no(self) -> int | None:
        """Get associated reply number."""
        return self._data.get("reply_no")

    async def download(self) -> bytes:
        """Download file content.

        Returns:
            File content as bytes
        """
        if not self.name:
            raise ValueError("File name is required for download")

        # Use the client's download_file method
        bio = await self.client.download_file(self.guid, self.name)
        return bio.read()

    async def delete(self) -> bool:
        """Delete this file.

        Returns:
            True if successful
        """
        try:
            result = await self.client.delete_file(self.guid)
            return result.get("success", True)
        except (AttributeError, KeyError, TypeError, ValueError):
            return False

    def get_download_url(self) -> str:
        """Get file download URL.

        Returns:
            Download URL string
        """
        if not self.name:
            raise ValueError("File name is required for download URL")

        return f"https://file.pararam.io/download/{self.guid}/{quote(self.name)}"

    def __str__(self) -> str:
        """String representation."""
        return self.name or f"File({self.guid})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<File(guid={self.guid}, name={self.name}, size={self.size})>"
