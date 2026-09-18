"""Validation helpers for SmartClinic data models."""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal


_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def validate_identifier(value: str, field_name: str = "identifier") -> str:
    """Return a valid identifier or raise ``ValueError``."""
    if not isinstance(value, str) or not value or not _IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(
            f"{field_name} must contain only letters, numbers, underscores, or hyphens"
        )
    return value


def validate_non_empty_name(value: str, field_name: str = "name") -> str:
    """Return a trimmed non-empty name or raise ``ValueError``."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be empty")
    return value.strip()


def validate_date(value: date, field_name: str = "date") -> date:
    """Return a date value, excluding datetimes, or raise ``ValueError``."""
    if not isinstance(value, date) or isinstance(value, datetime):
        raise ValueError(f"{field_name} must be a valid date")
    return value


def validate_datetime(value: datetime, field_name: str = "datetime") -> datetime:
    """Return a datetime value or raise ``ValueError``."""
    if not isinstance(value, datetime):
        raise ValueError(f"{field_name} must be a valid datetime")
    return value


def validate_positive_integer(value: int, field_name: str) -> int:
    """Return a positive integer or raise ``ValueError``."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")
    return value


def validate_non_negative_decimal(value: Decimal, field_name: str) -> Decimal:
    """Return a non-negative Decimal or raise ``ValueError``."""
    if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
        raise ValueError(f"{field_name} must be a finite, non-negative Decimal")
    return value
