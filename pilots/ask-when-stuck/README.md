# Ask when stuck: ALFWorld pilot

Does delivering a question-indexed atom **after a simulator failure** make memory growth less harmful than putting the same atoms in the initial prompt? Does an equally provisioned model-confidence gate do just as well?

[Frozen protocol](protocol.md) · [Greedy results](results.json) · [Temperature-control results](results-entropy.json)

## Results

**KILL at the CPU gate.** Failure pull did not decline less than matched push, did not beat either confidence control, and did not clear the source-fitted temperature control. This rules out scaling this configuration, not all failure-triggered retrieval.

### Greedy store-size sweep

Success (%) across 134 unseen ALFWorld tasks. Means and paired 95% Student t intervals are over five blocks of held-out task groups; the greedy no-memory reference scored 45.6%.

| Store | Always push | Push, matched | Failure pull | Confidence pull | Prospective confidence |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12, clean anchor | 52.4 | 45.7 | 44.8 | 42.6 | 47.0 |
| 36, stressed | 53.2 | 47.9 | 43.3 | 41.9 | 48.6 |
| 90, stressed | 50.0 | 44.1 | 42.6 | 41.1 | 45.6 |
| 180, stressed | 47.7 | 44.0 | 42.6 | 41.1 | 44.8 |
| 180, clean | 56.1 | 47.8 | 44.8 | 42.6 | 48.5 |

| Paired contrast | Difference, pp (95% CI) |
| --- | ---: |
| 180 stressed vs. 12, always push | −4.6 [−14.7, +5.4] |
| 180 stressed vs. 12, matched push | −1.6 [−8.6, +5.3] |
| 180 stressed vs. 12, failure pull | −2.2 [−4.7, +0.3] |
| Failure-pull change minus matched-push change | −0.6 [−9.4, +8.2] |
| Failure pull vs. matched push at 180 stressed | −1.5 [−4.0, +1.0] |
| Failure pull vs. confidence pull at 180 stressed | +1.4 [−2.5, +5.4] |
| Failure pull vs. prospective confidence at 180 stressed | −2.2 [−7.6, +3.2] |

The push declines were not established, and neither were a failure-pull advantage or practical equivalence to confidence pull within ±5 points. At matched budgets (41 queries per arm, 120 memory-slot tokens per query), failure pull saw 0.68 corrupt atoms per task vs. 0.72 for push; the paired difference was −0.05 [−0.15, +0.06] corrupt atoms per task. Always-push saw 2.23 per task, but it queried every task.

### Source-fitted temperature control at the largest stressed store

On the 48 source tasks, temperature 1.066 matched the memory-prompt entropy at 0.985 nats (unscaled: 0.952). On held-out failure retries, entropy was 0.943 for failure pull and 0.951 for the scaled no-memory policy (unscaled: 0.917). The control matched mean entropy closely without a held-out fit; it did not match individual action probabilities.

| Policy (stochastic decoding) | Task success | Difference vs. entropy-matched no memory, pp (paired 95% CI) |
| --- | ---: | ---: |
| No memory, entropy matched | 46.3% | — |
| No memory, unscaled | 47.0% | +0.7 [−1.3, +2.7] |
| Always push | 49.2% | +2.9 [−2.9, +8.7] |
| Push, matched | 47.0% | +0.7 [−3.1, +4.5] |
| Failure pull | 44.1% | −2.2 [−7.4, +3.0] |
| Confidence pull | 45.5% | −0.8 [−7.0, +5.3] |
| Prospective confidence | 47.7% | +1.4 [−3.8, +6.6] |

No memory arm cleared the entropy-matched no-memory control. This is a failure to establish a memory benefit, not evidence the policies are generally equivalent.

## What this tests

[More Memory, Worse Agents (§4.1, §D.1, §G.1)](https://arxiv.org/abs/2610.27406) freezes memory for evaluation on official ALFWorld unseen tasks and retrieves by goal plus initial observation. Its §G.1 ablation varies how many records enter context; this pilot instead varies **index size with top-five retrieval fixed**. The paper's main experiment evolves memory over ten rounds with much larger models. Here one Qwen2.5-0.5B checkpoint controls a single action plus at most one retry, with an official walkthrough providing the other actions. The simulator verifies each branch and whether the reference suffix completes the game. The checkpoint and small action menu make this a diagnostic, not a benchmark leaderboard result or evidence about full trajectories.

Training games and held-out games are the official disjoint splits. Each block builds its index only from 180 verified training walkthroughs. Indexed keys are past goals and initial observations. Answers are advice templates based on the successful procedural operation. The index has distinct task records but only five operation templates. Memory is immutable at test time; training exploration, new writes, and error reproduction are out of scope.

The stress index grows by adding a mixture of clean atoms and matched-scope, intentionally wrong advice. A large clean control replaces wrong answer text without changing any query, rank, or key. This isolates the effect of injected content at the largest size; stress growth alone confounds store size and corruption. The failure gate observes literal simulator feedback; it does not receive gold actions. The primary [FLARE-style](https://arxiv.org/abs/2305.06983) control retrieves for the least-confident retry states, using the same retry context as failure pull. An exploratory prospective variant instead rescores the least-confident first actions with memory before acting, regardless of outcome. Neither implements FLARE's sentence-generation algorithm.

All policies have at most two action opportunities and identically sized memory slots per prompt. The matched policies also receive the same **occupied memory-slot** token count in each block: each nonempty delivery is five 24-token slots including padding, with neutral content in otherwise empty prompts. Always-push uses more occupied slots and serves as a stress check. Overall input tokens and calls need not be identical: a successful first decision stops the episode. The matched controls share the failure gate's aggregate query count for the block; the push masks do not depend on which individual tasks failed. The prospective variant needs one extra neutral first-action score per episode that it rescores; its reported compute must include that score.

## Reproduce

Linux x86-64 and Python 3.10 (TextWorld may need GCC/G++ for dependencies); no API keys or GPU. In this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p artifacts/data
curl -fL https://github.com/alfworld/alfworld/releases/download/0.4.2/json_2.1.3_tw-pddl.zip -o artifacts/games.zip
curl -fL https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q4_k_m.gguf -o artifacts/model.gguf
curl -fL https://github.com/ggml-org/llama.cpp/releases/download/b6700/llama-b6700-bin-ubuntu-x64.zip -o artifacts/server.zip
echo '5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf  artifacts/games.zip' | sha256sum -c
echo '74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db  artifacts/model.gguf' | sha256sum -c
echo 'a6327798efc93e5b6ba377b866fcc9fbab5eaed12002b31b2b19d780b748db1f  artifacts/server.zip' | sha256sum -c
unzip -q artifacts/games.zip -d artifacts/data
unzip -q artifacts/server.zip -d artifacts/server
python benchmark.py artifacts/data/json_2.1.1 artifacts/cases.json
```

Start the pinned CPU server in a separate shell from the same directory:

```sh
artifacts/server/build/bin/llama-server -m artifacts/model.gguf --host 127.0.0.1 \
  --port 8991 -c 6144 -np 8 -t 4 -tb 4 -b 512 -ub 512 --cont-batching --no-webui
```

Then, from the virtual environment:

```sh
python benchmark.py artifacts/data/json_2.1.1 artifacts/source.json --source-for artifacts/cases.json
python entropy.py artifacts/source.json artifacts/cases.json artifacts/calibration.json --score-cache artifacts/scores.sqlite
python pilot.py artifacts/cases.json artifacts/trials-entropy.json --calibration artifacts/calibration.json --score-cache artifacts/scores.sqlite
python analyze.py artifacts/trials-entropy.json artifacts/results-entropy.json
python pilot.py artifacts/cases.json artifacts/trials.json --score-cache artifacts/scores.sqlite
python analyze.py artifacts/trials.json artifacts/results.json
python -m unittest -v
```

The raw traces are regenerated locally; the compact checked-in results include each block's counts so the paired intervals are auditable. Use a fresh score-cache file if the model or runtime configuration changes. The runner uses the server's letter probabilities, not its sampled token: greedy selection for the sweep and paired seeded sampling for the largest-store temperature check. llama.cpp's exact-token prefix cache and parallel batching can change near-tie logits across machines or reruns; token accounting counts the entire logical prompt.
