from decimal import Decimal

import pytest

from smart_clinic.models import Service
from smart_clinic.service_management import (
    ServiceAlreadyExistsError,
    ServiceManager,
    ServiceNotFoundError,
)


def make_service(
    service_id: str = "service-1",
    name: str = "Initial consultation",
    duration_minutes: int = 30,
    price: Decimal = Decimal("45.00"),
) -> Service:
    return Service(service_id, name, duration_minutes, price)


def test_add_and_get_service() -> None:
    manager = ServiceManager()
    service = make_service()

    assert manager.add_service(service) == service
    assert manager.get_service("service-1") == service


def test_add_rejects_non_service_data() -> None:
    with pytest.raises(TypeError, match="Service instance"):
        ServiceManager().add_service({"service_id": "service-1"})


@pytest.mark.parametrize(
    ("service_id", "name", "duration_minutes", "price"),
    [
        ("service 1", "Consultation", 30, Decimal("45.00")),
        ("service-1", "   ", 30, Decimal("45.00")),
        ("service-1", "Consultation", 0, Decimal("45.00")),
        ("service-1", "Consultation", 30, Decimal("-1.00")),
        ("service-1", "Consultation", 30, 45.0),
    ],
)
def test_service_model_rejects_invalid_data(
    service_id: str,
    name: str,
    duration_minutes: int,
    price: object,
) -> None:
    with pytest.raises(ValueError):
        Service(service_id, name, duration_minutes, price)


def test_add_rejects_duplicate_identifier() -> None:
    manager = ServiceManager([make_service()])

    with pytest.raises(ServiceAlreadyExistsError, match="service-1"):
        manager.add_service(make_service(name="Follow-up consultation"))


def test_list_services_preserves_order_and_is_independent() -> None:
    first = make_service()
    second = make_service("service-2", "Follow-up consultation")
    manager = ServiceManager([first, second])

    services = manager.list_services()
    services.clear()

    assert manager.list_services() == [first, second]


def test_search_services_matches_name_and_identifier_case_insensitively() -> None:
    first = make_service("service-1", "Initial consultation")
    second = make_service("dental-cleaning", "Dental Cleaning")
    manager = ServiceManager([first, second])

    assert manager.search_services("INITIAL") == [first]
    assert manager.search_services("DENTAL-CLEANING") == [second]
    assert manager.search_services("consult") == [first]


@pytest.mark.parametrize("search_term", ["", "   ", None])
def test_search_rejects_empty_or_invalid_term(search_term: object) -> None:
    with pytest.raises(ValueError, match="search_term"):
        ServiceManager().search_services(search_term)


def test_update_service_replaces_existing_record() -> None:
    manager = ServiceManager([make_service()])
    updated = make_service(
        name="Extended consultation", duration_minutes=60, price=Decimal("80.00")
    )

    assert manager.update_service(updated) == updated
    assert manager.get_service("service-1") == updated


def test_update_rejects_missing_service() -> None:
    with pytest.raises(ServiceNotFoundError, match="service-1"):
        ServiceManager().update_service(make_service())


def test_delete_service_removes_and_returns_record() -> None:
    service = make_service()
    manager = ServiceManager([service])

    assert manager.delete_service("service-1") == service
    assert manager.list_services() == []


def test_missing_service_behavior() -> None:
    manager = ServiceManager()

    with pytest.raises(ServiceNotFoundError, match="service-1"):
        manager.get_service("service-1")
    with pytest.raises(ServiceNotFoundError, match="service-1"):
        manager.delete_service("service-1")


@pytest.mark.parametrize("service_id", ["", "service 1", None])
def test_get_and_delete_reject_invalid_identifiers(service_id: object) -> None:
    manager = ServiceManager()

    with pytest.raises(ValueError, match="service_id"):
        manager.get_service(service_id)
    with pytest.raises(ValueError, match="service_id"):
        manager.delete_service(service_id)