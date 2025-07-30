from __future__ import annotations

from datetime import datetime
from io import BytesIO
from os import PathLike
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Iterable,
    Sequence,
    cast,
)
from urllib.parse import quote_plus

# Imports from core
from pararamio._core import (
    POSTS_LIMIT,
    PararamioLimitExceededException,
    PararamioMethodNotAllowed,
    PararamioRequestException,
    PararamioValidationException,
    validate_post_load_range,
)
from pararamio._core.base import BaseLoadedAttrPararamObject
from pararamio._core.utils.helpers import (
    encode_chats_ids,
    format_datetime,
    join_ids,
    parse_iso_datetime,
)

from .attachment import Attachment
from .base import BaseClientObject
from .post import Post

if TYPE_CHECKING:
    from .._types import (
        FormatterT,
        QuoteRangeT,
    )
    from ..client import Pararamio
    from .file import File

__all__ = ("Chat",)

ATTR_FORMATTERS: FormatterT = {
    "time_edited": parse_iso_datetime,
    "time_updated": parse_iso_datetime,
    "time_created": parse_iso_datetime,
    "user_time_edited": parse_iso_datetime,
}


def check_result(result: dict) -> bool:
    return "chat_id" in result


# validate_post_load_range is now imported from pararamio_core


class Chat(BaseLoadedAttrPararamObject, BaseClientObject):
    id: int
    title: str
    history_mode: str
    description: str | None
    posts_count: int
    pm: bool
    e2e: bool
    time_created: datetime
    time_updated: datetime
    time_edited: datetime | None
    author_id: int
    two_step_required: bool
    org_visible: bool
    organization_id: int | None
    posts_live_time: int | None
    allow_api: bool
    read_only: bool
    tnew: bool
    adm_flag: bool
    custom_title: str | None
    is_favorite: bool
    inviter_id: int | None
    tshow: bool
    user_time_edited: datetime
    history_start: int
    pinned: list[int]
    thread_groups: list[int]
    thread_users: list[int]
    thread_admins: list[int]
    thread_users_all: list[int]
    last_msg_author_id: int | None
    last_msg_author: str
    last_msg_bot_name: str
    last_msg_text: str
    last_msg: str
    last_read_post_no: int
    thread_guests: list[int]
    _data: dict[str, Any]
    _attr_formatters = ATTR_FORMATTERS

    def __init__(
        self,
        client: Pararamio,
        id: int | None = None,
        load_on_key_error: bool = True,
        **kwargs: Any,
    ) -> None:
        if id is None:
            id = kwargs.get("chat_id", None)
            if id is None:
                id = kwargs["thread_id"]
        self.id = int(id)
        self._data = {}
        if kwargs:
            self._data = {**kwargs, "id": id}
        self._load_on_key_error = load_on_key_error
        self._client = client

    def __str__(self) -> str:
        title = self._data.get("title", "")
        id_ = self.id or ""
        return f"{id_} - {title}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chat):
            return id(other) == id(self)
        return self.id == other.id

    def __contains__(self, item: Post) -> bool:
        if isinstance(item, Post):
            return item.chat == self
        return False

    def load(self) -> Chat:
        if self.id is None:
            raise PararamioMethodNotAllowed(f"Load is not allow for new {self.__class__.__name__}")
        chats = self.load_chats(self._client, [self.id])
        if len(chats) != 1:
            raise PararamioRequestException(f"failed to load data for chat id {self.id}")
        self._data = chats[0]._data
        return self

    def edit(self, **kwargs) -> None:
        """
        Updates the attributes of a chat instance with the provided keyword arguments.

        Parameters:
          kwargs: Arbitrary keyword arguments specifying the attributes to update.

        Returns:
          None

        Raises:
          Various exceptions based on the response from the API PUT request.
        """
        url = f"/core/chat/{self.id}"
        check_result(self._client.api_put(url, data=kwargs))

    def transfer(self, org_id: int) -> bool:
        url = f"/core/chat/{self.id}/transfer/{org_id}"
        return check_result(self._client.api_post(url, {}))

    def delete(self):
        url = f"/core/chat/{self.id}"
        return check_result(self._client.api_delete(url))

    def hide(self) -> bool:
        url = f"/core/chat/{self.id}/hide"
        return check_result(self._client.api_post(url))

    def show(self) -> bool:
        url = f"/core/chat/{self.id}/show"
        return check_result(self._client.api_post(url))

    def favorite(self) -> bool:
        url = f"/core/chat/{self.id}/favorite"
        return check_result(self._client.api_post(url))

    def unfavorite(self) -> bool:
        url = f"/core/chat/{self.id}/unfavorite"
        return check_result(self._client.api_post(url))

    def enter(self) -> bool:
        url = f"/core/chat/{self.id}/enter"
        return check_result(self._client.api_post(url))

    def quit(self) -> bool:
        url = f"/core/chat/{self.id}/quit"
        return check_result(self._client.api_post(url))

    def set_custom_title(self, title: str) -> bool:
        url = f"/core/chat/{self.id}/custom_title"
        return check_result(self._client.api_post(url, {"title": title}))

    def add_users(self, ids: list[int]) -> bool:
        url = f"/core/chat/{self.id}/user/{join_ids(ids)}"
        return check_result(self._client.api_post(url))

    def delete_users(self, ids: list[int]) -> bool:
        url = f"/core/chat/{self.id}/user/{join_ids(ids)}"
        return check_result(self._client.api_delete(url))

    def add_admins(self, ids: list[int]) -> bool:
        url = f"/core/chat/{self.id}/admin/{join_ids(ids)}"
        return check_result(self._client.api_post(url))

    def delete_admins(self, ids: list[int]) -> bool:
        url = f"/core/chat/{self.id}/admin/{join_ids(ids)}"
        return check_result(self._client.api_delete(url))

    def add_groups(self, ids: list[int]) -> bool:
        url = f"/core/chat/{self.id}/group/{join_ids(ids)}"
        return check_result(self._client.api_post(url))

    def delete_groups(self, ids: list[int]) -> bool:
        url = f"/core/chat/{self.id}/group/{join_ids(ids)}"
        return check_result(self._client.api_delete(url))

    def _load_posts(
        self,
        start_post_no: int = -50,
        end_post_no: int = -1,
        limit: int = POSTS_LIMIT,
    ) -> list[Post]:
        url = f"/msg/post?chat_id={self.id}&range={start_post_no}x{end_post_no}"
        _absolute = abs(end_post_no - start_post_no)
        if start_post_no < 0:
            _absolute = +1
        if _absolute >= limit:
            raise PararamioLimitExceededException(f"max post load limit is {limit - 1}")
        res = self._client.api_get(url).get("posts", [])
        if not res:
            return []
        return [Post(chat=self, **post) for post in res]

    def _lazy_posts_loader(
        self, start_post_no: int = -50, end_post_no: int = -1, per_request: int = POSTS_LIMIT
    ) -> Iterable[Post]:
        validate_post_load_range(start_post_no, end_post_no)
        absolute = abs(end_post_no - start_post_no)
        start, end = start_post_no, end_post_no
        if absolute > per_request:
            end = start_post_no + per_request - 1
        posts = iter(self._load_posts(start, end))
        counter = 0
        # For same start and end, need to load 1 post
        range_count = max(1, abs(end_post_no - start_post_no))
        for _ in range(range_count):
            try:
                yield next(posts)
            except StopIteration:
                counter += 1
                res = self._load_posts(start + per_request * counter, end + per_request * counter)
                if not res:
                    return
                posts = iter(res)

    def posts(
        self,
        start_post_no: int = -50,
        end_post_no: int = -1,
    ) -> list[Post]:
        if start_post_no == end_post_no:
            start_post_no = end_post_no - 1
        return list(self._lazy_posts_loader(start_post_no=start_post_no, end_post_no=end_post_no))

    def lazy_posts_load(
        self,
        start_post_no: int = -50,
        end_post_no: int = -1,
        per_request: int = POSTS_LIMIT,
    ) -> Iterable[Post]:
        return self._lazy_posts_loader(
            start_post_no=start_post_no,
            end_post_no=end_post_no,
            per_request=per_request,
        )

    def read_status(self, post_no: int) -> bool:
        return self.mark_read(post_no)

    def mark_read(self, post_no: int | None = None) -> bool:
        url = f"/msg/lastread/{self.id}"
        data: dict[str, int | bool] = {"read_all": True}
        if post_no is not None:
            data = {"post_no": post_no}
        res = self._client.api_post(url, data)
        if "post_no" in res:
            self._data["last_read_post_no"] = res["post_no"]
        if "posts_count" in res:
            self._data["posts_count"] = res["posts_count"]
        return True

    def post(
        self,
        text: str,
        quote_range: QuoteRangeT | None = None,
        reply_no: int | None = None,
        attachments: list[Attachment] | None = None,
    ) -> Post:
        if self.id is None:
            raise ValueError("can not post file to new chat")
        _attachments = []
        for attachment in attachments or []:
            _attachments.append(
                self.upload_file(
                    attachment.fp,
                    filename=attachment.guess_filename,
                    content_type=attachment.guess_content_type,
                    reply_no=reply_no,
                )
            )
        return Post.create(
            self,
            text=text,
            reply_no=reply_no,
            quote=cast(str, quote_range["text"]) if quote_range else None,
            attachments=[attach.guid for attach in _attachments],
        )

    def upload_file(
        self,
        file: str | BytesIO | BinaryIO | PathLike,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        reply_no: int | None = None,
        quote_range: str | None = None,
    ) -> File:
        if self.id is None:
            raise ValueError("can not upload file to new chat")
        if not isinstance(file, (str, PathLike)) and not filename:
            raise PararamioValidationException("can not determine filename for BinaryIO")
        attachment = Attachment(file, filename=filename, content_type=content_type)
        return self._client.upload_file(
            file=attachment.fp,
            chat_id=self.id,
            filename=attachment.guess_filename,
            content_type=attachment.guess_content_type,
            reply_no=reply_no,
            quote_range=quote_range,
        )

    @classmethod
    def load_chats(cls, client: Pararamio, ids: Sequence[int]) -> list[Chat]:
        url = f"/core/chat?ids={join_ids(ids)}"
        res = client.api_get(url)
        if res and "chats" in res:
            return [cls(client, **data) for data in client.api_get(url).get("chats", [])]
        raise PararamioRequestException(
            f"failed to load data for chats ids: {','.join(map(str, ids))}"
        )

    @classmethod
    def post_search(
        cls,
        client: Pararamio,
        q: str,
        *,
        order_type: str = "time",
        page: int = 1,
        chat_ids: list[int] | None = None,
        limit: int | None = POSTS_LIMIT,
    ) -> tuple[int, Iterable[Post]]:
        """
        Search for posts. Uses chat_ids parameter for chat filtering.
        Note: This endpoint is not in the official documentation but works in practice.
        """
        url = f"/posts/search?q={quote_plus(q)}"
        if order_type:
            url += f"&order_type={order_type}"
        if page:
            url += f"&page={page}"

        # API requires limit to be at least 10
        api_limit = max(limit or POSTS_LIMIT, 10) if limit else None
        if api_limit:
            url += f"&limit={api_limit}"

        # Handle chat_ids parameter if provided
        if chat_ids is not None:
            url += f"&chat_ids={','.join(map(str, chat_ids))}"

        res = client.api_get(url)
        if "posts" not in res:
            raise PararamioRequestException("failed to perform search")
        created_chats = {}

        def create_post(data):
            nonlocal created_chats
            _chat_id = data["thread_id"]
            post_no = data["post_no"]
            if _chat_id not in created_chats:
                created_chats[_chat_id] = cls(client, id=_chat_id)
            return Post(created_chats[_chat_id], post_no=post_no)

        posts = res["posts"]
        # Apply client-side limit if requested limit is less than API minimum (10)
        if limit and limit < 10 and limit < len(posts):
            posts = posts[:limit]

        return res["count"], map(create_post, posts)

    @classmethod
    def create(
        cls,
        client: Pararamio,
        title: str,
        *,
        description: str = "",
        users: list[int] | None = None,
        groups: list[int] | None = None,
        **kwargs,
    ) -> Chat:
        """

        Creates a new chat instance in the Pararamio application.

        Args:
            cls: The class itself (implicit first argument for class methods).
            client (Pararamio): An instance of the Pararamio client.
            title (str): The title of the chat.
            description (str, optional): A description of the chat. Default is an empty string.
            users (Optional[List[int]], optional): A list of user IDs to be added to the chat.
                                                   Default is None.
            groups (Optional[List[int]], optional): A list of group IDs to be added to the chat.
                                                    Default is None.
            **kwargs: Additional keyword arguments to be included in the chat creation data.

        Returns:
            Chat: An instance of the Chat class representing the newly created chat.
        """
        if users is None:
            users = []
        if groups is None:
            groups = []
        data = {
            "title": title,
            "description": description,
            "users": users,
            "groups": groups,
            **kwargs,
        }

        res = client.api_post("/core/chat", data)
        id_: int = res["chat_id"]
        return cls(client, id_)

    @classmethod
    def create_private_chat(cls, client: Pararamio, user_id: int) -> Chat:
        url = f"/core/chat/pm/{user_id}"
        res = client.api_post(url)
        id_: int = res["chat_id"]
        return cls(client, id=id_)

    @staticmethod
    def sync_chats(
        client: Pararamio,
        chats_ids: list[tuple[int, int, int]],
        sync_time: datetime | None = None,
    ) -> dict[str, Any]:
        url = "/core/chat/sync"
        data = {"ids": encode_chats_ids(chats_ids)}
        if sync_time:
            data["sync_time"] = format_datetime(sync_time)
        return client.api_post(url)
