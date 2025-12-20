# Philosophy Research Skill - Implementation Plan

**Status**: Planning complete, ready for implementation
**Last updated**: 2025-12-20

## Objective

Replace `WebSearch` in `domain-literature-researcher` agent with a Claude Skill that searches academic sources via APIs, reducing costs while maintaining citation quality.

## Architecture Decision

**Approach**: Claude Skill (not MCP)
**Rationale**: Simpler to implement, sufficient for this use case, skills can be used by subagents via `skills:` frontmatter.

## File Structure

```
.claude/skills/philosophy-research/
├── SKILL.md                    # Skill definition
├── scripts/
│   ├── search_sep.py           # SEP via Brave API
│   ├── search_philpapers.py    # PhilPapers via Brave API
│   ├── search_semantic.py      # Semantic Scholar API
│   ├── search_openalex.py      # OpenAlex API (backup)
│   ├── verify_paper.py         # CrossRef API
│   └── requirements.txt
└── references/
    ├── philpapers-categories.txt
    └── philosophy-journals.txt
```

## Search Sources

| Source | Method | Auth Required | Rate Limit | Notes |
|--------|--------|---------------|------------|-------|
| SEP | Brave API + `site:plato.stanford.edu` | BRAVE_API_KEY | 1/sec free | Works well |
| PhilPapers | Brave API + `site:philpapers.org` | BRAVE_API_KEY | 1/sec free | Safer than their restricted API |
| Semantic Scholar | Direct API | None | 100/sec | Primary paper source |
| OpenAlex | Direct API | None | 100k/day | Backup paper source |
| CrossRef | Direct API | None (polite pool) | 50/sec | DOI verification |

## API Specifications

### Brave Search API
- **Endpoint**: `https://api.search.brave.com/res/v1/web/search`
- **Auth**: Header `X-Subscription-Token: {BRAVE_API_KEY}`
- **Params**: `q` (query), `count` (max 20)
- **Cost**: 2,000 free/month, then $3/1000

### Semantic Scholar API
- **Endpoint**: `https://api.semanticscholar.org/graph/v1/paper/search`
- **Auth**: None required (optional API key for higher limits)
- **Params**: `query`, `fields` (title,authors,year,abstract,externalIds,citationCount), `limit`
- **Returns**: DOIs in `externalIds.DOI`

### OpenAlex API
- **Endpoint**: `https://api.openalex.org/works`
- **Auth**: None (add `mailto:` param for polite pool)
- **Params**: `search`, `filter`, `per_page`
- **Returns**: DOIs in `doi` field

### CrossRef API
- **Endpoint**: `https://api.crossref.org/works`
- **Auth**: None (add User-Agent with email for polite pool)
- **Params**: `query.title`, `query.author`, `rows`
- **Note**: `query.title` uses OR between words—use fuzzy matching on results

## Script Specifications

### search_sep.py
```python
# Input: query string
# Output: JSON list of {title, url, snippet}
# Method: Brave API with site:plato.stanford.edu
```

### search_philpapers.py
```python
# Input: query string, optional --limit
# Output: JSON list of {title, url, snippet, authors (if parseable)}
# Method: Brave API with site:philpapers.org
```

### search_semantic.py
```python
# Input: query string, optional --year-from, --limit
# Output: JSON list of {title, authors, year, abstract, doi, citation_count, url}
# Method: Semantic Scholar API
# Fields: title,authors,year,abstract,externalIds,citationCount,url
```

### search_openalex.py
```python
# Input: query string, optional --year-from, --limit
# Output: JSON list of {title, authors, year, abstract, doi, citation_count}
# Method: OpenAlex API
# Use as backup when Semantic Scholar gaps found
```

### verify_paper.py
```python
# Input: --title "...", optional --author "...", --year YYYY
# Output: JSON {title, authors, year, doi, publisher, match_confidence} or error
# Method: CrossRef API with fuzzy title matching (SequenceMatcher, threshold 0.85)
# CRITICAL: Exit 1 and print warning if not found—never fabricate
```

### requirements.txt
```
requests>=2.31.0
```

## Agent Integration

After skill is complete, modify `domain-literature-researcher.md`:

```yaml
# Change frontmatter
---
name: domain-literature-researcher
description: ...
tools: WebFetch, Read, Write, Grep, Bash  # REMOVE WebSearch
skills: philosophy-research               # ADD skill
model: sonnet
---
```

Update search process instructions to use scripts instead of WebSearch.

## SKILL.md Structure

```yaml
---
name: philosophy-research
description: Search philosophy literature across SEP, PhilPapers, Semantic Scholar, and OpenAlex. Use for literature review, paper discovery, or bibliography generation in philosophy. Verifies citations via CrossRef.
---
```

Body sections:
1. **Search Workflow**: SEP (concepts) → PhilPapers (philosophy papers) → Semantic Scholar (citations) → verify with CrossRef
2. **Available Scripts**: Usage examples for each script
3. **Verification Requirements**: Never fabricate, always verify, omit DOI if not found

## Implementation Order

1. `verify_paper.py` — foundation for accuracy
2. `search_semantic.py` — primary paper source
3. `search_sep.py` — conceptual overview
4. `search_philpapers.py` — philosophy-specific
5. `search_openalex.py` — backup source
6. `SKILL.md` — documentation
7. Test all scripts
8. Update `domain-literature-researcher.md`

## Environment Setup

```bash
export BRAVE_API_KEY="your-key-here"
pip install requests
```

## Success Criteria

- [ ] All scripts return valid JSON
- [ ] verify_paper.py finds DOI for "Freedom of the Will and the Concept of a Person" by Frankfurt
- [ ] search_semantic.py returns papers with DOIs
- [ ] domain-literature-researcher can complete a search without WebSearch
- [ ] No fabricated citations possible
