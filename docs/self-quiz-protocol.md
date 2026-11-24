# Self-quizzing retention pilot: matched-question falsifier

**Question.** Given the same pool of recalled old facts, does replaying an
LM's own verified answers retain more than replaying independent teacher
answers to **the same questions**, or replaying the LM's own generated
prose? This is a format-controlled test of the proposer/reviewer
shortlist, not a test of spaced scheduling.

Train a small CPU causal Transformer on word-token synthetic biographies,
then expose it to three successive batches of new, nonoverlapping
biographies. Use a common pre-stream checkpoint per seed. Old and new
entities have no overlapping IDs or contradicting attributes. Old
paraphrase templates are withheld for those entities until evaluation;
their syntax is seen only on unrelated background entities.

- **Self-QA:** prompt the pre-stream model with an old entity and field
  name (not its value). The model selects a question form and samples a
  complete answer. Verify the sampled value against the generator's
  fact table; the known answer is not given to the model.
- **Teacher QA:** the exact accepted self-question, same factual value,
  independent canonical wording authored by the benchmark. The answer
  token count is identical. Also check the logical control: if a teacher
  writes the identical response tokens, provenance cannot change an
  otherwise identical SGD update.
- **Generated prose:** freeze the same checkpoint and sample continuations
  of entity-and-field-anchored prose. Give the main raw baseline the
  same verification, supported facts, draws and target-token budget as
  self-QA. Also report unfiltered self-generated prose to show what
  verification buys. This is the synthetic analogue of [SSR replay](https://arxiv.org/abs/2605.26097),
  not a reproduction of its corpus-scale setup.
- **No replay:** exactly the same new examples from the same checkpoint;
  a manipulation check, not a compute-matched competitor.

Replay uniformly from a fixed bank of matched fact triplets, with identical
fact schedules, all-token next-token loss and equal numbers of active
replay target tokens. No teacher either sees later tasks or chooses which
facts to replay. Report generation attempts and acceptance separately.

## Decision and statistics

- Check the plumbing on development seed 41 only. The held-out seeds
  are 501–503. Measure old paraphrase accuracy before the stream, after
  every segment, and at the end; score the hidden value with a common
  evaluator marginalizing the grammatical answer forms. Report old
  NLL and new acquisition as secondary outcomes.
- Seed 41 showed a ceiling (97.6–100% retention across the replay arms)
  at 8 replay rows per 24 new rows. Freeze the more informative low
  budget of **1 per 24** for the held-out run. Each row has 12 active
  next-token targets.
- Manipulation checks: each held-out seed starts above 60% accuracy on
  old paraphrases, loses at least 10 percentage points after no replay,
  and has verified question/prose coverage of at least half the old
  facts. If these fail, mark the pilot inconclusive rather than negative.
- **Keep** only if self-QA beats *both* matched teacher QA and verified
  generated prose by at least 3 percentage points each in final old
  paraphrase accuracy, the respective paired 95% intervals exclude zero,
  and final new-fact accuracy is no more than 3 points below either
  baseline. Report all seed differences and paired Student-t intervals
  over seeds. With three seeds, wide intervals mean this is a stop/go
  screen, not a universal equivalence claim.
- **Otherwise kill escalation.** Beating raw prose alone does not
  isolate a self-retrieval effect: [auxiliary-view work](https://arxiv.org/abs/2609.04180)
  already shows benefits from reformulating training examples.
