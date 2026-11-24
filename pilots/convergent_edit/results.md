# HW1 pilot results

**Stop at the gate:** Neither live Lightning nor local Qwen produced held-out gain spread greater than seed variance on the initial CPU panel. The stub checks software paths only. See [API_RUN.md](API_RUN.md) for the full experiment and decision rule.

## Live OpenRouter Lightning gate

With `OPENROUTER_API_KEY` exported and the local task endpoint from the [README](README.md):

```sh
EVOLVER_MAX_REQUESTS=40 python3 -m pilots.convergent_edit.pilot --backend api \
  --proposal-batch-size 3 --curation-batch-size 6 --held-out-tasks 8 \
  --gate-only --output hw1-lightning-gate.json
```

The free **`nvidia/nemotron-3.5-lightning:free`** evolver returned **90 valid edits from exactly 30 successful HTTP requests** (no retries, no fallback, no paid calls). The task model stayed local: Qwen2.5-0.5B-Instruct Q4_K_M. All 90 discovery tasks ran; only the unseen panel was reduced from 30 to 8 tasks for CPU time, retaining seeds 11/29/47. The run took 14m39s, including overlap with the local run.

| Coverage and gate metric | Result |
|---|---:|
| Edit clusters | 72, all single-family |
| Base exact match (held out) | 0/24 |
| Range of cluster mean paired gains | 0 to +8.33 pp |
| Between-cluster gain variance | 0.000162 |
| Within-cluster seed variance | 0.001664 |
| Between/seed variance ratio [95% CI] | **0.098 [0.000, 0.258]** |
| Variance difference [95% CI] | **−0.001501 [−0.002160, −0.000906]** |

**Verdict: stop, not a rank-based kill.** Coverage passed but the variance gate failed; no selection arm was run. No cluster was eligible for breadth promotion at this threshold. The held-out solver returned all 24 answers in the required integer format but got none right, so this floor is not explained by output-format rejection. This does not establish what a better-calibrated solver or a larger held-out panel would show.

At the observed 72 clusters, a full run passing the gate would need **42** evolver requests (30 discovery + 12 curator) with batching or **162** unbatched (90 + 72, holding cluster count fixed), before retries. The 42-request budget fits a fresh ~50-request free window. No extra credits or live calls were used after this gate.

## Local Qwen CPU gate

Command: `python3 -m pilots.convergent_edit.pilot --backend local --held-out-tasks 8 --validation-blocks 1 --output hw1-local.json`. Both roles used Qwen2.5-0.5B-Instruct Q4_K_M on llama.cpp commit `d3c257a493b31cf06a4e724ab4648d6f1a3e5e1e` (8 CPU threads; 14m35s while also sharing the server with part of the Lightning run).

With 90 discovery tasks and 8 unseen tasks over seeds 11/29/47, **77 valid edits formed 73 clusters**; only one cluster had traces from more than one family. Base exact match on family 4 was **0/24**, and cluster mean gains ranged from 0 to +8.33 percentage points. Between-cluster variance was **0.000314**, vs. seed variance **0.002568**: ratio **0.122** (95% CI **[0.007, 0.247]**), difference **[−0.00312, −0.00155]**.

**Local verdict: stop at the variance gate.** No arm was scored; this is not a rank-based kill verdict for a stronger evolver or solver. The zero-accuracy solver and the small held-out panel limit external validity.

## Deterministic end-to-end integration check

Command: `python3 -m pilots.convergent_edit.pilot --backend stub --output hw1-stub.json`. With all 90 discovery tasks, 30 unseen tasks, and seeds 11/29/47, 90 valid edits formed **48 clusters**. Base exact match was **43.3%**. Between-cluster variance was **0.057643**, vs. seed variance **0.014444**: ratio **3.991** (95% CI **[2.670, 5.166]**), difference **[0.02412, 0.06018]**. The gate passed and all six arms executed at the same paired rollout budget.

| Arm | Spearman rho [95% CI] | Breadth minus arm rho [95% CI] | Final harness held-out gain, pp [95% CI] |
|---|---:|---:|---:|
| Breadth | 0.062 [−0.214, 0.340] | — | −3.33 [−24.44, 17.78] |
| LOFO paired validation | 0.878 [0.799, 0.916] | −0.816 [−1.084, −0.519] | 43.33 [25.56, 60.00] |
| Counterfactual filtering | 0.758 [0.576, 0.880] | −0.696 [−1.026, −0.349] | 53.33 [41.11, 64.44] |
| Within-family frequency | −0.228 [−0.510, 0.064] | 0.290 [−0.049, 0.610] | −10.00 [−28.89, 10.00] |
| ACE-style curator | 0.996 [0.989, 0.997] | −0.934 [−1.209, −0.655] | 53.33 [41.11, 64.44] |
| Continued evolution | 0.716 [0.535, 0.837] | −0.654 [−0.993, −0.279] | 33.33 [14.44, 51.11] |

**Integration result: synthetic kill.** The stub curator and stub task gains share the same hash, so the high curator rho is intentional for code-path coverage. Do not interpret this table as a real arm comparison.
