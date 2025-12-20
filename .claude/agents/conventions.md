# Shared Conventions for Literature Review Agents

This file contains specifications shared across multiple agents. Reference this file rather than duplicating content.

---

## File Encoding: UTF-8

**All output files MUST use UTF-8 encoding.**

Requirements:
- Preserve diacritics in author names exactly (e.g., Kästner, Müller, García)
- Use proper special characters: ä ö ü é è ñ ç etc.
- Use typographic characters: em-dash (—), en-dash (–), curly quotes (" " ' ')
- Never convert special characters to ASCII approximations

**Verification**: Run `file [filename]` — should show "UTF-8 Unicode text"

---

## BibTeX Format Specification

### Entry Types

| Type | Use For |
|------|---------|
| `@article` | Journal articles |
| `@book` | Books |
| `@incollection` | Book chapters |
| `@inproceedings` | Conference papers |
| `@phdthesis` | Dissertations |
| `@misc` | SEP entries, online resources |

### Citation Keys

Format: `authorYYYYkeyword`

Examples: `frankfurt1971freedom`, `fischerravizza1998responsibility`, `nelkin2011rational`

### Author Names

Format: `Last, First Middle and Last2, First2`

```bibtex
author = {Frankfurt, Harry G.}
author = {Fischer, John Martin and Ravizza, Mark}
author = {Smith, John and Jones, Mary and Brown, David}
```

### Required Fields by Entry Type

**@article**: author, title, journal, year, volume, pages
- Optional: number, doi

**@book**: author, title, publisher, year
- Optional: address, doi, edition

**@incollection**: author, title, booktitle, publisher, year, pages
- Optional: editor, address

### DOI Field

- Only include verified DOIs from publisher sites or CrossRef
- Format: `doi = {10.XXXX/xxxxx}` (no URL prefix)
- If DOI unavailable, omit the field entirely — never fabricate

### Keywords Field

Format: `topic-tag, position-tag, Importance-level`

Importance levels:
- `High` — Core paper, must cite
- `Medium` — Important context
- `Low` — Peripheral but relevant

Example: `keywords = {compatibilism, free-will, hierarchical-agency, High}`

---

## Chicago Citation Style (Author-Date)

### In-Text Citations

| Situation | Format | Example |
|-----------|--------|---------|
| Single author | (Author Year) | (Frankfurt 1971) |
| Two authors | (Author and Author Year) | (Fischer and Ravizza 1998) |
| Three+ authors | (Author et al. Year) | (Smith et al. 2020) |
| Multiple citations | (Author Year; Author Year) | (Frankfurt 1971; Dennett 1984) |
| With page numbers | (Author Year, pages) | (Fischer and Ravizza 1998, 31-45) |
| Author as subject | Author (Year) argues... | Frankfurt (1971) argues... |

### Bibliography Format

**Journal Article**:
```
Frankfurt, Harry G. 1971. "Freedom of the Will and the Concept of a Person." The Journal of Philosophy 68 (1): 5–20. https://doi.org/10.2307/2024717.
```

**Book**:
```
Fischer, John Martin, and Mark Ravizza. 1998. Responsibility and Control: A Theory of Moral Responsibility. Cambridge: Cambridge University Press. https://doi.org/10.1017/CBO9780511814594.
```

**Book Chapter**:
```
Nelkin, Dana Kay. 2011. "Freedom and Responsibility." In The Oxford Handbook of Free Will, edited by Robert Kane, 425–453. Oxford: Oxford University Press.
```

---

## Communication with Orchestrator

### Standard Return Message Format

```
[Task name] complete.

Results:
- [Key metric 1]: [value]
- [Key metric 2]: [value]
- [Key metric 3]: [value]

Status: [PASS | REVIEW | specific status]

Files:
- [filename1.ext] ([description])
- [filename2.ext] ([description])

[One-line next step or recommendation]
```

### Progress Updates During Execution

- Use clear phase indicators: "Phase 2/5: [description]..."
- Report completion with file references: "Section 1 complete → synthesis-section-1.md (450 words)"
- Track running totals: "Running total: 1800/3500 words"

---

## Quality Standards

### Citation Integrity

**Absolute Rules**:
- ❌ Never fabricate papers, authors, or publications
- ❌ Never create synthetic DOIs
- ❌ Never cite papers not verified through search
- ✅ Only cite papers found and verified via WebSearch
- ✅ If DOI unavailable, omit the field

### Citation Integration in Prose

**Good** (analytical):
> Fischer and Ravizza (1998) argue that guidance control—the ability to regulate behavior through reasons-responsive mechanisms—grounds moral responsibility. This differs crucially from libertarian views...

**Poor** (list-like):
> Many philosophers have written about this (Frankfurt 1971; Dennett 1984; Fischer and Ravizza 1998).

### Gap Specificity

**Good** (specific, evidence-based):
> While compatibilist frameworks are philosophically sophisticated, Vargas (2013) notes they "lack empirical operationalization" (p. 203). No study has measured neural mechanisms of reasons-responsiveness.

**Poor** (vague):
> More research is needed on free will and neuroscience.

---

## Domain File Structure

### BibTeX Domain Files

```bibtex
@comment{
====================================================================
DOMAIN: [Domain Name]
SEARCH_DATE: [YYYY-MM-DD]
PAPERS_FOUND: [N total] (High: [X], Medium: [Y], Low: [Z])
SEARCH_SOURCES: SEP, PhilPapers, Google Scholar, [other]
====================================================================

DOMAIN_OVERVIEW:
[2-3 paragraphs on main debates, key papers, developments]

RELEVANCE_TO_PROJECT:
[2-3 sentences connecting to research idea]

NOTABLE_GAPS:
[1-2 sentences on under-explored areas]

SYNTHESIS_GUIDANCE:
[1-2 sentences with recommendations]

KEY_POSITIONS:
- [Position 1]: [X papers] - [Brief description]
- [Position 2]: [Y papers] - [Brief description]
====================================================================
}

@article{citationkey,
  author = {...},
  title = {...},
  ...
  note = {...},
  keywords = {...}
}
```

---

## File Assembly

### Combining Section Files

Use proper spacing for markdown parsing:

```bash
for f in synthesis-section-*.md; do cat "$f"; echo; echo; done > literature-review-final.md
```

Two blank lines between sections ensures pandoc parses headings correctly.
