# Plan: Fix Environment Variable Propagation via `CLAUDE_ENV_FILE`

**Branch**: `fix/env-propagation-and-python-path`
**Date**: 2026-02-15
**Status**: Plan — awaiting implementation

## Problem Statement

Two related issues with how environment variables reach subagent-spawned Python scripts:

1. **API keys from `.env` don't propagate to subagents** (reported by Richard Yetter Chappell, partially fixed on `main`)
2. **No cross-platform `$PYTHON` variable** — instruction files hardcode `.venv/bin/python` which doesn't exist on Windows (`.venv/Scripts/python`)

## Root Cause Analysis

### How `CLAUDE_ENV_FILE` works

Claude Code's `SessionStart` hook can persist environment variables for the entire session by writing `export` statements to `$CLAUDE_ENV_FILE`. Variables written there are available to all subsequent Bash tool calls, **including those from subagents**.

### The bug in `setup-environment.sh`

The hook uses a before/after diff to capture only new or changed variables:

```
Line 51:  load_dotenv ".env"          ← .env vars exported HERE
Line 72:  ENV_BEFORE=$(export -p)     ← snapshot INCLUDES .env vars (already in env)
Line 74-88: uv sync + venv activate   ← only venv vars change
Line 91:  ENV_AFTER=$(export -p)      ← snapshot INCLUDES .env vars (unchanged)
Line 94:  comm -13 ... >> $CLAUDE_ENV_FILE  ← diff only captures venv changes
```

Because `.env` is loaded at line 51 (BEFORE `ENV_BEFORE` is captured at line 72), the `.env` variables appear in **both** snapshots. The `comm -13` diff only outputs lines present in `ENV_AFTER` but absent from `ENV_BEFORE` — so it captures venv activation changes (PATH, VIRTUAL_ENV, etc.) but **silently drops all `.env` variables**.

Result: `.env` API keys are in the hook's shell but never written to `CLAUDE_ENV_FILE`, so they don't propagate to the main session or subagents.

### Current state (on `main`)

The `load_dotenv` fix on `main` (commit `b5016b5`) added `python-dotenv` with `load_dotenv(override=True)` to all 13 Python scripts that read env vars. This works as a Python-level fallback — each script loads `.env` directly, bypassing the need for the shell environment to carry the values. But it doesn't fix the hook-level root cause.

### What's on this branch (unstaged)

Bare `python` replaced with `.venv/bin/python` in all instruction files (6 files). This is an improvement for macOS/Linux but does NOT work on Windows where the path is `.venv/Scripts/python`. These changes will be superseded by the `$PYTHON` approach below.

## Proposed Fix

### Step 1: Move `.env` loading after `ENV_BEFORE` capture

In `setup-environment.sh`, move `load_dotenv ".env"` from line 51 to after `ENV_BEFORE` is captured (after line 72). This way `.env` vars appear in `ENV_AFTER` but not `ENV_BEFORE`, so `comm -13` writes them to `CLAUDE_ENV_FILE`.

**Before:**
```bash
load_dotenv ".env"          # line 51
# ... stale venv detection ...
ENV_BEFORE=$(export -p | sort)  # line 72
# ... uv sync + activate ...
ENV_AFTER=$(export -p | sort)   # line 91
comm -13 ... >> "$CLAUDE_ENV_FILE"
```

**After:**
```bash
# ... stale venv detection ...
ENV_BEFORE=$(export -p | sort)
load_dotenv ".env"          # NOW after ENV_BEFORE
# ... uv sync + activate ...
ENV_AFTER=$(export -p | sort)
comm -13 ... >> "$CLAUDE_ENV_FILE"
```

**Safety**: The `.env` file only contains API keys (BRAVE_API_KEY, S2_API_KEY, etc.). None of these are needed by `uv sync` or venv activation. The stale venv detection (lines 53-69) also doesn't need them. So moving the load later has no side effects on the hook's own logic.

**Interaction with `load_dotenv(override=True)` in Python scripts**: Both mechanisms would now load `.env` with override semantics. When both are active (main session), the Python-level load is redundant but harmless. When only the Python-level is active (edge cases where `CLAUDE_ENV_FILE` doesn't work), it still functions as a fallback. Defense in depth.

### Step 2: Set `$PYTHON` in the hook

After venv activation but before `ENV_AFTER` capture, detect the platform and export `PYTHON`:

```bash
# Set cross-platform $PYTHON path (captured by ENV_AFTER diff)
if [ -f ".venv/Scripts/python" ]; then
  export PYTHON=".venv/Scripts/python"
else
  export PYTHON=".venv/bin/python"
fi
```

This goes between the venv activation block (line 88) and `ENV_AFTER` capture (line 91). The `comm -13` diff will include it in `CLAUDE_ENV_FILE`, making `$PYTHON` available to all Bash tool calls for the session.

### Step 3: Replace `.venv/bin/python` with `$PYTHON` in instruction files

Replace all `.venv/bin/python` (the changes currently unstaged on this branch) with `$PYTHON` in:

- `.claude/skills/philosophy-research/SKILL.md` (~33 instances)
- `.claude/agents/domain-literature-researcher.md` (~30 instances)
- `.claude/skills/literature-review/SKILL.md` (5 instances)
- `CLAUDE.md` (1 instance)
- `CONTRIBUTING.md` (1 instance)
- `GETTING_STARTED.md` (1 instance — user-facing, might keep as `.venv/bin/python` with a note)

### Step 4: Update documentation

- **CLAUDE.md** "Hooks and Python" section: Document that `$PYTHON` is set by `setup-environment.sh` and available in all Bash tool calls. Update the bullet about Bash tool calls.
- **CLAUDE.md** `.env` loading bullet: Note that `.env` vars are now also propagated via `CLAUDE_ENV_FILE`, not just Python-level `load_dotenv`.

## Risks and Open Questions

### Does `CLAUDE_ENV_FILE` actually propagate to subagent Bash calls?

This is the critical assumption. The mechanism is designed for this purpose (persisting session-wide env vars), and the venv-related variables (PATH, VIRTUAL_ENV) set via the same mechanism DO work in Bash tool calls. But it should be verified empirically in a subagent context, per the project's "verify assumptions empirically" principle.

**Test**: After implementing Step 2, start a new session and run a Task tool subagent that executes `echo $PYTHON` via Bash. If it outputs the correct path, propagation works. If empty, `CLAUDE_ENV_FILE` doesn't reach subagents and we need a different approach.

### Does `$PYTHON` expand correctly in subagent Bash calls?

Shell variable expansion (`$PYTHON`) requires the variable to be in the shell's environment when the command runs. If `CLAUDE_ENV_FILE` propagation works (question above), this should work. But instruction files use `$PYTHON` inside markdown code blocks — Claude (the AI) needs to understand this as a variable reference, not a literal string. Given that agents already use `$REVIEW_DIR` and `$PWD` in bash examples, this pattern is established.

### Ordering: `.env` load vs. stale venv detection

The stale venv detection (lines 53-69) reads activate scripts to check paths. It doesn't use `.env` variables. Moving `.env` loading after it is safe. But verify there's no hidden dependency.

### `GETTING_STARTED.md` — user-facing command

The `check_setup.py` command in GETTING_STARTED.md is run manually by users. Users may not have `$PYTHON` set if they're running outside Claude Code. Consider keeping this as `.venv/bin/python` with a note about Windows, or using `uv run python` which is venv-aware.

## Files to Modify

| File | Change |
|------|--------|
| `.claude/hooks/setup-environment.sh` | Move `.env` load; add `export PYTHON` |
| `.claude/skills/philosophy-research/SKILL.md` | `.venv/bin/python` → `$PYTHON` |
| `.claude/agents/domain-literature-researcher.md` | `.venv/bin/python` → `$PYTHON` |
| `.claude/skills/literature-review/SKILL.md` | `.venv/bin/python` → `$PYTHON` |
| `CLAUDE.md` | `.venv/bin/python` → `$PYTHON`; update docs |
| `CONTRIBUTING.md` | `.venv/bin/python` → `$PYTHON` |
| `GETTING_STARTED.md` | Possibly keep as-is (user-facing) |

## Implementation Order

1. Modify `setup-environment.sh` (Steps 1 + 2)
2. Test empirically: restart session, verify `$PYTHON` and API keys are in env
3. Test in subagent: spawn a Task tool agent, verify `$PYTHON` is available
4. If verified: replace `.venv/bin/python` → `$PYTHON` in instruction files (Step 3)
5. Update documentation (Step 4)
6. Run test suite
7. Review and commit
