# Vibe Coding Workflow

SmartClinic was developed in numbered, bounded steps. Each step was kept
focused, validated with tests, and stopped before the next step began.

## Working Principles

- Inspect the existing code and requirements before editing.
- Make the smallest change that satisfies the current step.
- Reuse existing models, validation, managers, and reporting functions.
- Keep business rules out of the CLI interaction layer.
- Add focused tests for new behavior.
- Run the complete pytest suite after implementation or refactoring.
- Review diagnostics and the resulting changes before reporting completion.
- Never fabricate screenshots, test results, commits, remotes, or URLs.

## Clean Code Practices

The implementation uses small focused functions, meaningful names, immutable
dataclass models, shared validation helpers, and in-memory managers with clear
exception types. The Step 12 refactoring removed duplicated CLI menu error
handling without changing public behavior or business rules.

## Current Verification

The latest verified complete-suite result is:

```text
77 passed in 1.09s
```

This documentation stage does not change application behavior.