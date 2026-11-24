# HW1: API and GPU run sheet

The primary evolver is OpenRouter's **`nvidia/nemotron-3.5-lightning:free`** (30B MoE, 3B active, 1M context). Use **`nvidia/nemotron-3-ultra-550b-a55b:free`** as a stronger fallback only in a separately recorded run; never swap models halfway through a run or choose models, thresholds, seeds, or budgets on the basis of family 4.

## Experiment

- **Discovery:** 30 distinct generated tasks each in inventory, scheduling and routing. Tasks have small record sets and three integer choices; the correct position is randomized and balanced in every three-task block. Every episode starts from the same base harness. The evolver sees the abstract exercise shape, row count, whether the completion was among the options, and its grading direction, not the individual records, numeric completion or answer. This discourages copying task solutions into overlays. No request sees another family's task, edit, or grade, and no proposal is fed back into another request. The quota-saving configuration batches six tasks **within one family**. Same-request tasks are not strictly isolated, which can influence within-family repetition. Use `--proposal-batch-size 1` for strict per-task isolation. Solver discovery seeds are `(11, 29, 47)[task_index % 3] + 100 * family_index`; evolver requests add 1,000 times the first task's index to the appropriate task or batch seed to keep distinct episodes from sharing cached proposals.
- **Clustering:** Complete-link cosine similarity of locally computed BGE-small-en-v1.5 embeddings at 0.72, with guards for mismatched numerals or units, explicit opposite operations, and pairs that name different task-specific operations. Use the observed medoid; ties go to the lexically first edit. The [hand-labeled audit](clustering_audit.json) identifies 7/10 paraphrases and rejects 11/11 nonmatches, including three false merges found during local cluster inspection and used to refine the guards before scoring. Do not tune against held-out gains. Report the cluster count and the number spanning two or more families, and inspect the multi-family clusters for false merges.
- **Truth and gate first:** Calibrate the fixed solver on disjoint tasks (indices 1000–1023) before touching evaluation. The fourth family is eligibility (30 unseen tasks by default; minimum **24**). Stop if held-out base exact match is outside **30–60%**. Compare each canonical instruction added alone to the base against the base on identical tasks with seeds **11, 29, 47**. Truth is mean paired exact-match change. Estimate seed variance as the average within-cluster variance of the three seed-level gains; estimate between-cluster variance as the variance of cluster means minus one-third of seed variance, floored at zero. Run selection only if there are at least **40 clusters**, breadth has variation including a multi-family cluster, and between-cluster variance exceeds seed variance. Report the ratio and difference with 2,000 cluster-bootstrap percentile CIs conditional on the seeds; the gate uses point estimates.

If the gate passes, each arm gets **27 pairs / 54 logical task-model rollouts per cluster** at the default three validation blocks (9 pairs per seed). Identical request payloads at the same endpoint reuse the same sampled response via the cache, so actual network calls can be fewer. All arms start from the same logs and candidate pool; none can see family 4, even though truth is measured first.

| Arm | What happens in each seed |
|---|---|
| Breadth (HW1) | Rank by the number of independently rediscovering training families. Only clusters present in at least two families can be promoted. The matched 9 validation pairs are run blind to the selector. |
| Leave-one-family-out (LOFO) | For each eligible validation family, use a medoid drawn only from traces originating in the other families. Split the 9 paired comparisons across eligible folds, averaging paired exact-match gains. The candidate identities are aligned to the shared clusters for the rho comparison; the validation-family traces do not supply edit text for their fold. |
| Bad Genius-style counterfactual | Use 3 source-family validation tasks, each in standard, reversed record/field order, and indexed/question-first protocol. All three renderings preserve the same question and multiset of records; rank by the worst mean paired gain across protocols. This fixed challenger is a small CHASE-inspired proxy, not a replication of adaptive challenger search. |
| Within-family frequency | Rank by the largest number of occurrences in any one training family. The matched 9 validation pairs are blinded. |
| ACE-style curator | Use the discovery traces as reflection evidence; the same evolver model scores each rule once on reusability, actionability, and observed regressions, with up to 30 entries per request in the quota-saving configuration. This is a rubric-based playbook selection proxy, not the full ACE update loop. The matched 9 validation pairs are blinded. |
| Plain continued evolution | In a pre-seeded shuffled candidate order, compare each edit added to the current shared harness vs. that incumbent on 9 pairs per seed. Rank by mean marginal gain; retain positive edits greedily, capped at 5. This uses the same edit stream rather than granting a new proposal budget. |

Draw validation tasks outside each cluster's source task IDs where possible. A pair changes only the harness, holding task, seed, protocol and model fixed. With the standard settings, the counterfactual repeats each underlying task under three protocols rather than letting one arm spend more completions. Each arm's final harness (up to 5 edits) is then tested on the same paired family-4 panel. Report Spearman rho with shared cluster bootstrap 95% CIs, paired breadth-minus-control rho CIs, and top-k accuracy gains with task-bootstrap 95% CIs conditional on seeds. Do not treat degenerate constant-score correlations as wins. **Keep** only if breadth's point-estimate rho beats every control and beats LOFO by **more than 0.10**; otherwise **kill**. Top-k gain is a separate sanity check, not a replacement for the stated rho criterion.

## Setup and exact commands

Use Python 3.10+ at the repository root:

```sh
python3 -m pip install -r pilots/convergent_edit/requirements.txt
```

Keep the task model fixed across runs. The [measured CPU setup](README.md) uses **Qwen3-0.6B Q8_0**, reasoning disabled, with constrained decoding over the displayed integer choices. For a GPU replication, use **Qwen3-0.6B** (BF16) and check calibration again before measuring gains:

```sh
vllm serve Qwen/Qwen3-0.6B --served-model-name hw1-task --dtype bfloat16 \
  --default-chat-template-kwargs '{"enable_thinking":false}' \
  --max-model-len 4096 --max-num-seqs 16 --port 8000
```

On the client set `TASK_BASE_URL=http://127.0.0.1:8000/v1` (or the cluster URL) and `TASK_MODEL=hw1-task` as below. The solver endpoint must support OpenAI-compatible integer-enum JSON-schema decoding (`TASK_CONSTRAIN_CHOICES=1`, the default). Optional `TASK_API_KEY` adds task-worker bearer auth. Endpoints should honor `seed`, `temperature`, and `max_tokens`. Provider seeding is best-effort; record provider/model revision, server versions, model precision and any seed limitations.

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
python3 -m pilots.convergent_edit.calibration --cache hw1-calibration.cache.sqlite3
python3 -m pilots.convergent_edit.semantic
```

**Primary OpenRouter run** (export `OPENROUTER_API_KEY` from your secret store first). Optional `OPENROUTER_HTTP_REFERER` and `OPENROUTER_X_TITLE` set the attribution headers. The endpoint and model below are the `--backend api` defaults. The client requests reasoning disabled for OpenRouter Nemotron models to preserve the short edit/output budget.

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=https://openrouter.ai/api/v1 EVOLVER_MODEL=nvidia/nemotron-3.5-lightning:free \
EVOLVER_MAX_REQUESTS=18 python3 -m pilots.convergent_edit.pilot --backend api \
  --proposal-batch-size 6 --curation-batch-size 30 --gate-only --output hw1-lightning-v2.json
```

If the gate passes, repeat without `--gate-only` using the same output and cache. For an existing cache with 30 Lightning attempts and at most 18 more authorized, use `--cache /persistent/path/prior-lightning.json.cache.sqlite3` and the cumulative cap `EVOLVER_MAX_REQUESTS=48`. The cap counts all HTTP attempts for that evolver in that cache, including retries, and survives process restarts. It defaults to 0 (no client cap); a killed process immediately after reservation can make the count conservatively high. A changed task or proposal prompt invalidates its response cache key, not the attempt count.

The V2 pilot used the CPU task worker from the [README](README.md) and 24 held-out tasks. To resume that exact run in the pilot workspace, use:

~~~sh
TASK_BASE_URL=http://127.0.0.1:8082/v1 TASK_MODEL=qwen3-0.6b TASK_CONSTRAIN_CHOICES=1 \
EVOLVER_BASE_URL=https://openrouter.ai/api/v1 EVOLVER_MODEL=nvidia/nemotron-3.5-lightning:free \
EVOLVER_MAX_REQUESTS=48 python3 -m pilots.convergent_edit.pilot --backend api \
  --held-out-tasks 24 --proposal-batch-size 6 --curation-batch-size 30 --gate-only \
  --cache /home/ubuntu/hw1-lightning-gate.json.cache.sqlite3 --output /home/ubuntu/hw1-lightning-v2.json
~~~

**OpenRouter fallback** (separate output and cache):

```sh
TASK_BASE_URL=http://127.0.0.1:8000/v1 TASK_MODEL=hw1-task \
EVOLVER_BASE_URL=https://openrouter.ai/api/v1 EVOLVER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free \
EVOLVER_MAX_REQUESTS=18 python3 -m pilots.convergent_edit.pilot --backend api \
  --proposal-batch-size 6 --curation-batch-size 30 --gate-only --output hw1-ultra.json
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

Let `E` be accepted edit texts from 90 episodes, `C` the resulting clusters, and `H` the held-out tasks. Discovery: 15 batched evolver requests (90 unbatched) and `90 + E` task calls. Truth: `3H(C+1)` task calls, reusing the paired base once. After a passing gate only: `ceil(C/30)` batched evolver curator requests (`C` unbatched), `324C` task calls for six arms' selection, and `18H` task calls for six final harnesses. No second discovery stream or ground-truth traffic is charged to a selector. Counts below assume `H=30` and exclude cache hits and retries.

| Gate passes, assuming E = 90 | C = 40 | C = 90 |
|---|---:|---:|
| Evolver requests, primary batch sizes (6 / 30) | 17 | 18 |
| Evolver requests, unbatched | 130 | 180 |
| Estimated evolver input / output tokens | 52.3k / 2.68k | 73.8k / 2.88k |
| Task-model calls | 17,370 | 38,070 |
| Estimated task-model input / output tokens | 5.56M / 139k | 12.18M / 305k |
| OpenRouter free evolver API cost | $0 | $0 |
| GPT-4o-mini evolver API cost | ~$0.009 | ~$0.013 |
| Qwen2.5-72B evolver API cost | ~$0.020 | ~$0.028 |

At these cluster counts a completed variance gate stops at **15** batched (or **90** unbatched) evolver requests and 3,870–8,370 logical task calls with 30 held-out tasks (3,132–6,732 at 24). Rough token assumptions for the unbatched paid configurations: 390/28 input/output per proposal, 430/4 per curator score, 320/8 per task call (longer prompts possible). Batching avoids repeated system prompts and adds JSON delimiters; task-model volumes do not change. Prices, per million input/output: [OpenAI](https://platform.openai.com/docs/pricing) $0.15/$0.60; [OpenRouter/DeepInfra](https://openrouter.ai/api/v1/models/qwen/qwen-2.5-72b-instruct/endpoints) budgeted at $0.36/$0.40. Confirm rates and availability before running; prices exclude GPU hosting of the task solver, retries and minimum billing.

Free-tier time estimate: a complete batched run uses **17–18 requests**, roughly one minute at 20 requests/minute, plus task work, latency and retries. The gate itself uses 15 requests. Within an 18-request allowance, the three spare attempts can cover retries or the two to three curator calls after a passing gate; they cannot cover both in every case. An unbatched run needs **3–4 daily quota windows** at 130–180 requests. OpenRouter's [documented limits](https://openrouter.ai/docs/api/reference/limits) depend on account credit purchases and are shared across free model variants. Resume after reset using the same cache and endpoint/model.

GPU planning estimate, not measured: for the task worker at an effective **10–50 requests/s** (including small, serially dispatched panels), 17k–38k requests take **0.10–1.06 GPU-hours** on one GPU, plus startup and idle time. Budget **1–2 GPU-hours** commonly billed on a reserved task worker, excluding multi-day quota idle. At **0.3–2 requests/s** the self-hosted 72B evolver's 130–180 calls take **0.02–0.17 worker-hours** of active processing or **0.07–0.67 active GPU-hours** with TP4; if kept up for the whole experiment, reserve **4–8 GPU-hours** at TP4 or **1–2** at TP1 for 32B. At an illustrative $2–$4/GPU-hour that is **$2–$8** for the task worker, plus **$8–$32** for a reserved TP4 evolver (or **$2–$8** for TP1). Cluster allocation, model loading, actual throughput and idle billing dominate the API charge. Capture observed wall time and token counts for decision-ready cost.
