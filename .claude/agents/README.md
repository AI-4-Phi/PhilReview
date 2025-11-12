# Research Proposal Literature Review Agents

**LiRA-Inspired Multi-Agent Workflow for State-of-the-Art Reviews**

## Overview

This directory contains a sophisticated 6-phase agent-based workflow for generating comprehensive, publication-ready state-of-the-art literature reviews for research proposals. The system is inspired by the LiRA (Literature Review Agents) framework but adapted specifically for philosophical research proposals.

## Recent Optimizations (Context Window Efficiency)

- **Compact bibliographies**: Domain researchers now produce structured bibliographies (1500-3000 words) instead of prose reviews (8000+ words)
- **Validation removed**: Phase 3 citation validation eliminated to reduce processing time
- **Task persistence**: Added `task-progress.md` for cross-conversation resume capability
- **Result**: Synthesis-planner can now read all 7 domains without context overflow

## Agent Architecture

### Meta-Orchestrator
- **research-proposal-orchestrator.md** - Coordinates the entire 6-phase workflow with task persistence

### Phase Agents

1. **literature-review-planner.md** - Plans review structure and domain decomposition
2. **domain-literature-researcher.md** - Produces compact structured bibliographies per domain (1500-3000 words)
3. **synthesis-planner.md** - Designs narrative structure for the review
4. **synthesis-writer.md** - Writes publication-ready literature review
5. **sota-review-editor.md** - Reviews and polishes against best practices
6. **novelty-assessor.md** - Assesses originality and provides strategic recommendations

## Workflow Phases

### Phase 1: Planning & User Collaboration
- **Agent**: `@literature-review-planner`
- **Output**: `lit-review-plan.md`
- **Process**: Analyzes research idea, decomposes into 3-8 searchable domains
- **User Input**: Review and approve plan (human-in-the-loop)

### Phase 2: Parallel Literature Search
- **Agent**: `@domain-literature-researcher` (multiple instances in parallel)
- **Output**: `literature-domain-1.md`, `literature-domain-2.md`, etc. (compact bibliographies: 1500-3000 words each)
- **Process**: Each agent searches and produces structured bibliographies with: Citation, Core Argument (2-3 sentences), Relevance (2-3 sentences), Position/Debate, Importance level
- **Key Feature**: Parallel execution + compact format enables synthesis-planner to read all domains
- **Architecture**: Multiple files (one per domain) created independently

### Phase 3: Synthesis Planning
- **Agent**: `@synthesis-planner`
- **Output**: `synthesis-outline.md`
- **Process**: Designs narrative structure, organizes literature thematically, plans gap analysis

### Phase 4: Synthesis Writing (Multi-Section)
- **Agent**: `@synthesis-writer` (invoked once per section)
- **Output**: `synthesis-section-1.md`, `synthesis-section-2.md`, etc. → assembled into `state-of-the-art-review-draft.md`
- **Process**: Each section written to separate file; orchestrator assembles sections into final draft
- **Key Feature**: Section-by-section writing (5-6 sections) with only relevant papers per section (~5k words input)
- **Architecture**: Multiple files (one per section) created independently, then concatenated

### Phase 5: Editorial Review
- **Agent**: `@sota-review-editor`
- **Output**: `state-of-the-art-review-final.md`, `editorial-notes.md`
- **Process**: Reviews against best practices, polishes prose, ensures publication readiness

### Phase 6: Novelty Assessment
- **Agent**: `@novelty-assessor`
- **Output**: `executive-assessment.md`
- **Process**: Assesses originality, competitive positioning, provides strategic recommendations

## Key Features

### Context Preservation
- **Isolated Contexts**: Each agent uses its own context window
- **Efficient Orchestration**: Orchestrator context stays minimal
- **Compact Output**: Domain researchers produce 1500-3000 word bibliographies (not 8000+ word prose)
- **Section-by-Section Writing**: Synthesis-writer reads only relevant papers per section (~5k words, not all 24k)
- **Task Persistence**: `task-progress.md` enables resume across conversations if context limit hit

### Parallelization
- **Phase 2**: Multiple domain researchers execute simultaneously
- **Speed**: 5x faster than sequential for comprehensive reviews
- **Scalability**: Can deploy 2-8 researchers based on project scope

### Iterative Refinement
- **User Checkpoints**: Human-in-the-loop mode allows review at each phase
- **Resume Capability**: Task list enables picking up from interruption
- **Editorial Polish**: Dedicated editing phase ensures quality

### Standardized Format
- **Literature Entries**: Compact format with Citation, Core Argument (2-3 sentences), Relevance (2-3 sentences), Position/Debate, Importance (High/Medium/Low)
- **Efficient for Synthesis**: Short entries enable synthesis-planner to read all domains without context overflow
- **Section Files**: Each synthesis section written to separate file, then assembled (mirrors Phase 2 architecture)
- **Gap Integration**: Gaps identified throughout, not just at end

## Usage

### Invoking the Workflow

```
I need a comprehensive state-of-the-art literature review for my research proposal on [topic].
```

The `@research-proposal-orchestrator` will automatically activate and guide you through the workflow.

### Execution Modes

**Autopilot Mode**:
- Execute all 6 phases automatically
- Present complete package at end
- Typical duration: 60-90 minutes
- Saves task progress for resume capability

**Human-in-the-Loop Mode**:
- Review and approve after each phase
- Iterate on plan, structure, or content as needed
- More interactive but ensures perfect alignment

## Output Structure

After complete workflow, you receive:

```
research-proposal-literature-review/
├── task-progress.md                      # Progress tracker (enables resume)
├── lit-review-plan.md                    # Phase 1
├── literature-domain-1.md                # Phase 2 (compact: 1500-3000 words)
├── literature-domain-2.md                # Phase 2 (compact: 1500-3000 words)
├── ...
├── synthesis-outline.md                  # Phase 3
├── synthesis-section-1.md                # Phase 4 (individual sections)
├── synthesis-section-2.md                # Phase 4 (individual sections)
├── synthesis-section-N.md                # Phase 4 (individual sections)
├── state-of-the-art-review-draft.md     # Phase 4 (assembled from sections)
├── state-of-the-art-review-final.md     # Phase 5
├── editorial-notes.md                    # Phase 5
└── executive-assessment.md               # Phase 6
```

## Integration with Existing Skills

These agents can reference your existing analytical philosophy skills:
- `philosophical-literature` skill provides search strategies
- `argument-reconstruction` skill guides argument analysis
- `conceptual-analysis` skill informs gap identification

The hybrid approach combines agent context isolation with skill domain knowledge.

## Comparison with Skill-Based Approach

### Skill-Based Meta-Orchestrator (Current)
- ✅ Excellent domain knowledge
- ✅ Task routing
- ❌ No context isolation
- ❌ No parallel execution
- ❌ Context window fills quickly

### Agent-Based Orchestrator (This System)
- ✅ Context isolation per agent
- ✅ Parallel execution (Phase 2: domains, Phase 4: sections)
- ✅ Iterative loops possible
- ✅ Orchestrator context preserved
- ✅ Scalable to large projects
- ✅ Multi-file-then-assemble pattern (Phase 2 & 4)
- ✅ Can still use skill knowledge

## Technical Details

### Models Used
- **Orchestrator**: Sonnet (strategic reasoning + task persistence)
- **Researchers**: Sonnet (literature search + compact bibliography generation)
- **Planner**: Sonnet (strategic planning + efficient reading)
- **Writer**: Sonnet (academic prose)
- **Editor**: Sonnet (quality assessment)
- **Assessor**: Sonnet (strategic analysis)

### Context Management
- Each phase agent: Isolated context (can use 50k+ tokens for search)
- Domain researchers: Output compact bibliographies (1500-3000 words, not 8000+)
- Synthesis-writer: Reads only relevant papers per section (~5k words, not all 24k)
- Orchestrator: Maintains minimal context via task-progress.md
- Synthesis-planner: Can read all 7 domains (7 × 3000 = ~21k words max)
- Communication: File-based (agents write, orchestrator tracks progress and assembles)

### File-Based Communication
- Agents write comprehensive results to files
- Multi-file pattern: Phase 2 (domains) and Phase 4 (sections) write separate files
- Orchestrator assembles multi-file outputs (concatenation)
- Preserves all intermediate work for transparency
- Enables human review at any checkpoint
- Easy to revise individual sections or domains

## Expected Performance

### Comprehensive Review (5-8 domains, 40-80 papers)
- **Duration**: 60-90 minutes
- **Output**: 6000-9000 word review
- **Citations**: 40-80 papers (compact bibliographies: 10-15k total words for synthesis-planner)
- **Gaps**: 3-5 specific, actionable gaps identified
- **Resume**: Can continue from interruption via task-progress.md

### Focused Review (3-4 domains, 20-40 papers)
- **Duration**: 30-45 minutes
- **Output**: 3000-5000 word review
- **Citations**: 20-40 papers (compact bibliographies: 5-8k total words)
- **Gaps**: 2-3 specific gaps identified

## Quality Standards

All outputs meet:
- ✅ Publication-ready academic prose
- ✅ Proper citation integration (not just listing)
- ✅ Clear, specific gap analysis
- ✅ Explicit connection to research project
- ✅ Strategic positioning for funding/publication
- ✅ Honest novelty assessment
- ✅ Context-efficient (can complete without hitting limits)
- ✅ Modular architecture (easy to revise individual sections)

## Future Enhancements

Potential additions:
- Specialized agents for interdisciplinary research
- Optional validation phase for citation accuracy (if needed)
- Integration with citation management tools
- Automated figure generation for literature maps
- Comparative analysis across multiple research ideas
- Funder-specific formatting agents

## References

**Inspired by**:
- LiRA Framework (arXiv:2510.05138) - Multi-agent literature review generation
- claude-code-heavy - Parallel research orchestration
- wshobson/agents - Sequential pipeline patterns
- Anthropic Agent SDK best practices

## Authors

Created for the analytical philosophy skills system.
Designed for academic philosophers, graduate students, and researchers.
