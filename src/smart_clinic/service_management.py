"""In-memory management operations for service records."""

from __future__ import annotations

from collections.abc import Iterable

from .models import Service
from .validation import validate_identifier


class ServiceAlreadyExistsError(ValueError):
    """Raised when a service identifier is already registered."""


class ServiceNotFoundError(LookupError):
    """Raised when a requested service does not exist."""


class ServiceManager:
    """Manage validated service records in memory."""

    def __init__(self, services: Iterable[Service] = ()) -> None:
        self._services: dict[str, Service] = {}
        for service in services:
            self.add_service(service)

    def add_service(self, service: Service) -> Service:
        """Add a service and reject duplicate identifiers."""
        self._require_service(service)
        if service.service_id in self._services:
            raise ServiceAlreadyExistsError(
                f"service '{service.service_id}' already exists"
            )
        self._services[service.service_id] = service
        return service

    def get_service(self, service_id: str) -> Service:
        """Return a service by identifier or raise ``ServiceNotFoundError``."""
        validated_id = self._validate_service_id(service_id)
        try:
            return self._services[validated_id]
        except KeyError as error:
            raise ServiceNotFoundError(
                f"service '{validated_id}' was not found"
            ) from error

    def list_services(self) -> list[Service]:
        """Return all services in insertion order."""
        return list(self._services.values())

    def search_services(self, search_term: str) -> list[Service]:
        """Return services whose identifier or name contains the search term."""
        if not isinstance(search_term, str):
            raise ValueError("search_term must be a string")
        normalized_term = search_term.strip().casefold()
        if not normalized_term:
            raise ValueError("search_term must not be empty")
        return [
            service
            for service in self._services.values()
            if normalized_term in service.service_id.casefold()
            or normalized_term in service.name.casefold()
        ]

    def update_service(self, service: Service) -> Service:
        """Replace an existing service with a validated record."""
        self._require_service(service)
        self.get_service(service.service_id)
        self._services[service.service_id] = service
        return service

    def delete_service(self, service_id: str) -> Service:
        """Delete and return a service by identifier."""
        validated_id = self._validate_service_id(service_id)
        try:
            return self._services.pop(validated_id)
        except KeyError as error:
            raise ServiceNotFoundError(
                f"service '{validated_id}' was not found"
            ) from error

    @staticmethod
    def _require_service(service: Service) -> None:
        if not isinstance(service, Service):
            raise TypeError("service must be a Service instance")

    @staticmethod
    def _validate_service_id(service_id: str) -> str:
        return validate_identifier(service_id, "service_id")