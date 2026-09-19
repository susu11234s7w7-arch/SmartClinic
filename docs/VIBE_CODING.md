# Vibe Coding Workflow

SmartClinic was developed in bounded numbered steps. Each change was kept focused, reviewed, and verified before the next step.

## Responsible AI-Assisted Workflow

1. Define one requirement and its boundaries.
2. Provide the relevant project context and existing APIs.
3. Use constrained prompts that prohibit unrelated features and destructive operations.
4. Generate or assist with a small implementation change.
5. Review naming, responsibilities, validation, error handling, and readability.
6. Inspect the diff and confirm that only intended files changed.
7. Run focused checks and then the complete pytest suite.
8. Correct real failures with the smallest safe change.
9. Accept only code that is understandable and consistent with the project.
10. Use Git checkpoints to preserve reviewable history.
11. Complete final verification of tests, Git state, documentation, and evidence.

## Clean Code Practices

The project uses meaningful names, small focused functions, immutable dataclass models, shared validation helpers, clear manager exceptions, separation of CLI interaction from business rules, and dependency injection for CLI testing. The Step 12 refactoring removed duplicated CLI menu error handling without changing business behavior.

## Verification

The latest verified complete-suite result is:

```text
77 passed in 0.30s
```

The final workflow does not fabricate screenshots, test results, commits, remotes, or URLs. Evidence is taken from actual project files and terminal output.
