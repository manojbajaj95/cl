# Handwritten LoRA 4: Move the Behaviour, Keep the Ledger

Child of [Handwritten LoRA 3: Store the Tests, Rebuild the Weights](handwritten-lora-3.md) ([PR #403](https://github.com/manojbajaj95/cl/pull/403), depth 3) · 25 candidate cards (HT01–HT25) · 4 ranked deeper questions · Ideas only; no experiments run

**Parent verdict.** The review of #403 gave no card a 4 and kept two lines at 3:
- **(a)** A repair-grown ledger carried across retrains and base upgrades. It is gated on previously repaired inputs regressing at ≥ 2× the base rate (HM17). Controls: KLOD at equal size, ledger replay, PCT, Self-Preservation.
- **(b)** One format-free spec compiled to the cheapest format per base (prompt, steering vector or LoRA). A spec is complete only when independent rebuilds agree (HM12, HM05).

The reviewer warned that the branch is drifting toward storage choices. This level therefore drops "what to store" and asks which new **operations** the ledger makes possible.

**Thesis.** Treat a behaviour as the invariant and every representation of it (prompt, soft prompt, steering vector, LoRA, the base weights themselves) as an interchangeable tier. The ledger (line a) is what stays fixed, and rebuild agreement (line b) is what certifies a representation. That defines three operations that neither storage nor ordinary training provides:
1. **Migrate.** Move a behaviour between tiers in both directions, including *demotion* from weights back to a prompt, and accept the move only if the ledger passes and independent rebuilds agree (HT01–HT06).
2. **Co-upgrade.** Make the *base* upgrade respect the adapter fleet's ledgers. Instead of porting every adapter to the new base, the new base, or one shim on it, is trained so that existing adapters keep passing (HT07–HT11). This reverses the porting direction of the whole branch.
3. **Find the underdetermined.** The inputs on which ledger-passing rebuilds disagree are exactly what the spec does not say. That set is a new object: it says where to ask the owner, which tier to use, and where the next retrain will flip (HT12–HT15).

The ledger also acts before damage (HT16–HT20) and is gated by HM17's repeat-offender test.

## Shared protocol

Inherits F1–F3 from [level 2](handwritten-lora-2.md#shared-protocol) and S1/S2, the equal-bytes harness and the held-out neighbour split from [level 3](handwritten-lora-3.md#shared-protocol).
- **Tiers.** T0 system prompt; T1 soft prompt ([CSPD](https://arxiv.org/abs/2611.27376)-style); T2 steering vector at one layer; T3 rank-r LoRA; T4 merged into base weights. A behaviour is *held* by a tier on a base if that representation passes its full ledger and 3 independent rebuilds agree (pairwise KL < ε on held-out domain inputs).
- **Release sequence.** Use the 4 consecutive Qwen releases of [UpgradeBench](https://arxiv.org/abs/2608.20918) where available; otherwise S1's chain.
- **Line (a) controls:** KLOD at equal size, ledger replay, PCT, Self-Preservation (all from level 3).
- **Line (b) and migration controls:** [Cortex](https://arxiv.org/abs/2610.20399) memory consolidation (context → parameters), [CSPD](https://arxiv.org/abs/2611.27376) composable soft-prompt distillation, context distillation, LoRA-only rebuild, and UpgradeBench's retain / port / refresh / retrain policies.
- **Retention.** As in the parents, plus a ledger pass on every behaviour that shares the base or is co-loaded, after every migration or upgrade.

## Literature check

alphaXiv discovery on moving behaviour between prompts and weights, consolidation, and backward-compatible model upgrades; abstracts checked on arXiv. Abstract-level screen.

| Nearest prior | What it already does | Boundary for this node |
|---|---|---|
| [Cortex](https://arxiv.org/abs/2610.20399), [CSPD](https://arxiv.org/abs/2611.27376), context distillation, [on-policy context distillation into weights](https://arxiv.org/abs/2610.07250), [WSP writes ICL](https://arxiv.org/abs/2611.26841) | Consolidate context into parameters (one direction), keep RL experts as composable soft prompts on a frozen model, write ICL task vectors into weights. | All move behaviour *upward* (context → weights) once. The new operation is bidirectional, ledger-gated migration, including demotion weights → prompt when a stronger base makes the adapter unnecessary. |
| [UpgradeBench](https://arxiv.org/abs/2608.20918), [Heirloom](https://arxiv.org/abs/2611.00650), [ReLoRA](https://arxiv.org/abs/2606.02606), [LoRA-X](https://arxiv.org/abs/2501.16559), [Theseus](https://arxiv.org/abs/2602.12952) | Decide and execute adapter migration per release: retain, port, refresh, retrain. | All move the *adapters* to the new base. HT07–HT08 move the *base* toward the adapters. |
| [Backward-compatible representation learning](https://arxiv.org/abs/2003.11942), [embedding backward-compatibility adapters](https://arxiv.org/abs/2609.16875), [backward-compatible retrieval](https://arxiv.org/abs/2610.29550) | Train new embedding models so old gallery embeddings remain usable without re-indexing. | That is the closest idea to co-upgrade, in retrieval. Carrying it to LLM bases against a fleet of adapter ledgers, with behavioural tests rather than embedding compatibility, is not in the abstracts read. |
| [Positive-congruent training](https://arxiv.org/abs/2011.09161), [no universal signal predicts LLM regression](https://arxiv.org/abs/2608.13607) | Constrain updates on old-correct samples; no inference-time signal predicts sample regressions. | HT12/HT14 propose rebuild disagreement as a pre-update signal, and HT16 acts on it before training. |
| [SEAL](https://arxiv.org/abs/2506.10943), [Safety must survive self-improvement](https://arxiv.org/abs/2610.01073) | Models generate their own fine-tuning edits; safety failures persist across self-improvement generations. | HT20 makes the ledger the acceptance gate for self-edits. |

## A · Migrate: move a behaviour between tiers

### HT01 · The migration operator
- **Primitive** (new operation).
- **Mechanism:** `migrate(b, src, dst, base)` compiles behaviour b into tier dst from its spec and ledger. The move is accepted only if (i) the full ledger passes in dst, (ii) 3 independent dst rebuilds agree, and (iii) every co-loaded behaviour's ledger still passes. The src representation is then retired. The output records the move and any ledger entries that dst could not hold.
- **Nearest prior / gap:** Cortex and CSPD consolidate one way, with no acceptance test on a carried ledger.
- **Cheapest first test:** 6 F2 behaviours × all 20 ordered tier pairs on Qwen2.5-1.5B. **Kill** if fewer than 25% of moves are accepted, which would leave nothing to choose, or if accepted moves do not keep held-out neighbour behaviour within 1 pp of the src tier.
- **Old-task retention:** Built into acceptance; also check the 3 benchmarks.
- **Risk / likely tie:** Most moves to T0/T2 may fail for skill behaviours; that pattern is HT04's map.

### HT02 · Demotion: retire an adapter into a prompt when the base outgrows it
- **Primitive-candidate** (the reverse of consolidation).
- **Mechanism:** After a base upgrade, try `migrate(b, T3, T0)`. A stronger base may already hold the behaviour from a short instruction. Demotion frees adapter slots and serving memory and removes a per-base porting cost forever.
- **Nearest prior / gap:** Prompt-to-weights consolidation runs only upward. UpgradeBench's "retain" keeps the old specialist rather than replacing it with a prompt.
- **Cheapest first test:** S1 upgrades; count the behaviours that can be demoted per upgrade. **Kill** if < 1 in 6 behaviours can be demoted on any upgrade, or if demoted prompts fail ledgers that the LoRA passed (> 2 pp held-out neighbour loss).
- **Old-task retention:** The prompt's effect on unrelated traffic. A prompt costs context, so measure its interference with other prompts and with co-loaded adapters.
- **Risk / likely tie:** Small bases rarely outgrow adapters; try the 9B step.

### HT03 · Promote by traffic into the next base
- **Primitive-candidate.**
- **Mechanism:** Behaviours loaded on > x% of traffic are merged into the base (T4) at the next upgrade, with their ledgers added to the upgrade's constraints (HT07). Rarely used behaviours drift down to T0/T1. This gives the fleet a consolidation schedule with a ledger check at every step, the systems analogue of hippocampus → cortex.
- **Nearest prior / gap:** [Cortex](https://arxiv.org/abs/2610.20399) frames memory consolidation; nobody schedules both directions by usage under a carried ledger.
- **Cheapest first test:** 20 simulated behaviours with a Zipf traffic distribution, 2 upgrades. **Kill** if promote/demote by traffic does not beat "keep every adapter at T3" on serving cost at equal served-ledger failures.
- **Old-task retention:** Every promoted behaviour's ledger and the base benchmarks after merge.
- **Risk / likely tie:** Merging many behaviours into the base will interfere; cap promotions per upgrade.

### HT04 · Round-trip loss as a map of what each tier can hold
- **Improvement / assay** (diagnostic for HT01–HT03).
- **Mechanism:** Move T3 → T0 → T3 and T3 → T2 → T3, and record which ledger entries fail after the round trip. The failures map which kinds of behaviour each tier cannot carry: facts, exceptions, format, refusal.
- **Nearest prior / gap:** None for ledger-level round trips.
- **Cheapest first test:** F2's 6 behaviours, 2 bases. **Kill** if the map is the same on both bases (it would be lore, not a measurement).
- **Old-task retention:** Per round trip.
- **Risk / likely tie:** Low risk; it is a measurement.

### HT05 · Split one behaviour across tiers
- **Primitive-candidate** (a compiled representation that is not one format).
- **Mechanism:** Compile the rule part of a behaviour into a prompt and its exceptions into LoRA counter-components (HC20). The compiler searches splits that pass the ledger at the least serving cost.
- **Nearest prior / gap:** Prompt + adapter combinations exist ad hoc; a ledger-checked split search does not.
- **Cheapest first test:** Unit conversion with 5% irregular units on 2 bases. **Kill** if the best split is never cheaper than pure T3 at equal ledger pass.
- **Old-task retention:** Both parts' ledgers and unrelated traffic.
- **Risk / likely tie:** Pure LoRA may be cheap enough on multi-LoRA servers.

### HT06 · Migration under co-loading
- **Improvement.**
- **Mechanism:** Demoting one behaviour to a prompt changes how it interacts with the adapters loaded beside it. Check acceptance under every co-load pair seen in traffic, not only in isolation.
- **Nearest prior / gap:** HC22 / HM22 at a single tier.
- **Cheapest first test:** 6 behaviours, all co-load pairs, 1 migration each. **Kill** if no isolated-accepted migration fails under co-loading (the check would be unnecessary).
- **Old-task retention:** All co-loaded ledgers.
- **Risk / likely tie:** Likely needed only for prompts.

## B · Co-upgrade: bend the base toward the fleet

### HT07 · Adapter-compatible base upgrades
- **Primitive** (new operation: a base release trained so that the existing adapter fleet keeps passing its ledgers).
- **Mechanism:** During the fine-tuning phase of a new base (or a final short compatibility phase), add a loss that keeps each existing adapter's ledger behaviour when that adapter is loaded on the new base after a fixed cheap transform (LoRA-X projection or identity, for same-shape releases). The vendor trains once, and every downstream adapter stays usable without porting.
- **Nearest prior / gap:** [BCT](https://arxiv.org/abs/2003.11942) does this for embedding models and old galleries; [UpgradeBench](https://arxiv.org/abs/2608.20918) assumes the base is fixed and the adapters move.
- **Cheapest first test:** Simulate a release: take Qwen2.5-0.5B, continue-train on 200M tokens of new data to make "v2", with and without the fleet-ledger loss for 6 F2 adapters. **Kill** if the compatible v2 loses > 1 pp on its own benchmarks, or if it does not cut fleet ledger failures under LoRA-X by ≥ 50% against plain v2.
- **Old-task retention:** v2's general benchmarks, the main cost, plus every adapter's ledger.
- **Risk / likely tie:** Vendors will not train against third-party ledgers. HT08 is the user-side version.

### HT08 · One compatibility shim per base instead of one port per adapter
- **Primitive-candidate** (new object: a base-side adapter that makes a whole fleet compatible).
- **Mechanism:** On the new base, train or handwrite one shim LoRA that maps the new base's behaviour toward the old base's on the union of fleet ledgers. Every old adapter is then loaded on new base + shim after a fixed transform. Cost is one shim per upgrade instead of N ports.
- **Nearest prior / gap:** [Embedding backward-compatibility adapters](https://arxiv.org/abs/2609.16875) use a learned adapter for embeddings. LoRA-X, ReLoRA and Theseus port each adapter separately.
- **Cheapest first test:** S1 first upgrade, 6 adapters. **Kill** if shim + transform does not reach ≥ 90% of per-adapter ReLoRA accuracy at ≤ 1/3 of its total cost, or if it breaks the new base's gains on non-fleet traffic by > 2 pp.
- **Old-task retention:** New base's benchmarks with the shim loaded but no domain adapter.
- **Risk / likely tie:** The shim may undo the upgrade's improvements. Load it only when a fleet adapter is loaded.

### HT09 · Ledger-level upgrade negotiation
- **Primitive-candidate** (decide per ledger entry whether the base change wins or the old behaviour is kept).
- **Mechanism:** A new base changes behaviour on some ledger entries. Some changes are improvements (the vendor fixed a bug the ledger froze) and some are regressions. Each entry is classified from its provenance and authority (HM23) and from whether the new behaviour passes a held-out correctness check. The shim (HT08) keeps only the regressions.
- **Nearest prior / gap:** Negative-flip work treats every change on an old-correct sample as a regression.
- **Cheapest first test:** S1 with 5 planted improvements and 5 planted regressions in v2. **Kill** if negotiation does not keep ≥ 4/5 improvements while blocking ≥ 4/5 regressions.
- **Old-task retention:** Blocked regressions are the measure.
- **Risk / likely tie:** Correctness checks need labels for some entries.

### HT10 · Pin behaviour across a base upgrade
- **Improvement** (a per-user product of HT08).
- **Mechanism:** A user may want old-base behaviour on their own ledger entries only. A pin adapter is written from the diff of old and new behaviour on those entries and holds nothing else.
- **Nearest prior / gap:** Keeping the old base is the control (expensive). Heirloom carries personalization, not pins.
- **Cheapest first test:** 3 users with distinct ledgers. **Kill** if pin adapters leak old behaviour onto non-pinned inputs (> 2 pp change from the new base).
- **Old-task retention:** New base's behaviour on non-pinned traffic is the retention target.
- **Risk / likely tie:** Close to HT08; merge if no difference appears.

### HT11 · Fleet ledgers as a release gate
- **Improvement / assay.**
- **Mechanism:** Before a base release, run the fleet's union ledger with each adapter transported cheaply. Its failure rate predicts migration cost. Test whether it predicts UpgradeBench's best decision (retain, port, refresh, retrain) per specialist.
- **Nearest prior / gap:** [UpgradeBench](https://arxiv.org/abs/2608.20918) evaluates the decisions longitudinally.
- **Cheapest first test:** UpgradeBench releases. **Kill** if ledger failure rate does not predict the best decision better than base benchmark deltas.
- **Old-task retention:** Not applicable (assay).
- **Risk / likely tie:** Base benchmark deltas may already predict it.

## C · The underdetermination set

### HT12 · The underdetermination set and spec-completion queries
- **Primitive** (new object: inputs where ledger-passing rebuilds disagree; new operation: ask the owner exactly those).
- **Mechanism:** Build k = 5 independent rebuilds that all pass the ledger. Sample traffic-like inputs and keep those where the rebuilds disagree, then cluster them. Each cluster is a question the spec does not answer ("which unit system when none is stated?"). Asking the owner one question per cluster and adding the answer as a ledger entry completes the spec where completion matters.
- **Nearest prior / gap:** Query-by-committee active learning labels points to fit one model. Here the committee is spread across tiers and rebuild methods, and the output is a set of questions, not labels. HM05/HM06 used disagreement to add tests but did not treat the set as an object.
- **Cheapest first test:** F2 domains, the owner simulated by the original training data. **Kill** if answering the top 10 clusters does not cut rebuild disagreement on held-out traffic by more than 10 random owner questions do.
- **Old-task retention:** New entries must not break existing ledgers.
- **Risk / likely tie:** Clusters may be incoherent; then this reduces to HM06.

### HT13 · Pick the tier with the smallest underdetermination on traffic
- **Improvement** (a choice rule for line b).
- **Mechanism:** Different tiers leave different things unsaid: a prompt is determined on format and loose on exceptions, a LoRA the reverse. Choose the cheapest tier whose underdetermination mass on live traffic is below a threshold, instead of the cheapest tier that passes the ledger.
- **Nearest prior / gap:** HM12 picks by ledger pass and cost.
- **Cheapest first test:** 6 behaviours × 3 tiers × 2 bases. **Kill** if the rule never changes HM12's choice, or its choices do not reduce served errors.
- **Old-task retention:** Served errors on held-out traffic.
- **Risk / likely tie:** Measuring mass on traffic needs a traffic sample; use held-out domain inputs.

### HT14 · Does underdetermination predict the next regression?
- **Primitive-candidate / assay** (a pre-update signal of the kind [2608.13607](https://arxiv.org/abs/2608.13607) did not find among inference-time signals).
- **Mechanism:** Inputs in the underdetermination set are where any retrain is free to flip. Test whether membership predicts regression at the next retrain better than confidence, margin or cross-version KL, and better than repair history (HM17).
- **Nearest prior / gap:** That paper's signals; HM17.
- **Cheapest first test:** S2 without constraints, 6 retrains. **Kill** if set membership has a regression odds ratio < 2, or does not add value beyond HM17's history signal.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** It may only duplicate low confidence.

### HT15 · Underdetermination across bases as a compatibility measure
- **Improvement / assay.**
- **Mechanism:** The same spec underdetermines more on a weaker or more different base. The size of the set on base v2 for the fleet's specs is a measure of how far v2 is from v1 *for this fleet*.
- **Nearest prior / gap:** MATCHA/representation similarity metrics are fleet-agnostic.
- **Cheapest first test:** S1 bases. **Kill** if it does not rank port difficulty better than MATCHA alignment error.
- **Old-task retention:** Not applicable.
- **Risk / likely tie:** Alignment error may rank the same.

## D · The ledger acting before damage (line a, gated by HM17)

### HT16 · Prophylactic writes before a retrain
- **Primitive-candidate** (new operation: repair predicted regressions before they occur).
- **Mechanism:** If HM17 passes (repaired inputs regress ≥ 2× the base rate), then before each retrain, select the entries predicted to regress (from history plus HT14) and constrain or counter only those. Repairs then happen before the damage instead of after serving it.
- **Nearest prior / gap:** KLOD at equal size, ledger replay, PCT and Self-Preservation all choose constraints without a per-input regression forecast.
- **Cheapest first test:** S2, 6 retrains. **Kill** if prophylaxis does not cut *served* regressions by ≥ 50% against KLOD at equal constraint count, or ledger replay matches.
- **Old-task retention:** Held-out neighbours never in the ledger.
- **Risk / likely tie:** Fails with HM17; run HT23 first.

### HT17 · Fragile inputs transfer across domains
- **Improvement / assay.**
- **Mechanism:** Inputs that regressed in domain A's retrains may also regress in domain B's retrains on the same base (shared fragile neighbours such as arithmetic or refusal). Pool ledgers across the fleet into a base-level fragile set.
- **Nearest prior / gap:** HM07 shares tests to save bytes; here sharing is used for prediction.
- **Cheapest first test:** 6 domains on one base. **Kill** if A's fragile set does not predict B's regressions above the base rate.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** Fragility may be domain-specific.

### HT18 · A base's fragility map, handed to the next upgrade
- **Primitive-candidate** (links D to B).
- **Mechanism:** The fleet-pooled fragile set, clustered, localizes behaviours of a base that every fine-tune breaks. Add it to HT07's compatibility loss so the next base is less fragile there. The fleet's repair history then becomes training signal for the base.
- **Nearest prior / gap:** [Edit-Ready Training](https://arxiv.org/abs/2611.26408) rehearses edits; HT07.
- **Cheapest first test:** Simulated v2 with and without the fragility loss. **Kill** if v2's fragile-set regression rate under the 6 domain retrains does not fall by ≥ 30%.
- **Old-task retention:** v2's benchmarks.
- **Risk / likely tie:** Requires base training access; the toy v2 is the cheap version.

### HT19 · Counterfactual necessity of a ledger entry
- **Improvement.**
- **Mechanism:** An entry is necessary if rebuilding or retraining without it reproduces the regression it records. Remove entries that are not necessary. This is a causal criterion, unlike HM18's activity criterion.
- **Nearest prior / gap:** HM18.
- **Cheapest first test:** S2 ledger after 6 retrains. **Kill** if necessity pruning does not keep retention at a smaller size than activity pruning.
- **Old-task retention:** Held-out neighbours.
- **Risk / likely tie:** Costly (one retrain per entry); sample entries.

### HT20 · The ledger as the acceptance gate for self-edits
- **Primitive-candidate** (new use: the gate that lets a model modify its own adapters).
- **Mechanism:** A model proposes its own adapter updates ([SEAL](https://arxiv.org/abs/2506.10943)-style self-edits, or a WSP self-edit). Each is accepted only if the ledger passes and rebuilds agree, and every rejected self-edit adds the failing case to the ledger. Self-improvement then cannot undo a repair.
- **Nearest prior / gap:** [Safety must survive self-improvement](https://arxiv.org/abs/2610.01073) shows failures persist across self-improvement generations; SEAL optimizes edits by reward.
- **Cheapest first test:** 10 self-edit rounds on Qwen2.5-0.5B, one domain. **Kill** if gated self-editing does not keep ledger failures at 0 while reaching ≥ 80% of ungated self-editing's target gain.
- **Old-task retention:** Ledger and benchmarks every round.
- **Risk / likely tie:** Gating may reject most self-edits; report the acceptance rate.

## E · Keep it honest

### HT21 · Control harness for both lines
- **Improvement / assay.**
- **Mechanism:** Every card runs its line's controls: KLOD at equal size, ledger replay, PCT and Self-Preservation for D; Cortex, CSPD, context distillation, LoRA-only rebuild and UpgradeBench's four policies for A–C. All controls get equal information and equal bytes.
- **Nearest prior / gap:** Level 3's HM24.
- **Cheapest first test:** Built with HT01. Fail any result without its controls.
- **Old-task retention:** Same for all arms.
- **Risk / likely tie:** None.

### HT22 · Measure on traffic, not on test sets
- **Improvement / assay.**
- **Mechanism:** Migration, demotion and underdetermination claims are about served behaviour, so evaluate on a held-out traffic sample with the deployment's mixture of domains and co-loads, not on per-domain test sets.
- **Nearest prior / gap:** Deployment evaluation.
- **Cheapest first test:** Simulated traffic for the 20-behaviour fleet (HT03). **Kill** a claim if its traffic number is > 2× worse than its test-set number.
- **Old-task retention:** Traffic includes unrelated requests.
- **Risk / likely tie:** None.

### HT23 · Gate D on HM17 before anything else
- **Improvement / assay** (sequencing).
- **Mechanism:** Run HM17 (do repaired inputs regress at ≥ 2× the base rate?) on S2 first. If it fails, drop HT16–HT19 and keep HT20, which does not depend on prediction.
- **Nearest prior / gap:** Reviewer's gate on line (a).
- **Cheapest first test:** HM17's run. **Kill** section D except HT20 if the ratio is < 2.
- **Old-task retention:** As HM17.
- **Risk / likely tie:** None.

### HT24 · Longitudinal cost across real releases
- **Improvement / assay.**
- **Mechanism:** On UpgradeBench's 4 Qwen releases, cost four fleet policies: UpgradeBench's best per-specialist policy; migrate/demote (A); shim (HT08); and compatible base (HT07, simulated). Count compute, writer tokens, serving memory and served-ledger failures.
- **Nearest prior / gap:** UpgradeBench; level-3 HM26.
- **Cheapest first test:** 6 specialists across 3 transitions. **Kill** A–B's deployment claim if UpgradeBench's best policy is cheapest at equal served failures.
- **Old-task retention:** Served-ledger failures are the retention metric.
- **Risk / likely tie:** UpgradeBench's best policy is a strong control by construction.

### HT25 · Choose the tier per request under load
- **Primitive-candidate** (a serving operation that only multi-tier specs allow).
- **Mechanism:** When a multi-LoRA server's adapter slots are full, serve a behaviour from a lower tier that holds it on this base (prompt or steering vector, both HT01-accepted) instead of queueing. Per-request tier choice depends on load and on the behaviour's underdetermination at that tier (HT13).
- **Nearest prior / gap:** [S-LoRA](https://arxiv.org/abs/2311.03285) and [Punica](https://arxiv.org/abs/2310.18547) schedule adapters; none falls back to another representation of the same behaviour.
- **Cheapest first test:** Simulated load on 20 behaviours. **Kill** if tier fallback does not cut p95 latency by ≥ 30% at ≤ 1 pp ledger failure increase.
- **Old-task retention:** Ledger pass under fallback.
- **Risk / likely tie:** Few behaviours may hold at lower tiers; HT04's map decides.

## Ranked deeper questions

1. **Can a base upgrade be bent toward the fleet: one shim, or one compatibility loss, instead of N ports (HT07, HT08, HT09)?** This is the most novel operation in the branch: [BCT](https://arxiv.org/abs/2003.11942) for LLM bases and adapter fleets, checked with behavioural ledgers. First run: HT08's shim on S1's first upgrade against per-adapter ReLoRA and LoRA-X.
2. **Is migration between tiers ledger-invariant in both directions, and does demotion ever happen (HT01, HT02, HT04)?** If behaviours can move down as bases improve, the ledger rather than the adapter is what the system keeps learning. First run: HT02 across S1's upgrades.
3. **Is the underdetermination set a real object: coherent questions, a tier-choice signal, a regression predictor (HT12, HT13, HT14)?** It turns "complete only when rebuilds agree" from a stopping rule into a source of questions and predictions.
4. **Once HM17 passes, does acting before damage beat repairing after it (HT23 → HT16, HT20)?** If the gate fails, HT20 (the ledger gates self-edits) is the part of line (a) that survives.
