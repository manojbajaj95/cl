# Pilot protocol: deferred trust in a continual learner

**Question.** Can a learner remember how *jointly* changing a few source-trust
weights would change its final parameters, without storing the stream or
maintaining one model per possible revision? The target is a finite,
chronological SGD run with revised weights, not a batch optimum or certified
unlearning. Source identity is available at ingestion; future edits are not.

## Hypotheses and kill criteria

1. **Sketch the interaction, not the checkpoint.** Maintain rank-one
   directional sketches of the source-weight Hessian as SGD runs. The
   cross-source Hessian can be both sparse in source pairs and high rank in
   parameter space, enabling subspace recovery. On paired streams at edit
   radius 0.5, pass only if the sketch has at least 3x fewer live parameter
   coordinates than the dense Hessian learner, meets dense Taylor's RMSE to
   within 10%, and reduces RMSE by at least 20% vs the best non-oracle
   control (including the exact diagonal second-order learner), with paired
   95% bootstrap interval excluding no improvement. At radius 1, report
   removal separately; do not infer it from the radius-0.5 result.
2. **Derivative-free mixed shadows.** Replace derivatives with finite
   differences between live, counterfactually weighted SGD shadows. At the
   same persistent parameter-vector budget as the sketch, a joint-shadow
   subspace decoder must reduce RMSE by at least 20% vs independent
   single-source shadows and a dense ridge decoder using the same shadow
   data, on paired streams at radius 0.5, with paired 95% intervals
   excluding no improvement. Otherwise do not retain the derivative-free
   claim.

The paired generator is an intentionally favorable mechanism test.
Evaluate both hypotheses on a bridged version, an unstructured dense version,
and a digits stream whose trust policy changes after supervised training.
Do not claim general utility or recommend a cluster without improvement vs
the strongest control beyond paired streams. Use an exact chronological
rerun per query as the scoring oracle only. Read out parameter RMSE and
clean-holdout excess log loss vs that oracle; a better oracle match alone
does not imply a better classifier.

## Frozen evaluation

- 24 source IDs, no source graph provided. 1,536 one-example logistic SGD
  updates at learning rate 0.16, baseline source weights all 1. The dense
  jet retains every pair, the sketch retains 48 Gaussian directional rows,
  and the shadow budget is 97 parameter vectors including the anchor.
- Development streams 11–14; held-out streams 101–124. Pair methods on
  stream, query and initialization. Draw six independent queries each
  editing 2, 4 and 8 distinct sources by signed changes of radius 0.5 and
  1. Each seed's loss averages its own queries. Bootstrap streams, not
  examples, for means and paired relative effects (10,000 draws).
- Mechanism diagnostic: compare recovered support with the generator's
  hidden source pairs at 12, 13 and 48 measurements. The 12-pair rank
  budget is specified before evaluation; wrong rank and feature bridges
  are stress cases, not tuning signals. At 12 rows MUSIC has no noise
  subspace, so treat support as non-identifiable by this decoder.
- Controls: unchanged anchor, exact first-order, exact diagonal
  second-order, live single-source shadows, equal-vector mixed shadow
  ridge, an affinity-gated exact jet tracking at most 24 pairs plus 24
  input fingerprints, regularized full-data batch refit on the favorable
  generator, and reservoir chronology (byte cap equal to sketch state). Report dense
  second-order separately as a memory-relaxed reference. Account for
  persistent state and per-event math separately; matching vector counts
  does not match FLOPs.

## Follow-up: can the learner tell when not to trust its sketch?

The first held-out run showed that the derivative-free decoder works under
weak coupling but not under dense coupling. Test a guard before scaling:
use the original analytic sketch's 48 rows as 32 fit, 8 selection and 8
confirmation rows. Compare rank-4/8/12/16/24 MUSIC and dense kernel ridge
on selection-row squared residual, then accept the best only if its
confirmation residual is at most 80% of the no-pair residual. Otherwise
use the diagonal jet. Neither validation split sees past examples.
Report constant-rank MUSIC and diagonal controls on the same streams.

Use new seeds 201–224, unchanged radius and query design. H3 passes if the
guard cuts radius-0.5 RMSE by 20% vs diagonal on **both** paired and
bridged streams (paired 95% intervals exclude zero improvement), and the
interval excludes more than a 5% regression on **both** dense and digits.
Include a rekeyed stress test: for the first quarter, pair sources under
one random assignment; then switch to an independent assignment with no
boundary marker. Report whether the guard beats axis shadows and online
feature affinity there. Only improvements on an independent, non-planted
dataset could support scaling.
