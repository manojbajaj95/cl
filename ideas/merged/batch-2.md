# Merged ideas, batch 2 (cross-section proposer)

Same rules as batch 1 (`ideas/merged/batch-1.md`): each card cites the partial results it reuses, compares against the **stacked** strongest part baselines at equal budget, and names the smallest test that isolates the interaction. Lesson/memory arms always include same-length filler and a source-fitted entropy-matched no-lesson temperature. Batch 1's MX1 (route-dependent correctability) and MX3 (correctability as plasticity meter) are referenced as parts.

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

## Self-killed while drafting

- **Order-robust writes via the two-order comparator** (PR #17: 100-step comparator ρ = 1.000 at both 200 and 1,000 steps + plasticity reserve): the comparator already hit the ranking ceiling on this panel. PR #11's simpler append baseline had much smaller, but nonzero, final order distance (0.028 vs 0.417 for utility eviction).
- **Margin-ordered replay** (forget small-margin old items first, replay them first): this is maximally-interfered / loss-based replay selection (MIR); the ledger's margin-confound pattern already covers the phenomenon.
- **Basin bifurcation predicts lost plasticity** (effect-class weight-4 collapse on 5/10 seeds, PR #27, + early divergence): early adoption rate extrapolation would tie it, and 2610.12397 covers prospective degradation prediction from training dynamics.
- **Loud-failing lesson contracts** (Toolbox + contamination law): converting lessons into tools gives the tool arm already proposed by the narrowed Toolbox card, not a new mechanism.
