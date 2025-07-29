from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Imports from core
from pararamio._core import PararamioValidationException
from pararamio._core.base import BasePararamObject

from .base import BaseClientObject

if TYPE_CHECKING:
    pass


class File(BasePararamObject, BaseClientObject):
    """
    File class is used to represent a file object in the Pararamio API.
    """

    _data: dict[str, Any]
    guid: str
    name: str
    mime_type: str
    size: int

    def __init__(self, client, guid: str, **kwargs):
        self._client = client
        self.guid = guid
        self._data = {**kwargs, "guid": guid}
        if "name" in kwargs:
            self._data["filename"] = kwargs["name"]

    def __str__(self):
        return self._data.get("filename", "")

    def serialize(self) -> dict[str, str]:
        """
        Serialize the object's data to a dictionary.

        Returns:
            Dict[str, str]: A dictionary representation of the object's data.
        """
        return self._data

    def delete(self):
        """

        delete()
            Deletes the file associated with the current instance.

            This method uses the client object to delete the file identified by its unique GUID.
        """
        self._client.delete_file(self.guid)

    def download(self, filename: str | None = None):
        """

        Downloads a file using the GUID associated with the client instance.

        Parameters:
        filename (Optional[str]): The name of the file to download.
                                  If not provided, the filename must be present in self._data.

        Raises:
        PararamioValidationException:
                 If the filename is not specified and 'filename' is not in self._data.
        """
        if filename is None and "filename" not in self._data:
            raise PararamioValidationException("can not determine filename")
        self._client.download_file(self.guid, filename or self._data["filename"])
