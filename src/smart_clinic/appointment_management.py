"""In-memory management operations for appointment records."""

from __future__ import annotations

from collections.abc import Iterable

from .models import Appointment
from .validation import validate_identifier


class AppointmentAlreadyExistsError(ValueError):
    """Raised when an appointment identifier is already registered."""


class AppointmentNotFoundError(LookupError):
    """Raised when a requested appointment does not exist."""


class AppointmentConflictError(ValueError):
    """Raised when an appointment overlaps another appointment for a patient."""


class AppointmentManager:
    """Manage validated appointments in memory."""

    def __init__(self, appointments: Iterable[Appointment] = ()) -> None:
        self._appointments: dict[str, Appointment] = {}
        for appointment in appointments:
            self.add_appointment(appointment)

    def add_appointment(self, appointment: Appointment) -> Appointment:
        """Add an appointment unless its ID or time slot conflicts."""
        self._require_appointment(appointment)
        if appointment.appointment_id in self._appointments:
            raise AppointmentAlreadyExistsError(
                f"appointment '{appointment.appointment_id}' already exists"
            )
        self._ensure_no_conflict(appointment)
        self._appointments[appointment.appointment_id] = appointment
        return appointment

    def get_appointment(self, appointment_id: str) -> Appointment:
        """Return an appointment by ID or raise ``AppointmentNotFoundError``."""
        validated_id = self._validate_appointment_id(appointment_id)
        try:
            return self._appointments[validated_id]
        except KeyError as error:
            raise AppointmentNotFoundError(
                f"appointment '{validated_id}' was not found"
            ) from error

    def list_appointments(self) -> list[Appointment]:
        """Return all appointments in insertion order."""
        return list(self._appointments.values())

    def get_patient_appointments(self, patient_id: str) -> list[Appointment]:
        """Return appointments belonging to a patient in insertion order."""
        validated_id = validate_identifier(patient_id, "patient_id")
        return [
            appointment
            for appointment in self._appointments.values()
            if appointment.patient_id == validated_id
        ]

    def update_appointment(self, appointment: Appointment) -> Appointment:
        """Replace an existing appointment after conflict validation."""
        self._require_appointment(appointment)
        self.get_appointment(appointment.appointment_id)
        self._ensure_no_conflict(appointment, ignore_id=appointment.appointment_id)
        self._appointments[appointment.appointment_id] = appointment
        return appointment

    def delete_appointment(self, appointment_id: str) -> Appointment:
        """Delete and return an appointment by ID."""
        validated_id = self._validate_appointment_id(appointment_id)
        try:
            return self._appointments.pop(validated_id)
        except KeyError as error:
            raise AppointmentNotFoundError(
                f"appointment '{validated_id}' was not found"
            ) from error

    def _ensure_no_conflict(
        self, appointment: Appointment, ignore_id: str | None = None
    ) -> None:
        for existing_appointment in self._appointments.values():
            if existing_appointment.appointment_id == ignore_id:
                continue
            if self._appointments_conflict(existing_appointment, appointment):
                raise AppointmentConflictError(
                    f"appointment conflicts with '{existing_appointment.appointment_id}'"
                )

    @staticmethod
    def _appointments_conflict(
        first: Appointment, second: Appointment
    ) -> bool:
        if first.patient_id != second.patient_id:
            return False
        return (
            first.start_time < second.end_time
            and second.start_time < first.end_time
        )

    @staticmethod
    def _require_appointment(appointment: Appointment) -> None:
        if not isinstance(appointment, Appointment):
            raise TypeError("appointment must be an Appointment instance")

    @staticmethod
    def _validate_appointment_id(appointment_id: str) -> str:
        return validate_identifier(appointment_id, "appointment_id")