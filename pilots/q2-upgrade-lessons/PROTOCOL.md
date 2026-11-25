# Fleet Q2: predict lesson utility through a model upgrade

Adapt the [frozen Q2 protocol](https://github.com/manojbajaj95/cl/blob/1eb8474f4f2fac5d53af88cbcbfc5731cb3e5562/pilots/fleet-q2-upgrade-triage/protocol.md)
to the ticket's plain likelihood-gain predictor. Use [G1's router](https://github.com/manojbajaj95/cl/pull/14)
and Qwen2.5-0.5B-Instruct → Qwen2.5-1.5B-Instruct (Q4_K_M, CPU).
Keep G1's exact prompt, legal A/B/C policy at temperature 1, action-dependent
transitions, and binary terminal reward (two or more correct routes).

## Freeze the lessons and episode splits

- Sample 300 old-model no-memory writer episodes. Draw 20 distinct failed
  episodes and have the old model distill one short playbook note from each,
  given the trace and verifier-correct route at each step. Also draw 7
  helpful, 7 neutral and 6 misleading notes from the three G1 strata. Freeze
  the emitted notes without filtering or rewriting them.
- Use starting codes 10, 11, 12, 16, 17 and 18 for all writer/probe
  episodes; hold out the other six for validation. One start from each
  remainder occurs in each validation half (13–15 and 19–21). Held-out
  **starts** and episodes are disjoint; later states can recur between
  partitions because the task has only 36 states.
- Probes are 60 no-memory episodes per model, independently sampled from
  the source starts. Report checkpoint-code coverage. A distilled note's
  source start is the start of the failed episode that authored it. Every
  G1 note is evaluated on all six source starts: all runs start at
  checkpoint one and visit each checkpoint, so a G1 note referencing a
  particular checkpoint does not select particular source starts.

## Gate 1: exact held-out truth and reliability first

For each start, enumerate all 27 action paths. Sum the probabilities of the
successful paths, pair the memory and no-memory arms and average their
difference over the six held-out starts. This is exact expected success on
the specified constrained policy, not a 200-rollout estimate. Assess
split-half agreement across lessons at the **start** level: Spearman between
the two start halves and Spearman–Brown corrected reliability. Stop before
the probe, predictor and judge analysis if corrected reliability is
undefined or below 0.70; do not collect more rollouts.

## Gate 2: predictor, controls, calibration

- Predictor: on actual actions from the 60 old-model probe episodes, keep
  the routes that the verifier marks correct, including correct routes in
  failed episodes. Mean new-model delta log probability of those logged
  actions, lesson minus no lesson. No synthetic replacement of a mistake
  with the gold action, no IS/DR or M2 visitation weighting.
- Controls: new-model zero-shot exact success on each lesson's source
  starts, old-model likelihood gain on the same logged successful routes,
  and the new-model judge's expected 1–5 rating given the lesson and
  its no-memory probe summary. Also report the frozen protocol's
  non-gating controls/diagnostics where applicable: the raw gain over
  old log states with oracle-correct routes, lift alignment, harmful lift
  on upgrade-improved states, the original M2-visitation-weighted
  probability lift, and a verifier-based source replay check.
- Direction: positive delta means more useful. Report signed rho for
  zero-shot success; compete with its absolute rho, which cannot make
  the zero-shot control weaker than using its conventional inverse sign.
  Kill if predictor rho <0.50 or predictor margin over zero-shot <0.15.
  Gates use point estimates. Report 95% paired bootstrap intervals for
  the rhos and all margins (4,000 lesson resamples); the intervals are
  conditional on the fixed router, starts and offline logs. Repeat after
  averaging the scores of any exact duplicate lesson texts.
- Report the old-model exact effect on the held-out starts, obsolete
  (old gain >0 and new gain ≤0), and harmful (new gain <0). The frozen
  protocol also flags fewer than 6 obsolete-or-harmful lessons; report
  that check separately from the ticket's two predictive decision gates.
- Non-gating deployment check: select eight random five-note packs
  before looking at rankings. Compare reloading all notes to retaining
  only the notes with positive predictor scores, leaving omitted slots
  as padded placeholders so both prompts use the same token count.
  Enumerate held-out success for each arm; report the paired mean with
  a bootstrap interval over packs and compare it with +3 percentage
  points. This is a prompt-level check, not a test of free-context reuse.
- Non-gating replication: re-use the frozen inventory and new-model truth,
  but use Qwen2-1.5B-Instruct as the old model for the 60 probes and old
  policy. This changes the reader pair, not the lesson author.

The original Q2 weighted probability-lift predictor and its 200-rollout
truth are replaced by the ticket's requested predictor and exact oracle.
The exact oracle shares local model likelihoods with the predictor,
but uses absolute path probabilities for all actions, including failures,
and different starts; one measure is not just a re-expression of the other.
