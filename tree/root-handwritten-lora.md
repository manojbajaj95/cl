# Root: LLM-handwritten LoRA weights

Root node (depth 0) · 33 candidate cards (HL01–HL33) · 5 ranked deeper questions · Ideas only; no experiments run

**Request (Manoj).** "Eval task: LLMs hand-write the correct LoRA weights + pick good sizes & layers/modules to improve on a benchmark. It's nice on infra because you can tailor per domain and hot swap with multi-LoRA serving. Train a LoRA → handwrite a LoRA. Is this pursuable?" The sketched pipeline: frozen base W → an LLM writes edited weights W′ → ΔW = W′ − W → top-r SVD ΔW ≈ BA → LoRA adapter (r = 1 for Qwen) → re-run the benchmark → serve base + hot-swapped adapters.

**Thesis.** A gradient-trained LoRA is a number with no reasons. A handwritten LoRA can be a short program: each rank-1 component says what it reads, what it writes and which test it passes. That only matters if the reasons do work after the first write, because writing weights to beat a benchmark is already an active field and the first write mostly loses to training (see below). The cards look for operations that a handwritten adapter supports and a trained one does not: recompiling it onto a new base, repairing a trained adapter's spillover, retracting one component by name, certifying that two hot-swapped adapters cannot interfere, and choosing *where* to write separately from *what* to write.

## Is this pursuable? Short answer

Yes as an eval and as a research line, but not as the claim "handwriting beats training on a benchmark".
- **The core task already exists as weight-space programming (WSP), Nov 2026.** Frontier LLMs edit Qwen-class models' weights without gradients: [Exploring WSP](https://arxiv.org/abs/2611.09382) (Qwen3.5-0.8B/9B; up to +29.45 pp on MATH-500 from 1,023 changed parameters, but 6 of 16 trajectories found no validated edit), [Self-WSP](https://arxiv.org/abs/2611.28833) (random search sometimes matches the LLM), [SelfWrite](https://arxiv.org/abs/2611.29513) (the model writes a program that builds a low-rank edit, gated on a hidden set; 76.30 → 77.75% held-out), [Language models can rewrite their own weights](https://arxiv.org/abs/2611.21885) (27B self-edit, +6.6 pp), [WSP writes ICL](https://arxiv.org/abs/2611.26841) (editors write the ICL task vector into near-silent MLP units; matches LoRA on the same examples). [WeightBench](https://arxiv.org/abs/2611.18553) reports frontier agents "cannot yet patch language models".
- **Training wins the head-to-head.** [Writing weights or training them?](https://arxiv.org/abs/2611.27089) on Qwen3.5-0.8B: the best handwritten patch reached 22.1% (reference-frame) and 33.7% (StepGame); a trained **rank-1 LoRA** reached 100% and 98.8%, but collapsed neighbouring distance tasks from 94% to 0–2%. That spillover is the opening.
- **The pipeline parts are known.** Delta → SVD → LoRA is standard LoRA extraction/compression ([LoRA-Squeeze](https://arxiv.org/abs/2602.10993), [LoRA on a Budget](https://arxiv.org/abs/2610.36386)); hot-swap is [S-LoRA](https://arxiv.org/abs/2311.03285), [Punica](https://arxiv.org/abs/2310.18547), [LoRAForge](https://arxiv.org/abs/2611.01256), [MoLoRA](https://arxiv.org/abs/2603.15965); rank/layer choice is [AutoPEFT](https://arxiv.org/abs/2301.12132), [FIM-LoRA](https://arxiv.org/abs/2605.16800), [LAARA](https://arxiv.org/abs/2607.19391); closed-form rank-1 edits are [ROME](https://arxiv.org/abs/2202.05262), [MEMIT](https://arxiv.org/abs/2210.07229), [AlphaEdit](https://arxiv.org/abs/2410.02355); generated adapters are [Text-to-LoRA](https://arxiv.org/abs/2506.06105) and [Drag-and-Drop LLMs](https://arxiv.org/abs/2506.16406).
- **What is not done (in the abstracts read):** a LoRA-format track with rank and placement as graded decisions; handwritten adapters as *source code* recompiled onto a new base; hand repair of a trained adapter's spillover; interference certificates for hot-swapped handwritten adapters; any continual stream of handwritten adapters with retention measured. Those are the cards below. Recommended first runs: HL01 (the benchmark, with HL29's controls built in) and HL15 (spillover repair on the published 2611.27089 setup).

**Scope.** Read before writing: the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). Different from the LoRA-writing learner root ([PR #344](https://github.com/manojbajaj95/cl/pull/344)): there a trained neural Learner (a hypernetwork) emits factors, and the triage ruled its core writer prior art (T2L/DnD); here a general reasoning LLM with tools writes each adapter case by case, and the card must use something the writer can *say* about the weights. Ledger results this root must respect:
- **WSP CL repair was killed at proposal** (Agent 8, [PR #7](https://github.com/manojbajaj95/cl/pull/7)) on 2611.25613, Self-WSP and 2611.26841: no card here is "an LLM repairs forgetting by editing weights" alone.
- **Edit capacity barely varied** ([PR #22](https://github.com/manojbajaj95/cl/pull/22)): HL23 must first show the number of handwritten edits before collapse varies more than a constant guess explains.
- **Fine-tuning damage is diffuse, not sparse** ([PR #24](https://github.com/manojbajaj95/cl/pull/24)): cards that localize a regression to a few components (HL07, HL15) must check that the damage they repair is concentrated.
- **Placement choice was graded IMPROVEMENT** (MX1, [PR #36](https://github.com/manojbajaj95/cl/pull/36)): the placement cards (HL02, HL24–HL27) are improvements unless they add a new object.
- **Retention in every first test:** each card names its old-task check; the default is the base model's scores on 3 untouched benchmarks (e.g. GSM8K, IFEval, a distance/neighbour task) and perplexity on held-out web text, measured with the adapter loaded.

**Shared conventions.** Base: Qwen2.5-0.5B on CPU for toys, Qwen3.5-0.8B on 1 GPU (the 2611.27089 and 2611.09382 base). Writer: a frontier LLM in a Python sandbox with read access to weights and activations and a forward-pass tool, no gradient tool. Every card reports three controls: a **trained LoRA** at the same rank, modules and examples; **random search** at the same number of evaluations; and a **permuted delta** (the 2611.27089 check). "Bytes" counts adapter parameters plus any text the adapter ships with.

## Literature check

alphaXiv searches: LLMs writing network weights, LoRA extraction and rank allocation, LLM-driven PEFT configuration search, compiled transformers, multi-LoRA serving, steering vectors as weights; abstracts read on arXiv for every paper cited below the line. Abstract-level screen, not full-text priority claims.

| Line | Already available | What a card here must add |
|---|---|---|
| LLM writes weights (WSP) | [Sparks of WSP](https://www.alphaxiv.org/abs/2611.weight-space-programming), [Exploring WSP](https://arxiv.org/abs/2611.09382), [Self-WSP](https://arxiv.org/abs/2611.28833), [SelfWrite](https://arxiv.org/abs/2611.29513), [Rewrite own weights](https://arxiv.org/abs/2611.21885), [WSP writes ICL](https://arxiv.org/abs/2611.26841), [Writing vs training](https://arxiv.org/abs/2611.27089), [Controlled repair](https://arxiv.org/abs/2611.25613), [WeightBench](https://arxiv.org/abs/2611.18553), [WeightCode](https://arxiv.org/abs/2611.25476), [WSP doesn't need transformers](https://arxiv.org/abs/2611.22055), [Interpretable WSP](https://arxiv.org/abs/2611.18114), [Edit-Ready Training](https://arxiv.org/abs/2611.26408) | One-shot gains on a benchmark are shown; the LLM's understanding of its edits is weak (Self-WSP) and gate overfitting is a live risk. A card must use the LoRA format or the writer's stated reasons in a later operation (revise, port, compose, certify). |
| Generated adapters | [Text-to-LoRA](https://arxiv.org/abs/2506.06105), [Drag-and-Drop LLMs](https://arxiv.org/abs/2506.16406), HyperTuning, Doc-to-LoRA (in PR #344) | Amortized zero-shot writers. A per-case reasoning writer must beat them at equal information, or do something they cannot (explain, revise). |
| Closed-form edits | [ROME](https://arxiv.org/abs/2202.05262), [MEMIT](https://arxiv.org/abs/2210.07229), [AlphaEdit](https://arxiv.org/abs/2410.02355) (null-space projection), [Tracr](https://arxiv.org/abs/2301.05062), [Tracr-Injection](https://arxiv.org/abs/2505.10719) | Rank-1 fact edits and compiled programs are solved for facts and toy programs. Handwriting must reach skills/formats, or choose what to protect better than a covariance. |
| Delta → LoRA, rank, placement | [LoRA-Squeeze](https://arxiv.org/abs/2602.10993), [LoRA on a Budget](https://arxiv.org/abs/2610.36386), [PiSSA](https://arxiv.org/abs/2404.02948), [AutoPEFT](https://arxiv.org/abs/2301.12132), [FIM-LoRA](https://arxiv.org/abs/2605.16800), [LAARA](https://arxiv.org/abs/2607.19391), [W2T](https://arxiv.org/abs/2603.15990) | SVD truncation and rank allocation are tooling. The question is whether an LLM's placement carries information a gradient-variance score does not. |
| Serving, merging, porting | [S-LoRA](https://arxiv.org/abs/2311.03285), [Punica](https://arxiv.org/abs/2310.18547), [LoRAForge](https://arxiv.org/abs/2611.01256), [MoLoRA](https://arxiv.org/abs/2603.15965), [TIES](https://arxiv.org/abs/2306.01708), LoraHub, [Trans-LoRA](https://arxiv.org/abs/2405.17258), [LoRA-X](https://arxiv.org/abs/2501.16559) | Serving many adapters is solved as systems; nothing certifies that a set of adapters is safe to load together, and porting transfers numbers, not intent. |
| Security | [LLMs write backdoors](https://arxiv.org/abs/2611.17395), [TrojanMaxxing](https://arxiv.org/abs/2611.27425) | Handwritten, hot-swappable adapters are an attack surface; a serve-time check is missing. |

## A · Make the eval itself (Manoj's task as a benchmark)

### HL01 · Handwritten-LoRA benchmark (HLB)
- **Improvement / assay** (enabling tool for every other card).
- **Mechanism:** Fixed base, fixed budget (total rank × modules ≤ K parameters), 8 tasks spanning facts, format, a narrow skill (StepGame, unit conversion), a domain (medical QA subset) and a refusal style. The writer submits a LoRA (B, A per module) and nothing else. Score = held-out gain minus a retention penalty on 3 untouched benchmarks, at fixed writer-token and evaluation budgets. The SVD route from the sketch is allowed (write full W′, the harness truncates to rank r) and its truncation loss is reported (HL05).
- **Nearest prior / gap:** [WeightBench](https://arxiv.org/abs/2611.18553) has reading/fixing/writing tracks over many networks but no LoRA-format LM track that frontier agents pass; [Exploring WSP](https://arxiv.org/abs/2611.09382) edits raw parameters with no budget. HLB fixes the format and charges for retention.
- **Cheapest first test:** 3 tasks on Qwen2.5-0.5B (CPU), 1 writer, 5 trajectories each. **Kill** if the trained LoRA at the same budget and random search do not separate by > 2 SE (the benchmark would not discriminate).
- **Old-task retention:** Built into the score.
- **Risk / likely tie:** Writers may fail every task at 0.5B; then raise to Qwen3.5-0.8B, where 2611.27089 shows non-zero handwritten gains.

### HL02 · Placement-only track: the writer picks rank, layers and modules; gradient fills values
- **Improvement** (decomposes the task; MX1 already rated placement an improvement).
- **Mechanism:** Split Manoj's task in two. In the placement track the writer chooses (layer, module, rank) per adapter from activations and weights, and a fixed 200-step LoRA training fills in the values. Compare with the full track (placement + values by hand) to see where the value of an LLM writer lies.
- **Nearest prior / gap:** [AutoPEFT](https://arxiv.org/abs/2301.12132), [FIM-LoRA](https://arxiv.org/abs/2605.16800), [LAARA](https://arxiv.org/abs/2607.19391), language-guided BO for LoRA hyperparameters. None uses a reasoning LLM that reads the weights.
- **Cheapest first test:** 4 HLB tasks. Arms: all-modules r = 8, FIM-LoRA allocation, AutoPEFT-style search at equal training runs, LLM placement. **Kill** if LLM placement is not ≥ 1 SE above FIM-LoRA on gain at equal parameters.
- **Old-task retention:** Penalty from HL01; placement may matter more for retention than for gain, so report both.
- **Risk / likely tie:** FIM-LoRA is cheap and strong.

### HL03 · Values-only track: placement fixed by an oracle, the writer writes the numbers
- **Improvement / assay.**
- **Mechanism:** Fix the placement to the best one found by training (sweep) and ask the writer only for B and A. This isolates whether LLMs can write the values at all once "where" is known.
- **Nearest prior / gap:** [WSP writes ICL](https://arxiv.org/abs/2611.26841) suggests editors write the ICL task vector; here the slot is given.
- **Cheapest first test:** Same tasks as HL02. **Kill** if handwritten values are not above the permuted-delta control and a rank-1 write of the mean activation difference (a one-line steering-vector baseline).
- **Old-task retention:** HL01 penalty.
- **Risk / likely tie:** The steering-vector baseline may be all the writer ever does; that is a result.

### HL04 · Rank as a price: the gain-per-rank curve of handwriting versus training
- **Improvement / assay.**
- **Mechanism:** Sweep r ∈ {1, 2, 4, 8, 16} for both writer and trainer. The sketch's "r = 1 for Qwen" predicts handwriting saturates at very low rank (one intent, one direction) while training uses rank for coverage. The crossover rank, if any, is the regime in which handwriting is worth considering.
- **Nearest prior / gap:** Rank-1 trained LoRA already hits 100% on StepGame (2611.27089); no paper reports the handwritten curve.
- **Cheapest first test:** 2 tasks × 5 ranks × 3 seeds. **Kill** if the trained curve dominates at every rank, including r = 1, on gain *and* retention.
- **Old-task retention:** Per rank.
- **Risk / likely tie:** Dominance at all ranks is plausible; then handwriting must win on later operations (B–D).

### HL05 · Truncation audit of the edit → delta → SVD route
- **Improvement / assay.**
- **Mechanism:** For every full-weight handwritten edit, compute how much benchmark gain survives top-r truncation and how much of ΔW's energy lies in the top r singular values. Compare with trained full fine-tune deltas. If handwritten edits are near rank-1 by construction (one direction written into one module), the SVD step is lossless and the LoRA format costs nothing; if they are diffuse (the 1,023-parameter edits in 2611.09382 are sparse, not low-rank), SVD may destroy them.
- **Nearest prior / gap:** [LoRA-Squeeze](https://arxiv.org/abs/2602.10993) compresses trained adapters; no audit of handwritten deltas.
- **Cheapest first test:** Re-use the released 2611.09382 / 2611.27089 patches if available, else HL01 trajectories. **Kill** (the route, not the root) if r ≤ 4 keeps < 50% of the gain; then the harness must accept sparse edits and the hot-swap story needs sparse adapters.
- **Old-task retention:** Truncation may *improve* retention by dropping spurious components; report both.
- **Risk / likely tie:** Sparse and low-rank are different; this card measures which one handwriting produces.

## B · What a handwritten adapter can be that a trained one cannot

### HL06 · Annotated components: an adapter as a list of documented rank-1 writes
- **Primitive** (new object: an adapter whose components each carry a read claim, a write claim and a unit test).
- **Mechanism:** The writer must emit each rank-1 component (b_i, a_i) with: "reads feature X (a_i matches activations on inputs like …)", "writes Y (b_i moves logits toward …)", and a 5-example unit test that fails without the component and passes with it. The harness checks every claim mechanically (activation projection on the claimed inputs, logit shift, test). An adapter is accepted only if all claims hold. This is the object the later cards operate on.
- **Nearest prior / gap:** [Interpretable WSP](https://arxiv.org/abs/2611.18114) builds transparent models from scratch; ROME edits carry a (subject, relation) key by construction; [Self-WSP](https://arxiv.org/abs/2611.28833) found writers do not understand their own edits. Checked, per-component claims inside an LM adapter are new.
- **Cheapest first test:** HLB, 3 tasks. Measure the fraction of components whose claims pass and the gain of the claim-passing subset alone. **Kill** if the claim-passing subset keeps < 60% of the full adapter's gain (claims would be decoration).
- **Old-task retention:** HL01 penalty for the claim-passing subset.
- **Risk / likely tie:** Writers may produce one large undocumentable component; the rank-1 constraint forces granularity.

### HL07 · Blame and bisect over components when a benchmark regresses
- **Primitive-candidate** (new operation: localize a regression to named components, then retract or rewrite only those).
- **Mechanism:** After loading a multi-component adapter, a retention check regresses. Ablate components one at a time (cheap: rank-1 each), find the culprit, read its claim, and either retract it or ask the writer to narrow its read direction. Trained adapters can be bisected too, but their singular directions have no claims, so a retracted direction cannot be rewritten with intent.
- **Nearest prior / gap:** Programs-weights flood ruled bisect/blame "tooling" in general; the new part is the rewrite step using the component's stated claim. PR #24 found fine-tuning damage diffuse, so first check concentration.
- **Cheapest first test:** Plant a known spillover (a component that also fires on distance questions). Arms: retract top-k SVD directions of a trained adapter, retract and retrain, bisect + claim-guided rewrite. **Kill** if claim-guided rewrite does not keep more target gain than retract-and-retrain at equal evaluations.
- **Old-task retention:** Is the target; also check unrelated benchmarks.
- **Risk / likely tie:** Retrain with a retention loss may tie cheaply.

### HL08 · Declared read-sets enforced at serve time
- **Primitive** (new object: an adapter that ships with the input subspace it may act on; the server gates it off outside it).
- **Mechanism:** Each handwritten component declares its read span (the span of its a_i plus a margin) and a domain description. At serve time the server computes the projection of the module's input onto the declared span; components whose input falls outside it are zeroed for that token. Retention is then enforced by construction on inputs outside the domain, not by training.
- **Nearest prior / gap:** [AlphaEdit](https://arxiv.org/abs/2410.02355) projects the edit onto the null space of preserved keys at write time; [MoLoRA](https://arxiv.org/abs/2603.15965) routes tokens to adapters with a learned router. A write-time *declaration* checked at serve time per token is new.
- **Cheapest first test:** HLB 3 tasks + 3 retention benchmarks. Arms: ungated adapter, AlphaEdit-projected adapter, learned router, declared-span gate. **Kill** if the gate does not cut retention loss by ≥ 50% versus ungated at ≤ 10% loss of target gain, or AlphaEdit projection matches it.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** Low-rank read spans may overlap general features (format, numbers), so the gate fires everywhere.

### HL09 · Handwritten protected sets for null-space edits
- **Improvement** (better choice of what AlphaEdit protects).
- **Mechanism:** AlphaEdit protects the covariance of a generic key sample. The writer instead names the behaviours to protect for this domain (e.g. "arithmetic still works", "distance questions"), the harness collects their keys, and the edit is projected onto that null space only. Smaller protected sets leave more room for the edit.
- **Nearest prior / gap:** AlphaEdit; [REX4 in cross-pool 108](https://github.com/manojbajaj95/cl/pull/36) handles keep/discard of residuals.
- **Cheapest first test:** StepGame on Qwen3.5-0.8B, the 2611.27089 distance tasks as the protected neighbours. **Kill** if the writer's protected set is not better than AlphaEdit's generic covariance on (target gain, neighbour retention).
- **Old-task retention:** Neighbour tasks plus generic benchmarks.
- **Risk / likely tie:** Generic covariance may already cover the neighbours.

### HL10 · Handwritten trigger components
- **Improvement** (a gate inside the adapter).
- **Mechanism:** Each skill component is paired with a trigger component that writes a large activation only on domain inputs and multiplies (through a nonlinearity the base already has, e.g. a gated MLP unit) the skill write. The writer builds the AND in weights, as [WSP writes ICL](https://arxiv.org/abs/2611.26841) found editors use near-silent MLP units keyed to prompt format.
- **Nearest prior / gap:** That paper's sparse keyed units; MoE gating. Building it deliberately with a stated trigger is the add.
- **Cheapest first test:** Same as HL08. **Kill** if it does not match HL08's gate without serving changes.
- **Old-task retention:** Off-domain benchmarks.
- **Risk / likely tie:** Merge with HL08 if they coincide.

### HL11 · Merging two domain adapters by reading their claims
- **Primitive-candidate** (new operation: merge by meaning, component by component).
- **Mechanism:** Two handwritten adapters (HL06) for domains D1 and D2 are merged by the writer: components with compatible claims are kept, conflicting ones (same read, opposite write) are resolved with a stated rule (domain trigger, keep newer, split by a cue). The merged adapter is one hot-swap unit for D1 ∪ D2.
- **Nearest prior / gap:** [TIES](https://arxiv.org/abs/2306.01708), DARE, LoraHub, task arithmetic merge numbers by sign and magnitude.
- **Cheapest first test:** 4 domain pairs with planted conflicts. **Kill** if claim-guided merge does not beat TIES and LoraHub on min(D1, D2) accuracy at equal rank.
- **Old-task retention:** Base benchmarks after the merge.
- **Risk / likely tie:** TIES is hard to beat on low-conflict pairs; the planted conflicts are where it must win.

### HL12 · Commutation certificates for hot-swapped adapter sets
- **Primitive** (new object: a checkable certificate that any subset of a set of adapters can be loaded together without changing each one's behaviour).
- **Mechanism:** Manoj's infra argument is per-domain hot swap. With many domain adapters, users will load several at once. If every component's read span (HL08) is orthogonal to every other adapter's write span in the next modules it feeds, adapters cannot interfere to first order. The writer is asked to write adapters that come with such a certificate (computed by the harness), and a server refuses co-loading without one.
- **Nearest prior / gap:** [S-LoRA](https://arxiv.org/abs/2311.03285), [Punica](https://arxiv.org/abs/2310.18547), [LoRAForge](https://arxiv.org/abs/2611.01256) serve many adapters but say nothing about co-loading; O-LoRA/InfLoRA separate subspaces during training of one sequence.
- **Cheapest first test:** 6 domain adapters on Qwen2.5-0.5B; load all 2^6 subsets. **Kill** if certified sets do not have ≥ 3× smaller worst-case drop in single-domain accuracy than uncertified trained adapters at equal rank, or if O-LoRA-trained adapters have the same property for free.
- **Old-task retention:** Base benchmarks with all 6 loaded.
- **Risk / likely tie:** First-order orthogonality may not survive nonlinearities across many layers; measure where it breaks.

## C · Hybrid loops: write where it helps, train where it helps

### HL13 · Handwritten adapter as LoRA initialization
- **Improvement.**
- **Mechanism:** Use the handwritten B, A as the starting point of LoRA training instead of zero/random; train k steps. If the handwritten adapter points in the right direction, training converges faster and stays closer to it (less spillover).
- **Nearest prior / gap:** [PiSSA](https://arxiv.org/abs/2404.02948) and LoRA-GA initialize from SVD of weights or gradients.
- **Cheapest first test:** HLB 3 tasks, k ∈ {10, 50, 200}. **Kill** if handwritten init does not beat PiSSA init on steps-to-90% and on retention.
- **Old-task retention:** At each k.
- **Risk / likely tie:** Gradient init is free; handwriting costs tokens.

### HL14 · Decompile a trained adapter, then recompile it by hand
- **Primitive-candidate** (new operation: replace a trained adapter with a documented one of the same behaviour).
- **Mechanism:** Train a LoRA, let the writer read it ([W2T](https://arxiv.org/abs/2603.15990), [From LoRA to Language](https://arxiv.org/abs/2611.09454)) and the behaviour change it causes, then write a fresh HL06 adapter meant to reproduce only the intended effect. The prediction: the recompiled adapter keeps the target, drops the template over-application 2611.27089 saw, and is smaller.
- **Nearest prior / gap:** HEX4 (decompilation, [cross-pool 107](https://github.com/manojbajaj95/cl/pull/36)) decompiles to text; this compiles back to weights.
- **Cheapest first test:** The StepGame rank-1 LoRA from 2611.27089 (retrain it if not released). **Kill** if the recompiled adapter does not keep ≥ 80% of target accuracy while recovering ≥ 50 pp of the distance-task collapse, or if retraining with a distance-task retention loss does as well at equal evaluations.
- **Old-task retention:** Distance tasks are the measure.
- **Risk / likely tie:** Retention-regularized training is the strong control.

### HL15 · Hand-repair of a trained adapter's spillover
- **Primitive-candidate** (new operation: a small handwritten counter-adapter that cancels one trained adapter's side effect).
- **Mechanism:** Keep the trained adapter; the writer adds 1–2 rank-1 components that read the "distance question" direction and write the opposite of what the trained adapter writes there. Smallest possible handwritten object with a clear, checkable job.
- **Nearest prior / gap:** [Controlled WSP repair](https://arxiv.org/abs/2611.25613) repairs planted faults; AlphaEdit projects edits. Repairing a *trained adapter's* spillover by hand is not in the abstracts read.
- **Cheapest first test:** 2611.27089 setup: Qwen3.5-0.8B, StepGame rank-1 LoRA, distance tasks at 0–2%. Arms: counter-adapter by hand, counter-adapter trained on distance examples at equal examples, AlphaEdit re-projection of the trained adapter, random rank-1 at matched norm. **Kill** if the handwritten counter-adapter does not restore distance accuracy to ≥ 80% with ≤ 5 pp StepGame loss, or the trained counter-adapter matches it at equal examples.
- **Old-task retention:** Distance tasks plus generic benchmarks.
- **Risk / likely tie:** A trained counter-adapter is easy; handwriting must win on examples needed (0–5 versus 50+).

### HL16 · Gradient proposes, the writer vetoes
- **Improvement.**
- **Mechanism:** Train a high-rank LoRA, take its SVD components, and have the writer accept or reject each with a reason after probing what it reads and writes. Keep the accepted set.
- **Nearest prior / gap:** LoRA-Squeeze and magnitude pruning keep top-k by size.
- **Cheapest first test:** HLB 3 tasks, r = 16 → keep ≤ 4. **Kill** if LLM veto does not beat top-4 by singular value and top-4 by retention-aware score on (gain, retention).
- **Old-task retention:** HL01 penalty.
- **Risk / likely tie:** A retention-aware score is a cheap automatic version.

### HL17 · Train the rule, handwrite the exceptions
- **Primitive-candidate** (new split of labour between trained and handwritten components).
- **Mechanism:** Training learns the frequent pattern; rare exceptions (a handful of counter-examples) are where training either ignores them or overfits. The writer adds one rank-1 component per exception class with a narrow read direction, documented as an exception.
- **Nearest prior / gap:** MEMIT for fact exceptions; CPX3 exception retention ([cross-pool 104](https://github.com/manojbajaj95/cl/pull/36)).
- **Cheapest first test:** Unit-conversion task with 5% irregular units. **Kill** if handwritten exception components do not beat upweighting the exceptions in training at equal parameters on exception accuracy without hurting the rule.
- **Old-task retention:** Rule cases and base benchmarks.
- **Risk / likely tie:** MEMIT on the exceptions may tie when exceptions are facts.

## D · Continual learning with handwritten adapters

### HL18 · A shared component bank that the writer reuses across domains
- **Primitive-candidate** (new object: a library of documented components that new adapters cite instead of rewriting).
- **Mechanism:** A stream of 10 domains. Before writing for domain k, the writer reads the bank of claim-checked components from domains 1..k−1 and may reuse a component by reference (shared weights) with a stated reason. Reused components are shared in serving, so the fleet grows sublinearly. Forward transfer and fleet size are measured.
- **Nearest prior / gap:** LoRA libraries with routing (Arrow, LoraHub, MoLoRA) reuse whole adapters; [PSX1](https://github.com/manojbajaj95/cl/pull/36) considers a shared LoRA basis. Reuse by a reasoned citation at component level is new.
- **Cheapest first test:** 10 small domains on Qwen2.5-0.5B. Arms: one trained adapter per domain, shared trained basis, bank with reuse. **Kill** if the bank does not cut total parameters by ≥ 30% at equal per-domain accuracy.
- **Old-task retention:** All earlier domains after each new one (shared components change only by appending).
- **Risk / likely tie:** Few components may be genuinely reusable.

### HL19 · Revise one component when the domain changes
- **Primitive-candidate** (new operation: an amendment that edits a named component, not the adapter).
- **Mechanism:** A domain rule changes (a new policy, a renamed product). The writer locates the component whose claim mentions the rule, rewrites only it, and re-runs its unit test and all other components' tests.
- **Nearest prior / gap:** Retraining the adapter, or MEMIT on top. LL19-type amendments in [PR #344](https://github.com/manojbajaj95/cl/pull/344) use a trained Learner.
- **Cheapest first test:** 3 domains, 3 rule changes each. **Kill** if component rewrite does not match retraining on new-rule accuracy at ≤ 1/5 the evaluations with no worse old-rule retention.
- **Old-task retention:** Unchanged rules in the same domain, other domains.
- **Risk / likely tie:** Rules may not map to single components.

### HL20 · Retire a component, keep its test
- **Primitive-candidate** (new object: a regression suite made of retired components' unit tests).
- **Mechanism:** When a component is retracted or superseded, its unit test (with the expected *new* outcome) joins a fleet-wide regression suite that every future handwritten write must pass. The fleet accumulates a memory of past intents without keeping their weights.
- **Nearest prior / gap:** Software regression suites; replay buffers keep data, not intents.
- **Cheapest first test:** HL19 stream with 10 retirements. **Kill** if the suite catches fewer regressions than a random sample of the same number of old training examples.
- **Old-task retention:** Is the measure.
- **Risk / likely tie:** Random old examples may cover the same cases.

### HL21 · Recompile an adapter onto a new base model from its spec
- **Primitive** (new operation: adapters as source code; on a base upgrade, port the intent, not the numbers).
- **Mechanism:** Base models get upgraded (Qwen2.5 → Qwen3.5). Trained adapters must be retrained or numerically transferred. A handwritten adapter has a spec (HL06 claims and unit tests); the writer re-derives every component on the new base by finding the new base's directions for the same claims, and the unit tests check the port. The fleet of domain adapters survives base upgrades at writer-token cost.
- **Nearest prior / gap:** [Trans-LoRA](https://arxiv.org/abs/2405.17258) transfers with synthetic data and retraining; [LoRA-X](https://arxiv.org/abs/2501.16559) projects adapters across models training-free. Both move numbers; neither has a per-component spec to check against.
- **Cheapest first test:** 4 HLB adapters written for Qwen2.5-0.5B, ported to Qwen2.5-1.5B and to a different family (SmolLM2). Arms: LoRA-X projection, Trans-LoRA, retrain on the original data, spec recompile. **Kill** if spec recompile does not reach ≥ 90% of retrain accuracy with fewer examples than Trans-LoRA, or LoRA-X matches it.
- **Old-task retention:** New base's benchmarks with the ported adapter.
- **Risk / likely tie:** Claims may be too vague to re-locate; the unit tests decide.

### HL22 · One spec, many sizes
- **Primitive-candidate** (follows HL21).
- **Mechanism:** Write the spec once against the smallest model, compile adapters for 0.5B, 1.5B and 7B. Tests whether the spec is model-independent and whether writing gets easier or harder with size (2611.21885 reports self-editing ability emerging with scale).
- **Nearest prior / gap:** HL21; LoRA-X across sizes.
- **Cheapest first test:** 2 adapters × 3 sizes. **Kill** if per-size accuracy falls below a per-size trained LoRA by > 10 pp at any size.
- **Old-task retention:** Per size.
- **Risk / likely tie:** Larger models may need more components for the same claim.

### HL23 · Sequential handwritten edits versus MEMIT and AlphaEdit
- **Improvement** (CL capacity of handwritten writes).
- **Mechanism:** Apply 1,000 handwritten rank-1 edits in sequence, the writer choosing layer and protected set per edit, against MEMIT and AlphaEdit sequential edits.
- **Nearest prior / gap:** AlphaEdit is built for sequential editing. PR #22: show N* varies before predicting it.
- **Cheapest first test:** CounterFact on GPT-2-XL (CPU, the PR #22/#24 setup). **Kill** if handwritten edits do not beat AlphaEdit on efficacy × locality at 1,000 edits.
- **Old-task retention:** Locality and generic perplexity.
- **Risk / likely tie:** AlphaEdit is closed-form and cheap; handwriting is slow. Likely tie or loss; kept as the honest control for the whole root.

## E · Picking sizes, layers and modules (Manoj's second half)

### HL24 · Causal localization before writing
- **Improvement.**
- **Mechanism:** The writer runs activation patching on 20 failing examples to find which layer/module carries the failure, then writes there. Compare with ROME-style causal tracing and gradient-norm placement.
- **Nearest prior / gap:** [ROME](https://arxiv.org/abs/2202.05262) causal tracing for facts; FIM-LoRA for skills.
- **Cheapest first test:** HLB 3 tasks, placement-only (HL02 harness). **Kill** if patching-based placement is not above FIM-LoRA.
- **Old-task retention:** HL01 penalty.
- **Risk / likely tie:** Same as HL02.

### HL25 · Predict placement from a task description alone
- **Improvement.**
- **Mechanism:** Before seeing any data, the writer predicts (module type, depth band, rank) from the task description and a library of past placements. Zero-shot placement is what a multi-domain fleet needs when a new domain arrives.
- **Nearest prior / gap:** Text-to-LoRA predicts whole adapters from descriptions; placement-only prediction is cheaper and checkable.
- **Cheapest first test:** 10 tasks with sweep-optimal placements known. **Kill** if predicted placement is not closer to optimal than a fixed "all MLP, middle third, r = 8" rule.
- **Old-task retention:** Same as HL02.
- **Risk / likely tie:** The fixed rule may be near-optimal for most tasks.

### HL26 · The smallest adapter that does the job
- **Improvement / assay.**
- **Mechanism:** The writer minimizes parameter count subject to gain ≥ g; report the Pareto frontier against AdaLoRA/LoRA-Squeeze pruning. [Exploring WSP](https://arxiv.org/abs/2611.09382) got +29.45 pp on MATH-500 from 1,023 parameters; is that gain reproducible and where does it live?
- **Nearest prior / gap:** Rank allocation and pruning methods.
- **Cheapest first test:** 3 tasks, g at 50% and 90% of the trained gain. **Kill** if the handwritten frontier is dominated by pruned trained adapters.
- **Old-task retention:** Smaller adapters should retain better; check.
- **Risk / likely tie:** The 1,023-parameter result may be a format fix (answer extraction), which is cheap for any method; test with format-normalized scoring.

### HL27 · A placement map: which module type holds facts, formats and procedures
- **Improvement / assay.**
- **Mechanism:** Collect the writer's placements and their outcomes across 30 tasks; fit a map (task type → module, depth). Test whether the map predicts where a *trained* LoRA's effect concentrates (by per-module ablation).
- **Nearest prior / gap:** Layer-role studies (facts in mid MLPs, format near output); MX1 route results in the ledger.
- **Cheapest first test:** 12 tasks in 3 types. **Kill** if the map's top placement matches the trained effect's top module in < 50% of held-out tasks.
- **Old-task retention:** Not applicable (assay); per-task penalty logged.
- **Risk / likely tie:** Known lore may already give the map.

## F · Making the eval honest and the infra safe

### HL28 · Gate-set overfitting audit
- **Improvement / assay.**
- **Mechanism:** WSP loops accept edits that improve a gate set ([SelfWrite](https://arxiv.org/abs/2611.29513)). With many writer attempts per task, the accepted edit is selected on the gate. Measure the gate-to-test gap as a function of attempts, for the writer and for random search, and correct scores by a held-out split the loop never sees.
- **Nearest prior / gap:** Adaptive data analysis / reusable holdout; Self-WSP's random-search finding.
- **Cheapest first test:** HLB, 50 attempts per task. **Kill** (the root's headline claims) if the writer's test gain is within CI of random search's at equal attempts.
- **Old-task retention:** Penalty also measured on the never-seen split.
- **Risk / likely tie:** This card may kill the head-to-head claim; it protects the rest.

### HL29 · Standard controls as a harness
- **Improvement / assay.**
- **Mechanism:** Bundle into HLB: permuted delta (2611.27089), random rank-1 at matched norm, ES/black-box search at equal evaluations, steering-vector rank-1 write, trained LoRA at equal examples and placement. Every card reports them.
- **Nearest prior / gap:** Scattered across the WSP papers.
- **Cheapest first test:** Run on HL01's first 3 tasks. **Kill** none; this is infrastructure. Fail if any control is missing from a reported result.
- **Old-task retention:** Same penalty for every control.
- **Risk / likely tie:** None.

### HL30 · Serve-time audit of handwritten adapters for hidden triggers
- **Primitive-candidate** (new operation: check an adapter's actual read spans against its declaration before hot-swap).
- **Mechanism:** LLMs can write backdoors into weights ([2611.17395](https://arxiv.org/abs/2611.17395), [TrojanMaxxing](https://arxiv.org/abs/2611.27425)). A fleet of handwritten, hot-swapped adapters needs an admission check. With HL08 declarations, the server compares each component's a_i with its declared span and probes it on random and adversarial inputs; components that read outside their declaration are refused.
- **Nearest prior / gap:** [LoRA-Patch](https://arxiv.org/abs/2611.03752) defends against backdoored LoRAs by steering after the fact.
- **Cheapest first test:** 20 benign and 20 backdoored handwritten adapters (writer asked to hide a trigger). **Kill** if detection AUROC < 0.9, or a generic weight-statistics detector does as well.
- **Old-task retention:** Benign adapters must pass admission with their full gain.
- **Risk / likely tie:** A writer can declare a broad span; the audit must charge for breadth.

### HL31 · Data-free domain adapters from a description and unlabelled inputs
- **Improvement** (head-to-head with amortized writers).
- **Mechanism:** Manoj's per-domain tailoring often has no labels. The writer gets a domain description and 50 unlabelled inputs, writes its own probe examples (as the strongest editor did in [WSP writes ICL](https://arxiv.org/abs/2611.26841)), and writes the adapter.
- **Nearest prior / gap:** [Text-to-LoRA](https://arxiv.org/abs/2506.06105) (description) and [Drag-and-Drop LLMs](https://arxiv.org/abs/2506.16406) (unlabelled prompts) do this in one forward pass.
- **Cheapest first test:** 5 domains held out from T2L/DnD training. **Kill** if the writer does not beat both at equal input information.
- **Old-task retention:** Base benchmarks.
- **Risk / likely tie:** T2L/DnD are far cheaper; the writer must win clearly.

### HL32 · Cost ledger: writer tokens versus GPU-seconds
- **Improvement / assay** (the deployment question).
- **Mechanism:** For every result, log writer tokens and dollars, evaluation calls, and the GPU-seconds a trained LoRA needed for the same gain. Find the regime (few examples, frequent revisions, many domains, base upgrades) in which handwriting is cheaper in total.
- **Nearest prior / gap:** PR #344's ranked question 4 asks the same for a neural writer.
- **Cheapest first test:** Fill in from HL01, HL19 and HL21 runs. **Kill** the infra pitch if no regime has handwriting cheaper at equal gain and retention.
- **Old-task retention:** Included in "equal retention".
- **Risk / likely tie:** Training a rank-1 LoRA on a 0.8B model costs minutes; handwriting must win on revisions and ports, not first writes.

### HL33 · Edit-ready bases for handwritten adapters
- **Improvement.**
- **Mechanism:** [Edit-Ready Training](https://arxiv.org/abs/2611.26408) rehearses the closed-form edits LLMs perform so vision models accept them better. Do the same for an LM base: a short fine-tune that rehearses rank-1 LoRA writes of the kinds writers make (keyed MLP units, task vectors), so later handwritten adapters land with less spillover.
- **Nearest prior / gap:** ERT on vision; editable training (MEND-style) for LMs.
- **Cheapest first test:** Qwen2.5-0.5B, ERT-style pre-pass, then HLB. **Kill** if handwritten gain and retention on the prepared base do not beat the unprepared base by > 2 SE, or the pre-pass costs > 1 pp on base benchmarks.
- **Old-task retention:** Base benchmarks before and after the pre-pass.
- **Risk / likely tie:** The pre-pass may help trained adapters as much.

## Ranked deeper questions

1. **Can a handwritten adapter be recompiled from its spec onto a new base model (HL21, HL22, HL06)?** This is the cleanest new primitive: adapters as source code, so a domain fleet survives base upgrades without data. First answer: HL21's Qwen2.5-0.5B → 1.5B and → SmolLM2 port against LoRA-X and Trans-LoRA. Dead if LoRA-X projection matches spec recompile.
2. **Can handwriting fix what training breaks (HL15, HL14, HL17)?** 2611.27089 shows a trained rank-1 LoRA wins the target but destroys neighbouring skills. If 1–2 handwritten components restore them with almost no examples, handwriting has a job training does not do well. First answer: HL15 on the published StepGame / distance setup.
3. **Do per-component claims make a hot-swap fleet safe to compose (HL08, HL12, HL30)?** Manoj's infra case is per-domain hot swap; the missing piece is knowing which adapters can be loaded together and that none hides a trigger. First answer: HL12's 6-adapter, 64-subset test.
4. **Where does the LLM writer add value: placement or values (HL02, HL03, HL04, HL24–HL27)?** If placement-only plus a short training run captures most of the gain, the eval should be "pick sizes and layers", and the handwriting half is optional. First answer: HL02 versus HL03 on the same 4 tasks.
5. **Does any of it survive honest controls and cost (HL28, HL29, HL32)?** Random search and gate overfitting have already matched LLM writers in Self-WSP. Run HL28 and HL29 with HL01 before any headline claim; use HL32 to state the regime in which the infra pitch holds.
