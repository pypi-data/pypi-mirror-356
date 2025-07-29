from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio._core import PararamNotFound
from pararamio._core.base import BaseLoadedAttrPararamObject
from pararamio._core.utils.helpers import format_datetime, format_or_none, parse_iso_datetime

from .base import BaseClientObject

if TYPE_CHECKING:
    from .._types import FormatterT, QuoteRangeT
    from ..client import Pararamio

__all__ = ("DeferredPost",)
ATTR_FORMATTERS: FormatterT = {
    "time_created": parse_iso_datetime,
    "time_sending": parse_iso_datetime,
}


class DeferredPost(BaseLoadedAttrPararamObject, BaseClientObject):
    id: int
    user_id: int
    chat_id: int
    text: str
    reply_no: int | None
    time_created: datetime
    time_sending: datetime
    data: dict
    _data: dict

    def __init__(self, client: Pararamio, id: int, load_on_key_error: bool = True, **kwargs):
        self._client = client
        self.id = id
        self._data = {"id": id, **kwargs}
        self._load_on_key_error = load_on_key_error

    def _get_formatted_attr(self, key: str) -> Any:
        try:
            try:
                return format_or_none(key, self._data, ATTR_FORMATTERS)
            except KeyError:
                return self._data.get("data", {})[key]
        except KeyError:
            if self._load_on_key_error:
                self.load()
                try:
                    return format_or_none(key, self._data, ATTR_FORMATTERS)
                except KeyError:
                    return self._data.get("data", {})[key]
            raise

    def __str__(self):
        text = self._data.get("text", None)
        if text is None:
            self.load()
            text = self._data["text"]
        return text

    def load(self) -> DeferredPost:
        for post in self.get_deferred_posts(self._client):
            if post.id == self.id:
                self._data = post._data
                return self
        raise PararamNotFound(f"Deferred post with id {self.id} not found")

    def delete(self):
        url = f"/msg/deferred/{self.id}"
        self._client.api_delete(url)

    @classmethod
    def create(
        cls,
        client: Pararamio,
        chat_id: int,
        text: str,
        *,
        time_sending: datetime,
        reply_no: int | None = None,
        quote_range: QuoteRangeT | None = None,
    ) -> DeferredPost:
        url = "/msg/deferred"
        data = {
            "chat_id": chat_id,
            "text": text,
            "time_sending": format_datetime(time_sending),
            "reply_no": reply_no,
            "quote_range": quote_range,
        }
        res = client.api_post(url, data)
        return cls(
            client,
            id=int(res["deferred_post_id"]),
            chat_id=chat_id,
            data=data,
            time_sending=time_sending,
        )

    @classmethod
    def get_deferred_posts(cls, client: Pararamio) -> list[DeferredPost]:
        url = "/msg/deferred"
        res = client.api_get(url).get("posts", [])
        return [cls(client, **post) for post in res]
