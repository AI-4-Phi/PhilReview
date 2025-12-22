# Literature Review Agent Improvements - Implementation Plan

## Overview

This plan addresses 5 critical improvements to the literature review system:
1. Fix orchestrator agent coordination
2. Parallelize domain researcher searches
3. Add progress feedback
4. Add retry logic with exponential backoff
5. Implement result caching

## Current Architecture Analysis

### Orchestrator (research-proposal-orchestrator.md)
- **Problem**: Lines 68, 80 use `@agent-name` syntax instead of Task tool
- **Impact**: Creates malformed message sequences, violates Claude API requirements
- **Pattern**: Fan-out-fan-in with file-based coordination

### Domain Researcher (domain-literature-researcher.md)
- **Current**: Sequential bash calls to search scripts (phases 1-5)
- **Bottleneck**: 20-40+ serial API calls, ~30-45 min per domain
- **Pattern**: Isolated context, single BibTeX output

### Search Scripts
- **Infrastructure**: rate_limiter.py with file-based coordination
- **ExponentialBackoff**: Already implemented (lines 118-181)
- **Output**: JSON with standardized schema
- **No retry**: Scripts fail on API errors without retry

## Implementation Plan

### Fix #1: Orchestrator Coordination

**Goal**: Replace `@agent-name` syntax with proper Task tool invocations

**Files to Modify**:
- `.claude/agents/research-proposal-orchestrator.md`

**Changes**:
```markdown
# BEFORE (lines 68, 80, etc.):
2. Invoke `@literature-review-planner` with research idea

# AFTER:
2. Use Task tool to invoke literature-review-planner:
   ```
   Task tool with:
   - subagent_type: "literature-review-planner"
   - prompt: [research idea + context]
   - description: "Plan literature review domains"
   ```
```

**Specific Line Changes**:
- Line 68: `@literature-review-planner` → Task tool invocation
- Line 80: `@domain-literature-researcher` → Task tool invocation (with parallel guidance)
- Line 92: `@synthesis-planner` → Task tool invocation
- Line 107: `@synthesis-writer` → Task tool invocation

**Testing**: Run orchestrator on test research idea, verify it completes Phase 1

**Dependencies**: None - standalone fix

---

### Fix #2: Parallelize Domain Researcher Searches

**Goal**: Enable concurrent API searches within a single domain research session

**Impact on Other Fixes**:
- ✅ Works with retry logic (each search retries independently)
- ✅ Works with result caching (cache checked before search)
- ⚠️  Progress feedback must be thread-safe or sequential

**Files to Modify**:
- `.claude/agents/domain-literature-researcher.md`

**Strategy**: Add "Parallel Search Mode" instructions

**Changes to domain-literature-researcher.md**:

Add new section after line 133 (after Phase 3):

```markdown
### Optimized Search Strategy: Parallel Execution

**For maximum speed, launch searches in parallel using a single bash command with background processes:**

```bash
# Launch all searches in parallel (example for Phase 2-3)
(
  python .claude/skills/philosophy-research/scripts/search_philpapers.py "{topic}" > /tmp/philpapers_${topic}.json &
  python .claude/skills/philosophy-research/scripts/s2_search.py "{topic}" --field Philosophy --year 2020-2025 > /tmp/s2_general_${topic}.json &
  python .claude/skills/philosophy-research/scripts/search_openalex.py "{topic}" --year 2020-2025 > /tmp/openalex_${topic}.json &
  python .claude/skills/philosophy-research/scripts/search_arxiv.py "{topic}" --category cs.AI --recent > /tmp/arxiv_${topic}.json &
  wait  # Wait for all background jobs to complete
)
```

**Then aggregate results:**
```bash
cat /tmp/philpapers_${topic}.json /tmp/s2_general_${topic}.json /tmp/openalex_${topic}.json /tmp/arxiv_${topic}.json | \
  python -c "import json, sys; results = []; [results.extend(json.load(open(f))['results']) for f in sys.argv[1:]]; print(json.dumps({'results': results}))"
```

**Benefits**:
- 4-5x speedup (parallel instead of serial)
- Rate limiter handles cross-process coordination via file locks
- Each search has independent retry logic

**When to use**:
- ✅ Use for Phase 2-3 broad searches
- ⚠️  Use sequentially for Phase 4-5 (citation chaining depends on earlier results)
```

**Testing**: Run domain researcher, verify parallel searches complete correctly

**Dependencies**:
- Requires Fix #3 (progress feedback) to be thread-aware
- Enhanced by Fix #4 (retry logic) for robustness

---

### Fix #3: Add Progress Feedback

**Goal**: Emit status messages during long-running searches

**Impact on Other Fixes**:
- Must coordinate with Fix #2 (parallel searches)
- Works with Fix #4 (retry shows retry attempts)
- Works with Fix #5 (cache shows "using cached result")

**Files to Modify**:
- All search scripts in `.claude/skills/philosophy-research/scripts/`:
  - `s2_search.py`
  - `s2_batch.py`
  - `search_openalex.py`
  - `search_arxiv.py`
  - `search_philpapers.py`
  - `search_sep.py`
  - `fetch_sep.py`
  - `verify_paper.py`

**Strategy**: Add stderr-based progress messages (leaves stdout for JSON)

**Implementation Pattern** (apply to all scripts):

```python
import sys

def log_progress(message: str) -> None:
    """Emit progress to stderr (visible to user, doesn't break JSON output)."""
    print(f"[{sys.argv[0].split('/')[-1]}] {message}", file=sys.stderr, flush=True)

# Usage in scripts:
log_progress(f"Searching Semantic Scholar for '{query}'...")
# ... make API call ...
log_progress(f"Found {len(results)} results")
```

**Specific Integration Points**:

For `s2_search.py` (add after line 150):
```python
log_progress(f"Searching Semantic Scholar: '{query}' (year={year_range}, field={field})")
# ... after search ...
log_progress(f"Semantic Scholar returned {len(results)} papers")
```

For `search_openalex.py`:
```python
log_progress(f"Searching OpenAlex: '{query}'...")
log_progress(f"OpenAlex returned {len(results)} works")
```

For all scripts with retry (after Fix #4):
```python
log_progress(f"API error, retrying (attempt {attempt+1}/{max_attempts})...")
log_progress(f"Retry successful after {backoff.last_delay:.1f}s backoff")
```

**Testing**: Run search, verify stderr shows progress while stdout has valid JSON

**Dependencies**:
- Independent of other fixes
- Enhanced by Fix #4 (shows retry progress)

---

### Fix #4: Add Retry Logic with Exponential Backoff

**Goal**: Handle transient API failures gracefully

**Impact on Other Fixes**:
- ✅ Works with Fix #2 (parallel searches retry independently)
- ✅ Works with Fix #3 (progress shows retry attempts)
- ⚠️  Cache should be checked BEFORE retry loop (don't retry if cached)

**Files to Modify**:
- All search scripts (same list as Fix #3)
- `rate_limiter.py` already has ExponentialBackoff - just needs integration

**Strategy**: Wrap API calls in retry loop with exponential backoff

**Implementation Pattern** (apply to all scripts):

```python
from rate_limiter import get_limiter, ExponentialBackoff

def search_with_retry(query: str, max_attempts: int = 5) -> dict:
    """Execute search with retry logic."""
    limiter = get_limiter("semantic_scholar")  # or appropriate API
    backoff = ExponentialBackoff(max_attempts=max_attempts, base_delay=1.0, max_delay=60.0)

    for attempt in range(max_attempts):
        try:
            limiter.wait()
            response = requests.get(url, headers=headers, params=params, timeout=30)
            limiter.record()

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 429:  # Rate limit
                log_progress(f"Rate limited, backing off (attempt {attempt+1}/{max_attempts})...")
                if not backoff.wait(attempt):
                    output_error(query, "rate_limit", "Max retry attempts exceeded after rate limiting", exit_code=3)
                continue

            elif response.status_code >= 500:  # Server error
                log_progress(f"Server error {response.status_code}, retrying (attempt {attempt+1}/{max_attempts})...")
                if not backoff.wait(attempt):
                    output_error(query, "api_error", f"Server error persists after {max_attempts} attempts", exit_code=3)
                continue

            else:  # Other error (don't retry)
                output_error(query, "http_error", f"HTTP {response.status_code}: {response.text[:200]}", exit_code=3)

        except requests.exceptions.Timeout:
            log_progress(f"Timeout, retrying (attempt {attempt+1}/{max_attempts})...")
            if not backoff.wait(attempt):
                output_error(query, "timeout", "Request timed out after multiple attempts", exit_code=3)
            continue

        except requests.exceptions.RequestException as e:
            log_progress(f"Connection error: {e}, retrying (attempt {attempt+1}/{max_attempts})...")
            if not backoff.wait(attempt):
                output_error(query, "connection_error", str(e), exit_code=3)
            continue

    output_error(query, "max_retries", f"Failed after {max_attempts} attempts", exit_code=3)
```

**Specific Changes per Script**:

1. **s2_search.py** - wrap lines ~150-180 in retry logic
2. **search_openalex.py** - wrap API call in retry logic
3. **search_arxiv.py** - wrap arxiv API call in retry logic
4. **search_philpapers.py** - wrap Brave search in retry logic (already has rate limiting)
5. **search_sep.py** - wrap Brave search in retry logic
6. **fetch_sep.py** - wrap requests.get in retry logic
7. **verify_paper.py** - wrap CrossRef API call in retry logic

**Error Handling Matrix**:
| Error Type | Retry? | Backoff? | Max Attempts |
|------------|--------|----------|--------------|
| 429 (rate limit) | ✅ Yes | ✅ Yes | 5 |
| 500-599 (server) | ✅ Yes | ✅ Yes | 5 |
| Timeout | ✅ Yes | ✅ Yes | 3 |
| Connection error | ✅ Yes | ✅ Yes | 3 |
| 400-499 (client) | ❌ No | ❌ No | 1 |

**Testing**:
1. Mock API returning 429, verify exponential backoff
2. Mock API with intermittent failures, verify eventual success
3. Mock permanent failure, verify max attempts and clean exit

**Dependencies**:
- Works with Fix #5 (check cache before entering retry loop)

---

### Fix #5: Implement Result Caching

**Goal**: Share search results across domain researchers to avoid duplicate API calls

**Impact on Other Fixes**:
- ✅ Works with Fix #2 (parallel searches can all check cache)
- ✅ Works with Fix #3 (shows "using cached result" progress message)
- ✅ Works with Fix #4 (cache checked BEFORE retry loop - no retries if cached)

**Files to Create**:
- `.claude/skills/philosophy-research/scripts/search_cache.py` (new)

**Files to Modify**:
- All search scripts (integrate cache check)

**Strategy**: File-based cache similar to rate_limiter, with cache invalidation

**search_cache.py Implementation**:

```python
"""
Shared search result cache for cross-agent coordination.

Caches search results to avoid duplicate API calls when multiple domain
researchers search for similar topics.

Usage:
    from search_cache import SearchCache

    cache = SearchCache()

    # Check cache before searching
    cached = cache.get("semantic_scholar", "free will compatibilism", {"year": "2020-2025"})
    if cached:
        return cached

    # After successful search:
    cache.put("semantic_scholar", "free will compatibilism", {"year": "2020-2025"}, results)
"""

import fcntl
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional


class SearchCache:
    """
    File-based search cache with TTL and size limits.
    Uses file locking to prevent race conditions across agents.
    """

    CACHE_DIR = Path("/tmp/philosophy_research_cache")
    MAX_AGE_SECONDS = 24 * 60 * 60  # 24 hours
    MAX_CACHE_SIZE_MB = 100  # Total cache size limit

    def __init__(self):
        self.CACHE_DIR.mkdir(exist_ok=True)

    def _get_cache_key(self, source: str, query: str, params: dict) -> str:
        """Generate cache key from search parameters."""
        # Normalize params for consistent hashing
        param_str = json.dumps(params, sort_keys=True)
        key_input = f"{source}:{query}:{param_str}"
        return hashlib.sha256(key_input.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path to cache file."""
        return self.CACHE_DIR / f"search_{cache_key}.json"

    def get(self, source: str, query: str, params: dict = None) -> Optional[dict]:
        """
        Retrieve cached results if available and fresh.

        Args:
            source: API source (e.g., "semantic_scholar", "openalex")
            query: Search query string
            params: Additional search parameters (year range, filters, etc.)

        Returns:
            Cached results dict or None if not found/expired
        """
        if params is None:
            params = {}

        cache_key = self._get_cache_key(source, query, params)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        # Check age
        age = time.time() - cache_path.stat().st_mtime
        if age > self.MAX_AGE_SECONDS:
            cache_path.unlink()  # Remove stale cache
            return None

        # Read cache with lock
        try:
            with open(cache_path, "r") as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
            return data
        except (json.JSONDecodeError, IOError):
            cache_path.unlink()  # Remove corrupt cache
            return None

    def put(self, source: str, query: str, params: dict, results: dict) -> None:
        """
        Store search results in cache.

        Args:
            source: API source
            query: Search query string
            params: Additional search parameters
            results: Results dict to cache
        """
        if params is None:
            params = {}

        cache_key = self._get_cache_key(source, query, params)
        cache_path = self._get_cache_path(cache_key)

        # Check total cache size and evict if needed
        self._evict_if_needed()

        # Write cache with lock
        with open(cache_path, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                json.dump(results, f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache exceeds size limit."""
        cache_files = list(self.CACHE_DIR.glob("search_*.json"))

        # Calculate total size
        total_size = sum(f.stat().st_size for f in cache_files) / (1024 * 1024)  # MB

        if total_size > self.MAX_CACHE_SIZE_MB:
            # Sort by modification time (oldest first)
            cache_files.sort(key=lambda f: f.stat().st_mtime)

            # Remove oldest until under limit
            for cache_file in cache_files:
                cache_file.unlink()
                total_size = sum(f.stat().st_size for f in self.CACHE_DIR.glob("search_*.json")) / (1024 * 1024)
                if total_size <= self.MAX_CACHE_SIZE_MB * 0.8:  # Leave 20% buffer
                    break

    def clear(self) -> int:
        """Clear all cached results. Returns number of files removed."""
        count = 0
        for cache_file in self.CACHE_DIR.glob("search_*.json"):
            cache_file.unlink()
            count += 1
        return count

    def stats(self) -> dict:
        """Get cache statistics."""
        cache_files = list(self.CACHE_DIR.glob("search_*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            "entries": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "max_size_mb": self.MAX_CACHE_SIZE_MB,
            "max_age_hours": self.MAX_AGE_SECONDS / 3600
        }
```

**Integration into Search Scripts**:

Pattern for each search script:

```python
from search_cache import SearchCache

def main():
    # ... parse arguments ...

    # Check cache FIRST (before retry loop)
    cache = SearchCache()
    params = {"year": year_range, "field": field, "limit": limit}  # Normalize params
    cached_result = cache.get("semantic_scholar", query, params)

    if cached_result:
        log_progress(f"Using cached results (age: {(time.time() - cached_result['cached_at']) / 60:.0f}m)")
        print(json.dumps(cached_result))
        sys.exit(0)

    # Not cached - proceed with search + retry logic
    results = search_with_retry(query, params)

    # Cache successful results
    results['cached_at'] = time.time()
    cache.put("semantic_scholar", query, params, results)

    print(json.dumps(results))
```

**Cache Key Parameters by Script**:
- `s2_search.py`: query, year, field, limit, bulk
- `search_openalex.py`: query, year, min_citations
- `search_arxiv.py`: query, category, recent
- `search_philpapers.py`: query, recent
- `search_sep.py`: query (SEP is stable, long TTL)

**Testing**:
1. Run search twice, verify second uses cache
2. Parallel domain researchers, verify cache sharing
3. Wait 24h, verify cache expiration
4. Fill cache to 100MB, verify eviction

**Dependencies**:
- Should be checked BEFORE retry loop in Fix #4

---

## Implementation Order

Given the interactions, implement in this order:

1. **Fix #3 (Progress Feedback)** - Independent, helps debug other fixes
2. **Fix #4 (Retry Logic)** - Independent, integrates with progress
3. **Fix #5 (Result Caching)** - Integrates with retry (cache checked first)
4. **Fix #2 (Parallelization)** - Leverages 3,4,5 for robust parallel execution
5. **Fix #1 (Orchestrator)** - Uses improved agents from 2-5

## Testing Strategy

### Per-Fix Testing
Each fix gets tested in isolation before moving to next:
- Unit tests for new modules (search_cache.py)
- Integration tests for modified scripts
- End-to-end test for agent modifications

### Full Integration Test
After all fixes:
1. Run complete literature review on test topic
2. Verify all phases complete
3. Measure performance improvement
4. Confirm cache sharing across domains

## Success Metrics

- **Orchestrator**: Completes full review without manual intervention
- **Parallelization**: Domain research ~10-15 min (down from 30-45 min)
- **Progress**: Clear status messages during execution
- **Retry**: 95%+ success rate on transient failures
- **Cache**: 50%+ cache hit rate on second domain using similar queries

## Rollback Plan

Each fix in separate commit. If issues arise:
1. Identify problematic commit via git log
2. `git revert <commit-hash>`
3. Test rollback works
4. Debug issue
5. Re-apply fix

## File Change Summary

**New Files**:
- `.claude/skills/philosophy-research/scripts/search_cache.py`
- `IMPLEMENTATION_PLAN.md` (this file)

**Modified Files**:
- `.claude/agents/research-proposal-orchestrator.md` (Fix #1)
- `.claude/agents/domain-literature-researcher.md` (Fix #2)
- `.claude/skills/philosophy-research/scripts/s2_search.py` (Fixes #3, #4, #5)
- `.claude/skills/philosophy-research/scripts/s2_batch.py` (Fixes #3, #4, #5)
- `.claude/skills/philosophy-research/scripts/search_openalex.py` (Fixes #3, #4, #5)
- `.claude/skills/philosophy-research/scripts/search_arxiv.py` (Fixes #3, #4, #5)
- `.claude/skills/philosophy-research/scripts/search_philpapers.py` (Fixes #3, #4, #5)
- `.claude/skills/philosophy-research/scripts/search_sep.py` (Fixes #3, #4, #5)
- `.claude/skills/philosophy-research/scripts/fetch_sep.py` (Fixes #3, #4)
- `.claude/skills/philosophy-research/scripts/verify_paper.py` (Fixes #3, #4)

**Total**: 1 new + 11 modified = 12 files
