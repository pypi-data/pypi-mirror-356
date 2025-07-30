"""Cookie managers for synchronous Pararamio client."""

from pararamio._core.cookie_manager import (
    CookieManager,
    FileCookieManager,
    InMemoryCookieManager,
    RedisCookieManager,
)

__all__ = [
    "CookieManager",
    "FileCookieManager",
    "InMemoryCookieManager",
    "RedisCookieManager",
]
