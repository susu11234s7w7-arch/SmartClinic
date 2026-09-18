from datetime import date, datetime
from decimal import Decimal

import pytest

from smart_clinic.models import Appointment, Patient, Service


def test_patient_accepts_valid_data() -> None:
    patient = Patient("patient-1", "  Ada Lovelace  ", date(1815, 12, 10))

    assert patient.patient_id == "patient-1"
    assert patient.name == "  Ada Lovelace  "


@pytest.mark.parametrize("patient_id", ["", "patient 1", "patient/1", None])
def test_patient_rejects_invalid_identifier(patient_id: object) -> None:
    with pytest.raises(ValueError, match="patient_id"):
        Patient(patient_id, "Ada Lovelace", date(1815, 12, 10))


@pytest.mark.parametrize("name", ["", "   ", None])
def test_patient_rejects_empty_name(name: object) -> None:
    with pytest.raises(ValueError, match="name"):
        Patient("patient-1", name, date(1815, 12, 10))


def test_patient_rejects_datetime_as_date_of_birth() -> None:
    with pytest.raises(ValueError, match="date_of_birth"):
        Patient("patient-1", "Ada Lovelace", datetime(1815, 12, 10))


def test_service_accepts_valid_data() -> None:
    service = Service("service-1", "Initial consultation", 30, Decimal("45.00"))

    assert service.duration_minutes == 30
    assert service.price == Decimal("45.00")


@pytest.mark.parametrize(
    ("duration_minutes", "price"),
    [(0, Decimal("10.00")), (-5, Decimal("10.00")), (30, Decimal("-1.00"))],
)
def test_service_rejects_invalid_information(
    duration_minutes: int, price: Decimal
) -> None:
    with pytest.raises(ValueError):
        Service("service-1", "Initial consultation", duration_minutes, price)


def test_service_rejects_non_decimal_price() -> None:
    with pytest.raises(ValueError, match="price"):
        Service("service-1", "Initial consultation", 30, 45.0)


def test_appointment_accepts_valid_interval() -> None:
    appointment = Appointment(
        "appointment-1",
        "patient-1",
        "service-1",
        datetime(2026, 9, 18, 9, 0),
        datetime(2026, 9, 18, 9, 30),
    )

    assert appointment.end_time > appointment.start_time


@pytest.mark.parametrize(
    ("start_time", "end_time"),
    [
        (datetime(2026, 9, 18, 9, 30), datetime(2026, 9, 18, 9, 30)),
        (datetime(2026, 9, 18, 10, 0), datetime(2026, 9, 18, 9, 30)),
        (date(2026, 9, 18), datetime(2026, 9, 18, 9, 30)),
    ],
)
def test_appointment_rejects_invalid_times(
    start_time: object, end_time: object
) -> None:
    with pytest.raises(ValueError):
        Appointment("appointment-1", "patient-1", "service-1", start_time, end_time)