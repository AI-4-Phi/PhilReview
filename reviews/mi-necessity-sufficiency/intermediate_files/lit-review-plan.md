# Literature Review Plan: Mechanistic Interpretability and AI Safety

## Research Idea Summary

This project examines whether mechanistic interpretability (MI) is necessary, sufficient, or neither for AI safety. The research addresses a fundamental conceptual confusion in the field: some authors (Hendrycks and Hiscott 2025) construe MI narrowly as analysis of individual neural activations, while others (Kastner and Crook 2024) include functional and higher-level mechanistic explanations. This definitional divergence has direct normative implications for what interpretability approaches AI safety requires.

## Key Research Questions

1. **Definitional**: What counts as "mechanistic interpretability"? How should we demarcate MI from other forms of XAI (e.g., post-hoc explanations, behavioral testing)?
2. **Conceptual**: How does the philosophy of science literature on mechanistic explanation bear on MI definitions in machine learning?
3. **Normative (Necessity)**: Is MI necessary for AI safety? Can systems be safe without mechanistic understanding of their internal workings?
4. **Normative (Sufficiency)**: Is MI sufficient for AI safety? Does understanding internal mechanisms guarantee safe deployment?
5. **Metatheoretical**: What epistemic standards should govern claims about AI system safety?

## Literature Review Domains

### Domain 1: Mechanistic Explanation in Philosophy of Science

**Focus**: The foundational philosophical literature on what makes an explanation "mechanistic," including debates about levels, decomposition, and the relationship between mechanism and function.

**Key Questions**:
- What constitutes a mechanistic explanation in philosophy of science?
- How do mechanistic explanations relate to functional explanations?
- What role do levels of organization play in mechanistic explanation?
- How does the "new mechanism" literature inform computational/AI contexts?

**Search Strategy**:
- Primary sources: SEP entries on "Mechanisms in Science," "Scientific Explanation"
- Key terms: ["mechanistic explanation", "new mechanism philosophy", "Craver mechanism", "Machamer Darden Craver", "levels of mechanism", "functional explanation mechanism", "componential explanation"]
- Key authors: Craver, Bechtel, Machamer, Darden, Glennan, Illari, Kaplan
- Expected papers: 12-18 foundational papers

**Relevance to Project**: Establishes the philosophical framework for evaluating whether MI in ML genuinely qualifies as "mechanistic" explanation, and at what grain of analysis.

---

### Domain 2: Explainable AI (XAI) Taxonomies and Definitions

**Focus**: The broader XAI literature that situates mechanistic interpretability within a taxonomy of explanation types, including post-hoc vs. inherent interpretability, local vs. global explanations, and model-agnostic vs. model-specific methods.

**Key Questions**:
- How do XAI researchers taxonomize different forms of interpretability?
- Where does mechanistic interpretability fit within XAI typologies?
- What distinguishes "interpretability" from "explainability" in the literature?
- How do different XAI approaches serve different epistemic and practical goals?

**Search Strategy**:
- Primary sources: PhilPapers (philosophy of AI), arXiv (cs.AI, cs.LG)
- Key terms: ["explainable AI taxonomy", "XAI survey", "interpretability vs explainability", "post-hoc explanation AI", "inherent interpretability", "local global explanation", "LIME SHAP mechanistic"]
- Expected papers: 15-20 papers (mix of CS surveys and philosophical analyses)

**Relevance to Project**: Provides the conceptual landscape against which MI's distinctiveness (or lack thereof) can be assessed.

---

### Domain 3: Mechanistic Interpretability in Machine Learning (Technical Literature)

**Focus**: The technical ML literature on mechanistic interpretability specifically, including circuit analysis, feature visualization, activation patching, and interpretability of transformer architectures.

**Key Questions**:
- What methods constitute "mechanistic interpretability" in current ML practice?
- How do MI researchers define their object of study?
- What are the key achievements and limitations of MI methods (e.g., Anthropic's circuit analysis)?
- How do practitioners distinguish MI from other interpretability approaches?

**Search Strategy**:
- Primary sources: arXiv (cs.LG, cs.AI), Semantic Scholar, Anthropic/DeepMind publications
- Key terms: ["mechanistic interpretability", "circuit analysis neural network", "activation patching", "feature visualization deep learning", "transformer interpretability", "superposition interpretability", "sparse autoencoders interpretability"]
- Key authors/labs: Olah, Elhage, Conerly (Anthropic), Neel Nanda, Rauker
- Expected papers: 15-20 technical papers (2020-2025)

**Relevance to Project**: Establishes what MI practitioners actually mean and do, which is essential for evaluating philosophical claims about MI.

---

### Domain 4: AI Safety Frameworks and Desiderata

**Focus**: Literature defining AI safety goals, threat models, and the properties safe AI systems should have. Includes alignment, robustness, controllability, and value alignment literatures.

**Key Questions**:
- What properties must AI systems have to be considered "safe"?
- How do AI safety researchers conceptualize the relationship between understanding and safety?
- What threat models (deceptive alignment, goal misgeneralization, etc.) does MI address or fail to address?
- What alternative or complementary safety approaches exist (RLHF, constitutional AI, formal verification)?

**Search Strategy**:
- Primary sources: arXiv (cs.AI), AI Alignment Forum, PhilPapers
- Key terms: ["AI safety framework", "AI alignment", "deceptive alignment", "goal misgeneralization", "AI controllability", "value alignment AI", "AI existential risk", "AI governance safety"]
- Key authors/organizations: Russell, Amodei, Christiano, MIRI, Anthropic, DeepMind safety team
- Expected papers: 15-20 papers

**Relevance to Project**: Defines the target explanandum (AI safety) whose relationship to MI is under investigation.

---

### Domain 5: Necessity and Sufficiency Arguments for Interpretability in AI Safety

**Focus**: The specific debate about whether interpretability (mechanistic or otherwise) is required for safe AI, including arguments for and against, and alternative safety paradigms.

**Key Questions**:
- What arguments support MI as necessary for AI safety?
- What arguments support MI as sufficient for AI safety?
- What counterarguments exist (e.g., behavioral testing suffices, MI is intractable)?
- How do empirical and normative considerations interact in these arguments?

**Search Strategy**:
- Primary sources: arXiv, PhilPapers, AI Alignment Forum, philosophy of science journals
- Key terms: ["interpretability necessary AI safety", "interpretability sufficient safety", "black box AI safety", "behavioral testing AI", "interpretability scalability", "understanding AI systems safety"]
- Key papers: Hendrycks and Hiscott 2025, Kastner and Crook 2024, responses and citations
- Expected papers: 10-15 papers (focus on 2023-2025)

**Relevance to Project**: Directly addresses the core normative questions of the research.

---

### Domain 6: Epistemic Standards and Normative Dimensions of AI Explanation

**Focus**: Philosophical literature on what we can know about AI systems, epistemic opacity, and the normative demands (ethical, legal, social) for AI explanation.

**Key Questions**:
- What epistemic access do we have to AI system internals?
- How does "epistemic opacity" constrain what interpretability can achieve?
- What normative frameworks (ethical, legal) govern demands for AI explanation?
- How do right-to-explanation requirements relate to MI?

**Search Strategy**:
- Primary sources: SEP, PhilPapers, philosophy journals, law reviews
- Key terms: ["epistemic opacity AI", "AI epistemology", "right to explanation AI", "GDPR explainability", "AI transparency ethics", "algorithmic accountability", "AI epistemic standards"]
- Key authors: Burrell, Humphreys, Zerilli, Sullivan
- Expected papers: 12-15 papers

**Relevance to Project**: Provides the epistemological and normative framework for assessing what MI can and should deliver.

---

## Coverage Rationale

These six domains provide comprehensive coverage by addressing:

1. **Conceptual foundations**: Domains 1-2 establish what "mechanistic" and "interpretability" mean philosophically and in AI research
2. **Technical grounding**: Domain 3 ensures the review is empirically informed about actual MI methods
3. **Safety context**: Domain 4 defines the safety goals MI is supposed to serve
4. **Core debate**: Domain 5 directly addresses the necessity/sufficiency questions
5. **Normative framing**: Domain 6 situates the debate within broader epistemic and ethical considerations

The domains are ordered to build understanding progressively: philosophical foundations, then technical landscape, then the specific debate, then normative evaluation.

## Expected Gaps

Based on initial analysis, the research may identify gaps in:

1. **Definitional clarity**: No consensus definition of MI that maps cleanly onto philosophical accounts of mechanism
2. **Level-relativity**: Insufficient attention to how MI claims vary by level of analysis (neuron vs. circuit vs. module)
3. **Sufficiency arguments**: More attention to necessity than sufficiency in the literature
4. **Empirical grounding**: Philosophical arguments often proceed without engagement with technical limitations
5. **Alternative safety paradigms**: Underexplored how MI compares to behavioral testing, formal methods, or process-based approaches

## Estimated Scope

- **Total domains**: 6
- **Estimated papers**: 70-100 total
- **Key positions**:
  - MI is necessary and sufficient (strong pro-MI)
  - MI is necessary but not sufficient (moderate pro-MI)
  - MI is neither necessary nor sufficient (skeptical)
  - MI is sufficient but not necessary (unusual position, likely underrepresented)

## Search Priorities

1. **Foundational works**: Craver/Bechtel on mechanism; classic XAI surveys; seminal AI safety papers
2. **Key debate papers**: Hendrycks and Hiscott 2025; Kastner and Crook 2024; direct responses
3. **Recent developments**: 2023-2025 papers on MI methods and safety applications
4. **Critical responses**: Papers skeptical of MI's role in safety
5. **Interdisciplinary bridges**: Papers explicitly connecting philosophy of science to ML interpretability

## Notes for Researchers

### Search Script Recommendations

- **Domain 1**: Start with `search_sep.py` for "Mechanisms in Science" and "Scientific Explanation"; use `search_philpapers.py` for "mechanistic explanation" + "Craver"
- **Domain 2**: Use `search_arxiv.py` with "explainable AI survey" (cs.AI); `search_philpapers.py` for "explainability interpretability"
- **Domain 3**: Heavy use of `search_arxiv.py` (cs.LG) with terms like "mechanistic interpretability", "circuit analysis"; `s2_search.py` for author searches (Olah, Elhage)
- **Domain 4**: `search_arxiv.py` for "AI alignment", "AI safety"; `search_philpapers.py` for "AI existential risk"
- **Domain 5**: Start from known papers (Hendrycks/Hiscott, Kastner/Crook); use `s2_search.py` with `--recent` flag; check citations
- **Domain 6**: `search_sep.py` for "Epistemology of AI"; `search_philpapers.py` for "epistemic opacity"; `search_openalex.py` for law review articles

### Special Instructions

1. **Temporal focus**: Prioritize 2023-2025 for Domains 3 and 5; allow broader range for philosophical foundations (Domains 1 and 6)
2. **Citation tracking**: For key debate papers (Hendrycks/Hiscott, Kastner/Crook), use citation tracking to find responses
3. **Preprints**: Include arXiv preprints for Domains 3-5 given rapid field development
4. **Cross-referencing**: Note when papers span multiple domains for synthesis planning
5. **Audience calibration**: Prioritize papers accessible to analytic philosophers; technical ML papers should be balanced with philosophical interpretations

### Key Papers to Anchor Searches

- Hendrycks, D. and Hiscott, L. (2025). "The Misguided Quest for Mechanistic AI Interpretability"
- Kastner, L. and Crook, B. (2024). "Explaining AI through Mechanistic Interpretability"
- Craver, C. (2007). *Explaining the Brain* (foundational mechanism)
- Lipton, Z. (2018). "The Mythos of Model Interpretability" (XAI foundations)
- Olah et al. (2020). "Zoom In: An Introduction to Circuits" (MI foundations)
