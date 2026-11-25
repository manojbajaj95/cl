# Effect-class distillation on a renamed API

**KILL.** On three CPU seeds, effect-class replay beat canonicalized token KL on the retention–adoption front, but did not beat execution-reward-only replay. Reward-only had higher front hypervolume in all three seeds. A GPU was not needed: building the frozen cache took 152.18 s on an eight-vCPU Xeon, and all seed training and evaluation after caching took 26.48 s.

## Results

| Front | Mean hypervolume (95% seed CI) | Effect minus control (paired 95% seed CI) |
| --- | ---: | ---: |
| Effect class | 0.9921 [0.9800, 1.0043] | — |
| Canonicalized token KL | 0.9823 [0.9761, 0.9885] | +0.0099 [+0.0032, +0.0165] |
| Execution reward only | 0.9949 [0.9859, 1.0040] | −0.0028 [−0.0064, +0.0008] |

Intervals are unclipped. Mean held-out old-task pass rose from 90.09% before stage 1 to 99.93% at the pre-migration checkpoint, with less than 0.002% new syntax in each checkpoint. The migration endpoints below are three-seed means. [Raw per-seed results](results.json) include the joint pass/adoption rate and per-arm execution counts.

| Migration arm | Replay weight | Old-task pass | New syntax on old tasks | New-task pass |
| --- | ---: | ---: | ---: | ---: |
| Naive SFT | 0 | 98.06% | 100.00% | 98.33% |
| Effect class | 0.25 | 98.61% | 99.99% | 99.24% |
| Effect class | 1 | 99.10% | 99.99% | 99.58% |
| Effect class | 4 | 97.97% | 89.71% | 99.49% |
| Canonicalized token KL | 0.25 | 94.41% | 66.39% | 98.83% |
| Canonicalized token KL | 1 | 96.62% | 52.22% | 98.37% |
| Canonicalized token KL | 4 | 97.17% | 40.68% | 98.26% |
| Execution reward only | 0.25 | 98.53% | 100.00% | 99.16% |
| Execution reward only | 1 | 99.02% | 99.99% | 99.55% |
| Execution reward only | 4 | 99.49% | 100.00% | 99.84% |

The naive arm is already near the ceiling on this stream, and the nearly perfect teacher puts most class mass on the same behavior that the binary reward favors. This is a negative result under the pilot criterion, not evidence about unrestricted generation or harder migrations.

## Design

- Qwen2.5-Coder-0.5B (revision `8123ea2`), with a rank-16, output-head-only LoRA adapter. The decoder is a constrained token trie over 24 legal one-call expressions per prompt: three operations, two API versions, two argument orders and two spacing styles. Frozen hidden states are cached at branch points; that is exact for head-only training, not an approximation to full-model LoRA. This tests relative preference among real code completions, not open-ended code generation.
- Three operations have new names and one also reverses positional arguments. The execution interpreter supports both APIs through a compatibility shim. Each stage has 36 supervised prompts and 24 held-out paraphrases; prompts ask for behaviors without specifying API version. The same semantics are required before and after migration.
- Seeds 101/202/303 each train a pre-migration checkpoint for 100 steps and start all migration arms from that checkpoint. Every arm receives the same 100×12 new SFT examples per seed and runs four frozen-teacher and four student completions per replay prompt: **9,600 completions / 67,200 executions per migration arm**, including unused draws in the controls and naive baseline. Each completion executes three class probes and four disjoint correctness tests.
- **Effect:** minimize sampled forward class cross-entropy: within each prompt and represented class, the student log-prob gradients share the empirical teacher class mass, with no target API tokens. Classes absent from student draws contribute no gradient at that step. **Token:** Monte Carlo forward KL (up to the fixed teacher entropy) on canonicalized code token paths; the AST normalizes spacing and positional variable names, not API names or argument order. **Reward:** on-policy replay weighted by the binary old-task test result, without a teacher target. Each replay arm sweeps loss weights 0.25, 1 and 4; naive is the common SFT-only point.
- Rates on held-out prompts are exact expectations under the constrained decoder (execute all completions, weight by policy probability). Retention is old-task unit-test pass, even if old names are used. Adoption is unconditional use of the new name on old-task prompts; a wrong new call still counts, so joint pass/adoption is reported separately in the raw results. New-task pass is a sanity check.
- The decision statistic is each seed's dominated hypervolume in (old-task adoption, old-task pass), relative to (0, 0) and including the common naive point. Keep only if both paired effect-minus-control 95% Student-`t` intervals across seeds are strictly above zero. The three-seed intervals do not measure variation across libraries or task sets.

The closest cited work anchors teacher decisions in text: [Persistent Teacher Anchoring](https://arxiv.org/abs/2609.04773) commits verified call text before execution, and [When Top-K Misses the Decision](https://arxiv.org/abs/2607.07050) studies teacher-logit support at tool-call boundaries. This pilot instead groups different call strings by the output vectors of executed probes; it is not an exhaustive novelty review.

## Reproduce

From this directory (Python 3.10, CPU):

```sh
python -m pip install -r requirements.txt
python -B -m unittest -v
python -B pilot.py --cache /path/to/cache.pt --output /path/to/results.json
```

The cache and output parent directories must exist. The cache is generated from the pinned Hugging Face checkpoint on the first run; subsequent runs reuse it.
