# Investigation: Incorrect Bibliographic Metadata

## Summary

**Problem**: LLM agents fill in bibliographic metadata from training data instead of using API output, despite explicit instructions not to. This causes incorrect journal names, volumes, pages, and entry types.

**Solution**: Add a technical enforcement hook that validates BibTeX metadata against cached API JSON files.

---

## Evidence (cdr-ethics-1 review)

### Example 1: `gardiner2011early` - Complete Entry Type Fabrication

**S2 API returned** (s2_gardiner.json, lines 6-30):
```json
"title": "Some Early Ethics of Geoengineering the Climate...",
"doi": "10.3197/096327111X12997574391689",
"journal": { "name": "Environmental Values", "pages": "163 - 188", "volume": "20" },
"publicationTypes": ["JournalArticle"]
```

**BibTeX entry has** (literature-all.bib, lines 492-508):
```bibtex
@incollection{gardiner2011early,
  booktitle = {Climate Ethics: Essential Readings},
  editor = {Gardiner, Stephen and Caney, Simon and Jamieson, Dale and Shue, Henry},
  publisher = {Oxford University Press},
  pages = {163--175},
}
```

**Problems**:
| Field | API Value | BibTeX Value | Status |
|-------|-----------|--------------|--------|
| Entry type | JournalArticle → @article | @incollection | FABRICATED |
| Venue | Environmental Values | Climate Ethics: Essential Readings | FABRICATED |
| Publisher | (none) | Oxford University Press | FABRICATED |
| Pages | 163-188 | 163-175 | FABRICATED |
| Editor | (none) | Gardiner, Caney, Jamieson, Shue | FABRICATED |

The LLM recognized the paper and used metadata for a *different version* (the 2010 Oxford anthology reprint) that was NOT in the API results.

### Example 2: `peacock2021much` - Issue Number Fabrication

**S2 API returned** (s2_mitigation.json, lines 110-114):
```json
"journal": { "name": "Ethics, Policy & Environment", "pages": "281 - 296", "volume": "25" }
```
(No `issue` field)

**BibTeX has**:
```bibtex
number = {3},
```

The `number = {3}` field does not exist in any API output.

### Example 3: Duplicate Peacock Entries - Different Venues

Two entries with identical title:
- `peacock2018negative`: Journal of Agricultural and Environmental Ethics, 2018
- `peacock2021much`: Ethics, Policy & Environment, 2021

S2 API only returns the 2021 version. The 2018 entry metadata may be fabricated or from a different search.

---

## Root Cause

1. **No technical enforcement**: `bib_validator.py` only validates BibTeX syntax, not metadata provenance
2. **Instructions insufficient**: Despite explicit prohibitions, LLMs still fill in "known" metadata
3. **Template encourages completion**: Example template shows all fields populated

---

## Proposed Solution: Metadata Provenance Validator

### New Hook: `metadata_validator.py`

Create a SubagentStop hook that:
1. Parses the BibTeX file being written
2. Scans JSON files in the same directory for API output
3. Validates that each BibTeX field value exists in at least one JSON file
4. Blocks write if unverifiable fields are found

### Validation Rules

**Always verify** (must exist in JSON):
- `journal` / `booktitle`
- `volume`
- `number` / `issue`
- `pages`
- `publisher`
- `doi`
- `year`

**LLM-generated** (exempt from validation):
- `note` (annotations)
- `keywords`
- `abstract_source` (metadata field, not bibliographic)

**Derived fields** (validate components):
- `author` (names must match API output)
- `title` (must match API output, allowing minor normalization)
- Citation key (derived from author+year, OK to generate)

### Implementation Approach

```
.claude/hooks/metadata_validator.py
```

1. **Parse BibTeX** using pybtex (already a dependency)
2. **Load JSON files** from `intermediate_files/json/` directory
3. **Build searchable index** of all values from JSON
4. **Check each entry**: For fields requiring validation, confirm value appears in index
5. **Report violations**: List field, expected source, and suggestion to omit

### Hook Configuration

```yaml
# .claude/hooks/hooks.json entry
{
  "event": "SubagentStop",
  "hooks": [{
    "name": "metadata-provenance",
    "command": "python .claude/hooks/metadata_validator.py \"$BIBTEX_FILE\" \"$JSON_DIR\"",
    "validation_fields": ["journal", "booktitle", "volume", "number", "pages", "publisher", "year"],
    "exempt_fields": ["note", "keywords", "abstract_source"]
  }]
}
```

---

## Files to Modify

| File | Change |
|------|--------|
| `.claude/hooks/metadata_validator.py` | **NEW** - Validation logic |
| `.claude/hooks/subagent_stop_bib.sh` | Add call to metadata_validator.py |
| `.claude/agents/domain-literature-researcher.md` | Update template to show omitted fields |
| `.claude/docs/conventions.md` | Document validation requirements |
| `tests/test_metadata_validator.py` | **NEW** - Test cases |

---

## Hook Execution: When and How

### SubagentStop Hook Behavior

Claude Code calls SubagentStop hooks after **any** subagent completes. The hook receives JSON context via stdin:

```json
{
  "agent_name": "domain-literature-researcher",  // or other agent type
  "cwd": "/path/to/working/directory",
  ...
}
```

### Existing Filtering (Already Implemented)

The existing `subagent_stop_bib.sh` **already filters by agent name** (lines 16-19):

```bash
# Only validate for domain-literature-researcher agent
if [[ "$AGENT_NAME" != "domain-literature-researcher" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi
```

**Effect**: For ALL other agents (synthesis-writer, synthesis-planner, etc.), the hook immediately returns `{"decision": "allow"}` and exits without running validation.

### Metadata Validator Integration

The metadata_validator.py will be called from within the same shell script, AFTER the existing BibTeX syntax validation, and ONLY when `AGENT_NAME == "domain-literature-researcher"`:

```bash
# In subagent_stop_bib.sh (after agent name check)

# First: BibTeX syntax validation (existing)
RESULT=$(python "$CLAUDE_PROJECT_DIR/.claude/hooks/bib_validator.py" "$bib_file" 2>&1 || true)

# Second: Metadata provenance validation (new)
JSON_DIR="${WORKING_DIR}/intermediate_files/json"
if [[ -d "$JSON_DIR" ]]; then
    METADATA_RESULT=$(python "$CLAUDE_PROJECT_DIR/.claude/hooks/metadata_validator.py" \
        "$bib_file" "$JSON_DIR" 2>&1 || true)
    # Check result and append errors if any
fi
```

### Execution Flow

```
Any subagent completes → SubagentStop hook fires
    ↓
Check agent_name
    ↓
If NOT domain-literature-researcher → allow immediately, exit
    ↓
If domain-literature-researcher:
    ├── 1. Find .bib files in working directory
    ├── 2. Run bib_validator.py (syntax check)
    ├── 3. Run metadata_validator.py (provenance check) [NEW]
    └── 4. Collect all errors, block if any found
```

### Why This Works

1. **Single hook file**: One `subagent_stop_bib.sh` handles all validation
2. **Agent filtering**: Line 16-19 ensures only domain-literature-researcher triggers validation
3. **Chained validation**: Syntax check first, then provenance check
4. **JSON dir requirement**: metadata_validator only runs if `intermediate_files/json/` exists (which it will for domain researchers)

---

## Implementation Details

### Core Components

**1. Metadata Index** - Extract and index all values from JSON files:
```python
@dataclass
class SourceMetadata:
    doi: Optional[str]
    title: str
    container_title: Optional[str]  # journal/booktitle
    volume: Optional[str]
    issue: Optional[str]
    pages: Optional[str]
    publisher: Optional[str]
    source_file: str
    source_api: str  # s2, openalex, crossref, arxiv
```

**2. API Parsers** - Handle different JSON formats:
- **S2**: `results[].journal.{name,volume,pages}`, `results[].venue`
- **OpenAlex**: `results[].source.name`, `results[].type`
- **CrossRef**: `results[].{container_title,volume,issue,page,publisher}`
- **arXiv**: `results[].journal_ref`

**3. Value Normalization**:
- Pages: `"163 - 188"` → `"163-188"` (handle BibTeX `--` vs API `-`)
- Journals: case-insensitive, strip "The", expand abbreviations

**4. Validation Rules**:
| Field | Must Verify | Source Priority |
|-------|------------|-----------------|
| `journal`/`booktitle` | Yes | CrossRef > S2 > OpenAlex |
| `volume` | Yes | CrossRef > S2 > OpenAlex |
| `number` | Yes | CrossRef > S2 > OpenAlex |
| `pages` | Yes | CrossRef > S2 > OpenAlex |
| `publisher` | Yes | CrossRef > S2 > OpenAlex |
| `note` | No | Agent-generated |
| `keywords` | No | Agent-generated |
| `abstract` | No | From API but stored separately |

### CLI Interface

```
python .claude/hooks/metadata_validator.py <bib_file> <json_dir> [--mode=strict|warn]

Exit codes:
  0: All fields verified
  1: Unverifiable fields found (strict mode)
  2: Configuration/file error

Output: JSON with errors and verified count
```

### Error Message Format

```
METADATA VALIDATION FAILED

Entry: gardiner2011early
  - Field 'booktitle' = "Climate Ethics: Essential Readings"
    NOT FOUND in API output. API sources contain:
      journal: "Environmental Values" (s2_gardiner.json)
    Action: Remove field or use value from API output

2 entries have unverifiable metadata fields.
```

### Special Cases

1. **CrossRef Priority**: Prefer CrossRef values as authoritative
2. **Entry Type Mismatch**: Flag when S2 returns JournalArticle but BibTeX is @incollection
3. **Missing JSON**: Warn but don't error (web sources may not have JSON backup)

---

## Verification Plan

**Unit Tests** (`tests/test_metadata_validator.py`):
1. `test_gardiner_hallucination` - Detect fabricated booktitle/publisher
2. `test_peacock_fabricated_issue` - Detect number field not in API
3. `test_pages_normalization` - Accept "163--188" when API has "163 - 188"
4. `test_crossref_priority` - Prefer CrossRef over S2 when different
5. `test_note_field_exempt` - Don't validate agent-generated fields

**Integration Test**: Run validator on cdr-ethics-1 BibTeX files, verify it catches known fabrications

**Manual Verification**: Check output on 2-3 reviews to ensure no false positives

---

## Implementation Phases

1. **Phase 1**: JSON parsing and indexing (parse_*_result functions)
2. **Phase 2**: Value normalization and matching
3. **Phase 3**: Validation logic and error formatting
4. **Phase 4**: Hook integration (modify subagent_stop_bib.sh)
5. **Phase 5**: Testing and refinement

---

## Reference Files

- `.claude/hooks/bib_validator.py` - Pattern for validator structure, CLI, pybtex usage
- `.claude/hooks/subagent_stop_bib.sh` - Hook integration point
- `.claude/skills/philosophy-research/scripts/verify_paper.py:114-163` - CrossRef result format
- `reviews/cdr-ethics-1/intermediate_files/json/s2_gardiner.json` - Example showing hallucination
- `tests/test_bib_validator.py` - Testing patterns to follow

---

## Relationship to Metadata Enrichment Feature

### Existing Feature (branch: `claude/abstract-and-content-enrichment`)

The enrichment branch adds:
- `enrich_bibliography.py` - Adds **abstracts** from APIs (S2, OpenAlex, CORE)
- `get_abstract.py` - Multi-source abstract resolution
- `INCOMPLETE` flag for entries missing abstracts

**What enrichment does**: Adds **new data** (abstracts) from APIs
**What enrichment does NOT do**: Validate existing bibliographic metadata

### How Validator Complements Enrichment

| Feature | Purpose | Data Direction |
|---------|---------|----------------|
| Enrichment | Add missing abstracts | API → BibTeX (additive) |
| Validator | Verify metadata provenance | BibTeX → JSON (checking) |

**They are orthogonal**:
- Enrichment adds data the LLM couldn't provide
- Validator prevents data the LLM shouldn't have provided

### No Breaking Changes

The validator does NOT affect enrichment because:
1. Different fields: Enrichment handles `abstract`; validator handles `journal`, `volume`, `pages`, etc.
2. Different direction: Enrichment adds from APIs; validator checks against APIs
3. Same JSON files: Both use `intermediate_files/json/` as source of truth
4. `INCOMPLETE` flag is exempt from validation (it's a metadata keyword, not bibliographic data)

### Architecture Synergies

**Shared Infrastructure**:
1. **BibTeX parsing**: Both scripts parse BibTeX. Current enrichment uses regex; validator can use pybtex. Could standardize on pybtex.
2. **JSON indexing**: Both need to search API output JSON files. Could share an indexing module.
3. **Field normalization**: Page ranges, journal names need normalization in both contexts.

**Proposed Shared Module** (future optimization, not required for initial implementation):
```
.claude/skills/literature-review/scripts/bib_utils.py
├── parse_bibtex() - Standardized BibTeX parsing
├── build_json_index() - Index all JSON files in directory
├── normalize_pages() - "163 - 188" → "163-188"
└── normalize_journal() - Case, abbreviation handling
```

For initial implementation, keep validator standalone. Share code in future refactoring if needed.

### Integration Point

Both validator and enrichment could run as part of the same post-processing pipeline:

```
Domain researcher writes BibTeX
    ↓
[NEW] metadata_validator.py checks provenance → BLOCKS if hallucinated fields found
    ↓
[EXISTING] enrich_bibliography.py adds abstracts
    ↓
Final enriched, validated BibTeX
```

The validator should run BEFORE enrichment to catch problems early.
