# Evolving Representations 4: Retire in Three Phases, Reuse What Survives

Child of [evolving-representations-3.md](evolving-representations-3.md) (depth 3) · 26 cards (19 candidate primitives, 2 improvements, 5 audits) · 4 ranked deeper questions · Ideas only; no GPU or experiments run

**Why this node exists.** The reviewer of [PR #330](https://github.com/manojbajaj95/cl/pull/330) promoted exactly two cards to score 3 ([flood triage, row 448][triage]):

1. **ER3-19 · Expand / dual-read / contract.** Install the fiber while the token still exists; compare the old and prospective reader paths on the retirement receipt; delete the token only after agreement. The reviewer requires retire-then-fiber, keeping the token, ER3-21's edit-order comparison, equal-step one-shot distillation, and a cue the replacement cannot reconstruct by its deadline.
2. **ER3-22 · Reuse a retired distinction in C.** A new action reads the existing fiber rather than relearning the cue from bytes. The reviewer requires equal-example byte learning, ER3-27's equal-bit Gray–Wyner private branch, restoring the token, a new action that needs a *slightly different* distinction, and rechecking act_3 after act_4 trains.

**Thesis.** A successful migration leaves a new computation, not a compatibility shim. The old token used to supply a distinction at a certain time and under a certain context. Commit should mean that the live computation, not just a clean-start test, can proceed without it. Reuse should mean that the surviving distinction helps a new reader, not that a second reader can call the old tokenizer under another name. These are separate tests: a perfectly adequate act_3 fiber may be deliberately too small for act_4.

**Fixture and common controls.** Extend the parent's F-dual: fit A over bytes with canonical token `ab`, text and act_1–3; propose the retirement in B; then train act_4 in C without a task-ID input to the model. Cross three cue classes: byte-recoverable by the read deadline; recoverable exactly one byte *after* it; and two identical full byte strings with a distinct exogenous fixture label (the byte path cannot recover it at any delay). Any separate producer for the last class is an explicit, charged input, never the old token under a new name. In C use both a same-cue action with a **different** payoff/readout and a near-cue action requiring an additional distinction (e.g. split one of the two cue classes by a suffix bit); hold out strings and break spurious cue correlations. Supply no oracle cue name to a learned route. Use enumerated traces as feasibility or negative controls; advance a surviving mechanism to a tiny CPU GRU with decoy fibers/edits before treating it as learnable.

- **Migration stack M (all A/C cards):** retire-then-fiber; keep the token; ER3-21 quotient-first vs fiber-first at matched schedules; one-shot cross-tokenizer distillation at equal updates and teacher calls; a deadline-impossible cue; and plain ER3-19 receipt agreement as the incumbent. An old path serving during overlap is allowed and charged; after contract remove input/output rows, re-encoding dependencies, old state reachable by live readers, and any teacher call. Pre-contract abort is permitted; post-contract restore is a control, not a candidate.
- **Reuse stack R (all B/C cards):** equal-example act_4 from bytes (matched head/search budget); ER3-27's equal-bit Gray–Wyner common/private codec with an act_4 readout on its private branch; restore/keep `ab`; direct frozen ER3-22 sharing; and the near-cue negative. Include an existing-module readout as a transfer baseline, not just random initialization. Joint cards must beat the strongest parts **stacked** (including M's best migration followed by R's best reuse).
- **Accounting and gates:** Report peak overlap bytes and compute, examples, teacher evaluations, steady-state bits and work, commit/abort rate, and steps/examples to 95% act_4 on balanced held-out data (report misses as misses). A receipted agreement is between *deadline-matched* outputs, including STOP/abstention; never compare different byte prefixes or let the candidate see the old-token path at training/evaluation of the new path except as supervision. Report actual served retention **and** candidate-only retention: per-family action accuracy/deadline misses and byte NLL/STOP during expand, dual-read, immediately after contract or abort, and after C. Report the worst transition window, not only steady state. Match old behavior exactly on deterministic fixtures; set tolerances before fitting a neural variant. An arm that always aborts does not get credit for safe retirement.
- **Inherited limits:** ER2-23's trained parse-pair equivalence check still gates every destructive text rewrite; on failure restrict to a demonstrated lawful subdomain or stop, not just distill harder and assume equivalence. Endpoint-respecting partition refinement is the exact baseline, not a discovery ([2608.06386][endpoint]). [The ledger][ledger] rules out save/restore, append-and-retrieve, and true-by-construction claims. Its read-pinning failure (PR #117) specifically warns that matching an internal interface can leave consumer behavior worse. Task retention is mandatory. Migration patterns are prior art in their own right. AUDIT cards establish a bound or diagnose a confound; IMPROVEMENT cards are controls/designs, not pilot nominations.

**Literature check.** Checked publisher/arXiv records and abstracts, and accessible method passages for the closest cross-field work (consistent updates, Taskonomy, stitching, causal abstraction and Jacobian matching). Each card names the point of contact and the narrower claim to test; absence of that claim from a comparator is not a priority claim. In particular, [Parallel Change][parallel] already supplies expand/migrate/contract; [Reitblatt et al.][updates] already supply per-flow migration consistency; [Kitsune][kitsune] already transforms live state. [ESCD][escd] supervises cross-tokenizer completion sets, while [DVLM][dvlm] constructs teacher supervision in the student's vocabulary. Neither is a straw-man token-index KL baseline. [Output-decomposed Mealy learning][mealy] and [Gray–Wyner][gw] already supply output projections and common/private coding. [Same Bytes, Different Authority][authority] and [Nameless Tokenization][nameless] establish why reserved-ID provenance must not be treated as recoverable from surface bytes.

## A · ER3-19: What qualifies a migration to contract?

### ER4-01 · Hand off a live reader at a regenerating prefix — PRIMITIVE
- **Mechanism:** Compile a bounded set of byte-prefix states where the new reader can reconstruct its live state from the current prefix state and the fiber alone. Switch an in-flight trace at the first such state; if no switch occurs by the overlap deadline, abort. Do not drain the request or reread consumed bytes.
- **Novelty vs nearest prior art:** [Kitsune][kitsune] supplies state transformers and [consistent updates][updates] already version whole flows. The hypothesis is that *learned synchronizing prefixes* offer a better overlap/deletion tradeoff than a general map or flow draining when token histories differ.
- **Cheapest first test:** Interleave eight short streams, half with an early reset symbol and half with delayed reset; add a misleading symbol with the same next-byte law but different future act_3. Compare explicit state map and per-flow drain plus M; kill if neither the cost nor the retirement deadline improves at equal exact trace agreement.
- **Old-task retention:** Check pending act_3 responses at every handoff position, then old-text prefix mass/STOP in both reset strata throughout and after C.

### ER4-02 · Contract against a distribution of finishing times — PRIMITIVE
- **Mechanism:** For each unresolved old-token event, the receipt compares remaining byte completions and the first time each completion can support the old decision. Train the fiber on this joint event, not just on eventual act_3. A migrate step is inadmissible if it moves a required decision later than its deadline.
- **Novelty vs nearest prior art:** [ESCD (2609.34738)][escd] already learns aggregate probability over completion sets. Gap: a joint completion-time/reader law for destructive cutover, where two paths can have equal completion mass yet disagree in time to act.
- **Cheapest first test:** Use an automaton with tied ending mass for `ab` and `aba` but unequal time to identify the event; distill two tiny readers with ESCD-style mass alone vs mass and deadlines. Kill if the latter adds no deadline-safe commits at the same overlap cost, or commits the impossible-delay control.
- **Old-task retention:** Score correct-and-on-time act_3 and STOP at each byte offset, including unfinished old inputs at cutover and after C.

### ER4-03 · Learn from the first disagreement on self-generated prefixes — PRIMITIVE
- **Mechanism:** During overlap, run the candidate closed loop in a sandbox. At its first departure from the old action trace, query the old path at the matched raw observation/history and distill there before resuming. Use separate episodes to decide commit; teacher-forced agreement alone cannot approve it.
- **Novelty vs nearest prior art:** [DAgger (1011.0686)][dagger] queries on learner-induced states, and [ESCD][escd] already uses student-generated paths. Neither difference alone is new; test whether reconstructing a *first divergent prefix of a changed tokenizer and stateful reader* is a more sample-efficient deletion operator than ordinary aggregation at equal queries.
- **Cheapest first test:** Add a branch reached only after a premature act_3. Compare against uniform DAgger-style querying and M; kill if the branch is not reachable from the candidate or first-divergence querying fails to improve commits at equal closed-loop retention.
- **Old-task retention:** Evaluate independent free-running traces, not only shared teacher prefixes: first act_3 failure, later act_1/2 and old-text bits/byte across phases.

### ER4-04 · Make the new path survive a hard dependency blackout — AUDIT
- **Mechanism:** Before irreversible deletion, run the prospective model in a namespace that cannot dereference old token rows, cached token-aligned states or the old event producer. Differentially reset each dependency when testing ordinary shadow agreement to identify which dependencies made that agreement misleading.
- **Novelty vs nearest prior art:** [DVLM (2609.33816)][dvlm] deliberately feeds parallel tokenized sequences to its teacher. [Translation Validation][validation] checks each translated artifact separately. Here the compiled successor is the artifact, and the fault is shadow agreement *through prohibited dependencies*, not a mismatch between vocabularies.
- **Cheapest first test:** Seed a student that reads a cached old-state feature through a shared encoder, and an independently computed fiber. Compare live shadow, clean-start deletion and in-flight blackout. Kill the audit's value claim if clean-start already finds every contaminated path at the same trace budget.
- **Old-task retention:** Recheck split and unsplit old-text cases and act_3 when the cache starts hot, when it starts cold, and after the next C update.

### ER4-05 · Use different stopping rules for different reader failures — IMPROVEMENT
- **Mechanism:** At frozen-candidate checkpoints, evaluate separate paired disagreement bounds for frequent reads, rare late reads and impossible cues. Allocate additional shadow queries to the largest unresolved bound; use disjoint audit streams or an explicit error budget across candidate changes. Missing strata block commit, not count as zeros.
- **Novelty vs nearest prior art:** [Confidence sequences (1810.08240)][howard] already support repeated peeking under their assumptions. The proposed gain is narrower: short overlap at fixed false-commit rate when receipts separate qualitatively different failure mechanisms, rather than one bound on aggregate disagreement.
- **Cheapest first test:** Simulate a 1% tail stratum with identical aggregate error in two placements. Match queries against a pooled time-uniform bound and fixed stratified samples; kill if adaptive allocation does not shorten safe overlap at matched false-commit rate. Do not certify out-of-support traffic.
- **Old-task retention:** Measure served and candidate act_3 separately in each stratum; measure old-text loss on both the common and tail populations through C.

### ER4-06 · A progress-preserving abort that discards the failed fiber — PRIMITIVE
- **Mechanism:** In expand, route learning on the still-served old model through edits that are legal on both paths; keep candidate-only edits separate. On abort drop the candidate edits but retain the overlapping legitimate old-model learning. Represent updates at the byte-event level so the old and new model need not share parameter coordinates.
- **Novelty vs nearest prior art:** [Edit Lenses][lenses] already translate changes between structured representations. The test is whether a **partial** lens over learned updates preserves intervening task learning without retaining a shadow snapshot after commit, rather than whether edits can be translated at all.
- **Cheapest first test:** Put one useful and one conflicting supervised update between expand and a forced abort. Compare discard-all rollback and a simple two-model update during overlap. Kill if the event lens gives no retained B progress at equal compute and A retention; count the overlap's extra writes.
- **Old-task retention:** Evaluate A text/act_3 before and immediately after abort and after resumed learning; B gains do not compensate for an A regression.

### ER4-07 · Counterexamples allocate fibers, not just receipt entries — PRIMITIVE
- **Mechanism:** Find matched new-state prefixes with incompatible old actions. Expand the fiber with the smallest feature that separates them *by the deadline*, or return an infeasibility witness. Repeat for the next receipt violation; parallel counters and decoy features compete under the same bit budget.
- **Novelty vs nearest prior art:** [CEGAR][cegar] already refines a model from counterexamples and [endpoint sufficiency][endpoint] covers exact refinement. The testable addition is allocating *learned reader-local, deadline-feasible* features instead of splitting all consumers' states, especially when examples admit many incorrect refinements.
- **Cheapest first test:** Give a finite prefix family one true resolver, three correlated decoys and a pair with identical available observations. Compare exact refinement with features/time accounted for and blind Gray–Wyner fit; kill if learned counterexamples save no search/bytes under held-out decorrelation.
- **Old-task retention:** Retest all old reader classes, including resolution collisions and ordinary text unaffected by the violating pair, immediately and after C.

### ER4-08 · Compile only the old row's decision effect, not its activation — PRIMITIVE
- **Mechanism:** During dual-read, pair an occurrence's old action margin with the same prefix's prospective margin under interventions on the live fiber. Solve for the smallest cue mapping that preserves the decision effect while allowing old and new hidden activations to differ; then remove the alignment scaffolding too.
- **Novelty vs nearest prior art:** [Model Stitching (2106.07682)][stitch] learns interfaces between frozen network pieces and [Net2Net][net] preserves functions during growth. Gap: learn a disposable bridge that yields a smaller *standalone* reader after deletion, not a stitched composite or hidden activation match.
- **Cheapest first test:** Give a GRU an old hidden nuisance direction correlated with the cue and decorrelate it at test time. Compare equal-rank stitching, output-only distillation, [directional Jacobian matching][jacobian] and M; kill if the bridge offers no matched-bit retention or C advantage once removed.
- **Old-task retention:** Report act_3 accuracy/margins on ordinary and nuisance-flipped held-out inputs, plus old byte NLL at each cutover stage.

### ER4-09 · Search for a witness that a bounded overlap cannot succeed — AUDIT
- **Mechanism:** Build one tree of observable prefixes up to the maximum overlap/read deadline. At leaves, collect the old action distribution, conditional on allowable inputs. If two branches are still observationally identical but require opposite deterministic actions, return the pair and its attainable error floor rather than an endless shadow trial.
- **Novelty vs nearest prior art:** [Endpoint sufficiency][endpoint] already compares enabled, trace and branching equivalence. This is a diagnostic, not a new quotient: it checks whether finite receipt coverage would ever expose a deadline-bound impossibility under the *deployment* information set.
- **Cheapest first test:** Contrast delayed recoverability and same-full-bytes opposite labels, each with a held-out rare arm. Compare byte-next agreement and finite exact reader refinement; kill the audit if ordinary receipt sampling locates the decisive pair as cheaply.
- **Old-task retention:** Verify that any declared-feasible retirement preserves act_3 on both branches and old-text STOP; for an infeasible case verify abort serves old tasks unchanged instead of forcing deletion.

## B · ER3-22: What exactly can a new action reuse?

### ER4-10 · Bind by a causal signature, not the fiber's name — PRIMITIVE
- **Mechanism:** Ask which candidate fiber actually mediates the act_4 decision: swap fiber values between byte-matched or valid paired contexts, and fit a binding from the direction of act_4's measured response. Select among cue, reversed cue and a correlated nuisance without assuming the library names carry meaning.
- **Novelty vs nearest prior art:** [Causal Abstractions (2106.02997)][causal] already use interchange interventions to test an alignment, and [Taskonomy (1804.08328)][taskonomy] learns transfer relations. Test whether intervention signatures can route an *unseen action* to a genuinely retired cue under fewer examples than observational routing.
- **Cheapest first test:** Offer three equal-width fibers, two observationally tied on train and one decoy. Give valid swaps plus equal real labels to both approaches (compare augmented byte learning too); kill if held-out decorrelation shows no C advantage over learned transfer affinity.
- **Old-task retention:** Evaluate old act_3 with interventions off, verify act_1/2 and old-text loss do not depend on new routing, and recheck after act_4 binds.

### ER4-11 · Share the old partition; refine only the unresolved cells — PRIMITIVE
- **Mechanism:** Fit act_4 as a read of the old cue plus a separate, sparse cell-specific refinement on bytes. If the residual requires changing act_3's partition rather than splitting its ambiguity, do not overwrite that fiber; start an independent reader and charge it.
- **Novelty vs nearest prior art:** [Concept Embedding Models (2209.09056)][cem] already let concept channels retain information beyond a binary concept, and [Mealy output decomposition][mealy] handles different projections. Gap: allocate *only the extra distinctions* needed by a later action, without widening or mutating the old channel.
- **Cheapest first test:** Split just one cue cell by a suffix bit; also try a target crossing both old cells. Compare a dense bottleneck with equal bits, independent sparse bytes model and R; kill if an equal-bit residual with no cell structure learns as fast.
- **Old-task retention:** Check act_3 within every refined cell after act_4 trains, plus byte NLL on the reading and nonreading contexts.

### ER4-12 · Treat cue inversion as an addressable reader transform — PRIMITIVE
- **Mechanism:** At binding, infer a local permutation of cue values under a new action's semantics. Store the permutation at the reader, not by changing the shared producer. Test whether factoring reusable correspondences across several new actions beats repeated head fitting.
- **Novelty vs nearest prior art:** [Taskonomy][taskonomy] already fits target readouts, and [model stitching][stitch] supplies simple learnable maps. The narrower hypothesis is that a reusable **cue-value correspondence** tied to the byte intervention survives further producer edits, where a dense fitted readout does not.
- **Cheapest first test:** Give a three-class retired cue to two new readers with different class permutations; re-encode the producer before a third reader. Compare matched tiny linear heads and alignments at equal examples; kill if any gain disappears after matching transform capacity.
- **Old-task retention:** Verify act_3 and earlier new readers after each re-encoding/bind, and text NLL/STOP on old slices.

### ER4-13 · Reuse a cue with a different deadline without duplicating it — PRIMITIVE
- **Mechanism:** Publish an unresolved value and its legal resolution event. Act_3 may wait for resolution while act_4 either waits or chooses an explicitly valid early action based on unresolved status. Never supply late information retroactively to an early reader.
- **Novelty vs nearest prior art:** [Selective Classification (1705.08500)][selective] already trades coverage for risk; [ESCD][escd] already distinguishes entered vs completed events. Gap: one retained producer supports different *action deadlines* while the base has no old-token time step.
- **Cheapest first test:** Use a late-resolution fixture where half of act_4 decisions can be made early independent of the pending bit; on the other half only waiting is legal. Compare independent selective byte readers and a private codec with time as input. Kill if sharing does not lower bits/steps at matched error, delay and abstention cost.
- **Old-task retention:** Check act_3's exact old pickup time and byte STOP; forcing C's early deadline onto act_3 is a failure even if final labels agree.

### ER4-14 · Let context provide half of a reused cue — PRIMITIVE
- **Mechanism:** Reuse the old fiber only when combined with act_4's local context disambiguates the desired action. Fit a small conditional decoder and prohibit copying its context back into the shared producer.
- **Novelty vs nearest prior art:** [Multi-Functional Compression with Side Information][sideinfo] already codes for multiple functions and decoder side information. Test the online benefit of reusing an *existing irreversible retirement code* instead of relearning a statically optimal one or shipping new common bits.
- **Cheapest first test:** Let act_4 need the retired bit XOR a local parity bit; add a missing-context slice. Compare R and the exact side-information coding solution; kill if sequential reuse offers no example/work advantage over re-fit codec at equal rate.
- **Old-task retention:** Measure act_3 after contextual decoder training with both parities and missing context; check old text on all three slices.

### ER4-15 · Freeze cue semantics while changing the writer — PRIMITIVE
- **Mechanism:** Permit act_4 gradients to train a replacement producer during a second expand/dual-read window, but compare it against a small set of **interventional** cue classes used by act_3. Commit the new writer only if those effects persist, then remove the previous fiber writer as well as the already deleted token.
- **Novelty vs nearest prior art:** [Lifelong Learning of Compositional Structures (2007.07732)][lifelong] already separates combining and adapting shared components. Test whether an explicitly retired cue can migrate its writer to a different computation without keeping the old module or hijacking its prior meaning.
- **Cheapest first test:** Bias act_4 labels so fine-tuning drifts a producer on one act_3 class. Compare freezing it, generic module adaptation plus replay at equal bytes, and R. Kill if the writer replacement cannot improve C over freeze without hurting the held-out old class.
- **Old-task retention:** Check act_3 on paired contexts that flip the cue independently of C's labels through both writer versions; remeasure text after the writer is removed.

### ER4-16 · Measure reuse in decision problems, not average features — AUDIT
- **Mechanism:** Estimate the transfer envelope of a retired stochastic cue by finding a small decision problem it cannot support from the available observations. Use the witness to construct near-cue act_4 rather than declaring general reuse from one positive action.
- **Novelty vs nearest prior art:** [Blackwell comparisons][blackwell] already relate stochastic garbling to performance over decision problems. The audit applies this limit under explicit post-retirement context and read deadlines; it does not claim a new sufficiency theorem.
- **Cheapest first test:** Enumerate all binary decisions on a three-state source and fit garbling feasibility with and without context. Compare nearest-neighbor cue accuracy against measured transfer; kill the audit if simple per-cell conflict witnesses give the same predictions on the noisy cases.
- **Old-task retention:** Include act_3 as a guaranteed test case, then repeat it and old-text loss after training the adversarial act_4; a predicted negative transfer is not permission to harm act_3.

### ER4-17 · Charge the reusable distinction against equal-bit adapters — AUDIT
- **Mechanism:** Separate reusable **state** from reusable **parameters**. Cross fiber-state access with an equal-size parameter adapter, including a shuffled-fiber matched-bandwidth arm. Run the same act_4 learning curve in each cell; a gain from parameters alone does not establish retired-cue reuse.
- **Novelty vs nearest prior art:** [Progressive Networks (1606.04671)][progressive] transfer via lateral connections to frozen features; [AdapterFusion (2005.00247)][adapter] combines existing task-specific adapters. These are direct alternatives to the reuse claim, not new primitives.
- **Cheapest first test:** Build two same-size cue readers, one state-dependent and one with only a shared bias useful for C. Kill the cue reuse claim if the adapter-only or shuffled-state arm ties genuine state access at equal bits and examples.
- **Old-task retention:** Measure act_3 before and after granting act_4 the new read connection, and old-text bits/byte after all cells finish C.

### ER4-18 · Bind across repeated retirements without a global feature registry — PRIMITIVE
- **Mechanism:** Two disjoint token retirements produce cue writers that are substitutable only on a common domain. Learn a reader-local dispatch with an explicit undefined case and delete duplicate computation on the overlap, without merging writers on contexts where they disagree.
- **Novelty vs nearest prior art:** [AdapterFusion][adapter] composes existing modules and [output-decomposed Mealy learning][mealy] projects outputs to smaller machines. The contested operation is *partial substitution with deletion* when a second retirement creates another producer for the same reader; weighted routing without removing anything is a control.
- **Cheapest first test:** Use two byte grammars sharing one exact cue domain, plus a false friend in each exclusive domain. Compare routing with both writers, domain-aware parameter sharing and R. Kill if substitution cannot reduce steady-state work versus the strongest sharing baseline at matched exact retention.
- **Old-task retention:** Recheck both old actions in the shared domain and on both false friends through the second deletion and act_4 training; test old-text loss per grammar.

## C · Joint: Design what survives without knowing the next action

### ER4-19 · Spend spare bits on the ambiguity that survives deletion — PRIMITIVE
- **Mechanism:** Among equally adequate act_3 fibers, choose a cue code that retains distinctions which are costly to recover from deployment bytes. Use cheap proxy decisions generated from B (e.g. suffix tests where old-state distinctions still matter), not labels from C. The candidate must stay inside the same fiber budget and delete the old row.
- **Novelty vs nearest prior art:** [Gray–Wyner (2601.21424)][gw] optimizes common/private coding for a known set of tasks, and [Blackwell][blackwell] orders fixed experiments. Gap: select an old-task-safe code before the next action is known, with downstream benefit predicted by residual recoverability from current bytes rather than feature entropy.
- **Cheapest first test:** Construct two one-extra-bit encoders with equal frequency and entropy; one bit is easy to recover, the other needs a long prefix dependency. Hold out C functions of either bit. Compare equal-bit reconstruction and fixed private-feature codecs plus M × R. Kill if the proxy does not predict C's transfer benefit better than simple prevalence or byte prediction.
- **Old-task retention:** Verify old act_3 and old-text STOP across every code, stratified by both extra bits, before deletion and after fitting each held-out C.

### ER4-20 · A retirement gate that checks whether a new reader can learn — PRIMITIVE
- **Mechanism:** While both paths exist, fit disposable readers for a fixed family of cheap B-derived proxy decisions and compare their few-example learning curves. Reject cutovers that preserve act_3 but erase all C-like adaptability relative to a declared target. No learned proxy head survives commit.
- **Novelty vs nearest prior art:** [Fiber Fingerprints (2608.15976)][finger] already expose future-learning inequivalence, and [Taskonomy][taskonomy] measures transfer with fitted heads. The proposed operation makes proxy learning a **destructive commit predicate**; the unresolved question is predictive power on unseen C, not that training responses can differ.
- **Cheapest first test:** On a tiny GRU, fit two equally accurate candidate fibers with similar byte likelihood, then rank them by response of small proxy heads. Compare output-only approval and single-pass [Jacobian matching (1803.00443)][jacobian]; kill if the proxy rule fails to predict held-out act_4 speed or merely approves fewer migrations.
- **Old-task retention:** Score candidate and served act_3/old text through the cutover; after C test whether the rejected and accepted candidates differ in retention as well as learning speed.

### ER4-21 · Commit a reader group on one typed interface, or none — PRIMITIVE
- **Mechanism:** If act_3 and a later reader have live output dependencies, stage a joint interface generation (cue domain, encoding and resolution time). Each reader can have a projected view, but observable traces must never combine inconsistent generations. Cut over when all pending reads can finish or translate, then delete the old generation.
- **Novelty vs nearest prior art:** [RAMP transactions][ramp] supply all-or-none visibility and [consistent updates][updates] supply per-flow consistency. The open delta is whether learning small *reader projections* enables group cutover at lower overlap than globally pinning flows or keeping all historical writers, when the interfaces are changed by learning.
- **Cheapest first test:** Interleave two tiny readers where a silent cue recoding preserves each isolated output with its own decoder but breaks the cross-reader handoff under a mixed generation. Compare generation pinning and global barrier at equal tail latency; kill if exact versioned routing ties the learned projection once all state is charged.
- **Old-task retention:** Check every interleaving's act_3/act_4 handshake and unrelated old actions, with text byte NLL/STOP before, during and after the group commit.

### ER4-22 · Admit a new reader only on the domain where its cue agrees — PRIMITIVE
- **Mechanism:** As a new reader's first consumer migration, shadow its byte learner with a hybrid fiber reader. Learn the domain where both mean the same thing; contract the alternate reader computation only there. Outside that domain the new path keeps a paid byte residual; it never falls back to the deleted token.
- **Novelty vs nearest prior art:** [Selective classification][selective] rejects uncertain examples, and [Taskonomy][taskonomy] finds global transfer edges. Gap: a *destructive domain-specific handoff* where an OOD near-cue case should trigger separate computation, not merely get a low confidence score.
- **Cheapest first test:** Use the same cue on one grammar and flip it on a rare second grammar. Compare learned mixture routing and a selective byte head with no phased deletion. Kill if the capacity-matched mixture makes equivalent safe deletions, or the candidate suppresses the difficult slice via abstention.
- **Old-task retention:** Check act_3 on both grammars before and after activating partial reuse; check text and earlier actions while the new route is in use.

### ER4-23 · Compare receipt signatures across *different* retiring symbols — PRIMITIVE
- **Mechanism:** Use the two old paths as temporary supervision for a single writer only if their reader intervention effects and resolution calendars coincide under a learned correspondence. The different byte surfaces remain distinct for text. A jointly installed feature may be reused by a third action; neither old token survives.
- **Novelty vs nearest prior art:** [Taskonomy][taskonomy] finds joint source sets and [Gray–Wyner][gw] already factors common information. The proposed test asks if agreement *across live retirements* identifies a shared writer when surface similarity or correlation alone predicts the wrong coupling.
- **Cheapest first test:** Retire two unrelated tokens with an identical cue in different scripts; include a near twin whose cue arrives one byte later. Compare independent ER3-19 writers followed by generic codec compression and equal-bit transfer. Kill if simultaneous receipts do not improve held-out C reuse per bit or fail to reject the late twin.
- **Old-task retention:** Check act_3 by token family and timing offset throughout both retirements, and old-text NLL including contexts where the two surfaces must remain distinct.

### ER4-24 · Preserve reusable predictions, not just the presently correct action — PRIMITIVE
- **Mechanism:** For a cue that predicts an upcoming event, contract on a compact discounted or finite-horizon prediction *in addition to* the old decision. A later reader can attach different costs to that prediction. Charge the prediction state against copies of the existing binary fiber.
- **Novelty vs nearest prior art:** [Successor Features (1606.05312)][successor] already separate expected future feature occupancy from reward weights. The narrower question is whether learning this predictive statistic during **alphabet deletion** changes which cue can be preserved and reused at equal bits, relative to exact reduction plus successor features.
- **Cheapest first test:** Give act_3 a myopic decision and act_4 a longer-horizon cost sensitive to two post-cue outcomes. Compare existing binary fiber, static successor features before/after plain migration, and re-learning from bytes; kill if the stacked baseline ties while discarding the original vocabulary.
- **Old-task retention:** Verify old action and STOP by horizon throughout migration and after learning the new cost; actuator accuracy cannot be traded for future reward.

### ER4-25 · Pick retirements whose reuse gain pays for their overlap — IMPROVEMENT
- **Mechanism:** Under a fixed B migration budget, prioritize retirements by expected availability of a reusable cue after safe cutover, less charged overlap and retained state. Predict from B-only proxy readouts and compare at fixed token rows deleted; report C learning for the full eligible pool, not just selected winners.
- **Novelty vs nearest prior art:** [LiteToken (2602.04706)][lite] already detects low-exposure merge residue, and [Taskonomy][taskonomy] optimizes transfer choices under supervision budgets. The gap is a joint schedule score for destructive migrations with future reuse as an empirical—not assumed—credit.
- **Cheapest first test:** Rank six candidate retirements with deliberately crossed exposure, overlap duration and reuse. Compare exposure, expected delete-bytes/overlap, proxy transfer alone, and strongest stacked score. Kill if the joint score does not improve held-out total C examples at fixed number of safe deletions.
- **Old-task retention:** Report each previously served action and old-text bits/byte, including the worst intermediate window and actions untouched by the chosen edits.

### ER4-26 · A lifecycle erase test: portable cue or disguised tokenizer? — AUDIT
- **Mechanism:** At every candidate delete, try to reconstruct the old token trace from the new state, separately on the cue-relevant span and on task-irrelevant parse details. Probe dependency by removing any reconstructive path that act_3 does not need, then retry C. Recovering the specific required bit is not itself leakage; using a complete re-tokenizer or cached teacher as the actual cue writer is a failed deletion.
- **Novelty vs nearest prior art:** [Lossless Vocabulary Reduction (2510.08102)][reduction] induces the reduced distribution from the original model, whereas [Pruned BPE (2608.00837)][pruned] can keep hidden construction nodes. Both are strong controls. The audit asks if the reduction is executable *without* those dependencies and whether the reuse gain persists under that restriction.
- **Cheapest first test:** Compare a true single-bit writer against an equal-output wrapper that rebuilds the whole old segmentation and a budget-matched codec. Decouple the old parse details from the cue; kill the reuse claim if only the wrapper survives after C, and the audit's extra value if dependency blackout alone finds every sham at equal cost.
- **Old-task retention:** Check act_3 and old-text NLL/STOP after each dependency severance and then after act_4 trains; report any erased side signal that silently served another reader.

## Ranked deeper questions

1. **Can a finite overlap authorize irreversible retirement on live traffic?** Start with ER4-01/02/04/09. Seek a learned handoff that beats per-flow draining and equal-step one-shot distillation at the same worst act_3/text dip, and refuses late or unobservable cues. Trace consistency, cue availability and statistical coverage are different conditions; quantify which is binding before increasing overlap or widening the fiber.
2. **What makes the surviving cue transferable rather than a private historical artifact?** Run ER4-10/11/17 against equal-bit Gray–Wyner, adapters and bytes, with same-cue and near-cue C. If a lateral adapter ties, retire the transfer claim. If exact cue reuse helps and near-cue transfer fails cleanly, find the smallest residual or context that makes the boundary predictable.
3. **Can a retirement receipt predict *future* learning without seeing the next task?** Test ER4-19/20 on held-out action families, matching old retention, bits and teacher evaluations. If ties with fixed private coding and output-only receipts persist, certify old behavior only; do not charge speculative reuse as a benefit.
4. **Can the system keep deleting infrastructure after the first successful reuse?** Combine ER4-15/21/23/26: change the writer or retire a second token while several dependent readers are live, then verify the old writer and token are genuinely gone. Compare against stacked migration and static routing, not against a brittle unversioned system.

[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L448
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[parallel]: https://martinfowler.com/bliki/ParallelChange.html
[updates]: https://doi.org/10.1145/2342356.2342427
[kitsune]: https://doi.org/10.1145/2629460
[validation]: https://dl.acm.org/doi/10.5555/646005.673739
[lenses]: https://doi.org/10.1145/2103656.2103715
[cegar]: https://doi.org/10.1007/10722167_15
[sideinfo]: https://doi.org/10.1109/GLOCOM.2009.5426284
[blackwell]: https://doi.org/10.1214/aoms/1177729032
[ramp]: https://doi.org/10.1145/2588555.2588562
[endpoint]: https://arxiv.org/abs/2608.06386
[escd]: https://arxiv.org/abs/2609.34738
[dvlm]: https://arxiv.org/abs/2609.33816
[mealy]: https://arxiv.org/abs/2405.08647
[gw]: https://arxiv.org/abs/2601.21424
[authority]: https://arxiv.org/abs/2609.35932
[nameless]: https://arxiv.org/abs/2609.16984
[dagger]: https://arxiv.org/abs/1011.0686
[howard]: https://arxiv.org/abs/1810.08240
[stitch]: https://arxiv.org/abs/2106.07682
[net]: https://arxiv.org/abs/1511.05641
[causal]: https://arxiv.org/abs/2106.02997
[taskonomy]: https://arxiv.org/abs/1804.08328
[cem]: https://arxiv.org/abs/2209.09056
[selective]: https://arxiv.org/abs/1705.08500
[lifelong]: https://arxiv.org/abs/2007.07732
[progressive]: https://arxiv.org/abs/1606.04671
[adapter]: https://arxiv.org/abs/2005.00247
[finger]: https://arxiv.org/abs/2608.15976
[jacobian]: https://arxiv.org/abs/1803.00443
[successor]: https://arxiv.org/abs/1606.05312
[lite]: https://arxiv.org/abs/2602.04706
[reduction]: https://arxiv.org/abs/2510.08102
[pruned]: https://arxiv.org/abs/2608.00837
