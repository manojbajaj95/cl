# Merged ideas, batch 2 (cross-section proposer)

Same rules as batch 1 (`ideas/merged/batch-1.md`): each card cites the partial results it reuses, compares against the **stacked** strongest part baselines at equal budget, and names the smallest test that isolates the interaction. Lesson/memory arms always include same-length filler and a source-fitted entropy-matched no-lesson temperature. Batch 1's MX1 (route-dependent correctability) and MX3 (correctability as plasticity meter) are referenced as parts.

**Ambitious but doable:** each card pairs a big claim with a tractable first test; risks are for the reviewer to weigh, not reasons to discard a card before review.

Prior-art screen (alphaXiv, Nov 2026): 2609.32818 (first-order bounds on per-fact forgetting from start-of-run measurements), 2609.08067 (popular facts propagate more errors under knowledge updating), 2605.27773 (follow-document vs trust-self depends on how well known a fact is), 2610.08718 (spurious forgetting), 2610.12397 (prospective OOD-degradation prediction from source-side dynamics), 2608.18319 (spectral collapse and plasticity), Override Gap 2604.23750.

---

## MY1. Overridability predicts which facts fine-tuning breaks

**Parts merged (5):** A3-anchor anomaly (PR #33: +90.97 pp vs +10.42 pp follow index at overlapping small margins in the natural position-prior and post-score-offset arms; menu order, action IDs, and baseline leader also differed); functional syndromes (PR #24: functional drops and raw damage are different targets, Pearson r ≈ −0.07 across facts in each seed of the initial run); reverse-grokking and cooldown kills (ledger: margin explained the reverse-grokking order and shrank the cooldown gap); edit capacity (PR #22: fixed 736-edit guess scored 0.216 pooled log error vs 0.220 for covariance); MX3 (correctability as plasticity).

**Claim.** A fact's in-context overridability (follow index of a paired contradicting directive, one forward pair per fact) measures how *anchored* its circuit is, and predicts its functional drop under later unrelated fine-tuning **after partialling out margin, popularity and the first-order bound**. Anchored facts survive; position-like/unanchored facts fall.

**Interaction.** Margin was a strong confound in the ledger's earlier forgetting-order pilots. This card tests a second axis, anchoring, suggested but not isolated by #33 and not measured in those pilots.

**Stacked control:** base margin + subject popularity/frequency (2609.08067, 2605.27773) + first-order per-fact bound at step 0 (2609.32818) + gradient norm on the fact; all in one regression.

**Smallest isolating test.** #24 harness (`pilots/functional_syndromes/`), GPT-2-XL, 1k CounterFact edits. Measure margin and follow index on the edited checkpoint, before the WikiText-2 shift; first check that the paired directive can elicit a nontrivial follow signal on GPT-2-XL. Measure post-shift functional drop and report results separately for the edits that actually flipped the answer (#24: 263/1,000). Gate first: functional-drop variance across facts must exceed seed variance. Then partial Spearman of follow index with drop given the stacked controls.

**Kill line.** Dead at the variance gate, if partial ρ < 0.2 (CI), or if adding follow index raises held-out R² by < 0.05 over the stack.

**Cost.** Unbenchmarked CPU estimate: ~40 min for a run. #24's main run took 1,921 s on eight threads at 22,334,316 kB peak RSS, so run it alone. The follow-index probes and added controls were not timed.

---

## MY2. Spend verifier budget where lessons can flip decisions (contamination law × margins)

**Parts merged (5):** self-contamination law R = k·(α_D·τ − d)/α_S (PR #4, piloting; real-unit challenge transmission 48.33% → 5% with verifier feedback, but the self-judge accepted 0/32 defective candidates, so no epidemic was observed); #31 (155/160 directed flips below 1 logit margin; the ledger's post-hoc estimate of shift versus filler was ~0.6–1.0 logit); A3 temperature (PR #27: entropy matching explained R² 0.953/0.951 of per-start effects in G1/Q2, with 0/2,520 argmax flips; #29 reproduced a high R² on 1.5B, not 0.5B); P3 writer distractibility (piloting); Agent Toolbox narrowed (passed proposal review, not yet a pilot result).

**Claim.** Lessons should transmit more defects when their target states have margin below the directive shift. Their *flippable mass* (share of target states with margin < a source-estimated shift, one no-lesson forward per state) is a proposed predictor of τ, not its definition: #4 estimates τ from the excess defective-write rate with a defective rather than sound parent, normalized by the sound-parent baseline. The prediction is that allocating a fixed verifier budget by flippable mass lowers R below 1 at a budget where uniform verification leaves R > 1.

**Interaction.** R's τ × margin: neither the law (which treats τ as a constant) nor the margin result (which never looked at defects) predicts that a verifier budget can be reallocated to cross the epidemic threshold.

**Stacked control (equal verifier calls):** uniform verification + writer-uncertainty allocation + recency + direct measured effect size on a small held-out state sample (the expensive oracle-ish baseline; the card must match it at ≤ 20% of its cost).

**Smallest isolating test.** Use the unit-conversion world in `agents/llm_pilot/challenge_trial.py` with a 0.5B/1.5B reader, 300 candidate lessons, and a 30% verifier budget. The existing trial is one-step and has no finite-action logit tape; add a common scored answer menu for margins and first check that flippable mass predicts measured τ against filler. Only then connect accepted writes to future trials (the stream loop in `agents/epidemic/model.py` is a reference) and compare uniform, uncertainty, flippable-mass, and measured-effect allocation on final defect share and fitted R. Stop if the uniform arm never enters the R > 1 regime.

**Kill line.** Dead if flippable-mass allocation does not beat uncertainty allocation on defect share by a CI-clear margin, or if measured-effect allocation at equal *total* compute wins.

**Cost.** Unbenchmarked CPU estimate: ~1–2 h for a small challenge with added scoring. Runtime for the longitudinal stream and matched controls is unknown.

---

## MY3. Correctability meter: one forward-pass number for plasticity, fragility and contagion (7-way)

**Parts merged (7):** MX1 route, MX3 plasticity, MY1 fragility, MY2 contagion, plasticity reserve (PR #9: 4.9 pp relative gain spread before retention matching; labeled oracle ρ = +0.704, with no winning label-free predictor in that pilot. PR #21: 0.091 absolute MSE points of spread after retention matching under projected SGD), R1 (PR #30), A3-anchor (PR #33).

**Claim.** One label-free measurement, the follow index of paired contradicting directives at matched margin, is a state variable of a continual learner: higher means the next task is learned faster (MX3), the stored fact is more fragile under unrelated updates (MY1), and lessons written by it transmit defects more (MY2). A learner controlled to hold this meter in a band (by choosing the consolidation route, MX1) gets a better plasticity–stability frontier than LR/regularization tuning at equal compute.

**Interaction.** The parts' controls are each one-endpoint predictors (readiness, margin, popularity, first-order bound, uncertainty). The card claims a single shared axis: the sign pattern (+plasticity, −stability, +contagion) must hold for the same meter on the same model.

**Stacked control:** the union of MX3, MY1, MY2 controls; for the controller, LR × label-smoothing grid at equal compute.

**Smallest isolating test.** Use MX3, MY1, and MY2 as separate feasibility gates; results from Qwen2.5-0.5B and GPT-2-XL alone do not establish a shared axis. If all three pass, use the same checkpoint family, margin-binned follow index, and matched candidate writes to collect all three endpoints, then check the joint sign pattern with CIs. Controller test only if the pattern holds: 3 consolidation cycles, meter-banded route choice vs best grid point, Pareto hypervolume.

**Kill line.** Dead if MX3, MY1, or MY2 dies, if the joint sign pattern fails on the shared set of candidate writes, or if the controller does not beat the grid's hypervolume by a CI-clear margin.

**Cost.** Separate pilots can be reused as feasibility checks; the shared-model panel is new work. Controller CPU estimate is ~2 h, unbenchmarked and excluding the panel.

---

## MY4. Format is a route: QA-form vs prose consolidation at matched absorption

**Parts merged (3):** self-QA (PR #8: 81.37% old-fact retention for self-QA, 82.75% for same-question teacher QA, and 82.29% for verified prose; paired retention differences were inconclusive, not proof of equivalence or a causal format effect); MX1 (route-dependent correctability); Cortex (2610.20399: prospective-query distillation).

**Claim.** Consolidation data format is a route in MX1's sense: QA-form distillation (as in Cortex's prospective queries) writes question-keyed, anchored priors that later context cannot override; prose-form writes overridable ones. Same retention, different correctability.

**Stacked control:** MX1's stack plus matched token count and fact coverage across formats.

**Smallest isolating test.** One extra arm in MX1's M3 run: same lessons rendered as QA vs prose, matched absorption, follow index by margin bin.

**Kill line.** Dead if format changes follow index by < 10 pp in shared margin bins. Folds into MX1 if MX1 dies.

**Cost.** Unbenchmarked estimate: ~30 additional CPU minutes on MX1.

---

## Bold cards (ambitious but doable)

The full claims are big swings. Start with a cheap CPU test on an existing world where possible, and leave the prior-art and feasibility risks visible for review. CPU costs below are planning estimates, not measured runtimes.

### MZ1. Lesson immune system: vaccinate the reader with attenuated defects

**Parts merged (6):** contamination law R (PR #4), Toolbox's silent-failure hypothesis, #31 small-margin flips, #33's prior-provenance contrast, N1 masks (PR #35), and MY2 flippable mass.

**Mechanism.** Train a small reader adapter on deliberately corrupted lessons (plausible but wrong action or fact swaps) paired with ground-truth outcomes. The adapter learns a *state-dependent override threshold*: follow lessons where they are usually right and resist them where defects concentrate. This targets transmission τ by changing how a planted lesson affects the reader and its next write. It only changes gate acceptance α_D if the adapter also decides which writes enter memory. The ambitious claim is enough selective resistance to push R below 1 at deployment without an external verifier.

**Step 1.** In PR #4's `agents/llm_pilot/challenge_trial.py` unit-conversion world, train LoRA on 2,000 synthetic pairs with a 0.5B reader. Hold out conversion families and corruption templates. Measure τ and true-lesson follow index against an untrained reference and a matched-budget stack of filler/ordinary robust training plus an uncertainty gate; run the entropy-matched no-lesson control. Budget ~2 CPU hours.

**Go further if** τ drops ≥20 pp while the true-lesson follow index drops <5 pp against the strongest matched control. Verify R separately in a stream rather than inferring an epidemic outcome from one-step trials. **Risk:** the reader may learn blanket skepticism or ordinary adversarial-training invariance, not a transferable state-dependent threshold.

### MZ2. Dreaming at the decision boundary

**Parts merged (7):** #31 (155 of 160 directed flips were below one logit of margin in that setup), M2 salience, N1 masks, MX2 margin gating, self-QA format/coverage controls (PR #8), plasticity reserve, and rare-event replay trade-offs.

**Mechanism.** In an offline “sleep” phase, the model searches for states where its margin is smaller than the directive's estimated shift. It writes counterfactual episodes there and consolidates on those episodes, using N1-style masks on the lesson-conditioned teacher. Boundary selection and masking are intended to allocate consolidation to states with leverage and preserve off-target behavior; N1 measured inference-time harm, not protection against weight updates.

**Step 1.** Reuse PR #30's `pilots/m3/` world: perturb queue/score prompts to make boundary episodes, then compare with random dreams, real replay, and self-QA replay. Include a matched-budget stack of margin-selected real replay, self-QA, and the same mask; cross dream selection with masking. Match tokens, training steps, and candidate-scoring compute; measure held-out follow and off-target harm. Budget ~1.5 CPU hours.

**Go further if** boundary dreams with masks Pareto-improve held-out follow and harm over the strongest stack. **Risk:** margin-selected replay may be sufficient; generation must buy useful boundary coverage that real-sample selection misses.

### MZ3. A trainable trust dial: knowledge whose overridability is a controllable variable

**Parts merged (8):** MX1, MX3, MY1, MY3, #33's prior-provenance contrast, [The Override Gap](https://arxiv.org/abs/2604.23750), [Engram Injection](https://arxiv.org/abs/2610.15882), and M3's keep-versus-evict diagnostic.

**Mechanism.** Add a scalar readout gate per stored fact or lesson that sets how strong a contradicting directive must be to overturn it. A meta-objective learns to leave memories with frequent contradictions easier to override and stable ones harder to override. The test is whether the dial controls follow independently of baseline margin and absorption, rather than simply scaling a prior.

**Step 1.** Extend the M3 setup into a synthetic churn world with known fact-change rates on a 0.5B reader. Compare adaptive dials to a fixed dial, a matched-margin route, a validity-tag baseline inspired by Engram Injection, and an LR grid; use the strongest combination at equal budget. Test accuracy after scheduled contradictions and retention of stable facts. Budget ~2 CPU hours.

**Go further if** the learned dial tracks change rates (Spearman ρ >0.5 on held-out facts) and beats the stack on the stability–editability frontier at matched margin and absorption. **Risk:** validity tags or simple margin rescaling may explain any gain; the dial may also collapse to a constant.

### MZ4. A lesson market across a fleet

**Parts merged (6):** fleet results (PR #23: H1's metapredictions were flat; H1b did not establish a gain over mean endorsement probability), contamination law R, MY2 flippable mass, plasticity reserve, [ALLOT](https://arxiv.org/abs/2609.32344) budgeted routing, and Toolbox.

**Mechanism.** Agents trade lessons at a buyer-specific price: flippable mass times verified outcome lift on the buyer's past states. As buyers observe more outcomes, a defective lesson can lose value with one buyer but remain relevant to another. The interaction to test is whether buyer-specific prices allocate a fixed verifier budget better than pooled credit and verification.

**Step 1.** Combine PR #23's `pilots/fleet_sp/` private-API world with planted lesson errors from PR #4's unit-conversion trial. Use eight agents in the proposed variant; PR #23 originally used 20. Compare market allocation with uniform sharing, popularity, verifier-based sharing, and a bandit baseline stacked with flippability and verification at equal verifier calls and scoring budget. Price with past feedback only; assess fleet defect share and task gain on held-out outcomes. Budget ~1 CPU hour for a small prototype, not an estimate for the full PR #23 pilot.

**Go further if** the market improves both endpoints over the best stack. **Risk:** buyer-specific bandit weights may already capture the pricing effect, and reducing the fleet size may weaken the rare-regime signal.

### MZ5. Diffuse damage, global antidote

**Parts merged (4):** functional syndromes (PR #24: top-decile raw key-response damage energy 18.58% and 18.62% in the two high-efficacy confirmation seeds), [Local Conflict, Targeted Repair](https://arxiv.org/abs/2606.02398), [When Forgetting is not Catastrophic](https://arxiv.org/abs/2610.08718), and MY1.

**Mechanism.** Diffuse raw key-response damage does not rule out a compact function-space correction. Fit a low-rank “antidote” from before/after functional gradients on 50 probe facts; apply it as one global correction per update rather than selecting facts to re-edit. The falsifiable claim is that functional recovery transfers to held-out facts without undoing the new task, not that diffuse damage makes targeted repair impossible.

**Step 1.** Reuse PR #24's `pilots/functional_syndromes/` harness. Sweep repair ranks 1–8 against targeted re-edit/rollback, spurious-forgetting realignment, and L2-to-init; include the strongest matched-budget combination of those controls. Match probe access, repair budget, and shift-task retention; evaluate functional recovery on held-out facts and measure shift-task gain on a held-out split. Budget ~45 CPU minutes for the prototype, unbenchmarked and run alone: PR #24's main run took 1,921 s and peaked at 22,334,316 kB RSS before any such repair sweep.

**Go further if** rank ≤4 recovers ≥50% of functional drop with <10% relative loss of positive shift-task gain while beating the stack at matched retention. **Risk:** realignment may already capture the same directions, or the apparent low rank may be a probe-selection artifact.

---

## Risky, kept for the reviewer

- **Order-robust writes via the two-order comparator.** Try screening writes by their effect on order sensitivity, while matching retention and memory size. **Risk:** PR #17's 100-step comparator already achieved ρ = 1.000 at 200 and 1,000 steps, and PR #11's append baseline had final order distance 0.028 versus 0.417 for utility eviction. **Cheap first step:** use the toy memory loop to test whether screening reduces long-run distance versus append at matched capacity and utility, rather than trying to improve the existing ranking ceiling.
- **Margin-ordered replay.** Use old-item margin to prioritize replay. **Risk:** MIR or plain loss priority may already give the same ordering. **Cheap first step:** in a toy replay run, match old-item losses and compare the replay selectors only on examples where their rankings differ.
- **Basin bifurcation predicts lost plasticity.** Use early changes in the effect-class replay run to predict which writes will later block adoption. **Risk:** adoption-rate extrapolation and [existing prospective degradation prediction](https://arxiv.org/abs/2610.12397) may explain the result. **Cheap first step:** inspect the PR #27 ten-seed weight-4 traces (5/10 below 95% adoption); if early checkpoints are missing, log them in the same small run and compare held-out prediction against early-rate extrapolation before proposing a controller.
- **Loud-failing lesson contracts.** Keep text lessons but attach a checkable contract that surfaces silent drift before the lesson is propagated. **Risk:** text plus the same regression tests is already the narrowed Toolbox control. **Cheap first step:** in a small API-drift sandbox, compare contract-triggered checks with those regression tests at equal calls, scoring time to detection and subsequent defect transmission.
