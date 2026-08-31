## Context

`/transcribe` runs the whole job in one Claude Code session: acquire scans, read each page, write
LaTeX, stitch, lint, preview the site, open the PR. Every page image read stays in context for the
rest of the run, so context grows monotonically and each turn re-sends every page read so far. The
measurements are in `proposal.md`; the short version is 4–6M tokens per transcribed page, of which
roughly 60% is scans being re-sent.

Inside Claude Code there is exactly one mechanism that resets context without ending the session:
dispatching a subagent, which runs in a fresh context and returns only its final text report. That
is the whole lever available here. The Tier-3 script cannot be borrowed, because it bills a
contributor's `ANTHROPIC_API_KEY` and Tier-2 exists so contributors can work on a Claude Code
subscription instead (PLAN.md §4.1, §7).

Constraints inherited from the project: the copyright gate stays a hard precondition, the human
review checkpoint stays before any push, provenance stays honest, and nothing added here may pull a
dependency into `pipeline/validate.py` or CI.

## Goals / Non-Goals

**Goals:**

- Per-page cost independent of how many pages precede it — flat, not linear.
- Cross-page consistency preserved by an explicit, reviewable artifact rather than by conversational
  memory.
- A measurement that shows whether transcription quality moved, on the same work and same scans,
  before the architecture is trusted with the rest of a work.
- The main session's context small enough that a cache miss is cheap rather than catastrophic.

**Non-Goals:**

- Changing what a faithful transcription is. `prompts/transcribe-chat.md` and `corpus/HOUSESTYLE.md`
  remain authoritative and substantively unchanged.
- Touching the Tier-3 Batch API path, which is already bounded per page.
- Fixing `/translate` (same shape, much smaller: it reads `original.tex`, never images).
- Eliminating the cache-miss behavior itself, which is not caused by the skill. This change only
  shrinks what a miss costs.

## Decisions

### D1. One subagent per batch of pages, not one per page

The main session becomes an orchestrator that never calls `Read` on a scan. Per batch it dispatches
one subagent with: the pinned prompt, the transcription-relevant house-style rules, the work's
notation glossary, the previous batch's trailing lines, and the list of page images to read. The
subagent reads those images, writes `corpus/<work-id>/pages/pNNN.tex`, and returns a compact report.

**Measured 2026-08-31** on two clean isolated runs over untranscribed Clebsch pages (N=4 on pp.
207–210, N=12 on pp. 211–222), both reproducing house style with 16/16 fragments passing
`houselint`:

| N | reported tokens | tool calls |
|---|---|---|
| 4 | 91.7k | 14 |
| 12 | 149.7k | 41 |

Fitting `tokens(N) = (B+P) + m·N` gives a **fixed cost per subagent of B+P = 62.7k** and a
**marginal cost per page of m = 7.25k**, with **t ≈ 3.4 turns per page**. Cumulative billed context
is then `(t·N + s) × (B+P + m·N/2)`, giving these per-page costs against the measured 4.2M/page
baseline:

| N | 2 | 3 | 4 | 5 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|---|
| tokens/page | 254k | 261k | 270k | 281k | 315k | 363k | 411k |
| vs baseline | 16.6× | 16.1× | 15.5× | 15.0× | 13.3× | 11.6× | 10.2× |

**This overturned the original N=8 default.** Decomposing the cost at N=5 shows why:

| term | tokens/page | depends on N? |
|---|---|---|
| `t·(B+P)` | **212k** | **no** |
| `t·m·N/2` | 61k | yes |
| `s·(B+P)/N` | 6k | yes |

Roughly **three quarters of the cost is `t·(B+P)` — every turn re-sending the subagent's fixed
baseline — and that term is completely independent of batch size.** Batch size is a second-order
lever. The first-order levers are the number of turns per page and the size of the fixed payload.

**Default N=4**, sitting within ~3% of the fitted optimum across every scenario below while keeping
several adjacent pages visible to one agent for local comparison. N=1 is marginally cheaper still
but loses that, and the curve is flat enough (±3% from N=2 to N=5) that quality wins the tie.

*Caveat on precision:* only two points were measured, and splitting the tool-call count into setup
turns `s` and per-page turns `t` is underdetermined by two points — the fitted `s=0.5` is not
physically meaningful next to the two style-file reads actually observed. Depending on that split
the optimum lands anywhere in N=1.6–3.2. The robust conclusions — small batches, and `t·(B+P)`
dominating — hold across the whole range. Per-turn context was not directly observable: subagent
transcripts are not persisted (empty `.output` files, no sidechain entries), so the cumulative-cost
figures are **modelled** from the measured endpoints, while `tokens(N)` and the turn counts are
**measured**.

*Alternative considered — one subagent per page:* maximally flat, but pays the ~35k baseline 91
times for a work like Abel and destroys within-batch comparison between adjacent pages. Rejected.

*Alternative considered — sliding-window context eviction in the main session:* Claude Code exposes
no way to drop a specific tool result, and compaction is neither controllable nor predictable.
Not available.

### D2. Cross-page consistency lives in `corpus/<work-id>/notation.md`

The genuine cross-page dependency is not back-references — an author's `équation (92)` is printed on
the page being transcribed and is copied verbatim, needing no memory of page 92 (Abel carries 202
such tags and they are all local). It is **work-spanning rendering decisions**: how this work's
Fraktur, long-ſ, orthography, and function-application notation are rendered. Those already end up
written down, as HOUSESTYLE R12, R13, R19 and R23 — the change is to capture them per work, while
the work is in progress, instead of after the fact.

`notation.md` is a short, human-readable list of decisions with a one-line rationale each. Every
batch subagent reads it before transcribing and returns any new decision it had to make; the main
session appends. It is optional (absent for a short work), reviewable in the PR diff, and correctable
by hand — none of which is true of context memory.

*Alternative considered — pass the full previous fragments into each batch:* recovers prose
continuity but reintroduces linear growth in text, and does not capture the *reasoning* behind a
rendering choice. The trailing-lines handoff (D3) covers the part that actually matters.

### D3. Batch boundaries get a trailing-lines handoff

Within a batch of 8, seven of the eight page boundaries are internal — the subagent holds all eight
pages at once, so local comparison is fully preserved. Only the boundary between batches needs a
handoff: the last ~15 lines of the previous batch's final fragment, passed as context, so a sentence
or display formula split across the break is joined correctly. This is the same mechanism
`pipeline/transcribe.py` already uses ("previous page's tail"), so the approach is settled in the
repo's own design.

### D4. Verification is a separate per-batch subagent

Today's Phase 5 re-reads pages "for free" because they are still resident — and that residency is
exactly what is being paid for. Verification instead becomes a per-batch subagent that reads the
fragment plus that batch's images in a fresh context and returns only a discrepancy list. Cost is
bounded the same way; the images are read twice in total, which is cheap precisely because neither
read persists.

### D5. One text-block crop per page, at 1568px on the long edge

**Corrected during implementation — the original rationale for this decision was wrong.** It claimed
that cropping margins would buy half-page resolution at full-page cost. It does not. The 1568px cap
applies to the image's **long edge**, which on a portrait page is the *height*, so the page height
consumes the budget and the text width takes what is left — regardless of how much margin is
removed. Measured on the Clebsch scans:

| | source | after the cap | text width |
|---|---|---|---|
| full page `p207.jpg` | 1400×1859 | 1180×1568 | **1180px** |
| half crop `c207a.jpg` | 1500×1062 | *not downscaled* | **1500px** |

A half-page crop is landscape, so its long edge falls under the cap and it is not downscaled at all.
Cropping cannot close that gap: the margins on these scans are ~10%, and the helper's detected crop
boxes came back at 88–95% of the page.

So this is a genuine trade, not a free lunch: **1180px vs 1500px of text width, 2375 vs 4274 tokens,
2 vs 3 turns per page.** The helper measured 2,375 tokens/page over pp. 207–214.

The decision is still to default to one image per page, for two reasons. Turns dominate — `t·(B+P)`
is three quarters of the cost — so the turn saved is worth more than the tokens saved. And there is
direct evidence the lower resolution suffices: **Abel 1841's 91 pages were transcribed at exactly
1147×1568** and are in the corpus.

But the resolution loss is real, so it is paid for **per page, on demand** rather than avoided
blanket-wise — see D5a.

The helper is standard-library/PyYAML-only and lives in `pipeline/` but is **not** imported by
`validate.py` — the gate keeps its single dependency and CI stays AI-free and image-library-free.
Pages where auto-crop is unsafe (a fold, a plate, a skewed scan) fall back to manual crops; the
skill must not fail the run over a crop it could not compute.

**The measurement promoted this from a nice-to-have to the single largest lever.** Its value is not
the image tokens it saves but the **turn** it saves: one image per page makes a page one `Read` plus
one `Write`, cutting `t` from 3.4 to 2. Since `t·(B+P) = 212k/page` is three quarters of the cost,
that is worth more than any batch-size choice:

| scenario | N* | tokens/page | vs 4.2M baseline |
|---|---|---|---|
| as measured (two half-crops, full HOUSESTYLE) | 1.6 | 254k | 16.5× |
| one crop, no escalation (*optimistic ceiling*) | 2.4 | 153k | 27.5× |
| **one crop + escalation on 25% of pages** | 2.2 | 170k | **24.6×** |
| **  + trimmed style payload** | 2.1 | 149k | **28.2×** |
| one crop + escalation on 50% of pages | 2.1 | 188k | 22.3× |
|   + trimmed style payload | 1.9 | 164k | 25.6× |

The no-escalation row is a ceiling, not a forecast: it assumes every page is legible at 1180px.
**Plan on ~20–28×, and let the group 5 measurement decide where in that band this lands** — the
escalation rate is the unknown, and it is a property of the scan, not of the design.

Trimming the style payload is the second lever: `HOUSESTYLE.md` is 36KB (~10k tokens) and every
subagent re-reads all of it, though most of its 26 rulings concern site rendering rather than
transcription. A transcription-relevant extract cuts `P` from ~12.7k to ~4k.

### D5a. Per-page escalation, capped

Since one image per page costs ~21% of the text width (D5), the subagent MUST be able to buy that
resolution back where it actually matters: by cropping and magnifying a *specific doubtful region*
into its own scratch directory. Targeted magnification beats blanket half-pages because it spends
turns only on the pages that need them — and the pages that need them announce themselves, since the
alternative to magnifying is raising `\uncertain{}`.

This is also a correctness requirement, not only a cost one. The N=12 run could not magnify at all —
the browser zoom does not operate on local files and the isolation rule forbade writing crops — so it
flagged rather than guessed. That was the right behavior, but it means **its flag rate measured the
tooling it was given, not the legibility of the scan**, which is exactly the confound that would make
group 5's quality comparison meaningless.

**Escalation MUST be capped** (default 3 magnified regions per page). Given the capability and no
cap, the glossary-test run made **32 zoom crops for 4 pages** — about 8 per page, which would add
more turns than the half-page approach it replaces and undo the whole saving.

### D6. Rollout is gated on an A/B diff, not on judgment

Clebsch 189–206 is transcribed and committed under the current architecture. Re-transcribing a
sample of those pages under the new one and diffing against the committed text measures quality
change directly, on the same work and the same scans. Substantive divergence blocks the rollout;
markup-only divergence is triaged against `houselint`. This runs before the remaining 37 pages are
committed.

### D7. Uncertainty flags become observable

All three measured works carry zero `\uncertain{}` and zero `\illegible` across 151 pages, so there
is presently no signal for where the model was unsure — and no way to see a quality regression.
The batch report carries a flag count, provenance records the total, and the review checkpoint shows
it. A zero stays possible; it just stops being invisible.

## Risks / Trade-offs

**Glyph disambiguation by comparison is genuinely lost.** A smudged character on page 220 that a
human (or a model holding the whole work) would resolve by recalling a clean instance on page 195 is
not recoverable from a batch of 8 plus a glossary. → `notation.md` catches the case where the symbol
is part of the work's known inventory, which is the common one; the verification pass catches some of
the rest; D7 makes the residue visible as flags instead of silent guesses. This is a real, accepted
reduction in the best case — against which the current design's actual behavior is the honest
comparison: Abel compacted at turn 1071 and lost its early pages outright, and attention over 900k of
context is not attention over 60k.

**Subagent reports are the only window into the transcription.** The contributor no longer watches
each page go by. → The report contract is fixed and includes pages written, flags raised, and
decisions added; fragments land on disk as `pages/pNNN.tex` and are reviewable per page in the PR
diff; the Phase 8 checkpoint is unchanged.

**A subagent may drift from house style in a way the main session cannot see.** → `houselint` runs
over each batch's fragments as they land, not only over the assembled `original.tex`, so drift
surfaces at the batch that caused it.

**Batch size is tuned on an estimate.** The ~35k subagent baseline is inferred from the main
session's observed ~39k cache floor; no prior run in this project used subagents, so it is unmeasured.
→ The first real batch reports actual context, and N is adjusted before committing to a long work.

**Fixed per-batch overhead could erase the savings on short works.** For a 5-page work, one subagent
plus orchestration costs more than just reading 5 pages inline. → The skill transcribes inline below
a threshold (~2 batches' worth) and switches to the batch loop above it.

## Migration Plan

1. Land the crop helper and the skill rewrite together; neither changes corpus content.
2. Run the D6 A/B on Clebsch 189–206 and record measured tokens/page against the 4.2M baseline.
3. On a clean A/B, transcribe Clebsch 207–243 with the new loop — the first real use.
4. Fold the delta spec into `openspec/specs/transcription-pipeline/spec.md` and archive.

Rollback is reverting `SKILL.md`; the crop helper and any `notation.md` written are inert on their
own, and no corpus content produced under the new loop differs in format from content produced under
the old one.

## Open Questions

None outstanding.

## Resolved

- **The A/B's mechanical checks are a sampler, not a gate** (decided 2026-08-31). A diff against the
  committed text plus a `houselint` comparison is necessary but **not sufficient** to green-light
  the rollout, for three reasons each observed in this change's own measurement:
  - *`houselint` has no opinion on faithfulness.* All 16 fragments from the two clean batches passed
    it, and p. 207 still carried the wrong summation glyph and six wrong multiplication dots. It
    checks presentation rulings, not whether the LaTeX matches the page.
  - *A perfect diff score can mean the opposite of quality.* The contaminated first run scored 1.000
    similarity because it had copied the committed file.
  - *The diff compares the new text to the old text, not to the scan.* The baseline pages are
    `ai-draft` and were never human-verified, so an error both versions share passes silently, and
    where they disagree the diff cannot say which side is right — settling `\sum` versus `\Sigma`
    took reading the scan.

  So the checks are run to **narrow the sample to its decision points**, and those points are then
  adjudicated against the scan — by the contributor, or by a verification subagent reading the page
  images. This stays cheap because decisions are far fewer than divergences: across 18 pages the two
  batches produced 25 divergent spots but only **two** decisions to settle. The rollout proceeds when
  every substantive divergence has been adjudicated against the scan and recorded in `notation.md`;
  markup-only divergence does not block. Byte-identical output fails as contamination rather than
  passing as agreement.

- **`notation.md` is a permanent corpus artifact** (decided 2026-08-31). It is committed with the
  transcription and kept after the work reaches `verified`; `corpus-format`'s work-directory layout
  is amended to list it. It records what a later transcriber, translator, or reviewer would
  otherwise re-derive from the scan, and it makes those decisions reviewable in a PR diff rather
  than implicit in the LaTeX. The first real one is
  `corpus/clebsch-1864-anwendung-abelschen-functionen/notation.md`.
- **The glossary works, and it transmits precision but not vagueness** (tested 2026-08-31). An
  isolated batch given `notation.md` transcribed p. 223 with the Sigma letter **19 times and `\sum`
  zero times** — the exact mirror of the pp. 207–210 batch, which without the glossary wrote `\sum`
  19 times and `\Sigma` zero. Same work, same model, same isolation; the glossary is the only
  difference. It also obeyed the "never `\cdot`" rule exactly (0 occurrences).
  **But the same run exposed the mechanism's failure mode.** That entry said only that "the spacing
  around it is normalized", and the run set 11 *spaced* dots where pages 189–206 set 63 *tight*
  ones. A vague entry does not merely fail to help — it licenses a new divergence. Glossary entries
  MUST be exact and MUST say what not to do; the corrected entry now pins tight spacing explicitly
  and names the one context where `\cdot` is legitimate. Implication for the skill: when a batch
  reports a new decision, the orchestrating session must write it down at that precision, not
  paraphrase it.
- **The cross-batch divergence this is meant to prevent is real, not hypothetical** (observed
  2026-08-31). Two isolated batches of the same work disagreed on its most frequent symbol: the
  pp. 207–210 batch rendered Clebsch's summation sign `\sum` 19 times, while pp. 189–206 and the
  independently-run pp. 211–222 batch both used the Sigma letter `\Sigma` (21× and 32×). The scan
  confirms one slanted sigma letter throughout, and p. 207 was conformed before assembly. Both
  batches had been told to read `corpus/HOUSESTYLE.md`; the rulings log does not cover this work's
  sigma, which is exactly the gap a per-work glossary fills.
