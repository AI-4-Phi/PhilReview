# Literature Review Plan: Mechanistic Interpretability and AI Safety

## Research Idea Summary

This literature review addresses a two-fold confusion in recent philosophical and technical literature: (1) the definition of "mechanistic interpretability" varies significantly across sources, ranging from narrow neuron-level activation analysis to broader functional explanations, and (2) the relationship between mechanistic interpretability (MI) and AI safety remains contested, with some authors claiming MI is necessary and/or sufficient for safety while others dispute these claims. This review aims to clarify these definitional and conceptual issues for an analytical philosophy audience.

## Key Research Questions

1. How do different authors and research communities define "mechanistic interpretability"? What are the sources of definitional disagreement?
2. Is mechanistic interpretability necessary for AI safety? What arguments support or challenge this claim?
3. Is mechanistic interpretability sufficient for AI safety? What other factors might be required?
4. What conceptual distinctions can help resolve the apparent confusion in the literature?

## Literature Review Domains

### Domain 1: Definitions and Taxonomy of Interpretability

**Focus**: Survey how "mechanistic interpretability," "explainability," and related terms are defined across philosophy of science, AI ethics, and technical ML literature. Identify competing definitions and their theoretical foundations.

**Key Questions**:
- What is the narrow vs. broad definition of mechanistic interpretability?
- How does MI relate to other forms of interpretability (functional, behavioral, counterfactual)?
- What role does the concept of "mechanism" play in philosophy of science definitions?
- How do technical ML researchers define MI compared to philosophers?

**Search Strategy**:
- Primary sources: SEP articles on "Scientific Explanation" and "Mechanisms in Science" via `search_sep.py`
- PhilPapers: "interpretability," "explainable AI," "mechanistic explanation" via `search_philpapers.py`
- Semantic Scholar: "mechanistic interpretability definition," "XAI taxonomy," "interpretability explainability distinction" via `s2_search.py --recent`
- arXiv: "mechanistic interpretability," "interpretability survey" via `search_arxiv.py`
- Expected papers: 12-18 key papers

**Relevance to Project**: Directly addresses core objective #1 (definitional clarity) by mapping the conceptual landscape.

---

### Domain 2: Technical Mechanistic Interpretability Methods

**Focus**: Survey the concrete technical methods used in mechanistic interpretability research, particularly in neural network analysis. This domain focuses on what practitioners actually DO when they claim to perform MI.

**Key Questions**:
- What methods count as "mechanistic interpretability" in practice? (e.g., activation analysis, circuit identification, feature visualization)
- How do these methods relate to traditional philosophy of science concepts of mechanism?
- What are the limitations and assumptions of current MI techniques?
- What is the state-of-the-art in MI as of 2024-2025?

**Search Strategy**:
- arXiv: "neural network circuits," "activation atlas," "mechanistic interpretability," "transformer circuits" via `search_arxiv.py --recent`
- Semantic Scholar: "interpretability methods deep learning," "feature visualization," "circuit discovery" via `s2_search.py`
- Focus on 2023-2025 papers showing recent developments
- Expected papers: 15-20 technical papers

**Relevance to Project**: Grounds philosophical analysis in actual technical practice; reveals what is operationally meant by "mechanistic."

---

### Domain 3: Philosophical Foundations of Explanation in AI

**Focus**: Philosophical literature on explanation, understanding, and mechanistic explanation as applied to AI systems. Includes philosophy of science and philosophy of mind perspectives.

**Key Questions**:
- How do philosophical theories of explanation (causal, mechanistic, functional) apply to AI?
- What constitutes "understanding" an AI system?
- Is mechanistic explanation the right kind of explanation for AI safety purposes?
- What is the relationship between explanation and prediction/control?

**Search Strategy**:
- SEP: "Mechanisms in Science," "Scientific Explanation," "Neuroscience" via `search_sep.py` and `fetch_sep.py`
- PhilPapers: "mechanistic explanation AI," "philosophy of AI explanation," "understanding machine learning" via `search_philpapers.py`
- Semantic Scholar: "Craver mechanisms AI," "mechanistic philosophy AI," "levels of explanation neural networks" via `s2_search.py`
- Key authors: Craver, Bechtel, Illari, Williamson (mechanism philosophers) + Lipton, Watson, Rudin (AI explanation)
- Expected papers: 10-15 papers

**Relevance to Project**: Provides philosophical rigor for analyzing competing definitions; clarifies what kind of explanation MI provides.

---

### Domain 4: AI Safety Theory and Requirements

**Focus**: What does "AI safety" mean, and what are its requirements? This domain surveys AI safety literature to understand what safety actually demands, enabling evaluation of whether MI is necessary/sufficient.

**Key Questions**:
- What are the core components of AI safety? (alignment, robustness, transparency, etc.)
- What role does interpretability play in different AI safety frameworks?
- What are the specific safety challenges that interpretability might address?
- Are there safety challenges that interpretability cannot address?

**Search Strategy**:
- arXiv: "AI safety," "AI alignment," "robustness deep learning," "AI safety requirements" via `search_arxiv.py --recent`
- Semantic Scholar: "AI safety interpretability," "transparency safety," "alignment problem" via `s2_search.py`
- OpenAlex: "artificial intelligence safety ethics" via `search_openalex.py`
- Key institutions: Anthropic, OpenAI, DeepMind safety teams
- Expected papers: 12-16 papers

**Relevance to Project**: Essential for evaluating necessity/sufficiency claims; defines the safety desiderata MI must satisfy.

---

### Domain 5: Arguments FOR MI as Necessary/Sufficient for Safety

**Focus**: Literature explicitly arguing that mechanistic interpretability is necessary and/or sufficient for AI safety. Includes both philosophical and technical arguments.

**Key Questions**:
- What arguments support the necessity claim?
- What arguments support the sufficiency claim?
- How strong are these arguments? What are their premises?
- What specific safety problems does MI supposedly solve?

**Search Strategy**:
- Start with: Kästner & Crook (2024) paper and its references
- Semantic Scholar: "interpretability necessary safety," "transparency AI safety requirement," "mechanistic interpretability safety" via `s2_search.py`
- Citation forward/backward search from Kästner & Crook via `s2_citations.py`
- PhilPapers: "interpretability safety argument" via `search_philpapers.py`
- Expected papers: 8-12 papers

**Relevance to Project**: Directly addresses core objective #2; maps strongest arguments for necessity/sufficiency.

---

### Domain 6: Arguments AGAINST MI as Necessary/Sufficient for Safety

**Focus**: Literature challenging the necessity and sufficiency claims, including alternative approaches to AI safety and critiques of interpretability-based safety.

**Key Questions**:
- What arguments challenge the necessity claim? (e.g., behavioral testing, formal verification)
- What arguments challenge the sufficiency claim? (e.g., explanation-action gap, context-dependence)
- What alternative or complementary approaches to safety exist?
- What are the limitations of MI for safety purposes?

**Search Strategy**:
- Start with: Hendrycks & Hiscott (2025) and its references
- Semantic Scholar: "interpretability limitations," "safety without interpretability," "formal verification AI," "testing vs interpretability" via `s2_search.py --recent`
- arXiv: "AI safety formal methods," "adversarial robustness," "scalable oversight" via `search_arxiv.py`
- Expected papers: 10-14 papers

**Relevance to Project**: Balances the review; identifies counterarguments and alternatives; supports gap analysis.

---

### Domain 7: Case Studies and Empirical Evidence

**Focus**: Empirical studies and case examples that test whether MI actually improves safety outcomes, or cases where MI failed/succeeded in identifying safety issues.

**Key Questions**:
- What empirical evidence exists for MI improving safety?
- What case studies demonstrate MI identifying safety problems?
- What case studies show MI limitations or failures?
- Is there quantitative evidence linking interpretability to safety outcomes?

**Search Strategy**:
- Semantic Scholar: "interpretability evaluation," "interpretability safety empirical," "case study interpretability," "debugging neural networks" via `s2_search.py`
- arXiv: "empirical interpretability," "interpretability benchmark," "red teaming language models" via `search_arxiv.py --recent`
- OpenAlex: "machine learning debugging interpretability" via `search_openalex.py`
- Expected papers: 8-12 papers

**Relevance to Project**: Grounds philosophical analysis in empirical reality; shows whether theoretical arguments hold in practice.

---

## Coverage Rationale

These seven domains provide comprehensive coverage by:

1. **Definitional clarity** (Domains 1-2): Establishing what MI means across communities and in practice
2. **Philosophical foundations** (Domain 3): Grounding analysis in philosophy of science
3. **Safety requirements** (Domain 4): Understanding what safety demands
4. **Argumentative landscape** (Domains 5-6): Mapping both sides of the necessity/sufficiency debate
5. **Empirical grounding** (Domain 7): Testing theoretical claims against evidence

This structure enables a rigorous analytical philosophy treatment while engaging with both technical and philosophical literature.

## Expected Gaps

Preliminary thoughts on gaps this research could fill:

1. **Conceptual clarity**: Lack of precise definitions and distinctions between types of interpretability
2. **Argument analysis**: Insufficiently rigorous analysis of necessity/sufficiency arguments
3. **Integration**: Little cross-disciplinary synthesis between philosophy of science (mechanisms) and AI safety literature
4. **Empirical gap**: Disconnect between theoretical claims about MI and empirical evidence
5. **Alternative frameworks**: Under-exploration of how MI relates to other safety approaches

## Estimated Scope

- **Total domains**: 7
- **Estimated papers**: 75-105 total (averaging 12-15 per domain)
- **Key positions**:
  - Narrow vs. broad definitions of MI
  - MI-necessary-for-safety position
  - MI-sufficient-for-safety position
  - MI-helpful-but-not-necessary/sufficient position
  - Alternative safety approaches (formal methods, behavioral testing)

## Search Priorities

1. **Foundational works**: Philosophy of science on mechanisms (Craver, Bechtel), classic AI safety papers
2. **Recent developments**: 2023-2025 papers on MI methods, safety frameworks, and empirical studies
3. **Critical responses**: Direct responses to Kästner & Crook, Hendrycks & Hiscott, and other key claims
4. **Interdisciplinary bridges**: Papers that connect philosophy and technical ML (especially in philosophy of science journals and arXiv)

## Notes for Researchers

### Critical Instructions:

1. **USE PHILOSOPHY-RESEARCH SKILL SCRIPTS EXTENSIVELY**: All domain researchers MUST use the structured API search scripts:
   - `search_sep.py` for philosophical foundations
   - `search_philpapers.py` for philosophy literature
   - `s2_search.py --recent` for recent interdisciplinary work (emphasize 2023-2025)
   - `search_arxiv.py --recent` for latest technical work
   - `search_openalex.py` for broad academic coverage
   - `s2_citations.py` for forward/backward citation traversal from key papers

2. **PRIORITIZE RECENT WORK**: User specified 2023-2025 focus. Use `--recent` flags and date filters where available.

3. **VERIFY KEY PAPERS**:
   - Kästner & Crook (2024) - DOI: 10.1007/s13194-024-00614-4
   - Hendrycks & Hiscott (2025) - verify if published or preprint

4. **BALANCED COVERAGE**: Ensure representation of:
   - Technical ML community perspective
   - Philosophy of science perspective
   - AI ethics/safety perspective
   - Both pro- and anti-MI-for-safety positions

5. **QUALITY OVER QUANTITY**: 75-105 papers is a target range. Prioritize highly relevant, rigorous papers over marginal citations.

6. **BIBTEX QUALITY**: Ensure all BibTeX entries include:
   - DOI when available
   - URLs for verification
   - Abstract summaries
   - Proper author formatting
   - Accurate publication venues and dates

### Expected Timeline:

- Domain 1-2: Foundational, may take longer due to definitional survey work
- Domain 3: Rich SEP/PhilPapers content available
- Domain 4-7: Recent, active literature - should be abundant on arXiv and Semantic Scholar

### Integration Notes:

Synthesis writers should watch for:
- Definitional shifts across domains (same term, different meanings)
- Implicit assumptions about what "mechanism" means
- Empirical evidence (or lack thereof) for theoretical claims
- Disciplinary differences in argument standards
- Gaps where philosophical rigor could strengthen technical claims
