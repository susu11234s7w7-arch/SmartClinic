"""Core data models for SmartClinic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from .validation import (
    validate_date,
    validate_datetime,
    validate_identifier,
    validate_non_empty_name,
    validate_non_negative_decimal,
    validate_positive_integer,
)


@dataclass(frozen=True, slots=True)
class Patient:
    """A patient record without management operations."""

    patient_id: str
    name: str
    date_of_birth: date

    def __post_init__(self) -> None:
        validate_identifier(self.patient_id, "patient_id")
        validate_non_empty_name(self.name, "name")
        validate_date(self.date_of_birth, "date_of_birth")


@dataclass(frozen=True, slots=True)
class Service:
    """A clinic service definition."""

    service_id: str
    name: str
    duration_minutes: int
    price: Decimal

    def __post_init__(self) -> None:
        validate_identifier(self.service_id, "service_id")
        validate_non_empty_name(self.name, "name")
        validate_positive_integer(self.duration_minutes, "duration_minutes")
        validate_non_negative_decimal(self.price, "price")


@dataclass(frozen=True, slots=True)
class Appointment:
    """A time interval linking a patient to a service."""

    appointment_id: str
    patient_id: str
    service_id: str
    start_time: datetime
    end_time: datetime

    def __post_init__(self) -> None:
        validate_identifier(self.appointment_id, "appointment_id")
        validate_identifier(self.patient_id, "patient_id")
        validate_identifier(self.service_id, "service_id")
        validate_datetime(self.start_time, "start_time")
        validate_datetime(self.end_time, "end_time")
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")