# HW1 pilot results

The original eight-task runs **did not constitute a valid test**: the held-out solver scored 0/24, and lexical clustering did not yield a usable breadth signal. The revised pilot below tests variance after correcting both issues. See [API_RUN.md](API_RUN.md) for the protocol.

## V2 calibration and clustering audit

Using Qwen3-0.6B Q8_0 on llama.cpp with reasoning disabled and decoding constrained to the three displayed integer choices, the frozen baseline on 24 **disjoint calibration tasks per family** (indices 1000–1023) was:

| Family | Correct |
|---|---:|
| Inventory | 9/24 (37.5%) |
| Schedule | 11/24 (45.8%) |
| Routing | 7/24 (29.2%) |
| Eligibility | 10/24 (41.7%) |

The choice position is balanced within three-task blocks. Rates close to three-choice chance should not be interpreted as evidence of reliable reasoning. An earlier corrected candidate with Qwen2.5-0.5B still scored 16/72 on its unseen panel and produced no cross-family clusters with raw task data in the proposal prompt, so we stopped before variance scoring and did not spend any Lightning requests. The final configuration uses a new eligibility generator and a stronger constrained solver. The evolver now sees abstract episode evidence, not the individual records or numeric answer. Evaluation uses **24 held-out tasks × three seeds**.

We hand-labeled [21 candidate edit pairs](clustering_audit.json) before the corrected gate result: 10 paraphrases and 11 nonmatches. A first local clustering pass had three apparent cross-family clusters; on inspection each combined instructions about distinct operations (for example, within **10%** of an initial value versus greater than **10**). We added those negative examples and refined the conflict guards. Complete-link clustering with BGE-small-en-v1.5 at 0.72 recovered **7/10** paraphrases, with **0/11** false merges on this calibration sample. For example, “Verify which endpoints are included before applying a boundary condition” and “Check whether each bound is inclusive or exclusive before filtering” scored **0.722** and merge; counting rows and summing values do not. This is not an independent precision estimate.

## V2 variance gates

Both reruns use the same fixed solver (llama.cpp revision `d3c257a493b31cf06a4e724ab4648d6f1a3e5e1e`) and 24 unseen eligibility tasks × three seeds. The held-out baseline was **25/72 (34.7%)**, with **8/24, 8/24, 9/24** for seeds 11, 29, and 47.

**Local Qwen2.5-1.5B evolver:** 90 accepted edits formed **19 clusters**; **one** was labeled cross-family by the algorithm (18 single-family, 1 two-family). Manual inspection found that pair matched “Check if the result is the listed integer” with a schedule-specific instruction to check the count of qualifying intervals against the given integer. We do not count that as credible independent rediscovery. The between-cluster variance was **0.001965**, vs. **0.005543** seed variance: ratio **0.354** (95% CI **[0.031, 0.644]**) and variance difference 95% CI **[−0.006413, −0.001544]**. The local gate stopped on both cluster count and gain spread; no arms ran.

**OpenRouter Nemotron 3.5 Lightning:** After the local gate, Lightning reused the V1 SQLite cache and made **15 additional HTTP requests**, no retries (45 cumulative of the 48 authorized). Three of 15 responses did not parse as six-edit arrays; **72/90** tasks supplied accepted edits (inventory 30, schedule 24, routing 18). These yielded **22 clusters**, **seven** labeled cross-family by the algorithm (15 single-family, six two-family, one three-family). Inspection found related advice across families, such as checking that the category filter matches the source records, but also clear overmerges such as “Confirm initial quantity is read from the first row before any event adjustments” with “Confirm start values are inclusive and end values are exclusive.” The seven is an algorithmic count, not seven verified equivalents. The between-cluster variance was **0.000484**, vs. **0.003104** seed variance: ratio **0.156** (95% CI **[0.000, 0.475]**) and variance difference 95% CI **[−0.004261, −0.001150]**.

**Verdict: stop this configuration at the gate.** The solver is no longer at the floor: the best observed mean paired gain was **+9.72 pp** locally and **+6.94 pp** on Lightning. But neither run reached 40 clusters or had gain spread that exceeded seed variance. Neither ran any selection arms, so these results do not establish whether breadth beats the controls. A fresh configuration should improve proposal validity/diversity and audit cross-family merges on training-only data before measuring another held-out panel.

## Original V1 runs, superseded

Local Qwen had ratio 0.122 (95% CI [0.007, 0.247]), 73 clusters and one cross-family cluster. Lightning had ratio 0.098 (95% CI [0.000, 0.258]), 72 clusters and no cross-family clusters. Both had zero baseline accuracy. Lightning V1 spent 30 requests; V2 reuses its SQLite cache and accounting, so the cumulative cap is 48 attempts rather than a fresh 48.

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
