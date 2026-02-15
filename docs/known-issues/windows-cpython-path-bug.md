# Windows: CPython PATH Corruption in Git Bash (Python <=3.12)

## Problem

Python's `activate` script for virtual environments produces corrupted PATH entries when run in Git Bash on Windows (Python <=3.12). This causes `python` to resolve to the system Python or Windows App Execution Alias stub instead of the venv Python.

**CPython bug**: [python/cpython#82764](https://github.com/python/cpython/issues/82764)
**Fixed in**: Python 3.13.1+

## Impact

Bare `python` in Bash tool calls may invoke the wrong interpreter on Windows, leading to missing packages or incorrect behavior.

## Workaround

PhilLit uses `$PYTHON` (set by `setup-environment.sh` via `CLAUDE_ENV_FILE`) instead of bare `python` in all instruction files. This resolves to `.venv/bin/python` on Unix and `.venv/Scripts/python` on Windows, bypassing PATH resolution entirely.

All agent definitions and skill instructions use `$PYTHON` in their Bash code blocks. The variable is available in all Bash tool calls (main session and subagents) because it is captured in the `ENV_BEFORE`/`ENV_AFTER` diff and written to `CLAUDE_ENV_FILE`.

## Future

On Python 3.13.1+, bare `python` should work correctly in Git Bash after venv activation. However, `$PYTHON` remains the safer approach for compatibility with older Python versions.
