from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Callable

from .utils.helpers import get_formatted_attr_or_load

if TYPE_CHECKING:
    from ._types import FormatterT
    from .client_protocol import AsyncClientProtocol, ClientProtocol
__all__ = (
    'BaseClientObject',
    'BaseLoadedAttrMetaClass',
    'BaseLoadedAttrPararamObject',
    'BasePararamObject',
)

DEFAULT_ATTRIBUTES = {
    '_attr_formatters': {},
    'load': lambda _: None,
    '_load_on_key_error': False,
}


# noinspection PyIncorrectDocstring
def get_loaded_formatted_attr(self, key: str) -> Any:
    """
    Fetches a formatted attribute from the object's internal storage.

    If the attribute is not already loaded and '_load_on_key_error' is True,
    the method attempts to load the attribute first.

    Parameters:
        key (str): The key corresponding to the desired attribute.

    Returns:
        Any: The formatted attribute value.
    """
    if key in DEFAULT_ATTRIBUTES:
        return DEFAULT_ATTRIBUTES[key]
    return get_formatted_attr_or_load(
        self,
        key,
        getattr(self, '_attr_formatters', None),  # pylint: disable=protected-access
        self.load if self._load_on_key_error else None,  # pylint: disable=protected-access
    )


# noinspection PyIncorrectDocstring
def get_formatted_attr(self, key: str) -> Any:
    """

    Retrieves the formatted attribute value for the specified key.

    Parameters:
        key (str): The attribute key whose formatted value is to be retrieved.

    Returns:
        Any: The formatted attribute value associated with the given key,
             or the original attribute value if no formatter is enabled.
    """
    if key in DEFAULT_ATTRIBUTES:
        return DEFAULT_ATTRIBUTES[key]
    return get_formatted_attr_or_load(self, key, getattr(self, '_attr_formatters', None))


def get_formatted_attr_fn(
    cls: BaseLoadedAttrMetaClass,
    can_be_loaded: bool = False,
) -> Any:
    """

    Determines the appropriate function to get an attribute from a class,
    potentially loading it if required.

    Returns a function that either retrieves a formatted attribute or
    loads it if 'load' and '_load_on_key_error' attributes are present in the class.

    Returns:
        get_formatted_attr_or_load: If the class has both
                                    'load' and '_load_on_key_error' attributes.
        get_formatted_attr: Otherwise.
    """
    _get_formatted_attr_fn = getattr(cls, '_get_formatted_attr', None)
    if _get_formatted_attr_fn:
        return _get_formatted_attr_fn
    if can_be_loaded:
        return get_loaded_formatted_attr
    return get_formatted_attr


class BaseLoadedAttrMetaClass(type):
    """Metaclass for classes that have loaded attributes.
    Adds a custom __getattr__ method to the class to fetch or load formatted attributes.

    this monkeypatching needs to be done to linter-check
    class attributes so that undeclared attributes throw an error
    """

    def __new__(mcs, name, bases, dct):  # pylint: disable=bad-mcs-classmethod-argument
        """

        Creates a new instance of the class, sets up custom attribute access.

        Parameters:
          mcs: The class being instantiated.
          name: The name of the class.
          bases: The base classes.
          dct: The class attributes.

        Returns:
          The new class instance with a custom __getattr__ method.
        """
        new_cls = super().__new__(mcs, name, bases, dct)
        with contextlib.suppress(NameError):
            new_cls.__getattr__ = get_formatted_attr_fn(
                new_cls, BaseLoadedAttrPararamObject in bases
            )
        return new_cls


class BasePararamObject(metaclass=BaseLoadedAttrMetaClass):
    _data: dict[str, Any]
    _attr_formatters: FormatterT
    _get_formatted_attr: Callable[[str], Any]


class BaseLoadedAttrPararamObject(BasePararamObject):
    _load_on_key_error: bool

    def load(self) -> Any:
        """
        Load the object from the server.
        """
        raise NotImplementedError


class BaseClientObject:
    _client: ClientProtocol | AsyncClientProtocol

    @property
    def client(self) -> ClientProtocol | AsyncClientProtocol:
        return self._client
