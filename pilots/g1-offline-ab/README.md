# G1 · Offline A/B of agent memory edits

## Effective sample size first

**0/30 lessons fell below ESS 50.** Terminal Kish ESS (of 500) was
**319.3 min / 434.8 median / 459.0 max**, with bootstrap 95% CIs
[295.5, 345.3] / [424.6, 444.1] / [453.0, 466.5], respectively.
[Results](results.json) give all 30 lessons' prefix ESS and CIs in lesson
file order. On average, 0.57 of the three sampled decisions per trajectory
had an absolute log-ratio above 0.1 (per-lesson means ranged 0.30–2.49).

## Verdict: KILL

DR missed the 0.60 rank threshold and trailed the likelihood control
instead of beating it by 0.15. It cleared the judge margin and beat the
uplift model on point estimates, but those margins are uncertain.

| Ranking method | Spearman vs fresh success | 95% CI | DR minus method (95% CI) |
| --- | ---: | ---: | ---: |
| Per-decision DR | 0.325 | [−0.244, 0.642] | — |
| Per-decision IS | 0.242 | [−0.277, 0.610] | — |
| Self-normalized per-decision IS | 0.290 | [−0.277, 0.615] | — |
| Success-minus-failure log-likelihood gain | 0.369 | [−0.227, 0.640] | −0.044 [−0.309, 0.264] |
| LLM judge | 0.058 | [−0.428, 0.500] | +0.267 [−0.485, 0.778] |
| UpliftMem-style learned uplift | −0.318 | [−0.661, 0.372] | +0.643 [−0.295, 1.072] |

The log succeeded on 185/500 runs (37%). Observed fresh success ranged
from 28% to 44% across lessons; 50 runs per lesson leave the truth ranking
noisy. The 2,000 bootstrap replicates propagate trajectory and lesson
uncertainty (judge conditional on the fixed log summary). This kills the
pilot at the prespecified point-estimate gates; it does not establish
that DR is inherently worse than the likelihood control.

## Pilot

One CPU agent (Qwen2.5-1.5B-Instruct, Q4_K_M) logs 500 episodes of a
three-checkpoint router task. Each tool choice is a single token; the next
code depends on the choice. We re-score the logged choices under 30 frozen
lesson prompts, rank the resulting policies with zero new episodes, and
compare the ranking to 50 independently sampled fresh episodes per lesson.
The fresh runs share randomly drawn starting codes, not action draws.
[Protocol](protocol.md) · [Frozen lessons](lessons.json)

### Scope

The ratios are exact for the legal-token policy at temperature 1. This is
a favorable, fixed three-decision setting, not a test of long-horizon,
unconstrained agent generation. The finite observation space lets us cache
logits, but live validation still samples new trajectories. The agent
observes the current code and checkpoint; the fitted Q model abstracts
away earlier choices. With terminal-only reward, uncorrected PDIS reduces
to trajectory IS; DR includes corrections at all three decisions.

The UpliftMem-style comparator is advantaged: it fits observed paired
memory/no-memory success differences on other lessons' fresh rollouts
(five-fold cross-fitting by lesson), never on the scored lesson's own
outcomes. A no-memory-only corpus cannot supply those direct uplift labels.
This is not a full UpliftMem retrieval-policy reproduction.

### Reproduce

Commands below run from this directory. The 1.5B model was run entirely on
CPU via llama.cpp; the download is about 1.1 GB. The runner checks the
pinned checkpoint's SHA-256.

```sh
python -m pip install -r requirements.txt
MODEL="$HOME/qwen2.5-1.5b-instruct-q4_k_m.gguf"
curl -fL 'https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf' -o "$MODEL"
export OPENBLAS_NUM_THREADS=1
python agent.py offline "$MODEL" --threads 4
python analysis.py --ess-only
python agent.py fresh "$MODEL" --threads 4
python analysis.py --bootstrap 2000
python -m unittest discover
```

The checked-in [offline data](offline.npz) contain states (zero-based code
offset from 10), actions (A/B/C = 0/1/2), per-token behavior log-probabilities,
terminal rewards and legal-token log-probability tables (baseline first).
The [fresh data](fresh.npz) contain the analogous trajectories for each
lesson and the judge's rating-token log-probabilities. Re-run only
`analysis.py` to regenerate [results.json](results.json) without a model.

### Related work

- [ADWM](https://arxiv.org/abs/2606.05558) simulates agent/environment
  transitions with a learned world model.
- [OTROPE](https://arxiv.org/abs/2609.36264) uses semantic transport and
  proxy residuals without behavior/target token likelihoods.
- [Amortized OPE](https://arxiv.org/abs/2610.10848) trains a prior-data
  fitted evaluator for contextual bandits under policy and reward shifts.
- [UpliftMem](https://arxiv.org/abs/2609.36805) learns set-level memory
  uplift from paired executions with and without retrieved memory.
