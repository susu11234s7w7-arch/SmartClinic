# SmartClinic Development Instructions

- Keep changes focused on the current project step.
- Preserve the existing models, managers, validation, reporting, and CLI APIs.
- Use Python standard-library features unless a dependency is explicitly required.
- Keep business rules outside the CLI interaction layer.
- Reuse shared validation helpers instead of duplicating validation logic.
- Add focused pytest tests for behavior changes.
- Run `python -m pytest -q` after implementation changes.
- Do not fabricate screenshots, test results, GitHub state, or evidence.
- Avoid destructive Git commands and do not rewrite history.
