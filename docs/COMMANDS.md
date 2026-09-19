# SmartClinic Commands

This document separates commands actually used in the project workflow from reference commands that were not claimed as executed.

## Environment and Linux Reference Commands

| Command | Purpose | Example or role |
| --- | --- | --- |
| `pwd` | Show the current directory | Standard Linux working-path check; not recorded as executed here |
| `ls` | List files and directories | Standard Linux structure check; not recorded as executed here |
| `cd` | Change directory | Used conceptually to work in `D:\SmartClinic`; the recorded terminal used PowerShell |
| `mkdir` | Create a directory | Standard Linux reference; not recorded as executed here |
| `python -m venv .venv` | Create a virtual environment | Documented setup command |
| `python -m pip install pytest python-docx` | Install development/documentation tools | Used for the final documentation task |

## Tests and Application

```bash
python -m pytest -q
python -m smart_clinic.cli
```

The final verified test result was `77 passed in 0.30s`, with zero failures and zero errors. The CLI stores records in memory for the current process.

## Executed Git Workflow

The following commands were used during the documented workflow:

```bash
git status --short
git status
git branch --show-current
git remote -v
git log --oneline --decorate --graph -5
git add .gitignore README.md docs/
git add pyproject.toml src/ tests/
git diff --staged --stat
git diff --staged --check
git diff --staged
git commit -m "feat: establish SmartClinic project baseline"
git add -- screenshots/14_01_git_status_staged.png screenshots/14_03_git_diff_staged_stat_terminal.png screenshots/14_04_git_diff_staged_check_terminal.png screenshots/14_05_pytest_full_suite_terminal.png screenshots/14_06_git_diff_staged_terminal.png screenshots/14_06_initial_commit_terminal.png screenshots/14_07_git_log_initial_commit_terminal.png screenshots/14_08_git_status_clean_terminal.png screenshots/14_09_git_log_terminal.png screenshots/15_04_git_status_clean_terminal.png
git commit -m "docs: add required lab screenshots"
git log --oneline --decorate -2
git ls-files -- screenshots
```

The baseline commit was `58ea81f` and the screenshot commit was `9924e98`. The working tree was verified clean and `main` synchronized with `origin/main` before the final documentation changes.

## GitHub Workflow

The public repository is `https://github.com/susu11234s7w7-arch/SmartClinic`. Remote configuration was verified with `git remote -v`, and the public repository page was checked. The exact push terminal output is not reproduced because it was not captured in this workspace.

Reference commands that were not claimed as executed in this record include:

```bash
git init
git restore --staged <path>
git restore <path>
git branch
git switch <branch>
git merge <branch>
git remote add origin <url>
git push origin main
git pull origin main
git --version
git config <key> <value>
```

## Evidence

The ten required terminal screenshots are committed under `screenshots/`. `SCREENSHOTS.docx` catalogs the actual images and descriptions. No screenshot evidence is fabricated.
