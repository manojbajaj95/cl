# Handwritten LoRA 5: One Shim for the Whole Fleet

Child of [Handwritten LoRA 4: Move the Behaviour, Keep the Ledger](handwritten-lora-4.md) ([PR #405](https://github.com/manojbajaj95/cl/pull/405), depth 4) · 25 candidate cards (HS01–HS25) · 4 ranked deeper questions · Ideas only; no experiments run

**Parent verdict.** The review of #405 gave no card a 4.
- **New at 3:** bend the base upgrade toward the adapter fleet. One compatibility shim, or a vendor-side compatibility loss, trained on the union of fleet ledgers, so that every adapter loads after a fixed transform; the pooled fragility map then feeds the next base (HT07, HT08, HT18). Controls: MUSCLE, LoRA-X/Trans-LoRA, ReLoRA, UpgradeBench policies, and a random-input shim.
- **Still at 3:** the ledger and the format-free spec.
- **Rated improvements:** rebuild disagreement and tier migration.

This level develops only the fleet-shim line.

**Thesis.** Every porting method in this branch, and in the literature, moves N adapters to the new base: N ports per upgrade. The fleet shim reverses that. It is one small base-side module S on base v2 such that, for every adapter Aᵢ trained on v1, v2 + S + T(Aᵢ) passes Aᵢ's ledger, where T is a fixed cheap transform (identity for same-shape releases, LoRA-X projection otherwise). The cost becomes one shim per upgrade.

The closest prior work does part of this:
- [MUSCLE](https://arxiv.org/abs/2407.09435) trains a *per-task* compatibility adapter that cuts negative flips by up to 40% from Llama 1 to Llama 2.
- [MKP-Adapter](https://arxiv.org/abs/2609.16875) does adapter-only backward compatibility for *embeddings*.
- The [Universal Activation Bus](https://arxiv.org/abs/2608.09521) gives each model one encoder–decoder pair to a shared space so that *read-only* tools (probes, SAEs) transfer.
- [Stitching for perception updates](https://arxiv.org/abs/2606.21509) keeps a *fixed downstream policy* working after its perception model changes.

None gives one shim that keeps a fleet of LoRA adapters, which both read and write the residual stream, valid across an LLM base upgrade.

The questions that make it a primitive or kill it:
1. How does the shim's size scale with fleet size N?
2. Can the vendor fit it without seeing the adapters?
3. Can the upgrade be certified to change behaviour only inside a declared envelope?
4. Does one shim also keep the rest of the fleet's tools valid (probes, steering vectors)?

## Shared protocol

- **Releases.** **R-toy:** v1 = Qwen2.5-0.5B; v2 = v1 continue-trained on 200M new-domain tokens plus an instruction-tuning pass, so the shape is the same and the change is known. **R-real:** consecutive Qwen releases from [UpgradeBench](https://arxiv.org/abs/2608.20918), plus Llama 1 → Llama 2 to compare directly with MUSCLE's numbers.
- **Fleets.** **N-small:** the 6 F2 adapters (level 2). **N-large:** 100 rank-8 LoRAs trained on Super-NaturalInstructions tasks on v1, each with a 50-entry ledger built as in level 3 (target tests + repaired neighbours), split 70 seen / 30 unseen by the shim.
- **Controls, on every card where they apply:** [MUSCLE](https://arxiv.org/abs/2407.09435) per-task compatibility adapters; per-adapter [LoRA-X](https://arxiv.org/abs/2501.16559), [Trans-LoRA](https://arxiv.org/abs/2405.17258) and [ReLoRA](https://arxiv.org/abs/2606.02606); [UpgradeBench](https://arxiv.org/abs/2608.20918)'s retain / port / refresh / retrain policies; and a **random-input shim** of the same architecture and compute, fit on generic text instead of ledger inputs. Report results on the 30 unseen adapters separately.
- **Metrics.** Per adapter: ledger pass rate and target accuracy on v2 + S + T(Aᵢ), and negative-flip rate against Aᵢ on v1. Fleet: mean and worst decile over adapters. **Base cost:** v2's own benchmarks with S loaded and no adapter, and S's leakage outside the fleet's inputs (HS10, HS17). **Compute:** shim training versus the sum of N per-adapter ports.
- **Retention.** For every card: (i) every adapter's ledger on v2, (ii) v2's general benchmarks with the shim loaded, so the shim must not erase the upgrade's gains, and (iii) v1-era held-out neighbours never in any ledger.

## Literature check

alphaXiv discovery on compatible LLM updates, backward-compatible training, model stitching, and cross-model activation interfaces; abstracts checked on arXiv. Abstract-level screen.

| Nearest prior | What it already does | Boundary for this node |
|---|---|---|
| [MUSCLE](https://arxiv.org/abs/2407.09435) | Shows that fine-tuned task adapters suffer negative flips when the base updates, and trains a compatibility adapter that cuts them by up to 40% (Llama 1 → 2). | Per task, and trained alongside each task's new adapter. The shim is *one* module for N old adapters, which are loaded unchanged after T. MUSCLE is the main control. |
| [BCT](https://arxiv.org/abs/2003.11942), [MKP-Adapter](https://arxiv.org/abs/2609.16875), [backward-compatible retrieval](https://arxiv.org/abs/2610.29550) | Keep new embedding models compatible with old galleries; MKP does it with an adapter only, without touching the backbone. | Embeddings are read-only outputs. LoRA adapters both read and write mid-network, so a shim must fix both sides (HS01). |
| [Universal Activation Bus](https://arxiv.org/abs/2608.09521), [MATCHA](https://arxiv.org/abs/2610.09058), [Interpretability Is Not Model-Specific](https://arxiv.org/abs/2611.12675) | One linear encoder–decoder pair per model into a shared space lets probes, SAEs and steering vectors transfer; residual-stream maps transfer refusal directions. | These carry read-only tools, or single directions, between models. The shim must carry *weight updates* whose effects compound across layers. |
| [Model stitching](https://arxiv.org/abs/2106.07682), [stitching foundation models](https://arxiv.org/abs/2603.12433), [stitching for perception updates](https://arxiv.org/abs/2606.21509) | Light stitch layers connect models or keep a fixed downstream policy compatible after its upstream model updates. | The closest analogue is the driving paper: fixed consumers, updated producer. In an LLM the consumers (adapters) are spread through the producer's own layers. |
| [Declared change envelopes](https://arxiv.org/abs/2611.04192), [Test Before You Deploy](https://arxiv.org/abs/2604.27789), [activation-monitor staleness](https://arxiv.org/abs/2606.15980) | Certify that an update changed decisions only inside a declared region, using anytime-valid tests on unlabelled traffic; deployer-side production contracts; probes going stale after fine-tuning. | They certify or test an update, and the shim is a way to *make* it compatible. Joining them gives an upgrade that is both shimmed and certified (HS10). Stale monitors are a second fleet the shim could serve (HS15). |
| [Trans-LoRA](https://arxiv.org/abs/2405.17258), [LoRA-X](https://arxiv.org/abs/2501.16559), [ReLoRA](https://arxiv.org/abs/2606.02606), [Heirloom](https://arxiv.org/abs/2611.00650), [UpgradeBench](https://arxiv.org/abs/2608.20918) | Per-adapter migration policies and benchmarks. | Controls at N ports per upgrade. |

## A · What the shim is

### HS01 · A two-sided shim around each adapter site
- **Primitive** (new object).
- **Mechanism:** At each module an adapter can target, S has a read map Rₗ (v2 input → v1-like input, applied only on the adapter's branch) and a write map Wₗ (the adapter's v1-coordinate output → v2 residual coordinates). Then v2 + S + Aᵢ computes h_v2 + Wₗ·Aᵢ(Rₗ·x). The base path is untouched, so v2's own behaviour is unchanged when no adapter is loaded. Fit Rₗ, Wₗ (low-rank + identity) on the union of fleet-ledger inputs, with each adapter's ledger behaviour as the target.
- **Nearest prior / gap:** The [Universal Activation Bus](https://arxiv.org/abs/2608.09521) uses encoder–decoder pairs for read-only tools; MUSCLE adds a per-task compatibility adapter on the base path.
- **Cheapest first test:** R-toy, N-small. **Kill** if the shim does not reach ≥ 90% of per-adapter ReLoRA accuracy on ≥ 5/6 adapters at ≤ 1/3 of the total compute of 6 ReLoRA runs.
- **Old-task retention:** v2's benchmarks with S loaded and no adapter must equal v2's (by construction; verify). Each adapter's ledger on v2.
- **Risk / likely tie:** Adapter effects compound through later layers, so per-site maps may not be enough. HS02 adds a base-path option.

### HS02 · An adapter-branch-only shim versus a base-path shim
- **Improvement** (design choice with a clear test).
- **Mechanism:** Compare (i) HS01, which touches only the adapter branch, with (ii) a base-path shim (a LoRA on v2, as in MUSCLE) and (iii) both. A base-path shim can repair compounding effects but changes v2 for all traffic.
- **Nearest prior / gap:** MUSCLE is (ii) per task.
- **Cheapest first test:** R-toy, N-small. **Kill** (ii)/(iii) if they do not beat (i) by ≥ 3 pp on fleet ledger pass, or if they cost > 1 pp on v2's benchmarks.
- **Old-task retention:** v2's benchmarks for (ii)/(iii).
- **Risk / likely tie:** (iii) may be necessary; then load the base-path part only when a fleet adapter is loaded.

### HS03 · How the shim's size scales with fleet size
- **Primitive-candidate** (the defining quantity: is one shim really cheaper than N ports as N grows?).
- **Mechanism:** For N = 6, 25, 50 and 100 (N-large), find the smallest shim rank that reaches a fixed fleet pass rate. If the required rank saturates (one v1→v2 correction serves every adapter), the shim is a fleet-level object. If it grows linearly, it is N ports in disguise.
- **Nearest prior / gap:** None measures compatibility cost against the number of consumers.
- **Cheapest first test:** R-toy, N-large. **Kill** if required shim rank grows ≥ 0.5× linearly in N.
- **Old-task retention:** Unseen-adapter (30) ledger pass at each N.
- **Risk / likely tie:** Adapters targeting different modules need different sites. Count sites as well as rank.

### HS04 · Ledger-input shim versus random-input shim
- **Improvement / control card** (the reviewer's random-input control as its own test).
- **Mechanism:** Fit the same shim on (i) union-of-ledger inputs, (ii) generic text at equal token count, (iii) ledger inputs plus generic text. If (ii) matches (i), the ledger adds nothing and the shim is just a v1→v2 activation stitch.
- **Nearest prior / gap:** Activation-alignment maps fit on generic prompts ([2611.12675](https://arxiv.org/abs/2611.12675) found that region-matched prompts raise transfer from 54% to 102%).
- **Cheapest first test:** R-toy, N-large. **Kill** the ledger's role if (i) − (ii) < 2 pp on unseen-adapter ledger pass.
- **Old-task retention:** As HS01.
- **Risk / likely tie:** A plain stitch may be enough for same-family releases. The ledger may matter only on R-real.

### HS05 · A shim fit without seeing any adapter
- **Primitive-candidate** (vendor-side compatibility with private adapters).
- **Mechanism:** The vendor never sees users' adapters. Users send only ledger inputs (or hashed activation statistics at adapter sites on v1). The vendor fits S to match v1's site activations and their downstream sensitivity (Jacobian sketches) on those inputs, with no adapter involved, and ships it with v2.
- **Nearest prior / gap:** HS06 is the same with no user inputs at all; MKP-Adapter has no private-fleet setting.
- **Cheapest first test:** R-toy, N-large. **Kill** if the adapter-blind shim gets < 80% of the adapter-aware shim's fleet pass rate.
- **Old-task retention:** As HS01.
- **Risk / likely tie:** Writes depend on adapter weights; without them the write map Wₗ may be guesswork. Sketches of v1's downstream Jacobian may suffice.

### HS06 · A fleet-blind shim from v1 and v2 alone
- **Improvement / lower bound.**
- **Mechanism:** Fit S only on v1 versus v2 site activations on generic text. This is what a vendor can ship with no fleet information at all, and it lower-bounds HS05 and HS01.
- **Nearest prior / gap:** Model stitching.
- **Cheapest first test:** R-toy and R-real, N-large. **Kill** none: it is a baseline row. Report the gap to HS05.
- **Old-task retention:** As HS01.
- **Risk / likely tie:** May be all one needs for minor releases; then the claim is restricted to major ones.

## B · Vendor-side compatibility loss

### HS07 · A fleet compatibility loss during the vendor's last training phase
- **Primitive-candidate** (deepens HT07).
- **Mechanism:** In v2's final phase (for R-toy, the instruction pass), add the loss Σᵢ KL(v1 + Aᵢ ‖ v2 + T(Aᵢ)) on the ledger inputs for a sample of fleet adapters (or their HS05 sketches). v2 itself is then compatible and no shim is needed.
- **Nearest prior / gap:** MUSCLE trains a compatibility adapter afterwards; [BCT](https://arxiv.org/abs/2003.11942) adds an influence loss during embedding training.
- **Cheapest first test:** R-toy, N-large (70 in the loss, 30 unseen). **Kill** if unseen-adapter negative flips do not fall ≥ 40% (MUSCLE's best reported reduction) at ≤ 1 pp cost on v2's benchmarks.
- **Old-task retention:** v2's benchmarks are the cost.
- **Risk / likely tie:** The loss may freeze v2 near v1 and erase the upgrade. HS09 maps that trade-off.

### HS08 · The pooled fragility map as a loss for the next base
- **Primitive-candidate** (deepens HT18: the fleet's repair history trains the next base).
- **Mechanism:** Pool ledger entries that regressed under the most fleet retrains into a fragility set, then cluster it. In v2's training, add a small loss that reduces the sensitivity of v2's outputs on those clusters to rank-8 perturbations at the adapter sites (random LoRA noise). The next fleet's fine-tunes should then break those behaviours less.
- **Nearest prior / gap:** [Edit-Ready Training](https://arxiv.org/abs/2611.26408) rehearses edits for vision models; sharpness-aware training is generic.
- **Cheapest first test:** R-toy, retrain 30 SNI adapters on v2 and v2-fragility. **Kill** if fragility-set regressions after retraining do not fall ≥ 30% against v2, or a random fragility set of equal size does as well.
- **Old-task retention:** v2's benchmarks and the fleet's new target accuracy (lower plasticity is a cost).
- **Risk / likely tie:** Lower sensitivity may also block wanted adaptation.

### HS09 · The trade-off between compatibility and upgrade gains
- **Improvement / assay.**
- **Mechanism:** Sweep the compatibility-loss weight (HS07) and the shim's capacity (HS01). Plot v2's own benchmark gain over v1 against fleet negative-flip rate. A vendor picks a point on this frontier; MUSCLE and UpgradeBench policies are single points on it.
- **Nearest prior / gap:** Regression-free update papers report single operating points.
- **Cheapest first test:** R-toy, 5 weights. **Kill** HS07 if its frontier is dominated by v2 + HS01 shim at every point.
- **Old-task retention:** Both axes are retention measures.
- **Risk / likely tie:** None; it is a map.

### HS10 · Shimmed upgrades with a declared change envelope
- **Primitive-candidate** (new operation: an upgrade that is both compatible for the fleet and certified to change only where declared).
- **Mechanism:** The vendor declares an envelope of inputs where v2 is meant to differ (new knowledge, fixed bugs). The shim is trained to keep fleet behaviour outside the envelope and to let v2's changes through inside it. Leakage outside the envelope is certified with the anytime-valid tests of [Declared change envelopes](https://arxiv.org/abs/2611.04192), over unlabelled fleet traffic with adapters loaded.
- **Nearest prior / gap:** That paper certifies an update; it does not make the fleet compatible. HT09 negotiates per entry without certification.
- **Cheapest first test:** R-toy with a planted envelope (one new domain). **Kill** if certified leakage outside the envelope with the shim is not ≥ 3× lower than without it, at equal in-envelope gain.
- **Old-task retention:** Leakage outside the envelope is the retention certificate.
- **Risk / likely tie:** Envelopes are hard to state for broad releases; start with narrow ones.

## C · Chains, co-existence and other tools

### HS11 · Chaining shims across releases
- **Improvement.**
- **Mechanism:** For v1 → v2 → v3, either compose S₁₂ ∘ S₂₃, refit a direct S₁₃, or port adapters at v3 and retire both shims. Measure drift and the inference cost of stacked shims.
- **Nearest prior / gap:** UpgradeBench's longitudinal sequence; HC11 measured chained drift for contracts.
- **Cheapest first test:** R-real, 3 consecutive Qwen releases, N-small. **Kill** composed shims if they lose > 5 pp against a direct refit.
- **Old-task retention:** Fleet ledgers at v3.
- **Risk / likely tie:** Refit is cheap and likely wins; composition only matters when v2 activations are no longer available.

### HS12 · When to retire the shim and port natively
- **Improvement.**
- **Mechanism:** A shim costs inference on every request with a fleet adapter and holds the fleet in v1 coordinates. Port an adapter natively when its traffic × shim overhead exceeds one port, or when its ledger fails under the shim.
- **Nearest prior / gap:** UpgradeBench decisions per specialist.
- **Cheapest first test:** Simulated Zipf traffic on N-large. **Kill** if the rule does not beat "shim all" and "port all" on total cost at equal fleet pass.
- **Old-task retention:** Ledger pass of ported adapters.
- **Risk / likely tie:** Low risk; this is scheduling.

### HS13 · Old adapters through the shim, new adapters native, in one fleet
- **Improvement** (a real deployment state).
- **Mechanism:** After the upgrade, new adapters are trained natively on v2 while old ones run through S. Co-loading one of each mixes coordinate systems. Test co-load ledgers, and whether new adapters should be trained on v2 + S (shared coordinates) instead.
- **Nearest prior / gap:** HM22 fleet constraints at one base.
- **Cheapest first test:** N-small old + 3 new adapters, all mixed pairs. **Kill** if mixed co-loads fail > 2× more ledger entries than same-system co-loads and training on v2 + S does not fix it.
- **Old-task retention:** All co-load ledgers.
- **Risk / likely tie:** Co-loading may be rare enough to ignore.

### HS14 · Co-loading several old adapters through one shim
- **Improvement.**
- **Mechanism:** S is fit per adapter on ledger behaviour; co-loading two old adapters through S may not reproduce their v1 co-load behaviour. Add co-load pairs from traffic to S's training.
- **Nearest prior / gap:** HC22, HM22.
- **Cheapest first test:** N-small, all pairs. **Kill** if pair-aware fitting does not cut co-load ledger failures ≥ 50%.
- **Old-task retention:** Co-load ledgers.
- **Risk / likely tie:** As HS13.

### HS15 · One shim for adapters, probes and steering vectors
- **Primitive-candidate** (the shim as a compatibility layer for every component built on v1, not only LoRAs).
- **Mechanism:** Fleets also hold activation monitors, which [go stale after fine-tuning-style updates](https://arxiv.org/abs/2606.15980), steering vectors and handwritten components. Add their ledgers (probe AUROC on v1-labelled inputs, steering effect) to S's objective. The read map Rₗ serves probes and the write map Wₗ serves steering vectors.
- **Nearest prior / gap:** The [Universal Activation Bus](https://arxiv.org/abs/2608.09521) covers read-only tools via a shared space; that paper benchmarks and repairs stale monitors one at a time.
- **Cheapest first test:** R-toy: 6 adapters + 4 safety probes + 3 steering vectors. **Kill** if one joint shim is worse than separate per-type shims by > 3 pp on any type.
- **Old-task retention:** Each tool's v1 behaviour.
- **Risk / likely tie:** UAB-style per-model pairs may already do the probe part.

## D · Failures and guarantees

### HS16 · Predict which adapters the shim will fail
- **Improvement / assay.**
- **Mechanism:** An adapter fails under S when its read and write subspaces overlap with the parts of v1 → v2 change that S cannot model. Score each adapter by the energy of (v2 − v1 site activations) projected onto its LoRA A and B subspaces, after S. Test the score as a predictor of ledger failure.
- **Nearest prior / gap:** [Backbone-specific LoRA geometry](https://arxiv.org/abs/2611.27201) uses subspace inner products for provenance.
- **Cheapest first test:** N-large. **Kill** if Spearman between score and failure < 0.5.
- **Old-task retention:** Is the target.
- **Risk / likely tie:** Low risk; useful for HS12 scheduling.

### HS17 · Does the shim undo the upgrade on fleet traffic?
- **Improvement / assay.**
- **Mechanism:** With an adapter loaded, the shim pulls behaviour toward v1 coordinates, which may also pull back v2's improvements on that adapter's traffic. Measure v2-over-v1 gains on fleet traffic with shim versus native port.
- **Nearest prior / gap:** HS09 at fleet level; [change envelopes](https://arxiv.org/abs/2611.04192).
- **Cheapest first test:** R-toy, with v2 improvements planted in 3 domains. **Kill** if the shim keeps < 50% of v2's planted gains that a native port keeps.
- **Old-task retention:** Both directions: keep v1 behaviour on ledgers, keep v2 gains elsewhere.
- **Risk / likely tie:** Use HS10's envelope to let gains through.

### HS18 · A poisoned adapter in the union ledger
- **Improvement** (robustness of a shared fit).
- **Mechanism:** The shim is fit on everyone's ledgers, so one malicious adapter's ledger can bend S and harm other adapters or base traffic. Defences: cap the loss weight per adapter, use median-of-means across adapters, and reject ledger entries that pull S far outside the fleet's consensus.
- **Nearest prior / gap:** Robust aggregation in federated learning; [LoRA-Patch](https://arxiv.org/abs/2611.03752) for backdoored adapters.
- **Cheapest first test:** N-large with 3 poisoned adapters. **Kill** if the defended shim's harm to the other adapters is not ≤ 1 pp while undefended harm is ≥ 5 pp.
- **Old-task retention:** Other adapters' ledgers and v2 benchmarks.
- **Risk / likely tie:** Standard defences may suffice; then it is tooling.

### HS19 · Keep wanted vendor changes out of the shim's objective
- **Improvement** (deepens HT09 inside shim training).
- **Mechanism:** Ledger entries on which v2's new behaviour is a verified improvement are excluded from S's KL objective (or reversed). The shim then preserves only regressions.
- **Nearest prior / gap:** HT09.
- **Cheapest first test:** R-toy with 5 planted improvements and 5 planted regressions in fleet ledgers. **Kill** if exclusion does not keep ≥ 4/5 improvements while blocking ≥ 4/5 regressions.
- **Old-task retention:** Blocked regressions.
- **Risk / likely tie:** Labelling improvements needs ground truth; use planted ones.

### HS20 · The cross-family limit
- **Improvement / assay** (scoping).
- **Mechanism:** For v2 in a different family (tokenizer and width change), the shim needs T = LoRA-X or Theseus transport, plus token-embedding maps. Measure how far the shim gets before per-adapter porting is necessary.
- **Nearest prior / gap:** Level 2's cross-family porting cards.
- **Cheapest first test:** Qwen2.5-0.5B → SmolLM2-360M, N-small. **Kill** the cross-family claim if the shim is not ≥ 70% of Trans-LoRA per adapter.
- **Old-task retention:** As HS01.
- **Risk / likely tie:** Likely fails; this scopes the primitive to same-family releases.

## E · Keep it honest

### HS21 · Control harness
- **Improvement / assay.**
- **Mechanism:** Every shim result reports MUSCLE (per task), LoRA-X, Trans-LoRA and ReLoRA (per adapter), UpgradeBench's four policies, and the random-input shim. All get equal fleet information and their compute is logged.
- **Nearest prior / gap:** Reviewer's control list.
- **Cheapest first test:** Built with HS01. Fail any result without it.
- **Old-task retention:** Same for all arms.
- **Risk / likely tie:** None.

### HS22 · Break-even fleet size
- **Improvement / assay.**
- **Mechanism:** Shim compute + inference overhead against N × per-adapter port cost. Report the N at which the shim pays, by release type.
- **Nearest prior / gap:** HT24.
- **Cheapest first test:** From HS03 and HS12 runs. **Kill** the deployment claim if break-even N > 100 on R-real.
- **Old-task retention:** At equal fleet pass.
- **Risk / likely tie:** Cheap ports (LoRA-X) push break-even up.

### HS23 · Real releases, not only the toy
- **Improvement / assay.**
- **Mechanism:** Run HS01, HS04, HS07 and HS10 on UpgradeBench's Qwen sequence and on Llama 1 → 2, and compare with MUSCLE's reported 40% reduction.
- **Nearest prior / gap:** MUSCLE, UpgradeBench.
- **Cheapest first test:** One release pair, N-small. **Kill** R-toy conclusions that do not hold on R-real.
- **Old-task retention:** As HS01.
- **Risk / likely tie:** Real releases change far more than R-toy.

### HS24 · Does the toy release predict real ones?
- **Improvement / assay.**
- **Mechanism:** Tune R-toy (amount of continued training, instruction pass) until its v1 → v2 activation shift statistics match a real Qwen release. Then check whether shim results transfer.
- **Nearest prior / gap:** None.
- **Cheapest first test:** Compare HS01 rankings on R-toy and R-real. **Kill** R-toy as a proxy if method rankings disagree.
- **Old-task retention:** Not applicable.
- **Risk / likely tie:** Low risk.

### HS25 · How the benefit scales with the fleet
- **Improvement / assay.**
- **Mechanism:** Plot unseen-adapter pass rate and per-adapter cost against N (6 → 100). A shim that improves on unseen adapters as N grows is learning the v1 → v2 change, not memorizing adapters.
- **Nearest prior / gap:** HS03 measures size; this measures generalization.
- **Cheapest first test:** N-large splits. **Kill** if unseen-adapter pass does not rise with N.
- **Old-task retention:** Unseen-adapter ledgers.
- **Risk / likely tie:** May saturate early; that is still a result.

## Ranked deeper questions

1. **Does one shim fit on ledger inputs let N old adapters load at ≥ 90% of per-adapter ReLoRA accuracy, with shim size sublinear in N and improving on unseen adapters (HS01, HS03, HS04, HS25)?** This decides whether the shim is a fleet-level primitive or N ports in disguise. First run: HS01 + HS04 on R-toy with N-large, against MUSCLE and the random-input shim.
2. **Can the vendor make v2 compatible without seeing any adapter (HS05, HS06, HS07)?** Private fleets make this the deployable version. The gap between the adapter-blind and adapter-aware shims is the cost of privacy.
3. **Can an upgrade be both shimmed and certified to change behaviour only inside a declared envelope, while keeping v2's gains (HS10, HS17, HS09)?** Joining compatibility with certification ([2611.04192](https://arxiv.org/abs/2611.04192)) turns the shim from a patch into an upgrade protocol.
4. **Does the pooled fragility map make the next base less fragile for the next fleet (HS08)?** If so, the fleet's repair history has become a training signal for the base. That is the continual-learning loop this branch has been looking for, running across model generations rather than inside one model.
