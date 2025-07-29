"""Base classes for async models."""

from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio_aio._core.models.base import CoreBaseModel
from pararamio_aio._core.utils.helpers import parse_iso_datetime

if TYPE_CHECKING:
    from ..client import AsyncPararamio

__all__ = ("BaseModel",)


class BaseModel(CoreBaseModel, ABC):
    """Base async model class.

    Unlike sync models, async models don't use lazy loading.
    All data must be explicitly loaded via async methods.
    """

    def __init__(self, client: AsyncPararamio, **kwargs):
        """Initialize async model.

        Args:
            client: AsyncPararamio client instance
            **kwargs: Model data
        """
        super().__init__(**kwargs)
        self._client = client

    @property
    def client(self) -> AsyncPararamio:
        """Get the client instance."""
        return self._client

    @classmethod
    def from_dict(cls, client: AsyncPararamio, data: dict[str, Any]) -> BaseModel:
        """Create model instance from dict data.

        Args:
            client: AsyncPararamio client instance
            data: Raw API data

        Returns:
            Model instance
        """
        # Apply any formatting transformations
        formatted_data = {}
        for key, value in data.items():
            if key.endswith("_created") or key.endswith("_updated") or key.endswith("_edited"):
                if isinstance(value, str):
                    formatted_data[key] = parse_iso_datetime(data, key)
                else:
                    formatted_data[key] = value
            else:
                formatted_data[key] = value

        return cls(client, **formatted_data)

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary.

        Returns:
            Model data as dict
        """
        result = {}
        for key, value in self._data.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    def __repr__(self) -> str:
        """String representation of the model."""
        model_name = self.__class__.__name__
        id_value = getattr(self, "id", None)
        return f"<{model_name}(id={id_value})>"
