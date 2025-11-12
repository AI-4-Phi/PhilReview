# Research Proposal Orchestrator Architecture

## Design Pattern: Multi-File-Then-Assemble

This orchestrator uses a consistent architectural pattern for computationally intensive phases: **multiple agents write to separate files, then orchestrator assembles the final output**.

## Pattern Implementation

### Phase 2: Parallel Domain Literature Search

**Pattern**: Multiple researchers → Individual files → Validated together

```
Input: lit-review-plan.md (identifies 7 domains)

Parallel Execution:
├── @domain-literature-researcher #1 → literature-domain-1.md
├── @domain-literature-researcher #2 → literature-domain-2.md
├── @domain-literature-researcher #3 → literature-domain-3.md
├── @domain-literature-researcher #4 → literature-domain-4.md
├── @domain-literature-researcher #5 → literature-domain-5.md
├── @domain-literature-researcher #6 → literature-domain-6.md
└── @domain-literature-researcher #7 → literature-domain-7.md

Each agent:
- Isolated context
- Searches specific domain
- Produces compact bibliography (1500-3000 words)
- Independent of other researchers

Orchestrator:
- Tracks completion in task-progress.md
- All files used together by synthesis-planner
- No explicit assembly needed (planner reads all)
```

### Phase 4: Section-by-Section Synthesis Writing

**Pattern**: Multiple writers → Individual section files → Assembled into draft

```
Input: synthesis-outline.md (identifies 5 sections)

Sequential/Parallel Execution:
├── @synthesis-writer #1 → synthesis-section-1.md (Introduction)
├── @synthesis-writer #2 → synthesis-section-2.md (Theoretical Foundations)
├── @synthesis-writer #3 → synthesis-section-3.md (Current State-of-the-Art)
├── @synthesis-writer #4 → synthesis-section-4.md (Research Gaps)
└── @synthesis-writer #5 → synthesis-section-5.md (Conclusion)

Each invocation:
- Isolated context
- Reads only relevant domain files (~5k words, not all 24k)
- Writes one complete section
- Independent markdown file

Orchestrator:
- Tracks completion in task-progress.md
- After all sections complete:
  cat synthesis-section-*.md > state-of-the-art-review-draft.md
```

## Benefits of This Pattern

### 1. Context Efficiency
- **Phase 2**: Each researcher reads only what it searches (~10k tokens)
- **Phase 4**: Each writer reads only relevant papers (~5k words vs 24k)
- **Reduction**: 80% per invocation in Phase 4

### 2. Parallelization
- **Phase 2**: Can run all 7 researchers simultaneously
- **Phase 4**: Can run sections in parallel (though sequential usually fine)
- **Speed**: 5-7x faster for Phase 2

### 3. Modularity
- Each file is independent
- Can review individual domains/sections
- Can regenerate specific pieces without affecting others
- Easy to see what's complete

### 4. Resilience
- If interrupted, task-progress.md shows which files exist
- Resume by generating missing files only
- Partial progress preserved
- No monolithic failures

### 5. Architecture Consistency
- Same pattern used twice in workflow
- Predictable behavior
- Easy to understand and maintain
- Elegant repetition

## Alternative Considered: Monolithic Approach

### What We Could Have Done (But Didn't)

**Phase 2**: Single researcher agent reads all domains, writes one massive file
- ❌ Context: ~70k words input + output
- ❌ Time: 60-90 minutes sequential
- ❌ Fragile: One failure loses everything
- ❌ Not resumable

**Phase 4**: Single writer reads all domains, writes entire review in one pass
- ❌ Context: 24k input + 8k output = 33k words
- ❌ Quality degradation in long sessions
- ❌ No review points
- ❌ Fragile

### Why Multi-File Pattern Wins

| Aspect | Monolithic | Multi-File Pattern |
|--------|-----------|-------------------|
| **Context per task** | 70k words | 5-10k words |
| **Parallelization** | None | Full (Phase 2), Partial (Phase 4) |
| **Resumability** | Lost on failure | Perfect |
| **Modularity** | None | High |
| **Review points** | None | After each file |
| **Revision** | Regenerate all | Regenerate one file |

## Complete Workflow Context Analysis

```
Phase 1: Planning
├── Input: Research idea (~1k words)
├── Output: lit-review-plan.md (~2k words)
└── Context: ~3k words ✓

Phase 2: Domain Search (MULTI-FILE PATTERN)
├── Per researcher: 
│   ├── Input: Plan excerpt (~500 words)
│   ├── Search: Web (isolated context)
│   └── Output: domain file (~2.5k words)
├── Context per researcher: ~10k words ✓
└── Total output: 7 files × 2.5k = 17.5k words

Phase 3: Synthesis Planning
├── Input: All domain files (~17.5k words) + plan (~2k)
├── Output: synthesis-outline.md (~2.5k words)
└── Context: ~20k words ✓

Phase 4: Synthesis Writing (MULTI-FILE PATTERN)
├── Per section:
│   ├── Input: Outline (~2.5k) + relevant domains (~5k)
│   ├── Output: section file (~1.5k words)
│   └── Context: ~9k words ✓
├── Assembly: cat synthesis-section-*.md > draft.md
└── Total output: 5 files × 1.5k = 7.5k words

Phase 5: Editorial Review
├── Input: Draft (~7.5k words)
├── Output: Final (~8k words) + notes (~1k)
└── Context: ~16k words ✓

Phase 6: Novelty Assessment
├── Input: Final review (~8k words) + idea (~1k)
├── Output: Executive assessment (~2k words)
└── Context: ~11k words ✓
```

**Maximum context in any phase: ~20k words (Phase 3)**
**Far below 200k token limit throughout**

## File Organization

```
research-proposal-literature-review/
├── task-progress.md                      # State tracker
│
├── lit-review-plan.md                    # Phase 1 output
│
├── literature-domain-1.md                # Phase 2 outputs (multi-file)
├── literature-domain-2.md
├── literature-domain-3.md
├── literature-domain-4.md
├── literature-domain-5.md
├── literature-domain-6.md
├── literature-domain-7.md
│
├── synthesis-outline.md                  # Phase 3 output
│
├── synthesis-section-1.md                # Phase 4 outputs (multi-file)
├── synthesis-section-2.md
├── synthesis-section-3.md
├── synthesis-section-4.md
├── synthesis-section-5.md
├── state-of-the-art-review-draft.md     # Phase 4 assembled
│
├── state-of-the-art-review-final.md     # Phase 5 output
├── editorial-notes.md
│
└── executive-assessment.md               # Phase 6 output
```

**Multi-file phases clearly visible**: Phase 2 (7 files) and Phase 4 (5 files)

## Key Design Decisions

### Why Separate Files vs. Appending?

**Considered**: Have synthesis-writer append sections to one file

**Rejected because**:
- Requires reading entire draft so far (context grows)
- Appending logic more complex
- Harder to revise individual sections
- Less consistent with Phase 2 pattern
- Can't parallelize

**Chosen**: Separate files, then assemble

**Benefits**:
- Each invocation is stateless (just write a complete section)
- Context stays constant (~9k words per section)
- Clean separation of concerns
- Mirrors Phase 2 architecture
- Simple concatenation for assembly

### Why Sequential Assembly vs. Streaming?

**Considered**: Have orchestrator stream sections as written

**Rejected because**:
- Adds complexity
- Harder to review individual sections
- Can't easily regenerate one section
- Premature optimization

**Chosen**: Write all sections, then assemble

**Benefits**:
- Simple: `cat synthesis-section-*.md > draft.md`
- All intermediate files preserved
- Can review before assembly
- Can regenerate any section
- Clear completion criteria

## Comparison to Other Orchestration Patterns

### Sequential Pipeline (e.g., wshobson/agents)

```
Agent A → complete → Agent B → complete → Agent C → complete
```

- ✅ Simple to reason about
- ❌ No parallelization
- ❌ Context accumulates

### Fan-Out-Fan-In (This System)

```
        ┌─ Agent 1 → file 1 ─┐
Input ──┼─ Agent 2 → file 2 ─┼── Assemble → Output
        └─ Agent 3 → file 3 ─┘
```

- ✅ Parallelization possible
- ✅ Context stays isolated
- ✅ Resilient to failures
- ✅ Modular outputs

### Monolithic (Traditional)

```
Single Agent → reads everything → writes everything
```

- ❌ Context explosion
- ❌ Fragile
- ❌ Long execution time
- ❌ Not resumable

## Performance Characteristics

### Time Complexity

**Phase 2 (parallel)**:
- Sequential: O(7n) where n = time per domain
- Parallel: O(n) with 7 workers
- **Speedup: 7x**

**Phase 4 (sequential in practice)**:
- Monolithic: O(5n) where n = time per section
- Multi-file: O(5n) but with much better context efficiency
- **Speedup: ~2x due to faster individual sections**

### Space Complexity

**Context usage**:
- Monolithic Phase 4: O(D + S) where D = all domains, S = output size
- Multi-file Phase 4: O(d + s) where d = relevant domains, s = section size
- **Reduction: 80% (24k → 5k words input)**

## Lessons Learned

1. **Multi-file patterns enable parallelization and resilience**
2. **Context efficiency comes from reading only what's needed**
3. **Simple assembly (concatenation) is sufficient**
4. **Architectural consistency (reusing patterns) aids understanding**
5. **Separate files are better than appending for complex workflows**
6. **Task persistence (task-progress.md) makes everything resumable**

## Future Extensions

### Potential Enhancements

1. **True parallel section writing**
   - Currently sequential for simplicity
   - Could parallelize with careful transition management
   - Task-progress.md already supports tracking

2. **Incremental assembly**
   - Stream sections as they complete
   - Would require more complex assembly logic
   - Current approach is sufficient

3. **Dependency graphs**
   - Some sections might depend on others
   - Could build DAG of section dependencies
   - Currently unnecessary (sections are independent)

4. **Caching**
   - Cache domain searches for similar projects
   - Cache section generation for iterative refinement
   - File-based architecture makes this natural

## Conclusion

The **multi-file-then-assemble** pattern is the key architectural insight that makes this orchestrator scalable and context-efficient. By breaking computationally intensive phases (Phase 2 and Phase 4) into multiple independent file outputs, we achieve:

- **80% context reduction** per invocation
- **Parallelization** where beneficial
- **Modularity** and easy revision
- **Resilience** to failures
- **Architectural consistency** across phases

This pattern should be the default for any multi-agent orchestration dealing with large knowledge synthesis tasks.