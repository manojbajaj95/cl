# Merged ideas, batch 1 (cross-section proposer)

Source: `reviews/idea-ledger.md` and `reviews/compute-requests.md` at PR #6 (b1a9f82), plus the pilot PRs they link. Every card follows the ledger rule for merges: it names each partial result it reuses, the **stacked** strongest baseline of its parts at equal tokens/compute, and the smallest test that isolates an interaction that stack cannot reproduce. All lesson/memory arms include same-length filler and a source-fitted entropy-matched no-lesson temperature.

Prior-art screen (alphaXiv, Nov 2026): Override Gap 2604.23750 (margin account of context-vs-adapter conflict; SLB layer boosting; CA probe chooses adaptation strength), Cortex 2610.20399 (consolidation-retention frontier), Engram Injection 2610.15882 (temporal validity of parametric memory), ALLOT 2609.32344 (budgeted hybrid retrieval/parametric routing), EASE-KV 2611.11299, OPCD 2602.12275, Local Conflict/Targeted Repair 2606.02398. None measures correctability of consolidated memory at matched margin as a function of the consolidation route, or uses it as a plasticity signal.

---

## MX1. Route-dependent correctability: consolidate lessons where later context can still override them

**Parts merged (5):** A3-anchor anomaly (PR #33: the 1.5B follow index was +90.97 pp [79.17, 99.38] in the natural position-prior arm vs +10.42 pp [0.00, 25.56] after a post-score offset to the original prior. The margin ranges overlapped, but labels, menu order, and baseline leader also differed); R1 correctability erosion (PR #30: an absorption-matched decline of 42.86 pp [−82.86, −2.86] from cycle 1 to 3, short of the prespecified −15 pp bound; lower LR was +20 pp [0, 60] vs keep at cycle 3 on 12 matched probes); M3 double dosing (PR #30: evicting after cycle 1 left absolute calibration error 13.25 pp [3.70, 22.81] above nominal context alone on the frozen model); N1 layer locality (PR #35: masks reduced held-out harm 37.43% vs a global bias matched on **training** gain); Override Gap SLB (2604.23750: layer allocation of an adapter matters beyond norm).

**Claim.** Whether a consolidated lesson can later be overridden in context is set by *where in the network the consolidation writes the prior*, not only by how large the resulting margin is. A consolidation that lands the prior late (readout-side adapter, last-block LoRA) behaves like #33's position prior (overridable); one that lands it in mid layers behaves like the anchored prior (sticky). That gives a consolidation method, **late-binding consolidation**, that keeps absorption while preserving correctability.

**Interaction the stack cannot reproduce.** Lower LR, early stopping and label smoothing all act through margin. The claim is a correctability gap *at matched absorption and matched post-consolidation margin*, across routes.

**Stacked control (equal steps, tokens, absorption):** lower-LR mid-layer LoRA + margin-matched label smoothing + keep-context copy (M3) + entropy-matched T + filler.

**Smallest isolating test.** `pilots/m3/` world, Qwen2.5-0.5B (then 1.5B). Consolidate the same 10 graded lessons by 3 routes: mid-layer LoRA (layers 8-16), last-2-block LoRA, readout logit adapter. Tune each to matched absorption (±2 pp) and bin probes by post-consolidation margin. Measure the follow index of a contradicting in-context directive (paired swap design from PR #31), per margin bin.

**Kill line.** Dead if, in shared margin bins, route differences in follow index are < 10 pp (CI), or margin-matched label smoothing on mid-layer LoRA ties the best route.

**Cost.** Unbenchmarked CPU estimate: ~1.5 h for 0.5B (3 routes x 2 seeds + probes), ~3 h for 1.5B. The 0.5B M3 main run took 1,196.6 s on eight CPU threads; route matching and larger-model runs are new work.

---

## MX2. Margin-gated lesson visibility: show a lesson only where it can flip the decision

**Parts merged (6):** #31 (155/160 directed flips at prior margin < 1 logit; the ledger's post-hoc estimate of directive shift versus filler was ~0.6–1.0 logit); N1 (PR #35: masks cut held-out harm 37.43% vs training-gain-matched bias but kept only 82.84% of full-visibility held-out gain); M2 (PR #35: on returns, outcome-trained salience +13.33 pp over entropy T but −0.42 pp vs each of LOO and recency; neither difference versus those two controls was established); B3 (PR #28: real lessons hurt continuous log-prob more than filler, 1.114 vs 0.670 nats, but the accuracy drop was smaller, 3.70 vs 7.08 pp); EASE-KV signed per-memory biases; ALLOT / Override-Gap CA (route by a base-model probe).

**Claim.** N1's harm cut and its lost gain have one cause: lessons are useful only in states whose base margin is below the directive's shift, and harmful (log-prob damage, B3) in high-margin states they cannot flip. A per-state gate on base margin (no training, one extra no-lesson forward) should keep ≥ 95% of full-visibility gain while matching or beating N1's harm cut.

**Interaction.** Margin x visibility: the stack below gates by *what the lesson is about* (retrieval, salience, recency), never by *whether this state is flippable*.

**Stacked control:** literal/embedding retrieval gating + LOO + recency + N1 learned masks + entropy T + filler, equal tokens.

**Smallest isolating test.** First rerun held-out N1 scoring with per-state no-lesson logits, gains and harms saved; the committed results aggregate by lesson and do not contain these traces. Stratify by the no-lesson margin. Gate: ≥ 70% of harm in states above the median margin, ≥ 70% of gain below it. If it passes, run an **unkeyed** variant of the M2/N1 valve world (station keys removed so literal retrieval cannot select), and compare margin-gated visibility vs the stack.

**Kill line.** Dead at the reanalysis gate, or if margin gating does not beat the stack by ≥ 5 pp returning-regime accuracy (or ≥ 0.1 nats harm at equal gain) in the unkeyed world.

**Cost.** Use N1's 21m57s and M2's 32m27s CPU runs as reference points; the trace collection and unkeyed variant are not timed. The statistical reanalysis itself needs no further inference once the traces are collected.

**Prior-art risk.** Override Gap CA picks adaptation strength per document from a base probe; MX2 gates per decision state for context memory. Reviewer should check this distinction holds.

---

## MX3. Correctability as a label-free plasticity meter

**Parts merged (4):** plasticity reserve (PR #9: current-loss-matched writes showed a 4.9 pp spread in **relative** gain; labeled next-task readiness oracle ρ = +0.704, but Gramian and current-task readiness failed. PR #21: jointly matching current loss and retention under projected SGD left 0.458 pp relative spread and 0.091 absolute MSE points, below the gate); R1 (PR #30: suggestive in-context correctability erosion, below its decision threshold); MX1's hypothesized route effect; A3-anchor (#33).

**Claim.** In-context correctability and in-weight plasticity are the same resource. Among consolidations with equal absorption, the one whose decisions remain more overridable by a contradicting directive (cheap: forward passes only, no labels for the next task) learns the next task faster.

**Interaction.** No part predicts the other alone: reserve had no working predictor; R1 measured correctability without a downstream plasticity endpoint.

**Stacked control:** optimization readiness (2605.09044), effective rank, gradient norm on the next task's first batch, post-consolidation margin, random choice.

**Smallest isolating test.** M3 world, 0.5B. Make 8 equal-absorption consolidations (LR, rank, seed, MX1 routes). Variance gate first (ledger rule): next-lesson-set gain spread must exceed seed spread. Then Spearman between follow index on held-out contradicting directives and next-set gain after a fixed fine-tune budget.

**Kill line.** Dead at the variance gate, if ρ < 0.5, or if any stacked control is within 0.1 of it.

**Cost.** Unbenchmarked CPU estimate: ~1.5 h (8 candidates x short LoRA fine-tunes on 0.5B).

---

## MX4. Override-budget memory lifecycle (8-way umbrella)

**Parts merged (8):** N2 positive rewrite (PR #26: wave-6 violations 71.50% with prohibitions vs 29.67% with positive rewrites), M2 salience, N1 masks, MX2 margin gate (#31/#33), M3 keep-context, R1 low-LR correctability, MX1 route, MX3 correctability-as-plasticity. The contamination law R (PR #4) supplies a failure model for the write gate, not a ninth mechanism in the merge.

**Claim.** One quantity governs a lesson's whole life: the **override budget** of a state, `b = directive shift − base margin`. Writing (positive phrasing raises shift), reading (salience, masks, margin gating spend it only where b > 0), consolidation (moves the prior into weights, lowers future b for contradictions, route-dependent), and retirement (consolidate when b is reliably large across states and post-consolidation correctability stays above a floor). Prediction: follow probability of any later directive = σ(a·b + c_route), one curve across all stages, with c_route the only stage-specific term.

**Interaction.** The umbrella passes only through its parts' isolating tests (MX1, MX2, MX3); its own test is that a single σ(a·b + c_route) fitted on stage 1 (in-context) predicts stage 3 (post-consolidation) following out of sample better than per-stage fits on margin alone.

**Stacked control:** per-stage margin-only logistic fits; full stack of each part's control.

**Kill line.** Dead if MX1 or MX2 dies, or if the shared curve's held-out log-loss is not better than per-stage margin fits by a CI-clear margin.

**Cost.** Free given MX1-MX3 data.

---

## Self-killed while drafting (not sent for review)

- **Function-space group testing for edit damage** (#24's 98.8%/98.7% top-decile concentration of squared positive functional drops + coded checks + targeted re-edit): the draft did not identify a pooling scheme cheaper than direct per-fact checks. The concentration came from the initial 1,000-edit run (263 newly flipped facts), not the high-efficacy confirmation. Raw key-space damage norm did not predict which facts had the largest functional drop (Pearson r ≈ −0.07).
- **Entropy-factored lessons** (lesson = state-conditional temperature + content residual, from A3 + M2 + B3): the stack LOO + recency + entropy T ties it by construction outside small-margin states; its only live part is MX2's margin gate.
- **Fleet soft-endorsement pooling** (H1's +19.75 pp endorsement probability hidden by greedy decoding + #31 margins): it is H1b, which tied its mean-P ablation.
