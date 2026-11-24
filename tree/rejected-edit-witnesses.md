# Rejected-edit witnesses: learn from the writes you refuse

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Cross-pool round 39](../ideas/flood/cross-pool-39.md) ([PR #36](https://github.com/manojbajaj95/cl/pull/36)). **Review seed:** [Flood triage row 264](https://github.com/manojbajaj95/cl/blob/563fd7a57adeb1bca9464bd071885ef27476e6d5/reviews/flood-triage.md#L264) gives WFG1 and WFG6 score 3: fit a teacher substitute where a finite edit lands that neither model would choose; shrink a refused edit to the correction it exposes and teach that correction rather than granting an exception. The reviewer did not rate the merge above its best parts.

## Is a memory that grows from its own refusals a new object for continual learning?

**Not by default.** A rejection loop is counterexample-guided repair, a tiny training set is condensation, and abstention is a decision rule. The candidate object is a **bounded training memory whose entries turn a diagnosed refusal into a corrective training effect that a later, independent editor can benefit from**. The memory changes what the learner can safely accommodate, not what the gate calls safe. It earns primitive status only if these effects transfer across unseen edits or reduce source/proof costs beyond counterexample-guided repair plus branch-matched condensation and exact rechecking, at the same old-task floors and fixed editor demand. An exception log, a gate predictor, and a cache of fixes for known payloads do not qualify.

### What a refusal teaches

1. **Freeze the demand.** An independent editor fixes the payload, utility target, allowed accommodations, and whether deployment is atomic or exposes intermediate states. Hold the old-task checks and threshold fixed. Separate the visible fit family from independent edit families committed before fitting; never replace a difficult payload with a friendlier one in the score.
2. **Diagnose before teaching.** Check the prospective edited state in shadow; a refusal can reflect a demonstrated miss in the substitute, an impossible demand under the allowed accommodations, or an incomplete proof. Also distinguish a repair outside the *witness language* from a repair outside the full accommodation budget. In finite toys enumerate both sets; outside them, a failed search is **unknown**, not a proof of impossibility. A failing live teacher disqualifies it as a corrective target for that branch, even if some other valid repair exists.
3. **Shrink the diagnosis, not the transaction.** Minimize a shadow edit/input or a causal prefix while preserving legality, the specific failed check, and the missing correction. A provider converts it into a truthful labeled example or a synthetic example in a declared grammar. Refit the witness and retry the **original** payload with an independent checker. The rejected payload neither runs live nor becomes an exception, and an ambiguous or unteachable failure need not add an example.
4. **Cover externally reached states.** Search source- and substitute-reachable states, plus shadow successors reached by legal proposed edits even if neither training policy generates them. “Legal” means in the declared proposal domain, not authorized to serve. Compare corrective transitions on the same full state (including slots, clocks and sampler where relevant), with the same batch and randomness. Recompute reachability after replacing the witness. Check old behavior independently of teacher agreement; a held-out pass is not a proof of unseen scope.

**Paper case.** Let the old signed margin be `m_q(t)=1−ReLU(t−q)`, with floor `1/2`, and an editor fix `t:0→1`. At zero, `q=1/4` and `q=3/4` give identical margins and tangents. After the edit, their margins are `1/4` and `3/4`; only the former needs a correction. If the accommodation adds to the old readout without touching the new target, the former needs at least `1/4` at the real endpoint. Its shadow failure can shrink to `t=3/4+ε`, where it needs only `ε`. Storing that point's correction verbatim need not fix the original edit. Keep enough information to teach the far-side response (or collect a second legal point), then recheck `t=1`. If the allowed readout increment is capped below `1/4`, collecting more examples cannot make that payload admissible through this accommodation. The example shows why neither local tangents nor smallest failing points alone establish the needed training effect.

### Prior art and common controls

- [Counterexample-guided neural repair](https://arxiv.org/abs/2301.11342) already alternates checking and refitting, and [Editable Neural Networks](https://arxiv.org/abs/2004.00345) trains models to accommodate corrections. [MEND](https://arxiv.org/abs/2110.11309) learns to transform edit gradients; [Rebuilding ROME](https://arxiv.org/abs/2403.07175) addresses collapse during sequential editing. The claim is neither that edits can be repaired nor that failure improves the next update; it concerns persisting a transferable *training* effect without an edit-specific patch or old-source read.
- [MTT](https://arxiv.org/abs/2203.11932), [gradient matching](https://arxiv.org/abs/2006.05929), [GCR](https://arxiv.org/abs/2111.11210), [DER](https://arxiv.org/abs/2004.07211), and [LwF](https://arxiv.org/abs/1606.09282) store or distill training signal; [DAgger](https://arxiv.org/abs/1011.0686) queries an expert on learner-induced states; [HAL](https://arxiv.org/abs/2002.08165) learns anchors against future interference. Give condensers and repair baselines the same blind-editor fit branches, counterexamples, and teacher queries. Compare also with [witness examples](https://github.com/manojbajaj95/cl/pull/163), [self-closing witnesses](https://github.com/manojbajaj95/cl/pull/165) without external edits, and [finite-edit guards](https://github.com/manojbajaj95/cl/pull/164) without new training evidence.
- [SelectiveNet](https://arxiv.org/abs/1901.09192) learns a reject option; [selective classification](https://arxiv.org/abs/1705.08500) prices risk against coverage; [weight-interval CL](https://arxiv.org/abs/2206.07996) constrains future weights for retention. Prediction abstention is not edit abstention, but coverage/risk accounting belongs in both. Rejected-preference learning (e.g. [DPO](https://arxiv.org/abs/2305.18290)) is another control for using a reject signal as supervision; the gate verdict alone does not identify any lawful accommodation.
- Following the [idea ledger](https://github.com/manojbajaj95/cl/blob/563fd7a57adeb1bca9464bd071885ef27476e6d5/reviews/idea-ledger.md), do not credit self-generated data over matched teacher data, assume sparse interference, or evaluate against mismatched new-task progress. Compare random boundary examples, raw counterexample replay, a refusal/exception cache (no unsafe overrides), exact repair from scratch, and repair plus MTT using the same checker, example grammar and acquisition budget. Record worst-prefix ordinary A/C performance including rare slices, from both acquisition and pre-edit references, on independent data. Count all frozen offers (including refuses and unknowns), new-task utility, source calls, solver work, final and peak bytes, including proof/metadata; never count a refusal as retention progress. Where claiming retirement, block source reads and overwrite the released storage; keep oracle/evaluation state separate. The literature check is provisional.

## Idea cards

**P** = conditional primitive candidate: hints at a reusable object or operation. **I** = improvement or audit: adapts known machinery. All first tests are CPU thought-outlines, not results.

### Find the correction, not just the failure

#### 01. A refusal that carries its own repair target (P)
- **Mechanism:** Store a lawful training example with the scoped corrective transition it can teach, keyed to a failed invariant, not to the editor ID. Let later edits reuse it under the same checker without accessing the original payload.
- **Novelty:** The [repair loop](https://arxiv.org/abs/2301.11342) is known; the proposed object is the reusable witness, rather than repaired weights or a failed-input replay item.
- **Cheapest first test:** Finite two-gate ReLU model, two committed editors with the same failed invariant but disjoint payloads; learn from one, test the other against matched repair plus MTT.
- **Old-task retention:** Check ordinary A and C after every accommodation and retry; include an untouched rare C slice that shares the repaired readout.

#### 02. Off-policy gate pairs (I)
- **Mechanism:** Fit on shadow pre/post states of external finite edits chosen to cross hidden gates; keep source and witness rollouts in the fit set too.
- **Novelty:** [DAgger](https://arxiv.org/abs/1011.0686) collects learner-induced states; the added sampler uses independent edits outside both policies, not a new aggregation algorithm.
- **Cheapest first test:** Use the paper case with two blind gates, equal teacher-query counts, and compare self-closing search, Jacobian matching, and branch-matched [MTT](https://arxiv.org/abs/2203.11932).
- **Old-task retention:** Check held-out A margins on both sides of each gate and ordinary C even for edits that do not activate either gate.

#### 03. The minimum that still teaches (I)
- **Mechanism:** Minimize the failed edit/input pair subject to retaining a separating correction, not merely a negative margin. Require witnesses that distinguish two candidate far-side response laws.
- **Novelty:** [Counterexample-guided repair](https://arxiv.org/abs/2301.11342) already selects violations; the extra minimization constraint retains teachability and may cost an additional point.
- **Cheapest first test:** On a rational grid construct two post-gate slopes agreeing at the smallest failing point; compare one-point shrinking, a separating pair, and raw replay at equal cost.
- **Old-task retention:** Repeat the full original edit and an unseen larger legal edit; score independent A/C at each prefix, not at the reduced point alone.

#### 04. Three different refusals that look identical (I)
- **Mechanism:** Emit different outcomes for a missing witness, genuine incompatibility, and verifier uncertainty; split a missing expressible witness from an inexpressible correction in metadata.
- **Novelty:** [SelectiveNet](https://arxiv.org/abs/1901.09192) has a reject option, not a diagnosis of which training action might change admission; repair already recognizes infeasibility.
- **Cheapest first test:** Enumerate a tiny witness grammar and a wider accommodation menu; blind the method to examples of each outcome and compare against adding a sample after every refusal.
- **Old-task retention:** Keep A/C floors fixed when an unknown is promoted to a checked admit; verify that proven-impossible payloads cannot enter through a fallback.

#### 05. Minimize the causal prefix (I)
- **Mechanism:** Shrink a sequence of edits and refreshes to the smallest legal subsequence retaining the same violation and missing transition. Carry the relevant optimizer state, not just the final input.
- **Novelty:** [MTT](https://arxiv.org/abs/2203.11932) matches trajectories; the proposed search finds which part of a trajectory gives supervision unavailable from its endpoint.
- **Cheapest first test:** Two writes and one momentum step on a scalar ReLU; enumerate prefixes whose weights agree but slots differ; compare weight-only and full-state counterexamples.
- **Old-task retention:** Roll out one extra refresh and score A/C every step; include an old task with no initial prediction change.

#### 06. Correction with no lawful example (I)
- **Mechanism:** Maintain a refusal class for effects achievable by an allowed direct repair but not by the current truthful-example pool or frozen synthetic grammar. Test these representability claims separately.
- **Novelty:** [Gradient matching](https://arxiv.org/abs/2006.05929) optimizes examples; the audit asks when failure is a limitation of the allowed examples, not of the optimizer.
- **Cheapest first test:** Enumerate a finite linear example pool whose updates miss an orthogonal correction, then reveal one truthful separating example and check which refusals disappear.
- **Old-task retention:** Include old A/C probes that constrain the untouched direction; the direct repair must satisfy the same floors as any example-based fix.

### Make a witness useful to an editor nobody has seen

#### 07. Correction classes, not edit clusters (P)
- **Mechanism:** Group refusals only when the same scoped witness fixes them under a declared continuation set. Split the group on a separating continuation, even if surface edits look identical.
- **Novelty:** [GCR](https://arxiv.org/abs/2111.11210) already groups by gradient effect; the proposed unit is interchangeability for admission after an independent finite continuation, not gradient similarity now.
- **Cheapest first test:** Four rational edits in two hidden correction classes; compare effect clustering, raw replay and exhaustive class construction on held-out editors.
- **Old-task retention:** Test A/C after two edits from each claimed class; count negative transfer when a class hits the wrong old slice.

#### 08. A witness that another host can use (P)
- **Mechanism:** Export a truthful example and a checked description of its corrective effect; a second learner with a different parameterization rechecks and binds that effect locally, without copying a source delta.
- **Novelty:** [MEND](https://arxiv.org/abs/2110.11309) learns reusable gradient transformations and [Pacti](https://arxiv.org/abs/2303.17751) supplies contract machinery. The proposed unit is portable evidence learned from a refusal whose effect must be re-established rather than assumed.
- **Cheapest first test:** Transfer between two ReLU learners with permuted units and a third with a shifted gate; compare raw examples, transported deltas and local repair with identical source access.
- **Old-task retention:** Check each host's separate A/C references after a frozen unseen edit, including C slices absent from the exporter.

#### 09. Two witnesses, one nonlinear repair (P)
- **Mechanism:** Fit two small witness sets whose joint effects repair a refusal only after their updates interact; certify legal orders rather than adding their effects linearly.
- **Novelty:** [Pacti](https://arxiv.org/abs/2303.17751) can compose effect contracts. The test is whether learning the two training sets produces a reusable composition beyond ordinary checked joint repair, not whether composition exists.
- **Cheapest first test:** Use a two-coordinate model where the old readout needs a product above a fixed bound; compare each set alone, their stack, and jointly learned MTT at equal bytes and proof effort.
- **Old-task retention:** Check A and C after each live step; if the deployment is atomic, separately test the shadow paths and never credit them as served prefixes.

#### 10. Distractor edits that share the failure signature (I)
- **Mechanism:** Collect hard negative pairs that look identical to the admission heuristic but require opposite corrections. Use them to learn when not to reuse a witness.
- **Novelty:** [Selective classification](https://arxiv.org/abs/1705.08500) already trades coverage against risk; here the negative signal vetoes a *training aid*, not the underlying frozen edit.
- **Cheapest first test:** Give two equal-margin failures one shared summary and opposite old-task gradients; compare summary routing with a separating witness and checker-only routing.
- **Old-task retention:** Include A and C cases separately damaged by opposite corrections; report wrong candidate reuse as well as post-check retention and coverage.

#### 11. Teach the next refusal using a legitimate example from today (I)
- **Mechanism:** When a refusal exposes a missing distinction, select a truthful current example that will teach it before the next blind refresh rather than persisting an extra synthetic example.
- **Novelty:** [HAL](https://arxiv.org/abs/2002.08165) uses look-ahead anchors; this adapts data selection to a diagnosed external-edit gap with a teacher-free refresh endpoint.
- **Cheapest first test:** Enumerate equal-size batches from a rule/shortcut toy; compare refusal-guided selection with look-ahead scoring and matched margins, without changing labels or the refresh schedule.
- **Old-task retention:** Score ordinary A/C after refresh and blocked source reads, with a withheld split where shortcut and rule disagree.

#### 12. The refused edit chooses a question, not an answer (I)
- **Mechanism:** Use a failed guard to choose between targeted teacher queries; accept an example only if the answer rules out at least one still-plausible corrective transition.
- **Novelty:** [DAgger](https://arxiv.org/abs/1011.0686) queries an oracle at encountered states. This is a query-efficiency refinement when passive rollouts cannot distinguish teachers, not a claim that rejection labels contain teacher knowledge.
- **Cheapest first test:** Two finite teachers agree on routine trajectories and disagree after one edit; compare matched random/source queries and the optimal exhaustive query policy.
- **Old-task retention:** Freeze after queries and run A/C in both teacher worlds on held-out edits, counting unresolved cases rather than guessing.

### Grow, spend, and retire the memory

#### 13. Refusal rent (P)
- **Mechanism:** Evict a witness only when its marginal contribution to future checked frozen-edit utility is lower than its byte-time cost; require an independent check on the updated store.
- **Novelty:** [GCR](https://arxiv.org/abs/2111.11210) allocates by gradient coverage; the proposed retained quantity is independently reusable admission coverage, which can disappear non-additively when another witness is evicted.
- **Cheapest first test:** Enumerate all fixed-byte buffers for a four-edit finite game, with one apparently redundant witness that becomes essential after a later edit.
- **Old-task retention:** Run A/C after every eviction and edit order; report worst-prefix rare retention and refusals, so refusing everything cannot win.

#### 14. A receipt for the shadow work already done (P)
- **Mechanism:** Bind a witness to a checkable slice of the transition relation; reuse that evidence for the same slice later while rechecking changed premises, rather than caching an accept verdict.
- **Novelty:** [Pacti](https://arxiv.org/abs/2303.17751) and incremental verification already reuse assumptions; novelty requires that the learned training artifact makes repeated proof cheaper even after charging provenance.
- **Cheapest first test:** Finite two-branch checker with one unchanged and one shifted guard; compare witness proofs to ordinary incremental verification, with proof byte and solve time totals.
- **Old-task retention:** Force a stale receipt to encounter an A violation and a separate C violation; both must fail rechecking without narrowing future demand.

#### 15. Refusals after the source is gone (P)
- **Mechanism:** Retire the teacher with a small scoped set of labeled separators the witness can lawfully use for later fitting. Refuse unknown cases when the retained evidence cannot distinguish the relevant teacher responses.
- **Novelty:** [DER](https://arxiv.org/abs/2004.07211) caches historical targets, and [FRCL](https://arxiv.org/abs/1901.11356) stores functional anchors. The proposed affordance is a limited capacity to answer *new repair questions* after actual source reclamation, not generic distillation.
- **Cheapest first test:** Hide two teacher rules that agree on all routine data; vary which separators survive overwrite and test fresh refusal repair against equal-byte DER and source summaries.
- **Old-task retention:** Score ordinary A/C before and after actual source storage reuse; a held-out impossible-to-answer case must stay refused without making the learner forget.

#### 16. Pay for negative evidence, not a blacklist (I)
- **Mechanism:** Store a bounded incompatibility certificate only when it proves no permitted accommodation can fix a class of requests. Keep it separate from the example store and revalidate its assumptions when the host changes.
- **Novelty:** [Counterexample-guided repair](https://arxiv.org/abs/2301.11342) and [Pacti](https://arxiv.org/abs/2303.17751) already reason about infeasible constraints; the audit tests whether persistent negative evidence saves repeated repair work.
- **Cheapest first test:** Use a finite menu with duplicate impossible offers and a near neighbor that is feasible. Compare no cache, raw refusals, and proof reuse at equal memory.
- **Old-task retention:** Try both the formerly impossible offer after a valid host change and the always-feasible neighbor; check A/C and count false refusals alongside false admits.

#### 17. Self-induced refusals move the frontier (P)
- **Mechanism:** After each witness refit, search the new source and replacement reachability sets for displaced refusals; choose candidates for two-round admission coverage instead of immediate gate-pass gain.
- **Novelty:** [DAgger](https://arxiv.org/abs/1011.0686) tracks induced states and [repair](https://arxiv.org/abs/2301.11342) reruns the checker. The proposed quantity is which future independent edits remain teachable because of today's witness, not fixed-point agreement alone.
- **Cheapest first test:** Enumerate a two-round edit game where equal first-step repairs differ on the second committed offer; compare against generic contingent planning plus repair.
- **Old-task retention:** Score A/C after both rounds on every legal served path and charge all refused leaf offers, including those masked by the first refusal.

#### 18. A stable service route while witnesses learn (I)
- **Mechanism:** Train witness candidates in shadow after a refusal, carry their versioned scope, and publish only after the original commit and accumulated old obligations pass together.
- **Novelty:** [Weight-interval CL](https://arxiv.org/abs/2206.07996) constrains allowed parameters and [PR #157](https://github.com/manojbajaj95/cl/pull/157) already proposes make-before-break. This is a test of the handover cost of refusal-driven refits, not a new deployment protocol.
- **Cheapest first test:** Two-slot finite host where the shadow learner needs an unsafe intermediate before reaching a safe final state; compare atomic publish and truly live training under the same rule.
- **Old-task retention:** Score continuously served A/C on the active slot, and explicitly test interrupted publication and the subsequent retry.

### Try to disprove the object

#### 19. Same witness with the refusal bit erased (I)
- **Mechanism:** Cross example content with how it was selected: identical witness with or without refusal metadata, versus equal-sized random, gradient-matched and refusal-mined stores.
- **Novelty:** [Dataset condensation](https://arxiv.org/abs/2006.05929) predicts the effect may come entirely from the examples. No primitive claim survives if refusal metadata adds no usable scope and selection beats only a weak baseline.
- **Cheapest first test:** Exhaustively match small buffers on update effects for seen branches, then compare cost and admission on disjoint frozen edit families.
- **Old-task retention:** Compare A/C at matched admitted utility across arms, including immediate and delayed interference; label unmatched operating points.

#### 20. A verifier can manufacture a memory (I)
- **Mechanism:** Replay the same frozen requests under an exact checker and a deliberately incomplete one. Track how much memory stores proof artifacts rather than correcting real behavior.
- **Novelty:** [Counterexample-guided repair](https://arxiv.org/abs/2301.11342) already links solver and refitting; this audit isolates the source of apparent continual progress.
- **Cheapest first test:** Rational-grid ReLU versus an interval checker that cannot represent correlated inputs; compare witness growth and exact behavior against tightening the checker alone.
- **Old-task retention:** Both checkers face the same independent A/C evaluation; verifier uncertainty cannot count as either forgetting or evidence of safe retention.

#### 21. Demand that the memory never gets to curate (I)
- **Mechanism:** Precommit an editor suite with ordinary offers, rare gate crossings, repeated offers, and feasible and impossible demands. Score independently of what the current memory chooses to solicit or retry.
- **Novelty:** [Selective classification](https://arxiv.org/abs/1705.08500) supplies the coverage-risk analogy, and [model editing evaluation](https://arxiv.org/abs/2502.11177) questions narrow edit scores. The audit makes the denominator fixed for longitudinal learning.
- **Cheapest first test:** Compare a gate that appears safer by refusing difficult requests with a witness arm that admits more at the same exact checker and service floor.
- **Old-task retention:** Report A/C at every live prefix and at matched accepted utility; separately expose rare slices whose service stays high only because all relevant edits are refused.

#### 22. A bit lower bound for anonymous refusals (I)
- **Mechanism:** Construct teacher pairs whose allowed refusals and routine observations coincide but whose valid corrections differ; then grow the family with independent hidden distinctions to stress memory/query limits.
- **Novelty:** [FRCL](https://arxiv.org/abs/1901.11356) and [gradient matching](https://arxiv.org/abs/2006.05929) offer compact summaries, not a reason to expect compression when refusal evidence lacks the distinguishing information. This is a lower-bound audit, not a storage proposal.
- **Cheapest first test:** Enumerate teachers indexed by a few hidden bits with identical refusal transcripts up to a cut; verify that one shared post-cut buffer cannot solve mutually exclusive correction targets. Then price one legitimate separating signal at a time.
- **Old-task retention:** Test held-out A/C for each teacher, counting abstention separately; an incompatible correction must not obtain credit for new utility at the expense of either old task.

## Ranked deeper questions

1. **Can one minimal refusal witness buy safe utility on frozen edits from an unseen editor after the original teacher is overwritten?** Start with cards 01–03 and 15. Give branch-matched MTT plus counterexample repair the same observations and checker. If it matches the admitted utility, old-task floors and source/proof costs, do not call the witness a new object.
2. **What is the smallest sufficient evidence: failing point, separating pair, or continuation-dependent response?** Cards 03, 05 and 22 separate informativeness from mere failure minimality. Look for worlds identical on every stored transcript but requiring different repairs, then identify the cheapest lawful signal that breaks the tie.
3. **Can memories learned from past refusals keep future repairs possible without following an ever-moving boundary?** Cards 07, 13 and 17 ask whether reusable effect classes and eviction rules preserve two-round utility better than counterexample repair plus planning. Check coverage on a fixed demand denominator; stopping growth by refusing harder edits is not success.
4. **Does refusal-guided growth repair the learner or just the verifier's picture of it?** Cards 04 and 19–21 hold service and editor demand fixed while changing proof strength and example selection. The strongest null is that ordinary checker improvements and matched raw counterexample replay recover the entire gain.
