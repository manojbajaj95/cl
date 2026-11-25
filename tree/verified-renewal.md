# Verified renewal: close the old right, check before shrinking, teach the next pair off the old receipt

**Status:** Ideas only. The two fixtures are exact rational paper checks (Python `fractions`), not learner results; no pilot or GPU work. **Parent:** [Rolling escrow across defaults](rolling-escrow.md) ([PR #226][parent]). **Seed:** round-53 merge **GPR11** ([cross-pool-53][gpr11], [flood triage row 347][triage], score 3): after a default, publish the first useful fragment with an independent clearing route, verify the incoming public uncertainty claim before any contraction that could erase evidence of under-reporting, then use already-needed successor training so the next pair no longer needs the old receipt. It joins [#226][parent] card 22 (renewal against an adaptive default schedule), [#232][shrink] card 18 (check before shrink) and [#214][lease] card 18 (finite rolling escrow). Required controls from the triage row: each part alone, their best stack, contraction before detection, authenticated chains, fresh reservations per pair, and an adaptive default schedule plus a misreport hidden by early contraction.

**Read first:** [idea ledger][ledger]. Rules carried here: merge cards must beat the stacked baselines of their parts at equal bytes, checks and compute; headline predictions that follow from linear algebra are killed; hidden-state claims must survive realistic step sizes and momentum (Noether kill); every first test includes an old-task retention check; label each card primitive or improvement.

**Verdict:** Each of the three moves is known alone: closing a revoked right is channel revocation and clearing (Lightning breach remedies, central-counterparty novation, CRLs); checking before pruning is an optimistic-rollup challenge window; retiring a dependency by training is distillation. The candidate primitive is their **coupling inside a learner**: a renewal step whose receipt can be deleted *only because* (i) the check ran while evidence still existed and (ii) ordinary successor training made the receipt's information irrelevant to every admitted continuation, while (iii) the raw hidden state still carries enough evidence for a later audit. A synchronizing reset buys (ii) by destroying (iii); a per-pair receipt buys (iii) by keeping bytes forever. GPR11 is worth pursuing only if it holds constant live receipts across defaults **and** keeps misreports detectable, at a cost the best stack of rollup-style challenge windows, authenticated chains and reset cannot match.

## Contract

- **Objects.** A = original tasks; Bᵢ = installed writes, including the defaulting partner's first useful fragment B_d; C = successor tasks; W = paired witness; R_d = the receipt the defaulter left (its claimed hidden-state set and the certificates it issued against that claim). A *clearing route* is a path that extinguishes the abandoned right and certifies B_d without reading or rebinding the backing the next pair will reserve.
- **Uncertainty claim.** Each hop publishes a set it claims contains its true hidden optimizer state (as in [#232][shrink]). Under-reporting means the true state is outside it. A claim is *harmful* only if some certificate issued under it (B_d's fallback, a reserved schedule) fails on the true state ([#232][shrink] N5b/N5c).
- **Shrink.** Any operation that reduces the reachable hidden set: clipping, bounded second moments, gate death, reset, synchronizing batches, checkpoint compaction. A shrink is *evidence-erasing* for a claim if after it no admitted public check can distinguish an honest history from some harmful lie.
- **Retirement.** R_d may be deleted only when (a) the check on its claim has passed or failed with consequences applied, and (b) no live obligation reads R_d. "No longer needs the receipt" means the same admitted action language, applied to all histories consistent with the *public* record, meets every floor without R_d.
- **Accounting.** Report live receipts, proof bytes, revocation state, check work, discarded slot mass, timely pairs and useful single arrivals separately, per default cycle and cumulatively, under an adaptive (not hindsight) default schedule.

## Two paper checks

### V1. Shrinking before the check erases the lie; shrinking to the claimed hull erases part of it

RMSprop slot, β₂ = 1/2, public truthful gradient with g² = 7, public statistic s = g²/v″ (squared update size, exact). A defaulting hop claims prior slots {1, 9}; honestly it ends at v ∈ {4, 8}. If it silently skipped decay it ends at v ∈ {9/2, 25/2}. The incoming partner's check is its first truthful step, v″ = v/2 + 7/2.

| Order | Honest s | Skipped-decay s | Lie detectable? | Discarded slot mass (honest / lie) |
|---|---|---|---|---|
| Check first | 14/11, 14/15 | 28/23, 28/39 | yes, all four distinct | 0 / 0 |
| Clamp v to [5, 8], then check | 7/6, 14/15 | 7/6, 14/15 | **no**: states merge | 1 / 5 |
| Clamp v to claimed hull [4, 8], then check | 14/11, 14/15 | 28/23, 14/15 | only for the 9/2 history | 0 / 9/2 |

The hull clamp is an exact no-op on honest histories (the [#232][shrink] N2 bulk-preserving property), so it looks free to apply before checking, yet it maps the 25/2 lie onto the honest image 8. The merging clamp also makes the receipt unnecessary for future service (state is known), which is why reset is the mandatory control: it ties on "no receipt" while destroying evidence and slot mass. What the evidence protects is the defaulter's *other* certificates: a fallback certified for B_d at multiplier ≥ 1/8 fails on the 25/2 history (multiplier 2/25) before the clamp, and only a detected lie tells the clearing route to recheck it.

### V2. The prep order retires the receipt without erasing evidence

The parent's F1 heavy-ball fixture (`m′ = m/2 + ∇L`, `w′ = w − m′`, aliases m = ±(1, 0) at w = 0, truthful batches H₁ = I, H₂, H₃).

| Arm | Final (x, y) momentum | Next H₁ step, x read | Receipt (sign bit) needed for W? | Alias still distinguishable in raw slots? |
|---|---|---|---|---|
| Default order 1→3→2 | ±(1/8, 1/4) | ∓1/16 | yes | yes |
| Legal slot reset | (0, 0) | 0 | no | **no** |
| Prep order 1→2→3 | ±(0, 1/2) | 0 | no (within the declared suffix) | yes, through y |

Only the prep arm has both properties. It is still scoped: two ordinary H₂ steps give x = ±1/4 at the second step, so the receipt becomes necessary again and must not have been deleted unless that suffix is outside the admitted language. Neither check is a learner result; together they show that the three GPR11 moves can conflict (V1) and can also coexist (V2) on exact toys.

## Idea cards

## A. Close the old right through a separate clearing route

### 01. Clearing route disjoint from the renewal backing — primitive candidate
**Mechanism.** On default, certify B_d and extinguish the abandoned right using only carriers the next pair will not reserve; the next pair's reservation is admitted as soon as the close is published, not when it finishes. **Novelty vs nearest prior art.** Central-counterparty novation and [#226][parent] card 01 (proof-carrying close) already close a right; the bet is a learner-side close whose certificate is independent of the reissued backing, so close and renewal can overlap. **Cheapest first test.** Two-carrier momentum host, three alternating defaults; compare sequential close-then-reissue, a shared-carrier close and the disjoint route at equal clocks, counting timely next pairs. **Old-task retention check.** A/C, B_d and every earlier Bᵢ at the close, at the overlapping first write of the next pair, and after one ordinary suffix.

### 02. Close against an outstanding challenge window — primitive candidate
**Mechanism.** Publish the close optimistically, keep only the bytes needed to refute the defaulter's claim for a fixed window, then finalize and delete them. **Novelty vs nearest prior art.** Optimistic rollups keep fraud-proof data for a challenge window before finality; the learner version asks whether the needed evidence can be the live hidden state itself rather than stored data. **Cheapest first test.** V1 with a window of 0, 1 and 2 successor steps, an equal-byte stored-receipt rollup, and a lie that becomes visible only at step 2. **Old-task retention check.** A/C and B_d at finalization and on the first step after the window, including the case where a late refutation forces a recheck.

### 03. Revocation without a growing tombstone — improvement
**Mechanism.** Mark the abandoned right dead by changing the learner state it would need (its read no longer meets its guard), not by recording its ID. **Novelty vs nearest prior art.** Generation counters and CRLs record revocations; [#226][parent] F2 shows a wrapping counter is unsound under unbounded delay. This audits whether "state-based" revocation is sound or just moves the tombstone into weights. **Cheapest first test.** Replay F2's wrap with a late original token against a guard bound to the current slot; include a lawful update that makes the guard true again. **Old-task retention check.** A/C and installed Bᵢ after stale rejection and after the guard-reopening update.

### 04. Penalize a breached claim by reassigning its backing — primitive candidate
**Mechanism.** If the check detects under-reporting, the clearing route forfeits the defaulter's remaining entitlement to the next pair (Lightning's breach remedy), funding its fallback. **Novelty vs nearest prior art.** Breach remedies are standard in payment channels; nobody uses a detected optimizer-state misreport to fund a learner's fallback capacity. **Cheapest first test.** V1 plus one forfeitable slot; compare forfeiture, fresh reservation per pair and "ignore the lie" on timely pairs and refusals. **Old-task retention check.** B_d must still meet its floor after forfeiture (forfeit rights, never installed skills); A/C after the forfeited slot is rewritten.

### 05. Close that survives a defaulter who also lies — primitive candidate
**Mechanism.** Certify B_d's fallback against the claim *and* against the widest set the public record admits, choosing the cheaper sound one after the check. **Novelty vs nearest prior art.** Robust certification ([#232][shrink] card 14) checks one claim; the new piece is a close whose cost drops exactly when the check passes. **Cheapest first test.** V1's 25/2 history with a B_d fallback that needs multiplier ≥ 1/8; compare claim-only, public-hull-only and check-gated certificates. **Old-task retention check.** B_d's rare slice and A/C under both certificate choices.

### 06. Install the first fragment before its pair exists — primitive candidate
**Mechanism.** Publish B_d only together with its clearing certificate, so a default never leaves an uncloseable fragment; refuse first writes whose close would need the partner. **Novelty vs nearest prior art.** [#214][lease] card 02 keeps the first live write; this makes "closeable alone" an admission condition for it. **Cheapest first test.** Enumerate first writes on the parent's host; count how many are refused and whether any timely pair is lost versus [#214][lease] JRO2. **Old-task retention check.** A/C and every Bᵢ under the refused and admitted first writes.

## B. Check the incoming claim before any evidence-erasing shrink

### 07. Detect-then-shrink scheduler — primitive candidate (restates #232#18)
**Mechanism.** Order each renewal as: incoming partner's check step, then any contraction, then reservation. **Novelty vs nearest prior art.** [#232][shrink] card 18 proposes the order; this card makes it a renewal invariant over repeated defaults. **Cheapest first test.** V1 as a three-default relay with an adaptive adversary choosing which hop lies; compare shrink-first, check-first and authenticated chains at equal bytes. **Old-task retention check.** A/C on every path admitted after contraction and B_d after a detected lie.

### 08. Evidence-preserving shrink: contract only along honest-invisible directions — primitive candidate
**Mechanism.** Choose a truthful example whose contraction is a no-op on the honest image and keeps every harmful lie's image disjoint from it (unlike V1's hull clamp). **Novelty vs nearest prior art.** [#232][shrink] card 08 asks for distinct images; the bet here is "distinct from honest" only, a weaker and cheaper target. **Cheapest first test.** Search truthful g² values and clamp bounds in V1 for any that shrink the lie set while keeping all lies off {4, 8}; prove impossibility otherwise. **Old-task retention check.** A/C and B_d on the contracted states.

### 09. Public uncertainty claims priced by what they would hide — improvement
**Mechanism.** Charge a hop for the width its claim omits only along directions some live certificate reads (N5b harmless aliasing). **Novelty vs nearest prior art.** [#232][shrink] card 15 has the harmless-aliasing rule; this prices it in the escrow. **Cheapest first test.** N5b/N5c plus V1; compare uniform claim-width pricing. **Old-task retention check.** A/C on paths admitted under cheap claims.

### 10. A check that rides on useful successor work — primitive candidate
**Mechanism.** Make the incoming partner's first truthful C batch the check (V1), so verification costs no extra step and no stored receipt. **Novelty vs nearest prior art.** Proof-of-Learning ([2103.05633][pol]) replays training segments; here the evidence read is an already-needed update size. **Cheapest first test.** Compare V1's free check with a dedicated probe step and a replay challenge at equal C progress. **Old-task retention check.** C progress and A/C after the check batch, versus a no-check run.

### 11. Detection margin as a renewable budget — primitive candidate
**Mechanism.** Under float noise the check has a tolerance; spend it across renewals and refuse a renewal whose shrink would push the cumulative margin below the smallest harmful lie. **Novelty vs nearest prior art.** [#226][parent] card 15 has nonrenewable error for equivalence; this applies it to detectability. **Cheapest first test.** V1 with additive rounding of size ε, sweep ε and number of renewals, report ROC per cycle ([#232][shrink] card 20). **Old-task retention check.** A/C on falsely refused honest renewals.

### 12. Adaptive adversary that hides behind early contraction — improvement (mandatory)
**Mechanism.** Let the default schedule choose when to default and lie after seeing the shrink policy; the scheduler must still detect every harmful lie. **Novelty vs nearest prior art.** The triage row's required negative; [#226][parent] card 22 handles adaptive defaults without lies. **Cheapest first test.** Finite game on V1 states with lie/no-lie and default/no-default moves; solve exactly. **Old-task retention check.** A/C and all Bᵢ on the adversary's best trace.

### 13. Compressed state that keeps its audit — primitive candidate
**Mechanism.** When checkpoint compaction is the shrink, accept a coded moment only if it reproduces the update and keeps harmful-lie images distinguishable. **Novelty vs nearest prior art.** [Guarded Adam-state compression][guarded] (2611.00589) certifies the first restored update for every clipped gradient; it does not consider misreported histories. **Cheapest first test.** Apply a guarded 8-bit code to V1 slot values; count lies it merges with honest images versus FP32. **Old-task retention check.** A/C after restore and one ordinary step.

## C. Teach the next pair off the old receipt

### 14. Receipt-retiring prep order — primitive candidate
**Mechanism.** Reorder the next pair's already-planned C batches so the receipt's bit becomes irrelevant to the admitted suffix (V2), then delete R_d. **Novelty vs nearest prior art.** [#226][parent] card 09 closes a continuation cell; the new requirement is that raw evidence survives so a later audit is still possible. **Cheapest first test.** V2 with a delayed lie detection: reset, default order and prep order; score receipts held and lies still detectable. **Old-task retention check.** A/C and Bᵢ at each prep prefix and after the H₂H₂ suffix that re-exposes the bit.

### 15. Retire only receipts no live certificate reads — improvement
**Mechanism.** Reference-count receipts by the certificates citing them; delete on zero. **Novelty vs nearest prior art.** Garbage collection and [#226][parent] card 02; included to show which receipts teaching is really needed for. **Cheapest first test.** Count receipts left after three defaults with and without card 14. **Old-task retention check.** A/C and Bᵢ after each deletion.

### 16. Teach the dependency away, not the skill — primitive candidate
**Mechanism.** Choose successor batches so B_d's acquisition floor holds through a younger shared carrier, after which B_d's old receipt no longer protects anything. **Novelty vs nearest prior art.** Distillation and [witness examples (PR #163)][witness] replace a teacher; [#226][parent] card 05 moves backing. The difference: retirement is gated on the check passing, so a lying defaulter's B_d is rechecked, not inherited. **Cheapest first test.** Two-carrier host with an honest and a lying defaulter; compare distillation, card 05 and check-gated migration. **Old-task retention check.** B_d's rare probe at both carrier switches and A/C after reuse.

### 17. Receipt-free next pair under a hidden alias — primitive candidate
**Mechanism.** Admit the next blind pair with no receipt at all once a closed cell covers every alias the public record allows (not just the claim). **Novelty vs nearest prior art.** [#226][parent] card 16 precommits against several witnesses; this precommits against the defaulter's possible lies. **Cheapest first test.** V2 with three aliases, one outside the claim; compare receipt-holding and query-first arms. **Old-task retention check.** A/C and Bᵢ under the out-of-claim alias.

### 18. Receipt half-life from ordinary training — improvement
**Mechanism.** Measure how many successor steps it takes for a receipt's information to stop changing any admitted decision under ordinary (unordered) training. **Novelty vs nearest prior art.** [#226][parent] card 13 expires proofs; this is the passive baseline cards 14 and 16 must beat. **Cheapest first test.** Random orders on V2 and a tanh host; distribution of receipt-irrelevance time. **Old-task retention check.** A/C at the irrelevance time.

### 19. Teach so the next default will be cheap to close — primitive candidate
**Mechanism.** Choose the next pair's order to make its own future first fragment closeable through a disjoint route (card 01) if it later defaults. **Novelty vs nearest prior art.** [Successor-funded returns (PR #206)][funded] buys recovery with learning; this buys future closeability. **Cheapest first test.** Two consecutive defaults; compare orders optimized for current service only. **Old-task retention check.** A/C and Bᵢ after both closes.

## D. Make the three moves earn their coupling

### 20. Constant live receipts across defaults with lies — primitive candidate
**Mechanism.** Run check-then-shrink, clearing route and receipt-retiring prep every cycle; claim at most one live receipt at any time. **Novelty vs nearest prior art.** [#214][lease] card 18 bounds entitlements, not receipts under misreports. **Cheapest first test.** Three defaults, overlapping arrivals, one liar, and a suffix that exposes the hidden slot (the GPR11 first test); compare cached receipts, separate fallback capacity and charged probes. **Old-task retention check.** Count installed jobs and later blind pairs separately; A/C and all Bᵢ after the exposing suffix.

### 21. Best-stack control: rollup window + authenticated chain + reset — improvement (mandatory)
**Mechanism.** Give the stack the same bytes, check work and clocks. **Novelty vs nearest prior art.** The triage row's controls; if it ties, GPR11 is composition. **Cheapest first test.** Run the card-20 setup with the stack. **Old-task retention check.** Per-cut A/C and Bᵢ noninferiority before comparing receipts.

### 22. Fresh reservations per pair as the capacity ceiling — improvement (mandatory)
**Mechanism.** Never reuse backing; measure how much capacity GPR11 actually reclaims. **Novelty vs nearest prior art.** Standard; it is the "no renewal" ceiling on safety and floor on capacity. **Cheapest first test.** Same as card 20 with growing capacity. **Old-task retention check.** A/C and Bᵢ at peak capacity.

### 23. Does any shrink both retire the receipt and keep evidence? — primitive candidate
**Mechanism.** Search for a truthful word that does V2's retirement and V1's detectability in one pass on a host where the receipt and the lie live on the same slot. **Novelty vs nearest prior art.** The joint-primitive question of [#232][shrink] Q4, transported to renewal. **Cheapest first test.** Exhaustive search over three-batch words on a two-coordinate RMSprop host; prove impossibility if none. **Old-task retention check.** A/C and Bᵢ along the found word.

### 24. Renewal under learner-law drift — primitive candidate
**Mechanism.** Re-verify the clearing route and receipt irrelevance when the successor's optimizer or loss changes between cycles. **Novelty vs nearest prior art.** [#226][parent] card 19 for quotient proofs. **Cheapest first test.** Switch β₂ from 1/2 to 3/4 between cycles in V1; count invalidated closes. **Old-task retention check.** A/C and Bᵢ at the first update under the new law.

## Ranked deeper questions

1. **Can one renewal keep at most one live receipt across repeated defaults while every harmful misreport stays detectable, beating the stack of challenge windows, authenticated chains and reset at equal bytes?** Cards 07, 14, 20, 21. Kill if the stack ties on timely pairs, receipts and detection at matched A/C/B retention.
2. **Is there a shrink that is evidence-preserving for every harmful lie, not just a no-op on honest histories?** Cards 08, 13, 23. V1 shows the claimed-hull clamp fails; if no truthful contraction keeps lies off the honest image, GPR11 must always check first and pay for the check's latency.
3. **Does ordinary successor training retire receipts fast enough to matter?** Cards 14, 16, 18. If unordered training already makes receipts irrelevant within one cycle, ordering is an improvement at most.
4. **Can the clearing route be independent of the renewal backing on a real shared host?** Cards 01, 05, 19. If B_d's close always needs the carrier the next pair reserves, close and renewal serialize and the coupling buys nothing over fresh reservations.

[parent]: https://github.com/manojbajaj95/cl/pull/226
[lease]: https://github.com/manojbajaj95/cl/pull/214
[shrink]: https://github.com/manojbajaj95/cl/pull/232
[gpr11]: https://github.com/manojbajaj95/cl/blob/6495bf986ca24f828f281ca2e429645b452c3ea3/ideas/flood/cross-pool-53.md
[triage]: https://github.com/manojbajaj95/cl/blob/2ae3dc935108edbb954849f7e09d6063e7a9f1ce/reviews/flood-triage.md#L347
[ledger]: https://github.com/manojbajaj95/cl/blob/2ae3dc935108edbb954849f7e09d6063e7a9f1ce/reviews/idea-ledger.md
[funded]: https://github.com/manojbajaj95/cl/pull/206
[witness]: https://github.com/manojbajaj95/cl/pull/163
[pol]: https://arxiv.org/abs/2103.05633
[guarded]: https://arxiv.org/abs/2611.00589
