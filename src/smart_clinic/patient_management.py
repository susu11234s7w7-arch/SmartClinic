"""In-memory management operations for patient records."""

from __future__ import annotations

from collections.abc import Iterable

from .models import Patient
from .validation import validate_identifier


class PatientAlreadyExistsError(ValueError):
    """Raised when a patient identifier is already registered."""


class PatientNotFoundError(LookupError):
    """Raised when a requested patient does not exist."""


class PatientManager:
    """Manage validated patient records in memory."""

    def __init__(self, patients: Iterable[Patient] = ()) -> None:
        self._patients: dict[str, Patient] = {}
        for patient in patients:
            self.add_patient(patient)

    def add_patient(self, patient: Patient) -> Patient:
        """Add a patient and reject duplicate identifiers."""
        self._require_patient(patient)
        if patient.patient_id in self._patients:
            raise PatientAlreadyExistsError(
                f"patient '{patient.patient_id}' already exists"
            )
        self._patients[patient.patient_id] = patient
        return patient

    def get_patient(self, patient_id: str) -> Patient:
        """Return a patient by identifier or raise ``PatientNotFoundError``."""
        validated_id = self._validate_patient_id(patient_id)
        try:
            return self._patients[validated_id]
        except KeyError as error:
            raise PatientNotFoundError(
                f"patient '{validated_id}' was not found"
            ) from error

    def list_patients(self) -> list[Patient]:
        """Return all patients in insertion order."""
        return list(self._patients.values())

    def search_patients(self, search_term: str) -> list[Patient]:
        """Return patients whose identifier or name contains the search term."""
        if not isinstance(search_term, str):
            raise ValueError("search_term must be a string")
        normalized_term = search_term.strip().casefold()
        if not normalized_term:
            raise ValueError("search_term must not be empty")
        return [
            patient
            for patient in self._patients.values()
            if normalized_term in patient.patient_id.casefold()
            or normalized_term in patient.name.casefold()
        ]

    def update_patient(self, patient: Patient) -> Patient:
        """Replace an existing patient with a validated record."""
        self._require_patient(patient)
        self.get_patient(patient.patient_id)
        self._patients[patient.patient_id] = patient
        return patient

    def delete_patient(self, patient_id: str) -> Patient:
        """Delete and return a patient by identifier."""
        validated_id = self._validate_patient_id(patient_id)
        try:
            return self._patients.pop(validated_id)
        except KeyError as error:
            raise PatientNotFoundError(
                f"patient '{validated_id}' was not found"
            ) from error

    @staticmethod
    def _require_patient(patient: Patient) -> None:
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient instance")

    @staticmethod
    def _validate_patient_id(patient_id: str) -> str:
        return validate_identifier(patient_id, "patient_id")