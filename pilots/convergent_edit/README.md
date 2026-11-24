# HW1: Convergent-edit promotion

Can the number of task families that independently rediscover a harness edit predict how well it transfers? This pilot implements the experiment proposed in [HW1](https://github.com/manojbajaj95/cl/pull/20). The solver's weights are fixed. The evolver proposes one instruction after seeing a graded attempt; the task retries with that instruction in its system prompt, and the episode's overlay is discarded. The offline selector gets the traces, not the held-out labels.

- [API and GPU run sheet](API_RUN.md): models, exact commands, protocols, rollout and compute budget, and decision rules.
- [Results](results.md): local and deterministic smoke evidence. Neither substitutes for an API-class run.

## Run locally

From the repository root with Python 3.10+:

```sh
python3 -m pip install -r pilots/convergent_edit/requirements.txt
python3 -m unittest -v pilots.convergent_edit.test_pilot pilots.convergent_edit.test_backends
python3 -m pilots.convergent_edit.pilot --backend stub --output hw1-stub.json
```

For a real CPU smoke run, build `llama-server` from [llama.cpp](https://github.com/ggml-org/llama.cpp) and download the [Qwen2.5-0.5B-Instruct Q4_K_M GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF). In one shell:

```sh
llama-server -m /path/to/qwen2.5-0.5b-instruct-q4_k_m.gguf \
  --alias qwen2.5-0.5b-instruct --port 8080 --parallel 16 -c 32768 -t 8 --no-webui
```

In another shell:

```sh
python3 -m pilots.convergent_edit.pilot --backend local --held-out-tasks 8 \
  --validation-blocks 1 --output hw1-local.json
```

Here a single local model serves both roles behind distinct interfaces; only the evolver can write edits. The shortened CPU run retains all 90 discovery tasks and all three seeds, but uses 8 instead of 30 unseen tasks and, if the gate allows, 9 instead of 27 validation pairs per cluster. The stub simulates accuracy using seeded hashes; its scores and correlations are pipeline checks rather than evidence for or against HW1.

## Limits

All tasks are generated, text-only, objectively graded microbenchmarks, not the larger agent benchmarks named as examples in the proposal. Lexical clusters miss some paraphrases and can mix near-identical instructions with different meanings. LOFO controls edit text and scoring within each fold on a common candidate universe; it does not independently rerun discovery for each fold. The ACE and CHASE arms are explicitly scoped proxies. Bootstraps are conditional on the chosen families and seeds rather than uncertainty over future family or model draws.
