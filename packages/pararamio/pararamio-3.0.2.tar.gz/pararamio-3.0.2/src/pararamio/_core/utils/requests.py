from __future__ import annotations

import codecs
import json
import logging
import mimetypes
from io import BytesIO
from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import HTTPCookieProcessor, Request, build_opener

from pararamio._core.constants import BASE_API_URL, FILE_UPLOAD_URL, UPLOAD_TIMEOUT, VERSION
from pararamio._core.constants import REQUEST_TIMEOUT as TIMEOUT
from pararamio._core.exceptions import PararamioHTTPRequestException

if TYPE_CHECKING:
    from http.client import HTTPResponse

    from pararamio._core._types import CookieJarT, HeaderLikeT

__all__ = (
    'api_request',
    'bot_request',
    'delete_file',
    'download_file',
    'raw_api_request',
    'upload_file',
    'xupload_file',
)
log = logging.getLogger('pararamio')
UA_HEADER = f'pararamio lib version {VERSION}'
DEFAULT_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'User-agent': UA_HEADER,
}
writer = codecs.lookup('utf-8')[3]


def multipart_encode(
    fd: BinaryIO,
    fields: list[tuple[str, str | None | int]] | None = None,
    boundary: str | None = None,
    form_field_name: str = 'data',
    filename: str | None = None,
    content_type: str | None = None,
) -> bytes:
    """
    Encodes a file and additional fields into a multipart/form-data payload.

    Args:
        fd: A file-like object opened in binary mode that is to be included in the payload.
        fields: An optional list of tuples representing additional form fields,
                with each tuple containing a field name and its value.
        boundary: An optional string used to separate parts of the multipart message.
                  If not provided, a default boundary ('FORM-BOUNDARY') is used.
        form_field_name: The name of the form field for the file being uploaded. Defaults to 'data'.
        filename: An optional string representing the filename for the file being uploaded.
                  If not provided, the name is derived from the file-like object.
        content_type: An optional string representing the content type of the file being uploaded.
                      If not provided, the content type will be guessed from the filename.

    Returns:
        A bytes' object representing the encoded multipart/form-data payload.
    """
    if fields is None:
        fields = []
    if boundary is None:
        boundary = 'FORM-BOUNDARY'
    body = BytesIO()

    def write(text: str):
        nonlocal body
        writer(body).write(text)

    if fields:
        for key, value in fields:
            if value is None:
                continue
            write(f'--{boundary}\r\n')
            write(f'Content-Disposition: form-data; name="{key}"')
            write(f'\r\n\r\n{value}\r\n')
    if not filename:
        filename = Path(fd.name).name
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    fd.seek(0)
    write(f'--{boundary}\r\n')
    write(f'Content-Disposition: form-data; name="{form_field_name}"; filename="{filename}"\r\n')
    write(f'Content-Type: {content_type}\r\n\r\n')
    body.write(fd.read())
    write(f'\r\n--{boundary}--\r\n\r\n')
    return body.getvalue()


def bot_request(
    url: str,
    key: str,
    method: str = 'GET',
    data: dict | None = None,
    headers: dict | None = None,
    timeout: int = TIMEOUT,
):
    """

    Sends a request to a bot API endpoint with the specified parameters.

    Parameters:
    url (str): The endpoint URL of the bot API.
    key (str): The API token for authentication.
    method (str): The HTTP method to use for the request. Defaults to 'GET'.
    data (Optional[dict]): The data payload for the request. Defaults to None.
    headers (Optional[dict]): Additional headers to include in the request. Defaults to None.
    timeout (int): The timeout setting for the request. Defaults to TIMEOUT.

    Returns:
    Response object from the API request.
    """
    _headers = {'X-APIToken': key, **DEFAULT_HEADERS}
    if headers:
        _headers = {**_headers, **headers}
    return api_request(url=url, method=method, data=data, headers=_headers, timeout=timeout)


def _base_request(
    url: str,
    method: str = 'GET',
    data: bytes | None = None,
    headers: dict | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = TIMEOUT,
) -> HTTPResponse:
    """
    Sends an HTTP request and returns an HTTPResponse object.

    Parameters:
        url (str): The URL endpoint to which the request is sent.
        method (str): The HTTP method to use for the request (default is 'GET').
        data (Optional[bytes]): The payload to include in the request body (default is None).
        headers (Optional[dict]): A dictionary of headers to include in the request
                                  (default is None).
        cookie_jar (Optional[CookieJarT]): A cookie jar to manage cookies for the request
                                           (default is None).
        timeout (int): The timeout for the request in seconds (TIMEOUT defines default).

    Returns:
        HTTPResponse: The response object containing the server's response to the HTTP request.

    Raises:
        PararamioHTTPRequestException: An exception is raised if there is
                                       an issue with the HTTP request.
    """
    _url = f'{BASE_API_URL}{url}'
    _headers = DEFAULT_HEADERS
    if headers:
        _headers = {**_headers, **headers}
    opener = build_opener(*[HTTPCookieProcessor(cookie_jar)] if cookie_jar is not None else [])
    _data = None
    if data:
        _data = data
    rq = Request(_url, _data, method=method, headers=_headers)
    log.debug('%s - %s - %s - %s - %s', _url, method, data, headers, cookie_jar)
    try:
        return opener.open(rq, timeout=timeout)
    except HTTPError as e:
        log.exception('%s - %s', _url, method)
        # noinspection PyUnresolvedReferences
        raise PararamioHTTPRequestException(e.filename, e.code, e.msg, e.hdrs, e.fp) from e


def _base_file_request(
    url: str,
    method='GET',
    data: bytes | None = None,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,  # type: ignore
    timeout: int = TIMEOUT,
) -> BytesIO:
    """
    Performs a file request to the specified URL with the given parameters.

    Arguments:
        url (str): The URL endpoint to send the request to.
        method (str, optional): The HTTP method to use for the request (default is 'GET').
        data (Optional[bytes], optional): The data to send in the request body (default is None).
        headers (Optional[HeaderLikeT], optional): The headers to include in the request
                                                   (default is None).
        cookie_jar (Optional[CookieJarT], optional): The cookie jar to use for managing cookies
                                                     (default is None).
        timeout (int, optional): The timeout duration for the request (default value is TIMEOUT).

    Returns:
        BytesIO: The response object from the file request.

    Raises:
        PararamioHTTPRequestException: If the request fails with an HTTP error code.
    """
    _url = f'{FILE_UPLOAD_URL}{url}'
    opener = build_opener(HTTPCookieProcessor(cookie_jar))
    if not headers:
        headers = {}
    rq = Request(_url, data, method=method, headers=headers)
    log.debug('%s - %s - %s - %s - %s', url, method, data, headers, cookie_jar)
    try:
        resp = opener.open(rq, timeout=timeout)
        if 200 >= resp.getcode() < 300:
            return resp
        raise PararamioHTTPRequestException(
            _url, resp.getcode(), 'Unknown error', resp.getheaders(), resp.fp
        )
    except HTTPError as e:
        log.exception('%s - %s', _url, method)
        # noinspection PyUnresolvedReferences
        raise PararamioHTTPRequestException(e.filename, e.code, e.msg, e.hdrs, e.fp) from e


def upload_file(
    fp: BinaryIO,
    perm: str,
    filename: str | None = None,
    file_type=None,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = UPLOAD_TIMEOUT,
):
    """
    Upload a file to a pararam server with specified permissions and optional parameters.

    Args:
        fp (BinaryIO): A file-like object to be uploaded.
        perm (str): The permission level for the uploaded file.
        filename (Optional[str], optional): Optional filename used during upload. Defaults to None.
        file_type (optional): Optional MIME type of the file. Defaults to None.
        headers (Optional[HeaderLikeT], optional): Optional headers to include in the request.
        Defaults to None.
        cookie_jar (Optional[CookieJarT], optional): Optional cookie jar for maintaining session.
        Defaults to None.
        timeout (int, optional): Timeout duration for the upload request.
        Defaults to UPLOAD_TIMEOUT.

    Returns:
        dict: A dictionary containing the server's response to the file upload.

    The function constructs a multipart form data request with the file contents,
    sends the POST request to the server,
    and returns the parsed JSON response from the server.
    """
    url = f'/upload/{perm}'
    boundary = 'FORM-BOUNDARY'
    _headers = {
        'User-agent': UA_HEADER,
        **(headers or {}),
        'Accept': 'application/json',
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    }
    data = multipart_encode(
        fp,
        boundary=boundary,
        form_field_name='file',
        filename=filename,
        content_type=file_type,
    )
    resp = _base_file_request(
        url,
        method='POST',
        data=data,
        headers=_headers,
        cookie_jar=cookie_jar,
        timeout=timeout,
    )
    return json.loads(resp.read())


def xupload_file(
    fp: BinaryIO,
    fields: list[tuple[str, str | None | int]],
    filename: str | None = None,
    content_type: str | None = None,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = UPLOAD_TIMEOUT,
) -> dict:
    """

    Uploads a file to a predefined URL using a multipart/form-data request.

    Arguments:
    - fp: A binary file-like object to upload.
    - fields: A list of tuples where each tuple contains a field name, z
     and a value which can be
    a string, None, or an integer.
    - filename: Optional; The name of the file being uploaded.
                If not provided, it defaults to None.
    - content_type: Optional; The MIME type of the file being uploaded.
                    If not provided, it defaults to None.
    - headers: Optional; Additional headers to include in the upload request.
               If not provided, defaults to None.
    - cookie_jar: Optional; A collection of cookies to include in the upload request.
                  If not provided, defaults to None.
    - timeout: Optional; The timeout in seconds for the request.
               Defaults to UPLOAD_TIMEOUT.

    Returns:
    - A dictionary parsed from the JSON response of the upload request.

    """
    url = '/upload'
    boundary = 'FORM-BOUNDARY'
    _headers = {
        'User-agent': UA_HEADER,
        **(headers or {}),
        'Accept': 'application/json',
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    }
    data = multipart_encode(
        fp,
        fields,
        filename=filename,
        content_type=content_type,
        boundary=boundary,
    )
    resp = _base_file_request(
        url,
        method='POST',
        data=data,
        headers=_headers,
        cookie_jar=cookie_jar,
        timeout=timeout,
    )
    return json.loads(resp.read())


def delete_file(
    guid: str,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = TIMEOUT,
) -> dict:
    url = f'/delete/{guid}'
    resp = _base_file_request(
        url, method='DELETE', headers=headers, cookie_jar=cookie_jar, timeout=timeout
    )
    return json.loads(resp.read())


def download_file(
    guid: str,
    filename: str,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = TIMEOUT,
) -> BytesIO:
    url = f'/download/{guid}/{quote(filename)}'
    return file_request(url, method='GET', headers=headers, cookie_jar=cookie_jar, timeout=timeout)


def file_request(
    url: str,
    method='GET',
    data: bytes | None = None,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = TIMEOUT,
) -> BytesIO:
    _headers = DEFAULT_HEADERS
    if headers:
        _headers = {**_headers, **headers}
    return _base_file_request(
        url,
        method=method,
        data=data,
        headers=_headers,
        cookie_jar=cookie_jar,
        timeout=timeout,
    )


def raw_api_request(
    url: str,
    method: str = 'GET',
    data: bytes | None = None,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = TIMEOUT,
) -> tuple[dict, list]:
    resp = _base_request(url, method, data, headers, cookie_jar, timeout)
    if 200 >= resp.getcode() < 300:
        contents = resp.read()
        return json.loads(contents), resp.getheaders()
    return {}, []


def api_request(
    url: str,
    method: str = 'GET',
    data: dict | None = None,
    headers: HeaderLikeT | None = None,
    cookie_jar: CookieJarT | None = None,
    timeout: int = TIMEOUT,
) -> dict:
    _data = None
    if data is not None:
        _data = str.encode(json.dumps(data), 'utf-8')
    resp = _base_request(url, method, _data, headers, cookie_jar, timeout)
    resp_code = resp.getcode()
    if resp_code == 204:
        return {}
    if 200 <= resp_code < 500:
        content = resp.read()
        try:
            return json.loads(content)
        except JSONDecodeError as e:
            log.exception('%s - %s', url, method)
            raise PararamioHTTPRequestException(
                url,
                resp.getcode(),
                'JSONDecodeError',
                resp.getheaders(),
                BytesIO(content),
            ) from e
    return {}
