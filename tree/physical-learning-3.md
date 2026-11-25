# Physical learning 3 — beating the extremum stack, and AC demagnetisation as bounded unlearning

Child of [PR #342](https://github.com/manojbajaj95/cl/pull/342) (`tree/physical-learning-2.md`). This node follows the reviewer's two score-3 ideas for #342 (`reviews/flood-triage.md`, row 467):

- **P01, the path-dependent target.** The reviewer's bar: beat an explicit one-bit latch (a Schmitt trigger on h) and an explicit extremum-stack table at equal bytes, on depth-k nested reversals beyond one bit. Its other controls: the equal-byte gated two-delta block, a nearest-mixture lookup, a GRU on the h history, EWC and replay, and A/B retention after 20 nested reversals.
- **P07, AC demagnetisation as bounded unlearning.** Its controls: gradient ascent and selective synaptic dampening at equal steps, deleting the band's entries from an explicit extremum-stack table, a poison band overlapping A or B, and A/B retention with B′ removed.

`reviews/idea-ledger.md` was read first. Each card is labelled PRIMITIVE or IMPROVEMENT, names its strongest control, and has an old-task retention check in its first test. The node avoids the reviewer's narrowing lines; in particular, no card measures how fast erased content comes back (relearnability). Ideas only, no GPU.

## What the literature check changed

I searched alphaXiv `discover_papers` and the Hugging Face papers index on 2026-11-25 and read the abstracts of the closest hits. Two results reshape this node.

1. **The extremum stack is provably the optimal memory.** Every rate-independent causal functional is a function of the Preisach extremum stack Π_n, and Π_n is a Shannon-minimal and Kolmogorov-minimal sufficient statistic (Frydrych, [2606.04784](https://arxiv.org/abs/2606.04784), [2606.05245](https://arxiv.org/abs/2606.05245); the same author's Preisach Attention, [2605.23603](https://arxiv.org/abs/2605.23603)). So a Preisach bank cannot beat an explicit stack table on *information*. It can only win on:
   - (a) bytes, when the readout f(Π) has structure that a table must enumerate;
   - (b) generalisation to turning-point values never seen in training;
   - (c) robustness when the drive is noisy and the exact stack fills with spurious extrema;
   - (d) where the state lives (inside trained weights, sharing a trunk) rather than in a side controller.
   
   Every R card below targets one of (a)–(d) and states which.
2. **Exact unlearning by deleting additive, region-indexed content exists.** Quantized Sufficient Statistics ([2610.07197](https://arxiv.org/abs/2610.07197)) keeps a frozen schema plus sum-decomposable content indexed by quantized regions, so deleting is exact subtraction. Related unlearning-by-design work: SISA sharding ([1912.03817](https://arxiv.org/abs/1912.03817)), its PEFT variants ([2406.16257](https://arxiv.org/abs/2406.16257)), IDSISA ([2611.06519](https://arxiv.org/abs/2611.06519)) and key deletion (MUNKEY, [2603.15033](https://arxiv.org/abs/2603.15033)). Forget-set-free unlearning also exists ([2604.10636](https://arxiv.org/abs/2604.10636), [2511.13116](https://arxiv.org/abs/2511.13116), [2508.15127](https://arxiv.org/abs/2508.15127)). AC demagnetisation is therefore close to QSS with regions over the *drive history* instead of the input. Its possible gains are four:
   - erasure keyed to a condition band without any per-example index;
   - no forget data;
   - a decaying-drive procedure that also leaves a defined default state (anhysteretic);
   - handling bands that overlap kept regimes.
   
   The D cards are scored against QSS and SISA as well as the reviewer's controls.

"No direct hit" below means no paper in the top results did the card's specific thing. It is not proof of novelty.

Shared toys (from #342):
- **Mix toy.** A 2-D input, 4-class rules A/B, drive h ∈ [0, 1], a 2-layer MLP of width 64.
- **Depth-k target.** The label rule at the current h is a fixed function of the top k entries of Π_n.
- **Byte accounting.** It counts every stored float or bit in a bank, table, latch or GRU state, plus its readout parameters.

---

## R. The path-dependent target, against the latch and the stack table

### R01 · The fair depth-k benchmark — PRIMITIVE, H — targets (a)–(c)
- **Mechanism.** Build a family of targets y = f(Π_n, x) where f reads the top k turning points, k ∈ {1, 2, 4, 8}. Three versions: f additive over turning points (Everett-style), f a generic lookup over stack signatures, and continuous-valued turning points. A one-bit latch solves only k = 1; an explicit stack table solves every case if given enough bytes. Report accuracy against bytes for the bank, the table, the latch cascade, the GRU, the nearest-mixture lookup and the gated two-delta block. This is the reviewer's gate, run as a frontier rather than one point.
- **Novelty vs prior art.** Frydrych's results ([2606.05245](https://arxiv.org/abs/2606.05245)) give the information floor but no continual-learning benchmark. Recurring-drift benchmarks (MICE [2610.36585](https://arxiv.org/abs/2610.36585)) have no nested reversals. No direct hit.
- **Cheapest first test.** CPU sweep of k × 3 target types × 4 byte budgets × 3 seeds. Falsifier: the bank is never on the accuracy-per-byte frontier above the stack table for any target type.
- **Retention check.** A at h = 0 and B at h = 1 after 20 nested reversals, at each byte budget, against EWC and equal-budget replay.

### R02 · Additive readouts: linear bytes against exponential tables — PRIMITIVE, H — targets (a)
- **Mechanism.** In the classical Preisach model the output is a sum of hysteron contributions (Everett function), so it represents 2^k stack configurations with O(k) to O(k²) numbers. A table that keys on stack signatures needs one entry per signature. If real path-dependent targets are close to additive, the bank's byte cost grows polynomially in depth where the table's grows exponentially.
- **Novelty vs prior art.** Everett additivity is textbook magnetics. Using it as the reason a learned bank beats a signature table at equal bytes is not found.
- **Cheapest first test.** R01's additive target with k = 8. Compare the bank against a signature table under a byte cap that fits 2^5 signatures. Falsifier: the capped table matches the bank, which would mean the target's signature use is sparse.
- **Retention check.** Per-signature accuracy for old regimes after 20 reversals.

### R03 · Non-additive readouts: where the bank should lose — IMPROVEMENT, M — calibrates (a)
- **Mechanism.** Generic signature targets (an XOR over turning points) break additivity. Measure how far the bank falls behind the table, and whether a second-order Preisach (pairwise hysteron products) or a small MLP readout over hysteron states closes the gap at equal bytes.
- **Novelty vs prior art.** Non-additive and "moving" Preisach variants exist in magnetics (Della Torre). IMPROVEMENT: it bounds R02's claim.
- **Cheapest first test.** XOR-of-turning-points target, k = 4. Falsifier for the whole R branch: the bank plus MLP readout needs more bytes than the table even at k = 2.
- **Retention check.** As R01.

### R04 · Off-grid turning points: generalising what the table cannot index — PRIMITIVE, H — targets (b)
- **Mechanism.** A stack table indexes the turning points it has seen, quantised. A bank with smooth relays and a learned density (#342 P03) interpolates the output at turning-point values between training ones. Train on turning points at h ∈ {0.1, 0.3, 0.5, 0.7, 0.9} and test at reversals at 0.2, 0.4, 0.6, 0.8.
- **Novelty vs prior art.** Interpolation in hysteresis-model identification is standard ([2611.23240](https://arxiv.org/abs/2611.23240), [2202.07747](https://arxiv.org/abs/2202.07747)). It has not been used as the advantage of a continual learner over an exact extremum memory.
- **Cheapest first test.** Compare the bank against a stack table with linear interpolation between stored entries, at equal bytes. Falsifier: the interpolating table ties.
- **Retention check.** On-grid A/B accuracy after off-grid excursions.

### R05 · Noisy drives: the stack table fills with spurious extrema — PRIMITIVE, H — targets (c)
- **Mechanism.** An estimated drive (#342 P10) jitters, and every jitter adds a turning point to the exact stack, so a byte-capped table evicts real history. Hysterons of width w ignore reversals smaller than w and wipe them out, so the bank compresses noise for free.
- **Novelty vs prior art.** Noise-robust extremum detection (dead-band filters, rainflow gating) is standard signal processing, so the fair control is a stack table behind a dead-band filter of the same width. No hit for this comparison.
- **Cheapest first test.** Drive noise σ ∈ {0, 0.02, 0.05, 0.1}. Compare the bank against a raw table and against a dead-band-filtered table at equal bytes. Falsifier: the filtered table ties at every σ.
- **Retention check.** A/B accuracy after 20 noisy nested reversals.

### R06 · Learned latch cascade: is the bank more than k Schmitt triggers? — IMPROVEMENT, M — targets (d)
- **Mechanism.** A cascade of k latches at different thresholds is a k-hysteron Preisach bank. The only difference left is whether thresholds and deltas are learned jointly with a shared trunk by gradient, or placed by hand with a fixed readout. This card isolates that difference.
- **Novelty vs prior art.** Cascaded Schmitt triggers are circuit design ([2006.08415](https://arxiv.org/abs/2006.08415)). IMPROVEMENT: it decides whether "learned" matters.
- **Cheapest first test.** Hand-placed cascade with a trained readout against a jointly trained bank, at equal bytes, on R01. Falsifier: the hand-placed cascade ties.
- **Retention check.** As R01.

### R07 · State inside the weights versus a side controller — PRIMITIVE, M — targets (d)
- **Mechanism.** In the bank, the history state selects deltas inside a shared trunk, so features learned under A help B. A side controller (the table) picks between separate heads. The claim: at equal bytes, sharing the trunk improves new-regime sample efficiency without hurting old regimes.
- **Novelty vs prior art.** Hard parameter sharing with task-gated heads is standard multi-task learning. The new part is gating by the drive history.
- **Cheapest first test.** Bank-in-trunk against table-plus-heads with equal total bytes. Measure samples to 90% on a third regime C. Falsifier: no sample-efficiency gain.
- **Retention check.** A/B accuracy after C.

### R08 · In-context stack against persistent bank — PRIMITIVE, M — targets (d)
- **Mechanism.** Preisach Attention computes stack functionals in context from the visible token history. A continual learner sees each batch once and cannot keep the whole h history. Compare a PAL-style layer with a truncated history window (equal bytes of cache) against a bank whose state persists in its weights.
- **Novelty vs prior art.** [2605.23603](https://arxiv.org/abs/2605.23603) is the direct comparison. No hit for the persistence question.
- **Cheapest first test.** History windows of 16 to 256 steps. Falsifier: a 64-step window ties the bank at k = 4.
- **Retention check.** As R01.

### R09 · Amplitude-ordered forgetting under a fixed budget — PRIMITIVE, M — targets (a)
- **Mechanism.** With too few hysterons, a bank first loses the smallest inner loops, because wiping-out removes them. A byte-capped stack table evicts by recency or depth. On targets where large excursions matter most (a big regime swing outweighs small wobbles), the bank degrades gracefully where the table drops the wrong entries.
- **Novelty vs prior art.** Rainflow and peak-picking compress load histories by amplitude in fatigue analysis. Not used as a CL memory-eviction rule. Control: a table with amplitude-ordered eviction.
- **Cheapest first test.** Budget sweep with mixed-amplitude reversals. Falsifier: the amplitude-evicting table ties.
- **Retention check.** Accuracy at large-excursion regimes after the budget is exceeded.

### R10 · Online identification of the bank from the stream — PRIMITIVE, M
- **Mechanism.** Without known turning points or FORC protocols (#342 P04), identify the Preisach density online. This uses recursive least squares over hysteron states, whose convergence under stochastic inputs is proven in control ([1503.02051](https://arxiv.org/abs/1503.02051)). New thresholds are added where residuals concentrate.
- **Novelty vs prior art.** Recursive Preisach identification is from control. Applying it to a continual learner's own weight deltas is not found.
- **Cheapest first test.** Online identification against an offline-fit bank and against the table, on R01. Falsifier: the online bank is more than 5 pp below offline after 1,000 steps.
- **Retention check.** As R01.

### R11 · Natural path-dependent streams — PRIMITIVE, M
- **Mechanism.** The P branch needs data where the correct output at a given condition depends on history. Candidates: physical hysteretic systems (accelerator magnets, [2202.07747](https://arxiv.org/abs/2202.07747); tendon robots, [2404.07168](https://arxiv.org/abs/2404.07168); Bouc–Wen structures, [2411.02776](https://arxiv.org/abs/2411.02776)); worker acceptance modelled as Preisach ([2606.04916](https://arxiv.org/abs/2606.04916)); and user-preference persistence in agent logs. Frame each as a continual-learning stream whose drive is a measured condition.
- **Novelty vs prior art.** These datasets model the hysteretic system itself. Using them as CL streams for a learner that must not forget regimes is not found.
- **Cheapest first test.** Bouc–Wen simulation stream on CPU, comparing the bank against the table and the GRU. Falsifier: the target turns out to be rate-dependent, so the stack is not sufficient and every rate-independent model fails.
- **Retention check.** Accuracy on early loading regimes after later cycles.

### R12 · Agent tension drive: a path-dependent register for user state — PRIMITIVE, M
- **Mechanism.** For an agent, the right register (formal or casual, cautious or fast) at a given tension level depends on whether the conversation is escalating or calming. A hysteron bank over a scalar tension estimate selects lesson sets. It must beat a one-bit latch, which captures escalating versus calming, on multi-reversal sessions.
- **Novelty vs prior art.** Dialogue-state tracking keeps explicit state. No hit for hysteretic register selection.
- **Cheapest first test.** A tabular simulated user with depth-3 nested tension reversals. Falsifier: the latch ties.
- **Retention check.** Success on the calm-user baseline task after tense sessions.

### R13 · Adversarial drives and a worst-case error bound — PRIMITIVE, M
- **Mechanism.** For a bank with threshold resolution δ, the output error under any drive path is bounded by the Everett mass in a δ strip, a structural bound. Generate adversarial reversal sequences against the bank and against the GRU; only the bank should hold its bound.
- **Novelty vs prior art.** Robustness of recurrent nets to adversarial sequences is studied; no hit for this bound in continual learning.
- **Cheapest first test.** Search for adversarial drives with a genetic algorithm on CPU. Falsifier: the bank's worst-case error exceeds its δ bound, or the GRU's worst case is no worse.
- **Retention check.** Worst-case A/B accuracy.

### R14 · Bank in the readout only — IMPROVEMENT, L
- **Mechanism.** Put the bank in the last layer only, with the trunk frozen after A. This is the cheapest placement and a lower bound for R07.
- **Novelty vs prior art.** IMPROVEMENT: a placement choice.
- **Cheapest first test.** Readout-only against full-trunk bank at equal bytes. Falsifier: readout-only ties.
- **Retention check.** As R01.

## D. AC demagnetisation as bounded unlearning

### D01 · The band-erasure guarantee, stated and tested — PRIMITIVE, H
- **Mechanism.** A decaying oscillating drive centred in band [h₁, h₂] with amplitude a(t) → 0 resets every hysteron with α, β in the band to the state the final drive implies, and leaves hysterons outside the band unchanged. Output change outside the band is then exactly zero for additive readouts. Test that exactness, and how much leaks through a shared trunk.
- **Novelty vs prior art.** Closest is QSS ([2610.07197](https://arxiv.org/abs/2610.07197)): exact subtraction of region-indexed additive content. Here regions are bands of drive history, and the eraser is a drive procedure that needs no index. No hit for demagnetisation as unlearning.
- **Cheapest first test.** Poison regime B′ at h ∈ [0.6, 0.8]. Compare demagnetisation against all of the reviewer's controls (gradient ascent and selective synaptic dampening at equal steps, deleting the band from an explicit stack table) and against QSS-style subtraction. Falsifier: demagnetisation leaks more off-band change than QSS, or than deleting the band from the table.
- **Retention check.** A and B accuracy after unlearning; B′ accuracy must fall to chance.

### D02 · Forget-set-free band unlearning — PRIMITIVE, H
- **Mechanism.** Demagnetisation needs only the band, not the examples learned there. This covers deletion requests where the data is gone or was never kept ("forget everything learned while the mix was in [0.6, 0.8]").
- **Novelty vs prior art.** Forget-set-free unlearning exists ([2604.10636](https://arxiv.org/abs/2604.10636); source-free [2508.15127](https://arxiv.org/abs/2508.15127); zero-glance [2511.13116](https://arxiv.org/abs/2511.13116)). It works by suppressing classes or identities, not condition bands, and gives no structural bound.
- **Cheapest first test.** Compare demagnetisation with no data against the forget-set-free method of 2604.10636 given the band's class labels. Falsifier: the baseline removes B′ with no more collateral.
- **Retention check.** A and B accuracy.

### D03 · Anhysteretic reset to a chosen default — PRIMITIVE, M
- **Mechanism.** Demagnetising around a DC bias h* leaves the anhysteretic state: the history-free state that h* alone implies. To unlearn a band and set it to a defined default (for example, regime A's behaviour), demagnetise with bias at A's h.
- **Novelty vs prior art.** Unlearning targets in prior work are a retrained model or random labels. Setting a history-free default for a band is not found.
- **Cheapest first test.** Anhysteretic reset against zero-bias demagnetisation and against fine-tuning the band to A labels. Falsifier: fine-tuning ties with equal collateral.
- **Retention check.** B accuracy outside the band.

### D04 · Thermal demagnetisation: erase by coercivity class — PRIMITIVE, M
- **Mechanism.** Heating above a blocking temperature erases hysterons with coercivity (α − β)/2 below a cutoff and keeps hard ones. In the bank this forgets weakly held, narrow-loop memories first. It joins the T branch of #342 and runs only if T03 passes.
- **Novelty vs prior art.** Unlearning by memorisation strength exists (forget the least-memorised examples); erasing by hysteron coercivity is not found.
- **Cheapest first test.** Coercivity-cutoff erasure against magnitude pruning of deltas at equal parameter change. Falsifier: pruning ties.
- **Retention check.** Wide-loop (deep) regime accuracy after erasure.

### D05 · Decrement law for clean demagnetisation — IMPROVEMENT, M
- **Mechanism.** If a(t) decays too fast, residual magnetisation remains. Derive the largest per-cycle decrement that still resets every hysteron in the band, given the threshold spacing, and use it to bound the cost of erasure.
- **Novelty vs prior art.** Standard in magnetics practice. IMPROVEMENT.
- **Cheapest first test.** Decrement sweep. Falsifier: residual state is independent of the decrement.
- **Retention check.** A/B off-band accuracy.

### D06 · Structural unlearning certificate — PRIMITIVE, M
- **Mechanism.** After demagnetisation, the in-band hysteron states are a known deterministic function of the procedure. A verifier checks the states directly instead of running membership inference.
- **Novelty vs prior art.** Unlearning audits rely on attacks and extraction ([2505.24379](https://arxiv.org/abs/2505.24379), [2606.16110](https://arxiv.org/abs/2606.16110)). QSS and SISA give exactness by construction. This card adds a check that needs no retained data. It is an audit, not a meter of learning, and is kept minimal.
- **Cheapest first test.** Certified bank against SISA's retrain-from-shard proof, comparing proof bytes and cost. Falsifier: the certificate misses leakage through the trunk that an extraction attack finds.
- **Retention check.** A/B accuracy after certified erasure.

### D07 · Adaptive threshold refinement near kept regimes — PRIMITIVE, H
- **Mechanism.** If the poison band overlaps A or B (the reviewer's hard control), coarse hysterons straddle the boundary and erasure takes kept content with them. Split hysterons finely near boundaries where kept and poison regimes meet, before erasing, so the cut is surgical.
- **Novelty vs prior art.** Adaptive refinement is standard in mesh and quantisation. Using it as a pre-unlearning step for overlapping bands is not found. Control: QSS with finer quantisation at equal bytes.
- **Cheapest first test.** Poison band overlapping B by 25%. Compare refined demagnetisation against plain demagnetisation, against fine-quantised QSS and against gradient ascent. Falsifier: fine QSS ties.
- **Retention check.** B accuracy on the non-overlapping part.

### D08 · Band erasure over source trust for agent lessons — PRIMITIVE, M
- **Mechanism.** In #342 P11's agent lesson bank, let the drive be a trust score of the lesson source. If a source is later found compromised over a trust range, demagnetise that range. Lessons admitted only through it leave; lessons with other support stay.
- **Novelty vs prior art.** Agent memory-poisoning defences filter at write time (pre-commit gating, [2608.05810](https://arxiv.org/abs/2608.05810)). No hit for removal by a trust band after the fact.
- **Cheapest first test.** A tabular agent with 30 lessons, 5 from a source later marked bad. Compare against deleting by source tag (the oracle) and against rerunning curation. Falsifier: demagnetisation removes fewer bad lessons or more good ones than rerunning curation.
- **Retention check.** Success on tasks served by good lessons.

### D09 · Continuous-index SISA — PRIMITIVE, M
- **Mechanism.** SISA shards data into discrete slices. Here each user or source maps to a drive value and the bank shards by threshold bands, so a deletion is a demagnetisation of a narrow band with no retraining. Many users share a trunk while erasures stay local.
- **Novelty vs prior art.** SISA ([1912.03817](https://arxiv.org/abs/1912.03817)), IDSISA ([2611.06519](https://arxiv.org/abs/2611.06519)) and QSS are the nearest prior art. The new part is a continuous index with hysteretic sharing.
- **Cheapest first test.** 50 synthetic users and 10 deletion requests. Compare against SISA with 10 shards and against QSS at equal bytes. Falsifier: SISA matches retention at lower cost.
- **Retention check.** Accuracy for non-deleted users.

### D10 · Rotating-field demagnetisation for vector drives — PRIMITIVE, L
- **Mechanism.** For #342 P05's simplex drives, erase a region of the simplex with a rotating, decaying field, as in vector-magnet demagnetisation.
- **Novelty vs prior art.** Magnetics practice. No CL hit.
- **Cheapest first test.** Erase one simplex corner among three regimes. Falsifier: off-region leakage above 1 pp.
- **Retention check.** Accuracy at the other two vertices.

### D11 · Deprecation demagnetisation to recycle capacity — PRIMITIVE, M
- **Mechanism.** When a regime ends for good (an API retired), demagnetise its band, and assign the freed hysterons to new thresholds where #342 P04 or R10 finds residual mass. Bank capacity is recycled with an erasure bound instead of growing.
- **Novelty vs prior art.** Capacity reuse by pruning and regrowth (PackNet, continual backprop) has no bound on what the pruning removes. No hit.
- **Cheapest first test.** A stream of 6 regimes with a fixed bank and 2 retired. Compare against a pruning-based reuse rule. Falsifier: equal retention of live regimes.
- **Retention check.** Live-regime accuracy after recycling.

### D12 · Erasure of a temperature band in the thermal bank — PRIMITIVE, L
- **Mechanism.** In #342 T09 (temperature as the drive), demagnetise a temperature band to unlearn the task stored at that temperature. This runs only after P01 and T03 pass.
- **Novelty vs prior art.** No hit.
- **Cheapest first test.** Erase task 2 of 3 in a thermal bank. Falsifier: tasks 1 and 3 lose more than 1 pp.
- **Retention check.** Tasks 1 and 3.

---

## Ranked deeper questions

1. **Is there a real target where the bank sits above the stack table on accuracy per byte?** The minimal-sufficiency theorem rules out an information win, so the R branch lives or dies on R02 (additive readouts), R04 (off-grid values) and R05 (noisy drives). Run R01's frontier first. If the dead-band-filtered, interpolating table ties everywhere, close the P branch.
2. **Does demagnetisation add anything over QSS-style exact subtraction?** D01 and D07 decide it: only off-band leakage through a shared trunk, and overlapping bands, can separate them. If QSS with a drive-band index ties, D becomes a re-description of QSS.
3. **Do natural continual-learning streams contain rate-independent path dependence?** R11 is the bridge from toys to reality. If real streams are mostly rate-dependent, the stack is not sufficient and every Preisach card loses its guarantee.
4. **Can erasure keyed to a condition band replace per-example deletion in practice?** D02, D08 and D09 test forget-set-free, trust-band and continuous-shard deletion. These are the cases where neither QSS nor SISA has the needed index.
5. **Where should the history state live?** R07, R08 and R14 compare inside-trunk, in-context and readout-only placements. The answer sets the engineering form of any surviving P-branch method.
