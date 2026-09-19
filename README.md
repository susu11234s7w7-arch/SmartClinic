# SmartClinic

SmartClinic is a local clinic management system for synthetic patient records, appointments, clinic services, and simple reports. It is an academic project and does not provide medical diagnosis or treatment advice.

## Features

- Validated `Patient`, `Appointment`, and `Service` dataclass models
- Shared validation for identifiers, names, dates, times, durations, and prices
- In-memory patient, appointment, and service managers
- Duplicate and missing-record handling with clear exceptions
- Patient-scoped appointment conflict detection
- Case-insensitive patient and service search
- Deterministic summary, date-grouped appointment, and service-usage reports
- Text-based CLI using the existing managers and reporting functions
- Focused pytest coverage for models, managers, reporting, and CLI behavior

The application uses only the Python standard library at runtime. It has no database, web API, GUI, authentication, or external service.

## Project Structure

- `src/smart_clinic/models.py` - core dataclass models
- `src/smart_clinic/validation.py` - shared validation helpers
- `src/smart_clinic/patient_management.py` - in-memory patient operations
- `src/smart_clinic/appointment_management.py` - appointment operations and conflict checks
- `src/smart_clinic/service_management.py` - in-memory service operations
- `src/smart_clinic/reporting.py` - pure reporting functions
- `src/smart_clinic/cli.py` - text-based application interface
- `tests/` - pytest test suite
- `docs/` - project workflow and delivery documentation
- `screenshots/` - ten committed terminal evidence screenshots
- `data/sample_data.csv` - synthetic sample records
- `SCREENSHOTS.docx` - catalog of the ten real screenshot images
- `pyproject.toml` - project metadata and pytest configuration

## Setup and Execution

Python 3.11 or newer is required.

```bash
python -m venv .venv
python -m pip install -U pip
python -m pip install pytest python-docx
```

Run the CLI from the project root:

```bash
python -m smart_clinic.cli
```

Run the complete test suite:

```bash
python -m pytest -q
```

The latest verified result is `77 passed in 0.30s`, with zero failures and zero errors.

## GitHub Delivery

The public repository is `https://github.com/susu11234s7w7-arch/SmartClinic`. The local `main` branch is synchronized with `origin/main`.

Verified commits:

```text
9924e98 docs: add required lab screenshots
58ea81f feat: establish SmartClinic project baseline
```

## Evidence

The ten required terminal screenshots are stored under `screenshots/` and documented with their exact filenames and descriptions in [SCREENSHOTS.docx](SCREENSHOTS.docx).

Clean Code decisions, Linux/Git workflow notes, Vibe Coding practice, and final verification are documented in `docs/`.
