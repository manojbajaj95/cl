# Ask when stuck: ALFWorld pilot

Does delivering a question-indexed atom **after a simulator failure** make memory growth less harmful than putting the same atoms in the initial prompt? Does an equally provisioned model-confidence gate do just as well?

[Frozen protocol](protocol.md) · [Greedy results](results.json) · [Temperature-control results](results-entropy.json)

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
  --port 8991 -c 12288 -np 16 -t 8 -tb 8 --cont-batching --no-webui
```

Then, from the virtual environment:

```sh
python pilot.py artifacts/cases.json artifacts/trials.json
python analyze.py artifacts/trials.json artifacts/results.json
python benchmark.py artifacts/data/json_2.1.1 artifacts/source.json --source-for artifacts/cases.json
python entropy.py artifacts/source.json artifacts/cases.json artifacts/calibration.json
python pilot.py artifacts/cases.json artifacts/trials-entropy.json --calibration artifacts/calibration.json
python analyze.py artifacts/trials-entropy.json artifacts/results-entropy.json
python -m unittest -v
```

The raw traces are regenerated locally; the compact checked-in results include each block's counts so the paired intervals are auditable. The runner uses the server's letter probabilities, not its sampled token: greedy selection for the sweep and paired seeded sampling for the largest-store temperature check. llama.cpp's exact-token prefix cache and parallel batching can change near-tie logits across machines or reruns; token accounting counts the entire logical prompt.
