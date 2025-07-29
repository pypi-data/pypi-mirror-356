from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio._core import (
    PararamioRequestException,
    PararamioServerResponseException,
    PararamioValidationException,
)
from pararamio._core.base import BaseLoadedAttrPararamObject

from .base import BaseClientObject

if TYPE_CHECKING:
    from ..client import Pararamio
    from .chat import Chat

__all__ = ("Poll",)


class PollOption:
    """Represents a poll option object."""

    id: int
    text: str
    count: int
    vote_users: list[int]

    def __init__(self, id: int, text: str, count: int, vote_users: list[int]) -> None:
        self.id = id
        self.text = text
        self.count = count
        self.vote_users = vote_users

    @classmethod
    def from_response_data(cls, data: dict[str, Any]) -> PollOption:
        """

        Creates an instance of PollOption from the provided response data.

        Args:
            data (Dict[str, Any]): The response data containing poll option information.

        Raises:
            PararamioServerResponseException: If any expected field is missing in the response data.

        Returns:
            PollOption: An instance of PollOption initialized with the response data.
        """
        for field in cls.__annotations__:  # pylint: disable=E1101
            if field not in data:
                raise PararamioServerResponseException(
                    f"invalid server vote option response, missing {field}",
                    data,
                )
        return cls(**data)


class Poll(BaseLoadedAttrPararamObject, BaseClientObject):
    """
    Represents a poll object.
    """

    _data: dict[str, Any]

    vote_uid: str
    chat_id: int
    anonymous: bool
    mode: str
    options: list[PollOption]
    question: str
    total_user: int
    total_answer: int
    user_id: int

    def __init__(
        self,
        client: Pararamio,
        vote_uid: str,
        load_on_key_error: bool = True,
        **kwargs: Any,
    ) -> None:
        self._client = client
        self.vote_uid = vote_uid
        self._data = {**kwargs, "vote_uid": vote_uid}
        self._load_on_key_error = load_on_key_error

    def __str__(self) -> str:
        return self.question

    def _update(self, response: dict[str, Any]) -> Poll:
        """
        Update the Poll object with the response data.

        :param response: A dictionary containing the response data.
        :type response: Dict[str, Any]
        :return: The updated Poll object.
        :rtype: Poll
        :raises PararamioServerResponseException: If 'vote' key is not present in the response.
        """
        if "vote" not in response:
            raise PararamioServerResponseException(
                f"failed to load data for vote {self.vote_uid} in chat {self.chat_id}",
                response,
            )
        self._data = {
            k: v if k != "options" else [PollOption.from_response_data(opt) for opt in v]
            for k, v in response["vote"].items()
        }
        return self

    def load(self) -> Poll:
        """
        Load the poll's data from the pararam server.

        :return: The updated instance of the poll.
        :rtype: Poll
        """
        res = self._client.api_get(f"/msg/vote/{self.vote_uid}")
        return self._update(res)

    @classmethod
    def create(
        cls, chat: Chat, question: str, *, mode: str, anonymous: bool, options: list[str]
    ) -> Poll:
        """
        Create a new poll in the specified pararam chat.

        :param chat: The chat in which the poll will be created.
        :type chat: Chat
        :param question: The question for the poll.
        :type question: str
        :param mode: Options select mode of the poll ('one' for single or 'more' for multi).
        :type mode: str
        :param anonymous: Whether the poll should be anonymous or not.
        :type anonymous: bool
        :param options: The list of options for the poll.
        :type options: List[str]
        :return: The created Poll object.
        :rtype: Poll
        :raises PararamioRequestException: If the request to create the poll fails.
        """
        res = chat.client.api_post(
            "/msg/vote",
            {
                "chat_id": chat.id,
                "question": question,
                "options": options,
                "mode": mode,
                "anonymous": anonymous,
            },
        )
        if not res:
            raise PararamioRequestException("Failed to create post")
        return cls(chat.client, res["vote_uid"]).load()

    def _vote(self, option_ids: list[int]) -> Poll:
        """
        Vote on the poll by selecting the given option IDs.

        :param option_ids: A list of integers representing the IDs of the options to vote for.
        :type option_ids: List[int]
        :return: The updated Poll object after voting.
        :rtype: Poll
        :raises PararamioValidationException: If any of the option IDs are incorrect.
        """
        ids_ = [opt.id for opt in self.options]
        if not all(opt_id in ids_ for opt_id in option_ids):
            raise PararamioValidationException("incorrect option")
        res = self._client.api_put(
            f"/msg/vote/{self.vote_uid}",
            {
                "variants": option_ids,
            },
        )
        return self._update(res)

    def vote(self, option_id: int) -> Poll:
        """
        Vote for a specific option in the poll.

        :param option_id: The ID of the option to vote for.
        :type option_id: int
        :return: The updated Poll object after voting.
        :rtype: Poll
        :raises PararamioValidationException: If the option_id is invalid.
        """
        return self._vote([option_id])

    def vote_multi(self, option_ids: list[int]) -> Poll:
        """
        Vote for multiple options in a poll.

        :param option_ids: A list of integers representing the IDs of the options to vote for.
        :type option_ids: List[int]
        :return: The updated instance of the poll.
        :rtype: Poll
        :raises PararamioValidationException: If the poll mode is not 'more' or
                                              if any of the option IDs are incorrect.
        """
        if self.mode != "more":
            raise PararamioValidationException(
                f"incorrect poll mode ({self.mode}) for multi voting"
            )
        return self._vote(option_ids)

    def retract(self) -> Poll:
        """
        Retracts the vote from the poll.

        :return: The updated instance of the poll.
        :rtype: Poll
        """
        return self._vote([])
