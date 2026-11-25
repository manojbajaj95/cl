# Harness proposer — batch 1: continually evolving harnesses (online + offline)

Scope: the model is fixed (or trained separately); what learns is the harness (prompts, skills, tools, hooks, memory). Online = edits made during or between live episodes; offline = edits/consolidation from logged trajectories.
Read before proposing: `reviews/idea-ledger.md` (PR #6, all 58 rows), `ideas/agents/` batches 1–12 + SUMMARY (PR #7), PR #14 (G1 killed). Inspiration: [Prism-Shadow/penguin-harness](https://github.com/Prism-Shadow/penguin-harness) (RSI toolkits: OPRO, APE, ACE, AWM, SkillAdam, SkillOpt, OpenSkill, TRACE, RRSI; snapshot-before-change, frozen-State evaluation).
Prior art via alphaXiv. Headline finding: **harness self-evolution is the most crowded corner of CL right now** (40+ papers Aug–Nov 2026). Most obvious "continual harness" mechanisms are already published, so this batch is mostly pre-kills plus one candidate.

## Landscape the reviewer should hold every harness idea against

| Problem | Already covered by |
|---|---|
| Harness forgetting across task families | 2611.03219 (SWE-Bench 94→32% after FeatureBench evolution), 2610.25858 (global edits interfere; retrieval collides) |
| Per-item regressions / noisy gates | SAGE 2609.36043 (per-item paired one-sided test), Winner's Curse 2610.09239, RRSI 2609.24972, GUARD 2611.23476 (pins mastered rules, non-regression buffer) |
| Selective verification on relevant tasks | HarnessLens 2608.27311 |
| Redundant safeguards silently deleted | Masked Erosion 2610.38392 (one-layer ablation audits fix it) |
| Prompt growth / unsafe deletion | Catastrophic Remembering 2608.11095 (comments carrying latent reasoning), SHarP 2610.04178, Cortex 2610.14216, ESPO 2609.04197 |
| Overfitting of evolved harness | HDA 2610.22466 (54% of gain is overfitting), Bad Genius 2609.18366, TextReg 2605.21318 |
| Online in-run evolution + offline meta-learning | Meta² 2611.05139, DeltaHarness 2611.21688, Continual Harness 2605.09998, Recurrent Harness 2610.12668 |
| Model or benchmark changes under the harness | SIM 2611.18856, HarnessBank 2607.13683 (gains are model-specific), MoHA 2611.27646 |
| Weight–harness co-evolution / internalization | Evo² 2610.13025, HarnessAdapt-RL 2610.28069, Harness-S 2611.04277, Harness Annealing 2610.01235, Box²-Bench 2609.39578, Harness-Zero 2609.24974 |
| Branches / populations of harnesses + router | Mixture of Branches 2609.37834, Population-centered evolution 2610.36660, HarnessBank |
| Evaluating the evolver itself | VERSE 2610.02616, Agent Plasticity 2610.08902, Flex-RSI 2611.08946 |

Rule for this batch: an idea survives only if it is not one of these and the simplest same-budget control (per-item paired gate, random old-task replay in the gate, ablation audit, per-family harness + router, or plain continued evolution) could plausibly lose to it.

## Candidate HW1 — Convergent-edit promotion (online local overlays, offline promotion by independent rediscovery)

**Mechanism.** Online: each task runs a local evolver that may edit a *task-local overlay* of the harness during the episode (Meta²/DeltaHarness style); the overlay is thrown away at episode end and only its edit log is kept. Offline: cluster logged overlay edits by semantic/functional equivalence (same diff on the same component, or same behavioural effect on a probe set). Promote a cluster into the shared harness ranked by **breadth of independent rediscovery** — the number of distinct task families whose local evolvers produced it without seeing each other — not by search-set gain. Claim: independent rediscovery across families is a label-free estimate of held-out transfer that is immune to the winner's curse, because the evidence for an edit comes from tasks that never scored it. Continual angle: the shared harness only absorbs what recurs across families, so a new family's local fixes stay local unless rediscovered (the forgetting mechanism in 2610.25858 is global edits from one family).

**Closest prior art.** Meta² 2611.05139 (online local evolution + offline learned meta-skill, but promotes *knowledge about when to evolve*, not edits by recurrence); Population-centered evolution 2610.36660; HDA 2610.22466 (measures overfitting, no selection rule); Mixture of Branches 2609.37834 (complementarity + router). Killed neighbours to distinguish: Matthew-effect libraries (row 43: success → exposure; here the count is of independent *discovery*, not of use) and H1 (consensus erases rare-regime lessons: rare-family edits stay in overlays/per-family harness rather than being deleted).

**Strongest controls (same eval budget, same overlay logs).**
1. Promote by per-item paired validation gain (SAGE gate) spending the budget the clustering would.
2. Promote by raw within-family frequency (tests that *distinct families* matter, not repetition).
3. ACE-style curator given the same overlay logs.
4. Plain continued shared-harness evolution (GEPA/Meta-Harness) at equal rollouts.

**Smallest falsifying test, kill line.** 3 task families × 30 tasks (e.g. BIRD / BFCL / ScienceWorld splits as in 2610.25858), one fixed task model, local evolver on. Gather ≥40 overlay-edit clusters. Ground truth per cluster: held-out gain from adding that edit alone to the base harness, measured on a 4th, unseen family (paired, 3 seeds). Kill if Spearman(breadth, held-out gain) is not ≥ 0.15 above Spearman(paired validation gain, held-out gain), or if within-family frequency ties breadth within CI. Second-stage kill: harness built by breadth promotion does not beat control 1 on old-family retention + unseen-family accuracy at equal budget.
Feasibility note: the evolver needs an API-class model; a 1.5B CPU model will not produce usable overlays. Ground-truth labelling is ~40 clusters × 2 arms × 3 seeds × held-out family.

## Pre-killed in this batch (do not re-propose without fixing the named reason)

| ID | Idea | Killed by |
|---|---|---|
| HK1 | Per-edit *witness tasks* (tasks an accepted edit flipped fail→pass) kept as the regression suite for later gates | SAGE per-item paired gate, GUARD mastered-rule pinning, HarnessLens behaviour-relevant verification; random old-task replay in the gate is the tie-candidate |
| HK2 | Edit-generated executable unit tests per instruction, so deletion stays safe | PromptPex 2503.05070, Catastrophic Remembering's latent-reasoning comments, Masked Erosion one-layer ablation audits, Cortex measurement-gated pruning |
| HK3 | Harness-component dropout during weight training so weights don't depend on the scaffold; harness edits then don't cause forgetting | Harness Annealing 2610.01235, Harness-S 2611.04277, HarnessAdapt-RL (gains persist after removal), Box²-Bench counterfactual SFT |
| HK4 | Divergence-point resume for offline evaluation of harness edits (replay logged run, re-execute only from first input that changes) | Reduces to seeded common-random-numbers full reruns: same paired variance, only cheaper; an engineering cost cut, not a CL mechanism. G1 (row 15, PR #14) already showed log re-scoring loses to simple scores |
| HK5 | Low-order Walsh/additive surrogate of per-task success over edit-presence bits fitted from the evolution log, for safe deletion and forgetting prediction | Ledger row 58 (sparse pairwise surrogate = BOCS; black-box search ties), Masked Erosion's frozen statistical model |
| HK6 | Fork the harness when a new edit helps new tasks but hurts old, route between forks | A3 (row 36, model pools), Mixture of Branches + router, 2610.25858 retrieval baselines |
| HK7 | Online factorial A/B toggling of harness components per episode → unbiased per-component effects, offline keep positive ones | Ordinary online A/B / bandit testing; Masked Erosion ablation audits; HDA attribution |
| HK8 | Make harness portable across model upgrades by keeping only edits whose gain replicates under two models | SIM 2611.18856, HarnessBank cross-model results, MoHA |

## What I learned for the next batch
- The harness-evolution literature has already covered gates, regressions, pruning, overfitting, online/offline splits, co-evolution with weights, and model swaps. A harness idea needs a signal those papers do not use; selection rules built on scores alone are taken.
- Signals still unused there: *independence structure* of evidence (who discovered an edit vs who scored it), and LLM-native exact signals on harness text (the ledger's surviving pattern), restricted to cases not already killed (row 56 likelihood-drop alarm, G1).
