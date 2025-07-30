from __future__ import annotations

import mimetypes
import os
from dataclasses import dataclass
from io import BufferedReader, BytesIO
from os import PathLike
from os.path import basename
from typing import BinaryIO

__all__ = ("Attachment",)


def guess_mime_type(filename: str | PathLike) -> str:
    if not mimetypes.inited:
        mimetypes.init(files=os.environ.get("PARARAMIO_MIME_TYPES_PATH", None))
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


@dataclass
class Attachment:
    file: str | bytes | PathLike | BytesIO | BinaryIO
    filename: str | None = None
    content_type: str | None = None

    @property
    def guess_filename(self) -> str:
        if self.filename:
            return self.filename
        if isinstance(self.file, (str, PathLike)):
            return basename(self.file)
        if isinstance(self.file, (BytesIO, BinaryIO, BufferedReader)):
            try:
                name = getattr(self.file, "name", None)
                if name:
                    return basename(name)
            except AttributeError:
                pass
        return "unknown"

    @property
    def guess_content_type(self) -> str:
        if self.content_type:
            return self.content_type
        if isinstance(self.file, (str, PathLike)):
            return guess_mime_type(self.file)
        if isinstance(self.file, (BinaryIO, BufferedReader)):
            if self.fp.name:
                return guess_mime_type(self.file.name)
        return "application/octet-stream"

    @property
    def fp(self) -> BytesIO | BinaryIO:
        if isinstance(self.file, bytes):
            return BytesIO(self.file)
        if isinstance(self.file, (str, PathLike)):
            with open(self.file, "rb") as f:
                return BytesIO(f.read())
        if isinstance(self.file, (BytesIO, BinaryIO, BufferedReader)):
            return self.file
        raise TypeError(f"Unsupported type {type(self.file)}")
