# H1 kill test: latent programs for a bracket stack

**Verdict: stop this retrofit.** The loop-plus-vectors arm got 22/64 (34.4%) at both depth 4 and depth 8, then fell to 11/64 (17.2%) at depth 12. At depth 12 it was behind the loop without vectors (23.4%), both one-pass vector controls (21.9%, 26.6%), few-shot RAG (26.6%), and RAG with scratchpad (25.0%). With vectors off, depth-12 perplexity drift was **+0.255**, over the +0.2 limit.

## Results

Exact-match accuracy, percent with 95% Wilson intervals in brackets; **64 examples per depth per arm** (32 per seed, shared across arms).

| Arm | Depth 4 (fit range) | Depth 8 (2× length) | Depth 12 (3× length) |
|---|---:|---:|---:|
| **Loop + 16 vectors** | **34.4 [23.9, 46.6]** | **34.4 [23.9, 46.6]** | **17.2 [9.9, 28.2]** |
| Loop, no vectors | 25.0 [16.0, 36.8] | 25.0 [16.0, 36.8] | 23.4 [14.7, 35.1] |
| One pass, identical vectors | 31.2 [21.2, 43.4] | 23.4 [14.7, 35.1] | 21.9 [13.5, 33.4] |
| One pass, refit vectors | 26.6 [17.3, 38.5] | 29.7 [19.9, 41.8] | 26.6 [17.3, 38.5] |
| Few-shot completion RAG | 25.0 [16.0, 36.8] | 25.0 [16.0, 36.8] | 26.6 [17.3, 38.5] |
| RAG + scratchpad | 18.8 [11.1, 30.0] | 21.9 [13.5, 33.4] | 25.0 [16.0, 36.8] |
| One pass, byte-matched LoRA | 28.1 [18.6, 40.1] | 21.9 [13.5, 33.4] | 26.6 [17.3, 38.5] |

At depth 12, paired loop-program differences were −6.2 percentage points versus loop-only (95% CI −21.9 to +9.4), −4.7 versus identical one-pass vectors (−15.6 to +4.7), and −9.4 versus refit one-pass vectors (−21.9 to +3.1). At depth 8, the gain over the refit one-pass vector control was +4.7 points (−9.4 to +18.8). Paired intervals use 10,000 bootstrap resamples of items within each seed. These intervals describe item-level uncertainty conditional on the two fits, not variability across new seeds, grammars, or architectures; [summary.json](summary.json) has counts by seed and all paired comparisons.

**WikiText-2 perplexity** (signed changes vs native **25.629** in parentheses):

| Loop passes | Vectors off | Vectors forced on, seed 3407 | Vectors forced on, seed 9041 |
|---|---:|---:|---:|
| 4 | 25.463 (−0.166) | 27.449 (+1.820) | 27.156 (+1.527) |
| 8 | 25.537 (−0.092) | 27.319 (+1.690) | 26.946 (+1.317) |
| 12 | 25.884 (+0.255) | 27.600 (+1.971) | 27.170 (+1.541) |

| H1 kill criterion | Outcome |
|---|---|
| At least 50% at 2× training length | **Miss:** 34.4% at depth 8 (95% CI 23.9–46.6); 17.2% at requested depth 12. |
| Beat byte-matched unlooped LoRA by at least 20 points | **Miss:** +12.5 points at depth 8 (95% paired CI +3.1 to +23.4), −9.4 at depth 12 (−21.9 to +3.1). |
| Beat few-shot RAG + scratchpad by at least 20 points | **Miss:** +12.5 points at depth 8 (+1.6 to +23.4), −7.8 at depth 12 (−21.9 to +6.2). |
| Program-off perplexity drift no greater than +0.2 | **Miss** at depth 12 (+0.255); within the limit at depths 4 and 8. |

The depth-12 baselines did not solve the task either: plain RAG emitted **B** for 59/64 items, and every scratchpad emitted a final checkpoint at position **16** (the demonstration length), not 48. The negative result applies to this host and install recipe, not all recurrent models: one grammar, one block, four rather than ten healing families, short training, small held-out samples and no optimization sweep. Tape length and nesting depth increase together. We did not test transfer to a second skill or directly probe a latent stack. The two measured stages took about 37 minutes combined on eight CPU threads, excluding downloads.

## Reproduce

On Linux/x86-64 with Python 3.10+, `venv`, `curl`, and `sha256sum`:

```sh
bash experiments/h1_latent_loop/reproduce.sh
```

This installs CPU dependencies into a local venv, downloads and verifies the pinned 3.1 GB Qwen2.5-1.5B **base** checkpoint and WikiText-2 splits, runs the seven arms, and writes `run.json` (item-level outputs), `summary.json` (scores and intervals), and fitted tensors under `~/.cache/cl-h1/results`. Set `H1_DATA` or `H1_OUT` to relocate inputs or outputs, and `H1_PYTHON` to use a Python environment with the pinned dependencies already installed. The default run uses eight CPU threads and FP32 computation. Run the local tests with `python -m pytest -q experiments/h1_latent_loop` in that environment.

## Protocol

- **Target.** Given a valid, unfinished prefix over four bracket types, give the next matching close as an answer letter A–D. Two trailing pops are mandatory; the label is the type of the opening left on top, not the type of the last close. Reference scoring uses a stack. Each seed has 64 unique depth-4 install examples and 32 distinct, label-balanced test examples per exact peak nesting depth; a uniform guess scores 25%. Seeds: 3407 and 9041. Training and test lengths are 16 symbols at depth 4, 32 at depth 8, and 48 at depth 12. Depth 8 measures H1's literal 2× training-length criterion; depth 12 is the requested 3× stress test. This is an adaptation of the prior suite's stateful nesting task, not a rerun of its bounded depth/peak/underflow record or its raw accuracy scale.
- **One retrofit.** On the frozen 28-layer Qwen base, repeat the four middle Qwen layers at zero-based indices 12–15. The first pass is native; each later pass applies a learned channelwise interpolation between the current state and the shared block output. Only the 1,536 gate logits train in 16 alternating updates on WikiText-2 train and four non-bracket stateful families (reset counter, rolling checksum, toggle, and finite-state ring). The gate sees loop counts 4, 8 and 12 during healing, but never the bracket task. It is frozen thereafter. For the grammar, set loop count to tape length divided by four (40, 56, or 72 total layer applications), which requires no computed stack state.
- **Skill program.** Fit 16 virtual prefix vectors at the loop entrance using only next-token answer loss on the 64 demos, three epochs at loop count 4, independently for each seed. The prefix states evolve through the block and are removed before the last 12 layers. Each vector has 128 learned coefficients expanded to 1,536 dimensions by a shared fixed sign projection; the FP16 payload is 4,096 bytes, excluding shared infrastructure and file headers.
- **Controls.** Compare the same loop with no vectors; the **identical fitted coefficients** applied at the same location with just one pass; the same vector parameterization refit from the same seed initialization for one pass; and a 4,096-byte FP16 rank-1 LoRA baseline on a 1,024 × 1,024 slice of the layer-12 attention output projection in the unlooped model. The trainable arms use the same examples, batch size, and epoch count, but not equal FLOPs. LoRA and vector tuning use different learning rates and neither was swept.
- **Text baselines.** The unlooped model gets the same explicit grammar plus three training demonstrations retrieved by nearest tape length (fixed install order breaks ties), following the prior suite's 3-shot completion approach. Scratchpad uses the same demonstrations with stack traces at roughly thirds and an `=>` delimiter, adapting the prior suite's checkpoint-trace prompt and parser. Neither baseline sees test demonstrations. Outputs are greedy and unconstrained: direct arms get a single token; scratchpad gets one line, at most 48 tokens, and missing/malformed final answers count as wrong. This tests useful exact completions, not forced-choice ranking of four logits.
- **Drift.** Compare teacher-forced, full-vocabulary perplexity on the same 16 held-out WikiText-2 test windows (1,008 predicted tokens). Use the same three loop counts with vectors off and with each installed program forced on unrelated text; the non-looped model is the reference. The runner asserts numerical parity between the custom one-pass path without vectors and native Transformers logits.

## Closest prior art

- **Wu, Hu & Zhang, [Shared Weights, Selected Computations](https://arxiv.org/abs/2609.39892) (Sep 2026)** is the closest steering precedent. They select graph-walk transitions in a frozen loop by learning an entering-state linear map, and their interventions link the effect to attention routing and what the host learned. This test instead fits a 4 KiB continuous prefix after a generic retrofit and asks whether terminal-only demonstrations install a *held-out* grammar. Neither an accuracy gain nor a failure would establish how any particular loop processes the stack.
- **McLeish et al., [Teaching Pretrained Language Models to Think Deeper with Retrofitted Recurrence](https://arxiv.org/abs/2511.07384) (2025)** is the closest retrofit precedent. They convert pretrained models using a recurrent core, a learned bridge and a depth curriculum, studying math at different compute budgets. Here the shared Qwen weights never move; a tiny gate is healed once, followed by an independently installed skill. Other retrofits include [LoopUS](https://arxiv.org/abs/2605.11011)'s selective gating and deep supervision, [Shapiro](https://arxiv.org/abs/2608.11233)'s Qwen recurrence with intermediate-step supervision and larger trainable budgets, [UpLoop](https://arxiv.org/abs/2610.25004)'s layer-local gates, and [LoopRes](https://arxiv.org/abs/2611.31094)'s cross-iteration residual attention.
- **[Ouro / Scaling Latent Reasoning via Looped Language Models](https://arxiv.org/abs/2510.25741)** and Geiping et al.'s **[Huginn](https://arxiv.org/abs/2502.05171)** learn recurrent-depth competence during pretraining; Ouro also learns depth allocation. Here the loop is a post-training retrofit, the iteration budget is prescribed from tape length, and the new skill is stored separately without changing the host.
- [Universal Transformers](https://arxiv.org/abs/1807.03819) share a block across depth; [Saunshi et al.](https://arxiv.org/abs/2502.17416) study reasoning and latent thoughts from such loops; [Giannou et al.](https://proceedings.mlr.press/v202/giannou23a.html) program specially constructed looped weights; [Coconut](https://arxiv.org/abs/2412.06769) feeds back continuous states in place of explicit reasoning tokens. [Prompt tuning](https://arxiv.org/abs/2104.08691) and [prefix tuning](https://arxiv.org/abs/2101.00190) are closest to the fitted parameterization; the one-pass controls specifically test whether repeated use matters beyond the soft prefix.
