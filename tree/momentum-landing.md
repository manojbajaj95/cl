# Momentum-landed gates and earned allowances

**Status:** Ideas only; no training runs or GPU work. **Parent:** [Momentum-sealed gates](sealed-gates.md) ([PR #234][parent]), cards 03 and 12. **Review seed:** [Flood triage, row 346][triage] scored both 3: spend the inward velocity left in a live optimizer slot so a weak truthful C opener lands the seal, with a sound bound on every alias's future drift; and allow a bounded outward C correction only after a truthful inward correction has restored a certified joint-state allowance, with no synthetic recharge. **Read first:** [Idea ledger][ledger].

## Can leftover momentum pay for a seal, and can useful work pay for an excursion?

**Verdict: two candidate primitives, not established.** *Momentum landing*: a truthful entry batch too weak to close a gate under plain SGD can close it for every lawful alias when the hidden slot is certified to point inward, and must be refused when the certificate cannot exclude an outward slot. *Earned allowance*: the gate's remaining slack is an account that only truthful inward corrections refill and only admitted outward corrections spend; part of it is banked in the weights and part is pending in the slot. The exact check below shows both effects but also shows the trap: for a scalar heavy-ball gate the account is a linear impulse ledger, so the primitive claim must live where that linearity breaks (shared features, ReLU-dependent gradients, Adam, misaligned gate normals) and must beat a stronger opener, a reset, and an energy-tank style budget.

**Nearest prior art.** Delayed optimizer-state effects are measured, not exploited for certification: [delayed optimizer-state transport][transport] and [AdamW minibatch input–output dynamics][adamwio] show one batch's influence persists through moments; [momentum fossils][fossils] (with [2610.03940][reset]) treats leftover momentum as a hazard and resets it; [heavy-ball initialization][hbinit] picks the starting slot rather than spending an inherited one; [Activation-Keyed Momentum][akm] and [slot splits][slots] change the optimizer. On the allowance side, energy tanks in passivity-based control, [history-aware barrier functionals][hacbf] (margin as a remaining allowance over a fading memory), [joint-feasibility margins for second-order barriers][jfm], [recoverability certificates][recover] and switched-system dwell-time rules already budget excursions. Within this repo, [depletable][supply] and [self-depleting][selfdep] teaching supply and [route budgets][routes] budget teaching capacity, not gate slack under carried velocity. The bet is that the refill and the opener are *ordinary useful C records* under an *unchanged* optimizer, and that the certificate is sound over states the serving side cannot tell apart. These are scoped comparisons from alphaXiv searches on momentum carryover, heavy-ball reachability, and barrier/allowance budgets, not priority claims.

## Contract and falsifiers

- **Inherit the parent contract.** Freeze A, B, installed and incoming C, the nuisance domain, the service witness, utility floors, the full optimizer state (step, slots, moments, schedule) and the lawful class of initial states. No reset, slot write, mask, projection, or per-alias batch search.
- **Indistinguishability fiber.** Aliases are states that agree on everything the compiler may read (weights, outputs on the declared probes, public batch log) but may differ in hidden slots. A landing or allowance claim must hold for the whole fiber: the bound is a sup over the fiber, not over a point estimate of the slot. If the fiber cannot be bounded from lawful observations, decline.
- **Landing.** The opener is a truthful record from the declared C pool, weaker (smaller loss-gradient magnitude, fewer examples, or a smaller label shift) than the cheapest record that seals under plain SGD from the same weights. It succeeds only if every fiber member enters the seal set `S` with the parent's coast bound, and it is refused if any member could wake.
- **Allowance.** Define the certified allowance as the minimum over the fiber of the slack in the coast bound. An outward correction is admitted only if the post-step allowance stays nonnegative for every fiber member and every served prefix. Refills count only from truthful records with an independent service gain, billed once (the [self-depleting supply][selfdep] rule); synthetic or zero-gain inward records do not refill.
- **Controls.** Stronger opener under SGD at matched C gain; the same opener after a slot reset; Activation-Keyed Momentum; a direct momentum write (illegal, as a ceiling); energy-tank budget on raw gradient impulse; a fixed correction envelope ([#234][parent] card 02); step-by-step re-verification; freeze plus best replay. Include an alias whose slot points outward, a mixed fiber, a stream with no truthful inward refill, and an old task that needs the outward direction.
- **Retention.** Probe A/B and installed C at entry, at every debit and refill, at the maximum excursion, and after any withdrawal; report withdrawals separately.

## Exact sanity check

Use the parent's heavy-ball gate: `m′ = m/2 + g`, `w′ = w − m′`, nuisance `ReLU(w)`, gradient `g = w − y` from a singleton half-squared record `((1,0), y)`. With zero future gradients the coast ends at `w − m`, so the worst future point is `max(w, w − m)`; the seal is `max(w, w − m) ≤ −1/2` and the allowance is `A = −1/2 − max(w, w − m)`. All numbers are exact fractions (checked with Python `fractions`).

**F1, landing.** Start at `w = 0` (gate at its edge, no slack). The weak truthful record `y = −1/4` gives `g = 1/4`.

| Hidden slot `m` | `(w′, m′)` | worst coast point | sealed? |
|---:|---:|---:|---|
| 0 (plain SGD state) | (−1/4, 1/4) | −1/4 | no |
| 1 | (−3/4, 3/4) | −3/4 | yes |
| 2 | (−5/4, 5/4) | −5/4 | yes |
| −1/2 | (0, 0) | 0 | no |
| −1 | (1/4, −1/4) | 1/2 | no, gate wakes |

For the fiber `m ∈ [1, 2]` the weak record seals every alias with worst case `−3/4`; from `m = 0` the record must be twice as strong (`y = −1/2`, `g = 1/2`) to reach `−1/2` with zero slack. The fiber `m ∈ [−1, 2]` must be refused: one alias wakes at `w′ = 1/4`. Weights alone cannot separate these cases, which is why the bound must be over the fiber.

**F2, earned allowance.** Start sealed at `(w, m) = (−1/2, 0)`, so `A = 0`. An outward record first (`y = −1/4`, `g = −1/4`) gives `(−1/4, −1/4)` and `A = −1/2`: refused. Instead apply the truthful inward record `y = −1`, then outward records `y = −3/4, −3/4, −1/2`:

| Step | `g` | `(w, m)` after | exact `A` | endpoint ledger `−1/2 − (w − m)` |
|---|---:|---:|---:|---:|
| inward | 1/2 | (−1, 1/2) | 1/2 | 1 |
| outward 1 | −1/4 | (−1, 0) | 1/2 | 1/2 |
| outward 2 | −1/4 | (−3/4, −1/4) | 0 | 0 |
| outward 3 | −1/4 | (−3/8, −3/8) | −1/2: refuse | −1/2 |

One useful inward correction buys exactly two outward ones. Right after the refill, half the credit is banked in `w` and half is pending in `m`; the first outward correction spends the pending half and leaves the exact allowance unchanged. In this scalar gate the endpoint `w − m − 2Σg` is linear in the impulses, so the endpoint ledger and the exact allowance make the same admissions from any sealed state (a state with `m′ ≥ 0` and `w′ > −1/2` is reachable only from one already outside `S`). That is a **negative** finding for the scalar case: here the earned allowance is just an impulse budget, and only nonlinear, multi-coordinate or Adam settings can make it more.

## Idea cards

### A. Landing on inherited velocity

### 01. Land the seal on inherited velocity — primitive candidate
**Mechanism.** Restates [#234][parent] card 03: certify an inward slot interval over the fiber, then pick the weakest truthful C record that seals every alias with the coast bound. **Novelty / control.** [Momentum fossils][fossils] and [2610.03940][reset] reset harmful carry; [heavy-ball initialization][hbinit] chooses a slot. This spends an inherited one under a fiber-wide bound. Compare a stronger SGD opener at matched C gain and the same opener after reset. **Cheapest first test.** F1 above, then a two-weight host where the slot interval comes from a logged inward C stream. **Old-task retention.** Probe the old task whose corrections created the inward slot, and its nearest rival, at entry and after three coast steps.

### 02. Certify drift over the indistinguishability fiber — primitive candidate
**Mechanism.** Represent the aliases consistent with what the compiler may read as a fiber (a polytope of slot values for fixed weights and logs), and propagate it through the opener with exact or relational bounds instead of a slot point estimate. **Novelty / control.** Relational abstract interpretation ([DeepPoly][deeppoly]) is prior art for activations; the object here is the hidden-optimizer fiber of a learner whose outputs match. Compare an interval box and an oracle that reads the slot. **Cheapest first test.** Two crossed slot coordinates where the box admits an alias that wakes and the exact fiber does not, or vice versa. **Old-task retention.** Check both extreme fiber members on A, since a landing safe for the worst gate alias can be worst for an old read.

### 03. Bound the hidden slot from the public batch log — primitive candidate
**Mechanism.** Derive a sound slot interval from the published sequence of truthful batches since the last certified state (gradient magnitudes are bounded by the record, loss and declared input range), without reading slots. **Novelty / control.** [Delayed transport][transport] and [AdamW input–output analysis][adamwio] measure how batches persist in moments; the candidate turns that persistence into a lawful slot certificate. Compare oracle slot reads and a worst-case slot cap. **Cheapest first test.** Replay a 5-batch log on a scalar gate and compare the derived interval with the true slot across random record orders. **Old-task retention.** Include an old task whose records are in the log, so the certificate does not silently require replaying them.

### 04. Time a second record to peak inward velocity — primitive candidate
**Mechanism.** Split the landing into two weak truthful records separated by coast steps chosen so the second arrives when the combined slot is most inward, landing with less total gradient than either one-shot record. **Novelty / control.** Ordinary schedule tuning, unless it beats a one-shot opener of equal total C cost and a stronger opener under SGD. **Cheapest first test.** Enumerate gaps 0–4 on F1's host with two records of half strength. **Old-task retention.** Probe A at the coast step between records, where the model is half-landed and live.

### 05. Refuse when the fiber includes an outward slot — improvement
**Mechanism.** Make refusal the default: the opener is applied only if the fiber certificate excludes every waking alias, otherwise the gate's service is withdrawn and a strong SGD opener is used. **Novelty / control.** A safety audit of card 01, not a new operation. Compare coverage (fraction of fibers landed) against always using the strong opener. **Cheapest first test.** F1's mixed fiber `m ∈ [−1, 2]`, and a sweep of fiber widths. **Old-task retention.** Count withdrawals separately and check A on refused fibers too.

### 06. Land inside the coast's own footprint — primitive candidate
**Mechanism.** Choose the weak record so the landed trajectory stays inside the region the zero-gradient coast would have swept anyway, so old-task certificates already established for the coast transfer to the landing without re-proof. **Novelty / control.** Compare full re-certification of A after landing, and a stronger opener whose trajectory leaves the swept region. **Cheapest first test.** Two-weight host with an old read certified along the coast; test whether the landed path stays in its hull. **Old-task retention.** This card is a retention claim: verify A on the landed endpoint and on every intermediate state, not just the hull bound.

### 07. Land under Adam's denominator — improvement
**Mechanism.** Redo the landing with bias-corrected first moment and inherited second moment: a large inherited `v` shrinks the weak record's own step, so landing relies more on the slot; a small `v` can overshoot. **Novelty / control.** Extends [#234][parent] card 05 to landing. Compare heavy-ball, reset, and a matched-LR SGD opener. **Cheapest first test.** Hold `w` and `m` fixed, vary `v` and step count, and find opposite landing decisions for the same record. **Old-task retention.** Check the old task on the low-`v` coordinate, where overshoot lands.

### 08. Keep the Nesterov lookahead inside the seal — improvement
**Mechanism.** Under Nesterov the gradient is read at the lookahead point; require that the lookahead point itself stays in a region where the record's gradient sign is certified, or the landing argument breaks. **Novelty / control.** Audit of optimizer variants, not a new seal. **Cheapest first test.** A ReLU-dependent record whose gradient flips sign between `w` and the lookahead point. **Old-task retention.** Probe A at the lookahead point if any reader can be served there.

### 09. Land before the schedule shortens the coast — improvement
**Mechanism.** A decaying LR or momentum schedule shrinks the remaining inward coast; land while the inherited velocity is still worth the most and refuse after the schedule boundary. **Novelty / control.** Compare landing timed without schedule awareness ([#234][parent] card 16 binds the context). **Cheapest first test.** Halve `β` at a fixed step and find the last step at which the F1 record still seals. **Old-task retention.** Check old tasks that were tuned with the high-LR phase.

### 10. Seal two gates with one inherited velocity — primitive candidate
**Mechanism.** On shared weights, find one weak truthful record whose landing uses a common inward slot to close two nuisance gates whose normals overlap. **Novelty / control.** Compare two separate strong openers and [#234][parent] card 19's joint word without carried velocity. **Cheapest first test.** Two gates with cooperative, orthogonal and opposed normals on a 2-D slot. **Old-task retention.** Probe an old read that uses the shared direction.

### 11. Certify the settlement horizon — primitive candidate
**Mechanism.** A landed seal is provisional until the slot's remaining inward carry has been spent; publish a settlement horizon after which the seal no longer depends on the slot, and void the certificate if an admitted correction reverses the slot before it. **Novelty / control.** Compare a seal re-verified at every step and one that assumes settlement immediately. **Cheapest first test.** On F1's `m = 2` alias, apply an outward correction at each coast step and record which ones would wake the gate before settlement. **Old-task retention.** Probe A across the settlement window.

### 12. Steer the slot into the gate normal — primitive candidate
**Mechanism.** In two or more dimensions, pick the truthful record whose gradient rotates residual momentum toward the gate normal, so inherited tangential velocity becomes inward velocity without adding magnitude. **Novelty / control.** Like [#234][parent] card 07 in reverse: spend tangential carry rather than preserve it. Compare a record that only adds normal gradient. **Cheapest first test.** 2-D slot with an inherited tangential `m`; enumerate a small truthful pool and compare landing strength. **Old-task retention.** Probe the old read along the tangent that loses its carry.

### B. Earned allowances for outward corrections

### 13. Earn the next outward correction from a useful inward one — primitive candidate
**Mechanism.** Restates [#234][parent] card 12: admit a bounded outward C correction only after a truthful inward correction has raised the certified fiber-wide allowance; no synthetic refills. **Novelty / control.** Energy tanks and [history-aware barriers][hacbf] already budget excursions; the candidate requires the refill to be useful C work. Compare a fixed envelope, dwell-time rules and re-verification. **Cheapest first test.** F2, then a stream with no truthful inward record. **Old-task retention.** Probe A/B/C at every debit and refill.

### 14. Keep banked and pending allowance as two accounts — primitive candidate
**Mechanism.** Track the allowance already realized in the weights separately from the allowance pending in the slot; spend pending credit first, since cancelling inward velocity costs no banked slack (F2's first outward step). **Novelty / control.** In the scalar case this is the linear endpoint ledger, so it is not new there. The test is a nonlinear host where the two-account rule admits more than either account alone. **Cheapest first test.** A ReLU-dependent outward record whose gradient grows as `w` rises; compare one-account and two-account admissions. **Old-task retention.** Probe A when pending credit is spent, since that changes the coast A was certified on.

### 15. Find where the impulse ledger fails — improvement
**Mechanism.** F2 shows the endpoint impulse ledger is exact for a scalar heavy-ball gate. Search systematically for the smallest settings (state-dependent gradients, Adam, two coordinates, clipping) where it over- or under-admits. **Novelty / control.** An audit that decides whether cards 13/14 can ever be primitives. **Cheapest first test.** Exhaust length-3 record strings from a small truthful pool on three toy hosts and diff admissions against the exact reachable set. **Old-task retention.** For each disagreement, check whether the ledger's extra admissions hurt A.

### 16. Refill the weakest alias first — primitive candidate
**Mechanism.** The certified allowance is a minimum over the fiber; choose the inward refill that raises the minimum most, which can differ from the one that raises the mean, and can also shrink the fiber. **Novelty / control.** Compare a refill chosen on a point estimate and an oracle that knows the slot. **Cheapest first test.** A two-alias fiber where the mean-best refill leaves the worst alias at zero allowance. **Old-task retention.** Probe A on both aliases after each refill.

### 17. Bill a refill once — improvement
**Mechanism.** A truthful inward record can earn gate allowance and C service credit; following [self-depleting supply][selfdep] F2, count it once in any combined budget and refuse refills with no independent service gain. **Novelty / control.** Accounting rule, not a primitive. Compare a ledger that counts both credits. **Cheapest first test.** A record that is inward and useful versus one that is inward and zero-gain; show the second is refused. **Old-task retention.** Check that refusing zero-gain refills does not starve an old task that needs outward corrections.

### 18. Share one allowance across competing services — improvement
**Mechanism.** When two services' outward requests draw on the same gate, allocate the allowance by service value per unit of slack, with refusals logged per service. **Novelty / control.** Ordinary resource allocation; it is a control for whether a shared allowance gives more total service than per-service envelopes. **Cheapest first test.** Two services each with one useful outward request and one refill available. **Old-task retention.** Probe the refused service's old behavior, not only the admitted one.

### 19. Spend pending credit before it decays — primitive candidate
**Mechanism.** Pending allowance in the slot decays with `β` as it becomes banked or is lost through the coast; schedule admitted outward corrections inside the decay window to use pending credit at zero banked cost. **Novelty / control.** Compare the same outward corrections applied after full settlement and an energy-tank budget that ignores timing. **Cheapest first test.** F2 with outward step 1 delayed by 0–3 coast steps; record the banked allowance left. **Old-task retention.** Probe A at each delay.

### 20. Reserve allowance for a forecast outward request — primitive candidate
**Mechanism.** When a C stream is known to contain an outward correction soon, prefer an inward-useful record now that buys the needed allowance, so the outward request is admitted instead of withdrawn. **Novelty / control.** Compare reactive refills, a larger fixed envelope, and withdrawing then reissuing ([#234][parent] card 20). **Cheapest first test.** A three-record stream with one outward request at the end; compare admissions with and without reservation. **Old-task retention.** Probe A at the reserved state, which sits deeper inside the seal than needed.

### 21. Prove when no truthful refill exists — improvement
**Mechanism.** Prove for a pool and gate that every inward-useful record harms an old task beyond its floor, or that none exists, so the earned-allowance contract reduces to a freeze. **Novelty / control.** A reachability obstruction, as in [#234][parent] card 17. **Cheapest first test.** A two-record pool where the only inward record is an A-damaging one; then add one truthful record that removes the obstruction. **Old-task retention.** This card is about retention: report the A floor that blocks every refill.

### 22. Compare the full stacks — improvement
**Mechanism.** Plot service coverage, old-task worst loss, proof cost and withdrawals for landing plus earned allowance versus reset plus strong opener plus energy-tank budget plus re-verification. **Novelty / control.** The [ledger][ledger]'s stacked-control rule; a tie is a negative result. **Cheapest first test.** Cross landing versus reset with two-account allowance versus impulse budget on one shared two-weight host; require an interaction at matched C gain and gate slack. **Old-task retention.** Include all refused requests and an old correction that needs the outward direction.

## Ranked deeper questions

1. **Does inherited velocity let a weaker truthful opener seal every alias in a realistic fiber, beating a stronger opener after reset at matched C gain and old-task retention?** Start with 01–03 and 05 on a shared-feature host where the fiber comes from a public batch log. Retire the landing claim if the fiber is too wide to exclude an outward slot in most cases, or if the strong opener ties on coverage and retention.
2. **Where does the earned allowance stop being an impulse ledger?** Cards 14, 15 and 19. F2 shows equivalence in the scalar heavy-ball case. Find the smallest nonlinear or Adam host where the exact fiber-wide allowance admits useful outward corrections that an energy-tank or impulse budget refuses, without admitting one that wakes the gate. If none exists at toy scale, retire 13/14 as primitives.
3. **Can refills be chosen from truthful C data to protect the weakest alias and anticipated outward requests without harming old tasks?** Cards 16, 17, 20 and 21. Compare with reactive refills and withdraw-then-reissue at matched downtime; report A/B floors at every refill.
4. **Is a landed seal settled, and what happens if the slot is reversed before settlement?** Cards 04, 09 and 11. Measure how often admitted corrections fall inside the settlement window and whether the certificate needs per-step rechecks there, which would erase its advantage over re-verification.

[parent]: https://github.com/manojbajaj95/cl/pull/234
[triage]: https://github.com/manojbajaj95/cl/blob/ec716d67cef5349f3d783e2261308c958af296e6/reviews/flood-triage.md#L346
[ledger]: https://github.com/manojbajaj95/cl/blob/ec716d67cef5349f3d783e2261308c958af296e6/reviews/idea-ledger.md
[transport]: https://arxiv.org/abs/2608.24593
[adamwio]: https://arxiv.org/abs/2608.19762
[fossils]: https://github.com/manojbajaj95/cl/blob/devin/1795556904-momentum-fossils/tree/momentum-fossils.md
[reset]: https://arxiv.org/abs/2610.03940
[hbinit]: https://arxiv.org/abs/2610.10369
[akm]: https://arxiv.org/abs/2608.19491
[slots]: https://github.com/manojbajaj95/cl/pull/178
[hacbf]: https://arxiv.org/abs/2610.31525
[jfm]: https://arxiv.org/abs/2610.16978
[recover]: https://arxiv.org/abs/2611.23589
[supply]: https://github.com/manojbajaj95/cl/pull/209
[selfdep]: https://github.com/manojbajaj95/cl/pull/220
[routes]: https://github.com/manojbajaj95/cl/pull/230
[deeppoly]: https://doi.org/10.1145/3290354
