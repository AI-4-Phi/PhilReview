# Literature Review Outline

**Research Project**: The Intersectionality Dilemma for Algorithmic Fairness
**Date**: 2026-01-10
**Total Literature Base**: 99 papers across 7 domains
**Target Audience**: ACM FAccT, Synthese, Philosophy & Technology (interdisciplinary ML/philosophy)

---

## Introduction

**Purpose**: Frame the intersectionality dilemma as arising from the interaction of two independent problems—statistical uncertainty and ontological uncertainty—neither of which has been adequately recognized as fundamentally limiting fairness auditing.

**Content**:
- Intersectional fairness auditing requires (1) estimating model performance across groups and (2) specifying which groups warrant consideration
- The first faces statistical uncertainty from sparse data; the second faces ontological uncertainty about social group constitution
- These problems interact: expanding groups exacerbates sparsity; constraining groups requires resolving contested ontological questions
- **Key claim**: Existing work treats these as separate optimization problems; we argue they form an intractable dilemma
- Review structure: technical approaches (Section 1), ontological debates (Section 2), measurement validity (Section 3), normative pluralism (Section 4), gaps (Section 5)

**Key Papers**:
- Crenshaw 1989 (foundational intersectionality concept from legal discrimination)
- Hébert-Johnson et al. 2018 (multicalibration as technical solution to exponentially many groups)
- Kong 2022 (philosophical analysis identifying dilemma between infinite regress and fairness gerrymandering)
- Haslanger 2012 (social construction of groups as practice-based, not attribute-based)

**Word Target**: 400-500 words

---

## Section 1: Technical Approaches to Intersectional Fairness and Their Limits

**Section Purpose**: Establish that the ML community has developed sophisticated technical solutions to statistical challenges (multicalibration, differential fairness, sparse data methods) but these solutions assume group specification is given, leaving the ontological problem unaddressed.

**Main Claims**:
1. Multicalibration and subgroup fairness frameworks demonstrate that calibration across exponentially many groups is computationally tractable
2. Recent work on sparse data provides statistical methods for handling small intersectional groups
3. Fairness gerrymandering reveals that even sophisticated metrics are vulnerable to strategic group selection
4. **Gap**: Technical solutions treat group specification as an input, not a contested normative-ontological question

### Subsection 1.1: Multicalibration and Rich Subgroup Frameworks

**Papers**: Hébert-Johnson et al. 2018, Gopalan et al. 2022, Lee et al. 2025, Globus-Harris et al. 2023

**Content**:
- Multicalibration requires calibrated predictions across rich collections of efficiently computable subgroups
- Efficient algorithms avoid explicit enumeration, achieving multicalibration without listing all intersections
- Low-degree multicalibration (Gopalan et al.) addresses sample complexity: exponentially growing data requirements motivate approximations
- Extensions to continuous and mixed-type attributes (Lee et al.) broaden beyond categorical intersections
- **Limitation**: Framework assumes class of group-defining functions is given; which functions to include remains unspecified

**Gap Connection**: Multicalibration's computational tractability depends on pre-specifying which attribute combinations define protected groups. No principled method for determining this set.

**Word Target**: 600-700 words

### Subsection 1.2: Sparse Data and Statistical Reliability

**Papers**: Ferrara et al. 2025, Cherian & Candès 2023, Zhioua et al. 2025, Jourdan et al. 2023, Singh & Chunara 2023

**Content**:
- Size-adaptive hypothesis testing (Ferrara et al.) handles varying data availability across groups
- Statistical inference frameworks (Cherian & Candès) provide rigorous auditing across rich subgroup collections with multiple testing control
- Sampling bias research (Zhioua et al.) distinguishes sample size bias from underrepresentation bias, showing these compound for marginalized groups
- Empirical evidence (Jourdan et al.) that fairness metrics yield unreliable, diverging results with small samples
- Sample size requirements (Singh & Chunara) for disparity estimation reveal trade-off: more groups = less precision per group under fixed budgets

**Gap Connection**: Even with sophisticated statistical methods, expanding intersectional coverage necessarily reduces per-group sample sizes, undermining reliability. Statistical rigor cannot eliminate this trade-off.

**Word Target**: 500-600 words

### Subsection 1.3: Fairness Gerrymandering and the Group Specification Problem

**Papers**: Kong 2022, Kearns et al. 2018, Tian et al. 2024, Räz 2023

**Content**:
- Fairness gerrymandering: classifiers appear fair on predefined groups but violate fairness on intersectional subgroups
- Kong's philosophical analysis: dominant statistical parity approach faces "dilemma between infinite regress and fairness gerrymandering"—either continuously split groups or arbitrarily select which to protect
- Kearns et al. prove preventing gerrymandering requires fairness across exponentially many subgroups, computationally equivalent to hard agnostic learning
- Gerrymandering extends to individual fairness (Räz), showing problem is fundamental to fairness metrics, not specific to group approaches
- MultiFair (Tian et al.) demonstrates empirically that per-attribute fairness leaves intersections unfair

**Gap Connection**: Gerrymandering is consequence of ontological uncertainty about group specification. Without principled method for determining which groups exist, metrics can be gamed through strategic selection.

**Word Target**: 500-600 words

### Subsection 1.4: Recent Philosophical-Technical Syntheses

**Papers**: Himmelreich et al. 2024, Gohar & Cheng 2023

**Content**:
- Himmelreich et al. explicitly frame intersectionality problem as involving both statistical challenges (small groups) and moral-methodological challenges (which groups matter)
- Survey work (Gohar & Cheng) identifies data scarcity as key challenge alongside computational complexity and metric selection
- **Critical observation**: Even papers recognizing both dimensions treat them as separate optimization problems rather than interacting constraints

**Gap Connection**: Existing philosophical-technical bridges identify statistical and normative dimensions but do not theorize their interaction as a dilemma.

**Word Target**: 300-400 words

**Section Summary**: Technical ML literature has achieved remarkable sophistication in handling exponentially many groups and sparse data. However, these solutions presuppose group specifications as inputs. Fairness gerrymandering demonstrates that strategic group selection undermines metrics, yet no computational method can determine "correct" groups from data alone. This reveals the unaddressed ontological dimension.

**Section Word Target**: 2000-2300 words

---

## Section 2: Ontological Uncertainty—The Social Construction of Intersectional Groups

**Section Purpose**: Establish that philosophical debates about social group constitution reveal deep disagreement about whether groups can be algorithmically derived from attributes or must be specified through practice-based, context-dependent processes. This ontological uncertainty is not resolvable through better conceptual analysis.

**Main Claims**:
1. Attribute-based accounts (treating groups as defined by shared demographic features) conflict with practice-based accounts (groups constituted through social roles, conferral, structural positioning)
2. Intersectionality theory itself divides between analytical/causal and hermeneutic/emergent interpretations
3. These ontological disagreements directly undermine algorithmic group specification: different metaphysical views yield different answers about which intersections exist
4. **Gap**: Philosophy literature focuses on conceptual analysis without engaging algorithmic implementation; ML literature assumes attribute-based ontology without philosophical justification

### Subsection 2.1: Intersectionality—Emergence vs. Reduction

**Papers**: Jorba & López de Sa 2024, Bernstein 2020, O'Connor et al. 2019, Yuval-Davis 2006, Carastathis 2016, Collins 2019

**Content**:
- Emergence view (Jorba & López de Sa): intersectional experiences emerge when social structures make category conjunctions relevant; cannot be reduced to additive effects
- Metaphysical questions (Bernstein): are intersectional identities ontologically novel or reducible to constituent categories? Grounding relations between intersections and base categories?
- Agent-based modeling (O'Connor et al.) shows intersectional disadvantage can emerge from bargaining dynamics even without explicit encoding
- Additive vs. mutually constitutive models (Yuval-Davis): additive models are computationally tractable but fail to capture how categories co-construct each other
- Black feminist theory (Collins, Carastathis): intersectionality as critical inquiry, not neutral analytic framework; resists formalization that domesticates radical potential

**Gap Connection**: If intersectional categories emerge contextually from social structures (not just from attribute combinations), algorithms cannot pre-specify all relevant groups. Emergence implies ontological openness incompatible with fixed fairness auditing schemas.

**Word Target**: 700-800 words

### Subsection 2.2: Social Ontology—Attribute-Based vs. Practice-Based Group Constitution

**Papers**: Haslanger 2012, Mallon 2016, Ásta 2018, Ritchie 2018, Thomasson 2019, Popescu-Sarry 2023

**Content**:
- Political constructionism (Haslanger): race and gender are social positions defined by systematic subordination/privilege, not intrinsic attributes
- Social role HPC kinds (Mallon): groups stabilized by homeostatic mechanisms of social roles; categories are contingent artifacts of practices, not natural divisions
- Conferralism (Ásta): social properties constituted through communal conferral; same attributes can ground different properties in different contexts
- Structuralism (Ritchie): groups are networks of social relations, not collections defined by shared attributes
- Ontological pluralism (Thomasson): different types of groups (gender, race, disability) may have fundamentally different constitution conditions
- Discrimination as construction (Popescu-Sarry): discrimination doesn't apply to pre-existing groups but constitutes groups through differential treatment

**Gap Connection**: Practice-based accounts imply that groups cannot be derived algorithmically from demographic features because group membership depends on social practices, conferral, and structural positioning that resist formalization. This creates irreducible ontological uncertainty for algorithmic group specification.

**Word Target**: 800-900 words

### Subsection 2.3: Methodological Tensions—Ameliorative Analysis and Regulative Ideals

**Papers**: Haslanger 2005, Jones 2014, Gasdaglis & Madva 2020

**Content**:
- Ameliorative analysis (Haslanger): concepts of social kinds should be evaluated for usefulness in critique, not just descriptive accuracy
- Application to intersectionality (Jones): can ameliorative analysis capture how multiple memberships affect lived experience, or does it require integrated account?
- Regulative ideal interpretation (Gasdaglis & Madva): intersectionality as guiding methodological principle, not substantive metaphysical thesis; sidesteps ontological questions by treating categories as provisional

**Gap Connection**: Ameliorative and regulative approaches suggest that there may be no politically neutral, purely descriptive way to specify groups. Ontological questions are partly normative, compounding uncertainty.

**Word Target**: 400-500 words

**Section Summary**: Philosophical debates reveal that group constitution is contested between attribute-based and practice-based accounts, with intersectionality theory itself divided between analytical and hermeneutic interpretations. These disagreements are not merely terminological but reflect fundamental differences about whether social groups have algorithmic-discoverable structures or context-dependent, practice-constituted boundaries. This ontological uncertainty is irreducible.

**Section Word Target**: 2000-2200 words

---

## Section 3: Measurement Validity—Do Fairness Metrics Measure What They Claim?

**Section Purpose**: Show that even when groups are specified, fairness metrics face construct validity problems—they lack clear articulations of what is being measured and often fail to correlate with normative fairness goals. This amplifies the dilemma by showing that operationalization challenges persist even after group specification.

**Main Claims**:
1. Measurement theory framework reveals that fairness metrics often lack construct validity
2. Target specification bias: operationalizations diverge from decision-makers' actual concerns
3. Empirical evidence shows fairness metrics are incompatible, unreliable with small samples, and misaligned with human judgments
4. **Gap**: Most measurement critiques focus on individual metrics; less attention to whether contested normative concepts like fairness can be validly operationalized at all

### Subsection 3.1: Construct Validity and Target Specification Bias

**Papers**: Tal 2023, Blodgett et al. 2021, Jacobs et al. 2020, Bean et al. 2025

**Content**:
- Target specification bias (Tal): operationalization of target variable doesn't match decision-makers' definitions; persists independently of data limitations
- Measurement modeling (Blodgett et al.): fairness benchmarks lack clear articulations of what is being measured, threatening validity
- Unobservable theoretical constructs (Jacobs et al.): fairness is theoretical construct requiring careful conceptualization before operationalization; mismatches create harms
- LLM benchmark analysis (Bean et al.): systematic review reveals patterns undermining construct validity across AI evaluation

**Gap Connection**: If fairness is a contested normative concept that resists stable operationalization, then specifying which groups to audit doesn't resolve measurement challenges. Target specification bias compounds group specification uncertainty.

**Word Target**: 500-600 words

### Subsection 3.2: Empirical Evidence of Metric Unreliability

**Papers**: Delobelle et al. 2022, Cao et al. 2022, Constantin et al. 2022, Long 2020

**Content**:
- Bias metric incompatibility (Delobelle et al.): fairness metrics for language models are not compatible; values depend on arbitrary choices (templates, seeds)
- Intrinsic vs. extrinsic fairness (Cao et al.): intrinsic and extrinsic metrics don't correlate, suggesting intrinsic metrics may not measure what matters
- Human judgment misalignment (Constantin et al.): algorithmic metrics don't align with human fairness judgments
- Normative critique (Long): false positive rate equality is "morally irrelevant" despite mathematical well-definedness

**Gap Connection**: Metric incompatibility and unreliability suggest fairness is not a unitary construct that can be operationalized through single metrics. This undermines assumption that valid auditing is possible once groups are specified.

**Word Target**: 400-500 words

### Subsection 3.3: Distributive Justice Foundations and Metric Diversity

**Papers**: Baumann et al. 2022, Truong et al. 2025, Buijsman 2023

**Content**:
- Unifying framework (Baumann et al.): different fairness metrics embody contested philosophical commitments about distributive justice
- Fair Equality of Chances (Truong et al.): construct validity problems stem from insufficient systematization; philosophical frameworks can guide valid operationalization
- Navigating tradeoffs (Buijsman): metric incompatibility requires normative theory to guide choices; Rawlsian framework as substantive solution

**Gap Connection**: Metric diversity partly reflects fairness's conceptual complexity and contested normative foundations. Choice between metrics is not technical but requires philosophical framework—itself contested.

**Word Target**: 400-500 words

**Section Summary**: Measurement theory reveals that fairness metrics face systematic construct validity problems: unclear conceptualizations, target specification bias, incompatibility, and misalignment with human judgments. These problems suggest that fairness—as a contested normative concept—may resist valid operationalization. This compounds the dilemma: even after specifying groups, measurement challenges remain.

**Section Word Target**: 1400-1600 words

---

## Section 4: Normative Pluralism—Which Groups Matter and Why?

**Section Purpose**: Demonstrate that different normative frameworks (prioritarianism, sufficientarianism, egalitarianism, relational equality) yield different answers about which groups warrant protection and how to prioritize them. This reveals that ontological uncertainty about group specification is partly normative, not purely metaphysical or empirical.

**Main Claims**:
1. Prioritarian, sufficientarian, and egalitarian frameworks differ not just in how much inequality to tolerate but in which groups matter and why
2. Fairness auditing serves distinct purposes (legal compliance vs. substantive justice) requiring different normative foundations
3. Normative disagreements compound ontological uncertainty: different ethical theories generate different group prioritizations
4. **Gap**: Most fairness work treats metric choice as technical; limited recognition that which groups matter is partly normative question

### Subsection 4.1: Distributive Justice Frameworks—Priorities and Thresholds

**Papers**: Shields 2016, Timmer 2021, Arneson 2000, Parfit 2012, Anderson 1999, Fazelpour et al. 2021

**Content**:
- Sufficientarianism (Shields, Timmer): securing sufficiency has special moral importance; groups below thresholds warrant priority
- Prioritarianism (Arneson, Parfit): greater moral weight to benefits for worse-off individuals; worst-off intersectional groups receive strongest priority
- Relational egalitarianism (Anderson): fundamental aim is preventing domination and creating equal social relations, not equalizing distributions
- Dynamic fairness (Fazelpour et al.): evaluate trajectories not snapshots; different frameworks prioritize different temporal dynamics

**Gap Connection**: These frameworks yield different answers to which intersectional groups warrant auditing: sufficientarians focus on groups below thresholds, prioritarians on worst-off groups, egalitarians on all groups equally, relationalists on groups facing domination. Ontological question (which groups) is partly normative.

**Word Target**: 600-700 words

### Subsection 4.2: Applications to Algorithmic Fairness

**Papers**: Hertweck et al. 2024, Holm 2025, Green 2022, Binns 2024

**Content**:
- Approximate justice (Hertweck et al.): algorithmic fairness should focus on distribution of errors, not just outcomes; different frameworks apply differently
- Separateness of persons (Holm): Broomean fairness requires respecting individual claims; statistical parity insufficient
- Formal vs. substantive fairness (Green): formal approaches focus on isolated decisions; substantive approaches examine structural context and power relations
- Rawlsian limits (Binns): Difference Principle doesn't transfer well to algorithmic contexts; may need alternative frameworks

**Gap Connection**: Normative framework choice affects both which groups matter and the purpose of auditing (compliance vs. structural transformation). This normative dimension is irreducible.

**Word Target**: 500-600 words

**Section Summary**: Different normative frameworks yield systematically different answers about which intersectional groups deserve protection and priority. Since these frameworks are contested in political philosophy, there is no neutral, objective way to determine which groups to audit. Ontological uncertainty is compounded by normative pluralism.

**Section Word Target**: 1200-1400 words

---

## Section 5: Epistemic Justice and the Dilemma's Interaction Effects

**Section Purpose**: Show how statistical uncertainty and ontological uncertainty interact to create a genuine dilemma, with epistemic justice concerns revealing that both horns involve structural injustice, not merely technical challenges.

**Main Claims**:
1. Data sparsity for marginalized groups constitutes epistemic injustice, not just statistical inconvenience
2. Requiring large sample sizes excludes groups from epistemic representation
3. Expanding group coverage to address ontological adequacy exacerbates statistical problems; constraining coverage to ensure reliability perpetuates epistemic marginalization
4. **Gap**: No existing work frames this interaction as a dilemma where addressing one horn worsens the other

### Subsection 5.1: Epistemic Injustice in Algorithmic Systems

**Papers**: Fricker 2007, Symons & Alvarado 2022, Anderson 2012, Hull 2023, Milano & Prunkl 2024

**Content**:
- Foundational framework (Fricker): testimonial injustice (credibility deficits) and hermeneutical injustice (gaps in collective interpretive resources)
- Application to data science (Symons & Alvarado): data collection practices and algorithmic opacity perpetrate epistemic injustices
- Institutional epistemic justice (Anderson): requires social institutions to correct for identity-prejudicial credibility assessments
- Data labeling (Hull): economic structure of data work creates hermeneutical injustice by excluding labelers from conceptualization
- Epistemic fragmentation (Milano & Prunkl): algorithmic profiling isolates individuals, undermining collective sense-making about harms

**Gap Connection**: Sparse data represents not just missing information but systematic undermining of marginalized groups' epistemic standing. Sample size requirements for statistical reliability can constitute epistemic injustice.

**Word Target**: 500-600 words

### Subsection 5.2: The Interaction—Statistical Reliability vs. Ontological Adequacy

**Papers**: Kong 2022, Zhioua et al. 2025, Konstantinov & Lampert 2021, Mhasawade et al. 2024

**Content**:
- Kong's dilemma formulation: infinite regress (continuous splitting creates ever-smaller groups) vs. fairness gerrymandering (arbitrary group selection)
- Sampling bias (Zhioua et al.): bias borne unequally by groups with sparse data, compounding discrimination
- Theoretical limits (Konstantinov & Lampert): underrepresentation creates fundamental vulnerabilities that cannot be overcome by collecting more data
- Explanation disparities (Mhasawade et al.): sparse data creates unequal explanation quality across groups—epistemic harm

**Gap Connection**: **This is the core dilemma**: expanding intersectional coverage to address ontological adequacy necessarily reduces per-group sample sizes, undermining statistical reliability. Constraining coverage to ensure reliability requires resolving contested ontological questions about which groups exist—but no resolution is available.

**Word Target**: 500-600 words

### Subsection 5.3: Critical Perspectives—Is the Dilemma Resolvable?

**Papers**: Green 2022, Wachter et al. 2021, Kasirzadeh 2022, Hampton 2021, Lopez 2024

**Content**:
- Formal vs. substantive fairness (Green): impossibility results stem from formalist methodology; substantive approaches may escape by expanding scope
- Automation limits (Wachter et al.): fairness cannot be automated because legal/moral conceptions exceed statistical formalization
- Structural injustice critique (Kasirzadeh): distributive justice frameworks (underpinning fairness metrics) cannot address oppressive structures
- Black feminist critique (Hampton): fairness discourse itself inadequate for addressing algorithmic oppression; points toward abolition
- Susceptibility to algorithmic disadvantage (Lopez): intersectional harms are "more than sum of parts"—emerge from interaction of vertical and horizontal dimensions

**Gap Connection**: Critical perspectives suggest the dilemma may be irresolvable within current fairness frameworks because formalization itself is limited. However, critics offer limited concrete alternatives beyond participatory approaches.

**Word Target**: 600-700 words

**Section Summary**: The interaction between statistical and ontological uncertainty creates a genuine dilemma: addressing one horn exacerbates the other. Epistemic justice concerns reveal this is not merely a technical optimization problem but involves structural injustice. Critical perspectives question whether fairness formalization can escape this dilemma.

**Section Word Target**: 1700-1900 words

---

## Section 6: Research Gaps and the Dilemma's Novelty

**Purpose**: Explicitly articulate what existing literature does NOT address—the interaction between statistical and ontological uncertainty as a dilemma—and position the research contribution.

**Gap 1: No Recognition of Statistical-Ontological Interaction as Dilemma**

**Evidence**:
- Technical ML literature (Domain 1) treats sparse data as engineering problem solvable through better methods (multicalibration, hierarchical models, adaptive testing)
- Philosophy literature (Domains 2-3) focuses on ontological analysis without engaging statistical feasibility constraints
- Even philosophical-technical bridges (Himmelreich et al. 2024, Gohar & Cheng 2023) identify both dimensions but do not theorize their interaction
- Kong (2022) comes closest by identifying "dilemma between infinite regress and fairness gerrymandering" but does not fully develop the statistical-ontological interaction

**Why it matters**: If the interaction constitutes a genuine dilemma (not merely two independent challenges), then existing approaches addressing either horn in isolation are systematically inadequate.

**How research addresses it**: Paper explicitly frames the interaction: expanding groups for ontological adequacy creates statistical unreliability; constraining groups for statistical reliability requires resolving contested ontological questions. This is a dilemma with intractable horns.

**Supporting literature**: Multicalibration assumes groups given (Domain 1); social ontology debates show groups contested (Domain 2); measurement theory reveals operationalization challenges (Domain 3); normative pluralism compounds uncertainty (Domain 4); epistemic justice shows both horns involve structural injustice (Domain 5).

**Word Target**: 500-600 words

**Gap 2: Limited Engagement with Statistical Feasibility in Social Ontology**

**Evidence**:
- Philosophy of intersectionality (Domain 2) focuses on conceptual analysis (emergence vs. reduction, analytical vs. hermeneutic interpretations) without considering algorithmic implementation constraints
- Social ontology debates (Domain 3) about attribute-based vs. practice-based group constitution rarely engage with computational contexts
- Measurement theory applications to fairness (Domain 4) focus on construct validity without addressing whether contested ontological foundations make valid operationalization impossible
- Few papers bridge philosophical ontology and statistical requirements for fairness auditing

**Why it matters**: Philosophical debates about group constitution have direct implications for whether algorithmic group specification is possible, yet these implications remain undertheorized.

**How research addresses it**: Paper connects practice-based social ontology (Haslanger, Mallon, Ásta, Ritchie) to impossibility of algorithmic derivation of groups, showing that ontological debates are not merely academic but constrain technical feasibility.

**Supporting literature**: Haslanger's political constructionism, Ásta's conferralism, Ritchie's structuralism all imply groups cannot be derived from attributes—yet ML fairness assumes attribute-based specification.

**Word Target**: 400-500 words

**Gap 3: Normative Foundations Left Implicit in Technical Fairness Work**

**Evidence**:
- Technical fairness literature (Domain 1) treats metric choice as technical decision
- Normative pluralism (Domain 4) shows different frameworks yield different group prioritizations, but this insight rarely informs technical work
- Measurement validity critiques (Domain 3) reveal that fairness metrics embody contested philosophical commitments, yet these remain implicit in most applications
- Little work on how normative disagreements about which groups matter affect fairness auditing scope

**Why it matters**: If which groups matter is partly normative question, then technical optimization alone cannot resolve group specification problem.

**How research addresses it**: Paper shows that ontological uncertainty is compounded by normative pluralism—different ethical frameworks (prioritarian, sufficientarian, egalitarian) generate different answers about which intersectional groups warrant auditing.

**Supporting literature**: Baumann et al. (metrics embody justice theories), Shields, Arneson, Parfit (distributive frameworks), Anderson (relational equality), Hertweck et al. (approximate justice), Holm (Broomean fairness).

**Word Target**: 400-500 words

**Gap 4: Critical Perspectives Without Constructive Alternatives**

**Evidence**:
- Domain 7 critical literature identifies fundamental limitations of fairness formalization (Green 2022, Wachter et al. 2021, Kasirzadeh 2022, Hampton 2021)
- Critics argue formalization obscures structural injustice, cannot be automated, or is conceptually inappropriate
- However, most critiques offer general calls for "substantive fairness," "participatory approaches," or "abolition" without specifying concrete alternatives to current auditing practices
- Limited guidance on how to conduct fairness assessment if formalization is inadequate

**Why it matters**: If formalization has inherent limits, we need principled understanding of what those limits are and what alternatives exist. Purely diagnostic critiques leave practitioners without guidance.

**How research addresses it**: By framing the intersectionality dilemma as arising from interaction of statistical and ontological constraints, paper provides principled analysis of formalization's limits. The dilemma helps explain why both technical optimization and critical rejection are inadequate responses—the problem is structural.

**Supporting literature**: Green's formal vs. substantive distinction, Wachter's automation impossibility thesis, Kasirzadeh's structural injustice critique, Hampton's Black feminist critique, Lopez's susceptibility framework.

**Word Target**: 400-500 words

**Section Summary**: Existing literature identifies components of the dilemma (sparse data challenges, ontological debates, measurement validity problems, normative disagreements, epistemic injustice) but does not recognize their interaction as constituting a genuine dilemma where addressing one horn exacerbates the other. This gap is both theoretical (misunderstanding the problem structure) and practical (leading to inadequate solution strategies).

**Section Word Target**: 1800-2100 words

---

## Conclusion

**Purpose**: Synthesize review findings and position the research contribution within the identified gaps.

**Content**:
- Summary of current state: ML has sophisticated technical solutions (multicalibration, sparse data methods) but assumes groups given; philosophy has rich debates about social ontology but rarely engages algorithmic constraints; measurement theory reveals validity problems; normative pluralism compounds uncertainty; epistemic justice shows structural dimensions
- **Key synthesis**: The intersectionality dilemma arises from interaction of statistical uncertainty (sparse data on small groups) and ontological uncertainty (contested group constitution). These interact as dilemma: expanding coverage for ontological adequacy creates statistical unreliability; constraining coverage for statistical reliability requires resolving irresolvable ontological questions.
- Existing work misses this interaction by treating statistical and ontological problems as independent optimization challenges
- Critical perspectives identify formalization limits but offer limited alternatives
- **Research contribution**: First explicit framing of statistical-ontological interaction as genuine dilemma; shows why both technical optimization and critical rejection are inadequate; provides principled account of fairness formalization's limits
- Implications: Fairness auditing may require accepting fundamental trade-offs rather than seeking optimal solutions; participatory approaches to group specification may be necessary but insufficient; need for institutional rather than purely algorithmic responses

**Word Target**: 400-500 words

---

## Notes for Synthesis Writer

**Papers by Section**:
- Introduction: 4-5 papers (Crenshaw 1989, Hébert-Johnson et al. 2018, Kong 2022, Haslanger 2012, plus 1-2 methodological)
- Section 1 (Technical): 18-20 papers (multicalibration 5-6, sparse data 6-7, gerrymandering 4-5, philosophical-technical 2-3)
- Section 2 (Ontology): 16-18 papers (intersectionality philosophy 6-7, social ontology 8-9, methodology 2-3)
- Section 3 (Measurement): 12-14 papers (construct validity 4-5, empirical evidence 4-5, distributive justice 3-4)
- Section 4 (Normative): 10-12 papers (distributive frameworks 6-7, applications 4-5)
- Section 5 (Epistemic Justice + Dilemma): 14-16 papers (epistemic injustice 5-6, interaction 4-5, critical perspectives 5-6)
- Section 6 (Gaps): 4-5 papers per gap (drawing from all domains to illustrate gaps)
- Conclusion: 3-4 synthesis papers plus key references from each section

**Total Papers**: 70-85 (comprehensive but selective; emphasizing High-importance papers)

**Total Word Target**: 4800-5400 words (targeting 5000 words)

**Citation Strategy**:
- Foundational: Crenshaw 1989, Fricker 2007, Haslanger 2012, Parfit 2012
- Recent ML: Hébert-Johnson et al. 2018, Gopalan et al. 2022, Ferrara et al. 2025, Lee et al. 2025
- Philosophy of intersectionality: Jorba & López de Sa 2024, Bernstein 2020, Carastathis 2016, Collins 2019
- Social ontology: Mallon 2016, Ásta 2018, Ritchie 2018, Epstein 2025
- Measurement: Tal 2023, Blodgett et al. 2021, Bean et al. 2025
- Normative: Shields 2016, Arneson 2000, Anderson 1999, Hertweck et al. 2024, Holm 2025
- Epistemic justice: Symons & Alvarado 2022, Anderson 2012
- Critical: Green 2022, Wachter et al. 2021, Kasirzadeh 2022, Kong 2022

**Tone**: Analytical and argumentative, building case that existing work misses the interaction. Emphasize the dilemma's novelty and theoretical significance. Critical but constructive—acknowledge sophistication of existing work while showing systematic gap.

**Key Analytical Moves**:
1. Show technical sophistication (Section 1) then reveal unaddressed ontological dimension
2. Establish ontological contestation (Section 2) then connect to algorithmic impossibility
3. Demonstrate measurement problems (Section 3) compound rather than resolve dilemma
4. Reveal normative pluralism (Section 4) makes ontological questions partly normative
5. Synthesize interaction (Section 5) as genuine dilemma with epistemic justice stakes
6. Explicitly map gaps (Section 6) showing what literature does NOT address
7. Position contribution (Conclusion) as filling identified gaps through dilemma framing

**Organizational Principle**: Build progressively from technical (what ML can do) → ontological (why group specification is contested) → measurement (why operationalization is problematic) → normative (why choices are value-laden) → epistemic (why interaction creates dilemma) → gaps (what's missing) → contribution (how paper fills gaps)
