"""Common validators for pararamio models."""

from .exceptions import PararamioValidationException

__all__ = [
    'validate_filename',
    'validate_ids_list',
    'validate_post_load_range',
]


def validate_post_load_range(start_post_no: int, end_post_no: int) -> None:
    """
    Validate post loading range parameters.

    Args:
        start_post_no: Starting post number
        end_post_no: Ending post number

    Raises:
        PararamioValidationException: If range is invalid
    """
    if (start_post_no < 0 <= end_post_no) or (start_post_no >= 0 > end_post_no):
        msg = 'start_post_no and end_post_no can only be negative or positive at the same time'
        raise PararamioValidationException(msg)
    if 0 > start_post_no > end_post_no:
        msg = 'range start_post_no must be greater then end_post_no'
        raise PararamioValidationException(msg)
    if 0 <= start_post_no > end_post_no:
        msg = 'range start_post_no must be smaller then end_post_no'
        raise PararamioValidationException(msg)


def validate_filename(filename: str) -> None:
    """
    Validate filename for file uploads.

    Args:
        filename: Name of the file

    Raises:
        PararamioValidationException: If filename is invalid
    """
    if not filename or not filename.strip():
        msg = 'Filename cannot be empty'
        raise PararamioValidationException(msg)

    # Add more filename validation as needed
    forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in forbidden_chars:
        if char in filename:
            msg = f'Filename cannot contain character: {char}'
            raise PararamioValidationException(msg)


def validate_ids_list(ids: list, max_count: int = 100) -> None:
    """
    Validate list of IDs.

    Args:
        ids: List of IDs to validate
        max_count: Maximum allowed count

    Raises:
        PararamioValidationException: If IDs list is invalid
    """
    if not ids:
        msg = 'IDs list cannot be empty'
        raise PararamioValidationException(msg)

    if len(ids) > max_count:
        msg = f'Too many IDs, maximum {max_count} allowed'
        raise PararamioValidationException(msg)

    for id_val in ids:
        if not isinstance(id_val, int) or id_val <= 0:
            msg = f'Invalid ID: {id_val}. IDs must be positive integers'
            raise PararamioValidationException(msg)
