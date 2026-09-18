# SmartClinic

SmartClinic is a local clinic management system for synthetic patient records,
appointments, clinic services, and simple reports. It is an academic project
and does not provide medical diagnosis or treatment advice.

## Implemented Features

- Validated `Patient`, `Appointment`, and `Service` data models
- In-memory patient, appointment, and service management
- Appointment conflict detection for overlapping appointments belonging to the same patient
- Case-insensitive patient and service search
- Deterministic summary, date-grouped appointment, and service-usage reports
- Text-based CLI for management operations and reports
- Focused pytest coverage for models, managers, reporting, and CLI behavior

The application has no database, web API, GUI, external service, or runtime
dependency outside the Python standard library.

## Project Structure

- `src/smart_clinic/` - application package
- `tests/` - pytest test suite
- `docs/` - project documentation and evidence preparation notes
- `screenshots/` - reserved for project evidence; no screenshots are claimed here
- `data/` - reserved for local project data; no database is used

## Setup

Python 3.11 or newer is required.

```bash
python -m venv .venv
```

Activate the environment using the command for your shell, then install the
development test dependency:

```bash
python -m pip install -U pip
python -m pip install pytest
```

## Run Tests

From the project root:

```bash
python -m pytest -q
```

The latest verified result before this documentation stage was `77 passed in
1.09s` with zero failures and zero errors. See [docs/DEVELOPMENT_LOG.md](docs/DEVELOPMENT_LOG.md)
for the project-stage record.

## Run the CLI

From the project root, with `src` available through the project environment:

```bash
python -m smart_clinic.cli
```

The CLI keeps data in memory for the current process. It does not persist
records between runs.

## Development Notes

Clean Code decisions, commands, workflow notes, and evidence requirements are
documented in [docs/COMMANDS.md](docs/COMMANDS.md),
[docs/VIBE_CODING.md](docs/VIBE_CODING.md), and
[docs/FINAL_CHECKLIST.md](docs/FINAL_CHECKLIST.md).
# SmartClinic

## Overview
SmartClinic is a local clinic management system for managing mock patient records, appointments, and clinic services. This project is designed for academic use and follows a clean Python project structure.

## Project Scope
This project focuses on:
- patient record management
- appointment scheduling
- conflict validation
- service definitions
- simple reporting
- automated testing

This project does not provide medical diagnosis or treatment advice.

## Project Structure
- `src/smart_clinic/` - application package
- `tests/` - pytest test suite
- `docs/` - project documentation
- `screenshots/` - project evidence screenshots
- `data/` - sample data files

## Local Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install pytest
```

## Run Tests
```bash
pytest -q
```

## Notes
This repository is intentionally minimal at this stage and is prepared for the later implementation of project features.
