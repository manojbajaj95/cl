# Stored slack: is "how far the fact can move" a new memory object for continual learning?

**Status:** ideas only; no experiments, probe code, or GPU. **Parent:** [Learned invalidation](learned-invalidation.md) ([PR #148](https://github.com/manojbajaj95/cl/pull/148)), cards 6 and 7. **Review seed:** [`reviews/flood-triage.md`, row 239](https://github.com/manojbajaj95/cl/blob/dfb4d52e8e2ef4938bc1e578baa9a04c8d98cad5/reviews/flood-triage.md#L239), which kept #148#6 with #148#7 at score 3: for each (answer, fact) edge, store signed slack in units of the fact, decrement it on sub-threshold moves, and write to the weights only when accumulated drift crosses the smallest dependent slack. Controls named there: #144#16 binding-only tracking, edit-on-answer-change, periodic full re-edit, an external slack table at equal bytes, untouched facts as retention.

The truck question from the parent: the toll is €14, the budget is €20, so the cached answer "yes" has €6 of slack on the toll edge. A move to €16 should change nothing visible but should leave €4. A later move to €21 should flip the answer. Today a network stores the "yes" and, at best, a logit margin in its own units, not the €6. This node asks two things. Is slack a memory object in its own right, distinct from the answer, the fact and the margin? And what does storing it do for forgetting?

## Why this is hard (root cause)

- **Slack duplicates information the model already has.** In the one-fact monotone case, slack is `threshold − value`. The answer plus its slack carries exactly what the fact value and the procedure's threshold carry. Storing slack therefore makes a per-consumer copy of shared state. That copy earns its bytes only if it buys one of three things: (i) serving without reading the fact, (ii) writes confined to the consumers that actually flip, or (iii) persistence where the fact slot or the procedure gets damaged. Without one of those, a pure reader that recomputes `threshold − value` is cheaper and exact.
- **A countdown is itself a write.** "Write weights only when slack runs out" holds only if the counter lives outside the weights that serve answers: an external scalar, an activation or KV state, or an isolated adapter. If the counter sits in shared weights, every decrement is a weight write with its own interference, and the claimed saving disappears. Every card has to say where the counter lives and charge counter writes to `C` and their collateral to `D`.
- **Slack is margin measured in fact units.** To first order `s ≈ m / |∂m/∂f|`, where `m` is the answer's logit margin. The ledger's margin-confound rule applies: any forgetting or ordering claim must match margin first. A stored-slack claim must also beat **computed slack**, meaning the margin divided by the model's own sensitivity (one forward and one backward pass), at equal serving cost.
- **Slack is identifiable only near thresholds.** Parent's crossed evidence identifies *whether* an edge exists. Slack needs the *location* of the boundary, which requires examples on both sides of each threshold and close to it (at least two bracketing values per edge, more for non-monotone procedures). Far-from-boundary crossings teach the edge but not its slack.
- **With several facts, slack is a region, not a number.** For "sum of tolls ≤ budget", the answer is safe anywhere in a polytope of fact values. A per-edge scalar is an axis-aligned box inside it, so splitting slack per edge is conservative and needs an allocation rule. Escrow transactions ([O'Neil 1986](https://dl.acm.org/doi/10.1145/7239.7265)) and the demarcation protocol ([Barbará & Garcia-Molina 1992](https://link.springer.com/chapter/10.1007/BFb0032439)) do this for distributed constraints. Safe regions for continuous queries over moving objects are the geometric version.

## What to count, and what would settle it

- **Inherit the parent's world and bill.** Toll world with arbitrary entity IDs, numeric facts and procedures (thresholds, sums, exceptions) executed outside the learner. The true graph `G*` and every edge's threshold are declared before training. The full `(C, D)` ledger from [PR #144](future-edit-cost.md) applies, plus the parent's invalidation precision and recall, scored separately on sub-threshold and crossing steps.
- **Score slack directly.** Report the signed slack error in fact units per edge, split three ways: false-safe (stored slack larger than true, which leads to a missed flip and a stale answer), false-alarm (smaller than true, which leads to an early write, a cost) and missing edge (slack ∞ where the true slack is finite). Report the write count per unit of tracked drift and the number of writes per boundary crossing (the ideal is one).
- **Streams that separate moves from crossings.** Runs of 3–20 small moves that flip nothing, then one move that crosses some consumers' boundaries and not others'. Include paths with equal endpoints and different histories (#148#9), and jittering facts near a boundary (#148#8).
- **Controls every card must beat.**
  - Computed first-order slack `m/|∂m/∂f|` from the same model.
  - An external slack table at equal bytes (the triage row's control).
  - The parent's true-graph cache with exact thresholds (upper bound).
  - Edit-on-answer-change and mistake-gated learning ([2604.14336](https://arxiv.org/abs/2604.14336)), which update only when an answer is wrong.
  - Write-every-move, and periodic full re-edit to the latest value.
  - #144#16 binding-only tracking (keep the fact current; no slack).
  - Event-driven accumulate-and-release of parameter updates ([EPD 2611.30397](https://arxiv.org/abs/2611.30397)) and error-feedback residual accumulation ([Karimireddy et al. 2019](https://arxiv.org/abs/1901.09847)).
  - [GRACE](https://arxiv.org/abs/2211.11031)'s deferral radius.
  - An external decision ledger with watch conditions ([Fresh at Decision, Stale at Action 2610.18126](https://arxiv.org/abs/2610.18126)), which stores trigger conditions outside the model.
- **Old-task retention in every first test.** A frozen panel of untouched facts, unaffected cached answers, old procedures evaluated closed-book and with oracle premises, and rare old exceptions, checked after every write and every counter update. A new metric joins the panel: **slack retention**, the stored-slack error on untouched edges after unrelated training (cards 12 and 13).

**Ledger and triage screen.** Read the [idea ledger](https://github.com/manojbajaj95/cl/blob/dfb4d52e8e2ef4938bc1e578baa9a04c8d98cad5/reviews/idea-ledger.md) first. Not revived:
- MX2 margin-gated lesson visibility (KILLED: confidence- and margin-gated memory is prior art, TrustMargin 2606.08397). No card here gates visibility on margin. Slack gates *writes* and is denominated in world units.
- Functional syndromes / coded checks (FALSIFIED, PR #24: damage was not sparse). Card 3's triangle check therefore puts its three carriers in different substrates and is scored against a dense control.
- Reverse grokking and cooldown facts (killed by the margin confound). Every forgetting-order claim here is margin-matched.
- MEMIT capacity laws without beating a constant.
- Exact store, replay or restore presented as discoveries.

Neighbours already graded and kept as controls when a card only renames them:
- #148#8 hysteresis bands and #148#9 cumulative-drift probes (triage: controls for #6).
- #148#15 graph-scoped protection.
- #141 delayed-release edits (optimizer-state release schedules).
- top-10 #4 rate–drift law.
- #130 / #132 fossils.
- [CABA 2610.40740](https://arxiv.org/abs/2610.40740) certified held-out anchors.
- [2609.32818](https://arxiv.org/abs/2609.32818) (first-order bound valid only while response drift stays below margin).
- [MaLoRA 2611.14397](https://arxiv.org/abs/2611.14397) (margin view of LoRA forgetting).

## Idea cards

### A. What slack is

#### 1. Slack is the weighted dependency graph

- **Mechanism:** One head outputs, for a cached query and a fact ID, a signed slack in fact units. Slack = ∞ means "no edge" and a finite value means "edge, with this much room". The parent's graph (#148#1–#5) and its slack ledger (#148#6) become one object. Invalidation is `slack ≤ 0` and the edge set is `slack < ∞`.
- **Novelty vs nearest prior art:** Knot ([2605.28047](https://arxiv.org/abs/2605.28047)) estimates dependence on context units without thresholds. LP sensitivity ranging gives exactly this for linear programs. GRACE's radius is in key space, not fact units. **Candidate primitive:** a single learned quantity that both routes invalidation and schedules writes.
- **Cheapest first test:** 64 bridges, 4 procedures, 2-layer MLP plus a slack head, trained on boundary-bracketing examples. Compare invalidation precision/recall and slack error against the parent's binary dependency head plus computed slack, at equal parameters.
- **Old-task retention check:** The slack head's auxiliary loss must not lower closed-book accuracy on rare exceptions or untouched facts.

#### 2. Stored versus computed slack: when does storing win?

- **Mechanism:** Computed slack is `m/|∂m/∂f|` from the current model. Stored slack is a head or counter. Storing should win in three cases: (a) a non-linear response, where first order misjudges far boundaries; (b) a fact slot that has not been written since the last moves, where computed slack reads a stale value; (c) a damaged fact slot or procedure, where computing from them inherits the damage.
- **Novelty vs nearest prior art:** First-order response models ([2609.32818](https://arxiv.org/abs/2609.32818)) and certified radii (randomized smoothing, [Cohen et al. 2019](https://arxiv.org/abs/1902.02918)) compute room-to-flip on demand. **Audit**, and the required gate for every card below: if computed slack ties, slack is a derived quantity and not a memory object.
- **Cheapest first test:** On the three regimes (linear threshold, non-linear sum-with-exception, stale fact slot), report false-safe and false-alarm rates for stored versus computed slack at equal serving FLOPs.
- **Old-task retention check:** After unrelated fine-tuning, compare how far each slack estimate degrades on untouched edges.

#### 3. The slack triangle: value, threshold and slack check each other

- **Mechanism:** Three carriers in different substrates: the fact value (fact slot), the threshold (procedure weights) and the slack (a counter or head). They must satisfy `slack = threshold − value`. A violation localizes which carrier drifted, by 2-of-3 agreement across many edges that share the fact or the procedure. The result is a label-free forgetting detector for facts versus skills.
- **Novelty vs nearest prior art:** This is a redundant code, so the PR #24 kill applies directly: coded checks failed there because damage was dense. **Candidate primitive** only if the substrates fail independently. That is the claim under test.
- **Cheapest first test:** Damage one carrier at a time (fine-tune the procedure on an unrelated task; perturb fact slots; perturb counters). Score localization accuracy against a dense random-projection sketch at equal bytes and against [#126](https://github.com/manojbajaj95/cl/pull/126)'s labelled canary.
- **Old-task retention check:** Repairs triggered by the check must not damage the carriers it judged healthy.

#### 4. Escrowed slack for answers that read several facts

- **Mechanism:** For "sum of tolls on the route ≤ budget", learn an allocation of the joint slack polytope to per-edge budgets, so each fact can drift within its share with no coordination. Re-allocate when one share runs out and others have room, as the demarcation protocol does.
- **Novelty vs nearest prior art:** Escrow and demarcation (O'Neil 1986; Barbará & Garcia-Molina 1992) and adaptive precision filters for replicated aggregates ([Olston & Widom 2000](https://dl.acm.org/doi/10.5555/645926.671877)) are classical, with hand-set allocations. **Candidate primitive:** an allocation learned from each fact's drift statistics and stored with the answer.
- **Cheapest first test:** Route answers over 2–5 bridges with heterogeneous drift rates. Compare learned allocation to equal split, to a joint polytope check (exact; priced in reads) and to computed slack. Score writes per crossing and false-safe rate.
- **Old-task retention check:** Re-allocation events must not change any answer; check single-fact consumers of the same bridges.

#### 5. Evidential slack for categorical beliefs

- **Mechanism:** For non-numeric facts (who runs the bridge), slack means the number of contradicting observations before the belief should flip. The model keeps per-belief pseudo-counts and flips only when contrary evidence exceeds them. It also stores how many confirmations remain before a dependent answer would flip.
- **Novelty vs nearest prior art:** Beta/Dirichlet pseudo-counts and Bayesian belief revision are classical. Time-sensitive editing ([2406.04496](https://arxiv.org/abs/2406.04496)) replaces values in one shot. **Improvement** unless evidence counts persist in weights through unrelated training. Card 13 tests that.
- **Cheapest first test:** Streams of noisy contradicting reports. Compare count-gated flipping against flip-on-latest (as editors do), majority over a window, and an external Beta table at equal bytes. Score stale exposure and spurious flips.
- **Old-task retention check:** Beliefs never contradicted must keep both their value and their counts.

#### 6. Can an LLM say its own slack?

- **Mechanism:** Ask a small LM "how much can the toll rise before your answer changes?". Compare the verbalized slack with the slack found by intervening on the prompt (bisection on the fact value in context) and with the executor's slack. Then fine-tune for agreement between the verbalized and intervened slack, so self-reports can drive the write schedule.
- **Novelty vs nearest prior art:** Introspection on learned behaviours ([2410.13787](https://arxiv.org/abs/2410.13787)) and verbalized confidence calibration concern confidence, not room-to-flip in world units. **Candidate primitive** if verbalized slack is faithful enough to schedule edits.
- **Cheapest first test:** Qwen2.5-0.5B on CPU, inference only, 300 synthetic threshold questions. Report rank correlation and signed error of verbalized versus intervened slack, against a constant and a margin-only predictor.
- **Old-task retention check:** If the agreement fine-tune is run, check general instruction following and untouched-fact recall on a fixed held-out set.

### B. Counting down: the write schedule

#### 7. Write on crossing only: a fact-level trigger read from stored slack

- **Mechanism:** Keep one external accumulator `D_f` per fact and a learned trigger level `s_min(f)`, the smallest dependent slack. Write to the weights only when `|D_f| ≥ s_min(f)`, then reset. Between writes the served model is exactly unchanged, and direct recall of the fact is answered from model plus accumulator. This is #148#7 developed against its nearest neighbours.
- **Novelty vs nearest prior art:** EPD (2611.30397) accumulates *optimizer* updates and releases them on a coordinate budget. Mistake gating (2604.14336) updates only on errors. Sigma-delta coding releases on fixed levels. **Candidate primitive:** the release level is a per-fact *behavioural* threshold reported by the model, so writes track answer flips rather than gradient size.
- **Cheapest first test:** 200-event drift streams. Count weight writes and cumulative old-panel damage against write-every-move, edit-on-flip, mistake gating, EPD with a matched release rate and an external slack table. Require equal current fact recall at every step.
- **Old-task retention check:** The main claim is that damage scales with the number of crossings, not the number of moves. Plot old-panel damage against each count separately.

#### 8. Where the counter lives

- **Mechanism:** Run the same countdown in three substrates: (a) an external scalar per edge or fact; (b) a dedicated low-rank adapter that only counters write to; (c) a recurrent or KV state carried across queries. Measure the interference each counter decrement causes. Only (a) is free. Whether (b) or (c) stays interference-free decides whether slack can live "inside" the model.
- **Novelty vs nearest prior art:** Sparse memory fine-tuning ([2510.15103](https://arxiv.org/abs/2510.15103)) isolates writes to memory slots. Fast weights and test-time memory hold state between steps. **Audit** of the root cause's second point; it decides how cards 7, 9 and 11 are billed.
- **Cheapest first test:** Equal stream and slack accuracy in all three substrates. Report answer changes caused by counter updates alone (should be zero), bytes, and slack error after 1,000 decrements.
- **Old-task retention check:** Counter updates must not move any old-panel answer. Count every such change as damage.

#### 9. Local writes: change only the consumers that cross

- **Mechanism:** When a move crosses some consumers' boundaries and not others', the editor can rewrite the fact (all consumers move through the graph) or write only the crossing consumers' answers and leave the fact slot to the accumulator. Slack tells which consumers cross. Compare the collateral of the two options.
- **Novelty vs nearest prior art:** The parent's one-write broadcast (#148#10) is the fact-write option. Answer-level patching is what GRACE and WISE ([2405.14768](https://arxiv.org/abs/2405.14768)) do. **Improvement** unless slack makes the choice better than a fixed policy.
- **Cheapest first test:** On mixed crossings, score `(C, D)` for fact write, answer write and a slack-chosen mixture. Score future edits too: answer-only writes leave the fact stale for later consumers.
- **Old-task retention check:** Non-crossing consumers of the same fact must keep both their answer and their slack.

#### 10. Re-anchoring slack after a write

- **Mechanism:** After a crossing write, every dependent's slack must be reset against the new value: the crossed ones get new slack on the other side, the others lose what was used. A recompute is exact but costly. A lazy refresh updates slack only when queried or near zero. Learn which dependents need eager refresh.
- **Novelty vs nearest prior art:** Self-adjusting computation ([Acar 2005](https://www.cs.cmu.edu/~rwh/students/acar.pdf)) and Adapton propagate changes lazily through a dependency graph. **Improvement** as a scheduler, required for any long-stream claim.
- **Cheapest first test:** Long streams with repeated crossings. Measure slack error growth over successive writes for eager, lazy and learned refresh at equal refresh budget.
- **Old-task retention check:** Refresh operations must change no answer.

#### 11. Learned expiry: slack divided by drift rate

- **Mechanism:** For facts that drift at a roughly steady rate, slack converts to a time-to-flip, so a cached answer carries an expiry date. Serve until expiry, recheck the fact at expiry, and write only if it really crossed.
- **Novelty vs nearest prior art:** Leases ([Gray & Cheriton 1989](https://dl.acm.org/doi/10.1145/74851.74870)) and TTL caches use fixed or per-object times. The decision ledger's freshness ceiling (2610.18126) bounds validity by the execution gap. **Improvement** unless the expiry comes from the model's own slack and rate estimates and beats fixed TTLs at equal rechecks.
- **Cheapest first test:** Facts with mixed drift rates. Compare learned expiry to the best fixed TTL, to per-fact TTL by rate only, and to the accumulator of card 7. Score stale exposure against recheck count.
- **Old-task retention check:** Never-drifting facts must get long expiries and keep their answers.

### C. Slack and forgetting

#### 12. Slack erosion as latent forgetting

- **Mechanism:** Unrelated training can shrink an old answer's slack while its accuracy stays at 100%. The answer is still right but will now flip under a smaller fact move or a smaller later update. Track slack retention on old edges as a forgetting metric that accuracy cannot see, and test whether erosion predicts which old answers break under the next small edit.
- **Novelty vs nearest prior art:** MaLoRA (2611.14397) and the margin literature track logit margins. Forgetting events ([Toneva et al. 2018](https://arxiv.org/abs/1812.05159)) count flips. **Candidate primitive:** erosion measured in world units, which compares across models and procedures, unlike a logit margin. The ledger's margin-confound rule makes margin-matched prediction the bar.
- **Cheapest first test:** Train task A in the toll world, then B. Measure slack retention and logit-margin retention on A's edges. Predict which A answers flip under a later small fact move. Must beat logit margin, margin over weight norm and computed slack at matched margin.
- **Old-task retention check:** This card's metric *is* a retention metric. Also report ordinary A accuracy to show the two diverge.

#### 13. Stale slack: forgetting the slack itself

- **Mechanism:** The slack store can be forgotten while answers and facts survive. False-safe stale slack misses a flip and serves a stale answer. False-alarm stale slack causes a needless write. Measure both under unrelated training and test whether replaying a few slack labels keeps them current.
- **Novelty vs nearest prior art:** No editor stores slack, so its decay is unmeasured. Wrong-wake fixed points ([PR #146](https://github.com/manojbajaj95/cl/pull/146)) shows that state which looks healthy can be wrong. **Audit**: a new failure mode that any slack-storing system must report.
- **Cheapest first test:** After B training, measure slack error on A's edges for each counter substrate (card 8) and the slack head (card 1). Compare slack-label replay against plain answer replay at equal tokens.
- **Old-task retention check:** Slack error on untouched edges is the metric. Answer accuracy is reported alongside.

#### 14. A free forgetting budget: store facts only as precisely as their consumers need

- **Mechanism:** A fact whose smallest dependent slack is €6 can be stored to ±€3 with no behavioural cost, as long as direct recall is not itself a consumer. Allocate fact-slot precision (quantization bits, rank, or slot sharing) by min-slack, and reclaim the rest for new tasks. Forgetting below slack is invisible by construction. Forgetting above it is real.
- **Novelty vs nearest prior art:** Mixed-precision quantization uses sensitivity, and rate–distortion allocation is classical. Adaptive weight decay for controlled forgetting ([2604.27063](https://arxiv.org/abs/2604.27063)) frees capacity by decay. **Candidate primitive:** a per-fact forgetting allowance in world units, derived from what the fact's consumers can tolerate.
- **Cheapest first test:** Fixed capacity. Compress fact slots by min-slack against uniform compression and Fisher-sensitivity compression at equal bytes. Score new-task capacity gained and old answers flipped.
- **Old-task retention check:** Direct-recall queries for each fact are scored separately and charged as a consumer whose slack is the recall tolerance.

#### 15. Slack-triggered replay for old tasks

- **Mechanism:** Move slack into weight space. For each old item, keep a budget of how far new-task updates can move it before it flips (from first-order response, refreshed periodically), and count it down during B training. Replay an item only when its budget nears zero.
- **Novelty vs nearest prior art:** Maximally interfered retrieval ([MIR 1908.04742](https://arxiv.org/abs/1908.04742)) picks replay by predicted loss increase. GEM constrains loss increase. Mistake gating replays errors. **Improvement** unless the countdown beats MIR and loss-threshold replay at equal replay budget, in particular by catching items before they flip.
- **Cheapest first test:** Two-task toll world plus a split-MNIST sanity check, MLP. Compare slack-triggered replay against MIR, random replay, replay-on-error and loss-threshold replay at equal replays and equal B progress.
- **Old-task retention check:** A accuracy and A slack retention (card 12). Also check an untouched third task C.

#### 16. Protect old answers up to a slack floor, not exactly

- **Mechanism:** EWC, LwF and GPM pin old behaviour as closely as possible. A slack floor lets B move A's outputs freely as long as each A answer keeps at least a floor of slack in fact units. A one-sided hinge replaces a two-sided pin, which should leave B more plasticity.
- **Novelty vs nearest prior art:** Margin-preserving distillation and GEM's one-sided constraint already exist. Parent #148#15 scopes protection by read set. **Improvement**: the new part is the floor's unit (world units, comparable across tasks), and it needs a large effect to pass.
- **Cheapest first test:** At equal A retention, measure B gain for the slack floor, a logit-margin floor, LwF, EWC and GPM.
- **Old-task retention check:** A accuracy plus slack after a later small fact move. A floor that keeps accuracy but loses room fails here.

#### 17. Unlearning as slack surgery, and fossils as infinite slack

- **Mechanism:** Forgetting a fact can set its consumers' slack to ∞, which detaches them and leaves them frozen. It can also hand them to a reader. Conversely, a cached answer whose stored or computed slack is ∞ on an edge the world says is finite is a fossil: it memorized its answer and will never update. Slack exposes fossils without labels on the new world.
- **Novelty vs nearest prior art:** Deep unlearning ([2410.15153](https://arxiv.org/abs/2410.15153)) severs paths. The fossil-beliefs node ([PR #132](https://github.com/manojbajaj95/cl/pull/132)) uses disagreement-gated KD. **Candidate primitive:** fossil detection as an ∞-slack audit on declared edges.
- **Cheapest first test:** Mix memorized and reading consumers (crossed-evidence data, [PR #143](crossed-evidence.md)). Score fossil detection by ∞ slack against disagreement-gated KD and an intervention bisection audit at equal queries.
- **Old-task retention check:** Reading consumers must keep finite slack and correct answers after the audit.

### D. Slack as a portable object

#### 18. Slack as a base-invariant contract

- **Mechanism:** Logit margins live in a model's coordinates. Slack in euros does not. Hand a new base the old model's answers plus slack and train it to match both. The result inherits not only what the old model says but how far each answer can move. That is a model-independent description of commitments.
- **Novelty vs nearest prior art:** Cross-generation inheritance ([PR #130](https://github.com/manojbajaj95/cl/pull/130)), TuneShift-KD ([2603.24518](https://arxiv.org/abs/2603.24518)) and proxy-tuning transfer outputs or deltas. **Candidate primitive:** a transfer target with units, testable for whether inherited slack is right in the new base.
- **Cheapest first test:** Two MLP bases of different widths. Distil answers only against answers plus slack at equal tokens. Score crossing-step correctness on a later drift stream in the new base.
- **Old-task retention check:** The new base's own untouched tasks and the inherited untouched facts.

#### 19. Let slack decide what to memorize and what to read

- **Mechanism:** Answers with large slack can be compiled to constants, so they need no fact read. Answers with small slack stay on the reader path. The memorize-or-read boundary moves as slack moves, and capacity follows how close answers are to their boundaries rather than traffic alone.
- **Novelty vs nearest prior art:** Parent #148#21 sets a two-level cache by traffic. #148#8 marks near-boundary answers. FinCacheServe ([2607.26076](https://arxiv.org/abs/2607.26076)) uses explicit dependencies. **Improvement** unless slack-sized compilation beats a traffic-sized boundary at equal bytes.
- **Cheapest first test:** Fixed capacity, drift streams. Compare slack-chosen, traffic-chosen and random boundaries on `(C, D)`.
- **Old-task retention check:** Demoted answers must stay correct through the reader. Promoted ones must still flip on a large move.

#### 20. Slack through multi-hop answers

- **Mechanism:** If answer b reads answer a, which reads fact f, then b's slack on f composes: by min for threshold chains, by a chain rule for smooth links. Store composed slack for cached multi-hop answers and test whether composing stored slack beats measuring it end to end.
- **Novelty vs nearest prior art:** MQuAKE ([2305.14795](https://arxiv.org/abs/2305.14795)) and RippleEdits test propagation, not room-to-flip. Interval arithmetic composes bounds. **Candidate primitive** if composed slack stays calibrated on long chains.
- **Cheapest first test:** Chains of 2–4 hops. Report composed against measured slack error by depth, and crossing correctness on the last hop.
- **Old-task retention check:** Single-hop answers that share the intermediate facts.

### E. Learning and checking slack

#### 21. Self-measured slack, distilled into a head

- **Mechanism:** Label slack without an executor. Bisect the fact slot's value by intervention until the model's own answer flips, then distil those slacks into a cheap head. The head is the model's account of its own boundaries. Faithfulness to later interventions is the test.
- **Novelty vs nearest prior art:** Interchange interventions (IIT [2112.00826](https://arxiv.org/abs/2112.00826)) align with a known causal model. Here the target is the model's own boundary, which may be wrong about the world. **Candidate primitive** for label-free slack, which separates "the model is wrong" from "the head misreports the model".
- **Cheapest first test:** Compare a self-measured head, an executor-labelled head and computed slack on (a) faithfulness to the model and (b) correctness about the world, after edits.
- **Old-task retention check:** Bisection runs on copies. Confirm the served model is untouched.

#### 22. Boundary-bracketing data: what slack supervision costs

- **Mechanism:** By the root cause, slack needs examples bracketing each threshold. Find how many per edge (teaching dimension for threshold location) and whether a schema-level threshold rule (all bridges: limit minus weight) lets slack generalize to bridges never seen near their boundary.
- **Novelty vs nearest prior art:** Active threshold learning by bisection and teaching dimension (Goldman–Kearns) are classical. Parent #148#19 tests schema transfer of edges. **Audit**, setting the supervision bill for every card.
- **Cheapest first test:** Vary bracketing examples per edge (0, 2, 4, 8). Hold out 25% of bridges from boundary data. Report slack error on held-out bridges.
- **Old-task retention check:** Extra boundary data must not displace rare exceptions at equal tokens.

#### 23. Slack is an attack surface; certify it

- **Mechanism:** Stored slack tells an attacker the cheapest fact edit that flips each answer. Measure the reduction in attack cost from exposing slack. Bound false-safe slack with a randomized audit: perturb facts by the stored slack plus ε and count answers that fail to flip. A Clopper–Pearson bound on that rate is the certificate, priced in `C`.
- **Novelty vs nearest prior art:** Certified robustness radii and #148#18's completeness certificate for edges. **Audit**: the gate for any card claiming exact flips.
- **Cheapest first test:** Plant known slack errors at controlled rates. Check that the bound covers them and that the audit cost scales as predicted.
- **Old-task retention check:** Audits run on copies only.

## Is slack a new memory object, and what does it do for forgetting?

**As a quantity, no.** Room-to-flip is margin divided by sensitivity (card 2), a certified radius, an LP sensitivity range, an escrow balance, a safe region, GRACE's radius or a decision ledger's watch condition. All of these exist, and all are either computed on demand or kept outside the model.

**As a continual-learning memory object, possibly, in three specific ways.** These are the claims to test, not established results.
1. **It has world units.** Slack in euros compares across models, procedures and bases (cards 12 and 18). A logit margin does not.
2. **It separates "still right" from "still live".** An answer can be correct with zero room (fragile), or correct with ∞ room on an edge that should be finite (a fossil). Neither shows in accuracy (cards 12 and 17).
3. **It schedules writes by behavioural consequence.** Writes happen when an answer must change, not when a fact changes or a gradient is large (card 7).

The object is new only if stored slack beats computed slack (card 2) and an external slack table at equal bytes (cards 7 and 8). Otherwise it is a cache over a reader.

**What it would do for forgetting.**
- Weight writes, and so interference, would scale with boundary crossings instead of with moves (cards 7 and 15).
- A latent forgetting signal becomes visible before accuracy falls: slack erosion (card 12), along with a new failure mode, stale slack (card 13).
- Forgetting below slack is free, which gives a principled capacity reclaim (card 14).
- Fossils become detectable as infinite slack (card 17).

The main risk is the root cause's second point. If counters must live in shared weights, every countdown step is a write, and the forgetting benefit is lost.

## Ranked deeper questions

1. **Is stored slack a memory object at all?** Does it beat computed slack `m/|∂m/∂f|` and an external slack table at equal bytes, on crossing-step correctness with zero intermediate answer changes, and in which substrate? Cards 2, 7 and 8 on the toll world, with linear, non-linear and stale-slot regimes. If computed slack ties in all three regimes, slack is derived and the node closes as a negative result.
2. **Does slack-gated writing make forgetting scale with crossings rather than moves?** Card 7 against write-every-move, edit-on-flip, mistake gating and EPD at equal current fact recall, with old-panel damage plotted against crossings and against moves. Card 15 is the weight-space version for ordinary task sequences.
3. **Is slack erosion a latent forgetting that accuracy and margin miss?** Card 12: after B training, does A's slack retention predict which A answers break under a later small move, beyond logit margin at matched margin (ledger rule)? A yes adds a retention metric every continual-learning paper could report. Card 13 asks whether the slack store itself survives.
4. **Does slack give a free forgetting budget?** Card 14: at fixed capacity, does min-slack precision allocation reclaim more new-task capacity than Fisher-sensitivity allocation at zero answer flips?
5. **Does slack transfer across bases in world units?** Card 18: does answers-plus-slack distillation give correct crossing behaviour in a new base where answers-only distillation does not?
