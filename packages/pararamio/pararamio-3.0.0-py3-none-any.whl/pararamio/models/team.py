from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio._core import PararamioRequestException
from pararamio._core.base import BaseLoadedAttrPararamObject, BasePararamObject
from pararamio._core.utils.helpers import parse_iso_datetime

from .base import BaseClientObject
from .group import Group
from .user import User

if TYPE_CHECKING:
    from datetime import datetime

    from .._types import FormatterT
    from ..client import Pararamio
__all__ = (
    "TeamMember",
    "Team",
    "TeamMemberStatus",
)

ATTR_FORMATTERS: FormatterT = {
    "time_edited": parse_iso_datetime,
    "time_created": parse_iso_datetime,
}
MEMBER_ATTR_FORMATTERS: FormatterT = {
    **ATTR_FORMATTERS,
    "last_activity": parse_iso_datetime,
}


class TeamMemberStatus(BasePararamObject):
    _data: dict[str, Any]
    id: int
    user_id: int
    setter_id: int
    org_id: int
    time_created: datetime
    status: str
    _attr_formatters = {
        "time_created": parse_iso_datetime,
    }

    def __init__(self, client: Pararamio, id: int, **kwargs: Any) -> None:
        self._client = client
        self._data = {**kwargs, "id": int(id)}


class TeamMember(BasePararamObject, BaseClientObject):
    _data: dict[str, Any]
    chats: list[int]
    email: str
    groups: list[int]
    id: int
    org_id: int
    inviter_id: int | None
    is_admin: bool
    is_member: bool
    last_activity: datetime
    phonenumber: str
    state: str
    time_created: datetime
    time_updated: datetime
    two_step_enabled: bool
    _attr_formatters = MEMBER_ATTR_FORMATTERS

    def __init__(self, client: Pararamio, id: int, org_id: int, **kwargs: Any) -> None:
        self._data = {**kwargs, "id": int(id), "org_id": int(org_id)}
        self._client = client

    def __str__(self):
        return self._data.get("email", self._data["id"])

    def __eq__(self, other):
        if not isinstance(other, (TeamMember, User)):
            return hash(other) == hash(self)
        return self.id == other.id

    @property
    def user(self) -> User:
        return User(client=self._client, id=self.id)

    def get_last_status(self) -> TeamMemberStatus | None:
        url = f"/core/org/status?user_ids={self.id}"
        res = self._client.api_get(url).get("data", [])
        if not res:
            return None
        return TeamMemberStatus(self._client, **res[0])

    def add_status(self, status: str) -> bool:
        url = "/core/org/status"
        data = {
            "org_id": self.org_id,
            "status": status,
            "user_id": self.id,
        }
        res = self._client.api_post(url, data=data)
        return bool(res) and res.get("result") == "OK"


class Team(BaseLoadedAttrPararamObject, BaseClientObject):
    _data: dict[str, Any]
    admins: list[int]
    default_thread_id: int
    description: str | None
    email_domain: str | None
    groups: list[int]
    guest_thread_id: int | None
    guests: list[int]
    id: int
    inviter_id: int | None
    is_active: bool
    slug: str
    state: str
    time_created: str
    time_updated: str
    title: str
    two_step_required: bool
    users: list[int]
    _attr_formatters = ATTR_FORMATTERS

    def __init__(self, client: Pararamio, id: int, load_on_key_error: bool = True, **kwargs):
        self._client = client
        self._load_on_key_error = load_on_key_error
        self._data = {**kwargs, "id": int(id)}

    def __str__(self):
        text = self._data.get("text", None)
        if text is None:
            self.load()
            text = self._data["text"]
        return text

    def __eq__(self, other):
        if not isinstance(other, Team):
            return hash(other) == hash(self)
        return self.id == other.id

    def __contains__(self, item):
        if not isinstance(item, (TeamMember, User)):
            return False
        return item.id in self.users

    def create_role(self, name: str, description: str | None = None) -> Group:
        return Group.create(
            self._client, organization_id=self.id, name=name, description=description
        )

    def load(self):
        """
        Fetches data from the API for the current organization's ID and updates the object's data.

        Requests data from the organization's endpoint using the object's ID,
        then updates the object's data with the response.

        Returns:
            self: The current object instance with updated data.
        """
        url = f"/core/org?ids={self.id}"
        res = self._client.api_get(url)
        self._data.update(res)
        return self

    def member_info(self, user_id: int) -> TeamMember:
        url = f"/core/org/{self.id}/member_info/{user_id}"
        res = self._client.api_get(url)
        if not res:
            raise PararamioRequestException(f"empty response for user {user_id}")
        return TeamMember(self._client, org_id=self.id, **res)

    def members_info(self) -> list[TeamMember]:
        url = f"/core/org/{self.id}/member_info"
        res = self._client.api_get(url)
        if res:
            return [TeamMember(self._client, org_id=self.id, **m) for m in res.get("data", [])]
        return []

    @classmethod
    def my_team_ids(cls, client: Pararamio) -> list[int]:
        url = "/core/org/sync"
        res = client.api_get(url) or {}
        return res.pop("ids", [])

    @classmethod
    def load_teams(cls, client: Pararamio) -> list[Team]:
        """

        Loads teams from the Pararamio client.

        @param client: An instance of the Pararamio client.
        @return: A list of Team objects.
        """
        ids = cls.my_team_ids(client)

        if ids:
            url = "/core/org?ids=" + ",".join(map(str, ids))
            res = client.api_get(url)

            if res:
                return [cls(client, **r) for r in res["orgs"]]

        return []

    def mark_all_messages_as_read(self) -> bool:
        return self._client.mark_all_messages_as_read(self.id)
