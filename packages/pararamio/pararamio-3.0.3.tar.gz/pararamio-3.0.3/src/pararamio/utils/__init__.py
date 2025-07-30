"""Utils package."""

# Re-export authentication utilities
from pararamio._core.utils.authentication import (
    authenticate,
    do_second_step,
    do_second_step_with_code,
    get_xsrf_token,
)

# Note: show_captcha was removed from core as it's an example function
# Re-export helper utilities
from pararamio._core.utils.helpers import (
    encode_digit,
    parse_iso_datetime,
    rand_id,
)

# Re-export request utilities
from pararamio._core.utils.requests import (
    api_request,
    raw_api_request,
)

__all__ = [
    # Authentication
    "authenticate",
    "do_second_step",
    "do_second_step_with_code",
    "get_xsrf_token",
    # Helpers
    "encode_digit",
    "parse_iso_datetime",
    "rand_id",
    # Requests
    "api_request",
    "raw_api_request",
]
