# Toolbox vs lessons under API drift: protocol (frozen before the full run)

Claim under test (reviewer's narrowed Agent Toolbox): a self-maintained **code
toolbox** detects API drift and recovers from it in fewer episodes than **text
lesson memory**, because tools fail loudly and lessons fail silently.
Strongest control: the same lessons with the same regression tests attached.

## Setup

* World: deterministic toy API (`env.py`), 20 API functions, one recurring
  procedure per function (20 procedures). Each procedure has a hand-written
  canonical tool (Python) and a lesson that says the same thing in English
  (API call, field, computation). Procedure semantics never change; the API does.
* Drift: at episode 60 of a 180-episode stream, 6 of 20 APIs (30%) change.
  3 are **breaking** and documented (function renamed, main return key
  renamed, both visible in the API listing). 3 are **silent** and
  undocumented (units/sign/format/order of the main field change; the
  listing is unchanged). Which APIs drift, the procedure order and inputs
  come from the seed and are shared by all arms (paired streams).
* Model: Qwen2.5-Coder-3B-Instruct Q4_K_M (llama.cpp, CPU), temperature 0.3,
  for every LLM step in every arm.
* Arms (2x2):
  * `tool`: memory is code; executed directly.
  * `tool+tests`: code plus 2 regression tests (fixed inputs, expected outputs).
  * `lesson`: memory is text; each episode the LLM writes code from the lesson
    and the current API listing, then it runs.
  * `lesson+tests`: text plus the same 2 regression tests, run on the code the
    LLM wrote from the lesson that episode.
* Signals available to every arm: a raised exception (or uncompilable code);
  tests failing (tests arms, run after every use); user feedback with the
  correct answer on 20% of wrong, non-crashing episodes (same draws across arms).
* Maintenance on any signal: the LLM rewrites the artifact (code or lesson)
  given the API listing, the artifact, the code that ran and the signal text.
  Tests arms verify the rewrite against the tests and get a second attempt
  if it fails; no-tests arms accept the single rewrite.
* Seeds 0, 1, 2. 18 drifted (seed, procedure) units per arm (9 breaking, 9 silent).

## Measures (per drifted unit, counted in uses of that procedure after drift)

* **Detect**: index of the first post-drift use that raises any signal on
  the procedure. Never: number of uses + 1 (censored).
* **Recover**: first use index k whose use is correct and whose next use (if
  any) is correct too. Never: uses + 1.
* Secondary: silent-wrong uses (wrong, no signal), pre-drift accuracy, false
  flags on undrifted procedures, LLM calls and tokens; detect/recover in
  stream episodes since drift.

## Decision rule

Primary contrast: `lesson+tests` minus `tool+tests` per unit (positive means
tools are faster). 95% CI by hierarchical bootstrap (resample seeds, then
units within seed), 10,000 draws; seed-level means reported too.

* **Kill** if lessons+tests match tools on both measures: neither CI excludes
  0 in the tools' favour.
* **Keep** if tools are faster on at least one measure (CI above 0) and not
  slower on recovery (CI not below 0).
* Tools faster only to detect but slower or tied to recover is reported as
  a kill for the claim as stated (detection without faster recovery).

## Addendum (added mid-run, before any `none` data): no-memory floor

Reviewer-approved control (anomaly batch 1, PR #27: an entropy-matched
temperature on the no-lesson policy reproduced ~95% of per-lesson effects).

* Arm `none`: no saved tool or lesson and no repair. Each episode the LLM
  writes the function from the procedure goal and the current API listing.
* Its temperature T is fit by entropy matching on source (pre-drift) tasks
  only (`fit_temperature.py`): mean per-token entropy of the `lesson` arm's
  greedy completions at T=0.3 on the 20 pre-drift prompts is the target; T is
  the grid value (0.05..2.00, step 0.05) whose no-memory entropy is closest.
  Fit written to `temperature_fit.json`.
* Reported as `none - <memory arm>` on detect and recover (positive: memory
  arm is faster than the floor). It is a floor only; the decision rule above
  is unchanged.
