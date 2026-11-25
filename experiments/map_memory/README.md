# Map memory: cue-free relation kill test

Can a frozen Qwen use a new fictional entity's coordinate, written into a native
activation direction, to answer unstated questions? The comparison is with
the same local statements in context, retrieved by name, and trained into a
byte-matched LoRA; solved-as-text controls for the external solver.

## Reproduce

From the repository root on Linux with Python 3.10+ and CPU PyTorch:

```sh
python -m pip install --index-url https://download.pytorch.org/whl/cpu 'torch>=2.9' && python -m pip install -r experiments/map_memory/requirements.txt && OPENBLAS_NUM_THREADS=1 python -m experiments.map_memory.run --model 1.5b --axes mass --threads 8 --causal-cases 6 --epochs 6 --demo-pairs 1 --output ~/map-memory-results.json
```

The run downloads pinned public model and WikiText-2 snapshots and writes a
checkpoint after each arm. Use `--path` and
`--wikitext` for already-downloaded copies, `--screen-only` to just screen
real axes, or `--force` to run a clearly exploratory evaluation even when the
native model misses the 75% real-pair gate. See [results.md](results.md) for
the exact flags and counts of the reported runs.

The focused, download-free checks are:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v experiments.map_memory.test_map_memory
```

## Protocol

1. **Freeze structural knowledge.** Split real names by sorted coordinate
   into disjoint ridge-fit, calibration, and test subsets, with a fixed seed.
   Screen real pairs with complementary relations and both display orders.
   The default reader chooses between the two entity names based on log
   probability at their first divergent answer token (after any shared prefix).
   Earlier yes/no and A/B formats are available for comparison. Every reported
   memory arm within a run uses the same reader and demonstrations.
2. **Identify a candidate axis, then intervene.** Predict standardized true
   coordinates with a ridge probe on the canonical last name token. Choose a
   layer and gain by answer changes on separate real calibration cases. In
   each case a comparator is strictly between the source and target real
   coordinates. Check the selected write on held-out real cases and compare
   with an equal-size write in the opposite direction. The original name never
   changes. The readout's Pearson correlation and the actual changes in the
   reader's answers are separate diagnostics.
3. **Bind new content in closed form.** Eight independent chains by default,
   each with four new names and two real endpoints, contribute five local
   statements per chain. Fit equal adjacent steps by a linear least-squares
   solve using the gold-parsed edges of those same statements and the
   established model readouts for the real endpoints. This pilot does not
   test extracting relations from prose. The solve reduces to equally spaced
   interpolation between
   the endpoints for these worlds. If the model readouts reverse an interval,
   report it; do not replace the readouts with true coordinates. Each write is
   a dense FP16 residual vector
   `gain * (solved_coordinate − original_readout) * w / (wᵀw)`, appended by
   name and added at the last token of every exact name occurrence. The map
   arm does not pass statements, numbers, or retrieved text to the model.
4. **Score the same balanced questions across arms.** Inverses swap the stated
   subject and object and test both directional choices. Two-hop questions
   combine a stated fictional-to-real edge with a separate real-to-real edge
   that is never provided. The same real comparator appears on opposite
   sides of fictional endpoints in matched chains, so a constant fictional
   coordinate cannot solve this family. Also score the counterbalanced
   subset whose two real legs the frozen model gets correct in both orderings
   and both directions. Transitive pairs
   skip one or two fictional nodes.
   Stated comparisons are a sanity check. The held-out two-hop and transitive
   pairs never appear together in a stored statement. “Cue-free” means
   conclusion-free here, not entity- or relation-free: questions name their
   endpoints and relation so all arms can use the same questions.
5. **Control for representation and storage.** RAG ranks statements by exact
   endpoint overlap, retrieves at most four, and uses stable ties. Full
   context uses all the identical statements. Solved-as-text retrieves both
   requested coordinates from the same fit, even for real comparators. LoRA
   trains on those statements only, using rank allocations across evenly
   spaced query projections and rounding adapter parameters to FP16. Match
   persistent tensor payload bytes (not file headers, maps, optimizer states,
   or the shared structural probe); report name-key bytes separately.
6. **Measure drift.** Compare wiki perplexity and held-out real comparisons
   with the entire name-keyed memory enabled vs. off; report how often a
   trigger fired. Drift in prompts with no triggers checks isolation, not
   benign behavior when triggers fire. Also report drift for the always-on
   LoRA.

The benchmark is an ordered-chain pilot, not a test of multidimensional
simultaneous binding, arbitrary graphs, implicit-use questions, or long
continual streams. A poor causal check makes a negative memory-arm result
evidence about this write mechanism, not about every possible latent map.
