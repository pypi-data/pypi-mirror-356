"""Decorator for automatic authentication error handling with cookie manager."""

from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable, TypeVar

from .cookie_manager import (
    AsyncCookieManager,
    AsyncFileCookieManager,
    AsyncRedisCookieManager,
    CookieManager,
    FileCookieManager,
    RedisCookieManager,
)

log = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


async def _ensure_cookies_async(obj: Any, cookie_manager_attr: str) -> None:
    """Ensure cookies are loaded and refreshed for async operations."""
    cookie_manager = getattr(obj, cookie_manager_attr, None)
    if isinstance(cookie_manager, AsyncCookieManager):
        # Ensure cookies are loaded
        if not cookie_manager.has_cookies():
            await cookie_manager.load_cookies()
        # Check version and refresh if needed
        await cookie_manager.refresh_if_needed()


def _ensure_cookies_sync(obj: Any, cookie_manager_attr: str) -> None:
    """Ensure cookies are loaded and refreshed for sync operations."""
    cookie_manager = getattr(obj, cookie_manager_attr, None)
    if isinstance(cookie_manager, CookieManager):
        # Ensure cookies are loaded
        if not cookie_manager.has_cookies():
            cookie_manager.load_cookies()
        # Check version and refresh if needed
        cookie_manager.refresh_if_needed()


# List of error indicators for authentication failures
AUTH_ERROR_INDICATORS = ['401', 'unauthorized', 'authentication', 'auth failed']


def is_auth_error(error: Exception) -> bool:
    """Check if an exception is an authentication error."""
    error_str = str(error).lower()
    return any(indicator in error_str for indicator in AUTH_ERROR_INDICATORS)


def with_auth_retry(cookie_manager_attr: str = 'cookie_manager'):
    """Decorator to automatically handle authentication errors with cookie manager.

    Args:
        cookie_manager_attr: Name of the attribute containing the CookieManager instance

    Example:
        class MyClient:
            def __init__(self):
                self.cookie_manager = FileCookieManager('/path/to/cookies')

            @with_auth_retry()
            def make_api_call(self):
                # This will automatically retry with cookie refresh on auth errors
                return self._do_api_request()
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):
            # Async version
            @functools.wraps(func)
            async def async_wrapper(self, *args, **kwargs):
                cookie_manager = getattr(self, cookie_manager_attr, None)
                if not isinstance(cookie_manager, (CookieManager, AsyncCookieManager)):
                    # No cookie manager, just call the function
                    return await func(self, *args, **kwargs)

                try:
                    return await func(self, *args, **kwargs)
                except Exception as e:
                    # Check if this is an authentication error
                    if is_auth_error(e):
                        log.info('Authentication error in %s: %s', func.__name__, e)

                        # Create retry function
                        async def retry():
                            return await func(self, *args, **kwargs)

                        # Use cookie manager to handle the error
                        return await cookie_manager.handle_auth_error(retry)
                    # Not an auth error, re-raise
                    raise

            return async_wrapper

        # Sync version
        @functools.wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            cookie_manager = getattr(self, cookie_manager_attr, None)
            if not isinstance(cookie_manager, CookieManager):
                # No cookie manager, just call the function
                return func(self, *args, **kwargs)

            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Check if this is an authentication error
                if is_auth_error(e):
                    log.info('Authentication error in %s: %s', func.__name__, e)

                    # Create retry function
                    def retry():
                        return func(self, *args, **kwargs)

                    # Use cookie manager to handle the error
                    return cookie_manager.handle_auth_error(retry)
                # Not an auth error, re-raise
                raise

        return sync_wrapper

    return decorator


def auth_required(cookie_manager_attr: str = 'cookie_manager'):
    """Decorator that ensures cookies are loaded before method execution.

    Args:
        cookie_manager_attr: Name of the attribute containing the CookieManager instance

    Example:
        @auth_required()
        def get_profile(self):
            # Cookies will be loaded automatically if needed
            return self.api_get('/user/profile')
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):
            # Async version
            @functools.wraps(func)
            async def async_wrapper(self, *args, **kwargs):
                await _ensure_cookies_async(self, cookie_manager_attr)
                return await func(self, *args, **kwargs)

            return async_wrapper

        # Sync version
        @functools.wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            _ensure_cookies_sync(self, cookie_manager_attr)
            return func(self, *args, **kwargs)

        return sync_wrapper

    return decorator


class CookieManagerMixin:
    """Mixin class to add cookie manager support to any client class.

    Example:
        class MyAPIClient(CookieManagerMixin):
            def __init__(self, cookie_path: str):
                self.init_cookie_manager(cookie_path)

            @with_auth_retry()
            def get_data(self):
                return self.api_request('/data')
    """

    cookie_manager: CookieManager | AsyncCookieManager

    def init_cookie_manager(
        self,
        cookie_path: str | None = None,
        redis_client: Any = None,
        key_prefix: str = 'pararamio:cookies',
        use_async: bool = False,
    ):
        """Initialize cookie manager.

        Args:
            cookie_path: Path to cookie file (for file-based storage)
            redis_client: Redis client instance (for Redis-based storage)
            key_prefix: Redis key prefix
            use_async: Whether to use async cookie manager
        """
        if redis_client:
            # Use Redis-based manager
            if use_async:
                self.cookie_manager = AsyncRedisCookieManager(redis_client, key_prefix)
            else:
                self.cookie_manager = RedisCookieManager(redis_client, key_prefix)
        elif cookie_path:
            # Use file-based manager
            if use_async:
                self.cookie_manager = AsyncFileCookieManager(cookie_path)
            else:
                self.cookie_manager = FileCookieManager(cookie_path)
        else:
            msg = 'Either cookie_path or redis_client must be provided'
            raise ValueError(msg)
