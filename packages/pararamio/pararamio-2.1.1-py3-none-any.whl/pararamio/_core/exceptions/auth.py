"""Authentication-specific exceptions."""

from __future__ import annotations

from typing import Any

from .base import PararamioException

__all__ = (
    'AuthenticationException',
    'CaptchaRequiredException',
    'InvalidCredentialsException',
    'RateLimitException',
    'SessionExpiredException',
    'TwoFactorFailedException',
    'TwoFactorRequiredException',
    'XSRFTokenException',
)


class AuthenticationException(PararamioException):
    """Base authentication exception."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        response_data: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.response_data = response_data or {}


class InvalidCredentialsException(AuthenticationException):
    """Invalid login credentials."""

    def __init__(self, message: str = 'Invalid email or password'):
        super().__init__(message, error_code='invalid_credentials')


class XSRFTokenException(AuthenticationException):
    """XSRF token related errors."""

    def __init__(self, message: str = 'XSRF token validation failed'):
        super().__init__(message, error_code='xsrf_token_error')


class TwoFactorRequiredException(AuthenticationException):
    """Two-factor authentication is required."""

    def __init__(self, message: str = 'Two-factor authentication required'):
        super().__init__(message, error_code='2fa_required')


class TwoFactorFailedException(AuthenticationException):
    """Two-factor authentication failed."""

    def __init__(self, message: str = 'Invalid two-factor authentication code'):
        super().__init__(message, error_code='2fa_failed')


class CaptchaRequiredException(AuthenticationException):
    """Captcha verification required."""

    def __init__(
        self,
        message: str = 'Captcha verification required',
        captcha_url: str | None = None,
    ):
        super().__init__(message, error_code='captcha_required')
        self.captcha_url = captcha_url


class RateLimitException(AuthenticationException):
    """Rate limit exceeded (429 Too Many Requests)."""

    def __init__(
        self,
        message: str = 'Rate limit exceeded',
        retry_after: int | None = None,
    ):
        super().__init__(message, error_code='rate_limit')
        self.retry_after = retry_after


class SessionExpiredException(AuthenticationException):
    """Session has expired."""

    def __init__(self, message: str = 'Session has expired, please authenticate again'):
        super().__init__(message, error_code='session_expired')
