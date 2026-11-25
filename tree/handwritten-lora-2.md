# Handwritten LoRA 2: Adapter Contracts

Child of [LLM-handwritten LoRA weights](root-handwritten-lora.md) ([PR #400](https://github.com/manojbajaj95/cl/pull/400), depth 1) · 28 candidate cards (HC01–HC28) · 4 ranked deeper questions · Ideas only; no experiments run

**Parent verdict.** The review of #400 gave no card a 4 and kept two lines at 3:
- **(a)** Adapters as source code, recompiled onto a new base: rank-1 components with read/write claims and unit tests (HL06, HL21, HL22). Controls: Trans-LoRA, LoRA-X, retraining.
- **(b)** A trained adapter plus handwritten rank-1 counter-components for spillover and exceptions (HL15, HL17, HL14). Controls: AlphaEdit, MEMIT, neighbour replay, KL regularization.

**Thesis: the candidate primitive is the adapter contract.** A contract is a small persistent object:
- **claims:** for each component, what it reads and what it writes, stated in text with probe inputs;
- **unit tests:** input → expected behaviour, including the target behaviour;
- **protected neighbours:** inputs whose behaviour must not change;
- **counter-components:** handwritten rank-1 writes that cancel known side effects.

The LoRA numbers become a compiled artifact for one base model. Lines (a) and (b) are two operations on the same object: *compile* the contract onto a new base, and *patch* a compiled adapter where it violates the contract. The continual-learning claim to test: what a deployment learns should persist as contracts, not as weights. Contracts survive base upgrades, retraining and adapter revisions, and they accumulate every repair as a new test. Each card below has to make that object do work that a numeric transport method or a regularized retrain cannot do at equal information.

## Shared protocol

- **Fixtures.** **F1 (spillover):** Qwen3.5-0.8B; the StepGame / reference-frame rank-1 LoRA from [Writing weights or training them?](https://arxiv.org/abs/2611.27089), where the trained adapter reaches 98.8–100% but neighbouring distance tasks fall from 94% to 0–2%. Retrain it if it is not released. **F2 (porting):** 6 domain adapters (unit conversion, a format rule, a medical-QA subset, a refusal style, a fact set, F1's spatial skill) on Qwen2.5-0.5B, ported to Qwen2.5-1.5B (same family), to Qwen3.5-0.8B (new generation, changed vocabulary) and to SmolLM2-360M (other family). **F3 (stream):** F2's adapters revised 3 times each while the base is upgraded once in the middle.
- **Porting controls (line a), on every porting card:** [Trans-LoRA](https://arxiv.org/abs/2405.17258) (synthetic data and distillation), [LoRA-X](https://arxiv.org/abs/2501.16559) (training-free subspace projection), [Theseus](https://arxiv.org/abs/2602.12952) and [Ariadne](https://arxiv.org/abs/2610.32581) (training-free functional transport by Procrustes alignment and closed-form ridge), [Heirloom](https://arxiv.org/abs/2611.00650) (old personal model as teacher on unlabelled prompts), and **retraining** on the original data. Every control receives the contract's test inputs as extra unlabelled prompts (equal information, HC27).
- **Repair controls (line b), on every repair card:** [AlphaEdit](https://arxiv.org/abs/2410.02355) and [MEMIT](https://arxiv.org/abs/2210.07229) edits of the neighbour behaviour, **neighbour replay** (retrain with neighbour examples mixed in), **KL to the base on neighbour inputs** (as in [KLOD](https://arxiv.org/abs/2608.27839)), [DG-Hard spectral repair](https://arxiv.org/abs/2605.20296), [LoRA-Norm](https://arxiv.org/abs/2610.02067), and [HyperRepair](https://arxiv.org/abs/2610.41147) where a pretrained repair network exists. All get the same neighbour examples as the handwritten counter-components.
- **Retention.** Every card measures: the base's scores on 3 untouched benchmarks (GSM8K, IFEval, a held-out distance/neighbour set) with the adapter loaded, the pass rate of every previously accepted contract test, and the target gain. A method cannot gain by reverting to the base: target gain is a floor, not a trade-off.
- **Budget.** Bytes = adapter parameters + counter-components + contract text + stored test inputs. Writer tokens and evaluation calls are logged against GPU-seconds of training (HL32).

## Literature check

alphaXiv discovery on cross-model LoRA/task-vector transfer, cross-model representation alignment, post-hoc repair of fine-tuning damage, and specification/provenance of adapters; abstracts checked on arXiv. Abstract-level screen, not full-text priority claims.

| Nearest prior | What it already does | Boundary for this node |
|---|---|---|
| [Trans-LoRA](https://arxiv.org/abs/2405.17258), [LoRA-X](https://arxiv.org/abs/2501.16559), [ReLoRA](https://arxiv.org/abs/2606.02606), [Heirloom](https://arxiv.org/abs/2611.00650), [GRAFT](https://arxiv.org/abs/2611.18638) | Port adapters across base versions, sizes, vocabularies, or text→VL, by distillation, subspace projection, re-initialization or a learned linear bridge. | Porting numbers is solved well enough to be the control. A contract port must win where these silently degrade (a missing feature, a changed tokenizer, chained upgrades), or say *which* component failed. |
| [Theseus](https://arxiv.org/abs/2602.12952), [Ariadne](https://arxiv.org/abs/2610.32581), [Transport and Merge](https://arxiv.org/abs/2602.05495) | Training-free functional transport: match the activation change an update causes, align spaces with Procrustes, solve for a native update. | Closest to "port the intent": they port the *function on observed activations*. The contract adds a stated per-component meaning and pass/fail tests, so a port can be checked and repaired one component at a time. |
| [MATCHA](https://arxiv.org/abs/2610.09058), [Interpretability Is Not Model-Specific](https://arxiv.org/abs/2611.12675), [Linear Representation Transferability](https://arxiv.org/abs/2506.00653), [Cross-architecture steering](https://arxiv.org/abs/2608.05164) | Learned maps between residual streams carry refusal directions and probes across 110 model pairs; transfer rises from 54% to 102% of refusal steering when the map is fit on prompts from the tool's own region. | Direction-level transfer works when fit on the right prompts. HC06 uses that finding: the contract's tests are the prompts. |
| [Backbone-Specific LoRA Geometry](https://arxiv.org/abs/2611.27201), [Audit Before You Merge](https://arxiv.org/abs/2611.10684), [From LoRA to Language](https://arxiv.org/abs/2611.09454) | Provenance signatures of LoRAs; auditing merged adapters for forgetting; recovering skill documents from adapters. | Provenance and text recovery exist. Executable tests, and compiling back to weights, are not part of them. |
| [DG-Hard / Spectral Unforgetting](https://arxiv.org/abs/2605.20296), [LoRA-Norm](https://arxiv.org/abs/2610.02067), [HyperRepair](https://arxiv.org/abs/2610.41147), [SPECTRA](https://arxiv.org/abs/2611.10279), [CSULoRA](https://arxiv.org/abs/2605.30640), [MaLoRA](https://arxiv.org/abs/2611.14397) | Post-hoc repair of fine-tuning damage: spectral thresholding, gain rebalancing, a gated side network from a hypernetwork, a training-free low-rank transfer of the refusal direction, a closest safe update, margin-based robustness. | Generic, data-free or amortized repairs of general capability. The counter-component line targets *named* neighbours from a handful of examples, ships as part of the contract, and must survive retraining and porting. SPECTRA is the closest single-behaviour training-free low-rank repair and is a control on HC14. |
| [ROME](https://arxiv.org/abs/2202.05262), [MEMIT](https://arxiv.org/abs/2210.07229), [AlphaEdit](https://arxiv.org/abs/2410.02355), [KLOD](https://arxiv.org/abs/2608.27839), [ripple-effect editing](https://arxiv.org/abs/2606.01610) | Closed-form or locality-constrained edits of facts and their neighbourhoods. | Fact neighbourhoods are covered. F1's neighbours are skills (distance reasoning), where these methods are the control rather than the answer. |

Ledger results this node respects: the WSP CL repair was killed at proposal ([PR #7](https://github.com/manojbajaj95/cl/pull/7)), so "an LLM repairs forgetting by editing weights" is not a card here. A card has to rely on the contract persisting. Fine-tuning damage was diffuse in [PR #24](https://github.com/manojbajaj95/cl/pull/24), so every repair card first measures how concentrated F1's spillover is (HC13).

## A · The contract as an object

### HC01 · Contract format and checker
- **Primitive** (new object; the base for every other card).
- **Mechanism:** A contract is a list of (component id, read claim + 10 probe inputs, write claim + expected logit shift, unit tests, protected-neighbour set) plus a list of counter-components with the neighbour each one protects. A checker compiles nothing. Given a base and an adapter, it reports, per component, whether the read projection exceeds its threshold on the probe inputs, whether the write shifts logits as claimed, whether the tests pass, and whether the neighbours are unchanged within a KL bound.
- **Nearest prior / gap:** HL06 in the parent; [From LoRA to Language](https://arxiv.org/abs/2611.09454) recovers text skill documents but nothing executable; WeightBench grades writes but does not keep a per-component contract.
- **Cheapest first test:** Write contracts for F2's 6 adapters on Qwen2.5-0.5B. **Kill** if the checker's per-component verdicts do not predict the effect of ablating that component (Spearman < 0.6 between "claim holds" and ablation loss on its tests).
- **Old-task retention:** The protected-neighbour field is the retention spec; check it against the 3 benchmarks.
- **Risk / likely tie:** Claims may be true but too broad to be useful (a read claim like "numbers"); HC04 checks coverage.

### HC02 · The minimal contract that pins an adapter
- **Primitive-candidate** (a new quantity: the smallest set of tests from which an adapter with equivalent behaviour can be regenerated).
- **Mechanism:** Greedily drop tests and claims while a regenerated adapter (written from the contract alone on the same base) still matches the original on held-out inputs. The result is the adapter's description length as an executable spec. It sets the cost of storing adapters as contracts (HC10).
- **Nearest prior / gap:** Edit-description lower bounds on the repo's `tree-edit-description-lower-bound` branch are about text edit descriptions; there is no executable minimal spec for adapters.
- **Cheapest first test:** F2's 6 adapters. **Kill** if the minimal contract is larger in bytes than the rank-4 adapter it pins.
- **Old-task retention:** Regenerated adapters must match the original's retention, not only its target gain.
- **Risk / likely tie:** Format adapters may need few tests and knowledge adapters many; report per type.

### HC03 · Extract a contract from a trained adapter
- **Primitive-candidate** (the operation that lets line (a) apply to adapters nobody handwrote).
- **Mechanism:** Most deployed adapters are trained. The writer probes a trained LoRA's SVD components (top-activating inputs, logit shifts, ablations) and writes a contract for it: claims per retained component, tests sampled from the training distribution, and protected neighbours found by diffing behaviour on a neighbour bank. Components it cannot describe are listed as "undocumented" with their measured share of the gain.
- **Nearest prior / gap:** [From LoRA to Language](https://arxiv.org/abs/2611.09454), [W2T](https://arxiv.org/abs/2603.15990), HL14.
- **Cheapest first test:** F1's trained adapter plus 3 trained F2 adapters. **Kill** if the documented components carry < 70% of the target gain.
- **Old-task retention:** The neighbour diff must find F1's distance collapse without being told about it.
- **Risk / likely tie:** Trained adapters may be mostly undocumentable; that number is itself a result for line (a).

### HC04 · Mutation testing a contract
- **Improvement** (borrowed from software testing; checks whether a contract is strong enough to rely on).
- **Mechanism:** Apply mutations to a compiled adapter: flip the sign of a component, rotate a read direction, add a random rank-1 of matched norm, add a planted trigger. Contract strength = fraction of behaviour-changing mutations the tests catch. Weak contracts are strengthened by adding tests that catch the surviving mutants.
- **Nearest prior / gap:** Mutation testing of programs; [Patch-correctness audits](https://arxiv.org/abs/2611.10837) show that test-guided repair overfits weak tests.
- **Cheapest first test:** F2 contracts, 200 mutants each. **Kill** if the mutation score after strengthening is not ≥ 0.9 at ≤ 2× the original test count.
- **Old-task retention:** Mutants that change only neighbour behaviour must be caught by the neighbour tests.
- **Risk / likely tie:** Rotations within the read span may not change behaviour; count only mutants that change held-out behaviour.

## B · Compile the contract onto a new base (line a)

### HC05 · Contract-guided port versus numeric transport
- **Primitive-candidate** (the main test of line (a)).
- **Mechanism:** For each component, the writer finds the new base's direction for the read claim (probe inputs → activation difference) and the write claim (target logit shift). It writes the rank-1 component natively on the new base, then runs the contract's tests. Components that fail are rewritten, or flagged (HC08).
- **Nearest prior / gap:** [Theseus](https://arxiv.org/abs/2602.12952) and [Ariadne](https://arxiv.org/abs/2610.32581) port the whole update's functional effect; [LoRA-X](https://arxiv.org/abs/2501.16559) projects subspaces; [Trans-LoRA](https://arxiv.org/abs/2405.17258) and [Heirloom](https://arxiv.org/abs/2611.00650) distill. None ports per component against tests.
- **Cheapest first test:** F2, 3 targets. Use all porting controls at equal information. **Kill** if contract port does not beat the best training-free control (Theseus/Ariadne/LoRA-X) on mean target accuracy at equal retention on ≥ 2 of 3 targets, or retraining reaches it with ≤ 50 examples.
- **Old-task retention:** New base's 3 benchmarks plus the contract's neighbour tests on the new base.
- **Risk / likely tie:** Ariadne already does activation-matched closed-form synthesis per block. It may tie on same-family ports, so the win must come on the cross-family and new-vocabulary targets.

### HC06 · Contract tests as alignment prompts
- **Improvement** (makes the strongest control better and tells us whether the contract's value is just its inputs).
- **Mechanism:** [Interpretability Is Not Model-Specific](https://arxiv.org/abs/2611.12675) found that a residual-stream map recovers 54% of refusal steering when fit on ordinary prompts and 102% when fit on prompts from the tool's region. Fit MATCHA/Procrustes maps on the contract's probe and test inputs, then transport. If this matches HC05, the contract is worth only as much as its prompts.
- **Nearest prior / gap:** That paper; [MATCHA](https://arxiv.org/abs/2610.09058).
- **Cheapest first test:** F2 → Qwen3.5-0.8B and SmolLM2. **Kill** (HC05's claim) if contract-prompt transport is within 1 SE of contract port.
- **Old-task retention:** Same as HC05.
- **Risk / likely tie:** Likely closes much of the gap. This is the decisive control for line (a).

### HC07 · Port each component on its own and localize failures
- **Primitive-candidate** (new operation: a partial port with a per-component report).
- **Mechanism:** Transport passing components numerically (cheap) and rewrite by hand only the components whose tests fail on the new base. The output is a port plus a list: "component 3 (reads 'metric unit', writes 'convert') failed on SmolLM2; rewritten with direction found from probes".
- **Nearest prior / gap:** Whole-update transport methods give one aggregate score.
- **Cheapest first test:** F2 → 3 targets. **Kill** if mixed porting does not reach HC05's accuracy at ≤ 50% of its writer tokens, or failing components are not concentrated (< 70% of the accuracy loss in ≤ 2 components).
- **Old-task retention:** Per-component neighbour tests.
- **Risk / likely tie:** Failures may be spread across components (PR #24's diffuse damage, in porting form).

### HC08 · Refuse a port the new base cannot host
- **Primitive-candidate** (new behaviour: a port that says "this claim has no home here" instead of degrading silently).
- **Mechanism:** Some claims rely on a feature the new base lacks (a token merged away, a capability absent at 360M). The writer tests whether the read claim's probes separate in any layer of the new base (a linear probe) before writing. If they do not, the port reports the claim unportable and proposes a substitute (a different read feature for the same tests) or an explicit gap.
- **Nearest prior / gap:** Numeric transport always returns an update; WeightBench has an impossibility-recognition track for writing, not for porting.
- **Cheapest first test:** Plant 2 unportable claims (features removed by tokenizer change or absent at small scale) in F2. **Kill** if refusal precision/recall < 0.8, or if the controls' silent degradation is not detectable from their outputs anyway.
- **Old-task retention:** Refused components are not loaded, so check that the remaining port keeps the neighbours.
- **Risk / likely tie:** Linear probes may find spurious separability; require causal steering, not only probing.

### HC09 · Ports across a tokenizer change
- **Improvement** (a regime where numeric transport is weakest).
- **Mechanism:** Claims and tests are stated in strings, so they survive a vocabulary change; the writer re-derives the write directions in the new vocabulary's unembedding. [Heirloom](https://arxiv.org/abs/2611.00650) names vocabulary changes as a reason adapters become incompatible.
- **Nearest prior / gap:** Heirloom's teacher distillation handles it with stored unlabelled inputs.
- **Cheapest first test:** Qwen2.5-0.5B → SmolLM2-360M (different tokenizers). **Kill** if contract port does not beat Heirloom at equal unlabelled prompts.
- **Old-task retention:** New base's benchmarks.
- **Risk / likely tie:** Heirloom is strong when inputs are plentiful; the contract has to win when only its tests are available.

### HC10 · Store contracts, compile adapters on demand
- **Primitive-candidate** (new fleet design: the stored artifact is the contract; adapters are a per-base build cache).
- **Mechanism:** A multi-LoRA server keeps contracts for N domains. When the base changes, adapters are compiled lazily on first request and cached. This gives storage per domain = contract bytes (HC02), a cold-start latency, and a rebuild cost per base upgrade.
- **Nearest prior / gap:** [ReLoRA](https://arxiv.org/abs/2606.02606) re-adapts stored adapters for evolving services; S-LoRA/Punica serve them.
- **Cheapest first test:** Simulate 20 domains, 3 base upgrades. **Kill** if total cost (writer tokens + checks) per upgrade exceeds ReLoRA's re-adaptation cost at equal accuracy.
- **Old-task retention:** Each compiled adapter must pass its full contract before it is served.
- **Risk / likely tie:** Compilation by a frontier writer is slow; the win depends on how often bases change.

### HC11 · Chained upgrades without accumulated drift
- **Primitive-candidate** (a property: contracts do not drift because each port is checked against the original tests).
- **Mechanism:** Port an adapter along Qwen2.5 → Qwen3 → Qwen3.5. Numeric transport chains its errors from hop to hop; a contract port re-derives every hop from the same claims and tests.
- **Nearest prior / gap:** Numeric transport papers evaluate single hops.
- **Cheapest first test:** 3 F2 adapters, 2-hop chain. **Kill** if the controls' drift over 2 hops is < 3 pp (nothing to fix) or contract port drifts as much.
- **Old-task retention:** Neighbour tests at every hop.
- **Risk / likely tie:** Two hops may be too few to show drift; add a third (Qwen3.5-9B) if needed.

### HC12 · Port the trained adapter and its counter-components together
- **Primitive-candidate** (joins lines a and b).
- **Mechanism:** A deployed unit is trained adapter + counter-components (line b). On a base upgrade, the trained part is ported numerically or retrained, and the counter-components are re-derived from their contract entries ("cancel the write on distance questions") against the *ported* adapter's new spillover. The new spillover may differ, so counters are re-measured, not copied.
- **Nearest prior / gap:** No porting method carries repairs; HyperRepair generalizes repairs across adaptation domains on one backbone.
- **Cheapest first test:** F1 adapter + counters, ported to Qwen3.5-9B and Qwen2.5-1.5B. **Kill** if the re-derived counters do not restore the neighbours on the new base better than (a) copying them numerically or (b) neighbour replay during retraining on the new base.
- **Old-task retention:** Distance tasks on the new base.
- **Risk / likely tie:** Retraining with replay on the new base is a strong, simple control.

## C · Counter-components for spillover and exceptions (line b)

### HC13 · Measure how concentrated the spillover is before repairing it
- **Improvement / assay** (gate for the whole of section C, per PR #24).
- **Mechanism:** For F1's trained adapter, ablate each SVD component and each layer; compute what fraction of the neighbour collapse is explained by the top-k read directions. A concentrated spillover can be cancelled by a rank-1 or rank-2 counter; a diffuse one cannot.
- **Nearest prior / gap:** [LoRA-Norm](https://arxiv.org/abs/2610.02067) finds that a few singular directions dominate trained updates ("adaptation imbalance"), which suggests concentration; PR #24 found diffuse damage on GPT-2-XL edits.
- **Cheapest first test:** F1 plus 3 F2 adapters with measured neighbour damage. **Kill** section C for an adapter whose top-2 directions explain < 50% of its neighbour loss.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** The rank-1 F1 adapter is concentrated by construction; F2's rank-8 adapters are the real test.

### HC14 · Handwritten counter-component versus the repair controls
- **Primitive-candidate** (the main test of line b).
- **Mechanism:** The writer adds 1–2 rank-1 components that read the neighbour's direction (from 5 neighbour examples) and write the negative of the trained adapter's write on those inputs. Their contract entry names the neighbour and the trained component they cancel.
- **Nearest prior / gap:** [SPECTRA](https://arxiv.org/abs/2611.10279) restores one behaviour (refusal) with a training-free low-rank activation-aware update; [DG-Hard](https://arxiv.org/abs/2605.20296) and [HyperRepair](https://arxiv.org/abs/2610.41147) repair general capability. A counter aimed at a named skill neighbour, from 5 examples, that stays part of the deployed unit, is not in the abstracts read.
- **Cheapest first test:** F1. Run all repair controls at 5 and 50 neighbour examples. **Kill** if the counter does not restore distance accuracy to ≥ 80% with ≤ 5 pp target loss at 5 examples, or SPECTRA-style transfer of the base's neighbour direction, AlphaEdit, or KL retraining matches it at 5 examples.
- **Old-task retention:** Distance tasks, 3 benchmarks, and the trained adapter's target tests.
- **Risk / likely tie:** SPECTRA's recipe applied to the distance direction is close to this card. The difference must come from cancelling the adapter's own write rather than re-adding the base's direction.

### HC15 · Retract or counter: a decision rule
- **Improvement.**
- **Mechanism:** For each spillover, either retract the trained component that causes it (if it carries little target gain) or add a counter (if it carries the gain). The rule is a measured trade-off per component: target gain lost by retracting versus bytes and residual damage of countering.
- **Nearest prior / gap:** DG-Hard thresholds singular values globally; LoRA-Norm rebalances gains.
- **Cheapest first test:** F2's rank-8 adapters. **Kill** if the rule does not beat always-counter and always-retract on (target, neighbour) jointly.
- **Old-task retention:** Neighbours and benchmarks.
- **Risk / likely tie:** A global spectral rule may approximate it.

### HC16 · Gate the counter on the neighbour's read direction
- **Improvement** (keeps the counter inert on target inputs).
- **Mechanism:** A plain counter also fires on target inputs that share the read direction, and costs target accuracy. Gate it with a trigger component (HL10) that fires only when the neighbour's distinguishing feature is present.
- **Nearest prior / gap:** HyperRepair's prompt-conditioned gate on its side network.
- **Cheapest first test:** F1, where distance and reference-frame questions share spatial features. **Kill** if gating does not cut target loss by ≥ 50% versus the ungated counter at equal neighbour recovery.
- **Old-task retention:** Neighbours, target and benchmarks.
- **Risk / likely tie:** HyperRepair's learned gate may do this without handwriting.

### HC17 · Keep counters valid when the trained adapter is retrained
- **Primitive-candidate** (new operation: detect and rewrite stale repairs).
- **Mechanism:** Domains change, so the trained adapter is retrained on new data. Its spillover moves, and an old counter may now over-correct. The contract's neighbour tests detect staleness after every retrain; stale counters are re-derived rather than kept or dropped.
- **Nearest prior / gap:** Repair methods are one-shot after a fixed fine-tune.
- **Cheapest first test:** F3, 3 retrains per adapter. Arms: keep counters, drop counters, re-derive on test failure, neighbour replay in every retrain. **Kill** if re-derivation does not beat replay-in-retrain on neighbour retention at equal neighbour examples.
- **Old-task retention:** All neighbour tests after each retrain.
- **Risk / likely tie:** Replay in every retrain is simple and strong.

### HC18 · One shared counter for a neighbour many adapters break
- **Primitive-candidate** (new fleet object: a counter shared across hot-swapped adapters).
- **Mechanism:** Several domain adapters damage the same neighbour (e.g. arithmetic). Instead of one counter per adapter, write one counter for the shared damage direction and load it whenever any of them is loaded. With several loaded at once (multi-LoRA), per-adapter counters add up and over-correct; one shared counter does not.
- **Nearest prior / gap:** HyperRepair generates per-model side nets; [Audit Before You Merge](https://arxiv.org/abs/2611.10684) audits forgetting after merging adapters.
- **Cheapest first test:** 6 F2 adapters, all subsets of size 1–3 co-loaded. **Kill** if the shared counter does not beat per-adapter counters on worst-subset neighbour accuracy.
- **Old-task retention:** Neighbours under every co-load subset.
- **Risk / likely tie:** Adapters may damage the neighbour in different directions.

### HC19 · Turn repairs into constraints on the next training round
- **Primitive-candidate** (learning from repairs: the contract changes how the next adapter is trained).
- **Mechanism:** Each counter-component's neighbour tests enter the next training round as KL constraints on those inputs ([KLOD](https://arxiv.org/abs/2608.27839)-style). The measure: does the next trained adapter need fewer or smaller counters? Repairs are then a curriculum for training, not a permanent patch.
- **Nearest prior / gap:** KL regularization with a fixed neighbour set; the new part is a neighbour set grown from repairs that were actually needed.
- **Cheapest first test:** F3, 3 rounds. **Kill** if contract-grown constraints do not cut counter bytes needed by ≥ 50% by round 3 versus a random neighbour set of equal size.
- **Old-task retention:** All accumulated tests each round.
- **Risk / likely tie:** A large generic KL set may prevent most spillover at a small target cost.

### HC20 · Handwritten exception components with their own tests
- **Primitive-candidate** (extends HL17).
- **Mechanism:** Training learns the rule; rare irregular cases get one rank-1 exception component each, with a read claim keyed narrowly to the case and a test. Exceptions are retired when a later trained adapter absorbs them (their tests pass without them).
- **Nearest prior / gap:** [MEMIT](https://arxiv.org/abs/2210.07229) for fact exceptions; upweighting rare cases in training.
- **Cheapest first test:** Unit conversion with 5% irregular units; F3 schedule. **Kill** if exception components do not beat upweighting and MEMIT on exception accuracy without hurting the rule.
- **Old-task retention:** Rule cases and benchmarks.
- **Risk / likely tie:** MEMIT ties when exceptions are fact-like.

## D · Contracts in a continual stream

### HC21 · Retrain under the full contract
- **Improvement** (the contract as a retention objective).
- **Mechanism:** Every retrain must pass all accepted tests. These enter the loss as hinge constraints, and a write is rejected if any test fails. Compare with replay of the same test inputs as data.
- **Nearest prior / gap:** Replay, KL, and constrained fine-tuning.
- **Cheapest first test:** F3. **Kill** if hinge-on-tests does not beat replay-of-tests at equal inputs on retention, or if it blocks target learning (> 3 pp target loss).
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** Replay of the same inputs may tie.

### HC22 · Detect conflicts between contracts before co-loading
- **Primitive-candidate** (new check: contract versus contract, not weights versus weights).
- **Mechanism:** Two domain contracts may require different behaviour on overlapping inputs. Running each contract's tests with the other adapter loaded finds conflicts before deployment. Conflicts are resolved by narrowing a read claim or by a routing rule written into both contracts.
- **Nearest prior / gap:** HL12's commutation certificate compares spans; TIES resolves sign conflicts in weights.
- **Cheapest first test:** 6 F2 adapters with 3 planted behavioural conflicts. **Kill** if cross-testing misses > 1 planted conflict or flags > 20% false conflicts.
- **Old-task retention:** Each domain's tests under co-loading.
- **Risk / likely tie:** Weight-space interference scores may find the same pairs.

### HC23 · Version history and blame across revisions and base upgrades
- **Improvement / tooling.**
- **Mechanism:** Keep each contract's history (claims added, tests added, counters added, ports) so that a regression after a base upgrade or revision can be traced to the change that introduced it.
- **Nearest prior / gap:** Software VCS; model registries track checkpoints, not contracts.
- **Cheapest first test:** F3 with 2 planted regressions. **Kill** if blame does not find both faster than bisecting checkpoints.
- **Old-task retention:** Not applicable (tooling); regression found is the retention event.
- **Risk / likely tie:** Likely tooling; keep only if HC05/HC14 survive.

### HC24 · Does contract pass rate predict benchmark retention?
- **Improvement / assay** (whether contracts can stand in for expensive retention evaluation).
- **Mechanism:** Across all F3 events, correlate the change in contract-test pass rate with the change in the 3 benchmarks. If they track, contracts are a cheap, always-on retention monitor for a serving fleet.
- **Nearest prior / gap:** Small canary sets in deployment.
- **Cheapest first test:** Log both on every F3 event. **Kill** if Spearman < 0.5, or a random canary set of equal size predicts as well.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** A random canary may do as well; then contracts are only for porting and repair.

### HC25 · Does a contract converge?
- **Primitive-candidate** (a property of a stream: repairs stop being needed).
- **Mechanism:** Each repair adds a test. Track new tests needed per revision. If the count falls toward zero, the contract has captured the domain's behaviour and later revisions and ports are cheap. If it grows linearly, contracts are a log, not a spec.
- **Nearest prior / gap:** Test-suite growth in software.
- **Cheapest first test:** F3 extended to 8 revisions on 2 adapters. **Kill** if new tests per revision do not decline over 8 revisions.
- **Old-task retention:** Full contract every revision.
- **Risk / likely tie:** Domains with drifting distributions will not converge by construction; use stable ones first.

## E · Keep the comparison honest

### HC26 · Contract gaming by the writer
- **Improvement / assay.**
- **Mechanism:** A writer can write tests that its own adapter passes trivially. A separate generator writes held-out adversarial tests from the claims alone, and a contract's score is its adapter's pass rate on those.
- **Nearest prior / gap:** [Patch-correctness audits](https://arxiv.org/abs/2611.10837): test-guided repair overfits.
- **Cheapest first test:** F2. **Kill** (the reported pass rates) if held-out pass rate is > 15 pp below the writer's own tests.
- **Old-task retention:** Held-out neighbour tests are part of the adversarial set.
- **Risk / likely tie:** None; required for every headline number.

### HC27 · Equal-information controls
- **Improvement / assay.**
- **Mechanism:** Every porting and repair control gets the contract's inputs (probe inputs, test inputs, neighbour inputs) as extra unlabelled prompts or examples. This separates the value of the contract's *structure* (per-component claims, pass/fail, counters) from the value of its *inputs*.
- **Nearest prior / gap:** HC06 is one instance.
- **Cheapest first test:** Re-run HC05 and HC14 controls with the inputs. **Kill** (the structure claim) if structured methods lose their advantage.
- **Old-task retention:** Same as the cards it controls.
- **Risk / likely tie:** Likely to shrink every gap; required.

### HC28 · Cost of contracts versus retraining
- **Improvement / assay.**
- **Mechanism:** Writer tokens for writing, extracting and porting contracts plus evaluation calls, against GPU-seconds of retraining with replay, per domain per base upgrade. Find the fleet size and upgrade frequency at which contracts pay.
- **Nearest prior / gap:** HL32 in the parent.
- **Cheapest first test:** From HC05, HC10 and HC14 logs. **Kill** the deployment pitch if no regime with ≤ 100 domains and ≤ 4 upgrades a year favours contracts.
- **Old-task retention:** Compare at equal retention.
- **Risk / likely tie:** Retraining small adapters is cheap; contracts must pay through fewer failed deployments and smaller data retention, not compute.

## Ranked deeper questions

1. **Does a per-component contract port better than the best functional transport fed the same inputs (HC05, HC06, HC27, HC08)?** This is line (a)'s whole claim. Ariadne/Theseus with contract-region prompts (per the 54% → 102% finding) is the control most likely to tie. If the contract only wins by refusing unportable claims (HC08), that is still a primitive: a port that knows what it lost. First run: HC06 against HC05 on F2 → SmolLM2.
2. **Can 1–2 handwritten rank-1 counters from 5 examples restore a named skill neighbour that training destroyed, better than SPECTRA-style transfer, AlphaEdit and KL retraining (HC13, HC14, HC16)?** Gate on HC13's concentration check, then run HC14 on F1. This is the cheapest decisive experiment in the node.
3. **Do repairs persist as knowledge across retraining and base upgrades (HC12, HC17, HC19)?** The continual-learning payoff: a deployment should not re-discover the same spillover after every retrain or upgrade. If contract-grown constraints (HC19) make later adapters need fewer counters, the contract is learning from its repairs.
4. **Is the contract a spec or a log (HC02, HC25, HC24)?** If minimal contracts are smaller than adapters and new tests per revision fall to zero, storing contracts and compiling adapters per base (HC10) becomes a real fleet design. If not, contracts are an audit trail and lines (a) and (b) stand separately.
