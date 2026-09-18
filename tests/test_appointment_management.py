from datetime import datetime, timedelta

import pytest

from smart_clinic.appointment_management import (
    AppointmentAlreadyExistsError,
    AppointmentConflictError,
    AppointmentManager,
    AppointmentNotFoundError,
)
from smart_clinic.models import Appointment


BASE_TIME = datetime(2026, 9, 18, 9, 0)


def make_appointment(
    appointment_id: str = "appointment-1",
    patient_id: str = "patient-1",
    start_time: datetime = BASE_TIME,
    duration_minutes: int = 30,
) -> Appointment:
    return Appointment(
        appointment_id,
        patient_id,
        "service-1",
        start_time,
        start_time + timedelta(minutes=duration_minutes),
    )


def test_add_and_get_appointment() -> None:
    manager = AppointmentManager()
    appointment = make_appointment()

    assert manager.add_appointment(appointment) == appointment
    assert manager.get_appointment("appointment-1") == appointment


def test_add_rejects_non_appointment_data() -> None:
    with pytest.raises(TypeError, match="Appointment instance"):
        AppointmentManager().add_appointment({"appointment_id": "appointment-1"})


def test_add_rejects_duplicate_identifier() -> None:
    manager = AppointmentManager([make_appointment()])

    with pytest.raises(AppointmentAlreadyExistsError, match="appointment-1"):
        manager.add_appointment(make_appointment(start_time=BASE_TIME + timedelta(hours=2)))


def test_list_appointments_preserves_order_and_is_independent() -> None:
    first = make_appointment()
    second = make_appointment(
        "appointment-2", start_time=BASE_TIME + timedelta(hours=1)
    )
    manager = AppointmentManager([first, second])

    appointments = manager.list_appointments()
    appointments.clear()

    assert manager.list_appointments() == [first, second]


def test_get_patient_appointments_retrieves_relevant_records() -> None:
    first = make_appointment()
    second = make_appointment(
        "appointment-2", "patient-2", BASE_TIME
    )
    manager = AppointmentManager([first, second])

    assert manager.get_patient_appointments("patient-1") == [first]
    assert manager.get_patient_appointments("patient-3") == []


def test_update_appointment_replaces_existing_record() -> None:
    manager = AppointmentManager([make_appointment()])
    updated = make_appointment(
        start_time=BASE_TIME + timedelta(hours=1), duration_minutes=45
    )

    assert manager.update_appointment(updated) == updated
    assert manager.get_appointment("appointment-1") == updated


def test_update_rejects_missing_appointment() -> None:
    with pytest.raises(AppointmentNotFoundError, match="appointment-1"):
        AppointmentManager().update_appointment(make_appointment())


def test_delete_appointment_removes_and_returns_record() -> None:
    appointment = make_appointment()
    manager = AppointmentManager([appointment])

    assert manager.delete_appointment("appointment-1") == appointment
    assert manager.list_appointments() == []


def test_missing_appointment_behavior() -> None:
    manager = AppointmentManager()

    with pytest.raises(AppointmentNotFoundError, match="appointment-1"):
        manager.get_appointment("appointment-1")
    with pytest.raises(AppointmentNotFoundError, match="appointment-1"):
        manager.delete_appointment("appointment-1")


def test_overlapping_appointments_for_same_patient_are_rejected() -> None:
    manager = AppointmentManager([make_appointment()])
    overlapping = make_appointment(
        "appointment-2", start_time=BASE_TIME + timedelta(minutes=15)
    )

    with pytest.raises(AppointmentConflictError, match="appointment-1"):
        manager.add_appointment(overlapping)


def test_non_conflicting_appointments_are_allowed() -> None:
    first = make_appointment()
    back_to_back = make_appointment(
        "appointment-2", start_time=BASE_TIME + timedelta(minutes=30)
    )
    different_patient = make_appointment(
        "appointment-3", "patient-2", BASE_TIME + timedelta(minutes=15)
    )
    manager = AppointmentManager([first])

    manager.add_appointment(back_to_back)
    manager.add_appointment(different_patient)

    assert manager.list_appointments() == [first, back_to_back, different_patient]


def test_update_rejects_new_conflict() -> None:
    manager = AppointmentManager(
        [
            make_appointment(),
            make_appointment(
                "appointment-2", start_time=BASE_TIME + timedelta(hours=1)
            ),
        ]
    )
    conflicting_update = make_appointment(
        "appointment-2", start_time=BASE_TIME + timedelta(minutes=15)
    )

    with pytest.raises(AppointmentConflictError, match="appointment-1"):
        manager.update_appointment(conflicting_update)


@pytest.mark.parametrize("appointment_id", ["", "appointment 1", None])
def test_retrieval_and_deletion_reject_invalid_identifiers(
    appointment_id: object,
) -> None:
    manager = AppointmentManager()

    with pytest.raises(ValueError, match="appointment_id"):
        manager.get_appointment(appointment_id)
    with pytest.raises(ValueError, match="appointment_id"):
        manager.delete_appointment(appointment_id)