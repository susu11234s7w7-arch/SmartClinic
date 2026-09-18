from datetime import date
from decimal import Decimal

from smart_clinic.cli import SmartClinicCLI
from smart_clinic.models import Patient, Service


def run_cli(inputs: list[str]) -> list[str]:
    output: list[str] = []
    values = iter(inputs)
    SmartClinicCLI(input_function=lambda _prompt: next(values), output_function=output.append).run()
    return output


def test_cli_can_exit_and_handles_invalid_main_menu_choice() -> None:
    output = run_cli(["invalid", "0"])

    assert "Invalid menu choice" in output
    assert output[-1] == "Goodbye"


def test_cli_adds_patient_and_reports_summary() -> None:
    output = run_cli(
        [
            "1", "1", "patient-1", "Ada Lovelace", "1815-12-10",
            "4", "1", "0", "0",
        ]
    )

    assert "Patient added" in output
    assert str({"patients": 1, "appointments": 0, "services": 0}) in output


def test_cli_handles_invalid_patient_input_without_crashing() -> None:
    output = run_cli(["1", "1", "bad id", "Ada Lovelace", "1815-12-10", "0"])

    assert any(message.startswith("Error:") for message in output)
    assert output[-1] == "Goodbye"


def test_cli_uses_existing_managers_and_reports() -> None:
    cli = SmartClinicCLI(input_function=lambda _prompt: "0", output_function=lambda _: None)
    patient = Patient("patient-1", "Ada Lovelace", date(1815, 12, 10))
    service = Service("service-1", "Consultation", 30, Decimal("45.00"))
    cli.patient_manager.add_patient(patient)
    cli.service_manager.add_service(service)

    assert cli.patient_manager.get_patient("patient-1") == patient
    assert cli.service_manager.get_service("service-1") == service