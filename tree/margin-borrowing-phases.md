# Margin-borrowing write phases

**Status:** Ideas only; no training runs, code, or GPU work. **Parent:** [Phase-cancelling protection cycles](cancelling-cycles.md) ([PR #210](https://github.com/manojbajaj95/cl/pull/210)), cards 06 and 14. **Review seed:** [Flood triage, row 321](https://github.com/manojbajaj95/cl/blob/1b941b702ffc6873034c8efbdb03e30bd85de32d/reviews/flood-triage.md#L321) gives both cards a 3: route one shared write through phases so each group of old items takes its reversible excursion only when its own margin has slack, and keep a fading phase-local trace so two independent truthful examples jointly cross a useful boundary while a lone unconfirmed write falls back, then retire both examples. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/1b941b702ffc6873034c8efbdb03e30bd85de32d/reviews/idea-ledger.md): match margins before crediting any forgetting order, stack the parts' best baselines for a merge, reject wins built into the simulator, remember that margin-gated visibility (MX2) is already dead, and check ordinary old tasks in every first test.

## Can old items lend margin on a schedule, and can a pending write live on that loan?

**Verdict: neither seed is new as a scheduler or as a counter.** A time-indexed margin solver, [GEM][gem] with phase-dependent tolerances, or the drift-plus-penalty queues of [COLD][cold] can already let old constraints dip and recover; a leaky integrator with a threshold is a coincidence detector, and [synaptic tagging and capture][stc] (with its model in [Clopath et al.][clopath]) already holds a tentative change that decays unless a second event consolidates it. [Lookahead][lookahead] and [fast weights][fastw] already run fast excursions that are pulled back. The candidate object is narrower: a **margin loan**, a write component whose disturbance on one old group is admitted only while that group has slack, carried by the learner's own cycle rather than a clock or per-task block, and repaid by the cycle's return. A pending, unconfirmed write is *stored as an outstanding loan*: a second independent truthful example converts it into a margin-neutral permanent change, while a lone write is repaid and vanishes. That is new only if it admits truthful writes that time-invariant protectors reject, and needs no buffer of pending examples that the stacked control would keep.

## Two hand checks before proposing a first test

**W7 — staggered loans beat every time-invariant protector, and a clocked solver ties them.** Two old groups have gap changes `g1, g2` relative to the no-write trace over three phases, a previously acquired job C reads `g1 + g2`, and a read at phase `t` is safe iff `g1(t) > −s1(t)`, `g2(t) > −s2(t)`, `g1(t)+g2(t) > −3`. The useful write must open two gates, `g1 ≤ −2` at some phase and `g2 ≤ −2` at some phase, and return to `g1 = g2 = 0` at phase 3. With slack `s1 = (3,1,1)` and `s2 = (1,3,1)`, a staggered schedule such as `g1 = (−5/2, −1/2, 0)`, `g2 = (0, −2, 0)` is safe at every read (exhaustive search on the half-integer grid finds 9 safe schedules). A time-invariant tolerance is `min_t s_i(t) = 1 < 2`, so per-step GEM, OGD/GPM nullspaces and a single-phase write admit nothing. With coincident slack `s1 = s2 = (3,1,1)` no schedule exists: both gates must open at phase 1, and C then reads `≤ −4`. So the whole gain is the *phase variance* of slack plus shared readers that forbid co-borrowing, and an oracle that reads `s_i(t)` solves it exactly. The primitive must reach W7's schedule from one frozen map with no clock, no per-group register and no margin oracle; otherwise it is an EDF-style scheduler ([Liu & Layland][edf]).

**W8 — a fading trace counts; it cannot tell truth from repetition.** Let a scalar trace follow `z ← ρz + u` with `ρ = 1/2`, latch at `z ≥ 1`, and let each truthful write give `u = 7/10`. A lone write peaks at `7/10` and decays; a pair one step apart reaches `21/20` and latches; a pair two steps apart reaches `7/8` and does not. Any pair with the same projections latches identically, including one example presented twice and two matched junk writes, and by the parent's W6 an identical post-write state cannot be labelled. Corroboration must therefore come from *structure*: a trace whose latch needs two different directions (so a duplicate cannot cover both), or a reader shaped by lawful pre-write data. A latched state also has to survive retirement of both examples, which a linear leaky trace cannot do (the parent's W4); it needs a second attractor. Report these three nulls (duplicate, matched junk pair, linear fade) in every first test.

### Shared contract for first tests

- Inherit the parent's contract: frozen host, batch, optimizer, step budget and readout before blind jobs; matched no-write traces at the same phase; signed true-vs-strongest-rival gaps for every old item; **A** ordinary old tasks including near-boundary items, **C** previously acquired jobs; reads at every exposed phase, returns 1, 8 and 64; matched pre-write margins per item.
- Define old **groups** before any job is drawn (by task, class or a fixed clustering of pre-write gradients), never from test labels. A loan is credited only when a group's gap actually moves by more than its time-invariant tolerance at some phase and returns within the declared period.
- For corroboration, an **independent** pair is two distinct truthful examples of the same unseen job drawn from different contexts; controls are the same example twice, a truthful example plus norm-, angle- and timing-matched junk, two junk writes, and a truthful pair spaced past the fade. After a latch both examples are deleted; no buffer may keep them.
- Give [GEM][gem] / [A-GEM][agem] with the best constant tolerance, GEM with a phase-indexed tolerance table, [COLD][cold], [OGD][ogd], [GPM][gpm], [PCGrad][pcgrad], [EWC][ewc], [PackNet][packnet] / [HAT][hat] private blocks, the parent's two-phase cancellation, momentum, gradient accumulation, and a replay buffer that waits for a second example their best shot. For merged claims stack the best scheduler with the best buffer. Charge every clock bit, register, stored example, dual variable and probe.

## Idea cards

### 01. Stagger margin loans across old groups — primitive candidate (seed, parent card 06)
**Mechanism.** One shared write is split over three phases so group 1 absorbs its disturbance while its margin is high and group 2 absorbs its own later; the return repays both, with no per-group phase or parameter block. **Novelty / control.** [PCGrad][pcgrad] and [GEM][gem] resolve conflicts per step; [COLD][cold] allows time-averaged deviations; W7 shows a clocked solver ties. The claim is admitted writes beyond time-invariant protectors from a frozen map that does not read the clock. **Cheapest first test.** Build W7 in a two-unit ReLU host whose natural cycle gives phase-shifted group margins; train one batch sequence, then apply held-out job gradients, comparing against constant-tolerance GEM, the phase-indexed table and PackNet. **Old-task retention.** Score both groups and C at every phase, including the coincident-slack negative where every arm must refuse.

### 02. Corroborate through a fading in-phase trace — primitive candidate (seed, parent card 14)
**Mechanism.** A phase-local trace holds each truthful write for a few cycles; two independent writes jointly cross a boundary into a translated job orbit, a lone write falls back to the original tube, and both examples are then retired. **Novelty / control.** [Synaptic tagging and capture][stc], [Modern Hopfield][modern] aggregation and momentum all integrate repeated evidence; W8 shows a scalar trace cannot separate duplicates or junk pairs. **Cheapest first test.** Enumerate true/true, duplicate, true/junk, junk/junk and late true/true pairs on unseen jobs in a bistable two-unit host, matched on norm, angle and spacing. **Old-task retention.** A/C between writes, at time-out, and after the latched orbit settles with both examples deleted.

### 03. Let the host's own oscillation be the loan calendar — primitive candidate
**Mechanism.** Shape the cycle so each group's margin peaks at a different phase as a side effect of serving A, and write job gradients through ordinary steps; loans land in high-slack phases because the dynamics put them there. **Novelty / control.** A time-division schedule is switched control ([Liberzon][switching]); W7's oracle ties. The candidate must beat the phase-indexed GEM table while storing no phase bit. **Cheapest first test.** Remove the clock from W7: give the learner only the current state; compare admitted job service against the table with one charged bit of phase state, and against a host trained without phase-shifted slack. **Old-task retention.** Check that shaping the oscillation does not lower any group's minimum margin before writes.

### 04. Certify the phases a write needs with a loan conflict graph — primitive candidate
**Mechanism.** Nodes are old groups whose loans a write needs; edges join groups that a shared reader (C, a common rival) forbids from borrowing together. A schedule is a colouring by phases with slack, so the chromatic number lower-bounds the period a write needs. **Novelty / control.** Interval and register colouring ([Chaitin][chaitin]) are classical; the object here is a learned-host graph whose colourability predicts which blind writes are admissible. **Cheapest first test.** Enumerate small three- and four-group hosts, compute the graph from pre-write probes, and check that predicted infeasible writes are exactly those exhaustive search rejects, against a constant-tolerance predictor. **Old-task retention.** Count A/C failures on writes the graph admits.

### 05. Repay loans with interest — primitive candidate
**Mechanism.** Shape the return so a group that lent margin ends the cycle with a *larger* margin than before, using the job write's shared feature, so lending raises the next write's slack. **Novelty / control.** Margin-maximizing replay and [MER][mer] shape future interference; the parent's card 12 widens the next job set. The test is whether lending itself causes the gain, against replay and a margin regularizer at equal steps. **Cheapest first test.** Compare a borrowed write and a projected write of equal job service in W7, then admit a second blind write; ablate the interest term. **Old-task retention.** Report A/C margins after each write, with interest counted only on items the write moved.

### 06. Bound the default if a read arrives mid-loan — improvement
**Mechanism.** Minimize the worst outstanding loan rather than total excursion, so an unscheduled read during any phase still keeps every group positive. **Novelty / control.** [Simplex][simplex] runtime assurance and the parent's card 17 already protect intermediate states. The improvement must admit more writes than worst-time shielding at equal service. **Cheapest first test.** Insert reads at every phase and one delayed phase in W7; compare min-max loans, total-cost loans and shielding. **Old-task retention.** Score every exposed read, not only returns.

### 07. Price each group's slack with a phase-local dual — improvement
**Mechanism.** Keep one dual variable per group that rises when its gap nears zero and falls while it has slack, so the write's loan routing follows prices instead of a planned schedule. **Novelty / control.** [COLD][cold] uses virtual queues for long-term stability and primal-dual CMDP methods do this per constraint; here constraints are hard per read and duals reset each cycle. **Cheapest first test.** Compare per-group phase duals with COLD's queue, constant GEM and the W7 oracle, counting dual state as storage. **Old-task retention.** Report worst A/C margin and any read where a lagging dual allowed a flip.

### 08. Keep an outstanding-loan ledger without storing writes — primitive candidate
**Mechanism.** When a second write arrives before the first's loans are repaid, admit it only if the combined outstanding loans per group stay below current slack, reading that total from the state's displacement from the reference orbit rather than from a write log. **Novelty / control.** Credit limits are bookkeeping; a stored write list ties by construction. The claim is that the displacement alone is a sufficient ledger. **Cheapest first test.** Overlap two blind writes at all offsets in W7; compare against a write log, a reset between writes and constant GEM. **Old-task retention.** Score A/C at the worst overlap and after both repay.

### 09. Require two views for a latch — primitive candidate
**Mechanism.** Split the trace into two channels fed by different input contexts; the latch needs both above half threshold, so one example repeated cannot latch, but two independent examples of the same job can. **Novelty / control.** Multi-view agreement is [co-training][cotrain]; two matched junk writes in different channels still latch. The claim is lower false latching from duplicates and stale repeats than a scalar trace at equal true latch rate. **Cheapest first test.** W8 with a 2D trace; enumerate duplicates, cross-channel junk pairs and true pairs on unseen jobs; compare with a replay buffer that waits for two distinct examples. **Old-task retention.** A/C while one channel is pending and after a false latch is rejected.

### 10. Hold the unconfirmed write as a margin loan — primitive candidate (merge of 01 and 02)
**Mechanism.** The first truthful example is admitted as a loan on one group's slack; the cycle repays it unless a second independent example arrives in the window, which turns the pair into a margin-neutral permanent change. The pending state is the excursion itself, not a buffer. **Novelty / control.** Merge rule: stack the best scheduler (phase-indexed GEM) with the best buffer (replay that waits for corroboration) at equal bytes. The interaction to isolate is that removing the loan also removes the memory of the first example. **Cheapest first test.** In a W7 host, apply one or two blind examples at all spacings; ablate the loan (project it out) and check that corroborated latching disappears, then compare with the stacked control. **Old-task retention.** A/C at every phase while the loan is outstanding, after repayment of a lone write and after latching.

### 11. Let a contradicting example cancel the pending loan — improvement
**Mechanism.** A truthful example that contradicts the pending write repays its loan faster than decay, so contradicted writes never latch even if a junk corroborator follows. **Novelty / control.** Belief revision and the parent's card 13 cover reversal after install; this acts before install. Compare with a buffer that deletes on contradiction. **Cheapest first test.** Sequences true, contradict, junk and true, contradict, true at matched norms; measure latch rates. **Old-task retention.** A/C after early repayment, checking that it does not overshoot into a new old-gap drift.

### 12. Set the fade from the accidental-coincidence rate — improvement
**Mechanism.** Choose the trace decay so independent junk arriving at the measured nuisance rate latches below a fixed rate α, using the classical accidental-coincidence count `2τ r₁ r₂`, while truthful pairs at the job rate still latch. **Novelty / control.** This is coincidence-detector design and [SPRT][sprt]-style evidence; an improvement only if it sets a better operating point than a tuned replay-wait window. **Cheapest first test.** Sweep decay and nuisance rate in W8 streams; compare false and true latch rates with a two-example buffer at matched window. **Old-task retention.** Report A/C after every false latch at the chosen decay.

### 13. Make the latched job independent of which pair latched it — primitive candidate
**Mechanism.** After retirement, different corroborating pairs for the same job should land on the same translated orbit, so the state encodes the job, not its examples. **Novelty / control.** [Hopfield][hopfield] memories store patterns; storing both examples is not credited. **Cheapest first test.** Latch the same unseen job with several disjoint pairs; measure orbit distance between outcomes and held-out service, against a buffer that keeps the pair. **Old-task retention.** A/C on each terminal orbit.

### 14. Bound pending writes by groups with slack — primitive candidate
**Mechanism.** Each pending write holds a loan on a different group, so at most as many unconfirmed writes can wait as there are groups currently in slack; a k-of-n rule falls out of the loan graph. **Novelty / control.** A fixed-size buffer ties at equal count; the claim is that capacity follows actual slack and shrinks safely when margins tighten. **Cheapest first test.** Stream interleaved pending writes for three jobs into a three-group host; compare drops and false latches with a fixed buffer of equal maximum size. **Old-task retention.** A/C at peak pending load.

### 15. Test whether momentum is already the trace — improvement (vacuity audit)
**Mechanism.** Adam's first moment decays as `β₁ᵗ` and accumulates aligned writes, so a pair inside the window already moves further than a lone write. **Novelty / control.** If an ordinary optimizer at matched step size reproduces card 02's latch rates, card 02 is momentum. **Cheapest first test.** Run W8's pairs through SGD with momentum and Adam with no designed trace; compare latch and fall-back with the designed host. **Old-task retention.** A/C under both optimizers, with slots reset and kept.

### 16. Price the cheapest junk pair that fakes corroboration — improvement (audit)
**Mechanism.** Find the smallest-norm junk pair that latches, and report the ratio to the smallest truthful pair: a corroboration margin. **Novelty / control.** Adversarial robustness bounds ([CROWN][crown]) give the same kind of certificate for inputs; here it is for writes. **Cheapest first test.** Solve the minimal-norm pair exactly in two-unit hosts; compare against scalar-trace and two-view designs. **Old-task retention.** A/C under the minimal junk pair.

### 17. Borrow against a write's own positive transfer — improvement
**Mechanism.** Allow a group to lend more than current slack when the job write is predicted to raise that group's margin after return. **Novelty / control.** This is a forecast; the plasticity-reserve forecasts failed, so it must beat a constant forecast. **Cheapest first test.** Compare forecast-gated loans with constant tolerance on writes with known positive and negative transfer. **Old-task retention.** Count reads where a wrong forecast caused a flip.

### 18. Keep staggered loans safe under phase jitter — improvement
**Mechanism.** Train loans to stay safe when phase durations vary by one step, widening the slack window each loan needs. **Novelty / control.** [Tube MPC][tube] handles bounded timing noise; the gain must be service at a jitter level where a robust single-phase design admits nothing. **Cheapest first test.** Enumerate jittered W7 schedules and compare robust stagger with a robust constant tolerance. **Old-task retention.** Worst A/C over jitter patterns.

### 19. Borrow hidden-unit slack instead of output margin — primitive candidate
**Mechanism.** Route the excursion through activation slack, units far from their ReLU kink for one group's inputs, so that group's output gaps never move while the write still passes through shared weights. **Novelty / control.** [GPM][gpm] protects activation subspaces at all times; here protection holds only while the slack exists. **Cheapest first test.** Compare activation-slack loans with GPM and output-margin loans on a two-layer toy where the groups' activation slack peaks at different phases. **Old-task retention.** A/C including inputs near the kink.

### 20. Prove when staggering buys nothing — improvement
**Mechanism.** If every group's slack is constant across phases, or the conflict graph needs more colours than phases, return a certificate that no schedule beats time-invariant protection. **Novelty / control.** A cheap falsifier like the parent's card 21. **Cheapest first test.** Enumerate small hosts with constant, coincident and staggered slack; check the certificate against exhaustive search. **Old-task retention.** Include C reads so infeasibility is not hidden by skipping a reader.

### 21. Rescue a rare true example that falls back — improvement
**Mechanism.** A lone truthful write that faded leaves no trace; re-offer its loan on the next cycle only if a weak marker survives in another group's slack. **Novelty / control.** False rejection of rare truths is the cost of corroboration; compare with a replay buffer that keeps singletons and with no rescue. **Cheapest first test.** Stream rare single true examples and junk at equal rates; measure service on rare jobs and junk latches. **Old-task retention.** A/C after a rescued and an unrescued singleton.

### 22. Discover groups by when their margins peak — primitive candidate
**Mechanism.** Cluster old items by the phase signature of their margins on the unperturbed cycle, so groups for lending are found from pre-write data rather than task labels. **Novelty / control.** Task-free CL and GPM bases group by gradients; the candidate groups by slack timing. Compare with task-label groups and gradient clusters. **Cheapest first test.** On a three-group host with mixed labels, recover groups by phase signature and measure admitted writes against oracle groups. **Old-task retention.** A/C per discovered group, including items whose signature is ambiguous.

## Ranked deeper questions

1. **Can one frozen map hold an unconfirmed write as a margin loan and latch it only on independent corroboration, beating phase-indexed GEM plus a waiting buffer at equal bytes?** Start with 10, 01, 02 and 09. Require that ablating the loan removes the memory of the first example, that duplicates and matched junk pairs do not latch, and that A/C stay safe at every phase. If the stacked control ties, keep the scheduler and the trace as separate tools.
2. **Does staggered borrowing need a clock?** Start with 03, 04 and 20. If every gain over constant tolerance vanishes once a one-bit phase register is charged, the primitive is a scheduler, and W7's oracle is the result.
3. **What lawful structure separates corroboration from repetition?** Start with 09, 12, 15 and 16. If plain momentum reproduces the latch rates, or the corroboration margin is near 1, report the counting null from W8.
4. **Does lending survive many writes?** Start with 05, 08 and 14. If outstanding loans or the pending capacity behave like a fixed buffer under load, keep only the single-write result.

These are nearest comparisons, not exhaustive novelty claims. The first gate is an exact or enumerated CPU case with held-out job service and ordinary old-task retention, not a schedule drawn with a known clock or a trace that reads a hidden label.

[ogd]: https://arxiv.org/abs/1910.07104
[gpm]: https://arxiv.org/abs/2103.09762
[ewc]: https://doi.org/10.1073/pnas.1611835114
[gem]: https://arxiv.org/abs/1706.08840
[agem]: https://arxiv.org/abs/1812.00420
[pcgrad]: https://arxiv.org/abs/2001.06782
[cold]: https://arxiv.org/abs/2606.08452
[packnet]: https://arxiv.org/abs/1711.05769
[hat]: https://arxiv.org/abs/1801.01423
[stc]: https://doi.org/10.1038/385533a0
[clopath]: https://doi.org/10.1371/journal.pcbi.1000248
[lookahead]: https://arxiv.org/abs/1907.08610
[fastw]: https://arxiv.org/abs/1610.06258
[modern]: https://arxiv.org/abs/2008.02217
[hopfield]: https://doi.org/10.1073/pnas.79.8.2554
[switching]: https://doi.org/10.1007/978-3-319-44830-5_3
[edf]: https://doi.org/10.1145/321738.321743
[chaitin]: https://doi.org/10.1145/800230.806984
[mer]: https://arxiv.org/abs/1810.11910
[simplex]: https://doi.org/10.1109/ACC.1998.703255
[cotrain]: https://doi.org/10.1145/279943.279962
[sprt]: https://doi.org/10.1214/aoms/1177731118
[crown]: https://arxiv.org/abs/1811.00866
[tube]: https://doi.org/10.1016/j.automatica.2004.08.019
