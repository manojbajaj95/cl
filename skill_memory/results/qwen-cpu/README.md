# Qwen CPU pilot

[Summary table with 95% seed bootstrap intervals](summary.md) · [Run metrics and
source calibration](results.json) · [Online curves](curves.json) · [Raw episodes](episodes.csv)

Qwen2.5-1.5B-Instruct Q4_K_M completed 4,480 episodes across eight arms and five
paired evaluation seeds (11, 23, 37, 53, 71), 48 online steps on either side of
drift and 16 retention probes per arm × seed. The run took 3,164 seconds
(52.7 minutes), including calibration and analysis, on an eight-vCPU Xeon VM.
The runner is pinned at `6ae5253` and the command is in the
[testbed README](../../README.md#run-it).

- llama.cpp `b7184`, commit `35cf8887e119eb9b9f090349129e1e71a9eb608b`.
- GGUF revision `91cad51170dc346986eccefdc2dd33a9da36ead9`; file SHA-256
  `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.

## What the pilot showed

The pooled source memory entropy was **0.1291 nats/token**. The fitted no-lesson
temperature was **0.55** (source entropy **0.1183**, vs. **0.1789** at the reference
temperature 0.7). On held-out uncoached episodes, pooled memory / matched control /
plain control entropy was **0.1313 / 0.1274 / 0.1804**. Individual memory arms
ranged from **0.0973** to **0.1511** on that held-out measure; the control matches
the pooled average approximately, not every arm.

- **Explicit workflow templates beat both controls.** AutoSkill led on overall
  success (55.8%) and beat the entropy control by **49.0 pp [45.6, 52.3]**.
  OpenSkill, the skill library and Knowledge Cards gained **35.2**, **30.2** and
  **28.5 pp**, respectively, against the same control. This comparison is not
  evidence for one isolated mechanism: AutoSkill writes from operator coaching
  and OpenSkill has extra public evidence.
- **MCP and Reflection were weak under this actor and action format.** The model
  never emitted a valid named-tool action for MCP. That arm completed 1/420
  uncoached tasks versus 2/420 for the entropy control; its overall **+2.5 pp**
  came from coached tasks (44/60 versus 31/60). The MCP result therefore does not
  test successful callable skill reuse. Reflection tied the entropy control
  overall (**0.0 pp [-2.1, 2.3]**). The plain and entropy controls produced
  invalid output on 332/480 and 327/480 online tasks, respectively. A clean
  follow-up should compare the same text and callable procedures with a model
  or action decoder that can reliably use both surfaces.
- **Drift and retirement exposed different failures.** Every arm failed all ten
  changed-family tasks in the first post-drift wave. After the coaching wave,
  OpenSkill and AutoSkill succeeded on 78/100 and 72/100 subsequent changed-family
  episodes, compared with 0/100 for both controls. The recovery target is each
  arm's own pre-drift score, so nominally fast recovery at a near-zero target is
  not evidence of adaptation. For unchanged retired workflows, AutoSkill went
  from 62.5% to 42.5% and OpenSkill from 45.0% to 27.5%. In contrast,
  zero forgetting for the controls means zero probe accuracy at both checkpoints.

This is a five-stream diagnostic with pointwise intervals; large gaps can
reflect protocol and output-format differences as well as memory.
