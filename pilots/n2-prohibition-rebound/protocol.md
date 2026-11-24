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
python3 run.py collect raw.csv
python3 run.py report raw.csv
python3 -m unittest discover -p 'test_*.py'
```

The collector uses llama-server's native tokenization and completion
endpoints. It verifies the legal action IDs, the two-action distribution
and the three distinct prompt lengths per probe. The CSV stores one row per wave/probe
(with both draws for each seed reconstructed from the recorded probabilities,
the fixed RNG algorithm and the seed).
