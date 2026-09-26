# transcription-pipeline

## Purpose

How scan pages become a faithful, house-style LaTeX transcription in the corpus. Established by the
`transcription-skill` change (2026-07-22), which built the Tier-2 Claude Code path, and extended by
`transcription-pipeline-tier3` (2026-07-24), which added the Tier-3 Batch API path (PLAN.md §4.1).
All AI compute runs on the **contributor's** own account; the project runs only the free non-AI
gate in CI.
## Requirements
### Requirement: Tier-2 transcription skill

A Claude Code skill at `.claude/skills/transcribe/` SHALL transcribe a work's scan pages into
`corpus/<work-id>/` and open a pull request. Invoked as `/transcribe <work-id> <pages>` (both
arguments optional, requested interactively when absent). In a Claude Code run, Claude itself (with
vision) does the page-level transcription that the Batch API would do in a Tier-3 run.

The skill SHALL execute page-level transcription in **bounded context**, so that the cost of
transcribing a page does not grow with the number of pages already transcribed. The orchestrating
session MUST NOT read scan images itself. Instead it dispatches one subagent per batch of pages
(default 12, ending instead at a chapter, part, or article boundary within about three pages of that
mark, and not exceeding about 15), each of which reads only its own batch's images, writes one
fragment per page to `pNNN.tex`, and returns a text report naming the pages written, the uncertainty
flags raised, any notation decision it had to make, and the trailing lines of its final fragment.
Scan images therefore never enter the orchestrating session's context, and the assembly, validation,
review, and pull-request phases run with no images resident.

The default follows the price-weighted measurement in `transcribe-cost-rebaseline`: per-batch turns
do not grow with the batch, so larger batches cost less, and a 12-page batch was at least as accurate
as 4-page batches on the adjudicated pages, while a 28-page batch carried one agent's wrong
convention across every page.

Per-page fragments are **working files and live outside the corpus**, in the same scratch area as
the prepared page images. They are stitched into `corpus/<work-id>/original.tex`, which is what is
committed; `corpus-format`'s work-directory layout is the authority on what a work directory holds.

Each batch subagent SHALL receive the pinned `prompts/transcribe-chat.md` rules, a
**transcription-relevant extract** of `corpus/HOUSESTYLE.md` rather than the whole file, the work's
notation glossary when one exists, and the previous batch's trailing lines so that text spanning a
batch boundary is joined correctly. The extract is a maintained file, not something each run
re-derives: most of `HOUSESTYLE.md` governs site rendering rather than transcription, and every
subagent re-reads whatever payload it is sent.

Below a work size of about 8 pages the skill MAY transcribe inline in the orchestrating session,
because the fixed per-subagent overhead would otherwise exceed the saving. The threshold is absolute,
not a multiple of the batch size, so that raising the batch size does not move scan images into the
orchestrating session.

#### Scenario: Invoked to transcribe a work

- **WHEN** a contributor runs `/transcribe <work-id> <pages>`
- **THEN** the skill transcribes those scan pages into `corpus/<work-id>/` and opens a pull request

#### Scenario: Page images stay out of the orchestrating session

- **WHEN** a work large enough to batch is transcribed
- **THEN** the orchestrating session reads no scan image, and each batch's images are read only inside that batch's subagent

#### Scenario: Text spanning a batch boundary is joined

- **WHEN** a sentence or display formula continues across the boundary between two batches
- **THEN** the later batch receives the earlier batch's trailing lines and joins the text correctly

#### Scenario: A short work skips the batch loop

- **WHEN** the requested page range is smaller than about 8 pages
- **THEN** the skill may transcribe inline rather than dispatching subagents

#### Scenario: A batch ends at a nearby structural boundary

- **WHEN** a chapter, part, or numbered-article boundary known from earlier batches falls within about three pages of the 12-page mark
- **THEN** the batch ends at that boundary instead, and no batch exceeds about 15 pages

### Requirement: The gate is a hard precondition

The skill MUST NOT transcribe or open a PR for a work that fails `pipeline/validate.py`. For a new
work it authors `work.yaml` from `.claude/skills/transcribe/templates/work.yaml`, requires the
copyright-critical facts (author death dates, first-publication year, edition) to be **sourced**,
and fills `copyright_assessment` by running the gate in `--write` mode — never hand-writing the
verdicts. A work assessed `public_domain: false` is refused.

#### Scenario: Non-public-domain work is refused

- **WHEN** the work is assessed `public_domain: false`
- **THEN** the skill refuses to transcribe or open a PR

#### Scenario: Assessment is written by the gate, not by hand

- **WHEN** a new work's `copyright_assessment` is filled
- **THEN** it comes from running the gate in `--write` mode over sourced facts, not hand-written verdicts

### Requirement: Faithful transcription in house style

Output SHALL follow `prompts/transcribe-chat.md` and the rulings log in `corpus/HOUSESTYLE.md`: the
author's notation and spelling are preserved; only typography is normalized; each page begins with
`\origpage{N}`; uncertainty is flagged with `\uncertain{}`/`\illegible`; figures are never redrawn
(a `\rmfigure{}` placeholder is emitted for a separately-added crop); apparent printer's errors are
reproduced and flagged, never silently corrected.

#### Scenario: Printer's error is preserved and flagged

- **WHEN** the scan contains an apparent printer's error
- **THEN** the transcription reproduces it and flags it rather than silently correcting it

### Requirement: Verification pass

This requirement SHALL govern the Claude Code Tier-2 skill at `.claude/skills/transcribe/` only. The
corpus is transcribed by two skills whose cost dynamics differ on purpose — this one, built around
bounded-context subagents on Claude models, and the Antigravity skill at `.agents/skills/transcribe/`
built around Gemini 3.8 Flash's long context. Everything below about subagents, turns and
magnification governs the Claude Code skill; the Antigravity skill carries its own requirements in
this spec and is not bound by these.

Before proposing anything, the skill SHALL verify the transcription against each scan page, resolve
or flag discrepancies, and record the flagged pages in `provenance.yaml`.

Verification SHALL run in bounded context on the same terms as transcription: one subagent per
batch, reading that batch's fragments together with that batch's scan images in a fresh context and
returning only a discrepancy list. It MUST NOT depend on scan images still being resident from the
transcription phase.

Because each verification subagent re-reads its own images and consumes no other subagent's output,
the batch verifiers have no ordering dependency among themselves and SHALL be dispatched
**concurrently**.

The text-only proofread described below SHALL run **before** the batch verifiers, not after them,
and each verifier SHALL be given the proofread's `needs scan` findings for its own pages. A
`needs scan` finding is by definition one only the print can settle, and the verifiers are the only
pass that reads the print; resolving them afterwards requires a further subagent and a second
reading of the same images.

The model tier used for verification SHALL be recorded in `provenance.yaml`, so that a run's
verification tier is stated rather than inferred. A tier below the one used for transcription MAY be
used only where a like-for-like comparison on the same pages has shown it misses none of the
corrections the higher tier found.

The mechanical house-style linter (`pipeline/houselint.py`) SHALL run over each batch's fragments as
they land, not only over the assembled `original.tex`, so that a batch which drifts from house style
is identified as the batch that caused it.

**Verification against the scans is not sufficient on its own.** A per-batch pass compares page N's
text to page N's image, so it is structurally blind to any defect that spans a page or batch join,
or that makes two parts of the work disagree — which is the failure mode a batched architecture
most endangers. The skill SHALL therefore ALSO run a **text-only proofread of the assembled
`original.tex`**: one subagent, one context, reading the whole file together with the work's
notation glossary and **no scan images**, returning findings only.

That pass SHALL classify each finding as a **defect** (the transcription is internally broken), an
**inconsistency** (two parts of the work, or the work and its glossary, disagree), or **needs scan**
(only the print can settle it). It SHALL be given `provenance.yaml` so it does not re-report the
printer's errors already documented there. Its findings MUST be verified before they are acted on:
it cannot see the print, so a confident-sounding claim may be inference rather than observation.

This pass is cheap relative to what it covers — a 130KB work is roughly 32k tokens, about a
twentieth of the cost of scan-verifying the same pages — and it covers the whole work rather than
one batch. It runs once, over the assembled file, ahead of the batch verifiers.

#### Scenario: Discrepancies are flagged before proposing

- **WHEN** the verification pass finds a discrepancy between the transcription and a scan page
- **THEN** it is resolved or recorded as a flagged page in `provenance.yaml` before anything is proposed

#### Scenario: Verification re-reads its own images

- **WHEN** a batch is verified
- **THEN** its subagent reads that batch's scan images itself rather than relying on images read during transcription

#### Scenario: Batch verifiers run concurrently

- **WHEN** more than one batch is to be verified against the scans
- **THEN** their subagents are dispatched concurrently rather than one after another

#### Scenario: A needs-scan finding is settled by the pass that reads the scan

- **WHEN** the text-only proofread classifies a finding as `needs scan`
- **THEN** it is handed to the batch verifier covering that page, and settled during that verifier's own reading of the scan rather than by a further subagent afterwards

#### Scenario: The verification tier is recorded

- **WHEN** a transcription run completes
- **THEN** `provenance.yaml` states the model tier the verification pass ran on

#### Scenario: House-style drift is localized to its batch

- **WHEN** a batch's fragments violate a house-style ruling
- **THEN** `houselint` reports it as those fragments land, before the work is assembled

#### Scenario: A defect spanning a page join is caught

- **WHEN** a word, sentence, or convention is broken across a page or batch boundary
- **THEN** the text-only proofread reports it, even though every page passed its own check against its own scan image

#### Scenario: The proofread does not re-report documented misprints

- **WHEN** the work reproduces a printer's error that `provenance.yaml` already records under R4
- **THEN** the proofread leaves it alone rather than reporting it as a defect

#### Scenario: A proofread finding is verified before it is applied

- **WHEN** the text-only proofread asserts that some markup is broken
- **THEN** the claim is tested before any edit is made, because the pass cannot see the print and may be reasoning rather than observing

### Requirement: Honest provenance and status

Machine output SHALL be recorded as `status: ai-draft` with `model`, `effort`, `prompt_version`
(matching the prompt actually followed), `submitted_via: skill`, and the `produced` date. A higher
status on the ladder (`skimmed`, `verified`) is set only when a human has performed that level of
review, with a `reviewers:` entry naming them.

A transcription run also seeds a starter `changelog` entry in `provenance.yaml` —
`{date: today, summary: "Transcription added (AI draft)."}` — appended only when no entry with that
summary already exists, so re-running does not duplicate it and existing changelog entries are
preserved. Both the Tier-2 skill and the Tier-3 pipeline seed it (via
`validate.add_changelog_entry`); the entry is a starting point the maintainer may edit.

#### Scenario: Machine output recorded as ai-draft

- **WHEN** a transcription run completes
- **THEN** provenance records `status: ai-draft` with model, effort, prompt_version, `submitted_via: skill`, and the produced date

#### Scenario: Re-run does not duplicate the changelog seed

- **WHEN** a run seeds the starter `changelog` entry and an entry with that summary already exists
- **THEN** no duplicate is appended and existing entries are preserved

### Requirement: Human review checkpoint, then a DCO-signed PR

The skill SHALL present the transcription, the uncertain/flagged passages, and the gate result to the
contributor for correction **before** anything is pushed. It then validates
(`pipeline/validate.py` and `pytest pipeline/tests`), commits on a branch with a DCO `-s` sign-off
(never pushing to `main`), and opens a PR whose body states the pages covered, model,
`prompt_version`, flagged pages, source scan, and the `ai-draft` status pending review.

#### Scenario: Review precedes any push

- **WHEN** a transcription run finishes
- **THEN** the contributor reviews the transcription, flagged passages, and gate result before any commit, and the PR is a DCO-signed branch (never `main`)

### Requirement: Tier-3 Batch API pipeline

A script at `pipeline/transcribe.py` SHALL transcribe a work's scan pages into `corpus/<work-id>/`
using the Anthropic **Batch API**, run on the **contributor's** own account. Invoked as
`python pipeline/transcribe.py <work-id> --pages <spec> --images <dir>`, where `<spec>` is a page
range/list (e.g. `293-297`) and `<dir>` holds one image file per page named by its printed page
number. Model defaults to Claude Opus 4.8 for hard material, with a flag to select Claude Sonnet 5
for clean modern typography; the run records which was used.

The same honesty constraints as the skill apply and are enforced by the same artifacts: the gate is
a hard precondition (a work assessed `public_domain: false` by `pipeline/validate.py` is refused,
with the failing rule named); each page is one Batch request whose instructions are the pinned
`prompts/transcribe-chat.md` (prompt-cached shared prefix) plus the page image; fragments are
stitched by page order (never arrival order) into `original.tex` with the standard scaffold; a
verification pass on a cheaper model (default Claude Haiku 4.5, skippable with `--no-verify`) flags
discrepancies; provenance records `status: ai-draft`, `submitted_via: pipeline`, the model,
`effort`, `prompt_version`, `batch_ids`, and the verification-flagged pages; and the script writes
the corpus files and stops without committing, leaving the contributor to review, validate, and open
a DCO-signed PR.

#### Scenario: Fragments stitched by page order

- **WHEN** Batch requests return page fragments out of order
- **THEN** they are stitched into `original.tex` by page order, never arrival order

#### Scenario: Pipeline stops without committing

- **WHEN** the Tier-3 script finishes writing the corpus files
- **THEN** it stops without committing, leaving the contributor to review, validate, and open a DCO-signed PR

### Requirement: Per-work notation glossary

A work's cross-page rendering decisions SHALL be recorded in an optional
`corpus/<work-id>/notation.md` rather than held only in conversational context — how this work's
Fraktur, long-ſ, orthography, function-application notation, and comparable recurring choices are
rendered. Each entry is a short decision with a one-line rationale.

Every batch subagent MUST read the glossary before transcribing and MUST report any new decision it
had to make; the orchestrating session appends reported decisions. The glossary is reviewable in the
pull-request diff and correctable by hand. `pipeline/validate.py` MUST tolerate its presence and MUST
NOT require it — a work whose transcription needed no such decision has no glossary.

An author's own back-references (`équation (92)`, `Gleichung (3)`, section numbers) are printed on the
page being transcribed and are copied verbatim; they are not glossary entries and require no
knowledge of the referenced page.

#### Scenario: A recurring notation decision is carried across batches

- **WHEN** a batch subagent makes a rendering decision that will recur later in the work
- **THEN** it reports the decision, the orchestrating session records it in `notation.md`, and later batches read it before transcribing

#### Scenario: Glossary is optional

- **WHEN** a work is transcribed without needing any work-spanning notation decision
- **THEN** no `notation.md` is written and `pipeline/validate.py` passes

### Requirement: Text-block page crops

A helper in `pipeline/` SHALL prepare one image per scan page, cropped to the printed text block and
sized so its long edge does not exceed 1568 pixels — the point above which the vision API downscales.
One image per page is chosen because it makes a page one `Read` plus one `Write`, and turns dominate
the cost.

This trades resolution, and the trade MUST be acknowledged rather than designed around: the cap
applies to the LONG edge, which on a portrait page is the height, so a full page yields roughly
1180px of text width against a half-page crop's 1500px. Cropping margins does not close that gap.
The resolution is bought back per page by escalation, not avoided by splitting every page.

The helper MUST NOT be imported by `pipeline/validate.py` or the CI test suite, and MUST NOT import
the `anthropic` SDK, so the copyright gate and CI keep their single PyYAML dependency. Where an
automatic crop is unsafe — a fold, a plate, a skewed scan — the helper SHALL pass the page through
uncropped, report it, and continue, never failing a run over a crop it could not compute.

Detection SHALL NOT be a bounding box over every dark pixel, and its ink test SHALL be a **count of
dark pixels per row and column, not a fraction** of them. Both rules exist because the naive forms
fail silently, which is worse than failing loudly:

- A bounding box is set by its extremes, so one speck of dust or one nick in a page edge drags the
  box out to the whole scan and the crop quietly becomes a no-op. The helper therefore projects the
  ink onto each axis and keeps the rows and columns actually carrying type, having first eroded the
  mask and discarded a border fraction — the scanner background and the page edge live there and are
  dense enough to pass any ink test.
- A fraction rule drops a column of genuine but sparse type. Measured on Betti 1871, the right-hand
  columns of one page hold nothing but four flush-right equation numbers out of forty-five lines: a
  vanishing fraction, unmistakably type, and cropping them would have removed four `\tag` numbers
  from the transcription.

A detected block covering essentially the whole page SHALL be reported and refused rather than used.
It is not the untrusted-block case above — it looks large and plausible, so it passes any
"is this block big enough" test — and it means the ink threshold is counting the scanner background
as type. The threshold and the ink floor SHALL therefore be adjustable per run, since which value
works is a property of the scan and not something the helper can know in advance.

#### Scenario: A page is prepared for transcription

- **WHEN** the helper crops a scan page
- **THEN** it emits a single image of the printed text block whose long edge is at most 1568 pixels

#### Scenario: Auto-crop cannot be computed

- **WHEN** the helper cannot safely determine a page's text block
- **THEN** that page is passed through uncropped and reported, and the run continues

#### Scenario: A speck of dust does not defeat the crop

- **WHEN** a page carries isolated marks outside the printed text block
- **THEN** they are excluded from the detected block, and the crop is still tight to the type

#### Scenario: A sparse column of real type is kept

- **WHEN** a column of the text block holds only a few flush-right equation numbers
- **THEN** it is kept inside the crop, because the ink test counts pixels rather than proportions

#### Scenario: The ink threshold is saturated by the scan's background

- **WHEN** the detected text block covers essentially the whole page
- **THEN** the helper reports it and keeps the page uncropped, rather than accepting a crop that does nothing

#### Scenario: The gate stays dependency-free

- **WHEN** `pipeline/validate.py` or the CI test suite runs
- **THEN** the crop helper, Pillow, and the `anthropic` SDK are not imported

### Requirement: Capped per-page escalation

This requirement SHALL govern the Claude Code Tier-2 skill at `.claude/skills/transcribe/` only.
Magnification exists because that skill sends one downscaled image per page and must buy the lost
resolution back a region at a time. The Antigravity skill ingests high-resolution scans or split
tiles directly and is explicitly exempted from interactive `magnify.py` escalation by its own
requirement; nothing here binds it.

A batch subagent SHALL be able to crop and magnify a specific doubtful region of its own pages into a
scratch directory, and the number of magnified regions per page MUST be capped (default 3).

The capability is required because one image per page costs roughly 21% of the text width; without
it, a subagent's `\uncertain{}` flags measure the tooling it was given rather than the legibility of
the scan, which would invalidate any quality comparison. The cap is required because the capability
is used freely when ungoverned — an observed run produced 32 magnified crops for 4 pages, which would
add more turns than the one-image-per-page design removes.

Magnification SHALL be **batched**: a page's regions are produced by a single invocation of the
magnification helper, and a batch's invocations and crop reads are issued together rather than one
per turn. Per-region cropping is forbidden, because each region cropped on its own costs a
compute-and-save turn plus a read turn, and at a measured 1.7 regions per page that escalation tax
roughly doubled the turns per page — the dominant term in the cost of a run.

The per-page cap MUST hold **across invocations, not merely within one**. A second call for the same
page buys no further regions. Measured: a batch given a per-call cap took "3 + 1 follow-up" regions
on one page — inside the cap twice, past it in total — and silently overwrote its own first crop,
because output names restart at `r1` on each call.

**Batching is a property of the instruction, not of the helper, and MUST be stated to the subagent.**
Measured across five batches of four pages with identical tooling: a batch that wrote its four
fragments in four separate messages cost **12 turns**, against **4** for batches that issued the
reference reads, the chained magnification, the crop reads and the fragment writes as one message
each. Three times the cost for the same work. The instruction SHALL therefore tell the subagent to
issue every independent call together, naming the fragment writes explicitly.

Magnification is preferred over raising `\uncertain{}` where it settles the reading, and
`\uncertain{}` is preferred over guessing where it does not.

Each batch report SHALL additionally state how many regions it magnified — alongside the pages,
flags, notation decisions and trailing lines it already carries — so that a run which begins
magnifying freely once magnification is cheap is visible rather than silent.

#### Scenario: A doubtful glyph is magnified rather than guessed

- **WHEN** a subagent cannot resolve a glyph at the prepared page's resolution
- **THEN** it magnifies that region into its scratch directory rather than guessing, and flags `\uncertain{}` only if magnification does not settle it

#### Scenario: A page's regions are produced in one invocation

- **WHEN** a subagent needs more than one magnified region on the same page
- **THEN** it produces them all in a single invocation of the helper and reads them in a single turn

#### Scenario: A second call does not raise the per-page cap

- **WHEN** a subagent has already magnified the cap's worth of regions on a page and calls the helper again for that page
- **THEN** the helper refuses, rather than writing further crops or overwriting the ones already read

#### Scenario: Independent calls are issued together

- **WHEN** a batch subagent writes its fragments, or issues its magnification calls and crop reads
- **THEN** the calls that do not depend on one another are issued in a single message, because turns rather than tool calls are what re-send the fixed payload

#### Scenario: Escalation stays bounded

- **WHEN** a page would need more magnified regions than the cap allows
- **THEN** the subagent stops magnifying and flags the remaining doubtful passages instead

#### Scenario: Magnification volume is reported

- **WHEN** a batch subagent returns its report
- **THEN** the report states the number of magnified regions it used

### Requirement: Page-marker integrity is enforced by the gate

`pipeline/validate.py` SHALL check that a transcription's `\origpage{N}` markers form an ascending
run. Duplicate markers and descending order are **errors** that block publication; a gap is a
**warning**, because a work may legitimately transcribe a selection of pages rather than a
contiguous range.

This exists because a batched transcription assembles one fragment per printed page, so a dropped,
duplicated, or mis-ordered fragment is a real and silent failure mode. Nothing caught it before: the
gate never looked at page markers and `houselint` has no opinion on them.

The check SHALL strip LaTeX comments before extracting markers, since a file's header comment may
legitimately discuss a marker without being one. It stays stdlib-only, so the gate keeps its single
PyYAML dependency.

#### Scenario: A duplicated or mis-ordered fragment blocks publication

- **WHEN** an assembled `original.tex` repeats an `\origpage` number, or its markers descend
- **THEN** `pipeline/validate.py` fails and the work does not publish

#### Scenario: A deliberate page selection is not blocked

- **WHEN** a work transcribes a non-contiguous selection of pages
- **THEN** the gate warns which pages are skipped but does not fail

#### Scenario: A marker discussed in a comment is not counted

- **WHEN** a file's header comment mentions an `\origpage` marker in prose
- **THEN** the check ignores it rather than reporting a duplicate

### Requirement: Prepared pages carry a coordinate mapping back to the scan

The page-preparation helper SHALL emit, alongside the prepared images, a machine-readable mapping
from each prepared image's coordinate space back to its source scan — an offset and a scale per
page, such that `source = offset + prepared / scale`.

A batch subagent sees the prepared image but must magnify out of the source scan, which is cropped
and downscaled differently on every page. Without the mapping it has to infer one: a measured batch
that did so landed two of its three magnification crops on the wrong lines, spending its entire
per-page escalation budget without settling anything.

Emitting the mapping is a property of the shared page-preparation helper and therefore applies
whichever skill prepares the pages. The clause below concerns `magnify.py`, and so governs **the
Claude Code skill at `.claude/skills/transcribe/`** only.

The mapping SHALL be applied by the magnification helper rather than by the subagent. The subagent
names regions in the coordinate space of the image it can actually see — the prepared page — and the
helper converts them and crops from the source scan. Coordinate arithmetic performed by hand in a
subagent is a repeat of a measured failure, so it is not merely discouraged but replaced.

#### Scenario: A subagent magnifies without converting coordinates

- **WHEN** a batch subagent needs to magnify a doubtful region
- **THEN** it names the region in prepared-image coordinates and the helper converts them and crops from the source scan

#### Scenario: The mapping is emitted with the prepared pages

- **WHEN** pages are prepared for transcription
- **THEN** an offset and a scale per page are written alongside the prepared images

### Requirement: Uncertainty flagging is observable

The uncertainty flags a run produced SHALL be visible rather than silent. Each batch report carries
the count of `\uncertain{}` and `\illegible` markers raised in that batch; `provenance.yaml` records
the total for the run; and the human review checkpoint states it alongside the flagged pages.

A count of zero is permitted — a clean scan legitimately yields no flags — but it MUST be reported as
a zero, so that an absence of flags is distinguishable from an absence of flagging.

#### Scenario: Flag count reaches provenance and the checkpoint

- **WHEN** a transcription run completes
- **THEN** `provenance.yaml` records the total uncertainty-flag count and the review checkpoint states it

#### Scenario: Zero flags is reported, not omitted

- **WHEN** a run raises no uncertainty flags
- **THEN** the count is reported as zero rather than left unstated

### Requirement: CI and the gate stay AI-free

The Tier-3 path depends on the `anthropic` SDK, which SHALL be imported lazily and listed as a
contributor-only dependency. `pipeline/validate.py` and the CI test suite MUST NOT import it, so the
copyright gate and CI keep their single PyYAML dependency and cost the project nothing.

#### Scenario: Gate never imports the AI SDK

- **WHEN** `pipeline/validate.py` or the CI test suite runs
- **THEN** the `anthropic` SDK is not imported

### Requirement: Antigravity Tier-2 transcription skill

An Antigravity workspace skill at `.agents/skills/transcribe/SKILL.md` SHALL transcribe a work's scan pages into `corpus/<work-id>/` and open a pull request. Invoked within Antigravity as `/transcribe <work-id> <pages>` or in response to an agentic transcription instruction.

The skill SHALL leverage Gemini 3.8 Flash's multimodal long-context capabilities:
1. **High-resolution scan ingestion**: The skill SHALL NOT enforce lossy 1568px long-edge downscaling or require interactive multi-turn region-by-region crop calculation (`magnify.py`); it SHALL ingest high-resolution page scans or half-page splits directly.
2. **Global Phase 0 Notation Scan**: The skill SHALL scan all page images of the work prior to page-by-page transcription to generate a comprehensive `corpus/<work-id>/notation.md` glossary, eliminating cross-batch notation drift before text generation begins.
3. **Long-context retention**: The skill MAY retain the entire work's images and preceding transcriptions resident in context across turns.
4. **Thinking effort**: The skill SHALL instruct Gemini 3.8 Flash with `effort: high` for both transcription and verification, and record this setting in `provenance.yaml`.
5. **Invariants**: The skill SHALL enforce the copyright gate as a hard precondition (`pipeline/validate.py`), adhere strictly to `prompts/transcribe-chat.md` and `corpus/HOUSESTYLE.md`, and record status `ai-draft` pending human review.
6. **Direct execution without plan approval**: The skill SHALL execute immediately upon invocation without entering planning mode, creating `implementation_plan.md`, or pausing for user plan approval; human contributor review is held at Phase 8 before pushing to git.

#### Scenario: Invoked in Antigravity to transcribe a work
- **WHEN** a contributor asks Antigravity to transcribe a public-domain work
- **THEN** the skill executes the transcription pipeline and opens a pull request

#### Scenario: Direct execution without planning mode
- **WHEN** `/transcribe` is invoked in Antigravity
- **THEN** the skill begins Phase 1 immediately without creating an implementation plan or asking for approval

#### Scenario: Global notation scan before transcription
- **WHEN** transcribing a multi-page work
- **THEN** all scan pages are examined upfront to establish `notation.md` before any page fragment is emitted

#### Scenario: High-resolution scans without interactive magnification turns
- **WHEN** page scans contain fine mathematical subscripts and punctuation
- **THEN** high-resolution scans or split tiles are provided upfront without requiring interactive multi-turn `magnify.py` crop escalation

#### Scenario: Copyright gate blocks non-compliant works
- **WHEN** `pipeline/validate.py` fails or the work is not public domain
- **THEN** the skill refuses to transcribe or open a PR

### Requirement: Antigravity proofread-first verification sequencing

The Antigravity transcription skill SHALL execute a whole-work text-only proofread of the assembled `original.tex` **before** the scan verification pass, and route all findings classified as `NEEDS SCAN` directly into the scan verification pass so each page's scan is opened only once.

The skill SHALL run `pipeline/houselint.py` over each page fragment as it is written to identify house-style drift immediately before file stitching.

The skill SHALL record the verification model (e.g. `gemini-3-8-flash`) and an explicit total count of `uncertainty_flags` in `provenance.yaml`.

#### Scenario: Text-only proofreading routes needs-scan queries to scan verifier
- **WHEN** the assembled text is proofread
- **THEN** structural and linguistic issues are checked without images, and any reading requiring visual confirmation is handed to the scan verification pass as a targeted `needs scan` query

#### Scenario: Early house-style linting catches fragment issues
- **WHEN** a LaTeX fragment is written to scratch
- **THEN** `pipeline/houselint.py` validates the fragment before assembly into `original.tex`

#### Scenario: Verification model and uncertainty count recorded
- **WHEN** provenance is authored
- **THEN** `provenance.yaml` includes the verification model and the explicit integer count of uncertainty flags (including 0)

### Requirement: Skill metadata and path integrity testing

The automated test suite SHALL verify the structure, YAML frontmatter, and referenced path integrity of the Antigravity skill at `.agents/skills/transcribe/SKILL.md` via `pipeline/tests/test_skills.py`.

#### Scenario: Skill file and frontmatter validation
- **WHEN** pytest runs `pipeline/tests/test_skills.py`
- **THEN** it verifies that `.agents/skills/transcribe/SKILL.md` exists, contains valid YAML frontmatter with `name: transcribe` and a non-empty `description`, and all referenced repo paths and templates exist

### Requirement: Workspace and branch isolation for Tier-2 skills

Tier-2 transcription skills (both Claude Code and Antigravity) SHALL establish workspace and branch isolation before creating or modifying any work files in Phase 1, rather than deferring branch creation to Phase 8.

Single-session runs SHALL switch to a dedicated branch `transcribe/<work-id>` off `origin/main` at Phase 1 Step 0.

Concurrent or parallel transcription runs (running across multiple sessions, tools, or models) SHALL execute in isolated git worktrees (`git worktree add ../rtm-<work-id> -b transcribe/<work-id> origin/main`), ensuring independent working directories and indices so that in-progress work files and whole-corpus validation runs (`pipeline/validate.py`) in one session do not collide with or block other active sessions.

#### Scenario: Branch isolation established in Phase 1
- **WHEN** a transcription skill starts working on `<work-id>`
- **THEN** it creates or checks out the branch `transcribe/<work-id>` before generating or editing files, keeping `main` clean

#### Scenario: Concurrent transcription sessions use git worktrees
- **WHEN** multiple transcription sessions execute in parallel
- **THEN** each session runs in an independent git worktree, preventing `pipeline/validate.py` failures caused by partial works in sibling sessions

### Requirement: Transcription cost is measured at what it is billed for
Cost measurements of Tier-2 transcription runs SHALL report a price-weighted figure computed from a
per-model price table, SHALL reconstruct output tokens from context growth rather than from logged
usage, and SHALL read per-turn usage from persisted subagent transcripts where they exist. Raw token
volume MAY be reported alongside, and any comparison MUST state which of the two metrics it uses.

Logged `output_tokens` in Claude Code transcripts is a stream-start snapshot and undercounts output
by orders of magnitude on long replies; the plan meter weights usage approximately by API price, not
by raw volume. A cost model fitted to raw volume with logged output optimizes cache reads, the
cheapest token class, and cannot see thinking, the most expensive one.

#### Scenario: A run is re-scored
- **WHEN** `pipeline/measure_session.py` reports on a session with subagent transcripts
- **THEN** it prints, per subagent and in total, cache reads, cache writes by TTL, fresh input and
  reconstructed output, with the API-price cost of each and each one's share of the total
- **AND** it prints the raw-volume total separately, labelled as such

#### Scenario: Output is reconstructed
- **WHEN** a turn's logged `output_tokens` is smaller than the next turn's context growth minus the
  tool results fed into it
- **THEN** the reconstructed figure is used, and the visible/thinking split is reported as an
  estimate

#### Scenario: The instrument is checked against known answers
- **WHEN** the reconstruction is changed
- **THEN** its tests include a transcript whose true output is known, and the reconstructed total
  falls within 5% of it

### Requirement: Verification batches are sized independently of transcription batches

Tier-2 verification subagents SHALL each cover about 4 pages and SHALL be dispatched concurrently,
whatever the transcription batch size; a 12-page transcription batch is verified by three verifiers.

Verification's batch size was previously inherited from transcription. Decoupling it keeps
wall-clock short as transcription batches grow, and four adjacent pages still let a verifier compare
a doubtful glyph against a clearer instance nearby. Verification cost per page was flat across the
measured arms.

#### Scenario: A 12-page transcription batch is verified

- **WHEN** a transcription batch of 12 pages has landed and been proofread
- **THEN** three verification subagents of 4 pages each are dispatched in one message and run concurrently

### Requirement: Recommended effort is stated and recorded

The Tier-2 transcription skill SHALL state effort `medium` as the recommended setting for a run,
with the measured reason, and SHALL tell the contributor how to confirm the effort actually in use;
provenance MUST record the effort the run actually used.

A skill cannot set its session's effort, so this is a recommendation, not enforcement. On Opus 5.5,
`low` failed the kill criterion — its verifier introduced errors — and `medium` made no misreading on
the adjudicated pages where the Opus 5 `high` reference made two.

#### Scenario: A contributor starts a run

- **WHEN** the skill is invoked
- **THEN** it states that `medium` is recommended and how to check the session's effort before transcription begins

#### Scenario: A run used a different effort

- **WHEN** the session ran at an effort other than `medium`
- **THEN** provenance records the effort actually used, not the recommended one

### Requirement: Paragraph breaks at displays are verified against the scan

Each Tier-2 verification subagent SHALL check every paragraph break immediately before or after a
display against its scan — an indented next line is a new paragraph, a flush-left one is a
continuation — correct the fragment, and list each changed break in its discrepancy list.

This was the most frequent error in every measured run, the Opus 5 `high` reference included, and no
other pass can settle it: the proofread has no scan, and a new sentence after a display is not by
itself evidence of a new paragraph.

#### Scenario: A continuation after a display was set as a new paragraph

- **WHEN** a fragment has a blank line after a display and the print continues flush left
- **THEN** the verifier removes the break and lists the change

#### Scenario: A new paragraph after a display was run on

- **WHEN** a fragment has no blank line after a display and the print's next line is indented
- **THEN** the verifier inserts the break and lists the change

### Requirement: The magnification cap cannot be reset by the caller

`pipeline/magnify.py` SHALL enforce the per-page region cap per page and per pass (`transcribe` or
`verify`) through a ledger kept beside the prepared pages, independent of the output directory, and
MUST NOT allow a caller to raise the cap above its default; `pipeline/prepare_pages.py` SHALL clear
the ledger entries for the pages it prepares.

Counting crops in the output directory let a verifier take 7 regions on one page by writing to fresh
directories, and `--cap` let any caller raise the limit. The pass remains the caller's declaration;
the ledger makes a false one visible afterwards.

#### Scenario: A fresh output directory does not reset the cap

- **WHEN** a caller has used the cap for a page and pass, then calls again with a different `--out`
- **THEN** the helper refuses, naming the ledger and the regions already used

#### Scenario: Transcription and verification have separate budgets

- **WHEN** a page's transcriber used 3 regions and its verifier requests regions with `--pass verify`
- **THEN** the verifier's request is counted against its own cap of 3

#### Scenario: The cap cannot be raised

- **WHEN** a caller passes `--cap` above the default
- **THEN** the helper refuses; a lower `--cap` is accepted

#### Scenario: Re-preparing a page starts fresh

- **WHEN** `prepare_pages.py` prepares a page that has ledger entries
- **THEN** those entries are cleared

