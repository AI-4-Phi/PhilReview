# Research Proposal Literature Review Agents

**LiRA-Inspired Multi-Agent Workflow for State-of-the-Art Reviews**

## Overview

This directory contains a sophisticated 5-phase agent-based workflow for generating focused, insight-driven literature reviews for research proposals. The system is inspired by the LiRA (Literature Review Agents) framework but adapted specifically for philosophical research proposals, emphasizing analytical depth over comprehensive coverage.

**Key Features**: 
- Domain researchers output **valid BibTeX files** (`.bib`) for direct Zotero import
- Focused reviews words) emphasizing key debates and research gaps

## Recent Optimizations (Context Window Efficiency)

- **BibTeX output**: Domain researchers now produce valid BibTeX files (`.bib`) instead of prose reviews
- **Citation validation**: Phase 3 validates citations, removes unverified entries to `unverified-sources.bib`
- **Task persistence**: Added `task-progress.md` for cross-conversation resume capability
- **Zotero integration**: Users can directly import BibTeX files into Zotero with one click
- **Result**: Synthesis-planner can now read all 7 domains without context overflow; users get verified, reference-manager-ready bibliographies

## Agent Architecture

### Meta-Orchestrator
- **research-proposal-orchestrator.md** - Coordinates the entire 6-phase workflow with task persistence

### Phase Agents

1. **literature-review-planner.md** - Plans review structure and domain decomposition
2. **domain-literature-researcher.md** - Produces valid BibTeX files (`.bib`) per domain with rich metadata in @comment entries and note fields
3. **citation-validator.md** - Validates citations, removes unverified entries to `unverified-sources.bib`
4. **synthesis-planner.md** - Designs tight narrative structure for focused  review
5. **synthesis-writer.md** - Writes focused, insight-driven literature review emphasizing key debates and gaps

## Workflow Phases

### Phase 1: Planning & User Collaboration
- **Agent**: `@literature-review-planner`
- **Output**: `lit-review-plan.md`
- **Process**: Analyzes research idea, decomposes into 3-8 searchable domains
- **User Input**: Review and approve plan (human-in-the-loop)

### Phase 2: Parallel Literature Search
- **Agent**: `@domain-literature-researcher` (multiple instances in parallel)
- **Output**: `literature-domain-1.bib`, `literature-domain-2.bib`, etc. (valid BibTeX files)
- **Process**: Each agent searches and produces BibTeX bibliography with:
  - Domain metadata in @comment entries (overview, gaps, synthesis guidance)
  - Standard BibTeX entries (@article, @book, etc.) with proper citation data
  - Rich metadata in `note` fields (Core Argument, Relevance, Position)
  - Importance levels in `keywords` fields (High/Medium/Low)
- **Key Feature**: Parallel execution + BibTeX format enables direct Zotero import AND synthesis-planner reading
- **Architecture**: Multiple files (one per domain) created independently

### Phase 3: Citation Validation
- **Agent**: `@citation-validator`
- **Output**: `validation-report.md`, `unverified-sources.bib`, modified `.bib` files (cleaned)
- **Process**: Validates every BibTeX entry (DOI check, Google Scholar verification), removes unverified entries to `unverified-sources.bib`, preserves only verified papers in domain files
- **Key Feature**: Ensures only real, verified papers make it to Zotero import and synthesis phases

### Phase 4: Synthesis Planning
- **Agent**: `@synthesis-planner`
- **Output**: `synthesis-outline.md`
- **Process**: Designs tight narrative structure (3-4 sections, 3000-4000 words), selects 15-25 papers to cite, emphasizes key debates and specific gaps
- **Key Feature**: Focus on analytical insight over comprehensive coverage

### Phase 5: Synthesis Writing (Multi-Section)
- **Agent**: `@synthesis-writer` (invoked once per section)
- **Output**: `synthesis-section-1.md`, `synthesis-section-2.md`, etc. → assembled into `literature-review-final.md`
- **Process**: Each section written to separate file with specific word targets; orchestrator assembles into final review
- **Key Feature**: 
  - Section-by-section writing 
  - Analytical depth over comprehensive coverage
- **Architecture**: Multiple files (one per section) created independently, then concatenated

## Key Features

### Context Preservation
- **Isolated Contexts**: Each agent uses its own context window
- **Efficient Orchestration**: Orchestrator context stays minimal
- **BibTeX Output**: Domain researchers produce valid `.bib` files (not prose reviews)
- **Section-by-Section Writing**: Synthesis-writer reads only relevant papers per section (~5k words, not all 24k)
- **Zotero Integration**: BibTeX files can be directly imported into reference managers
- **Task Persistence**: `task-progress.md` enables resume across conversations if context limit hit

### Parallelization
- **Phase 2**: Multiple domain researchers execute simultaneously
- **Speed**: 5x faster than sequential for comprehensive reviews
- **Scalability**: Can deploy 2-8 researchers based on project scope

### Iterative Refinement
- **User Checkpoints**: Human-in-the-loop mode allows review at each phase
- **Citation Validation**: Ensures only verified papers proceed to synthesis
- **Resume Capability**: Task list enables picking up from interruption
- **Editorial Polish**: Dedicated editing phase ensures quality

### Standardized Format
- **BibTeX Format**: Valid `.bib` files with standard citation fields (author, title, journal, year, doi, etc.)
- **Rich Metadata**: Domain overview in @comment entries; paper analysis in note fields
- **Direct Import**: Users can import BibTeX files directly into Zotero
- **Agent-Readable**: Synthesis agents parse @comment and note fields for planning and writing
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
- Execute all 5 phases automatically
- Present focused literature review at end
- Typical duration: 45-60 minutes
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
├── literature-domain-1.bib               # Phase 2 (BibTeX - import to Zotero)
├── literature-domain-2.bib               # Phase 2 (BibTeX - import to Zotero)
├── literature-domain-N.bib               # Phase 2 (BibTeX - import to Zotero)
├── validation-report.md                  # Phase 3 (validation results)
├── unverified-sources.bib                # Phase 3 (removed entries - DO NOT import)
├── synthesis-outline.md                  # Phase 4
├── synthesis-section-1.md                # Phase 5 (individual sections)
├── synthesis-section-2.md                # Phase 5 (individual sections)
├── synthesis-section-N.md                # Phase 5 (individual sections)
└── literature-review-final.md            # Phase 5 (assembled, 3000-4000 words)
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
- ✅ Parallel execution (Phase 2: domains, Phase 5: sections)
- ✅ Citation validation (Phase 3: ensures only verified papers)
- ✅ Orchestrator context preserved
- ✅ Scalable to large projects
- ✅ Multi-file-then-assemble pattern (Phase 2 & 5)
- ✅ Can still use skill knowledge

## Technical Details

### Models Used
- **Orchestrator**: Sonnet (strategic reasoning + task persistence)
- **Researchers**: Sonnet (literature search + BibTeX generation)
- **Validator**: Sonnet (citation verification)
- **Planner**: Sonnet (strategic planning for focused reviews)
- **Writer**: Sonnet (tight, analytical academic prose)

### Context Management
- Each phase agent: Isolated context (can use 50k+ tokens for search)
- Domain researchers: Output valid BibTeX files (`.bib`) with structured metadata
- Synthesis-writer: Reads only relevant BibTeX files per section (3-5 papers)
- Orchestrator: Maintains minimal context via task-progress.md
- Synthesis-planner: Can read all 7 BibTeX domain files comfortably
- Communication: File-based (agents write, orchestrator tracks progress and assembles)

### File-Based Communication
- Agents write comprehensive results to files
- Multi-file pattern: Phase 2 (domains) and Phase 4 (sections) write separate files
- Orchestrator assembles multi-file outputs (concatenation)
- BibTeX format: Phase 2 outputs are valid `.bib` files for Zotero import
- Preserves all intermediate work for transparency
- Enables human review at any checkpoint
- Easy to revise individual sections or domains
- Users can import BibTeX files to reference manager immediately

## Expected Performance

### Focused Review 
- **Citations**: 15-25 papers cited in review (selected from 40-80 found in domain search)
- **BibTeX**: 5-8 `.bib` files ready for Zotero import (all found papers)
- **Gaps**: 2-3 specific, well-defined gaps
- **Focus**: Analytical depth over comprehensive coverage
- **Resume**: Can continue from interruption via task-progress.md

### Quick Review (3-4 domains, 10-15 papers cited)
- **Duration**: 30-40 minutes
- **Output**: 2500-3000 word review
- **Citations**: 10-15 papers cited in review
- **BibTeX**: 3-4 `.bib` files ready for Zotero import
- **Gaps**: 1-2 specific gaps identified

## Quality Standards

All outputs meet:
- ✅ Focused, insight-driven prose 
- ✅ **Validated citations** (only verified papers in BibTeX files)
- ✅ Clear, specific gap analysis (2-3 gaps)
- ✅ Explicit connection to research project throughout
- ✅ Strategic positioning for funding/publication
- ✅ Analytical depth over comprehensive coverage
- ✅ Context-efficient (can complete without hitting limits)
- ✅ Modular architecture (easy to revise individual sections)

## Future Enhancements

Potential additions:
- Optional editorial review phase (for users who want 6000+ word comprehensive reviews)
- Optional novelty assessment phase (executive summary with strategic recommendations)
- Specialized agents for interdisciplinary research
- Enhanced Zotero integration (automated collection creation, tagging)
- Automated figure generation for literature maps
- Comparative analysis across multiple research ideas
- Funder-specific formatting agents
- Export to other formats (RIS, EndNote, etc.)

## References

**Inspired by**:
- LiRA Framework (arXiv:2510.05138) - Multi-agent literature review generation
- claude-code-heavy - Parallel research orchestration
- wshobson/agents - Sequential pipeline patterns
- Anthropic Agent SDK best practices

## Authors

Created for the analytical philosophy skills system.
Designed for academic philosophers, graduate students, and researchers.
