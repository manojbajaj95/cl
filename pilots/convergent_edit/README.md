# HW1: Convergent-edit promotion

Can the number of task families that independently rediscover a harness edit predict how well it transfers? This pilot implements the experiment proposed in [HW1](https://github.com/manojbajaj95/cl/pull/20). The solver's weights are fixed. The evolver proposes one instruction after seeing a graded attempt; the task retries with that instruction in its system prompt, and the episode's overlay is discarded. The offline selector gets the traces, not the held-out labels.

- [API and GPU run sheet](API_RUN.md): models, exact commands, protocols, rollout and compute budget, and decision rules.
- [Results](results.md): calibration, local and OpenRouter variance gates, and a deterministic integration check.

## Run locally

From the repository root with Python 3.10+:

```sh
python3 -m pip install -r pilots/convergent_edit/requirements.txt
python3 -m unittest -v pilots.convergent_edit.test_pilot pilots.convergent_edit.test_backends
python3 -m pilots.convergent_edit.pilot --backend stub --output hw1-stub.json
```

For a real CPU smoke run, build `llama-server` from [llama.cpp](https://github.com/ggml-org/llama.cpp). Serve the fixed [Qwen3-0.6B Q8_0 GGUF](https://huggingface.co/Qwen/Qwen3-0.6B-GGUF) in one shell:

```sh
llama-server -m /path/to/Qwen3-0.6B-Q8_0.gguf --alias qwen3-0.6b \
  --port 8082 --parallel 16 -c 32768 -t 8 --reasoning off --no-webui
```

Serve the [Qwen2.5-1.5B-Instruct Q4_K_M evolver](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF) in a second shell:

```sh
llama-server -m /path/to/qwen2.5-1.5b-instruct-q4_k_m.gguf --alias qwen2.5-1.5b-instruct \
  --port 8081 --parallel 16 -c 32768 -t 8 --no-webui
```

In a third shell:

```sh
python3 -m pilots.convergent_edit.calibration --cache hw1-calibration.cache.sqlite3
python3 -m pilots.convergent_edit.semantic
python3 -m pilots.convergent_edit.pilot --backend local --held-out-tasks 24 \
  --validation-blocks 1 --gate-only --output hw1-local.json
```

The task solver uses constrained decoding over exactly the displayed choices, with the same constraint for every arm. The CPU run retains all 90 discovery tasks and all three seeds, but uses 24 instead of 30 unseen tasks and, if the gate allows a follow-on, 9 instead of 27 validation pairs per cluster. The stub simulates accuracy using seeded hashes; its scores and correlations are pipeline checks rather than evidence for or against HW1.

## Limits

All tasks are generated, text-only, objectively graded microbenchmarks, not the larger agent benchmarks named as examples in the proposal. The three-choice format makes a 33% random baseline possible and should not be mistaken for broad task competence. Embedding clusters can miss paraphrases or group related but inequivalent instructions. LOFO controls edit text and scoring within each fold on a common candidate universe; it does not independently rerun discovery for each fold. The ACE and CHASE arms are explicitly scoped proxies. Bootstraps are conditional on the chosen families and seeds rather than uncertainty over future family or model draws.
