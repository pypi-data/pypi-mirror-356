"""Exceptions for pararamio package."""

from pararamio._core.exceptions import (
    PararamioAuthenticationException,
    PararamioCaptchaAuthenticationException,
    PararamioException,
    PararamioHTTPRequestException,
    PararamioPasswordAuthenticationException,
    PararamioRequestException,
    PararamioSecondFactorAuthenticationException,
    PararamioValidationException,
    PararamioXSFRRequestError,
    PararamModelNotLoaded,
    PararamNoNextPost,
    PararamNoPrevPost,
)

__all__ = [
    "PararamioException",
    "PararamioAuthenticationException",
    "PararamioCaptchaAuthenticationException",
    "PararamioPasswordAuthenticationException",
    "PararamioSecondFactorAuthenticationException",
    "PararamioXSFRRequestError",
    "PararamioHTTPRequestException",
    "PararamioRequestException",
    "PararamioValidationException",
    "PararamModelNotLoaded",
    "PararamNoPrevPost",
    "PararamNoNextPost",
]
