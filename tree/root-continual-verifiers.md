# Root: Continual verifiers

Root node (depth 0) · 34 idea cards · **Ambitious but doable** · Ideas only; no experiments run

**Thesis.** A continual verifier should learn how to decide more cases without quietly changing what counts as correct. A verdict is conditional on a claim, observed evidence, a rule version, and a verification procedure. All four can change: a solver finds new ways to produce answers, observations lose or gain detail, an authority revises the rule, and a checker improves or regresses. If the system updates one scalar reward in response to all of them, better solving, better checking, and easier grading become indistinguishable. Build a frozen checking kernel, versioned statements and bindings, and a plastic layer that discovers evidence, transports certificates, or proposes checker revisions. Keep **proved relative to stated assumptions**, **empirically supported**, **refuted**, and **unknown** distinct; a failed proof search is not a refutation. Rule changes require independent authority, not solver success or judge consensus.

**Pramaana Labs.** Pramaana publicly describes a [compiler for verifiable decisions](https://pramaanalabs.ai/blog/we-raised-27m-to-build-a-compiler-for-mission-critical-ai). In its [IMO report](https://pramaanalabs.ai/blog/pramaana-solves-imo-2026-in-lean-4-in-under-7-hours), Panini formalizes natural-language statements, Hardy searches for proofs, and Lean 4 checks them. Its [everyday-provers report](https://pramaanalabs.ai/blog/towards-everyday-provers-for-real-world-verification) reports domain-dependent proof-search efficiency on statutory and software tasks. Take this division of labor as the starting architecture, not as a claim that the lab does or does not have a continual system. CV01–CV07 ask how the formal pipeline survives change; CV08–CV14 ask how the evidence survives change. A Lean proof certifies the formal statement under its assumptions, not faithfulness to the source, completeness of the observations, or the authority of a rule update.

**Scope and overlap.** Read against the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). [Learner–world co-evolution](https://github.com/manojbajaj95/cl/pull/372) already covers extracting or waking a skill via a checker; here the checker is what must learn and retain. [RL-on-OOD](https://github.com/manojbajaj95/cl/pull/51) already has verifier twins/mutants, and [fork invalidation](https://github.com/manojbajaj95/cl/pull/408) tracks which stored preferences a solver update could cross; neither cue inversion nor generic change-impact selection is a new card here. [Test-time learners](https://github.com/manojbajaj95/cl/pull/373) update a solver during inference; extra test-time search for a verdict alone is not a persistent verifier write. No likelihood-only retention alarms, self-judged replay loops, or exact save/restore as evidence of learning.

## Literature check

Checked targeted alphaXiv searches, arXiv titles/abstracts and Pramaana's public technical reports. These are nearest-mechanism comparisons, not exhaustive novelty claims. **P** means a candidate primitive (a reusable object or operation); **I** means an improvement or assay using an existing operation. A tie with the nearest matched control drops the primitive claim.

| Already available | What a continual verifier must add |
|---|---|
| [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) scores reasoning steps; [Rewarding Progress](https://arxiv.org/abs/2410.08146) measures progress under a separate prover policy. [GenRM](https://arxiv.org/abs/2408.15240) and [GenPRM](https://arxiv.org/abs/2504.00891) make verification generative, with test-time reasoning. | Separate logically valid steps from useful moves under a changing continuation policy; persist checkable evidence rather than a generated rationale. |
| [MT-Bench/Chatbot Arena](https://arxiv.org/abs/2306.05685) studies LLM judges and their biases; [RewardBench](https://arxiv.org/abs/2403.13787) evaluates reward models. [Verification Transport](https://arxiv.org/abs/2611.18471) tests stability when execution evidence is abstracted; [Adaptive Conformal Inference](https://arxiv.org/abs/2106.00170) adapts coverage under shift. | Retain the ability to recover evidence and measure selective error under actual solver and observation changes; agreement and marginal coverage are not per-slice correctness. |
| [Reward overoptimization](https://arxiv.org/abs/2210.10760), [Verifier Errors in RLVR](https://arxiv.org/abs/2609.35677) and [exact process-oracle audits](https://arxiv.org/abs/2611.21538) show why rising proxy scores are insufficient. [Budgeted strong-verifier audits](https://arxiv.org/abs/2610.35716) already target consequential reward errors. | Measure effects on future independently scored solver choices while protecting verification coverage and retaining unaffected rules. |
| [Co-Evolving Inspectable Graders](https://arxiv.org/abs/2610.11464), [VeriFine](https://arxiv.org/abs/2610.08761) and [EvoRS](https://arxiv.org/abs/2609.12459) already co-evolve detectors, judges, rubrics or reward DAGs with agents. | Benchmark these as direct controls. The novelty cannot be the feedback loop; it must lie in what each revision can carry forward, invalidate or learn from independently. |
| [RuleArena](https://arxiv.org/abs/2412.08972) benchmarks real-world rule reasoning; [AuXSpec](https://arxiv.org/abs/2611.21421) uses executable postconditions to supervise autoformalization. [ProofPatch](https://arxiv.org/abs/2611.01357) tracks review validity across Lean edits; [certified temporal specification revisions](https://arxiv.org/abs/2609.33461) already guard changing requirements. | Distinguish changed rules from bad translations and bind transported verdicts to authorized semantic scope and surviving evidence, not just recompilation. |

**First-test convention.** Use a CPU-enumerable world first: synthetic baggage tariffs, toy arithmetic proofs, or a simulator for packing and sorting. Keep an oracle outside the adaptation loop except for explicitly budgeted queries. Before each write, score live requests against that version's oracle; afterward score untouched old tasks A/B with current routing, including an unchanged rule and a close exception. When authorities actually change a rule, score both retention on unchanged scope and correct version-specific flips; do not reward agreement with superseded verdicts. Match labels, strong-check calls, bytes (including frozen versions and evidence), search/update compute, and answer coverage where applicable. Count false accepts, false rejects, abstentions, revision delay and independently scored solver success separately; record where oracle truth is unavailable. Use frozen checker, replay/refit, and full recheck controls wherever applicable; report full independent supervision separately as an upper bound. Every test below is proposed, not run.

## A · Learn what the rule means without moving the kernel

### CV01 · Verdict migration with a scoped change witness — Ambitious but doable (P)
- **Mechanism:** Make the output of a rule edit a three-way partition: carry old verdicts in a proved agreement region, replace verdicts in the authorized flip region, reopen the rest. Carry a witness that proves agreement without pinning the exact syntax or the proof that happened to run last time.
- **Nearest prior / gap:** [ProofPatch](https://arxiv.org/abs/2611.01357) tracks elaborated dependencies; [certified temporal revisions](https://arxiv.org/abs/2609.33461) constrain specification changes. The candidate object is reusable, instance-scoped verdict transport across an intentional change, not preserving an approved statement globally.
- **Cheapest first test:** Edit one exception to a synthetic baggage tariff, then refactor a shared definition. Compare dependency invalidation plus incremental Datalog ([2308.04214](https://arxiv.org/abs/2308.04214)) and rechecking all at equal total cost. Count independently confirmed flips, stale carries and rechecks under both edits.
- **Old-task retention:** Score old itineraries in two unaffected jurisdictions under live migrated state and replay a held-out historical itinerary against its original rule version.

### CV02 · Clarification that survives the next amendment — Ambitious but doable (P)
- **Mechanism:** Record an answer to a clarification as a discriminating input/output constraint between competing formalizations, with the clause and assumptions that keep the answer in scope. A new clause may revoke one constraint without erasing everything the reviewer taught.
- **Nearest prior / gap:** [Interactive specification elicitation](https://arxiv.org/abs/2610.22382) already asks clarifying questions. Test whether answer-to-constraint transport beats retrieving the same scoped questions as text across successive amendments.
- **Cheapest first test:** Enumerate four plausible readings of two tariff clauses; amend one and add an exception to the other. Compare stored Q&A plus clause retrieval, fresh elicitation, and scoped constraints at equal reviewer questions.
- **Old-task retention:** Re-test the unchanged reading and an old exception requiring two still-valid answers.

### CV03 · Proven discrepancy between rule releases — Ambitious but doable (P)
- **Mechanism:** An accepted update must return a concrete change witness for each declared behavioral change and prove no additional flips in the decidable test domain, or explicitly list the unresolved regions. This lets a reviewer sign differences rather than review two whole rulebooks.
- **Nearest prior / gap:** [Protected Cores Are Not Enough](https://arxiv.org/abs/2609.33461) certifies admissible changes; [SemantEq](https://arxiv.org/abs/2610.32919) studies equivalence of formal statements. The gap is a review interface for intentional non-equivalence, not a new solver for equivalence.
- **Cheapest first test:** Seed two intended changes and one accidental boundary change in a finite tariff release. Compare semantic-diff alone and delta witnesses mapped to declared intent at equal expert minutes; drop the claim if the plain diff gives the same speed and error.
- **Old-task retention:** Check unchanged ranges and a historical dispute at the outgoing version.

### CV04 · Authority-specific projection of a proof — Ambitious but doable (P)
- **Mechanism:** Represent a verdict by alternative sufficient assumption sets. When an authority retires a source, project the proof onto surviving sources rather than retaining a numerical vote or invalidating all cases touched by that source.
- **Nearest prior / gap:** [Semiring provenance](https://arxiv.org/abs/1712.01980) tracks alternative derivations and is the strongest symbolic control. The gap is projecting a mixed empirical/formal argument without letting a statistical premise masquerade as a theorem.
- **Cheapest first test:** Give two sources overlapping facts and a noisy observation model; retire one source. Compare symbolic provenance plus independent empirical recalibration against an explicit typed projection at equal memory. If the stacked baseline ties, keep it as the default.
- **Old-task retention:** Verify decisions with surviving support and abstentions on cases the retired source alone resolved.

### CV05 · Counterexample transplants for repaired translations — Ambitious but doable (P)
- **Mechanism:** Generalize a human-confirmed mismatch between text and logic into a parameterized boundary witness. Only transplant it to a new clause after showing the language-to-logic binding exposes the same boundary; keep the failed transplant as evidence of scope.
- **Nearest prior / gap:** [Deterministic specification diagnosis](https://arxiv.org/abs/2610.22568) repairs generated specifications. The proposal transfers a reviewer-confirmed semantic failure across different rule schemas, not a patch to the original formula.
- **Cheapest first test:** Move an inclusive-threshold mismatch from a weight clause to a piece-count clause alongside a distractor that intentionally excludes equality. Compare archived counterexamples in context and generic mutation testing at equal evidence and checks.
- **Old-task retention:** Keep both inclusive and intentionally exclusive legacy clauses correct after a second transplant.

### CV06 · Proof search learns; acceptance does not — Ambitious but doable (I)
- **Mechanism:** Continually train a search scheduler from proof and timeout histories, but let only the fixed checker and fixed statement determine acceptance. A timeout schedules a better tactic, not a negative label.
- **Nearest prior / gap:** [GenPRM](https://arxiv.org/abs/2504.00891) spends more inference on checking; [curriculum proof repair](https://arxiv.org/abs/2611.13627) learns from counterexamples. Improvement only: reuse search under a stream of changing domains, not new proof semantics.
- **Cheapest first test:** Stream three arithmetic proof families with disjoint tactic frequencies, then recur to the first. Compare static tactics, per-family cache and replay-trained scheduler on checked proofs per search node.
- **Old-task retention:** Compare proof yield and timeout rate on unseen old theorems at the same search budget, not just invariant soundness.

### CV07 · Exception graft with a rejection certificate — Ambitious but doable (P)
- **Mechanism:** Ask for a typed exception patch. The checker returns either an admissible patch with preserved obligations or a smallest conflicting set of already accepted obligations; the learner uses the latter as a constraint on its next proposal.
- **Nearest prior / gap:** [Certified temporal revisions](https://arxiv.org/abs/2609.33461) and [deterministic diagnosis](https://arxiv.org/abs/2610.22568) guard or repair specs. The candidate primitive is a persistent conflict certificate reusable on *other* patches, not failure feedback on one patch.
- **Cheapest first test:** Propose a sequence of overlapping discounts in a finite tariff language. Compare verifier-guided search with fresh unsat cores, replay of prior failures, and transported scoped cores; test future proposal count and wrong rejections.
- **Old-task retention:** Preserve valid old discount combinations and an unaffected exception.

## B · Learn what evidence a verdict needs

### CV08 · Transport with an evidence receipt — Ambitious but doable (P)
- **Mechanism:** A new trace interface returns an evidence receipt mapping each verdict premise to an observation or explicitly marking it missing. If the verdict cannot travel, the verifier requests a specific missing observable, not the whole trajectory.
- **Nearest prior / gap:** [Verification Transport](https://arxiv.org/abs/2611.18471) compares native, abstracted and restored views. The candidate operation learns which evidence to restore on unseen interfaces and accounts for the cost of restoration.
- **Cheapest first test:** Wrap a toy packing simulator's actions in two unseen macro tools that hide different observations. Compare full restoration, fixed field selection and a budget-matched evidence requester; score false accepts and bytes at equal coverage.
- **Old-task retention:** Grade old raw and old macro traces after learning the new receipt formats.

### CV09 · Negative verdict with a repair witness — Ambitious but doable (P)
- **Mechanism:** For a rejection, supply both a counterexample to the current claim and a checked minimal permitted change that would make it pass, if one exists. Learn reusable distinctions between recoverable and irrecoverable failures without learning from bare declines.
- **Nearest prior / gap:** [Deterministic diagnosis](https://arxiv.org/abs/2610.22568) repairs specifications; [Rewarding Progress](https://arxiv.org/abs/2410.08146) measures improved continuations. Here minimal repair is a checked property of the rejected artifact, not estimated success of a solver.
- **Cheapest first test:** Enumerate small packing plans with a bounded edit grammar; compare a counterexample-only verifier, edit-distance search and learned witness reuse on two shifts. Measure correct minimum edits per call and false repairs.
- **Old-task retention:** Recheck old minimally repairable failures and old infeasible cases after rule expansion.

### CV10 · Abstention compiled into the next observation — Ambitious but doable (P)
- **Mechanism:** When two possible worlds consistent with the evidence give opposite verdicts, return them with a feasible observation that separates them, if one exists. Accumulate reusable observation plans, not abstention thresholds.
- **Nearest prior / gap:** [Online cost-constrained verification](https://arxiv.org/abs/2610.02632) selects verification under budget; [interactive specification elicitation](https://arxiv.org/abs/2610.22382) resolves ambiguities in intent. This queries state evidence under a fixed intent, guided by an explicit disagreement witness.
- **Cheapest first test:** Hide either units or actual quantity in a toy shipping record and charge different read costs. Compare uncertainty-based escalation and learned entropy-greedy queries with witness-guided queries at equal cost.
- **Old-task retention:** Retain correct accept/refute behavior on complete A/B records and old missing-field cases.

### CV11 · Composable cost of hidden evidence — Ambitious but doable (P)
- **Mechanism:** A verifier for each subtask publishes sufficient evidence alternatives with acquisition costs. Compose them over a shared observation graph, paying once for a witness used by multiple subtasks and returning unknown when alternatives cannot be obtained.
- **Nearest prior / gap:** [Semiring provenance](https://arxiv.org/abs/1712.01980) already composes witnesses; [cost-constrained verification](https://arxiv.org/abs/2610.02632) budgets checks. Test whether learning transportable local evidence choices beats their direct combination, not whether shared costs can be counted.
- **Cheapest first test:** Learn policies for two packing subtasks, then add a composite task whose cheapest witnesses overlap only in combination. Compare exact provenance plus greedy acquisition, same-budget joint relearning, and composition.
- **Old-task retention:** Check both original subtasks for error and evidence cost after updating the composite planner.

### CV12 · Evidence downgrade rather than verdict overwrite — Ambitious but doable (P)
- **Mechanism:** Represent conclusions that depended on a now-weaker observation as guarded, conditional verdicts. A stronger evidence source can discharge the guard locally, so the rest of the chain does not need to be retrained or recertified.
- **Nearest prior / gap:** [Sound regression verification with partial contracts](https://arxiv.org/abs/2607.10291) is close for logical dependencies. The candidate operation also tracks which rules depended on empirical observations and refuses to convert downgraded confidence into proof.
- **Cheapest first test:** Replace exact counts with intervals in a finite stream. Compare full recertification, static partial contracts plus confidence routing, and conditional carries on intervals straddling the decision boundary.
- **Old-task retention:** Verify old exact-input cases and unchanged interval cases at matched answer coverage.

### CV13 · Coverage with named blind spots — Ambitious but doable (I)
- **Mechanism:** Report which predefined evidence strata lack enough adjudicated cases to support a release. Use a reserved random audit stream and a separate stream for chosen disagreements, so selective labels do not serve as the denominator for correctness.
- **Nearest prior / gap:** [Adaptive conformal inference](https://arxiv.org/abs/2106.00170) and [conformal weighting for LLM evaluation](https://arxiv.org/abs/2610.21214) handle calibration. Improvement only: audit explicitly missing evidence strata and avoid promising guarantees where the audit provides no support.
- **Cheapest first test:** Make a format shift hide one counterexample family. Compare marginal adaptive calibration and stratified audits at equal labels; report errors, abstentions and audit counts by stratum.
- **Old-task retention:** Re-measure old format strata at matched coverage rather than claiming retention by abstaining more.

### CV14 · A learned witness compressor with a mechanical readout — Ambitious but doable (P)
- **Mechanism:** Learn to replace a long witness with a set of facts and a checked derivation for exactly the queried premises. Preserve enough information to answer a declared family of future verifier changes, or expose the first unsupported query when that contract fails.
- **Nearest prior / gap:** [Verification Transport](https://arxiv.org/abs/2611.18471) measures information loss; [ProofPatch](https://arxiv.org/abs/2611.01357) records dependencies. The proposed object is a budgeted, forward-compatible evidence capsule, not a shorter explanation.
- **Cheapest first test:** Compress tiny simulator traces before sampling a held-out slice of possible rule edits. Compare selected raw events, static dependency slices and learned capsules at equal bytes; measure certified answer re-use and unsupported queries.
- **Old-task retention:** Retain a compositional old rule and a rare old exception after compressing under a second rule family.

## C · Learn from a moving solver without tracking its mistakes as truth

### CV15 · Factorial probes that identify what moved — Ambitious but doable (P)
- **Mechanism:** Maintain a small set of crossing interventions on claim producer, observation interface, checker and spec. For a changed verdict, replay the same latent execution with one factor changed at a time; where two factors interact, require a joint witness before choosing which component may learn.
- **Nearest prior / gap:** [Verification Transport](https://arxiv.org/abs/2611.18471) controls factors to isolate representation loss; [VeriFine](https://arxiv.org/abs/2610.08761) diagnoses failures to decide when to improve a judge. The gap is a learned probe set that can route writes under multiple potential causes, not the factorial experiment itself.
- **Cheapest first test:** Randomly inject a solver mistake, hidden observation, authorized rule edit or checker regression, then introduce pairs of shifts. Compare fixed factorial probes, static rules and disagreement-driven replay at equal independent labels. Penalize writing to the wrong component and require unknown in non-identifiable cases.
- **Old-task retention:** After each routed write, score untouched old rule, interface and solver slices separately.

### CV16 · Process labels with an expiration condition — Ambitious but doable (P)
- **Mechanism:** Store checked validity and predicted progress as separate fields on a step. The progress field additionally carries a continuation capability test; when a new solver can finish a branch that the old one could not, retire the progress label without retiring the proof of step validity.
- **Nearest prior / gap:** [Rewarding Progress](https://arxiv.org/abs/2410.08146) defines progress using a distinct prover. [Repo fork invalidation](https://github.com/manojbajaj95/cl/pull/408) reopens policy-dependent preferences; here a single stored step decomposes into a durable validity label and a replaceable progress label with different consumers.
- **Cheapest first test:** In a short arithmetic puzzle, add a legal continuation that bypasses the old shortcut. Compare separate validity/progress heads without guarded labels, full relabeling and selective refresh. If whole-label invalidation at equal cost ties, drop the primitive.
- **Old-task retention:** Check old invalid steps, valid detours and progress ordering on a solver family unaffected by the added continuation.

### CV17 · Train a judge on errors its own use would amplify — Ambitious but doable (I)
- **Mechanism:** Weight repair labels by their effect on candidate selection rather than by generic disagreement. Record random audits as well, so policy-induced exposure does not make blind spots disappear from the estimate.
- **Nearest prior / gap:** [Audit Where Hacks Pay](https://arxiv.org/abs/2610.35716) already directs strong verifier calls toward update consequences; [overoptimization-aware reward evaluation](https://arxiv.org/abs/2505.12763) studies utility beyond static ranking. Improvement: use the audit for judge repair and ask if it transfers to a later solver.
- **Cheapest first test:** Use candidate sets from two toy arithmetic solvers with different high-score mistakes. Compare error-frequency replay, uncertainty and budgeted impact audits, then assess accepted top candidates from a held-out solver.
- **Old-task retention:** Check both old error families and false rejects on old correct alternatives at matched acceptance coverage.

### CV18 · Patch exchange that carries a failure boundary — Ambitious but doable (P)
- **Mechanism:** Ship a judge patch with a checked success pair and an adjacent hold-out region it must not touch. A recipient tests the patch's claimed scope under its *own* solver distribution before using it for reward.
- **Nearest prior / gap:** [Inspectable graders](https://arxiv.org/abs/2610.11464) synthesize detectors with local gates; [Verification Transport](https://arxiv.org/abs/2611.18471) probes cross-view stability. New only if paired boundary witnesses reduce adaptation cost or unintended negatives over detector transfer plus revalidation.
- **Cheapest first test:** Transfer a fix for miscounted dimensions between two synthetic solver families with distinct trace layouts; include a benign near-neighbor each uses heavily. Compare raw detector transfer, same-example replay and witness-scoped transfer.
- **Old-task retention:** Score legitimate old traces on both sides of the new patch boundary under live routing.

### CV19 · Teach invariance from a proof, not from judge consensus — Ambitious but doable (P)
- **Mechanism:** Use proof-checked meaning-preserving transformations to bind multiple renderings of a claim to one verdict target; tag a transformation with the exact fields and premises it preserves. Reuse it to train only on nuisance changes known not to affect truth.
- **Nearest prior / gap:** [Invariant Risk Minimization](https://arxiv.org/abs/1907.02893) learns predictors across environments and [SemantEq](https://arxiv.org/abs/2610.32919) tests formal equivalence. This transfers equivalence certificates into the verifier's data generator instead of assuming augmentations preserve labels.
- **Cheapest first test:** Add unseen notations and unit aliases to a toy formalized tariff task. Compare ordinary augmentation, IRM and proof-bound augmentation at equal examples; include a similar-looking conversion that changes truth.
- **Old-task retention:** Check old notations plus cases where a superficially similar rewrite must change the verdict.

### CV20 · Keep uncertainty about the checker separate from uncertainty about the case — Ambitious but doable (P)
- **Mechanism:** Carry two actionable uncertainty fields: plausible intended worlds disagree, or candidate verification procedures disagree while evidence and intent are fixed. The first can buy an observation; the second can buy an independently adjudicated label. Do not train one kind of uncertainty away using the other's answers.
- **Nearest prior / gap:** [Online verification under cost constraints](https://arxiv.org/abs/2610.02632) addresses escalation; [VeriFine](https://arxiv.org/abs/2610.08761) queries humans on disputed cases. Test whether a typed query operation with separate update targets beats an equally expressive learned router, not whether two heads beat one threshold.
- **Cheapest first test:** Mix hidden quantities with cases where two learned checkers misparse complete inputs; separately price evidence reads and human labels. Compare risk–coverage under matched combined cost against a joint cost-sensitive router.
- **Old-task retention:** Verify old complete inputs and the proper escalation choice for old ambiguities after adding a parser failure mode.

### CV21 · Non-circular self-verification gate — Ambitious but doable (I)
- **Mechanism:** Blind a generative judge to the solver identity, remove rationales that merely announce success, and require the decisive observation or independently checked derivation for hard accepts. Let otherwise useful probabilistic judgments stay explicitly provisional.
- **Nearest prior / gap:** [MT-Bench](https://arxiv.org/abs/2306.05685) studies judge biases; [GenPRM](https://arxiv.org/abs/2504.00891) uses generative verification; [Inspectable graders](https://arxiv.org/abs/2610.11464) expose vacuous consensus. This is an independence control, not a novel source of truth.
- **Cheapest first test:** Cross two arithmetic generator families with judge versions before and after a small adaptation; compare ordinary anonymization, witness gating alone and both at matched coverage on an independently scored holdout.
- **Old-task retention:** Preserve valid alternative proofs and old incorrect answers that happen to have fluent explanations.

## D · Keep reward revisions accountable for what they teach

### CV22 · A verifier patch with a downstream teaching receipt — Ambitious but doable (P)
- **Mechanism:** An accepted reward patch carries paired, same-start learner updates using the pre- and post-patch reward, and an independent score of the ensuing decisions. Release for RL only into regimes where the patch improves independently checked behavior; it may still ship as a more accurate evaluator elsewhere.
- **Nearest prior / gap:** [Inspectable graders](https://arxiv.org/abs/2610.11464) distinguish teacher usefulness from grader accuracy; [overoptimization-aware evaluation](https://arxiv.org/abs/2505.12763) scores utility. The candidate object is a locally reusable, independently verifiable teaching-effect receipt attached to a patch, not another global judge score.
- **Cheapest first test:** Use a contextual bandit whose two solver initializations react differently to a locally corrected reward. Compare global accuracy gating, fresh one-step utility gating and receipt reuse on a third solver version. Reject the claim if reuse offers no decisions-per-independent-label gain.
- **Old-task retention:** Score verifier accuracy and old policy performance independently after two rewarded learning blocks.

### CV23 · Attribute skill loss to the reward version that taught it — Ambitious but doable (P)
- **Mechanism:** Log which verification premise was decisive in each rewarded choice. On discovering a false premise, test the smallest set of learning batches likely affected using matched replays; do not assume a logged dependency proves a causal training effect.
- **Nearest prior / gap:** [TracIn](https://arxiv.org/abs/2002.08484) and [Datamodels](https://arxiv.org/abs/2202.00622) estimate effects of training examples; the proposal attributes a versioned *reward premise* across many value labels and compares a replay from clean state.
- **Cheapest first test:** Train tiny linear policies in a packing bandit with one erroneous rule branch shared by many contexts. Compare sample attribution, whole-version rollback and premise-based batch selection; score repair compute against clean replay.
- **Old-task retention:** Check old decisions learned from unaffected premises and those sharing examples with the revoked premise.

### CV24 · Reward credits that mature after independent review — Ambitious but doable (I)
- **Mechanism:** Store a bounded log of decisions whose rewards were provisional. When delayed evidence arrives, use paired independent rescoring to release or replace the eligible update rather than treating either all early rewards as final or all as missing.
- **Nearest prior / gap:** [Selective verifier control](https://arxiv.org/abs/2609.35677) studies how to limit optimization against bad rewards; [Doubly Robust OPE](https://arxiv.org/abs/1511.03722) estimates value off-policy. This is delayed feedback with explicit claim scope, not a new learning operation or a guarantee of unbiased correction.
- **Cheapest first test:** Simulate delayed strong feedback for two rule families in a contextual bandit. Compare waiting, immediate updates plus ordinary correction and a capped provisional grant; compare independently scored regret at matched storage and latency.
- **Old-task retention:** Measure unaffected old policy and grader slices after mixed confirmations and reversals.

### CV25 · Preserve uncontested rankings during reward repair — Ambitious but doable (I)
- **Mechanism:** Patch a reward head against newly adjudicated errors while constraining it on old independently supported score differences, not raw logit magnitudes. Allow true ranking reversals where the official specification changed.
- **Nearest prior / gap:** [Weight interval constraints for CL](https://arxiv.org/abs/2206.07996) protect previous tasks and [EvoRS](https://arxiv.org/abs/2609.12459) revises scoring mechanisms. Improvement: apply backward compatibility to verified pairwise reward order rather than the full frozen teacher.
- **Cheapest first test:** Shift answer formats and change one arithmetic tolerance rule; compare rank-distillation on replay, margin-constrained repair and recalibration at equal labels and update size.
- **Old-task retention:** Keep old certified preferences and bandit decisions while explicitly checking intended reversals separately.

### CV26 · Counterfactual reward explanation across versions — Ambitious but doable (P)
- **Mechanism:** For a reward that changed, produce a matched pair of cases distinguishing a lawful rule flip, a changed observation, and a ranking artifact from score mixing. Use this pair to direct separate corrections in the reward computation and the RL data it generated.
- **Nearest prior / gap:** [EvoRS](https://arxiv.org/abs/2609.12459) patches an executable reward DAG from traces; [Optimistic Verifiers Get Hacked](https://arxiv.org/abs/2611.21538) analyzes proxy failure modes against a process oracle. The candidate operation is cross-version paired evidence with a distinct correction path for each cause.
- **Cheapest first test:** Create identical changes in aggregate reward by shifting individual factors in a toy pack-and-sort stream. Compare reward-DAG debugging from logs, CV15-style diagnosis alone and paired explanations that also migrate implicated training targets.
- **Old-task retention:** Keep old reward ordering and independently scored old solver behavior after an unrelated composition repair.

### CV27 · Negative evidence that survives aggregation into reward — Ambitious but doable (P)
- **Mechanism:** Allow an independently checked counterexample to attach a named, non-compensable veto to a candidate, separate from soft rewards. A later authority-approved revision can discharge it only by invalidating the tagged premise or replacing the evidence.
- **Nearest prior / gap:** [Inspectable graders](https://arxiv.org/abs/2610.11464) compose drawback detectors; [EvoRS](https://arxiv.org/abs/2609.12459) evolves reward DAGs. A fixed veto is not novel; the claim is the reusable, dischargeable counterexample across aggregator replacements.
- **Cheapest first test:** Mix reward-head replacement and a legitimate exception change in finite packing problems. Compare a static hard veto, freshly recomputed veto and carried witnesses against reward-based candidate selection.
- **Old-task retention:** Retain old upheld vetoes and old accepted near-neighbors, and lift only those vetoes affected by the authorized change.

### CV28 · Audit the policy you made, not just the data you saw — Ambitious but doable (I)
- **Mechanism:** Maintain randomized shadow slices and frozen audit generators distinct from adaptation data. Measure how use of a checker changes the distribution presented to its next version, before treating fewer discovered errors as progress.
- **Nearest prior / gap:** [Performative Prediction](https://arxiv.org/abs/2002.06673) formalizes predictor-induced shift; [reward overoptimization](https://arxiv.org/abs/2210.10760) compares proxy and independent reward. Improvement only: make the input-distribution change measurable during continual verifier updates.
- **Cheapest first test:** Alternate two cheap bandit checkers that select different borderline cases, logging uniform exposure and independent outcomes. Compare naive on-policy error, importance-weighted audit and a frozen-generator panel.
- **Old-task retention:** Score the same old task mixture before and after revision, alongside the new endogenous mixture; report slices without overlap as unknown.

## E · Compose and deploy verifiers without compounding unearned trust

### CV29 · Independence receipts for verdict ensembles — Ambitious but doable (P)
- **Mechanism:** Attach premise and evidence-lineage tags to several verdicts. The aggregate counts agreement on one shared observation as one evidence source, while keeping different derivations or independently observed premises separate.
- **Nearest prior / gap:** [Reward-model ensembles](https://arxiv.org/abs/2310.02743) mitigate overoptimization; [semiring provenance](https://arxiv.org/abs/1712.01980) tracks alternate derivations. The claim is improved aggregation under correlated changing evidence, not that declaring provenance establishes conditional independence.
- **Cheapest first test:** Use three toy judges with overlapping deterministic inputs and correlated noisy counts, then swap one input source. Compare ordinary ensembles, oracle-grouped averaging, and lineage-aware aggregation at equal calls.
- **Old-task retention:** Preserve old genuinely independent corroboration and do not increase false acceptance when old sources become shared.

### CV30 · Revalidate a subverifier by asking its callers what they need — Ambitious but doable (P)
- **Mechanism:** Downstream verifier modules publish the exact observation abstractions and error directions they rely on. An upstream replacement migrates only after meeting these obligations or returning a counterexample caller can use to adapt.
- **Nearest prior / gap:** [Partial contracts](https://arxiv.org/abs/2607.10291) support regression verification; [Verification Transport](https://arxiv.org/abs/2611.18471) measures abstraction failures. The candidate is learning from caller-specific failed substitution rather than demanding identical outputs.
- **Cheapest first test:** Swap a small interval estimator used by a threshold judge and an ordering judge that need different guarantees. Compare full output matching, fixed interface contracts plus replay, and learned caller obligations on a later replacement.
- **Old-task retention:** Retain both old downstream uses and verify an untouched caller relying on exact boundary behavior.

### CV31 · Reservoir of future-sensitive witnesses — Ambitious but doable (P)
- **Mechanism:** Retain witnesses chosen for the diversity of verdicts they could discriminate under a declared family of future rule or sensor edits, not for how much current score they preserve. Record which possible amendments are unsupported at the current storage budget.
- **Nearest prior / gap:** [ProofPatch](https://arxiv.org/abs/2611.01357) revalidates reviews after edits; [Verification Transport](https://arxiv.org/abs/2611.18471) isolates lost evidence. The operational claim is a coreset valuable for *future re-adjudication* after raw evidence is gone, not ordinary replay retention.
- **Cheapest first test:** Retain an equal-byte subset of finite traces, then draw held-out rule edits after freezing the reservoir. Compare random, rarity/margin and dependency-coverage coresets; score recoverable adjudications and false confidence on uncovered amendments.
- **Old-task retention:** Recheck unchanged A/B rule families and rare exceptions under the same storage cap.

### CV32 · Independent audit budget that survives repeated release attempts — Ambitious but doable (I)
- **Mechanism:** Keep release audit items and outcomes out of adaptation; only disclose a pooled gate result with a limit on repeated looks. Use a fresh oracle sample or stop once that gate can no longer support a decision.
- **Nearest prior / gap:** [Adaptive holdout reuse](https://arxiv.org/abs/1506.02629) already targets adaptive reuse. This applies that guard to repeated verifier release attempts rather than claiming self-certification from frozen examples.
- **Cheapest first test:** Simulate successive candidate checker patches tuned after each gate decision. Compare a visible frozen set, reserved fresh samples and a reusable holdout at equal adjudications; score false promotions on unseen examples.
- **Old-task retention:** Reserve old A/B audit strata and report whether repeated gates increase their true false-accept rate.

### CV33 · Cross-version verifier gym with hidden change factors — Ambitious but doable (I)
- **Mechanism:** Generate independently randomized changes to solver, checker, observation and authorized rule, including pairs whose aggregate reward effect is identical. Separately score update routing, correct abstention, adaptation and retention.
- **Nearest prior / gap:** [RuleArena](https://arxiv.org/abs/2412.08972), [RewardBench](https://arxiv.org/abs/2403.13787), [AgentProcessBench](https://arxiv.org/abs/2603.14465) and [Verification Transport](https://arxiv.org/abs/2611.18471) cover complementary probes. This is an assay, not a new learning primitive.
- **Cheapest first test:** Exhaustively generate 2×2×2×2 release tuples in toy baggage rules; check that frozen, replay/refit and co-evolving judges fail on measurably different hidden factors at equal oracle calls. Do not count detecting a built-in change flag.
- **Old-task retention:** Hold out two invariant tasks and historical-version queries; a system that learns C by rewriting A/B fails the assay.

### CV34 · Rebuild a verifier from signed obligations, not from old weights — Ambitious but doable (P)
- **Mechanism:** Swap the judge family and reconstruct only from accepted semantic constraints, scoped witness/repair pairs and unchanged authority rules. The old judge may be compared afterward but cannot write its own targets for the successor.
- **Nearest prior / gap:** [AuXSpec](https://arxiv.org/abs/2611.21421) learns from executable postconditions and [ProofPatch](https://arxiv.org/abs/2611.01357) binds review state to formal statements. The proposed portable state is a budgeted replay substitute for a *verifier*, not proof that an identical checkpoint restores behavior.
- **Cheapest first test:** Replace a small linear trace judge with a shallow tree, then add a new layout. Compare obligations to replay, ordinary distillation and matched retrieval of rules plus fixtures; score labels-to-recovery after two swaps and recovery after adding the layout.
- **Old-task retention:** Recheck untouched old decisions based on disjoint evidence families plus an old exception with no direct stored example.

## Ranked deeper questions

1. **What should survive a real rule amendment: the verdict, the proof, or only the evidence? (CV01, CV03, CV04, CV12)** Start with two held-out amendments and a harmless refactor. Compare ProofPatch-style dependency invalidation plus incremental evaluation and full recheck. A useful transport operation must lower rechecks without stale accepts, preserve unaffected A/B, and still flip precisely where authority changed the rule. If only syntax changes benefit, this is incremental verification, not a continual primitive.
2. **Can a verifier learn to buy exactly the missing evidence on a new interface? (CV08, CV10, CV14, CV31)** Freeze an evidence budget, then draw unseen macro wrappers and rule amendments. Compare full restoration as an upper bound, provenance slicing plus active querying, and equal-byte replay. If the learned receipts and compressed witnesses do not reduce cost at matched error and coverage on both new and old interfaces, keep the simpler contract.
3. **Can the verifier identify which component is licensed to learn from a failure? (CV15, CV16, CV20, CV33)** Hide crossing shifts and include observationally identical cases. Benchmark VeriFine-style human queries, EvoRS and anchored inspectable graders with the same oracle budget. Require fewer harmful writes, unchanged-slice retention and explicit abstention when no available probe separates causes.
4. **Which checker improvements actually teach a stronger next solver? (CV17, CV22, CV23, CV28)** Freeze a held-out solver family, then compare repair by grader accuracy, impact audits and patch teaching receipts. Equalize independent checks and policy update steps; score successor correctness and old skills separately from grader agreement. If the receipt does not transfer beyond the solver that generated it, it belongs in release evaluation rather than persistent state.
5. **What verifier state is portable after the judge family changes? (CV02, CV19, CV30, CV34)** Replace two verifier backbones in succession, then introduce a held-out exception. Compare constraints/witnesses against equal-byte replay, distillation and rules-plus-fixtures retrieval. A transferable state should recover old decisions and require fewer *new independent judgments*, not merely preserve old judge biases.
