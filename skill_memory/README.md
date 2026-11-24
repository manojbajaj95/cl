# Continual agent skill-memory testbed

Six memory policies and two no-memory controls share one mock API, action format,
verifier, and paired task stream. The runner needs Python 3.10+ and has no Python
dependencies. The scripted agent is for CI and debugging, not for comparing
research methods; it omits the entropy control because it has no token distribution.

[Qwen CPU pilot: results, intervals, and raw logs](results/qwen-cpu/README.md)

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

`--url` selects the llama-server chat-completions base URL and `--model`
selects the served model. The server must support post-sampling token
probabilities. Every action prompt asks for JSON without grammar masking; every
action uses top-20 sampling and at most 55 output tokens. Each seed has the same
task/probe ordering and RNG seeds across arms; each arm × seed starts with empty
memory.

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
| No lesson, entropy matched | Exactly the no-memory observation and write policy, with a single source-fitted temperature instead of the reference temperature | [Anomaly batch 1, PR #27](https://github.com/manojbajaj95/cl/pull/27): controls for changes to policy sharpness without any lesson content |
| Skill library | Embedding-retrieve one verified executable workflow; upsert after a successful run | [Voyager, 2305.16291](https://arxiv.org/abs/2305.16291): safe two-call DSL instead of JavaScript; no automatic curriculum |
| Skills over MCP | The model sees a catalog of goal descriptions and may invoke a skill by name; same successful-trace upserts as the library | [MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): in-process JSON-RPC `tools/list` and `tools/call`, no network transport or initialization handshake. The agent selects the tool via JSON and does not see the bound procedure |
| OpenSkill | Search a synthetic operator manual after attempting a workflow; publish a compiled recipe only if the independently provided public sandbox fixture agrees | [OpenSkill: Open-World Self-Evolution for LLM Agents, 2606.06741](https://arxiv.org/abs/2606.06741), not the rating system. A local document collection stands in for web search; fixed sandbox fixtures stand in for a synthesized verifier. The arm does not use the hidden score. This arm has extra public evidence by design |
| AutoSkill | Read with hybrid cosine/token overlap; extract durable operator coaching only, add new skill, discard duplicate, or version a corrected same-family skill | [AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution, 2603.01145](https://arxiv.org/abs/2603.01145), not MUSE-Autoskill. Structured teaching events stand in for user interaction; fixed extraction and merge rules replace separate LLM calls |
| Reflection | On failure, ask the same model to author one verbal lesson from the attempt and feedback; inject the three most recent lessons | [Reflexion, 2303.11366](https://arxiv.org/abs/2303.11366): feedback-to-episodic verbal memory across stream tasks; one extra generation per failure. Scripted mode records feedback but does not reason over prose |
| Knowledge Cards | Retrieve a structured workflow card with a concept, scope/invalidating condition, rule, provenance, and validation record; write only on verified success | Interprets the name as [Knowledge Cards: Structured Knowledge for AI Systems, 2608.26176](https://arxiv.org/abs/2608.26176), a schema rather than a continual agent. The mock workflow taxonomy and runtime replace the ontology and expert review |

Memory surface, retrieval policy, and source of update evidence are not all
matched, and Reflection incurs extra generations. The pilot is a
diagnostic, not a causal test of which component is best.

### Entropy control

All memory arms and plain no-memory sample actions at the reference temperature
`T=0.7`. Reflection lesson generation is greedy and does not enter the action
entropy target. The entropy-matched no-lesson control uses a single temperature
fitted to the **pooled** source memory-arm entropy, not to model accuracy or to
held-out entropies. This is one added control, not six per-arm controls.

1. In disjoint source seeds 101 and 103, run only the first two **pre-drift**
   waves. The first wave gives the memory arms their shared operator coaching;
   only the second wave's uncoached action outputs contribute to the fit.
2. For each action, compute the mean Shannon conditional token entropy in nats
   along the sampled prefix, using the complete post-sampling top-20 distribution
   at each reported token. Average actions, then equally weight memory arms.
   This measures token sampling entropy, not semantic entropy over API plans.
3. On the same uncoached source prompts, test no-memory temperatures in
   `[0.15, 0.35, 0.5, 0.7, 0.9, 1.15, 1.5]`, refine around the closest grid
   value twice, and freeze the temperature minimizing absolute source entropy
   error. Start every evaluation stream with new empty memory. Never fit on
   evaluation probes or pre-/post-drift evaluation steps.

Matching a pooled source average does not guarantee a match per arm or after
drift; the results report the source fit profile and held-out uncoached entropy.
The main effect comparison for **each** memory arm is its paired gain vs this
control, shown alongside its gain vs plain no-memory.

## Outputs and metrics

- `episodes.csv`: action, action-token entropy, first and final feedback, number of
  action attempts, phase, task identity, coaching flag, and success for each arm ×
  seed × episode.
- `results.json`: config, source entropy calibration, elapsed time, per-seed
  metrics, and aggregate statistics.
  Overall and uncoached online success exclude probes. Cumulative gain is the
  net number of additional successes vs. each no-memory control on the paired stream.
- `curves.json`: per-step success and cumulative successes, both absolute and
  paired gains vs. both no-memory controls. Probes do not consume online steps.
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
