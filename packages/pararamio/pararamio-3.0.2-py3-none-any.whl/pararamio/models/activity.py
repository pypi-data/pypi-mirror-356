from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Callable

# Imports from core
from pararamio._core.utils.helpers import parse_iso_datetime

__all__ = ("ActivityAction", "Activity")


class ActivityAction(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    READ = "thread-read"
    POST = "thread-post"
    CALL = "calling"
    CALL_END = "endcall"


class Activity:
    action: ActivityAction
    time: datetime

    def __init__(self, action: ActivityAction, time: datetime):
        self.action = action
        self.time = time

    def __str__(self):
        return str((self.time, self.action))

    @classmethod
    def _from_api_data(cls, data: dict[str, str]) -> Activity:
        time = parse_iso_datetime(data, "datetime")
        if time is None:
            raise ValueError("Invalid time format")
        return cls(
            action=ActivityAction(data["action"]),
            time=time,
        )

    @classmethod
    def get_activity(
        cls,
        page_loader: Callable[..., dict[str, Any]],
        start: datetime,
        end: datetime,
        actions: list[ActivityAction] | None = None,
    ) -> list[Activity]:
        results = []
        actions_: list[ActivityAction | None] = [None]
        if actions:
            actions_ = actions  # type: ignore[assignment]
        for action in actions_:
            page = 1
            is_last_page = False
            while not is_last_page:
                data = page_loader(action, page=page).get("data", [])
                if not data:
                    break
                for d in data:
                    act = Activity._from_api_data(d)
                    if act.time > end:
                        continue
                    if act.time < start:
                        is_last_page = True
                        break
                    results.append(act)
                page += 1
        return sorted(results, key=lambda x: x.time)
