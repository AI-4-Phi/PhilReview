# Philo-sota — SOTA Literature Review Multi‑Agent System

LiRA‑inspired, file‑based, multi‑agent workflow for generating focused, insight‑driven state‑of‑the‑art (SOTA) literature reviews with verified, reference‑manager‑ready bibliographies.

This system is designed for research proposals and high‑stakes reviews where analytical depth, citation integrity, and fast iteration matter. It decomposes the job across specialized agents, keeps contexts small, runs domain searches in parallel, validates citations, and writes the review section‑by‑section before assembling a final draft.

---

## Highlights

- Multi‑phase orchestration with task persistence and resume capability
- BibTeX‑first literature gathering (ready for direct import into Zotero and other managers)
- Automated citation validation and DOI checks (no fabricated citations)
- Parallel domain research; section‑by‑section synthesis for context efficiency
- Tight, narrative‑driven review emphasizing key debates, recent contributions, and concrete gaps
- Optional editorial polish and novelty/strategy assessment

---

## How it works (at a glance)

1) Plan
- Analyze the research idea and decompose it into 3–8 searchable, coherent domains.
- Output: lit‑review‑plan.md

2) Research (parallel)
- Run one domain researcher per domain to produce valid BibTeX files with rich metadata.
- Output: literature‑domain‑X.bib (includes @comment domain overview + per‑entry notes)

3) Validate
- Verify each BibTeX entry (existence, metadata, DOI). Remove unverified entries to a separate file.
- Output: validation‑report.md, unverified‑sources.bib, and cleaned .bib files

4) Synthesize (plan)
- Read the plan and validated BibTeX files. Design a tight outline for a focused review.
- Output: synthesis‑outline.md

5) Write (section‑by‑section)
- Write each section as its own file using only the relevant subset of BibTeX.
- Assemble sections into the final review.
- Output: synthesis‑section‑N.md → literature‑review‑final.md

6) Optional: Edit + Assess
- Editorial agent polishes structure, clarity, and citation practice.
- Novelty assessor provides an executive strategy brief and positioning recommendations.

Task progress is tracked across phases in task‑progress.md so you can pause and resume anytime.

---

## Why this approach

- Insight over coverage: Focuses on the arguments, tensions, and strategic research gaps that matter
- Proven context efficiency: Parallel domain search and section‑by‑section writing keep contexts small and fast
- Modular and resilient: Multi‑file pattern makes progress reviewable, resumable, and easy to revise
- Citation integrity: Validation removes questionable entries before synthesis and import
- Ready for reference managers: BibTeX artifacts are valid and importable with one click

---

## Agents

- research‑proposal‑orchestrator
  - The meta‑agent that coordinates all phases, tracks progress, and assembles outputs

- literature‑review‑planner
  - Decomposes the topic into domains, search strategies, and scope; creates lit‑review‑plan.md

- domain‑literature‑researcher
  - Performs web‑based literature searches per domain; outputs valid BibTeX (.bib)
  - Each entry uses note fields (CORE ARGUMENT, RELEVANCE, POSITION) and keywords with importance tags (High/Medium/Low)
  - Adds a top‑level @comment block with domain overview, gaps, and synthesis guidance

- citation‑validator
  - Verifies entries and DOIs; moves unverified items to unverified‑sources.bib and writes validation‑report.md
  - Cleans domain .bib files so they are ready for import and synthesis

- synthesis‑planner
  - Reads plan + BibTeX to design a tight outline emphasizing key debates and gaps; writes synthesis‑outline.md

- synthesis‑writer
  - Writes sections one‑by‑one to separate files, using only relevant BibTeX subsets; final draft assembled at the end

- sota‑review‑editor (optional)
  - Reviews and revises the draft for structure, clarity, balance, and citation practice

- novelty‑assessor (optional)
  - Produces an executive assessment of novelty, competitive landscape, positioning, risks, and recommendations

---

## End‑to‑end workflow and artifacts

- Phase 0: Task tracking
  - task‑progress.md (created at start; updated after every step; enables resume)

- Phase 1: Planning
  - lit‑review‑plan.md

- Phase 2: Domain research (parallel)
  - literature‑domain‑1.bib
  - literature‑domain‑2.bib
  - …
  - Each .bib contains:
    - @comment with DOMAIN, overview, notable gaps, synthesis guidance, positions
    - Structured per‑entry notes and keywords (with High/Medium/Low importance)

- Phase 3: Citation validation
  - validation‑report.md
  - unverified‑sources.bib (removed entries with reasons)
  - Cleaned literature‑domain‑*.bib (verified entries only)

- Phase 4: Synthesis planning
  - synthesis‑outline.md (section structure, word targets, citation selection)

- Phase 5: Synthesis writing
  - synthesis‑section‑1.md
  - synthesis‑section‑2.md
  - …
  - literature‑review‑final.md (assembled)

- Optional Phase 6: Editorial + executive assessment
  - state‑of‑the‑art‑review‑final.md (polished)
  - editorial‑notes.md
  - executive‑assessment.md (novelty/strategy)

---

## Project structure

- .claude/agents
  - Agent specifications, behaviors, and phase contracts

- docs/
  - Space for internal notes and ideas

- reviews/
  - Suggested location for your generated artifacts (plans, bib files, sections, final drafts)

Tip: The orchestrator writes outputs wherever your runtime is configured. Many teams keep all generated artifacts in a versioned subdirectory (e.g., reviews/[topic]/…).

---

## Usage

1) Kickoff
- Ask for a state‑of‑the‑art literature review and provide:
  - A 2–5 paragraph research idea or problem statement
  - Any constraints (domains to include/exclude, time window, venues)
  - Target audience (e.g., grant reviewers, journal editors)
  - Target word count and desired citation range (typical: 15–25 cited works)

2) Choose mode
- Autopilot
  - Runs all phases start‑to‑finish with status updates; returns the final draft and all intermediate artifacts
- Human‑in‑the‑loop
  - Reviews and approval checkpoints after Planning, Domain Research, Validation, and Synthesis Planning

3) Resume anytime
- If interrupted, simply request “Resume from task‑progress.md”
- The system detects the last completed task and continues from there

4) Import to Zotero (or other managers)
- Import the cleaned literature‑domain‑*.bib files (not unverified‑sources.bib)
- The note fields preserve argument/relevance metadata for later use

Example prompts:
- “I need a SOTA literature review for [topic]: [brief description]. Audience: [funder/venue]. Please run in Autopilot.”
- “Plan a literature review for [topic] focusing on [sub‑areas], last 5 years emphasized.”
- “Resume from task‑progress.md and proceed to synthesis planning.”

---

## Quality standards

- No fabricated citations or DOIs; only verified entries proceed past validation
- Insight over coverage; emphasize key debates, recent contributions, and concrete gaps
- Clear connection to the research idea throughout
- (Author Year) in‑text citations; Chicago‑style references at the end
- Balanced and charitable presentation of positions and objections
- Section‑by‑section writing ensures tight narrative and context efficiency

---

## Design principles

- Multi‑file‑then‑assemble pattern
  - Domains → multiple .bib files → validated together
  - Sections → multiple .md files → assembled into the draft
- Context efficiency
  - Agents read only what they need (relevant domains per section)
- Parallelization
  - Fan‑out (domain research), fan‑in (validation), then focused synthesis
- File‑based communication
  - Transparent, reviewable artifacts; easy to re‑run any piece

---

## Tips for best results

- Provide a crisp problem statement, constraints, and preferred scope up front
- Specify “focused” vs “comprehensive” tone and a target word range
- Call out must‑include domains, debates, or exemplar papers if you have them
- For interdisciplinary topics, note the non‑philosophy sources to prioritize
- If you will import to Zotero, stick to the cleaned domain .bib files only

---

## Extensibility

- Add agents for field‑specific needs (e.g., policy synthesis, legal doctrine, empirical replication scans)
- Extend validation to other formats (RIS, EndNote XML)
- Add visualization steps (e.g., literature maps based on BibTeX metadata)
- Introduce funder/venue‑specific formatting and scoring rubrics
- Swap in alternative writing/validation heuristics while keeping the file contracts stable

---

## Inspiration

- Inspired by LiRA (Literature Review Agents) patterns and multi‑agent best practices
- Adapts those ideas to emphasize citation integrity, BibTeX‑first artifacts, and section‑by‑section synthesis

---

## Frequently asked questions

- Will it include the latest work?
  - Yes. Domain researchers are instructed to perform web‑based searches and include very recent publications. Validation checks help ensure integrity.

- Why BibTeX instead of prose summaries for domains?
  - BibTeX enables direct import and structured metadata for synthesis agents. Prose still appears in @comment and note fields, but the files remain machine‑parseable and reference‑manager‑ready.

- What happens to questionable citations?
  - They are moved to unverified‑sources.bib with reasons and excluded from synthesis and import.

- Can I iterate on a single section or domain?
  - Yes. The multi‑file pattern makes it easy to regenerate specific domains or sections without redoing the entire workflow.

---

## Getting started

- Ask for a literature review on your topic and choose Autopilot or Human‑in‑the‑loop
- Review lit‑review‑plan.md to confirm the domain scope
- After Phase 3, import the cleaned .bib files to your reference manager
- Use synthesis‑outline.md to steer emphasis before writing sections
- After assembly, request editorial polish and, if desired, a novelty assessment

By combining file‑based orchestration, parallel domain research, and strict validation, Philo‑sota delivers trustworthy, focused SOTA reviews that help you argue for the importance, novelty, and feasibility of your project.