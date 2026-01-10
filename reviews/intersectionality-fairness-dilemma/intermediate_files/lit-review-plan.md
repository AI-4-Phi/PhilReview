# Literature Review Plan: The Intersectionality Dilemma for Algorithmic Fairness

## Research Idea Summary

This paper argues that intersectional algorithmic fairness faces a genuine dilemma arising from the interaction of statistical uncertainty (sparse data on small intersectional groups) and ontological uncertainty (contested questions about which groups warrant consideration). Expanding the set of groups exacerbates statistical problems; constraining it requires resolving contested questions in social ontology. The paper claims existing technical approaches do not resolve this dilemma.

## Key Research Questions

1. How do statistical uncertainty and ontological uncertainty interact in intersectional fairness auditing?
2. Does this interaction constitute a genuine dilemma that cannot be resolved by existing technical or philosophical approaches?
3. What are the implications for the feasibility of intersectional fairness auditing in practice?
4. How should fairness researchers navigate trade-offs between statistical reliability and ontological adequacy?

## Literature Review Domains

### Domain 1: Algorithmic Fairness and Intersectionality (ML/CS Literature)

**Focus**: Technical approaches to intersectional fairness metrics, methods for handling sparse data in fairness auditing, fairness gerrymandering, and surveys of the field.

**Key Questions**:
- What technical solutions have been proposed for intersectional fairness measurement?
- How do existing methods handle the statistical challenges of small group sizes?
- What is fairness gerrymandering and how does it relate to group specification?
- Do any papers explicitly identify the interaction between statistical and ontological problems?

**Search Strategy**:
- Primary sources: Semantic Scholar, OpenAlex (CS/ML venues)
- Key venues: FAccT, NeurIPS, ICML, AAAI, AIES
- Key terms: "intersectional fairness", "fairness gerrymandering", "subgroup fairness", "multicalibration", "intersectionality machine learning", "sparse data fairness"
- Expected papers: 20-30 key papers
- Already in bibliography (do not duplicate): Kearns et al. 2018, Foulds et al. 2020, Molina and Loiseau 2022, Gohar and Cheng 2023, Herlihy et al. 2024, Buolamwini and Gebru 2018, Morina et al. 2019, Lum et al. 2022, Paes et al. 2024, Cooper et al. 2024, Choi et al. 2025, Dwork et al. 2012
- Time focus: Emphasize 2020-2025 work

**Relevance to Project**: Core domain establishing the state of technical solutions and identifying whether existing work recognizes the dilemma structure.

---

### Domain 2: Philosophy of Intersectionality

**Focus**: Analytical vs. hermeneutic interpretations of intersectionality, causal modeling of intersectionality, theoretical foundations of intersectionality as a social-scientific construct.

**Key Questions**:
- What are the competing philosophical interpretations of intersectionality?
- How do analytical/causal approaches differ from hermeneutic/interpretive approaches?
- What is the social construction of intersectional group identity?
- Can intersectionality be reduced to combinations of attributes or does it require emergent categories?

**Search Strategy**:
- Primary sources: PhilPapers (social epistemology, feminist philosophy, social philosophy), SEP ("intersectionality", "social construction"), Semantic Scholar (philosophy)
- Key terms: "intersectionality philosophy", "causal models intersectionality", "social construction intersectionality", "hermeneutic intersectionality", "intersectionality ontology"
- Expected papers: 12-18 key papers
- Already in bibliography (do not duplicate): Bright et al. 2016, Ruíz 2017
- Look for: Recent philosophy of science work (2018-2025) on intersectionality as theoretical construct

**Relevance to Project**: Provides philosophical grounding for the "ontological uncertainty" horn of the dilemma—demonstrates that group specification is contested.

---

### Domain 3: Social Ontology and Group Constitution

**Focus**: Constitution of social groups, debates between combinatorial/attribute-based accounts vs. practice-based/hermeneutic accounts, social kinds, and social construction.

**Key Questions**:
- How are social groups constituted?
- Can groups be derived algorithmically from attributes or must they be specified through social practices?
- What is the relationship between social categories and demographic attributes?
- How do practice-based accounts challenge attribute-based models?

**Search Strategy**:
- Primary sources: SEP ("social ontology", "social construction", "social institutions"), PhilPapers (social ontology, metaphysics of social groups)
- Key terms: "social ontology", "constitution of social groups", "social kinds", "social construction groups", "practice-based accounts", "collective intentionality"
- Expected papers: 10-15 key papers
- Look for: Haslanger, Appiah, Mallon, Ásta on social construction; recent debates on attribute vs. practice-based accounts

**Relevance to Project**: Directly supports the claim that specifying $\mathcal{G}$ (the set of groups) faces ontological uncertainty—no consensus on how to derive the "right" groups.

---

### Domain 4: Measurement Theory and Construct Validity in ML

**Focus**: Operationalization of fairness concepts, construct validity for fairness metrics, what fairness metrics actually measure, gap between formal definitions and normative goals.

**Key Questions**:
- What is construct validity in the context of fairness metrics?
- Do fairness metrics measure what they purport to measure?
- How should we evaluate operationalizations of normative concepts?
- What are the limits of formalization for contested normative concepts?

**Search Strategy**:
- Primary sources: Semantic Scholar (FAccT, ML venues), PhilPapers (philosophy of science, measurement theory)
- Key terms: "construct validity fairness", "operationalization fairness", "measurement theory machine learning", "validity fairness metrics", "formalization normative concepts"
- Expected papers: 10-15 key papers
- Already in bibliography (do not duplicate): Jacobs and Wallach 2021
- Look for: Recent FAccT papers on measurement, philosophy of science on measurement in social contexts

**Relevance to Project**: Supports the broader claim that fairness auditing faces fundamental conceptual challenges, not just technical optimization problems.

---

### Domain 5: Normative Frameworks for Fairness

**Focus**: Prioritarianism, sufficientarianism, egalitarianism, and their application to algorithmic fairness; purposes of fairness audits (legal compliance vs. substantive non-discrimination); group vs. individual fairness.

**Key Questions**:
- What normative frameworks should guide intersectional fairness?
- How do prioritarian and sufficientarian views apply to algorithmic decision-making?
- What is the purpose of fairness auditing—compliance or substantive justice?
- How do different normative frameworks affect which groups matter and how much?

**Search Strategy**:
- Primary sources: SEP ("egalitarianism", "distributive justice"), PhilPapers (political philosophy, applied ethics, technology ethics), Semantic Scholar (philosophy + fairness)
- Key terms: "prioritarianism algorithmic fairness", "sufficientarianism", "egalitarianism machine learning", "normative foundations fairness", "distributive justice algorithms"
- Expected papers: 10-15 key papers
- Already in bibliography (do not duplicate): Parfit 1997, Frankfurt 1987, Slote 1989
- Look for: Applications of distributive justice theories to algorithmic fairness (philosophy venues + FAccT/Philosophy & Technology)

**Relevance to Project**: Shows that ontological uncertainty (which groups matter) is partly normative—different ethical frameworks yield different answers.

---

### Domain 6: Epistemic Uncertainty and Data Sparsity

**Focus**: Reasoning under uncertainty about group-level properties, epistemic justice in data collection, statistical reliability vs. representation of marginalized groups, trade-offs between sample size and group coverage.

**Key Questions**:
- How should we reason under statistical uncertainty in fairness auditing?
- What are the epistemic justice implications of requiring large sample sizes?
- How do researchers navigate trade-offs between statistical power and group representation?
- Are there epistemic arguments for or against expanding $\mathcal{G}$?

**Search Strategy**:
- Primary sources: PhilPapers (social epistemology, feminist epistemology, applied epistemology), Semantic Scholar (epistemic justice + algorithms, uncertainty + fairness)
- Key terms: "epistemic justice data", "epistemic uncertainty fairness", "statistical reliability fairness", "sample size fairness auditing", "data sparsity machine learning", "uncertainty quantification fairness"
- Expected papers: 8-12 key papers
- Look for: Miranda Fricker on epistemic injustice, data feminism literature, philosophy of statistics applied to fairness

**Relevance to Project**: Directly supports the "statistical uncertainty" horn of the dilemma and connects it to broader epistemic justice concerns.

---

### Domain 7: Critical Perspectives on Fairness Formalization

**Focus**: Fundamental critiques of fairness formalization projects, impossibility results, limitations of mathematical fairness, arguments that fairness cannot be fully operationalized, calls for qualitative/participatory approaches.

**Key Questions**:
- What are fundamental limitations of formal fairness approaches?
- Do critics argue that fairness formalization is inherently inadequate?
- How do impossibility results (e.g., fairness gerrymandering) relate to our dilemma?
- Are there alternatives to formal fairness auditing?

**Search Strategy**:
- Primary sources: Semantic Scholar (FAccT, critical algorithm studies), PhilPapers (philosophy of technology, critical theory)
- Key terms: "limitations fairness metrics", "critique algorithmic fairness", "impossibility fairness", "participatory fairness", "qualitative fairness assessment", "limits of formalization"
- Expected papers: 8-12 key papers
- Look for: Critical race theory + algorithms, feminist critiques of fairness formalization, STS perspectives
- Already in bibliography (do not duplicate): Himmelreich et al. 2025 (if it contains critical perspective)

**Relevance to Project**: Provides broader context for whether the dilemma is resolvable or points to fundamental limits of intersectional fairness auditing.

---

## Coverage Rationale

These seven domains provide comprehensive coverage because:

1. **Domains 1-2** establish the technical and philosophical state of the art on intersectionality
2. **Domains 3-4** provide theoretical foundations for the ontological uncertainty problem
3. **Domain 5** shows that normative disagreements compound ontological uncertainty
4. **Domain 6** provides theoretical foundations for the statistical uncertainty problem
5. **Domain 7** contextualizes whether the dilemma points to fundamental limits

The domains are weighted to balance ML/CS literature (Domains 1, 4, 6) with philosophy (Domains 2, 3, 5, 7), meeting the interdisciplinary requirement.

## Expected Gaps

Preliminary hypothesis (to be tested during research):

- **No existing work frames the interaction between statistical and ontological uncertainty as a dilemma** with two horns that exacerbate each other
- Technical ML literature treats sparse data as an engineering problem (solve with better methods) rather than recognizing ontological constraints
- Philosophy literature on intersectionality focuses on conceptual analysis without engaging statistical feasibility
- Existing work may identify one horn or the other, but not their interaction

## Estimated Scope

- **Total domains**: 7
- **Estimated papers**: 90-120 total (comprehensive review)
  - Domain 1: 20-30 papers
  - Domain 2: 12-18 papers
  - Domain 3: 10-15 papers
  - Domain 4: 10-15 papers
  - Domain 5: 10-15 papers
  - Domain 6: 8-12 papers
  - Domain 7: 8-12 papers
- **Key positions to cover**:
  - Technical optimism: sparse data problems are solvable with better methods (multicalibration, hierarchical models)
  - Ontological realism: there is a fact of the matter about which groups exist
  - Ontological constructivism: groups are constituted by social practices, not derivable from attributes
  - Critical skepticism: fairness formalization projects are fundamentally limited
  - Normative pluralism: different ethical frameworks yield different group prioritizations

## Search Priorities

1. **Foundational works**: Establish what "intersectionality" means in CS vs. philosophy; canonical formulations of fairness metrics
2. **Recent developments (2020-2025)**: Especially ML papers—field is moving quickly; use `--recent` flag with s2_search.py
3. **Critical responses**: Papers identifying limitations, impossibility results, or fundamental challenges to intersectional fairness
4. **Bridging work**: Papers that combine philosophical and technical perspectives (e.g., FAccT papers with normative arguments, philosophy papers engaging ML)

## Notes for Researchers

**Use philosophy-research skill scripts extensively**:
- Start each domain with `search_sep.py` for foundational philosophical context (Domains 2, 3, 5, 6, 7)
- Use `search_philpapers.py` for targeted philosophy searches with category filters
- For ML/CS papers: `s2_search.py` with `--recent` flag for 2020-2025 work, venue filters for FAccT/NeurIPS/ICML
- Use `search_openalex.py` for interdisciplinary work (philosophy + CS)
- Try `search_arxiv.py` for very recent preprints (2024-2025)

**Emphasis on critical perspectives**:
- Actively search for papers that identify limitations, impossibilities, or fundamental challenges
- Include papers that argue against the feasibility of intersectional fairness
- Balance technical optimism with philosophical skepticism

**Avoid duplicating existing bibliography**:
- The research proposal lists 20 papers already known to authors
- Cross-check found papers against this list before including
- Focus on filling gaps rather than re-finding canonical works

**Target output length**: Aim for comprehensive review (~5,000 words), which requires substantial literature base. Err on the side of more papers rather than fewer.

**Prioritize interdisciplinary sources**: Papers that bridge philosophy and ML/CS are especially valuable (e.g., FAccT papers with philosophical arguments, philosophy venues engaging with ML fairness).
