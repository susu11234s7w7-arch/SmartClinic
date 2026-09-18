"""Pure reporting functions for SmartClinic records."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date

from .models import Appointment, Patient, Service


def summary_counts(
    patients: Iterable[Patient],
    appointments: Iterable[Appointment],
    services: Iterable[Service],
) -> dict[str, int]:
    """Return total counts for patients, appointments, and services."""
    return {
        "patients": sum(1 for _ in patients),
        "appointments": sum(1 for _ in appointments),
        "services": sum(1 for _ in services),
    }


def appointments_by_date(
    appointments: Iterable[Appointment],
) -> dict[date, list[Appointment]]:
    """Group appointments by their start-time calendar date."""
    grouped_appointments: dict[date, list[Appointment]] = {}
    for appointment in appointments:
        appointment_date = appointment.start_time.date()
        grouped_appointments.setdefault(appointment_date, []).append(appointment)
    return grouped_appointments


def service_usage(appointments: Iterable[Appointment]) -> dict[str, int]:
    """Count appointments for each service identifier."""
    usage_counts: dict[str, int] = {}
    for appointment in appointments:
        usage_counts[appointment.service_id] = (
            usage_counts.get(appointment.service_id, 0) + 1
        )
    return usage_counts