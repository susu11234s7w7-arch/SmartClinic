# Development Log

## Project Stages

- Steps 1-5: project setup and initial structure were completed before the implementation stages.
- Step 6: added validated `Patient`, `Appointment`, and `Service` models with standard-library validation helpers.
- Step 7: added in-memory patient management.
- Step 8: added in-memory appointment management and patient-scoped conflict detection.
- Step 9: added in-memory service management.
- Step 10: added deterministic summary, appointment-date, and service-usage reports.
- Step 11: added the dependency-injected text CLI using existing managers and reporting functions.
- Step 12: removed duplicated CLI menu error handling through a small internal refactoring.
- Step 13: prepared project documentation and evidence checklists.
- Step 14: reviewed staged changes, ran tests, created the baseline commit, and verified the clean working tree.
- Step 15: created the public GitHub repository, pushed `main`, and committed the ten required terminal screenshots.
- Final completion: updated documentation, added synthetic sample data and Copilot instructions, and created `SCREENSHOTS.docx` from the ten real images.

## Verified Git State

```text
9924e98 docs: add required lab screenshots
58ea81f feat: establish SmartClinic project baseline
```

The public repository is `https://github.com/susu11234s7w7-arch/SmartClinic`. The configured remote is `origin`, and `main` was verified synchronized with `origin/main` before this final documentation completion phase.

## Tests

The latest verified complete pytest run reported:

```text
77 passed in 0.30s
```

Passed: 77. Failed: 0. Errors: 0.

## Evidence

The ten required terminal screenshots are committed under `screenshots/`. `SCREENSHOTS.docx` contains the actual ten images and their exact filenames/descriptions. Old laboratory screenshots remain outside the project at `D:\Lab_Screenshots`.

## Scope

The application uses synthetic/local data and keeps records in memory. No database, GUI, web API, authentication, or external service was added.
