# Continual agent skill-memory testbed

Seven memory policies share one mock API, action format, verifier, and paired task
stream. The runner needs Python 3.10+ and has no Python dependencies. The scripted
agent is for CI and debugging, not for comparing research methods.

## Run it

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -v
python -m skill_memory.run --output /tmp/skill-memory-smoke \
  --pre 8 --post 8 --seeds 11 23 --recovery-window 2
```

For a CPU model, build [llama.cpp](https://github.com/ggml-org/llama.cpp) with the
`llama-server` target and get
[`qwen2.5-1.5b-instruct-q4_k_m.gguf`](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF).
The server uses continuous batching; set thread and worker counts for the machine.

```sh
llama-server -m /path/to/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --host 127.0.0.1 --port 8085 --parallel 12 -c 12288 -t 8 -tb 8
python -m skill_memory.run --agent llm --workers 12 --pre 48 --post 48 \
  --seeds 11 23 37 53 71 --output "$HOME/skill-memory-qwen"
```

`--url` selects an OpenAI-compatible chat-completions base URL and `--model`
selects the served model. The pilot uses JSON mode for actions, temperature 0,
and up to 55 output tokens per generation. Each seed has the same task/probe
ordering and sampling seeds across arms; each arm × seed starts with empty memory.

## Protocol

- Each episode proposes two ordered tool calls; a third-party-style runtime supplies
  the episode entity as each call's argument value. The verifier rejects missing
  endpoints, wrong argument keys, and unmet prerequisites and checks the final
  workflow state. An MCP memory tool can submit the same two calls as one skill.
- Eight workflows appear before drift. At online step 49 (zero-based index 48
  at the default length), scanner, sensor, parcel, and badge leave the learning
  stream unchanged. Invoice and shipment remain active but each rename an
  endpoint and change argument keys; account and ticket remain active and stable.
  Each wave shuffles the participating families once and varies prompts/entities.
- The common registry includes a stable set of plausible, distractor, and obsolete
  endpoint/key pairs; the model is not given the drift step or current revision.
  All arms see the same operator recipe during the first pre-drift wave and
  second post-drift wave. The first post-drift wave is uncoached, so old behavior
  is tested before a correction is shown. The raw logs distinguish coached tasks.
- Predict, score, then write. Eight held-out entities from the four retired
  workflows are tested at the pre-drift checkpoint and again after the stream.
  Both evaluations use the same goals, entities, and decoding seeds, with no
  coaching and no memory writes. Retirement, not obsolete API usage, defines
  the old-skill probe cohort.

## Baselines

These are controlled, **mechanism-level adaptations**, not reproductions of the
original systems or comparable paper scores. Structured banks hold six entries,
evicting the oldest write, not the oldest read. Text retrieval uses fixed CPU
word/trigram hashing into a 256-dimensional embedding and cosine scoring.

| Arm | Reads and writes | Adaptation from source |
| --- | --- | --- |
| No memory | Common registry and current coaching only | Identical model, tools, and verifier; no cross-episode state |
| Skill library | Embedding-retrieve one verified executable workflow; upsert after a successful run | [Voyager, 2305.16291](https://arxiv.org/abs/2305.16291): safe two-call DSL instead of JavaScript; no automatic curriculum |
| Skills over MCP | The model sees a catalog of goal descriptions and may invoke a skill by name; same successful-trace upserts as the library | [MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): in-process JSON-RPC `tools/list` and `tools/call`, no network transport or initialization handshake. The agent selects the tool via JSON and does not see the bound procedure |
| OpenSkill | Search a synthetic operator manual after attempting a workflow; publish a compiled recipe only if the independently provided public sandbox fixture agrees | [OpenSkill: Open-World Self-Evolution for LLM Agents, 2606.06741](https://arxiv.org/abs/2606.06741), not the rating system. A local document collection stands in for web search; fixed sandbox fixtures stand in for a synthesized verifier. The arm does not use the hidden score. This arm has extra public evidence by design |
| AutoSkill | Read with hybrid cosine/token overlap; extract durable operator coaching only, add new skill, discard duplicate, or version a corrected same-family skill | [AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution, 2603.01145](https://arxiv.org/abs/2603.01145), not MUSE-Autoskill. Structured teaching events stand in for user interaction; fixed extraction and merge rules replace separate LLM calls |
| Reflection | On failure, ask the same model to author one verbal lesson from the attempt and feedback; inject the three most recent lessons | [Reflexion, 2303.11366](https://arxiv.org/abs/2303.11366): feedback-to-episodic verbal memory across stream tasks; one extra generation per failure. Scripted mode records feedback but does not reason over prose |
| Knowledge Cards | Retrieve a structured workflow card with a concept, scope/invalidating condition, rule, provenance, and validation record; write only on verified success | Interprets the name as [Knowledge Cards: Structured Knowledge for AI Systems, 2608.26176](https://arxiv.org/abs/2608.26176), a schema rather than a continual agent. The mock workflow taxonomy and runtime replace the ontology and expert review |

Memory surface, retrieval policy, and source of update evidence are not all
matched, and Reflection incurs extra generations. The seven-way pilot is a
diagnostic, not a causal test of which component is best.

## Outputs and metrics

- `episodes.csv`: action, first and final feedback, number of action attempts,
  phase, task identity, coaching flag, and success for each arm × seed × episode.
- `results.json`: config, elapsed time, per-seed metrics, and aggregate statistics.
  Overall and uncoached online success exclude probes. Cumulative gain is the
  net number of additional successes vs. no memory on the paired stream.
- `curves.json`: per-step success and cumulative successes, both absolute and
  paired gains vs. no memory. Probes do not consume online steps.
- `summary.md`: mean [95% percentile bootstrap interval] for the main metrics.
  Each draw resamples whole seeds, keeping arms paired when forming differences.
  Curves use pointwise, not simultaneous, intervals.

Forgetting = before minus after on the fixed probe set (positive is worse).
Post-drift AUC is the normalized area under the binary online success trace,
reported for all online post-drift tasks and for the two changed families only.
Recovery targets the last pre-drift window of changed-family success on the same
seed; the first complete post-drift window over those families to meet it sets
the recovery time, counted in all online post-drift tasks. Misses are censored;
the restricted mean (†) uses post length + 1 for misses and is reported next to
the recovered fraction. A low pre-drift target can make a weak arm look fast.

## Add another arm

Implement `Memory.read(task)` and `Memory.write(experience)` and register the class
in `ARMS` in [memory.py](memory.py). `read` produces text or named tools;
`invoke` maps a selected tool to the common DSL. `write` observes only completed
episodes and can call the supplied reflection or public-search callbacks.
For toolbox-vs-lessons, hold the underlying entries and tests fixed while varying
the read surface; for failure-triggered pull, make initial read empty and put
retrieval in the optional `after_failure(task, outcome)` hook (one retry max).
Compare with a matched-action-budget control; all shipped arms use one action
attempt per episode.
