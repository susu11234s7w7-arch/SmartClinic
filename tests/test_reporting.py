from datetime import date, datetime
from decimal import Decimal

from smart_clinic.models import Appointment, Patient, Service
from smart_clinic.reporting import (
    appointments_by_date,
    service_usage,
    summary_counts,
)


def make_patient(patient_id: str = "patient-1") -> Patient:
    return Patient(patient_id, "Ada Lovelace", date(1815, 12, 10))


def make_service(service_id: str = "service-1") -> Service:
    return Service(service_id, "Consultation", 30, Decimal("45.00"))


def make_appointment(
    appointment_id: str = "appointment-1",
    service_id: str = "service-1",
    start_time: datetime = datetime(2026, 9, 18, 9, 0),
) -> Appointment:
    return Appointment(
        appointment_id,
        "patient-1",
        service_id,
        start_time,
        start_time.replace(minute=start_time.minute + 30),
    )


def test_reports_are_empty_for_empty_collections() -> None:
    assert summary_counts([], [], []) == {
        "patients": 0,
        "appointments": 0,
        "services": 0,
    }
    assert appointments_by_date([]) == {}
    assert service_usage([]) == {}


def test_summary_counts_normal_collections() -> None:
    patients = [make_patient("patient-1"), make_patient("patient-2")]
    appointments = [make_appointment(), make_appointment("appointment-2")]
    services = [make_service(), make_service("service-2")]

    assert summary_counts(patients, appointments, services) == {
        "patients": 2,
        "appointments": 2,
        "services": 2,
    }


def test_appointments_by_date_groups_multiple_appointments() -> None:
    first_date = date(2026, 9, 18)
    second_date = date(2026, 9, 19)
    first = make_appointment("appointment-1", start_time=datetime(2026, 9, 18, 9))
    second = make_appointment("appointment-2", start_time=datetime(2026, 9, 18, 10))
    third = make_appointment("appointment-3", start_time=datetime(2026, 9, 19, 9))

    assert appointments_by_date([first, second, third]) == {
        first_date: [first, second],
        second_date: [third],
    }


def test_appointments_by_date_preserves_appointment_order() -> None:
    later = make_appointment("appointment-2", start_time=datetime(2026, 9, 18, 11))
    earlier = make_appointment("appointment-1", start_time=datetime(2026, 9, 18, 9))

    assert appointments_by_date([later, earlier])[date(2026, 9, 18)] == [
        later,
        earlier,
    ]


def test_service_usage_counts_multiple_services() -> None:
    first = make_appointment("appointment-1", "service-1")
    second = make_appointment("appointment-2", "service-2")
    third = make_appointment("appointment-3", "service-1")

    assert service_usage([first, second, third]) == {
        "service-1": 2,
        "service-2": 1,
    }


def test_reports_accept_generators() -> None:
    assert summary_counts(
        (make_patient() for _ in range(2)),
        (make_appointment() for _ in range(3)),
        (make_service() for _ in range(4)),
    ) == {"patients": 2, "appointments": 3, "services": 4}