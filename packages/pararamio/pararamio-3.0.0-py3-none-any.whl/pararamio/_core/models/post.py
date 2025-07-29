"""Core Post model without lazy loading."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pararamio._core.utils.helpers import parse_iso_datetime

from .base import CoreBaseModel

if TYPE_CHECKING:
    from datetime import datetime

    from pararamio._core._types import FormatterT, PostMetaT, TextParsedT

__all__ = ('CorePost',)


# Attribute formatters for Post
POST_ATTR_FORMATTERS: FormatterT = {
    'post_no': lambda data, key: int(data[key]),
    'time_edited': parse_iso_datetime,
    'time_created': parse_iso_datetime,
}


class CorePost(CoreBaseModel):
    """Core Post model with common functionality."""

    # Post attributes (copied from original)
    _chat: Any  # Reference to chat object
    chat_id: int
    event: dict[str, Any] | None
    id: int | None
    is_deleted: bool
    meta: PostMetaT
    post_no: int
    reply_no: int | None
    text: str
    text_parsed: list[TextParsedT]
    time_created: datetime
    time_edited: datetime | None
    user_id: int
    uuid: str | None
    ver: int | None

    def __init__(self, chat: Any, **kwargs: Any) -> None:
        self._chat = chat
        self._attr_formatters = POST_ATTR_FORMATTERS

        # Call parent constructor
        CoreBaseModel.__init__(self, **kwargs)

    @property
    def chat(self) -> Any:
        """Get chat object."""
        return self._chat

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CorePost):
            return id(other) == id(self)
        return self.chat_id == other.chat_id and self.post_no == other.post_no

    def __str__(self) -> str:
        return f'Post {self.post_no} in Chat {self.chat_id}'
