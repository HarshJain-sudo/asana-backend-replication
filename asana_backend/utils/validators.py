"""
Utility functions for validation.
"""
import re
import uuid
from typing import Optional
from django.core.exceptions import ValidationError


def validate_uuid(value: str) -> uuid.UUID:
    """
    Validate UUID string and return UUID object.
    Raises ValidationError if invalid.
    """
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid UUID format: {value}")


def validate_hex_color(value: Optional[str]) -> Optional[str]:
    """
    Validate hex color format (#RRGGBB or #RRGGBBAA).
    Returns None if value is None or empty.
    """
    if not value:
        return None

    value = value.strip()
    if not value.startswith('#'):
        raise ValidationError(
            f"Color must start with #: {value}"
        )

    # Remove # and validate hex
    hex_value = value[1:]
    if len(hex_value) not in [6, 8]:
        raise ValidationError(
            f"Color must be 6 or 8 hex digits: {value}"
        )

    if not re.match(r'^[0-9A-Fa-f]+$', hex_value):
        raise ValidationError(
            f"Color contains invalid hex characters: {value}"
        )

    return value.upper()


def validate_pagination_params(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    max_limit: int = 100
) -> tuple[int, int]:
    """
    Validate and normalize pagination parameters.
    Returns (offset, limit) tuple.
    Raises ValidationError for invalid values.
    """
    if offset is None:
        offset = 0
    else:
        try:
            offset = int(offset)
            if offset < 0:
                raise ValidationError(
                    f"Offset must be >= 0, got: {offset}"
                )
        except (ValueError, TypeError) as e:
            raise ValidationError(
                f"Offset must be a valid integer, got: {offset}"
            )

    if limit is None:
        limit = 50
    else:
        try:
            limit = int(limit)
            if limit < 1:
                raise ValidationError(
                    f"Limit must be >= 1, got: {limit}"
                )
            elif limit > max_limit:
                raise ValidationError(
                    f"Limit must be <= {max_limit}, got: {limit}"
                )
        except (ValueError, TypeError) as e:
            if not isinstance(e, ValidationError):
                raise ValidationError(
                    f"Limit must be a valid integer, got: {limit}"
                )
            raise

    return (offset, limit)


def validate_date_range(
    start_date: Optional[str],
    end_date: Optional[str],
    start_field_name: str = "start_date",
    end_field_name: str = "end_date"
) -> None:
    """
    Validate that end_date >= start_date if both are provided.
    """
    if start_date and end_date:
        from datetime import datetime
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            if end < start:
                raise ValidationError(
                    f"{end_field_name} must be >= {start_field_name}"
                )
        except ValueError:
            # If dates are not in ISO format, skip validation
            # (Django will handle format validation)
            pass

