# Development Log

## Project Stages

- Steps 1-5: project setup and initial structure were completed before the
  current implementation stages.
- Step 6: added validated `Patient`, `Appointment`, and `Service` models with
  standard-library validation helpers.
- Step 7: added in-memory patient management.
- Step 8: added in-memory appointment management and patient-scoped conflict
  detection.
- Step 9: added in-memory service management.
- Step 10: added deterministic summary, appointment-date, and service-usage
  reports.
- Step 11: added the dependency-injected text CLI using existing managers and
  reporting functions.
- Step 12: removed duplicated CLI menu error handling through a small internal
  refactoring.
- Step 13: prepared project documentation and evidence checklists.

## Verification

The latest complete pytest run before this documentation stage reported:

```text
77 passed in 1.09s
```

Passed: 77. Failed: 0. Errors: 0.

No database, GUI, web API, external service, GitHub remote, commit, push, or
fabricated screenshot is part of the verified project state.

## Scope Notes

The application uses synthetic/local data and keeps records in memory. The
`data/` and `screenshots/` directories are reserved project locations, not
claims that data or screenshots currently exist.