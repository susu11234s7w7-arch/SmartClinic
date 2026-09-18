from datetime import date

import pytest

from smart_clinic.models import Patient
from smart_clinic.patient_management import (
    PatientAlreadyExistsError,
    PatientManager,
    PatientNotFoundError,
)


def make_patient(patient_id: str = "patient-1", name: str = "Ada Lovelace") -> Patient:
    return Patient(patient_id, name, date(1815, 12, 10))


def test_add_and_get_patient() -> None:
    manager = PatientManager()
    patient = make_patient()

    assert manager.add_patient(patient) == patient
    assert manager.get_patient("patient-1") == patient


def test_add_rejects_non_patient_data() -> None:
    manager = PatientManager()

    with pytest.raises(TypeError, match="Patient instance"):
        manager.add_patient({"patient_id": "patient-1"})


def test_add_rejects_duplicate_identifier() -> None:
    manager = PatientManager([make_patient()])

    with pytest.raises(PatientAlreadyExistsError, match="patient-1"):
        manager.add_patient(make_patient(name="Grace Hopper"))


def test_list_patients_preserves_insertion_order_and_is_independent() -> None:
    manager = PatientManager()
    first = make_patient()
    second = make_patient("patient-2", "Grace Hopper")
    manager.add_patient(first)
    manager.add_patient(second)

    patients = manager.list_patients()
    patients.clear()

    assert manager.list_patients() == [first, second]


def test_search_patients_matches_name_and_identifier_case_insensitively() -> None:
    manager = PatientManager(
        [
            make_patient("patient-1", "Ada Lovelace"),
            make_patient("patient-2", "Grace Hopper"),
            make_patient("client-3", "Alan Turing"),
        ]
    )

    assert manager.search_patients("ADA") == [make_patient("patient-1", "Ada Lovelace")]
    assert manager.search_patients("CLIENT-3") == [
        make_patient("client-3", "Alan Turing")
    ]


@pytest.mark.parametrize("search_term", ["", "   ", None])
def test_search_rejects_empty_or_invalid_term(search_term: object) -> None:
    with pytest.raises(ValueError, match="search_term"):
        PatientManager().search_patients(search_term)


def test_update_patient_replaces_existing_record() -> None:
    manager = PatientManager([make_patient()])
    updated_patient = Patient("patient-1", "Ada Byron", date(1815, 12, 10))

    assert manager.update_patient(updated_patient) == updated_patient
    assert manager.get_patient("patient-1") == updated_patient


def test_update_rejects_missing_patient() -> None:
    with pytest.raises(PatientNotFoundError, match="patient-1"):
        PatientManager().update_patient(make_patient())


def test_delete_patient_removes_and_returns_record() -> None:
    patient = make_patient()
    manager = PatientManager([patient])

    assert manager.delete_patient("patient-1") == patient
    assert manager.list_patients() == []


def test_get_and_delete_raise_for_missing_patient() -> None:
    manager = PatientManager()

    with pytest.raises(PatientNotFoundError, match="patient-1"):
        manager.get_patient("patient-1")
    with pytest.raises(PatientNotFoundError, match="patient-1"):
        manager.delete_patient("patient-1")


def test_management_operations_reject_invalid_identifiers() -> None:
    manager = PatientManager()

    with pytest.raises(ValueError, match="patient_id"):
        manager.get_patient("patient 1")
    with pytest.raises(ValueError, match="patient_id"):
        manager.delete_patient("patient 1")