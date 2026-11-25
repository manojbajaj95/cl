# Root: Abliteration-style learners

Root node (depth 0) · 34 candidate cards (AL01–AL34) · 5 ranked deeper questions · Ideas only; no experiments run

**Request (Manoj).** "Check ideas towards, how we generate abliterated models, can we use similar techniques to build a better model, teach them on the fly on the tasks".

**Thesis.** Yes, if some task errors are caused by an existing shortcut crowding out a capability the model already has. Abliteration supplies the analogy: identify a direction from contrastive activations and test whether intervening on it changes behavior. A learner could do that on a task stream, using verified corrections to decide what to suppress, what to teach instead, and when to decline a write. The harder bet is that the learner can maintain and revise those edits as evidence changes, not just pick a better steering vector once. Keep the research on benign task skills and preserve the base model's safety behavior; refusal suppression is prior art, not an objective.

## Is this pursuable? Short answer

Yes as a reversible, few-shot update rule; no as a claim that subtracting directions makes arbitrary new skills appear.
- **Start with three distinct operators.** Let `x` be a column input to a linear map `W`; let `u` be a unit direction in its output space. ActAdd-style addition injects a constant at a site. A shortcut write subtracts a state-dependent term: `W′ = (I − λuuᵀ)W`, which changes that map's contribution only. A teaching write `ΔW = baᵀ` produces an output direction `b` only to the extent its input matches `a`. Do not equate editing one map with projecting the whole residual stream.
- **Separate discovery from teaching.** Contrasts from identical inputs and aligned token positions can nominate directions; interventions on unseen items must establish utility. If suppression only recovers a known routine, call it recovery. To claim acquisition, require transfer on a newly assigned rule, with the teaching examples removed, against explicit lookup and in-context learning.
- **The useful work begins after the first write.** If the edit survives changing evidence, protects earlier tasks, or stores a distinction a plain adapter cannot recover at the same budget, it earns a research line. Otherwise this is a cheap steering baseline.

**Scope.** Read before writing: the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). The ledger's [edit-capacity result](https://github.com/manojbajaj95/cl/pull/22) weakens global capacity forecasts; its [functional-syndrome result](https://github.com/manojbajaj95/cl/pull/24) cautions against assuming damage is sparse. Don't revive proposal-killed WSP repair (Agent 8, [PR #7](https://github.com/manojbajaj95/cl/pull/7)) or claim cheap placement is a primitive (MX1, [PR #36](https://github.com/manojbajaj95/cl/pull/36)). [Test-time learners](https://github.com/manojbajaj95/cl/pull/373) already covers persistent fast weights, closed-form ICL writes and push/pop; its [first child](https://github.com/manojbajaj95/cl/pull/374) covers context handoff and tacit residuals. [Handwritten LoRA](https://github.com/manojbajaj95/cl/pull/400) already proposes annotated components, recompilation, and rank-1 spillover repair; here evidence, not an LLM writer, determines the contrast and the task stream tests its lifetime. Flood P21/P17 already sketch residual instructions and linkers; a collection of signed rank-1 writes is not a new instruction set or linker.

**Shared conventions.** First tests below are proposals only. Use toy streams or one small frozen model (e.g. Qwen2.5-0.5B) with a clean reset per stream. Predict before revealing verified feedback; enforce a support/calibration/test split by task instance and, where relevant, template. Use matched forward passes, examples and sweeps for random/permuted directions, raw contrast steering, rank-1 LoRA and ICL or lookup where applicable; separate the serving-cost comparison from the equal-feedback comparison. Compare prequential gain, correction lag and worst old-task loss; charge persistent state (including replay and routing state), peak state, and write/read latency. Retention always includes untouched base tasks and a fixed policy-behavior sentinel set with the edit active; the card names the additional relevant old-task slice. Compare matched confidence or entropy when an edit could just sharpen or flatten answers. No adaptation on the retention or final test split.

## Literature check

Positioning against named work and the repo's reviews, not an exhaustive priority search. “Gap” describes what the proposed test must distinguish, not a claim of first publication.

| Line | Already available | What a card here must add |
|---|---|---|
| Abliteration / representation engineering | [Arditi et al.](https://arxiv.org/abs/2406.11717) localize and intervene on refusal-related directions; [Zou et al.](https://arxiv.org/abs/2310.01405) frame reading and controlling representations | Learn task-specific contrasts from verified feedback and test selective, revisable effects while retaining other uses of the model |
| Additive / gated activation steering | [ActAdd](https://arxiv.org/abs/2308.10248), [Contrastive Activation Addition](https://arxiv.org/abs/2312.06681) | Evidence that a subtractive, conditional or persistent write has value beyond a matched steering baseline |
| Representation fine-tuning | [ReFT](https://arxiv.org/abs/2404.03592) learns interventions in activation space | Few-shot closed-form operations must win somewhere on latency, selective revision or retention, not merely use the same intervention family |
| Model editing | [ROME](https://arxiv.org/abs/2202.05262), [MEMIT](https://arxiv.org/abs/2210.07229), [AlphaEdit](https://arxiv.org/abs/2410.02355) edit weights, with AlphaEdit pursuing retention through null-space projection | Evidence about future task revisions, or a new operation on contrasts, beyond preserving a fixed key set |
| Task vectors / weights as programs | [Task Arithmetic](https://arxiv.org/abs/2212.04089), [TIES](https://arxiv.org/abs/2306.01708), [WSP writes ICL](https://arxiv.org/abs/2611.26841), [PR #400](https://github.com/manojbajaj95/cl/pull/400) | Distinguish changing the learner's estimate of what to remove or preserve from composing trained or handwritten deltas |

## A · Isolate something worth writing

### AL01 · Online difference-of-means teacher
- **Improvement** (CCA-style steering updated from corrections; a baseline for the root).
- **Mechanism:** On a verifier failure, collect pooled activations at equivalent decision boundaries from a verified retry and a failed trajectory; update two running means, then use their difference as a transient steering vector on the next item.
- **Nearest prior / gap:** CAA, ActAdd and [ICV](https://arxiv.org/abs/2311.06668); persistence and recency are not new operations.
- **Cheapest first test:** Swap the output convention midway through a small table-transformation stream. **Kill** if the rolling contrast does not beat a frozen contrast and recency-matched ICL on post-switch prediction at comparable old-task loss.
- **Old-task retention:** Original transformations under their explicit convention and previously learned unrelated transforms.
- **Risk / likely tie:** Retry language may supply the entire contrast; match token position and length and include useless but equally fluent retries.

### AL02 · Counterbalanced shortcut square
- **Primitive** (write evidence is a crossed contrast, not a good/bad label pair).
- **Mechanism:** Make four support cells crossing a real selector with a spurious cue, with answer identities balanced. Estimate the nuisance main effect and its interaction with the selector separately; subtract only the part shown by held-out intervention to cause shortcut errors off the correlation.
- **Nearest prior / gap:** Contrastive representation engineering and [PR #140](https://github.com/manojbajaj95/cl/pull/140)'s crossed evidence; test the crossed contrast as the actual write operand rather than as training data.
- **Cheapest first test:** Table interpretation where color predicts the correct column in one support partition. **Kill** if ordinary CAA on the same four cells or equal-budget ReFT matches off-correlation accuracy at equal loss on true color queries.
- **Old-task retention:** Color-selection requests where color really is the rule.
- **Risk / likely tie:** Better sampling alone may account for any win; give all writers the same cells.

### AL03 · Causal contrast swap
- **Improvement** (a direction screen, not a new learner).
- **Mechanism:** In a failed trace swap in only the candidate scalar from its verified twin at the last shared decision point; make the reverse swap in the twin. Nominate only directions whose swaps move the decision in opposite predicted directions.
- **Nearest prior / gap:** Activation patching and interchange interventions; use bidirectional effects to select a low-rank write, not to claim a discovered circuit.
- **Cheapest first test:** Two arithmetic shortcuts with precomputed correct traces. **Kill** if bidirectional selection predicts no more held-out edit gain than mean separation or same-budget black-box layer selection.
- **Old-task retention:** Correct traces that use the same intermediate quantity legitimately.
- **Risk / likely tie:** Off-manifold swaps and maximum-over-sites bias; test sites chosen without held-out labels.

### AL04 · One example with two witnesses
- **Primitive** (an edit operand with independent evidence for its efficacy and its protected reuse).
- **Mechanism:** Demand a matched retry and a separately selected counterexample on which the candidate direction ought to remain useful. Use the retry to nominate the vector, then use both witnesses to select between suppression, conditioned suppression or abstention.
- **Nearest prior / gap:** HL06 has declared tests; the proposed second witness is queried from the stream and chooses which operation is legal before fitting.
- **Cheapest first test:** Teach a format exception whose cue also appears in a normal request. **Kill** if a held-out gate after ordinary CAA or ReFT on the same two examples makes equally selective decisions.
- **Old-task retention:** Unseen examples of the protected use, not just the witness.
- **Risk / likely tie:** A strong scope classifier may solve the whole problem without writing a direction.

### AL05 · Rule discovery via subtraction–addition factorial
- **Improvement** (assay separating recovery from teaching).
- **Mechanism:** Include no edit, subtraction only, addition only and both. Pair a familiar task blocked by a misleading cue with a new arbitrary rule using the same inputs. Measure whether addition learns the new rule and whether subtraction is necessary for it to stick.
- **Nearest prior / gap:** Task-vector arithmetic and Arditi et al.'s necessity/sufficiency logic; distinguishes operations on a newly assigned rule from recovery.
- **Cheapest first test:** Reassign two random symbol-to-operation mappings after an episode boundary. **Kill** the joint mechanism if the new rule does not generalize off examples or if the strongest stacked additive and subtractive controls match it.
- **Old-task retention:** Familiar rules with and without the misleading cue.
- **Risk / likely tie:** An explicit keyed table may dominate; include it and give it the same observed mappings.

### AL06 · Reward-twin eligibility
- **Improvement** (lower-variance contrast on delayed feedback).
- **Mechanism:** From one benign task state, sample two short continuations. A verifier score difference weights their contrast at the shared decision point. Do not update when both continuations get the same score.
- **Nearest prior / gap:** Pairwise preference learning, branched rollouts in flood [PR #51](https://github.com/manojbajaj95/cl/pull/51); the rank-1 editor changes the update budget, not credit assignment's basic object.
- **Cheapest first test:** Simulator for sorting with a two-step delayed score. **Kill** if branch-weighted steering ties matched-return CAA or small preference-trained LoRA at the same rollout budget.
- **Old-task retention:** Earlier sort keys and immediate-feedback sorting.
- **Risk / likely tie:** A contrast in private reasoning length may encode only confidence; compare length- and entropy-matched twins.

## B · Write negative evidence, not just a positive adapter

### AL07 · The shortcut write
- **Improvement** (rank-1 orthogonalization itself is established abliteration).
- **Mechanism:** Apply a bounded subtractive write to one map's output contribution, using a direction nominated by task failures. Sweep the dose on support only; compare with the same direction injected additively and with exact activation projection at the same site.
- **Nearest prior / gap:** Arditi et al. already demonstrate orthogonalization; the gap is whether this is a useful, retention-preserving online task update.
- **Cheapest first test:** Teach a small model to stop treating a distractor column as an answer key. **Kill** if the edit never produces a better prequential gain/retention point than additive steering or rank-1 ReFT.
- **Old-task retention:** Read the distractor column when explicitly requested, plus other table schemas.
- **Risk / likely tie:** Subtraction and activation projection at the same linear contribution are equivalent by construction, not independent evidence.

### AL08 · Write the exclusion in evidence space
- **Primitive** (negative evidence removes attribution to one factor without discarding a shared activation coordinate).
- **Mechanism:** Fit two readouts for a correlated cue and a real selector from crossed examples. Subtract the cue-conditioned prediction of the shared component at fixed selector, rather than projecting its entire direction out. Keep the selector-conditioned contribution.
- **Nearest prior / gap:** Linear concept erasure (including [LEACE](https://arxiv.org/abs/2306.03819)) and conditional steering; the conjecture is useful selective erasure when wanted and unwanted uses occupy the same coordinate.
- **Cheapest first test:** CPU shared-coordinate toy, then the color task in AL02 with held-out cue/selector combinations. **Kill** if conditional LEACE, route-then-project or a rank-matched ReFT gives the same Pareto frontier.
- **Old-task retention:** Correct selector-driven decisions at all cue values, including old combinations not used to fit.
- **Risk / likely tie:** If the selector must be known perfectly by an external router, call it routed erasure rather than a learned primitive.

### AL09 · Inhibition with a rescue write
- **Primitive** (a subtractive edit has a measured, separately addressable legitimate-use rescue).
- **Mechanism:** When removing a shortcut hurts a distinct old task, measure the missing component on old-task witnesses and return it only where a separately validated predicate fires. Update the rescue alone when the legitimate-use boundary moves.
- **Nearest prior / gap:** HL15+HL17 cancel adapter spillover; here the rescue is a reversible reinstatement of a removed signal and its read conditions can be revised independently.
- **Cheapest first test:** Two old units rules sharing one cue, then change which inputs qualify for one rule. **Kill** if a single routed projection or AlphaEdit plus replay matches revision cost and retention at the same budget.
- **Old-task retention:** Old applications of both rules plus previously corrected shortcut errors.
- **Risk / likely tie:** If the rescue just negates an inhibit gate, it is equivalent to changing that gate.

### AL10 · One write must earn two signs
- **Primitive** (a single direction is treated as a signed transfer map with counterfactual obligations in both directions).
- **Mechanism:** Derive a candidate direction on one environment, then verify a negative dose helps when the cue is misleading and a positive dose helps in a matched environment where it is diagnostic. Reuse the direction on changes in cue validity; re-estimate only the signed dose.
- **Nearest prior / gap:** Task Arithmetic and signed activation steering already allow sign flips; the proposed reuse is a two-sided evidence requirement, not the algebra.
- **Cheapest first test:** Change the reliability of a formatting cue twice in toy extraction. **Kill** if independently fit vectors or a fixed direction with feedback-tuned dose adapts just as quickly and selectively.
- **Old-task retention:** Both previously observed cue-validity regimes, plus uncued items.
- **Risk / likely tie:** Opposite signs may merely implement log-odds weighting of a single input cue.

### AL11 · Subtract a dependency edge, not a feature
- **Primitive** (source-to-sink coupling is the writable object).
- **Mechanism:** Identify a nuisance source by patching and a sink that causes the wrong action. Use a source-keyed rank-1 counter-write immediately at the sink, leaving the nuisance source available to other sinks.
- **Nearest prior / gap:** Edge patching / attribution, ROME's keyed writes and HL24 localization; the test is whether a measured edge can be inhibited while the same source and same sink still do other useful jobs.
- **Cheapest first test:** Two decisions in a small transformer reuse a feature, only one wrongly. **Kill** if whole-feature projection or equally local ReFT reaches the same joint accuracy under held-out cue combinations.
- **Old-task retention:** Other uses of the source and other inputs to the edited sink.
- **Risk / likely tie:** Attribution may be diffuse (ledger PR #24); stop if no stable source–sink pair survives split-half checks.

### AL12 · Fractional inhibition with a known inverse
- **Improvement** (use exact linear invertibility as a control, not an achievement).
- **Mechanism:** Use a fractional single-site projection with `0 < λ < 1` and log its dose. At a later point test whether inverse restoration on the affected map is enough or later writes must be retaught. A full projection is singular and cannot be undone by applying an inverse.
- **Nearest prior / gap:** TT02 push/pop and counterfactual rollback; the question is the cost of repairing descendants after local undo, not whether matrix inversion works.
- **Cheapest first test:** Three writes, withdraw the earliest, compare inverse-at-site with restoring the base and replaying remaining evidence in order. **Kill** if selective local repair offers no revision-cost advantage at matched behavior.
- **Old-task retention:** Later learned edits and tasks that relied on the original suppressed component.
- **Risk / likely tie:** Near-full inhibition makes the inverse ill-conditioned; inverse weights do not undo intervening nonlinear behavior.

## C · Learn directions that endure changing evidence

### AL13 · Retract the evidence, then reevaluate the write
- **Primitive** (an activation edit with an evidence-level retraction).
- **Mechanism:** Store signed, count-weighted activation contributions in a fixed base coordinate frame. When a verifier reverses a decision, remove that witness from the sufficient statistics, recompute the contrast and validate the remaining evidence; do not subtract the witness's old parameter delta.
- **Nearest prior / gap:** HL07 bisects components; TT02 pops edits; incremental statistics and unlearning from sufficient statistics are known. Here retraction can rotate a *shared* task edit without reverting other supported witnesses.
- **Cheapest first test:** Stream mislabeled teaching pairs, revoke one after learning a second rule. **Kill** if adapter replay or explicit premise invalidation reaches the same correction lag with no greater memory and latency.
- **Old-task retention:** Keep held-out predictions supported by non-revoked witnesses and other learned rules.
- **Risk / likely tie:** Fixed-base statistics may miss directions that exist only after adaptation; the distinction from rebuilding a tiny adapter may be economically negligible.

### AL14 · Keep a contrast from both sides of a write
- **Primitive** (disagreement between frozen and adapted contrasts is a signal to choose the next write type).
- **Mechanism:** On the same evidence, estimate directions in a frozen shadow and the current model. If only the adapted-side contrast predicts an effect, evaluate a repair to the learner's last write before editing the base capability. Compare by held-out intervention, not by angle alone.
- **Nearest prior / gap:** TT's frozen-self shadow and PR #400's spillover repair; here the two views diagnose whether the new error requires changed evidence, changed scope, or a fresh edit.
- **Cheapest first test:** Mix planted base shortcuts and learned shortcuts with the same failure rate. **Kill** if the signed shadow disagreement does not improve assignment versus leave-one-edit-out plus a frozen shadow.
- **Old-task retention:** Preserve gains from the last write on its genuine target while removing its shortcut.
- **Risk / likely tie:** The two activation bases may drift enough to make vector comparisons meaningless; use matched downstream causal effects.

### AL15 · Save a disagreement mode, not two concepts
- **Primitive** (a provisional write retains a common direction and one directional disagreement that is reactivated by discriminating evidence).
- **Mechanism:** When two task hypotheses agree on today's queries, commit their shared effect only. Retain the cheapest directional contrast that distinguishes their predictions so a future witness resolves the branch without replaying all support.
- **Nearest prior / gap:** [PR #378](https://github.com/manojbajaj95/cl/pull/378) tests forking contradictory habits; this is before the contradiction is observed, and stores the difference between plausible edits instead of two complete edits.
- **Cheapest first test:** Two candidate table rules agree on most examples until a crossed query arrives. **Kill** if a same-byte pair of full hypotheses or matched buffered replay adapts as quickly without speculative failures.
- **Old-task retention:** Old rules and all queries in the two hypotheses' agreement region.
- **Risk / likely tie:** A symbolic candidate set may be much smaller for clean tasks; test cases where hypotheses are induced rather than supplied.

### AL16 · Learn the transition separately from the rule
- **Primitive** (a context-transition direction changes which evidence counts without rewriting the rule itself).
- **Mechanism:** Fit recurring rule directions once. On a confirmed regime switch, update a separate contrast of boundary evidence that shifts the learner's active evidence weighting. Require it to predict what counts on a new rule pair never seen together.
- **Nearest prior / gap:** Context-inference CL, mixtures of adapters, task-switching in [PR #378](https://github.com/manojbajaj95/cl/pull/378); the gap is transfer of the transition edit across previously unseen combinations.
- **Cheapest first test:** Alternate instruction formats across extraction rules; hold out one format-by-rule switch. **Kill** if a lightweight learned router with independent task vectors transfers equally well.
- **Old-task retention:** Old rule/format combinations, including switches back to earlier regimes.
- **Risk / likely tie:** Equivalent to a shared router if there is no benefit from modifying the contrast's evidence weighting.

### AL17 · Teach the direction with the most decisive question
- **Improvement** (active learning over candidate writes).
- **Mechanism:** Choose a benign support query where two candidate suppressions cause different counterfactual predictions; ask a verifier to resolve it instead of selecting the query with the most uncertain base prediction.
- **Nearest prior / gap:** Query by committee, crossed evidence in PR #140; moves the committee to inexpensive proposed interventions.
- **Cheapest first test:** Given a small verifier budget, disambiguate two visually similar routing conventions in synthetic records. **Kill** if uncertainty sampling and a standard committee at equal queries locate the right edit as quickly.
- **Old-task retention:** Already resolved conventions and queries unaffected by either hypothesis.
- **Risk / likely tie:** Charging intervention forwards may erase the apparent label-efficiency win.

### AL18 · Keep the incompatibility, not the losing write
- **Primitive** (a future write can consult a retained counterexample to a *kind* of suppression).
- **Mechanism:** If two edits conflict, archive a compact protected read statistic and the *change in prediction under the conflicting operation*. Use the pair to challenge future proposals before they repeatedly suppress the same capability, distinguishing “this direction is risky here” from “this lesson failed.”
- **Nearest prior / gap:** AlphaEdit protection and the future-write-witness line in [PR #374](https://github.com/manojbajaj95/cl/pull/374); test whether a measured intervention effect transfers across candidate writers instead of just preserving fixed keys.
- **Cheapest first test:** Teach three tasks on one feature, each using a different candidate write. **Kill** if old examples plus null-space projection prevent repeat damage just as well at matched bytes.
- **Old-task retention:** Protect the original conflicting use and two unseen examples sharing its relevant property.
- **Risk / likely tie:** Safe generalization from a counterexample may appear only if candidate writes are unrealistically similar.

## D · Compose writes without quietly erasing earlier skills

### AL19 · Measure a loop before accepting a write
- **Primitive** (a directional write has an empirical local commutator as a composition diagnostic).
- **Mechanism:** Compare the held-out output under A then B versus B then A. Record where order matters and investigate whether that predicts which later evidence needs re-estimation; distinguish the algebraic commutator on fixed maps from refitting the directions after each write.
- **Nearest prior / gap:** Task Arithmetic/TIES and connection/holonomy ideas in [PR #397](https://github.com/manojbajaj95/cl/pull/397); this loop is used to allocate *revision* budget, not merely quantify order effects.
- **Cheapest first test:** Three sequential task writes with a hidden fourth revision. **Kill** if the loop residual adds no predictive value over geometric overlap, joint rank-2 fit and matched pairwise validation.
- **Old-task retention:** Score all earlier tasks and their held-out combinations after cycling the order.
- **Risk / likely tie:** Vanilla commutators can be large without any behavioral difference, or small at one point while later nonlinear drift dominates.

### AL20 · Re-orthogonalize only a broken dependency
- **Primitive** (a revision operation addresses a collision between two writes, not just either write alone).
- **Mechanism:** For writes shown to interfere, re-fit the smallest change to one write's read vector against two sets of live activations: examples where its effect must hold and examples where the other write must remain unchanged. Leave rather than edit if the constraints cannot be separated.
- **Nearest prior / gap:** AlphaEdit and orthogonal adapters; distinguish selective pair repair using incident evidence from refitting a global protected subspace.
- **Cheapest first test:** Five tasks with one planted collision and one dense-collision control. **Kill** if AlphaEdit plus matched replay wins at equal bytes or only the planted case works.
- **Old-task retention:** Both colliding tasks, a protected neighbor and earlier nonincident tasks.
- **Risk / likely tie:** Damage may be diffuse as in PR #24; sparse repair is a hypothesis, not an assumption.

### AL21 · Cancellation is not forgetting
- **Improvement / assay** (distinguish live but canceled effects from destroyed evidence).
- **Mechanism:** Tag each sign in a suppress/teach pair. Probe the pair both intact and with one side temporarily absent to detect a concealed contribution, and check whether the result predicts selective reactivation when a past regime returns.
- **Nearest prior / gap:** Task-vector cancellation and toggling adapters; this is an assay for silent interference, not a claim that restoration by an explicit switch is new.
- **Cheapest first test:** Alternate two inconsistent harmless conventions, then return to the first with one verified example. **Kill** if absent-side effects do not predict useful reactivation better than held-out margins.
- **Old-task retention:** Both conventions under explicit selectors, plus unrelated tasks when the pair is intact.
- **Risk / likely tie:** The apparent benefit may be exact saved-state replay by construction.

### AL22 · Consolidate only shared exclusions
- **Primitive** (an intersection of independently supported exclusion constraints, validated on an unseen task).
- **Mechanism:** When several tasks reject the same cue, consolidate only the component whose removal helps on all and whose legitimate uses remain recoverable; leave contested components local. Re-open consolidation if later witnesses invalidate the intersection.
- **Nearest prior / gap:** Invariant risk minimization, LEACE and multi-task adapters; tests whether pooling negative evidence transfers to entirely new tasks better than pooled labeled fitting.
- **Cheapest first test:** Learn three schemas with a repeated distractor, transfer to a fourth with a legitimate reuse inserted. **Kill** if pooled CAA or pooled null-space fitting matches transfer and revision after that reuse.
- **Old-task retention:** Old schemas under both misleading and legitimate cue assignments.
- **Risk / likely tie:** Common exclusions may just be shortcuts planted too uniformly by the benchmark.

### AL23 · Separate a retired rule from a prohibited operation
- **Improvement** (scope discipline when revisions happen in stages).
- **Mechanism:** When a benign convention is retired, stop invoking its positive write on new items but don't learn a new negative write unless verified examples show that operation is wrong in scope. Track the distinction under cycles of deployment and retirement.
- **Nearest prior / gap:** Routed adapters, append/retrieve and TT02. The value would be fewer damaging negative updates, not a novel router.
- **Cheapest first test:** Stagger two convention retirements, with one later reinstated. **Kill** if simply unloading an adapter at each retirement performs as well at equivalent state cost.
- **Old-task retention:** Archived inputs and explicit use of the retired convention in its original scope.
- **Risk / likely tie:** A table of versioned conventions may solve the stream without touching the model.

### AL24 · Reserve the next writable split
- **Primitive** (preserve a degree of freedom for future correction rather than just today's predictions).
- **Mechanism:** When installing a new write, retain the distinguishability of two provisional subclasses at its read site, even if their current labels agree. Predict whether a later exception can be installed without rebuilding the current edit.
- **Nearest prior / gap:** AlphaEdit's protection of existing keys and [PR #374](https://github.com/manojbajaj95/cl/pull/374)'s future-edit checks; distinguish preservation of a specific local split, tested on held-out future revisions, from generic larger rank or replay.
- **Cheapest first test:** Teach one format rule, then reveal an independently sampled exception aligned or not with the reserved split. **Kill** if equal-budget rank headroom and standard replay match exception edit cost without reservation.
- **Old-task retention:** Non-exception members of both subclasses and earlier unrelated rules.
- **Risk / likely tie:** If the exception is foreshadowed too explicitly, this is benchmark leakage; reserve from unlabeled descriptors only.

## E · Move from error correction to learning a genuinely new task

### AL25 · Teach the rule, not today's answer
- **Primitive** (a write is factored into a learned selection direction and a runtime value binding).
- **Mechanism:** Use demonstrations to learn where to read the operative field and where to write its effect; bind the new input's value at inference rather than writing target values into weights. Check the distinction by changing the value with the requested operation held fixed.
- **Nearest prior / gap:** ROME's key–value view, function vectors and the [fact–skill entanglement node](https://github.com/manojbajaj95/cl/pull/140); here the role direction is taught online and must continue to work under held-out value substitutions.
- **Cheapest first test:** Invent a rule that chooses a field and applies an existing conversion; swap all field values at test time. **Kill** if function-vector steering, a trained rank-1 read/write or matched ICL transfers equally well.
- **Old-task retention:** Original field selectors, value copying and the conversion when requested independently.
- **Risk / likely tie:** This tests new bindings over existing operations, not acquiring the conversion itself.

### AL26 · Bind an exclusion to a relation instead of a token
- **Primitive** (a rule can suppress a relation under variable substitution).
- **Mechanism:** Create matched examples where each token is sometimes useful and sometimes misleading. Fit a read direction from the composed representation at a decision site, then subtract only the relation-dependent effect. Test on unseen tokens and incompatible templates.
- **Nearest prior / gap:** Concept erasure, function vectors and compositional ReFT; success requires portability under renaming rather than tracking a memorized string.
- **Cheapest first test:** Teach “don't select duplicated values when asked for the unique entry” across tables whose value vocabularies are disjoint. **Kill** if raw CAA plus templated routing or matched ReFT transfers equally well.
- **Old-task retention:** Duplicate-counting and tasks where selecting a repeated value is correct.
- **Risk / likely tie:** ICL may solve the relation with far fewer examples; match the actual feedback given to it, not just inference tokens.

### AL27 · Separately accumulate the skill and the anti-shortcut
- **Primitive** (two state variables respond to different verified events and can be independently retracted).
- **Mechanism:** Let successful novel-rule applications teach a positive read/write map; let controlled cue failures teach inhibition. First learn both, then receive feedback that changes only one of them. Reuse the unchanged statistic instead of replacing the entire task delta.
- **Nearest prior / gap:** Task Arithmetic and HL15+HL17 add corrections to a trained adapter. Here feedback streams identify which dynamic component should change; first demonstrate separability beyond an offline additive fit.
- **Cheapest first test:** Alternate between changing the mapping and changing the distractor, in a stream with factorial controls. **Kill** if one equal-rank adaptive ReFT or separately fitted adapters with simple routing match the revision curve at equal bytes.
- **Old-task retention:** A rule stable across both changes and unaffected cases of each changing rule.
- **Risk / likely tie:** Clean factorization on a toy could be guaranteed by design; require tests with partially correlated change events.

### AL28 · Teach a missing distinction by intervening before gathering labels
- **Primitive** (temporary interventions create a teaching view that the unedited learner cannot easily sample).
- **Mechanism:** If the model deterministically repeats a shortcut, test a temporary, benign shortcut inhibition only for generating candidate solutions. Use external verification to learn a distinct positive write from the verified rollout; discard the exploration edit.
- **Nearest prior / gap:** [SEAL](https://arxiv.org/abs/2506.10943), best-of-N and verifier-twin ideas in PR #51; the claim is better evidence from a specific representational intervention, not self-training itself.
- **Cheapest first test:** Small exact arithmetic tasks where the default trace picks a misleading heuristic. **Kill** if entropy-matched sampling, prompt perturbations or best-of-N yield equally valuable examples under the same verifier and forward budget.
- **Old-task retention:** Correct uses of the original heuristic, assessed after discarding the exploration edit and applying the learned write.
- **Risk / likely tie:** The verifier can make any diversity strategy look effective; filter all arms identically and test on unseen structures.

### AL29 · Distill a bounded teaching pulse into one map
- **Improvement** (deployment alternative to a live activation hook).
- **Mechanism:** Fit a low-rank parameter delta to reproduce the effect of a temporary multi-token teaching intervention on observed inputs, then remove the hook and rerun with no support. Match effects on old-task witnesses as well as current ones.
- **Nearest prior / gap:** ReFT, WSP writes ICL and PR #374's context handoff already cover related transfers; this is an engineering comparison of two deployment forms.
- **Cheapest first test:** Three output formats after a single teaching pulse each. **Kill** if distillation loses its latency advantage or rank-1 LoRA reaches the same retention and gain at lower total cost.
- **Old-task retention:** Original formats and longer outputs that reuse the edited map at multiple positions.
- **Risk / likely tie:** Exact injection at the same linear site is a degenerate control; compare only where the behavior being distilled is broader than that one operator.

### AL30 · Spend the same bytes on exceptions or geometry
- **Improvement / assay** (find the boundary where a directional learner beats explicit memory).
- **Mechanism:** Supply a stream with a reusable base operation and progressively more arbitrary exceptions. Compare storing eligible exception rows against storing only directions, and against a hybrid, at constant total serving state.
- **Nearest prior / gap:** GRACE-style editing, replay and PR #374's residual split; the purpose is to estimate a regime, not reinvent a cache.
- **Cheapest first test:** A small switchable table task with 0, 4, 16 and 64 independently generated exceptions at a matched byte cap. **Kill** the compact-learning claim if lookup plus ICL dominates on gain, latency and retention across the sweep.
- **Old-task retention:** The reusable operation outside exceptions and earlier exceptions after admitting later ones.
- **Risk / likely tie:** Arbitrary exceptions carry irreducible information; an apparent win could reflect hidden structure or an undercharged router.

## F · Make the learner know when not to write

### AL31 · No-write certificates from competing explanations
- **Primitive** (an episode can yield an evidence-backed decision not to write, with a condition that would reopen it).
- **Mechanism:** When candidate interventions agree on support but disagree in effects on protected witnesses, hold off. Record a query family that would disambiguate the proposed writes; reopen only when the needed evidence arrives.
- **Nearest prior / gap:** Calibrated abstention, active learning, TT23–TT28 gates; beyond a scalar threshold, an unresolved distinction identifies exactly which evidence can make the write admissible.
- **Cheapest first test:** Mix streams with genuinely ambiguous shortcuts and streams with noise-only corrections. **Kill** if threshold gating plus query-by-committee matches erroneous-write rate and recovery lag at equal evidence cost.
- **Old-task retention:** Protected ambiguous-task witnesses and previously learned unambiguous rules.
- **Risk / likely tie:** “Certificate” is empirical and scoped to the proposed write family; a hidden alternative can invalidate it.

### AL32 · Empirical headroom for the next write
- **Improvement / assay** (local warning signal, not a global edit-capacity law).
- **Mechanism:** Compare gain–damage slopes for tiny hypothetical writes against held-out current and old tasks. Test if the slope forecasts the next real write's feasible dose more usefully than activation overlap or weight norm.
- **Nearest prior / gap:** [PR #22](https://github.com/manojbajaj95/cl/pull/22) falsified the stronger pre-edit capacity claim; this narrower prediction concerns one next update and observable old-task violations.
- **Cheapest first test:** Six sequential tiny edits with varied overlap. **Kill** if the forecast is no better than an equal-budget norm threshold plus a single dry-run edit.
- **Old-task retention:** Per-old-task violation rates, not only average damage.
- **Risk / likely tie:** Almost identical pilot and actual doses can make the forecast trivial; hold out doses and task pairs.

### AL33 · Learn a harmless edit prior, then freeze it
- **Improvement** (test whether edit-ready training reduces evidence requirements).
- **Mechanism:** On benign training streams, learn a small set of sites where support-derived rank-1 writes are usually safe. Freeze that choice; then fit only contrast statistics online on novel streams. Retest against a model selected for equal base quality without edit rehearsal.
- **Nearest prior / gap:** Editable training (MEND), ReFT and HL33; empirical question is whether rehearsal helps closed-form writes specifically out of distribution.
- **Cheapest first test:** Rehearse on format changes, hold out schema and arithmetic changes. **Kill** if the rehearsed base does not beat untouched-base steering and equal-budget ReFT once all rehearsal cost is charged.
- **Old-task retention:** Measure base scores before rehearsal, after rehearsal and after novel writes.
- **Risk / likely tie:** This can become ordinary training on the test task family; hold out entire change mechanisms, not just instances.

### AL34 · Keep a fixed reviewer of behavior changes
- **Improvement / assay** (a release gate for an online writer).
- **Mechanism:** Give an independent frozen gate paired pre-/post-edit outputs and separate benign scope checks. Reject edits that change protected behavior or only improve a verifier proxy; monitor false negatives against planted benign collateral errors rather than deliberately targeting safety behavior.
- **Nearest prior / gap:** TT's frozen-self scoring and PR #400's serve-time auditing; required infrastructure, not a proposed new editing method.
- **Cheapest first test:** Use held-out collateral changes from AL07 and AL20, plus equally sized useful edits. **Kill** the learned gate if a fixed regression suite and an entropy-matched delta threshold flag the same damage at lower cost.
- **Old-task retention:** Direct gate target; report worst-slice misses on independently labeled old tasks and policy sentinels.
- **Risk / likely tie:** Optimizing for a repeatedly queried gate may overfit its examples; keep the final audit inaccessible to the learner.

## Ranked deeper questions

1. **Can negative evidence teach a model to ignore one use of a signal without losing the others (AL02, AL08, AL11)?** Start with the crossed table stream: the same cue is wrong in one decision and useful in another. Compare an edge write and evidence-space subtraction against equal-data conditional erasure and ReFT. If neither adds selective transfer off the supported cue combinations, treat subtraction as a baseline rather than a learning primitive.
2. **Can a learner retract one wrong lesson without replaying everything it learned around it (AL13, AL14, AL19)?** Withdraw a witness after two dependent writes, with later rules still in use. Test whether evidence retraction plus the order diagnostic reduces revision cost compared with the strongest stacked baseline: replay and incident-only validation at equal bytes. If the issue is just subtracting a saved delta, this branch is already covered by rollback.
3. **Can remove-and-teach acquire new rules, or does it only expose routines already in the model (AL05, AL25, AL27, AL30)?** Require a fresh, arbitrary rule that must bind to unseen values, teach it, drop the examples and perturb the shortcut separately. If matched context or lookup retains more old skills at the same total cost, reserve direction writes for recovery rather than arbitrary acquisition.
4. **Can the next correction be made cheaper by what a write chooses not to erase today (AL15, AL18, AL24)?** Reserve a split using only unlabeled hints, then evaluate an independently sampled revision stream. Beat equal-rank headroom and replay on revision latency as well as retention; otherwise this is just more memory for potential exceptions.
5. **What is the smallest credible online loop for using these writes (AL01, AL07, AL17, AL31, AL34)?** Start from one contrast, a bounded subtractive write, a no-write arm and an independent retention check. Count support, calibration and inference cost; if this loop cannot match few-shot context on stable tasks at any gain/latency/retention point, defer more elaborate deployment ideas.
