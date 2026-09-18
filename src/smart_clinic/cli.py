"""Text-based SmartClinic application layer."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from .appointment_management import AppointmentManager
from .models import Appointment, Patient, Service
from .patient_management import PatientManager
from .reporting import appointments_by_date, service_usage, summary_counts
from .service_management import ServiceManager


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


class SmartClinicCLI:
    """Coordinate terminal interaction with SmartClinic managers."""

    def __init__(
        self,
        input_function: InputFunction = input,
        output_function: OutputFunction = print,
    ) -> None:
        self._input = input_function
        self._output = output_function
        self.patient_manager = PatientManager()
        self.appointment_manager = AppointmentManager()
        self.service_manager = ServiceManager()

    def run(self) -> None:
        """Run the main menu until the user chooses to exit."""
        self._output("Welcome to SmartClinic")
        while True:
            self._show_main_menu()
            choice = self._input("Choose an option: ").strip()
            if choice == "1":
                self._patient_menu()
            elif choice == "2":
                self._appointment_menu()
            elif choice == "3":
                self._service_menu()
            elif choice == "4":
                self._report_menu()
            elif choice == "0":
                self._output("Goodbye")
                return
            else:
                self._output("Invalid menu choice")

    def _show_main_menu(self) -> None:
        self._output("\n1. Patient management")
        self._output("2. Appointment management")
        self._output("3. Service management")
        self._output("4. Reports")
        self._output("0. Exit")

    def _patient_menu(self) -> None:
        self._output("\nPatient management")
        self._output("1. Add  2. List  3. Search  4. Update  5. Delete  0. Back")
        choice = self._input("Choose an option: ").strip()
        self._run_menu_action(lambda: self._handle_patient_choice(choice))

    def _handle_patient_choice(self, choice: str) -> None:
        if choice == "1":
            self._add_patient()
        elif choice == "2":
            self._display_items(self.patient_manager.list_patients())
        elif choice == "3":
            term = self._input("Search term: ")
            self._display_items(self.patient_manager.search_patients(term))
        elif choice == "4":
            self._update_patient()
        elif choice == "5":
            self.patient_manager.delete_patient(self._input("Patient ID: ").strip())
            self._output("Patient deleted")
        elif choice != "0":
            self._output("Invalid menu choice")

    def _add_patient(self) -> None:
        patient = Patient(
            self._input("Patient ID: ").strip(),
            self._input("Name: "),
            self._read_date("Date of birth (YYYY-MM-DD): "),
        )
        self.patient_manager.add_patient(patient)
        self._output("Patient added")

    def _update_patient(self) -> None:
        patient = Patient(
            self._input("Patient ID: ").strip(),
            self._input("Name: "),
            self._read_date("Date of birth (YYYY-MM-DD): "),
        )
        self.patient_manager.update_patient(patient)
        self._output("Patient updated")

    def _appointment_menu(self) -> None:
        self._output("\nAppointment management")
        self._output("1. Add  2. List  3. By patient  4. Update  5. Delete  0. Back")
        choice = self._input("Choose an option: ").strip()
        self._run_menu_action(lambda: self._handle_appointment_choice(choice))

    def _handle_appointment_choice(self, choice: str) -> None:
        if choice == "1":
            self._add_appointment()
        elif choice == "2":
            self._display_items(self.appointment_manager.list_appointments())
        elif choice == "3":
            patient_id = self._input("Patient ID: ").strip()
            self._display_items(
                self.appointment_manager.get_patient_appointments(patient_id)
            )
        elif choice == "4":
            self._update_appointment()
        elif choice == "5":
            self.appointment_manager.delete_appointment(
                self._input("Appointment ID: ").strip()
            )
            self._output("Appointment deleted")
        elif choice != "0":
            self._output("Invalid menu choice")

    def _add_appointment(self) -> None:
        appointment = self._read_appointment()
        self.appointment_manager.add_appointment(appointment)
        self._output("Appointment added")

    def _update_appointment(self) -> None:
        appointment = self._read_appointment()
        self.appointment_manager.update_appointment(appointment)
        self._output("Appointment updated")

    def _read_appointment(self) -> Appointment:
        return Appointment(
            self._input("Appointment ID: ").strip(),
            self._input("Patient ID: ").strip(),
            self._input("Service ID: ").strip(),
            self._read_datetime("Start (YYYY-MM-DDTHH:MM): "),
            self._read_datetime("End (YYYY-MM-DDTHH:MM): "),
        )

    def _service_menu(self) -> None:
        self._output("\nService management")
        self._output("1. Add  2. List  3. Search  4. Update  5. Delete  0. Back")
        choice = self._input("Choose an option: ").strip()
        self._run_menu_action(lambda: self._handle_service_choice(choice))

    def _handle_service_choice(self, choice: str) -> None:
        if choice == "1":
            self._add_service()
        elif choice == "2":
            self._display_items(self.service_manager.list_services())
        elif choice == "3":
            term = self._input("Search term: ")
            self._display_items(self.service_manager.search_services(term))
        elif choice == "4":
            self._update_service()
        elif choice == "5":
            self.service_manager.delete_service(self._input("Service ID: ").strip())
            self._output("Service deleted")
        elif choice != "0":
            self._output("Invalid menu choice")

    def _add_service(self) -> None:
        service = self._read_service()
        self.service_manager.add_service(service)
        self._output("Service added")

    def _update_service(self) -> None:
        service = self._read_service()
        self.service_manager.update_service(service)
        self._output("Service updated")

    def _read_service(self) -> Service:
        return Service(
            self._input("Service ID: ").strip(),
            self._input("Name: "),
            self._read_positive_integer("Duration in minutes: "),
            self._read_decimal("Price: "),
        )

    def _report_menu(self) -> None:
        self._output("\nReports")
        self._output("1. Summary  2. Appointments by date  3. Service usage  0. Back")
        choice = self._input("Choose an option: ").strip()
        if choice == "1":
            self._output(str(summary_counts(
                self.patient_manager.list_patients(),
                self.appointment_manager.list_appointments(),
                self.service_manager.list_services(),
            )))
        elif choice == "2":
            self._output(str(appointments_by_date(
                self.appointment_manager.list_appointments()
            )))
        elif choice == "3":
            self._output(str(service_usage(
                self.appointment_manager.list_appointments()
            )))
        elif choice != "0":
            self._output("Invalid menu choice")

    def _display_items(self, items: list[object]) -> None:
        if not items:
            self._output("No records found")
            return
        for item in items:
            self._output(str(item))

    def _run_menu_action(self, action: Callable[[], None]) -> None:
        try:
            action()
        except (TypeError, ValueError, LookupError) as error:
            self._output(f"Error: {error}")

    def _read_date(self, prompt: str) -> date:
        return date.fromisoformat(self._input(prompt).strip())

    def _read_datetime(self, prompt: str) -> datetime:
        return datetime.fromisoformat(self._input(prompt).strip())

    def _read_positive_integer(self, prompt: str) -> int:
        return int(self._input(prompt).strip())

    def _read_decimal(self, prompt: str) -> Decimal:
        try:
            return Decimal(self._input(prompt).strip())
        except InvalidOperation as error:
            raise ValueError("price must be a valid decimal") from error


def main() -> None:
    """Start the SmartClinic command-line application."""
    SmartClinicCLI().run()


if __name__ == "__main__":
    main()