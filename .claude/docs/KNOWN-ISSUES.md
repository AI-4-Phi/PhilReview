# Known Issues

## Memory Crash During Literature Review Orchestration (macOS)

**Date Identified**: 2025-12-29
**Status**: Unresolved (upstream Claude Code bug)
**Affected Platform**: macOS (Darwin)
**Severity**: Critical — prevents workflow completion

### Symptoms

When running the `research-proposal-orchestrator` agent to generate a literature review:

1. Claude Code process memory grows rapidly (450MB → 18GB+)
2. CLI becomes unresponsive
3. Process terminates with "Aborted()" error
4. May show: `FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory`

### Root Cause

This is a **known bug in Claude Code**, not an issue with the agent definitions. Two open GitHub issues document this:

**[Issue #7020: Memory Leak When Initializing Sub-Agent Orchestration](https://github.com/anthropics/claude-code/issues/7020)**
- Memory grows from ~450MB → 30GB+ → crash
- Triggered by orchestrator patterns that spawn sub-agents via Task tool
- **macOS-specific** (Linux reported as working normally)
- Labels: `bug`, `memory`, `platform:macos`, `oncall`
- Status: **OPEN**

**[Issue #4580: 100% CPU Freeze During Multi-Agent Task JSON Serialization](https://github.com/anthropics/claude-code/issues/4580)**
- CLI becomes unresponsive during sub-agent spawning
- Root cause: Circular references or deep nesting in JSON serialization (2000+ recursive calls)
- Affects versions 1.0.60+
- Status: **OPEN**

### Why the Orchestrator Triggers This Bug

The `research-proposal-orchestrator` uses a "fan-out" pattern that matches the bug trigger:

```
Phase 3: Spawns 3-8 parallel domain-literature-researcher agents
Phase 5: Spawns N parallel synthesis-writer agents
```

Per `ARCHITECTURE.md`, a typical run spawns:
- 7 parallel domain researchers (Phase 3)
- 5 parallel synthesis writers (Phase 5)

Each agent receives context (plan files, BibTeX files, paths), and the orchestrator tracks their completion. This pattern causes memory accumulation during JSON serialization of context data between agents.

### Exacerbating Factors

1. **Parallel Task tool calls** — Multiple agents spawned in single message
2. **Context accumulation** — BibTeX files, outlines, and plans passed between agents
3. **macOS platform** — The bug is specifically tagged `platform:macos`
4. **Long-running workflow** — 6-phase workflow maintains large context

### Workarounds

#### Option 1: Environment Variables (Temporary Relief)

Set before running Claude Code:

```bash
export MALLOC_TRIM_THRESHOLD_=-1
export MALLOC_MMAP_THRESHOLD_=134217728  # 128MB threshold
export MALLOC_ARENA_MAX=4
export NODE_OPTIONS="--max-old-space-size=4096"
```

Add to shell profile (e.g., `~/.zshrc`) for persistence.

**Effectiveness**: Partial — may delay but not prevent crash.

#### Option 2: Run on Linux

The bug is macOS-specific. Users report normal behavior (200-300MB max) on Linux.

Options:
- Use a Linux VM or container
- Use a cloud-based Linux development environment
- Use WSL2 on Windows

**Effectiveness**: Full — bypasses the platform-specific bug.

#### Option 3: Sequential Agent Spawning

Modify the orchestrator to spawn agents sequentially instead of in parallel. This reduces memory pressure by avoiding concurrent JSON serialization.

**Trade-off**: Significantly slower (7x for Phase 3).

#### Option 4: Smaller Batches

Reduce the number of domains per literature review:
- 2-3 domains instead of 7
- Run multiple smaller reviews and combine manually

**Trade-off**: More manual work, but may complete successfully.

#### Option 5: Manual Phase Execution

Instead of running the full orchestrator, execute phases manually:

1. Run Phase 1-2 (planning) in one session
2. Start fresh session, run Phase 3 (domain research) — one domain at a time if needed
3. Start fresh session, run Phase 4-5 (synthesis)
4. Run Phase 6 (assembly) manually

**Trade-off**: Loses automation benefits, but preserves output quality.

### Monitoring the Issue

Track these GitHub issues for updates:

- https://github.com/anthropics/claude-code/issues/7020
- https://github.com/anthropics/claude-code/issues/4580
- https://github.com/anthropics/claude-code/issues/15487 (related: maxParallelAgents feature request)

### Related Issues

Other memory-related Claude Code issues that may compound the problem:

- [Issue #11155](https://github.com/anthropics/claude-code/issues/11155): Bash output stored in memory (90GB+)
- [Issue #3178](https://github.com/anthropics/claude-code/issues/3178): Resume causes heap out of memory
- [Issue #1421](https://github.com/anthropics/claude-code/issues/1421): Recurring crashes during 'thinking'

### Recommendations

| Timeframe | Action | Effort | Effectiveness |
|-----------|--------|--------|---------------|
| Immediate | Try environment variables | Low | Partial |
| Short-term | Test on Linux VM | Medium | Full |
| Medium-term | Modify orchestrator for sequential spawning | Medium | Partial |
| Long-term | Wait for upstream fix | None | Full (when fixed) |

### Architecture Implications

The multi-file-then-assemble pattern in `ARCHITECTURE.md` is sound and should be preserved. The issue is not with the agent design but with Claude Code's handling of the Task tool on macOS.

When the upstream bug is fixed, the parallel spawning pattern should work as intended, providing:
- 7x speedup for Phase 3
- Context isolation per agent
- Resilience to individual agent failures

---

*Last updated: 2025-12-29*
