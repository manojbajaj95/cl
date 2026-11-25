# Map memory kill test

CPU run on Qwen2.5-1.5B-Instruct, seed 41. See the [one-command reproducer](README.md#reproduce)
and [raw results](mass-qwen15.json) for per-question predictions, the exact
fictional statements, fitted coordinates, calibration trials and drift.

## Native reader screen

The eligibility gate was 75% on 80 balanced held-out real comparisons per
axis. Geography and historical birth order were the initial axes. The
comparison screen used no supplied coordinates or newly memorized facts.
The first yes/no completion template collapsed to 40/80, 40/80 and 39/80 on
latitude, longitude and birth order with 0.5B; a chat multiple-choice format
scoring the entity names was used for the main test instead. Atomic number
and typical adult animal mass were fallback axes, not additional fictional
worlds tested and selected for performance.

| Axis | Qwen2.5-0.5B-Instruct | Qwen2.5-1.5B-Instruct |
|---|---:|---:|
| Latitude | 39/80 | 43/80 |
| Longitude | 39/80 | 40/80 |
| Birth year | 44/80 | 52/80 |
| Atomic number | — | 48/80 |
| Animal log mass | 42/80 | **67/80 (83.75%)** |

Geography used four demonstration questions; birth used two with 0.5B and
four with 1.5B (the latter also scored 52/80 without demos); atomic number
used zero demonstrations; mass used the same two demonstrations in both sizes.
These are screening runs, not a controlled comparison of model scale.

## Held-out real causal check

On animal mass, the mass probe was fit on 42 names; 14 other names were
reserved for layer/gain calibration and 14 for testing. Calibration selected
transformer block 3 (zero-indexed) and gain 4.0. The held-out probe Pearson
correlation was 0.761. The retained native comparator answered 67/80
held-out comparisons correctly before any write.

| Held-out intervention (6 real triples, 4 prompts each) | Answers matching the counterfactual | Flips toward target when initially correct |
|---|---:|---:|
| No write | 3/24 | 0/21 |
| Norm-matched opposite-direction sham | 5/24 | 3/21 |
| Write toward target mass coordinate | **16/24** | **13/21 (61.9%)** |

The question wording and original animal name were unchanged, and the
same held-out real cases were scored for all three conditions.

## Fictional world

32 fictional animals in eight chains supplied 40 local statements and 320
balanced questions. The statements were the only information about the new
entities. In the initial design, exterior comparators leaked two-hop answers:
the no-write control got 52/64 and assigning every fictional entity the
same median real mass got 64/64. The reported design counterbalances every
real comparator across two matched fictional chains, so that median
shortcut gets 32/64. The initial design is not used in the main comparison.

Directly comparing the solved coordinates without the LM gave 80/80 stated,
80/80 inverse, 52/64 two-hop and 96/96 transitive. All eight fitted chains
were correctly oriented; two-hop failures were due to the real comparator's
probe coordinate relative to the fitted fictional endpoint. The model
answered 41/52 real-leg checks and got all four paraphrases right for
7/13 distinct links. Only one of eight matched comparator pairs had
both real legs fully verified, so that subset is just eight questions.

### Accuracy by arm

| Arm | Inverse (80) | Two-hop (64) | Transitive (96) | Stated (80) | Payload bytes |
|---|---:|---:|---:|---:|---:|
| No write | 40/80 (50.0%) | 33/64 (51.6%) | 42/96 (43.8%) | 40/80 (50.0%) | 0 |
| Map memory | 40/80 (50.0%) | 42/64 (65.6%) | 39/96 (40.6%) | 38/80 (47.5%) | 98,304 |
| Few-shot RAG, k=4 | 41/80 (51.2%) | 28/64 (43.8%) | 49/96 (51.0%) | 49/80 (61.2%) | 1,488 |
| Full context | 40/80 (50.0%) | 32/64 (50.0%) | 48/96 (50.0%) | 37/80 (46.2%) | 1,488 |
| Solved-as-text | 60/80 (75.0%) | 41/64 (64.1%) | 67/96 (69.8%) | 49/80 (61.2%) | 1,251 |
| Map + RAG | 41/80 (51.2%) | 46/64 (71.9%) | 54/96 (56.2%) | 51/80 (63.8%) | 99,792 |
| Byte-matched LoRA | 39/80 (48.8%) | 33/64 (51.6%) | 50/96 (52.1%) | 44/80 (55.0%) | 98,304 |

The activation write misses the proposed 90% stated-fact sanity threshold.
On combined distant questions (two-hop and transitive), it gets 81/160
versus 80/160 for the stronger of few-shot RAG and full context, a 0.6-point
gain versus the proposed 15-point bar. The two-hop lift over no write does
not show an inverse or transitive lift. Solved-as-text is 19.6 points ahead of map
memory across the 240 unstated questions, with the same fitted geometry.
The 1/64 map advantage on two-hop over solved-as-text is only one answer;
they tied at 6/8 on the subset with both real legs verified.

Map + RAG improved two-hop over either component, but its 100/160 combined
distant score was 12.5 points above full context and 5 points below
solved-as-text. Its 8/8 result on the strict real-leg subset is descriptive
only. These 320 prompts are mirror comparisons over eight correlated chains,
not 320 independent worlds.

The map and hybrid each also use 236 bytes for the fictional name keys.
LoRA used rank 2 on eight query projections; mean training loss fell from
7.041 to 5.735 across six epochs. Text includes UTF-8 separators;
solved-as-text counts only the new records
(real readouts come from the shared structural probe). Model, probe,
serialization overhead and training optimizer state are excluded.

## Drift

With all map writes available, real comparison accuracy stayed at 67/80,
with no prediction changes. WikiText-2 test perplexity was 20.894 before
and after writing on 1,016 next-token predictions. No fictional name
occurred in that text; zero drift is isolation with no trigger, not
evidence of harmless steering once a trigger fires. The byte-matched LoRA
scored 65/80 real comparisons (−2.5 points), with perplexity 21.330 (+0.436).

## Decision

**Stop this name-keyed ridge/pseudoinverse write as tested.** The native
real comparison and real causal checks passed, and the closed-form solver
preserved all local and within-chain ordinal relations in this world.
But on fictional entities the frozen reader did not acquire reliable
inverse, transitive or even stated comparison behavior from the writes.
For this task favor storing the solved coordinates as text. This is a
single seed, one-dimensional, small-model test; it does not rule out a
different causal write direction or a reader that can make better use of
the written coordinates.

## Closest prior art

- [REMEDI: Inspecting and Editing Knowledge Representations in LMs](https://arxiv.org/abs/2304.00740)
  adds one vector to an entity's hidden state at one layer to install an
  attribute: the closest mechanism (a per-entity residual write), but with a
  trained editor, single attributes and no unstated relational inferences.
- [Linearity of Relation Decoding (LRE)](https://arxiv.org/abs/2308.09124)
  edits a subject by inverting a relation's affine map, the same closed-form
  inverse used here, but per relation rather than onto a shared axis.
- [BAKE/BIRD](https://arxiv.org/abs/2310.10322) and bilinear representations
  (ICLR 2026) show edits fail in the reverse direction unless training adds
  bilinear structure; map memory targets inverses without training.
- [Cognitive Maps in LLMs](https://arxiv.org/abs/2610.25596): unstated
  relations from in-context statements fail below about 10B parameters.
- [Language Models Represent Space and Time](https://arxiv.org/abs/2310.02207)
  decodes real spatiotemporal coordinates from pretrained LMs. A readable
  coordinate is not necessarily a direction the model uses when asked to
  compare, or one into which a new entity can be written.
- [Emergent Ordinal Geometry in Transformers Trained on Local Comparisons](https://arxiv.org/abs/2606.01269)
  finds ordinal structure and distant inference after training on adjacent
  comparisons, and ordinal geometry for some pretrained relations.
  [Relational reasoning and inductive bias in transformers and large language models](https://arxiv.org/abs/2506.04289)
  contrasts emergent linear embeddings with in-context match-and-copy.
  This test tries fast external binding into a pretrained reader rather
  than learning the geometry or its use on the new world.
- [Cognitive Maps in Large Language Models](https://arxiv.org/abs/2610.25596)
  is the closest behavioral and causal comparison: above roughly 10B
  parameters, unstated relational inference emerges in context; reported
  representations are mostly pairwise links rather than global coordinates.
  Perturbing entity-binding keys and values changed answers. This test asks
  whether a solved global coordinate can be written into a much smaller
  frozen model and outperform both raw and pre-solved text.
- [The Tolman–Eichenbaum Machine and Transformer](https://arxiv.org/abs/2112.04035)
  motivate separating reusable relational structure from quickly attached
  content. [ROME](https://arxiv.org/abs/2202.05262) uses a closed-form update
  to shared weights to edit factual associations; this test writes external
  name-keyed vectors and leaves shared weights unchanged.

## Follow-up: is the write channel the bottleneck?

This run uses the same frozen model, 32 names, 40 statements and 320 prompts.
The runner checks the regenerated statements and questions against the
original raw results.

- **Stronger closed-form write.** Keep the original block-3 probe direction
  and sweep gains or replay the same FP16 vector at three early blocks.
  Select one challenger per family solely on the real calibration triples
  not used to fit the probe: maximize target accuracy, then expected flips,
  then prefer smaller gain and the first listed block pattern on a tie.
  Report each setting on separate real test triples; no fictional answers
  select a setting.
- **Oracle.** The original world defines an order, not unique numeric
  spacings. To fix a hidden numerical ground truth without changing any
  statements or questions, place the four names at uniform intervals in
  log mass between their known endpoints' **true** coordinates. Write these
  coordinates at the original and both selected settings, without using
  solved model readouts for the target. Real comparator tokens are unchanged.
- **Variant B.** Optimize one zero-initialized dense vector per name through
  the frozen reader at the original block 3. Train on the two directional
  choices in the stated subject/object order per statement, 80 balanced
  prompts in all, for 20 epochs with AdamW (learning rate 0.03). No inverted
  order, held-out two-hop pair, or transitive pair is used for training.
  Stated accuracy here is training-set fit; inversion and other inference
  scores are out of training. All follow-up rows store the same 98,304
  vector bytes (plus the original name keys), including the multi-layer case.

Reproduce from the repository root with the same dependencies as the
[original run](README.md#reproduce):

```sh
OPENBLAS_NUM_THREADS=1 python -m experiments.map_memory.followup --output ~/map-memory-followup.json
```

### Real causal sweep

Flips are toward the counterfactual among originally correct responses.
Target counts include all 24 responses in each split (six triples, four
prompts each).

| Blocks (zero-indexed) | Gain per block | Calibration flips | Calibration target | Held-out flips | Held-out target |
|---|---:|---:|---:|---:|---:|
| 3 (original) | 4 | 12/17 | 19/24 | 13/21 | 16/24 |
| 3 | 6 | 10/17 | 17/24 | 9/21 | 12/24 |
| **3 (gain sweep)** | **8** | **11/17** | **18/24** | **8/21** | **11/24** |
| 3 | 12 | 6/17 | 12/24 | 7/21 | 10/24 |
| 3 | 16 | 6/17 | 12/24 | 8/21 | 11/24 |
| **1, 3, 5 (multi-layer)** | **1** | **11/17** | **18/24** | **15/21** | **18/24** |
| 1, 3, 5 | 2 | 10/17 | 17/24 | 10/21 | 13/24 |
| 1, 3, 5 | 4 | 7/17 | 13/24 | 7/21 | 10/24 |
| 1, 3, 5 | 8 | 6/17 | 10/24 | 7/21 | 9/24 |
| 3, 4, 5 | 1 | 11/17 | 18/24 | 14/21 | 17/24 |
| 3, 4, 5 | 2 | 10/17 | 17/24 | 10/21 | 13/24 |
| 3, 4, 5 | 4 | 9/17 | 15/24 | 8/21 | 11/24 |
| 3, 4, 5 | 8 | 5/17 | 9/24 | 7/21 | 9/24 |

Larger single-block gains did not improve the real intervention. The
calibration-selected multi-block replay improved held-out flips from
13/21 (61.9%) to 15/21 (71.4%), despite a one-answer decrease on calibration.

### Same-world fictional questions

Counts are correct answers. The first three rows are references from the
original run. The coordinate-only oracle simply compares the true scalars;
it does not run the model or write a vector.

| Arm | Inverse /80 | Two-hop /64 | Transitive /96 | Stated /80 | Vector bytes |
|---|---:|---:|---:|---:|---:|
| No write | 40 | 33 | 42 | 40 | 0 |
| Original map (block 3, gain 4) | 40 | 42 | 39 | 38 | 98,304 |
| Solved-as-text | 60 | 41 | 67 | 49 | — |
| Gain sweep, solved | 42 | 45 | 41 | 36 | 98,304 |
| Multi-layer, solved | 37 | 36 | 47 | 40 | 98,304 |
| Oracle, original | 41 | 51 | 39 | 38 | 98,304 |
| Oracle, gain sweep | 42 | 43 | 36 | 41 | 98,304 |
| Oracle, multi-layer | 39 | 46 | 43 | 41 | 98,304 |
| Variant B, trained on stated only | 36 | 43 | 54 | 80 | 98,304 |
| Oracle, coordinates compared directly | 80 | 64 | 96 | 80 | — |

**Conclusion.** The stronger and oracle axis writes stayed near chance on
stated facts (36–41/80), even though direct comparisons of the true
coordinates answered all 320 questions. The original oracle did improve
two-hop accuracy from 42/64 to 51/64, so coordinate estimation mattered in
that family, but fixing it did not fix stated readout, inverses, or transitive
inference. Variant B fit all 80 stated prompts at the same site and byte
budget, ruling out a blanket lack of capacity at that site. It did not learn
a transferable ordering: it scored 133/240 (55.4%) on unstated prompts versus
168/240 (70.0%) for solved-as-text, and inverses alone were 36/80. The evidence
favors a bottleneck in writing/reading the axis for fictional names, not an
absence of inferential information in the coordinates. A direct-fact fit
using unconstrained vectors is not evidence of a coordinate representation.

[Raw trial counts, predictions, and training trace](followup-mass-qwen15.json).
