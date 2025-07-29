from __future__ import annotations

import logging
import os
from http.cookiejar import CookieJar, FileCookieJar, MozillaCookieJar
from io import BytesIO
from typing import (
    Any,
    BinaryIO,
    Callable,
    Iterable,
    Sequence,
    cast,
)

# Imports from core
from pararamio._core import (
    XSRF_HEADER_NAME,
    CookieManager,
    InMemoryCookieManager,
    PararamioException,
    PararamioHTTPRequestException,
    PararamioValidationException,
)
from pararamio._core._types import ProfileTypeT, SecondStepFnT
from pararamio._core.exceptions import PararamioAuthenticationException
from pararamio._core.utils import (
    api_request,
    authenticate,
    delete_file,
    do_second_step,
    do_second_step_with_code,
    download_file,
    get_xsrf_token,
    xupload_file,
)
from pararamio._core.utils.helpers import (
    check_login_opts,
    get_empty_vars,
    lazy_loader,
    unescape_dict,
)

from .models import Chat, File, Group, Post, User, UserSearchResult

__all__ = ("Pararamio",)
log = logging.getLogger("pararamio.client")


class Pararamio:
    """Pararamio client class.

    This class provides a client interface for interacting with the Pararamio API.

    Parameters:
        login: Optional string for the login name.
        password: Optional string for the password.
        key: Optional string for an authentication key.
        cookie: Optional CookieJar object for handling cookies.
        cookie_manager: Optional CookieManager instance for cookie persistence.
        wait_auth_limit: Boolean flag to wait for rate limits instead of raising
            exception (default False).
    """

    _login: str | None
    _password: str | None
    _key: str | None
    _authenticated: bool
    _cookie: CookieJar | FileCookieJar
    _cookie_manager: CookieManager | None
    __profile: ProfileTypeT | None
    __headers: dict[str, str]
    __user: dict

    def __init__(
        self,
        login: str | None = None,
        password: str | None = None,
        key: str | None = None,
        *,
        cookie: CookieJar | None = None,
        cookie_manager: CookieManager | None = None,
        wait_auth_limit: bool = False,
    ):
        self._login = login
        self._password = password
        self._key = key
        self._wait_auth_limit = wait_auth_limit
        self.__headers = {}
        self.__profile = None
        self._authenticated = False
        self._cookie_manager = cookie_manager

        if cookie is not None:
            self._cookie = cookie
        elif cookie_manager is not None:
            # Use provided CookieManager
            self._cookie = MozillaCookieJar()

            # Load cookies through manager
            if self._cookie_manager and self._cookie_manager.load_cookies():
                self._cookie_manager.populate_jar(self._cookie)
                self._authenticated = True
                # Extract XSRF token
                for cj in self._cookie:
                    if cj.name == "_xsrf":
                        self.__headers[XSRF_HEADER_NAME] = str(cj.value)
                        break
            else:
                log.info("No existing cookies found, will authenticate on first request")
                self._authenticated = False
        else:
            # Use InMemoryCookieManager by default
            self._cookie_manager = InMemoryCookieManager()
            self._cookie = CookieJar()

        # If no XSRF token found in cookies, check if we have any cookies
        if not self.__headers.get(XSRF_HEADER_NAME) and self._cookie:
            for cj in self._cookie:
                if cj.name == "_xsrf":
                    self.__headers[XSRF_HEADER_NAME] = str(cj.value)
                    break

    def get_cookies(self) -> CookieJar | FileCookieJar:
        """
        Retrieve the cookie jar containing authentication cookies.

        Checks if the user is authenticated, and if not, performs the authentication process first.
        Once authenticated, returns the cookie jar.

        Returns:
            Union[CookieJar, FileCookieJar]: The cookie jar containing authentication cookies.
        """
        if not self._authenticated:
            self.authenticate()
        return self._cookie

    def get_headers(self) -> dict[str, str]:
        """
        Get the headers to be used in requests.

        Checks if the user is authenticated, performs authentication if not authenticated,
        and returns the headers.

        Returns:
            Dict[str, str]: The headers to be used in the request.
        """
        if not self._authenticated:
            self.authenticate()
        return self.__headers

    def _save_cookie(self) -> None:
        """
        _save_cookie:
            Saves the cookies in the FileCookieJar instance, if applicable.
            Ensures that cookies are saved persistently by ignoring the discard attribute.
        """
        if self._cookie_manager:
            # Update cookie manager with current cookies
            self._cookie_manager.update_from_jar(self._cookie)
            self._cookie_manager.save_cookies()
        elif isinstance(self._cookie, FileCookieJar):
            self._cookie.save(ignore_discard=True)

    def _profile(self, raise_on_error: bool = False) -> ProfileTypeT:
        """

        Fetches the user profile data from the API.

        Parameters:
        - raise_on_error (bool): If set to True, an error will be raised in case of a failure.
                                 Defaults to False.

        Returns:
        - ProfileTypeT: The unescaped user profile data retrieved from the API.

        """
        return cast(
            "ProfileTypeT",
            unescape_dict(
                self.api_get("/user/me", raise_on_error=raise_on_error),
                keys=["name"],
            ),
        )

    def _do_auth(
        self,
        login: str,
        password: str,
        cookie_jar: CookieJar,
        headers: dict[str, str],
        *,
        second_step_fn: SecondStepFnT,
        second_step_arg: str,
    ) -> None:
        """
        Authenticate the user and set the necessary headers for future requests.

        Args:
            login (str): The user's login name.
            password (str): The user's password.
            cookie_jar (CookieJar): The cookie jar to store cookies.
            headers (Dict[str, str]): The headers to be included in the request.
            second_step_fn (SecondStepFnT): The function to handle
                                            the second step of authentication if required.
            second_step_arg (str): An argument for the second step function.

        Returns:
            None

        Sets:
            self._authenticated (bool): True if authentication is successful, False otherwise.
            self.__headers[XSRF_HEADER_NAME] (str): The XSRF token if authentication is successful.
        """
        self._authenticated, _, xsrf = authenticate(
            login,
            password,
            cookie_jar,
            headers,
            second_step_fn=second_step_fn,
            second_step_arg=second_step_arg,
            wait_auth_limit=self._wait_auth_limit,
        )
        if self._authenticated:
            self.__headers[XSRF_HEADER_NAME] = xsrf
            self._save_cookie()

    def _authenticate(
        self,
        second_step_fn: SecondStepFnT,
        second_step_arg: str,
        login: str | None = None,
        password: str | None = None,
    ) -> bool:
        """
        Authenticate the user with the provided login and password,
        performing a secondary step if necessary.

        Arguments:
        second_step_fn: Function to execute for the second step of the authentication process
        second_step_arg: Argument to pass to the second step function
        login: Optional login name. If not provided,
               it will use login stored within the class instance.
        password: Optional password. If not provided,
                  it will use the password stored within the class instance.

        Returns:
        bool: True if authentication is successful, False otherwise

        Raises:
        PararamioAuthenticationException: If login or password is not provided or empty

        Exceptions:
        PararamioHTTPRequestException:
                        Raised if there is an error during the HTTP request in the profile check.

        """
        login = login or self._login or ""
        password = password or self._password or ""
        if not check_login_opts(login, password):
            raise PararamioAuthenticationException(
                f"{get_empty_vars(login=login, password=password)} must be set and not empty"
            )
        if not self._cookie:
            self._do_auth(
                login,
                password,
                self._cookie,
                self.__headers,
                second_step_fn=second_step_fn,
                second_step_arg=second_step_arg,
            )
        try:
            self._authenticated = True
            self._profile(raise_on_error=True)
        except PararamioHTTPRequestException:
            self._authenticated = False
            self._do_auth(
                login,
                password,
                self._cookie,
                self.__headers,
                second_step_fn=second_step_fn,
                second_step_arg=second_step_arg,
            )
        return self._authenticated

    def authenticate(
        self,
        login: str | None = None,
        password: str | None = None,
        key: str | None = None,
    ) -> bool:
        """
        Authenticate a user using either a login and password or a key.

        This method attempts to authenticate a user through provided login credentials
        or a predefined key. If the key is not provided, it will use the instance key
        stored in `self._key`.

        Args:
            login (str, optional): The user's login name. Defaults to None.
            password (str, optional): The user's password. Defaults to None.
            key (str, optional): A predefined key for authentication. Defaults to None.

        Returns:
            bool: True if authentication is successful, False otherwise.

        Raises:
            PararamioAuthenticationException: If no key is provided.

        """
        key = key or self._key
        if not key:
            raise PararamioAuthenticationException("key must be set and not empty")
        return self._authenticate(do_second_step, key, login, password)

    def authenticate_with_code(
        self,
        code: str,
        login: str | None = None,
        password: str | None = None,
    ) -> bool:
        """

        Authenticates a user using a provided code and optionally login and password.

        Parameters:
          code (str): The authentication code. Must be set and not empty.
          login (str, optional): The user login. Default is None.
          password (str, optional): The user password. Default is None.

        Returns:
          bool: True if authentication is successful, otherwise raises an exception.

        Raises:
          PararamioAuthenticationException: If the code is not provided or is empty.
        """
        if not code:
            raise PararamioAuthenticationException("code must be set and not empty")
        return self._authenticate(do_second_step_with_code, code, login, password)

    def _api_request(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        *,
        callback: Callable = lambda rsp: rsp,
        raise_on_error: bool = False,
    ) -> Any:
        """
        Performs an authenticated API request with XSRF token management and error handling.

        Args:
            url (str): The API endpoint URL to which the request is made.
            method (str): The HTTP method to use for the request. Defaults to 'GET'.
            data (Optional[dict]): The data payload for the request, if applicable.
                                   Defaults to None.
            callback (Callable): A callback function to process the response.
                                 Defaults to a lambda that returns the response.
            raise_on_error (bool): Flag to determine if exceptions should be raised.
                                   Defaults to False.

        Returns:
            Any: The result of the callback processing on the API request response.

        Raises:
            PararamioHTTPRequestException:
                                         If an HTTP error occurs and raise_on_error is set to True.

        Notes:
            - The function ensures that the user is authenticated before making the request.
            - Manages the XSRF token by retrieving and saving it as needed.
            - Handles specific error cases by attempting re-authentication or
              renewing the XSRF token.
        """
        if not self._authenticated:
            self.authenticate()
        if not self.__headers.get(XSRF_HEADER_NAME, None):
            self.__headers[XSRF_HEADER_NAME] = get_xsrf_token(self._cookie)
            self._save_cookie()
        try:
            return callback(
                api_request(
                    url, method=method, data=data, cookie_jar=self._cookie, headers=self.__headers
                )
            )
        except PararamioHTTPRequestException as e:
            if raise_on_error:
                raise
            if e.code == 401:
                # Authentication error - use cookie manager if available
                if self._cookie_manager:

                    def retry():
                        self._authenticated = False
                        return self._api_request(
                            url=url,
                            method=method,
                            data=data,
                            callback=callback,
                            raise_on_error=True,
                        )

                    return self._cookie_manager.handle_auth_error(retry)
                # Fallback to old behavior
                self._authenticated = False
                return self._api_request(
                    url=url,
                    method=method,
                    data=data,
                    callback=callback,
                    raise_on_error=True,
                )
            message = e.message
            if message == "xsrf":
                log.info("xsrf is expire, invalid or was not set, trying to get new one")
                self.__headers[XSRF_HEADER_NAME] = ""
                return self._api_request(
                    url=url,
                    method=method,
                    data=data,
                    callback=callback,
                    raise_on_error=True,
                )
            raise

    def api_get(self, url: str, raise_on_error: bool = False) -> dict:
        """

        Handles HTTP GET requests to the specified API endpoint.

        Arguments:
        url (str): The URL of the API endpoint.

        raise_on_error (bool): If set to True, an exception will be raised
                               if the API response indicates an error. Defaults to False.

        Returns:
        dict: The JSON response from the API, parsed into a Python dictionary.

        """
        return self._api_request(url, raise_on_error=raise_on_error)

    def api_post(
        self,
        url: str,
        data: dict[Any, Any] | None = None,
        raise_on_error: bool = False,
    ) -> dict:
        """
        Sends a POST request to the specified URL with the given data.

        Parameters:
        url (str): The endpoint URL where the POST request should be sent.
        data (Optional[Dict[Any, Any]], optional): The payload to be sent in the POST request body.
                                                   Defaults to None.
        raise_on_error (bool, optional): Whether to raise an exception if the request fails.
                                         Defaults to False.

        Returns:
        dict: The response from the server as a dictionary.
        """
        return self._api_request(url, method="POST", data=data, raise_on_error=raise_on_error)

    def api_put(
        self,
        url: str,
        data: dict[Any, Any] | None = None,
        raise_on_error: bool = False,
    ) -> dict:
        """
        Sends a PUT request to the specified URL with the provided data.

        Parameters:
        - url: The URL to send the PUT request to.
        - data: Optional dictionary containing the data to include in the request body.
        - raise_on_error: Boolean flag indicating whether to raise an exception
                          if the request results in an error.

        Returns:
        A dictionary containing the server's response to the PUT request.
        """
        return self._api_request(url, method="PUT", data=data, raise_on_error=raise_on_error)

    def api_delete(
        self,
        url: str,
        data: dict[Any, Any] | None = None,
        raise_on_error: bool = False,
    ) -> dict:
        """
        Sends a DELETE request to the specified URL with optional data.

        Parameters:
        url (str): The URL to send the DELETE request to.
        data (Optional[Dict[Any, Any]], optional): Optional payload to include in the request.
        raise_on_error (bool, optional): Determines whether an exception should be raised
                                         on request failure.

        Returns:
        dict: The response from the API request.
        """
        return self._api_request(url, method="DELETE", data=data, raise_on_error=raise_on_error)

    def _upload_file(
        self,
        file: BinaryIO | BytesIO,
        chat_id: int,
        *,
        filename: str | None = None,
        type_: str | None = None,
        organization_id: int | None = None,
        reply_no: int | None = None,
        quote_range: str | None = None,
    ) -> tuple[dict, dict]:
        """
        _upload_file is a method for uploading a file to a specified chat or organization.

        Arguments:
            file: A binary stream of the file to be uploaded.
            chat_id: The ID of the chat where the file will be uploaded.
            filename: An optional parameter that specifies the name of the file.
            type_: An optional parameter that specifies the type of file being uploaded.
                   If not provided, it will be inferred from the filename.
            organization_id: An optional parameter that specifies the ID of the organization
                             if the file is an organization avatar.
            reply_no: An optional parameter that specifies the reply number
                      associated with the file.
            quote_range: An optional parameter that specifies the range
                         of quotes associated with the file.

        Returns:
            A tuple containing a dictionary with the response from the xupload_file function
            and a dictionary of the fields used during the upload.

        Raises:
            PararamioValidationException: If filename is not set when type is None,
            or if organization_id is not set when type is organization_avatar,
            or if chat_id is not set when type is chat_avatar.

        Notes:
            This method ensures that the necessary headers and
            tokens are set before attempting the file upload.
        """
        if type_ is None and not filename:
            raise PararamioValidationException("filename must be set when type is None")
        if not self._authenticated:
            self.authenticate()
        if not self.__headers.get(XSRF_HEADER_NAME, None):
            self.__headers[XSRF_HEADER_NAME] = get_xsrf_token(self._cookie)
        if type_ == "organization_avatar" and organization_id is None:
            raise PararamioValidationException(
                "organization_id must be set when type is organization_avatar"
            )
        if type_ == "chat_avatar" and chat_id is None:
            raise PararamioValidationException("chat_id must be set when type is chat_avatar")
        content_type = None
        if type_ not in ("organization_avatar", "chat_avatar"):
            content_type = type_
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0, 0)
        fields: list[tuple[str, str | int | None]] = [
            ("type", type_),
            ("filename", filename),
            ("size", file_size),
            ("chat_id", chat_id),
            ("organization_id", organization_id),
            ("reply_no", reply_no),
            ("quote_range", quote_range),
        ]
        return xupload_file(
            fp=file,
            fields=fields,
            filename=filename,
            content_type=content_type,
            headers=self.__headers,
            cookie_jar=self._cookie,
        ), dict(fields)

    def upload_file(
        self,
        file: str | BytesIO | BinaryIO | os.PathLike,
        chat_id: int,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        reply_no: int | None = None,
        quote_range: str | None = None,
    ) -> File:
        """
        upload_file uploads a file to a specified chat.

        Parameters:
        file: Union[str, BytesIO, os.PathLike] The file to be uploaded. It can be a file path,
              a BytesIO object, or an os.PathLike object.
        chat_id: int
            The ID of the chat where the file should be uploaded.
        filename: Optional[str]
            The name of the file.
            If not specified and the file is a path, the basename of the file path will be used.
        content_type: Optional[str]
            The MIME type of the file.
        reply_no: Optional[int]
            The reply number in the chat to which this file is in response.
        quote_range: Optional[str]
            The range of messages being quoted.

        Returns:
        File
            An instance of the File class representing the uploaded file.
        """
        if isinstance(file, (str, os.PathLike)):
            filename = filename or os.path.basename(file)
            with open(file, "rb") as f:
                res, extra = self._upload_file(
                    f,
                    chat_id,
                    filename=filename,
                    type_=content_type,
                    reply_no=reply_no,
                    quote_range=quote_range,
                )
        else:
            res, extra = self._upload_file(
                file,
                chat_id,
                filename=filename,
                type_=content_type,
                reply_no=reply_no,
                quote_range=quote_range,
            )
        return File(self, guid=res["guid"], mime_type=extra["type"], **extra)

    def delete_file(self, guid: str) -> dict:
        """
        Deletes a file identified by the provided GUID.

        Args:
            guid (str): The globally unique identifier of the file to be deleted.

        Returns:
            dict: The result of the deletion operation.

        """
        return delete_file(guid, headers=self.__headers, cookie_jar=self._cookie)

    def download_file(self, guid: str, filename: str) -> BytesIO:
        """
        Downloads and returns a file as a BytesIO object given its unique identifier and filename.

        Args:
            guid (str): The unique identifier of the file to be downloaded.
            filename (str): The name of the file to be downloaded.

        Returns:
            BytesIO: A BytesIO object containing the downloaded file content.
        """
        return download_file(guid, filename, headers=self.__headers, cookie_jar=self._cookie)

    def get_profile(self) -> ProfileTypeT:
        """
        Get the user profile.

        If the profile is not yet initialized, this method will initialize it by calling the
        _profile method.

        Returns:
            ProfileTypeT: The profile object.
        """
        if not self.__profile:
            self.__profile = self._profile()
        return self.__profile

    def search_users(self, query: str, include_self: bool = False) -> list[UserSearchResult]:
        """Search for users based on the given query string.

        Parameters:
        query (str): The search query used to find matching users.
        include_self (bool): Whether to include current user in results. Default is False.

        Returns:
        List[UserSearchResult]: A list of User objects that match the search query.
        """
        return User.search(self, query, include_self)

    def search_groups(self, query: str) -> list[Group]:
        """Search for groups based on a given query string.

        Note: This uses the user search endpoint which also returns groups.

        Arguments:
        query (str): The search term used to find matching groups.

        Returns:
        List[Group]: A list of Group objects that match the search criteria.
        """
        return Group.search(self, query)

    def search_posts(
        self,
        query: str,
        *,
        order_type: str = "time",
        page: int = 1,
        chat_ids: list[int] | None = None,
        limit: int | None = None,
    ) -> tuple[int, Iterable[Post]]:
        """

        search_posts searches for posts based on a given query and various optional parameters.

        Arguments:
        - query: The search term used to find posts.
        - order_type: Specifies the order of the search results. Default is 'time'.
        - page: The page number of the search results to retrieve. Default is 1.
        - chat_ids: Optional list of chat IDs to search within. If None, search in all chats.
        - limit: The maximum number of posts to return. If None, use the default limit.

        Returns:
        - A tuple containing the total number of posts matching
          the search query and an iterable of Post objects.
        """
        return Chat.post_search(
            self, query, order_type=order_type, page=page, chat_ids=chat_ids, limit=limit
        )

    def list_chats(self) -> Iterable[Chat]:
        """
        Returns iterable that yields chat objects in a lazy-loading manner.
        The chats are fetched from the server using the specified URL and are returned in batches.

        Returns:
            Iterable: An iterable that yields chat objects.
        """
        url = "/core/chat/sync"
        chats_per_load = 50
        ids = self.api_get(url).get("chats", [])
        return lazy_loader(self, ids, Chat.load_chats, per_load=chats_per_load)

    def get_groups_by_ids(self, ids: Sequence[int], load_per_request: int = 100) -> Iterable[Group]:
        """
        Fetches groups by their IDs in a lazy-loading manner.

        This method allows fetching large numbers of groups by their IDs, utilizing a
        lazy-loading technique which loads the data in smaller chunks to avoid high
        memory consumption.

        Parameters:
            ids (Sequence[int]): A sequence of group IDs to fetch.
            load_per_request (int): The number of groups to load per request. Defaults
                to 100.

        Returns:
            Iterable[Group]: An iterable of Group objects fetched in chunks using the
            lazy loader.
        """
        return lazy_loader(self, ids, Group.load_groups, per_load=load_per_request)

    def get_users_by_ids(self, ids: Sequence[int], load_per_request: int = 100) -> Iterable[User]:
        """
        Returns an iterable for lazily loading User objects based on a list of
        user IDs. Uses `User.load_users` method to load users in chunks.

        Parameters:
        ids (Sequence[int]): A sequence of user IDs for which User objects need to
            be loaded.
        load_per_request (int): The number of users to load per request.
        maximum 100.

        Returns:
        Iterable[User]: A lazy iterable that provides the loaded User objects.
        """
        return lazy_loader(self, ids, User.load_users, per_load=load_per_request)

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None if not found
        """
        try:
            users = list(self.get_users_by_ids([user_id]))
            return users[0] if users else None
        except (PararamioException, IndexError, KeyError):
            return None

    def get_chat_by_id(self, chat_id: int) -> Chat | None:
        """Get chat by ID.

        Args:
            chat_id: Chat ID

        Returns:
            Chat object or None if not found
        """
        try:
            # Direct instantiation since we know the ID
            chat = Chat(self, chat_id)
            # Try to load chat data to verify it exists
            chat.load()
            return chat
        except (PararamioException, IndexError, KeyError):
            return None

    def get_group_by_id(self, group_id: int) -> Group | None:
        """Get group by ID.

        Args:
            group_id: Group ID

        Returns:
            Group object or None if not found
        """
        try:
            groups = list(self.get_groups_by_ids([group_id]))
            return groups[0] if groups else None
        except (PararamioException, IndexError, KeyError):
            return None

    def create_chat(self, name: str, description: str | None = None) -> Chat:
        """Create a new chat.

        Args:
            name: Chat name
            description: Optional chat description

        Returns:
            Created Chat object
        """
        return Chat.create(self, name, description=description or "")

    def post_private_message_by_user_email(self, email: str, text: str) -> Post:
        """

        Posts a private message to a user identified by their email address.

        :param email: The email address of the user to whom the message will be sent.
        :type email: str
        :param text: The content of the message to be posted.
        :type text: str
        :return: A Post object representing the posted message.
        :rtype: Post
        """
        url = "/msg/post/private"
        resp = self._api_request(url, method="POST", data={"text": text, "user_email": email})
        return Post(Chat(self, resp["chat_id"]), resp["post_no"])

    def post_private_message_by_user_id(self, user_id: int, text: str) -> Post:
        """
        Send a private message to a specific user.

        Parameters:
        user_id (int): The ID of the user to whom the message will be sent.
        text (str): The content of the message to be sent.

        Returns:
        Post: The Post object containing information about the scent message.
        """
        url = "/msg/post/private"
        resp = self._api_request(url, method="POST", data={"text": text, "user_id": user_id})
        return Post(Chat(self, resp["chat_id"]), resp["post_no"])

    def post_private_message_by_user_unique_name(self, unique_name: str, text: str) -> Post:
        """
        Post a private message to a user identified by their unique name.

        Parameters:
        unique_name (str): The unique name of the user to whom the private message is to be sent.
        text (str): The content of the private message.

        Returns:
        Post: An instance of the Post class representing the posted message.
        """
        url = "/msg/post/private"
        resp = self._api_request(
            url, method="POST", data={"text": text, "user_unique_name": unique_name}
        )
        return Post(Chat(self, resp["chat_id"]), resp["post_no"])

    def mark_all_messages_as_read(self, org_id: int | None = None) -> bool:
        """

        Marks all messages as read for the organization or everywhere if org_id is None.

        Parameters:
        org_id (Optional[int]): The ID of the organization. This parameter is optional.

        Returns:
        bool: True if the operation was successful, False otherwise.
        """
        url = "/msg/lastread/all"
        data = {}
        if org_id is not None:
            data["org_id"] = org_id
        return self.api_post(url, data=data).get("result", None) == "OK"
