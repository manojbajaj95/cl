# N2: prohibition rebound under memory accumulation

This is the smallest falsifying test in [N2](https://github.com/manojbajaj95/cl/pull/18),
not a test of its proposed attention mechanism.

* Freeze Qwen2.5-1.5B-Instruct Q4_K_M on CPU, 60 distinct queue/tool rules,
  their insertion order, 20 held-constant probe phrasings per wave-1 queue,
  and sampling seeds 17, 29 and 43. Each probe asks a router to choose
  tool A or B for a queue and names the queue's habitual (prohibited) tool.
  The habitual tool alternates across queues, giving five of each in wave 1.
  A matching memory rule takes priority over the habitual tool. This
  binary action space makes a positive rewrite logically equivalent to
  the corresponding prohibition. No queue is calibrated away after
  observing model behavior; report a no-rule baseline as a manipulation check.
* Append 10 rules per wave, oldest first. Repeat the same 200 wave-1
  probes per wave per seed. Text says `For QUEUE, never use BAD`.
  Rewrite says `For QUEUE, always use GOOD`. Measure and enforce
  equal prompt token counts. No-rule and logit-mask runs put inert slot
  markers in the memory block, matched to the same token budget; neither
  receives a textual rule. For a stored queue, the mask zeroes the
  prohibited action's softmax weight and renormalizes, equivalent to
  setting its logit to minus infinity before sampling. Here tool calls
  are single tokens, so there are no spelling or tokenizer bypasses.
* Take one forward pass per prompt. Sample two independent single-token
  proposals at temperature 1 with common random numbers across methods
  and waves for each seed/probe. Use the first draw except in the
  verifier arm: start from the same text policy, accept the first legal
  draw, otherwise accept the second if legal, otherwise abstain.
  Every method has the same logical input tokens, one next-token
  distribution and two draws, including the discarded second draw.
  A retry samples the cached distribution without a new model pass.
  This matches LM and draw budgets, not measured wall time; prefix
  caching and constant-time filtering can have different costs.
* Report the fraction of prohibited tool calls per attempted probe.
  For the verifier additionally report the fraction left unresolved
  after both draws (coverage = 1 minus that fraction). In this binary
  world every allowed action is correct; a mask's zero violation rate
  is by construction, and not evidence of a learned behavior.
* Primary contrasts in percentage points: text at wave 6 minus text
  at wave 1; rewrite at wave 6 minus mask at wave 6. Report paired
  95% percentile bootstrap intervals (10,000 replicates), resampling
  queues and phrasings within each selected queue, carrying all waves,
  arms and three seed draws along jointly. These intervals are
  conditional on the three fixed seeds, one order and one model.
  A zero-event bootstrap interval is degenerate; report a conservative
  one-sided exact 95% upper bound on the probability of any observed
  rewrite violation in a queue when there are zero events in all ten
  queues (under independent queue sampling).
* **KILL** if the text rise is below 5 pp, or if zero lies in the
  paired 95% interval for rewrite minus mask (the proposal's
  `matches ... within the CI` rule, not a formal equivalence claim).
  Otherwise **KEEP** for a richer pilot, not a general claim.

## Reproduction

Download [the official GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf).
SHA-256: `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.
Build llama.cpp at `66a3b01b0a243f119b144abfa7122b1677ea9114`, then:

```sh
llama-server --host 127.0.0.1 --port 8080 -m qwen2.5-1.5b-instruct-q4_k_m.gguf -ngl 0 -t 8 -tb 8 -np 16 -c 16384
python3 run.py collect reproduced.csv
python3 run.py report reproduced.csv
python3 -m unittest discover -p 'test_*.py'
```

The collector uses llama-server's native tokenization and completion
endpoints. It verifies the legal action IDs, the two-action distribution,
and the lengths of the three distinct prompts per probe. To reanalyze
the archived run without a model, use `python3 run.py report raw.csv`.
The CSV stores one row per wave/probe; both draws for each seed are
reconstructed from the recorded probabilities and fixed RNG algorithm.

## Reviewer-requested screened rerun

Keep the same model, 60 rules, order, six waves, and three sampling
seeds. Freeze the candidate pool in `rerun.py`: the original 20
phrasings followed by versions that make the habitual route explicit
without giving a new routing instruction. For each candidate, screen
on the exact next-action probability of its habitual tool in the
length-matched **no-rule** prompt. A candidate must have probability
at least 0.70 at every wave. Stop screening a candidate on its first
failed wave. Take the first 20 eligible phrasings per wave-1 queue in
candidate order (up to 200 probes); if a queue falls short, keep all
of its eligible phrasings and report the shortfall. Freeze selection
before querying any text-rule prompt.

Query only the negative text and no-rule arms; skip rewrite, mask
and verifier. Use fresh sampling draws (same seeds 17, 29 and 43,
with a rerun-specific probe key), paired across waves and arms.
Report exact screened baseline probabilities as well as sampled
baseline rates; selection does not use sampling draws. Use the prior
paired queue-and-phrasing bootstrap for 95% intervals, conditional on
the selected cohort, same model and fixed order. The final decision
uses text wave 6 minus text wave 1: **KILL and close N2 if the
increase is less than 5 pp**, otherwise **KEEP** for follow-up. The
gate is on the point estimate, with its 95% CI reported separately.

```sh
python3 rerun.py collect reproduced-screen.csv reproduced-rerun.csv
python3 rerun.py report rerun-raw.csv
```

`rerun-screen.csv` archives each no-rule score that was evaluated
before selection. `rerun-raw.csv` archives the selected prompts'
no-rule and negative-text probabilities at all six waves.
