## Context

`proposal.md` has the motivation; the numbers behind it are in
`openspec/changes/archive/2026-09-02-transcribe-per-batch-subagents/measurements.md`. The one fact
this design is built on:

```
cost/page ≈ t·(B+P)  +  t·m·N/2  +  s·(B+P)/N
             ^^^^^^^     dominant term: 212k of 509k at N=5
             turns × the 62.7k fixed payload re-sent on every turn
```

`B+P` is not ours to shrink much — it is a subagent's system prompt, tools, the pinned rules, the
house-style extract and the glossary, and the extract has already been trimmed from 9.5k to 2.6k.
`m` is 7.25k/page and small. **`t` is the free variable, and it came in at 5.7 against a design
assumption of 2.** So this change is about turns, plus the one place where subagents are run serially
for no reason.

Whether to keep the vision reader at all was settled first: see `ocr-assessment.md`. Verdict was to
keep it, which is why this change optimizes rather than replaces.

Constraints inherited: the copyright gate stays a hard precondition and stays dependency-free and
AI-free; the human review checkpoint stays before any push; provenance stays honest; nothing here
touches what a faithful transcription is.

## Goals / Non-Goals

**Goals:**

- Cut `t` for transcription from ~5.7 toward ~3.3 by removing the per-crop turn tax.
- Stop paying serial wall-clock for the verification pass, which has no ordering dependency.
- Establish whether verification — half the run's cost — needs the top model tier, by measurement
  rather than assumption.
- Leave a measurement that is like-for-like with the 509k/page and ~1.0M/page figures.

**Non-Goals:**

- **The Antigravity skill at `.agents/skills/transcribe/`.** The corpus is transcribed by two skills
  on purpose: this one on Claude models, where bounded-context subagents and per-turn payload
  re-sending make *turns* the dominant cost, and the Gemini 3.8 Flash skill, where a long context and
  direct high-resolution ingestion make them largely irrelevant — it is explicitly exempted from
  `magnify.py` escalation by its own requirement. Every decision below is an optimization against
  Claude's economics and must not be generalized to the other skill. The delta scopes the shared-
  sounding requirements accordingly.
- Changing the transcription rules, the house style, or the status ladder.
- **Parallelizing transcription.** Explicitly rejected in D4, not deferred.
- Touching the Tier-3 Batch API path, already bounded per page.
- Replacing the vision reader with OCR (`ocr-assessment.md`).
- Shrinking `B+P` itself. Worth maybe 12% per the archived scenarios table, and mostly outside our
  control; not this change.

## Decisions

### D1. A `pipeline/magnify.py` helper that takes many regions at once

Today a subagent writes ad-hoc crop code per region: one Bash call to compute and save, one `Read`
to look at it. At 1.7 crops/page that is ~3.4 turns/page of pure escalation tax, and it is why the
36-crop run cost what it did.

The helper accepts a page and a list of regions in *prepared-image* coordinates, applies the
`zoom-map.json` mapping itself (`source = offset + prepared/scale`), crops from the **source** scan,
and writes all the crops in one invocation. The subagent then reads them in a single turn by issuing
parallel `Read` calls in one message.

```
before:  [Bash crop] [Read] [Bash crop] [Read] [Bash crop] [Read]   = 6 turns
after:   [Bash magnify --regions ...] [Read ×3 in one message]      = 2 turns
```

At the cap of 3 regions this is 6 turns → 2. At the measured 1.7 crops/page it removes ~2.4
turns/page, i.e. the bulk of the gap between `t = 5.7` and the archived design's assumed `t = 2`.

Second benefit, free: the coordinate mapping stops being something each subagent re-implements. The
spec already records a batch that landed 2 of 3 crops on the wrong lines by inferring the mapping.
Putting the arithmetic in tested code removes that failure mode rather than warning about it.

*Alternative rejected:* keep ad-hoc cropping and merely instruct subagents to batch their Bash calls.
Instruction-only fixes to turn count are exactly what the archived design tried; the measured `t` is the result.
Code enforces what prose asked for.

### D2. Verification runs concurrently, unconditionally

The existing spec already requires each verification subagent to read its own images in a fresh
context and forbids depending on transcription's residency. There is therefore no ordering
dependency to remove — verification is embarrassingly parallel today and is merely being run
serially. Dispatch the batch verifiers concurrently.

No quality trade-off is being made here at all, which is why this decision has no A/B attached, and
why it is the only concurrency this change introduces.

**Batch granularity is inherited, not chosen, and is not settled by the data we have.** The spec
says "one subagent per batch"; this change keeps that and flips serial to concurrent. Whether
verification wants a different `N` than transcription now that wall-clock is no longer additive is a
fair question with no determinate answer yet:

| reading of the cost model | N=1 vs N=4, per page |
|---|---|
| cumulative context `(t·N + s)(B+P + m·N/2)` | ~457k vs ~417k — about 10% worse, because `B+P` is re-sent per *turn*, so fewer pages means proportionally fewer turns |
| the reported-token endpoints (91.7k at N=4, 149.7k at N=12) | fits a large genuinely-fixed component — about 3× worse |

The archived measurements flag exactly this: subagent transcripts are not persisted, so per-turn
context is unobservable, and "two points cannot separate setup turns `s` from per-page turns `t`."

Independent of cost there is a quality reason not to go to N=1: a verifier holding four adjacent
pages can compare a doubtful glyph against a clearer instance nearby, which is the stated reason
batch 4 was chosen for transcription and matters at least as much for verification, where the
recurring questions — continuation-dot counts, subscript bracing, `\frac` nesting — are precisely the
ones that only resolve by comparison across pages.

So N stays at the transcription default, and task 6.6 measures it rather than leaving it inherited.

### D3. The text-only proofread runs before the batch verifiers, not after

The text-only proofread classifies each finding as **defect**, **inconsistency**, or **needs scan**. Run after the
verifiers, every `needs scan` finding is stranded: the orchestrating session cannot read images, so
settling them requires dispatching a further subagent that re-reads scans the verifiers have just
finished reading.

Run first, they become targeted questions handed to the verifier covering those pages, settled
inside a reading that is happening anyway.

```
before:  [stitch] → [verifiers ×5] → [proofread] → [extra subagent for needs-scan]
after:   [stitch] → [proofread] → [verifiers ×N, each carrying its pages' needs-scan items]
```

Three waves become two, and each page's scan is read once rather than twice.

The proofread costs ~32k for a 130KB work and reads no images, so front-loading it is nearly free.
What it gives up is reading the *corrected* text — but its measured high-value findings were a word
split across a page break, six paragraph breaks inserted mid-sentence, and four conventions one
batch disagreed with the rest of the work. None of those is introduced or removed by verification's
per-page glyph corrections, so little is lost. Where a proofread finding and a verifier finding do
overlap, the redundancy is cheap and the scan settles it.

*Alternative rejected:* run the proofread concurrently with the verifiers. They are mutually
independent so it would work, and it saves one round-trip — but it discards the `needs scan`
routing, which is the whole point. One extra wave is cheaper than a second reading of every scan.

### D4. Transcription stays sequential — the glossary is worth more than the wall-clock

Parallelizing the transcription batches was designed out and then rejected. The design that would
have permitted it replaced the trailing-lines handoff with the prepared image of the page preceding
each batch, removing the ordering dependency at the cost of one image read per batch. Two reasons it
is not worth it:

- **`notation.md` accumulates per batch, and that granularity is the point.** The glossary is the
  highest-value quality mechanism measured: `\Sigma` went 0/19 without it to 19/19 with it, and the
  `x_1`/`x_{1}` split happened between two batches of the *same* run. Any parallel scheme coarsens
  the loop from per-batch to per-wave, so a decision made in batch 2 no longer reaches batch 3. That
  is the exact failure the glossary exists to prevent, traded for wall-clock.
- **The preceding-page image is pure cost once we are not parallelizing.** It is ~2.4k tokens
  resident across a batch's ~23 turns — roughly 10k/page more than the trailing lines it replaces,
  ~2% of per-page cost. Small, but it buys nothing at all if the batches still run in order. It only
  ever existed to unlock concurrency.

So the trailing-lines handoff stands, batches run one at a time, and Phase 3a keeps updating the
glossary after each batch. The `Tier-2 transcription skill` requirement is not modified by this
change.

**What this costs:** a 5-batch work keeps its 5 serial transcription round-trips. Only verification
collapses — 5 serial verifier round-trips become 1, so the run goes from ~11 serial round-trips to
~7. About a 35–40% wall-clock reduction rather than the ~65% full parallelism would give.

*Revisit condition:* if a later run shows the per-batch glossary loop is not actually catching
divergences that a per-wave loop would miss, the wave design is written up here and can be lifted
back out.

### D5. The verification model tier is a measurement, not a decision

Verification costs ~508k/page against transcription's 509k — half the run. PLAN.md §4.1 step 4
already proposes a cheap model for it. But the pass earns its keep on fine-grained work: it corrected
five continuation-dot rows by pixel-lattice profile and caught three `\frac`/`\dfrac` slips. Whether
a smaller model does that is not knowable from the armchair.

So this change **does not adopt** a cheaper tier. It runs the A/B, on the same pages, using the group-5
methodology from the archived change, with a stated kill criterion: if the cheaper tier misses any
correction the current tier found on the same pages, the tier stays. Provenance records the
verification model either way, so a run's verification tier is never inferred.

## Risks / Trade-offs

- **Batched crops may encourage speculative magnification** — if three crops cost two turns instead
  of six, the incentive to stay under the cap weakens → the cap of 3 regions per page stays and is
  enforced in the helper rather than in prose; the crop count per page is reported in every batch
  report so a run that starts magnifying freely is visible.
- **The helper's coordinate conversion becomes a single point of failure** — a bug in it mis-crops
  every escalation in every run, where the ad-hoc version failed one batch at a time → tested
  against known `zoom-map.json` rows, and it refuses rather than silently no-ops on an
  out-of-bounds or degenerate box, following the precedent in `prepare_pages.py`.
- **A cheaper verification tier silently degrading** → D5's kill criterion, and provenance recording
  the model so any later regression can be attributed.
- **Concurrent verifiers make the orchestrator's own context noisier** — the archived measurement
  already found the orchestrator at a 192k mean with `result: Bash` at 59%, and several reports now
  arrive together → reports stay the same fixed size, and the tasks re-measure the orchestrator
  rather than assuming it is unchanged.
- **Wall-clock gain is bounded by D4** — transcription remains the long pole, and on a work with
  many batches it dominates. Accepted deliberately.

## Migration Plan

No data migration; the corpus is untouched. Roll out on one work, comparing against the archived
Clebsch figures on the same pages, exactly as the per-batch-subagent change was rolled out. If the
measurement does not show a turn reduction, the skill changes revert cleanly — `magnify.py` is
additive and harmless on its own.

## Open Questions

- Does `t` actually land near 3.3, or does removing the crop tax reveal another turn sink? The
  archived change over-projected once already; the measurement decides, and the tasks say so.
- Does concurrent verification change what verification *finds*? It should not — each verifier is
  isolated by construction — but the run should confirm the discrepancy list is comparable, not just
  faster.
- What is the right `N` for a verification batch, now that batches no longer queue behind each
  other? D2 sets out two readings of the cost model that disagree by 3×, and only a run at two
  different `N` on the same pages separates them (task 6.6).
- How many `needs scan` findings does a typical work actually produce? D3's saving is proportional
  to that count, and it has never been measured — the reorder is cheap enough to be worth doing
  regardless, but the claimed saving should be reported honestly (task 6.5).
