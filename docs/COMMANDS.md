# SmartClinic Commands

These commands describe the local development workflow. They do not claim that
GitHub operations, commits, pushes, or screenshots have been completed.

## Environment Setup

```bash
python -m venv .venv
python -m pip install -U pip
python -m pip install pytest
```

Activate `.venv` using the command appropriate for the current shell.

## Test Commands

Run the complete suite:

```bash
python -m pytest -q
```

The verified project result is `77 passed in 1.09s`, with zero failures and
zero errors.

## Run the Application

```bash
python -m smart_clinic.cli
```

The CLI is an in-memory application. Records are lost when the process exits.

## Local Git Workflow

Use ordinary, non-destructive commands to inspect work:

```bash
git status --short
git diff -- README.md docs src tests
```

Review changes before creating a commit. No commit, remote, push, or GitHub URL
is claimed by this documentation.

## Linux and Windows Notes

The Python commands above work on Linux and Windows when Python is installed
and available as `python`. Virtual-environment activation differs by shell;
consult the shell's standard activation syntax rather than assuming one shell.

## Evidence Commands

Use the test command output and reviewed source files as evidence for local
verification. Screenshots must be captured separately from the running project
and stored under `screenshots/`; this repository currently claims no screenshot
evidence.