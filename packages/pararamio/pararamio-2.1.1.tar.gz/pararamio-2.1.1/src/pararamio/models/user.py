from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Sequence, TypedDict
from urllib.parse import quote

# Imports from core
from pararamio._core import PararamNotFound
from pararamio._core.base import BaseLoadedAttrPararamObject
from pararamio._core.utils.helpers import unescape_dict

from .activity import Activity, ActivityAction
from .base import BaseClientObject
from .chat import Chat

if TYPE_CHECKING:
    from datetime import datetime

    from .._types import QuoteRangeT
    from ..client import Pararamio
    from .post import Post

__all__ = ("User", "UserSearchResult", "UserInfoParsedItem")


@dataclass
class UserSearchResult:
    id: int
    avatar: str | None
    name: str
    unique_name: str
    custom_name: str | None
    time_created: str
    time_updated: str
    other_blocked: bool
    pm_thread_id: int | None
    is_bot: bool
    user: User

    @property
    def has_pm(self) -> bool:
        return self.pm_thread_id is not None

    def get_pm_thread(self) -> Chat:
        if self.pm_thread_id is not None:
            chat = Chat(self.user._client, self.pm_thread_id)
            return chat
        return Chat.create_private_chat(self.user._client, self.id)

    def post(
        self,
        text: str,
        quote_range: QuoteRangeT | None = None,
        reply_no: int | None = None,
    ) -> Post:
        chat = self.get_pm_thread()
        return chat.post(text=text, quote_range=quote_range, reply_no=reply_no)


class UserInfoParsedItem(TypedDict):
    type: str
    value: str


INTERSECTION_KEYS = (
    "id",
    "name",
    "unique_name",
    "time_created",
    "time_updated",
    "is_bot",
)


class User(BaseLoadedAttrPararamObject, BaseClientObject):
    id: int
    name: str
    name_trans: str
    info: str
    unique_name: str
    deleted: bool
    active: bool
    time_updated: str
    time_created: str
    is_bot: bool
    alias: None | None
    timezone_offset_minutes: int
    owner_id: None | None
    organizations: list[int]
    info_parsed: list[UserInfoParsedItem]
    _data: dict[str, Any]

    def __init__(self, client, id: int, load_on_key_error: bool = True, **kwargs):
        self._client = client
        self.id = id
        self._data = {"id": id, **kwargs}
        self._load_on_key_error = load_on_key_error

    def __eq__(self, other):
        if not isinstance(other, User):
            return id(other) == id(self)
        return self.id == other.id

    def load(self) -> User:
        resp = list(self._client.get_users_by_ids([self.id]))
        if len(resp) != 1:
            raise PararamNotFound()
        self._data = resp[0]._data
        return self

    @classmethod
    def load_users(cls, client: Pararamio, ids: Sequence[int]) -> list[User]:
        if len(ids) == 0:
            return []
        if len(ids) > 100:
            raise ValueError("too many ids, max 100")
        url = "/user/list?ids=" + ",".join(map(str, ids))
        return [
            cls(client=client, **unescape_dict(data, ["name"]))
            for data in client.api_get(url).get("users", [])
        ]

    def post(
        self,
        text: str,
        quote_range: QuoteRangeT | None = None,
        reply_no: int | None = None,
    ) -> Post:
        for res in self.search(self._client, self.unique_name):
            if res.unique_name == self.unique_name:
                return res.post(text=text, quote_range=quote_range, reply_no=reply_no)
        raise PararamNotFound(f"User {self.unique_name} not found")

    def __str__(self):
        if "name" not in self._data:
            self.load()
        return self._data.get("name")

    @classmethod
    def search(
        cls, client: Pararamio, search_string: str, include_self: bool = False
    ) -> list[UserSearchResult]:
        url = f"/user/search?flt={quote(search_string)}"
        if not include_self:
            url += "&self=false"
        result: list[UserSearchResult] = []
        for response in client.api_get(url).get("users", []):
            data = unescape_dict(response, keys=["name"])
            data["user"] = cls(client, **{k: data[k] for k in INTERSECTION_KEYS})
            result.append(UserSearchResult(**data))
        return result

    def _activity_page_loader(self) -> Callable[..., dict[str, Any]]:
        def loader(action: ActivityAction | None = None, page: int = 1) -> dict[str, Any]:
            action_ = action.value if action else ""
            url = f"/activity?user_id={self.id}&action={action_}&page={page}"
            return self._client.api_get(url)

        return loader

    def get_activity(
        self,
        start: datetime,
        end: datetime,
        actions: list[ActivityAction] | None = None,
    ) -> list[Activity]:
        """get user activity

        :param start: start time
        :param end: end time
        :param actions: list of action types (all actions if None)
        :returns: activity list
        """
        return Activity.get_activity(self._activity_page_loader(), start, end, actions)
