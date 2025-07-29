"""Simplified base classes for core models without lazy loading."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pararamio._core._types import FormatterT

__all__ = (
    'CoreBaseModel',
    'CoreClientObject',
)


class CoreBaseModel:
    """Base model class without lazy loading magic."""

    _data: dict[str, Any]
    _attr_formatters: FormatterT

    def __init__(self, **kwargs: Any) -> None:
        self._data = kwargs
        self._attr_formatters = {}

    def __getattribute__(self, key: str) -> Any:
        # Simple version without lazy loading
        try:
            return super().__getattribute__(key)
        except AttributeError:
            if key.startswith('_'):
                raise

            # Get from _data if exists
            data = super().__getattribute__('_data')
            if key in data:
                value = data[key]
                # Apply formatter if exists
                formatters = super().__getattribute__('_attr_formatters')
                if key in formatters:
                    return formatters[key](data, key)
                return value
            raise

    def load_data(self, data: dict[str, Any]) -> None:
        """Load data into the model."""
        self._data.update(data)

    def to_dict(self) -> dict[str, Any]:
        """Get data as dictionary."""
        return self._data.copy()


class CoreClientObject:
    """Base class for objects that need client reference."""

    _client: Any  # Union[ClientProtocol, AsyncClientProtocol] but without import

    def __init__(self, client: Any, **kwargs: Any) -> None:
        self._client = client
        # kwargs are passed to subclasses, not used here
        _ = kwargs

    @property
    def client(self) -> Any:
        return self._client
