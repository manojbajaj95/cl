# Serving skills over MCP: what works, major flaws, and paper directions

Scan date: 2026-11-26. This is a literature and spec review with no new experiments. Numbers come from the cited papers. Ids are arXiv/alphaXiv ids.

## 1. What the protocol gives us today

- The MCP Skills extension ([SEP-2640](https://modelcontextprotocol.io/seps/2640-skills-extension), [spec](https://github.com/modelcontextprotocol/ext-skills/blob/main/specification/beta/skills.mdx)) is **read-only**. It has `skills/list` (paginated; frontmatter plus a file manifest with SHA-256 digests), `skills/get` by URI, and `resources/read` for `SKILL.md` and its files. It has no `skills/search`, no publish/update, no outcome feedback, and no version lineage. A skill's identity is `(server, URI)`.
- Hosts use the Agent Skills progressive-disclosure pattern: about 50-100 tokens of name and description per skill stay in context, and the body (<5k tokens) loads on demand.
- Pre-extension servers expose skills as tools instead (`list_skills`, `find_helpful_skills`, `get_skill`), e.g. skills-mcp, K-Dense, and Local Skills MCP. SkillSeek (2609.38822) serves BM25 plus a cross-encoder over MCP.

## 2. What works (evidence)

| Finding | Source |
|---|---|
| Curated skills raise pass rate from 33.9% to 50.5% across 18 model-harness configs. Focused skills (<=3 modules) beat large bundles. | SkillsBench 2602.12670 |
| Skills mostly act as *procedural anchors* (65.7% of cases); fact injection accounts for only 4.5%. Skills beat workflow memory by 6.06 pts. | Demystifying Agent Skills 2608.14036 |
| Plain IR retrieval served over MCP matches an LLM-mediated retrieval loop and cuts spend from $51.30 to $27.54 per trial. | SkillSeek 2609.38822 |
| Body-aware retrieve-and-rerank (1.2B) reaches 74.0% Hit@1 over about 80K skills. | SkillRouter 2603.22455 |
| Rewriting only the *description* of each new skill to contrast it with its nearest neighbour selects all required skills on 76.3% of queries, against 36.4% for the original metadata (731 skills). | Skill++ 2611.00544 |
| Lazy schema loading cuts tool tokens by 95% (47.3k to 2.4k), measured in simulation only. Code mode beats plain MCP with 70-90% fewer tokens, and a router in front of it adds nothing significant. | Tool Attention 2604.21816; Beyond Plain MCP 2611.19123 |
| A frozen LLM's own hidden states route skills better than retrievers that add 1.2B-16B parameters. | Gavel 2609.15982 |
| Path-addressed skills ("reading is using"), with prompt residency only for skills explicitly installed. | @skills 2608.12610 |
| Playbooks (ACE / SkillBook style) curated by **randomized block inclusion** reach 66.9 average success, against 55.5 for the whole playbook and 53.8 when the agent judges its own lessons. | RBC 2610.18427 |
| SkillBook-style distill-verify-admit loop: 28.7% to 49.7% held-out pass; curation, training and routing are bundled, so the gain is not isolated. | MERA 2608.10333 |
| Branching search over library versions beats linear evolution in 9/10 settings. | SkillVine 2609.32731 |

Our own [PR #422](https://github.com/manojbajaj95/cl/pull/422) ([paper](https://www.alphaxiv.org/abs/2611.when-should-a-self-written-skill-branch)) found that adaptive branching beats a shared compromise when the cue is strong (.232 vs .139 worst-cohort utility). Fixed cue-conditioned variants did much better (.544), and weak cues never triggered a split.

## 3. Major flaws of serving skills over MCP

1. **No learning loop.** The extension is read-only and has no outcome channel. A server cannot tell whether a skill helped, so curation, branching, retirement and A/B tests (RBC, Skill++, #422) cannot run server-side without out-of-band telemetry. This is the biggest structural gap.
2. **Catalog-in-context does not scale.** With progressive disclosure, actual-use precision falls from 29.6% to 3.3% as the pool grows from 5 to 100 (2608.14036), and @skills estimates fewer than about 100 reliable prompt slots. A 1,000-skill catalog costs 50-100k tokens before any work starts.
3. **Routing interference as libraries grow.** A new, similar skill displaces an old one even though neither changed (Skill++). This is class-incremental forgetting, a CL problem that sits at the server boundary.
4. **Metadata-only discovery throws away signal.** Hiding the body costs 37-44 pts of routing accuracy (SkillRouter). MCP lists frontmatter, so descriptions carry the whole selection burden.
5. **Triggering and compliance are separate failures.** The best Skill-Use score is 0.613, and rankings shift with the harness (2608.04828). Serving the right skill does not mean it is used.
6. **Staleness with valid digests.** A digest pins bytes, not validity against a changed environment. Stale skills can cost more than 10 pts or add about 40% execution cost compared with no skill (2611.22525). Usefulness also differs per model: skills get internalized, and retirement verdicts vary by model (2610.32322).
7. **Self-written SkillBooks are unstable.** The same procedure can write a playbook up to 69.6 pts *below* no playbook (RBC). Serving unvetted agent-written skills at scale amplifies this.
8. **Trust and supply chain.** A content hash is not publisher trust. 49.6% of ClawHub skills with resolvable dependencies pin a version with a known CVE, and 21 of 22 sampled first-party flaws are reachable (2611.30932). Frontmatter can also be poisoned to bias routing, as with MCP tool poisoning.
9. **Versioning and branching are conventions only.** Without lineage or immutable-revision semantics, branches, rollback and per-cohort variants are ad hoc across servers.

## 4. What can be done: candidate papers, ordered by novelty and feasibility

Each paper reuses the [PR #38](https://github.com/manojbajaj95/cl/pull/38) skill-memory fixture (paired tasks, deterministic verifier, endpoint/argument drift) with a native Skills-over-MCP server swapped in for its tool mock.

1. **The MCP server as a randomized experimenter (population-curated SkillBook).** A server sees traffic from many clients. It can randomize which skill blocks or variants each request gets (RBC across clients rather than practice tasks), estimate each block's causal effect from a minimal outcome signal, and serve the curated book per cohort or per model. This needs a small `skills/feedback` notification, which is the protocol gap from flaw 1.
   - *Primitive:* serving-time causal curation.
   - *Risks:* sparse or noisy outcomes, and poisoned feedback.
   - *First test:* simulated multi-client stream on the PR #38 tasks, comparing agent-judged curation, unconditional writes, and randomized-inclusion curation at a matched request budget.
2. **Catalog-relative descriptions against routing interference.** The server rewrites a skill's description as a function of the *neighbours it is listed with* (per request or per top-k), not once at install time as Skill++ does. It is framed as lifelong class-incremental routing with retention measured on old skills.
   - *First test:* grow a library to about 700 skills and compare static, Skill++-at-install and catalog-relative descriptions on all-required recall, false triggers and token cost.
   - *Closest prior art:* Skill++, SkillRouter.
3. **Served branching under real costs (follow-up to #422).** Expose cue-conditioned variants as immutable sibling URIs and let the client cue select one. Test whether #422's negative result (fixed conditioning beats adaptive branching) survives once prompts, approvals and maintenance are priced, and whether SkillVine-style branch search helps when only server-side signal exists.
   - *A clean negative result is publishable.*
4. **Validity-aware serving: staleness and internalization.** Attach replayable applicability checks to each skill (selective maintenance, 2611.22525) and serve per-model catalogs that drop skills a given model has internalized (2610.32322). Measure post-drift recovery and tokens saved.
5. **Discovery, not transport, is the bottleneck (benchmark / negative-result paper).** Hold content fixed and compare local files, full MCP list, MCP with server-side body-aware top-k, and tool-wrapped skills across catalog size, cache state and host. Report a decision trace: retrieved, selected, loaded, followed.
   - *Expected result:* transport is roughly neutral and discovery dominates.

Recommendation: start with (1). It is the most novel, it directly fixes the biggest flaw, and it is a CL contribution (a server-side learning loop under non-stationary traffic). (3) is the cheapest because it reuses #422.

## Sources

Spec and implementations: [Skills extension overview](https://modelcontextprotocol.io/extensions/skills/overview), [WG rationale](https://github.com/modelcontextprotocol/ext-skills/blob/main/docs/rationale.md), [Agent Skills spec](https://agentskills.io/specification), [skills-mcp](https://github.com/skills-mcp/skills-mcp), [K-Dense claude-skills-mcp](https://github.com/K-Dense-AI/claude-skills-mcp).
Papers: 2602.12670, 2603.22455, 2604.21816, 2608.04828, 2608.10333, 2608.12610, 2608.14036, 2609.15982, 2609.32731, 2609.38822, 2610.18427, 2610.23554, 2610.32322, 2611.00544, 2611.19123, 2611.22525, 2611.25429, 2611.30932 (all at `https://www.alphaxiv.org/abs/<id>`).
