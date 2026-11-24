# HW1: API and GPU run sheet

The primary evolver is OpenRouter's **`nvidia/nemotron-3.5-lightning:free`** (30B MoE, 3B active, 1M context). Use **`nvidia/nemotron-3-ultra-550b-a55b:free`** as a stronger fallback only in a separately recorded run; never swap models halfway through a run or choose models, thresholds, seeds, or budgets on the basis of family 4.

## Experiment

- **Discovery:** 30 distinct generated tasks each in inventory, scheduling and routing. Every episode starts from the same base harness. The evolver proposes one local instruction per task based on its initial completion and grade. The task model retries with the instruction; only the trace persists. No request sees another family's task, edit, or grade; no proposal is fed back into other proposal requests. The quota-saving primary configuration batches three tasks **within one family** in each proposal request, prompting the model to diagnose the entries separately. Same-request tasks are not strictly isolated, which can influence within-family repetition. Use `--proposal-batch-size 1` for strict per-task isolation. The solver's discovery seeds are `(11, 29, 47)[task_index % 3] + 100 * family_index`; batched requests use the same cycle on family-local batch indices.
- **Clustering:** Sort unique edit texts and use complete-link multiset Jaccard at 0.78 with separate numeric literals; pick the observed medoid (lexical tie-break). This is a deliberately conservative lexical proxy for functional equivalence. The JSON audit preserves edits and origin tasks. Do not lower the threshold to get more breadth or split clusters to get to 40.
- **Truth and gate first:** The fourth family is eligibility (30 unseen tasks). For each cluster, compare its canonical instruction added alone to the fixed base against the base on identical tasks with seeds **11, 29, 47**. Ground truth is mean paired exact-match change. Estimate seed variance as the average within-cluster variance of the three seed-level gains; estimate between-cluster variance as the variance of cluster means minus one-third of the seed variance, floored at zero. Stop before running any selection arms unless there are at least **40 clusters** and the between-cluster variance exceeds seed variance. Report the variance ratio and difference with 2,000 cluster-bootstrap percentile CIs (conditional on the three seeds); the gate uses the point estimate, not the CI. Zero denominator makes the ratio unavailable; the difference still determines the gate.

If the gate passes, each arm gets **27 pairs / 54 logical task-model rollouts per cluster** at the default three validation blocks (9 pairs per seed). Identical request payloads at the same endpoint reuse the same sampled response via the cache, so actual network calls can be fewer. All arms start from the same logs and candidate pool; none can see family 4, even though truth is measured first.

| Arm | What happens in each seed |
|---|---|
| Breadth (HW1) | Rank by the number of independently rediscovering training families. Only clusters present in at least two families can be promoted. The matched 9 validation pairs are run blind to the selector. |
| Leave-one-family-out (LOFO) | For each eligible validation family, use a medoid drawn only from traces originating in the other families. Split the 9 paired comparisons across eligible folds, averaging paired exact-match gains. The candidate identities are aligned to the shared clusters for the rho comparison; the validation-family traces do not supply edit text for their fold. |
| Bad Genius-style counterfactual | Use 3 source-family validation tasks, each in standard, reversed record/field order, and indexed/question-first protocol. All three renderings preserve the same question and multiset of records; rank by the worst mean paired gain across protocols. This fixed challenger is a small CHASE-inspired proxy, not a replication of adaptive challenger search. |
| Within-family frequency | Rank by the largest number of occurrences in any one training family. The matched 9 validation pairs are blinded. |
| ACE-style curator | Use the discovery traces as reflection evidence; the same evolver model scores each rule once on reusability, actionability, and observed regressions, with up to six entries per request in the primary configuration. This is a rubric-based playbook selection proxy, not the full ACE update loop. The matched 9 validation pairs are blinded. |
| Plain continued evolution | In a pre-seeded shuffled candidate order, compare each edit added to the current shared harness vs. that incumbent on 9 pairs per seed. Rank by mean marginal gain; retain positive edits greedily, capped at 5. This uses the same edit stream rather than granting a new proposal budget. |

Draw validation tasks outside each cluster's source task IDs where possible. A pair changes only the harness, holding task, seed, protocol and model fixed. With the standard settings, the counterfactual repeats each underlying task under three protocols rather than letting one arm spend more completions. Each arm's final harness (up to 5 edits) is then tested on the same paired family-4 panel. Report Spearman rho with shared cluster bootstrap 95% CIs, paired breadth-minus-control rho CIs, and top-k accuracy gains with task-bootstrap 95% CIs conditional on seeds. Do not treat degenerate constant-score correlations as wins. **Keep** only if breadth's point-estimate rho beats every control and beats LOFO by **more than 0.10**; otherwise **kill**. Top-k gain is a separate sanity check, not a replacement for the stated rho criterion.

## Setup and exact commands

Use Python 3.10+ at the repository root:

```sh
python3 -m pip install -r pilots/convergent_edit/requirements.txt
```

Keep the task model fixed across runs. Recommended: a separate vLLM worker running **Qwen2.5-0.5B-Instruct** (BF16); the [CPU smoke setup](README.md) is also available, but freeze the precision and serving configuration within a comparison.

```sh
vllm serve Qwen/Qwen2.5-0.5B-Instruct --served-model-name hw1-task \
  --dtype bfloat16 --max-model-len 4096 --max-num-seqs 16 --port 8000
```

On the client set `TASK_BASE_URL=http://127.0.0.1:8000/v1` (or the cluster URL) and `TASK_MODEL=hw1-task` as below. Optional `TASK_API_KEY` adds task-worker bearer auth. The client expects OpenAI-compatible `/chat/completions`, honoring `seed`, `temperature`, and `max_tokens`. Provider seeding is best-effort; record provider/endpoint/model revision, server versions, model precision and any provider seed limitations with results.

**Primary OpenRouter run** (export `OPENROUTER_API_KEY` from your secret store first). Optional `OPENROUTER_HTTP_REFERER` and `OPENROUTER_X_TITLE` set the attribution headers. The endpoint and model below are the `--backend api` defaults. The client requests reasoning disabled for OpenRouter Nemotron models to preserve the short edit/output budget.

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=https://openrouter.ai/api/v1 EVOLVER_MODEL=nvidia/nemotron-3.5-lightning:free \
EVOLVER_MAX_REQUESTS=40 python3 -m pilots.convergent_edit.pilot --backend api \
  --proposal-batch-size 3 --curation-batch-size 6 --gate-only --output hw1-lightning.json
```

If the gate passes, repeat without `--gate-only` using the same output and cache. Set `EVOLVER_MAX_REQUESTS` high enough to accommodate cached attempts plus the required new curation calls and any retry headroom, but no higher than the confirmed quota across the planned windows. The cap counts all HTTP attempts for that evolver in that cache, including retries, and survives process restarts. It defaults to 0 (no client cap); a killed process immediately after reservation can make the count conservatively high.

**OpenRouter fallback** (separate output and cache):

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=https://openrouter.ai/api/v1 EVOLVER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free \
EVOLVER_MAX_REQUESTS=40 python3 -m pilots.convergent_edit.pilot --backend api \
  --proposal-batch-size 3 --curation-batch-size 6 --gate-only --output hw1-ultra.json
```

HTTP 429 and 5xx retry with exponential backoff and jitter, honoring `Retry-After`; if asked to wait over 300 seconds or the retry budget runs out, the client exits so you can resume. The free variants default to 20 requests/minute per evolver client. Override with `EVOLVER_REQUESTS_PER_MINUTE` (0 disables spacing) and `EVOLVER_MAX_RETRIES` (default 5). **Resume by repeating the same command** with the same persistent working directory. Each successful response is checkpointed immediately in `OUTPUT.cache.sqlite3` by SHA-256 of endpoint and request body, without storing keys; `--cache /persistent/path/run.sqlite3` overrides the location. Preserve that file across quota windows and don't share it across independent replications. The final JSON is emitted only after the run finishes or the gate stops.

**Hosted GPT-4o-mini** (export `EVOLVER_API_KEY` from your secret store first):

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=https://api.openai.com/v1 EVOLVER_MODEL=gpt-4o-mini-2024-07-18 \
python3 -m pilots.convergent_edit.pilot --backend api --output hw1-gpt4o-mini.json
```

**Hosted Qwen2.5-72B** (uses `OPENROUTER_API_KEY`; OpenRouter model ID shown):

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=https://openrouter.ai/api/v1 EVOLVER_MODEL=qwen/qwen-2.5-72b-instruct \
python3 -m pilots.convergent_edit.pilot --backend api --output hw1-qwen72b-api.json
```

**Self-hosted Qwen2.5-72B**: start the task worker above, then start the separate evolver worker. A lower-cost open-model replication can swap in `Qwen/Qwen2.5-32B-Instruct` and `--tensor-parallel-size 1` on an 80 GB GPU, or TP2 if cache headroom is limited. The client is identical and needs no credentials on private unsecured endpoints.

```sh
vllm serve Qwen/Qwen2.5-72B-Instruct --served-model-name hw1-evolver \
  --dtype bfloat16 --tensor-parallel-size 4 --max-model-len 4096 --max-num-seqs 16 --port 8001
```

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=http://127.0.0.1:8001/v1 EVOLVER_MODEL=hw1-evolver \
python3 -m pilots.convergent_edit.pilot --backend api --output hw1-qwen72b-vllm.json
```

## Calls, tokens and compute per run

Let `E` be accepted edit texts from 90 episodes and `C` the resulting clusters. Discovery: 30 batched evolver requests (90 unbatched) and `90 + E` task calls. Truth: `90(C+1)` task calls, reusing the paired base once. After a passing gate only: `ceil(C/6)` batched evolver curator requests (`C` unbatched), `324C` task calls for six arms' selection, and 540 task calls for six final harnesses. No second discovery stream or ground-truth traffic is charged to a selector. Counts below are logical requests before cache hits and exclude retries.

| Gate passes, assuming E = 90 | C = 40 | C = 90 |
|---|---:|---:|
| Evolver requests, primary batch sizes (3 / 6) | 37 | 45 |
| Evolver requests, unbatched | 130 | 180 |
| Estimated evolver input / output tokens | 52.3k / 2.68k | 73.8k / 2.88k |
| Task-model calls | 17,370 | 38,070 |
| Estimated task-model input / output tokens | 5.56M / 139k | 12.18M / 305k |
| OpenRouter free evolver API cost | $0 | $0 |
| GPT-4o-mini evolver API cost | ~$0.009 | ~$0.013 |
| Qwen2.5-72B evolver API cost | ~$0.020 | ~$0.028 |

At these cluster counts a failed gate stops at **30** batched (or **90** unbatched) evolver requests and 3,870–8,370 task calls. Rough token assumptions for the unbatched paid configurations: 390/28 input/output per proposal, 430/4 per curator score, 320/8 per task call (longer prompts possible). Batching avoids repeated system prompts and adds JSON delimiters; task-model volumes do not change. Prices, per million input/output: [OpenAI](https://platform.openai.com/docs/pricing) $0.15/$0.60; [OpenRouter/DeepInfra](https://openrouter.ai/api/v1/models/qwen/qwen-2.5-72b-instruct/endpoints) budgeted at $0.36/$0.40. Confirm rates and availability before running; prices exclude GPU hosting of the task solver, retries and minimum billing.

Free-tier time estimate: a complete batched run uses **37–45 requests**, roughly **1.9–2.3 minutes** at 20 requests/minute, plus task work, latency and retries. The gate itself uses 30 requests. A fresh 50-request daily quota can fit one batched run with 5–13 requests of headroom; an unbatched run needs **3–4 daily quota windows** at 130–180 requests. OpenRouter's [documented limits](https://openrouter.ai/docs/api/reference/limits) depend on account credit purchases and are shared across free model variants; provider capacity and quotas may change. Resume after reset rather than leaving expensive task workers idle for days; bring them back at the same endpoint/model so the cache still hits.

GPU planning estimate, not measured: for the task worker at an effective **10–50 requests/s** (including small, serially dispatched panels), 17k–38k requests take **0.10–1.06 GPU-hours** on one GPU, plus startup and idle time. Budget **1–2 GPU-hours** commonly billed on a reserved task worker, excluding multi-day quota idle. At **0.3–2 requests/s** the self-hosted 72B evolver's 130–180 calls take **0.02–0.17 worker-hours** of active processing or **0.07–0.67 active GPU-hours** with TP4; if kept up for the whole experiment, reserve **4–8 GPU-hours** at TP4 or **1–2** at TP1 for 32B. At an illustrative $2–$4/GPU-hour that is **$2–$8** for the task worker, plus **$8–$32** for a reserved TP4 evolver (or **$2–$8** for TP1). Cluster allocation, model loading, actual throughput and idle billing dominate the API charge. Capture observed wall time and token counts for decision-ready cost.
