# Handwritten LoRA 3: Store the Tests, Rebuild the Weights

Child of [Handwritten LoRA 2: Adapter Contracts](handwritten-lora-2.md) ([PR #401](https://github.com/manojbajaj95/cl/pull/401), depth 2) · 26 candidate cards (HM01–HM26) · 4 ranked deeper questions · Ideas only; no experiments run

**Parent verdict.** The review of #401 gave no card a 4 and kept two lines at 3:
- **(a)** A minimal regenerating contract (HC02, HC10): store only contracts and rebuild adapters per base. Controls: stored weights at equal bytes, Text-to-LoRA, ReLoRA, LoRA-X.
- **(b)** Repairs that persist across retrains (HC17, HC19): neighbour tests become KL constraints. Controls: one-shot repair, KLOD, replay.

**Thesis.** Both lines store behaviour as tests instead of weights.
- **Line (a)** asks how few tests can pin a behaviour well enough to regenerate it on any base. That is a rate–behaviour curve: contract bytes against behavioural distortion of the rebuilt adapter. The only claim that would be new is that, after a base upgrade, this curve beats weights compressed to the same bytes and then ported.
- **Line (b)** asks whether the tests created by repairs are the right constraints for future training. [Why Constrained Updates Still Forget](https://arxiv.org/abs/2610.30191) splits forgetting under constraints into probe mismatch, gradient staleness and finite-step terms. Repair-derived tests are probes placed exactly where forgetting has already happened, so they should shrink the probe-mismatch term.

**Candidate primitive: a behaviour ledger.** It is an append-only set of (input, expected behaviour, provenance) entries. Every write, repair and base upgrade reads it as a constraint and adds to it. Weights are rebuilt from it, and the cards test whether it stays small.

## Shared protocol

Inherits F1–F3, retention, budget, and equal-information rules from [the parent](handwritten-lora-2.md#shared-protocol).
- **Line (a) controls:**
  - **Stored weights at equal bytes:** the adapter compressed to the contract's byte count with [NOLA](https://arxiv.org/abs/2310.02556), [SeedLM](https://arxiv.org/abs/2410.10714)-style seeds, or [Kilobyte Models](https://arxiv.org/abs/2608.00860) seed + quantized latent; on a new base, ported with [LoRA-X](https://arxiv.org/abs/2501.16559) or re-adapted with [ReLoRA](https://arxiv.org/abs/2606.02606).
  - **[Text-to-LoRA](https://arxiv.org/abs/2506.06105)** given the contract's text as its description.
  - **Store the data:** raw training examples at equal bytes, then retrain.
- **Line (b) controls:**
  - **One-shot repair:** counter-components or DG-Hard repair after each retrain, without carrying anything forward.
  - **[KLOD](https://arxiv.org/abs/2608.27839)** with a fixed neighbour set.
  - **Replay** of the same neighbour inputs.
  - **Regression-free update methods:** [positive-congruent training](https://arxiv.org/abs/2011.09161), the [NLP regression-bug constrained update](https://arxiv.org/abs/2105.03048), and [margin-preserving training](https://arxiv.org/abs/2511.08322), all on the full old-correct set at equal compute.
- **Streams.** **S1:** F3 extended to 3 base upgrades (Qwen2.5-0.5B → Qwen2.5-1.5B → Qwen3.5-0.8B → SmolLM2-360M) and 6 retrains per adapter, 6 domains. **S2:** F1's spatial skill retrained 6 times on shifting StepGame splits, with the distance neighbours tracked.

## Literature check

alphaXiv discovery on regenerating weights from compact descriptions, regression-free model updates and negative flips, and constrained continual fine-tuning of LLMs; abstracts checked on arXiv. Abstract-level screen, not full-text priority claims.

| Nearest prior | What it already does | Boundary for this node |
|---|---|---|
| [NOLA](https://arxiv.org/abs/2310.02556), [PRANC](https://arxiv.org/abs/2206.08464), [SeedLM](https://arxiv.org/abs/2410.10714), [Kilobyte Models](https://arxiv.org/abs/2608.00860), [random reparameterization theory](https://arxiv.org/abs/2608.12597) | The deployable artifact is a seed plus a few coefficients or a quantized latent; weights are regenerated exactly. | Equal-bytes weight compression is the line-(a) control. It is tied to one base, and a contract is not. A card must win after a base change, or on a format change (HM12). |
| [Text-to-LoRA](https://arxiv.org/abs/2506.06105), [Drag-and-Drop](https://arxiv.org/abs/2506.16406), [ReLoRA](https://arxiv.org/abs/2606.02606), [LoRA-X](https://arxiv.org/abs/2501.16559), [Heirloom](https://arxiv.org/abs/2611.00650) | Regenerate from a description or prompts; re-adapt or project stored adapters to a new base; distill on stored unlabelled inputs. | Tests with expected behaviour are more than a description and less than a dataset. The card must show which bytes earn their place. |
| [Positive-congruent training](https://arxiv.org/abs/2011.09161), [regression bugs in NLP updates](https://arxiv.org/abs/2105.03048), [margin-preserving training](https://arxiv.org/abs/2511.08322), [no universal signal predicts LLM regression](https://arxiv.org/abs/2608.13607), [regression-testing world models](https://arxiv.org/abs/2610.41130) | Negative flips are measured and reduced by constrained or distillation objectives over old-correct samples. No inference-time signal predicts sample-level regressions across LLM versions. | Constraining all old-correct samples is the line-(b) control. The candidate is a constraint set *grown from repairs* that is far smaller. HM17 tests whether repair history is the predictive signal that 2608.13607 did not find. |
| [Why Constrained Updates Still Forget](https://arxiv.org/abs/2610.30191), [KLOD](https://arxiv.org/abs/2608.27839), [Self-Preservation](https://arxiv.org/abs/2610.12602), [Self-addressed replay](https://www.alphaxiv.org/abs/2611.self-addressed-replay-language-model-facts), [Low-rank Fisher regularisation](https://arxiv.org/abs/2611.20288), [Null-basis LoRA](https://arxiv.org/abs/2609.25618) | Constrained SFT forgets through probe mismatch and staleness, and a refresh budget follows. Models choose their own preservation targets from task banks. Low-rank Fisher protects safety subspaces. | Choosing *where* to constrain is the open part. Repair-derived probes are one answer; self-chosen targets (HM21) and Fisher (HM16) are its controls. |
| [SkillEvoReg](https://arxiv.org/abs/2609.30861), [risks of LLM-generated regression tests](https://arxiv.org/abs/2610.11835) | Text-skill evolution overfits and grows; LLM-written regression tests can encode current bugs as expected behaviour. | The ledger must prune (HM18) and must not freeze wrong behaviour (HM23, HM25). |

## A · Regenerating contracts (line a)

### HM01 · The rate–behaviour curve of a contract
- **Primitive-candidate** (new measure: contract bytes against the behavioural distortion of an adapter rebuilt from them).
- **Mechanism:** For each F2 adapter, prune the contract to sizes from 0.5 KB to 64 KB (HC02's greedy pruning). Rebuild an adapter from each size and measure distortion as mean KL to the original adapter's outputs on held-out domain inputs, plus target accuracy. Draw the same curve for NOLA/SeedLM/Kilobyte-compressed adapters and for stored raw data.
- **Nearest prior / gap:** Weight-compression rate–distortion; HC02 found only a single minimal point.
- **Cheapest first test:** 3 adapters, same base. **Kill** nothing yet: on the same base, compressed weights are expected to dominate. Record the gap; HM02 is where the contract must win.
- **Old-task retention:** Each rebuilt adapter's 3-benchmark retention is part of distortion.
- **Risk / likely tie:** None; this sets the baseline curve.

### HM02 · The curve after a base upgrade
- **Primitive-candidate** (the decisive test of line a).
- **Mechanism:** Repeat HM01 on each new base in S1. Weight-compressed adapters must be decompressed and then ported (LoRA-X, ReLoRA) or re-adapted; contracts are rebuilt natively. The claim holds if, at equal stored bytes, the contract curve lies below the ported-weights curve on the new base.
- **Nearest prior / gap:** ReLoRA and LoRA-X port full-precision stored adapters; nobody has compared at equal bytes.
- **Cheapest first test:** 3 adapters × 1 upgrade (Qwen2.5-0.5B → Qwen3.5-0.8B). **Kill** if compressed-then-ported weights match the contract at every byte budget ≤ 16 KB, or Text-to-LoRA on the contract text matches it.
- **Old-task retention:** New base's benchmarks and neighbour tests.
- **Risk / likely tie:** ReLoRA with a few examples may be enough. Give it the contract's inputs (equal information).

### HM03 · Which regenerator: a reasoning writer or a trained contract-to-LoRA network
- **Improvement** (makes regeneration cheap enough to serve).
- **Mechanism:** Rebuilding with a frontier writer is slow. Train a T2L-style hypernetwork whose input is (contract text + test inputs + expected outputs) and whose output is a LoRA, on pairs collected from writer rebuilds. Then compare: writer, contract hypernetwork, and Text-to-LoRA (description only).
- **Nearest prior / gap:** [Text-to-LoRA](https://arxiv.org/abs/2506.06105) uses descriptions; the tests are the added input. PR #344's Learner is the same machinery.
- **Cheapest first test:** 40 small domains for training the hypernetwork, 6 held out. **Kill** (the tests' value) if the hypernetwork with tests is not ≥ 1 SE better than Text-to-LoRA on held-out domains.
- **Old-task retention:** Same retention checks on every rebuilt adapter.
- **Risk / likely tie:** 40 domains may be too few to train a hypernetwork; reuse T2L's released checkpoint and fine-tune.

### HM04 · Contracts made of distilled examples, rebuilt by a short training run
- **Improvement** (a different regenerator: training, not handwriting).
- **Mechanism:** Replace claims with 20–50 synthesized examples optimized so that 100 LoRA steps on them reproduce the adapter (dataset distillation for adapters). Rebuild on any base by training.
- **Nearest prior / gap:** Dataset distillation; [Heirloom](https://arxiv.org/abs/2611.00650) distills on stored unlabelled inputs.
- **Cheapest first test:** F2, 1 upgrade. **Kill** if distilled examples do not beat the same number of random training examples at equal bytes.
- **Old-task retention:** Retrained adapter's benchmarks.
- **Risk / likely tie:** Distilled examples may overfit to the source base.

### HM05 · Regeneration stability
- **Primitive-candidate** (new property: a contract pins behaviour only if two rebuilds agree).
- **Mechanism:** Rebuild each contract 5 times (different writer seeds and trajectories) and measure pairwise behavioural KL on held-out inputs. Add tests where rebuilds disagree until the pairwise KL is below ε. A contract counts as complete when its rebuilds agree with one another, not only when one rebuild matches the original.
- **Nearest prior / gap:** Reproducibility of fine-tuning runs; nobody uses rebuild disagreement to find missing tests.
- **Cheapest first test:** F2, 5 rebuilds. **Kill** if disagreement-driven tests do not reduce distortion to the original more than the same number of random tests.
- **Old-task retention:** Disagreement on neighbour inputs counts.
- **Risk / likely tie:** Random tests may do as well when the domain is narrow.

### HM06 · Choose tests where candidate rebuilds disagree
- **Improvement** (active contract minimization).
- **Mechanism:** Generate candidate inputs, keep those on which the current set of rebuilds disagree most (query-by-committee), and label them with the original adapter's behaviour. Compare with greedy pruning (HC02).
- **Nearest prior / gap:** Active learning; HM05.
- **Cheapest first test:** F2. **Kill** if active selection does not reach HC02's distortion with ≤ 60% of its bytes.
- **Old-task retention:** As HM05.
- **Risk / likely tie:** Merge with HM05 if they coincide.

### HM07 · Share tests across a fleet of contracts
- **Improvement.**
- **Mechanism:** Many domain contracts carry the same tests (format, refusal, arithmetic neighbours). Store shared tests once and reference them from each contract, which reduces total fleet bytes.
- **Nearest prior / gap:** Deduplication; HC18's shared counters.
- **Cheapest first test:** 20 simulated domains. **Kill** if sharing saves < 25% of fleet bytes.
- **Old-task retention:** Shared neighbour tests are retention tests for every adapter that cites them.
- **Risk / likely tie:** Low-risk saving; tooling unless it changes HM02's curve.

### HM08 · Rebuild only the failing components on a base upgrade
- **Improvement** (deepens HC10 with HC07).
- **Mechanism:** On an upgrade, first port numerically, run the contract, and rebuild only components whose tests fail. Total upgrade cost = port + checks + partial rebuild. Compare lazy (on first request) and eager scheduling.
- **Nearest prior / gap:** ReLoRA re-adapts all adapters.
- **Cheapest first test:** S1, 6 domains, 3 upgrades. **Kill** if partial rebuild is not ≥ 2× cheaper than full rebuild at equal accuracy, or ReLoRA is cheaper still.
- **Old-task retention:** Full contract before serving.
- **Risk / likely tie:** Partial ports may hide interactions between ported and rebuilt components; run the full contract.

### HM09 · Where contracts stop being smaller than data
- **Improvement / assay** (maps the boundary of line a).
- **Mechanism:** For adapter types from format rules to fact sets with 1,000 facts, compare minimal contract bytes with raw training data bytes. For fact-heavy adapters the contract converges to the dataset, and line (a) should be scoped to skill and format adapters.
- **Nearest prior / gap:** None needed; this is a measurement.
- **Cheapest first test:** 5 adapter types. **Kill** line (a) for a type if the contract is > 50% of the data bytes.
- **Old-task retention:** Not applicable; per-type retention logged.
- **Risk / likely tie:** The boundary may sit close to format-only adapters, which would shrink the claim.

### HM10 · Contracts that grow from rebuild failures across upgrades
- **Primitive-candidate** (the ledger, applied to line a).
- **Mechanism:** When a rebuilt adapter on a new base fails a held-out check, the failing case becomes a new test in the contract. Measure tests added per upgrade over 3 upgrades. If the count falls, the contract is converging to a base-independent spec.
- **Nearest prior / gap:** HC25 counted growth across revisions on one base.
- **Cheapest first test:** S1. **Kill** if tests added per upgrade do not fall from upgrade 1 to upgrade 3.
- **Old-task retention:** All tests are checked on every base.
- **Risk / likely tie:** Each base may fail in new ways; three upgrades is a small sample.

### HM11 · What a contract leaks compared with an adapter or stored inputs
- **Improvement** (a deployment property for per-user adapters).
- **Mechanism:** Run membership inference against private training examples for: the trained adapter, the stored unlabelled inputs (Heirloom), and the contract. Contracts contain chosen tests rather than user data, so they may leak less.
- **Nearest prior / gap:** [Heirloom](https://arxiv.org/abs/2611.00650) keeps unlabelled inputs on device.
- **Cheapest first test:** One personalization domain with planted canaries. **Kill** if the contract leaks canaries at the same rate as the adapter.
- **Old-task retention:** Not applicable; utility measured at equal accuracy.
- **Risk / likely tie:** Writers may copy training examples into tests; forbid it and check.

### HM12 · One contract, several formats: LoRA, steering vector or prompt
- **Primitive-candidate** (new object: a format-agnostic behaviour spec compiled to the cheapest format that passes it on each base).
- **Mechanism:** Some contracts pass as a system prompt on a strong base, as a steering vector on a mid base, and need a LoRA on a weak one. The compiler tries formats from cheapest to most expensive and serves the first that passes. Weight-compressed adapters cannot change format.
- **Nearest prior / gap:** [WSP writes ICL](https://arxiv.org/abs/2611.26841) shows weights can carry ICL; prompt-to-LoRA distillation goes one way.
- **Cheapest first test:** 6 F2 contracts × 3 bases × 3 formats. **Kill** if one format passes everywhere (no choice to make), or if format choice gives < 20% serving-cost saving at equal pass rate.
- **Old-task retention:** Each format's 3-benchmark retention; prompts cost context, not retention.
- **Risk / likely tie:** LoRA may pass everywhere and be cheap enough on multi-LoRA servers.

## B · Repairs that persist across retrains (line b)

### HM13 · Repair-grown KL constraints across retrains
- **Primitive-candidate** (the main test of line b, deepening HC19).
- **Mechanism:** After each retrain in S1/S2, failing neighbour tests are repaired (a counter or a retrain) and added to a ledger. Every later retrain adds KL-to-reference on all ledger inputs. Measure counter bytes, neighbour failures per retrain, and target gain over 6 retrains.
- **Nearest prior / gap:** KLOD with a fixed neighbour set; replay; one-shot repair. None grows its constraint set from failures it has already repaired.
- **Cheapest first test:** S2 (6 retrains). **Kill** if the ledger does not cut neighbour failures per retrain by ≥ 50% by retrain 6 against KLOD on a fixed neighbour set of the same final size, or if replay of the ledger inputs matches.
- **Old-task retention:** Ledger tests, held-out neighbours (never in the ledger), and benchmarks.
- **Risk / likely tie:** Replay of the same inputs is the likely tie; the difference must come from KL targets versus labels.

### HM14 · Do repair-derived probes shrink probe mismatch?
- **Primitive-candidate / assay** (tests the mechanism behind HM13).
- **Mechanism:** [Why Constrained Updates Still Forget](https://arxiv.org/abs/2610.30191) splits old-loss change under constraints into controlled-direction, gradient-staleness, probe-mismatch and finite-step terms. Compute this decomposition for KL constraints on (i) repair-derived probes, (ii) random old-domain probes, (iii) Self-Preservation's chosen probes, all at equal count. Prediction: (i) has the smallest probe-mismatch term on held-out neighbours.
- **Nearest prior / gap:** That paper's matched QLoRA interventions.
- **Cheapest first test:** S2, 2 retrains. **Kill** if the probe-mismatch term for (i) is not lower than for (ii) by > 2 SE.
- **Old-task retention:** Held-out neighbours.
- **Risk / likely tie:** The decomposition may need their code; reimplementing it is the cost.

### HM15 · Refresh the constraint targets or keep them fixed
- **Improvement.**
- **Mechanism:** Ledger KL targets can be the base model's outputs, the outputs of the last accepted adapter, or the expected behaviour as a label. The functional-path paper derives a conditional refresh budget; test which target choice keeps neighbours without freezing improvements.
- **Nearest prior / gap:** [2610.30191](https://arxiv.org/abs/2610.30191) refresh budget; KLOD uses base outputs.
- **Cheapest first test:** S2. **Kill** if no choice beats base-output targets by > 2 SE on neighbours at equal target gain.
- **Old-task retention:** Neighbours and benchmarks.
- **Risk / likely tie:** Base outputs may be the best choice; then this is a setting, not a card.

### HM16 · Repair ledger versus regression-free update methods on all old-correct data
- **Improvement / control card.**
- **Mechanism:** Positive-congruent training, the NLP regression-free constrained update, margin-preserving training and low-rank Fisher regularisation protect every old-correct sample or a sensitive subspace. The ledger protects only the cases that actually broke. At equal compute, compare negative-flip rate on held-out neighbours and target gain.
- **Nearest prior / gap:** [PCT](https://arxiv.org/abs/2011.09161), [2105.03048](https://arxiv.org/abs/2105.03048), [2511.08322](https://arxiv.org/abs/2511.08322), [2611.20288](https://arxiv.org/abs/2611.20288).
- **Cheapest first test:** S2. **Kill** line (b)'s efficiency claim if PCT on all old-correct samples matches the ledger at ≤ 2× its compute.
- **Old-task retention:** Negative-flip rate is the measure.
- **Risk / likely tie:** PCT is strong; the ledger has to win on compute and on bytes stored.

### HM17 · Repeat offenders: does repair history predict the next regression?
- **Improvement / assay** (cheapest card in the node).
- **Mechanism:** [No universal signal predicts sample-level LLM regression](https://arxiv.org/abs/2608.13607) finds that no inference-time signal predicts which samples regress after an update. Test a history signal instead: inputs repaired before are more likely to regress at the next retrain. If true, the ledger is a regression predictor as well as a constraint set.
- **Nearest prior / gap:** That paper's single-model and cross-version signals.
- **Cheapest first test:** S2 with no constraints, 6 retrains; log regression per input. **Kill** if regression rate among previously repaired inputs is not ≥ 2× the base rate.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** Regressions may be random across retrains; that would also undercut HM13.

### HM18 · Prune constraints that never bind
- **Improvement** (keeps the ledger small).
- **Mechanism:** Track, per ledger entry, whether its KL term was active (above threshold) during each retrain. Drop entries inactive for k rounds into a cold set that is only tested, not trained against; re-activate them if they fail.
- **Nearest prior / gap:** [SkillEvoReg](https://arxiv.org/abs/2609.30861) controls structural growth of text skills.
- **Cheapest first test:** S2 extended to 10 retrains. **Kill** if pruning to ≤ 50% of entries raises held-out neighbour failures by > 1 pp.
- **Old-task retention:** Cold-set tests every round.
- **Risk / likely tie:** Entries may be inactive only because they are constrained; test with ablation.

### HM19 · Constraint or counter: what to do when a constraint blocks the target
- **Improvement.**
- **Mechanism:** Some neighbour constraints conflict with the target (shared features). When adding a ledger entry costs > x pp of target, keep it as a counter-component (HC14/HC16) instead of a training constraint. The policy is chosen per entry.
- **Nearest prior / gap:** HC15 (retract or counter); this is the third option.
- **Cheapest first test:** S2, where distance and reference-frame features overlap. **Kill** if the mixed policy does not beat all-constraint and all-counter on (target, neighbour) jointly.
- **Old-task retention:** Neighbours and benchmarks.
- **Risk / likely tie:** One option may dominate on this fixture.

### HM20 · Constraints that survive a base upgrade
- **Primitive-candidate** (joins lines a and b).
- **Mechanism:** KL targets are outputs of one base and do not carry to a new base. Store each ledger entry as (input, expected behaviour label or tolerance band) rather than logits, so the ledger constrains retraining on any base. After an upgrade, retrain on the new base with the label-based ledger; compare with retraining plus fresh neighbour discovery.
- **Nearest prior / gap:** HC12 ported counters; [ReLoRA](https://arxiv.org/abs/2606.02606) and Heirloom carry adapters, not repair history.
- **Cheapest first test:** S1, 1 upgrade. **Kill** if the carried ledger does not cut neighbour failures in the first retrain on the new base by ≥ 50% against no carried ledger.
- **Old-task retention:** New base's neighbours and benchmarks.
- **Risk / likely tie:** The new base may break different neighbours; that is what the test measures.

### HM21 · Repair-derived targets versus self-chosen preservation targets
- **Improvement / control card.**
- **Mechanism:** [Self-Preservation](https://arxiv.org/abs/2610.12602) has a frozen model choose preservation targets from task banks before training. The ledger chooses them after observing failures. Compare broad retention at equal target count, and test the hybrid: seed with self-chosen targets, grow with repairs.
- **Nearest prior / gap:** That paper; [self-addressed replay](https://www.alphaxiv.org/abs/2611.self-addressed-replay-language-model-facts).
- **Cheapest first test:** S1, 6 retrains. **Kill** if self-chosen targets match the ledger on held-out neighbours at equal count.
- **Old-task retention:** Broad benchmarks beyond the neighbours, since Self-Preservation targets breadth.
- **Risk / likely tie:** The two may be complementary; then the hybrid is the card.

### HM22 · Fleet-level constraints for co-loaded adapters
- **Primitive-candidate** (non-regression across a fleet, not one adapter).
- **Mechanism:** When adapter X is retrained, it also trains against the ledger entries of the adapters it is often co-loaded with, measured under co-loading. Retraining one adapter then cannot break another's behaviour in a multi-LoRA deployment.
- **Nearest prior / gap:** HC22 detects contract conflicts; O-LoRA separates subspaces in sequential training.
- **Cheapest first test:** 6 F2 adapters, co-load pairs, 3 retrains of one adapter. **Kill** if fleet constraints do not cut co-loaded regressions by ≥ 50% against single-adapter ledgers.
- **Old-task retention:** Every co-loaded pair's ledger.
- **Risk / likely tie:** Orthogonal training may give the same protection more cheaply.

### HM23 · Expire constraints when the right behaviour changes
- **Primitive-candidate** (keeps a persistent ledger from freezing stale behaviour).
- **Mechanism:** Some neighbours should change: a policy updates, a fact changes. Each ledger entry carries its provenance (which repair, which authority). An authorized update can mark entries as superseded, and the next retrain treats them as targets for change. Unauthorized drift is still blocked.
- **Nearest prior / gap:** [Risks of LLM-generated regression tests](https://arxiv.org/abs/2610.11835): tests can encode current bugs. Permission and authority cards in PR #344.
- **Cheapest first test:** S1 with 3 planted legitimate changes and 3 planted harmful drifts. **Kill** if the ledger does not block ≥ 90% of harmful drifts while allowing ≥ 90% of authorized changes.
- **Old-task retention:** Non-superseded entries.
- **Risk / likely tie:** Needs an authority signal; take it from the fixture, don't infer it.

## C · Keep the comparison honest

### HM24 · Equal-bytes harness
- **Improvement / assay.**
- **Mechanism:** One harness counts bytes for every arm: contract text, tests, seeds, quantized latents, stored inputs, ledger entries, counters. Every curve in A and every ledger in B is plotted against bytes.
- **Nearest prior / gap:** Required by the reviewer's "stored weights at equal bytes".
- **Cheapest first test:** Built with HM01. Fail any result that lacks a byte count.
- **Old-task retention:** Same checks for every arm.
- **Risk / likely tie:** None.

### HM25 · Keep repair tests and evaluation neighbours apart
- **Improvement / assay.**
- **Mechanism:** Ledger entries come from repairs on discovered failures. Evaluation must use held-out neighbours drawn from the same distributions but never seen by any repair or regenerator. Otherwise line (b)'s gains are memorization.
- **Nearest prior / gap:** HC26 in the parent.
- **Cheapest first test:** Split every neighbour pool 50/50 before S1/S2 begin. **Kill** a reported number if its held-out gap is > 2× the in-ledger gap.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** None; required.

### HM26 · Two-year cost simulation
- **Improvement / assay** (the deployment question for both lines).
- **Mechanism:** Simulate 50 domains, quarterly base upgrades and monthly retrains over 2 years. Cost each policy: store weights + port, store contracts + rebuild, store data + retrain, with and without the ledger. Count compute, writer tokens, bytes, and regressions that reached serving.
- **Nearest prior / gap:** HC28 and HL32 in the parents.
- **Cheapest first test:** Use measured unit costs from HM02, HM08 and HM13. **Kill** both lines' deployment pitch if store-data + retrain + PCT is cheapest at equal served regressions.
- **Old-task retention:** Served regressions are the retention metric.
- **Risk / likely tie:** Storing data is often allowed and cheap; the contract case is strongest where data cannot be kept (HM11).

## Ranked deeper questions

1. **After a base upgrade, does a contract beat weights compressed to the same bytes and then ported (HM01, HM02, HM24)?** This one result decides line (a). On the same base, compressed weights should win; the contract has to win across bases. First run: HM02 on Qwen2.5-0.5B → Qwen3.5-0.8B with NOLA + LoRA-X, ReLoRA and Text-to-LoRA as controls.
2. **Is repair history the regression signal that inference-time signals are not (HM17, HM14)?** HM17 is cheap and gates line (b): if repaired inputs do not regress more often, a repair-grown ledger has no advantage over a random neighbour set.
3. **Does a repair-grown ledger beat KLOD, replay and PCT at equal compute and bytes, and does it carry across a base upgrade (HM13, HM16, HM20)?** That would make the ledger a continual-learning primitive: behaviour that has broken once stays protected through every retrain and base change, at a size that grows with failures rather than with data.
4. **Can one behaviour spec compile to the cheapest format per base (HM12, HM09)?** If yes, the stored object for a domain becomes a format-free spec, which weight compression cannot offer. If it fails, line (a) narrows to LoRA-only rebuilds of skill and format adapters.
