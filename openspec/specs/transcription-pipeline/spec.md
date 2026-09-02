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
(default 4, adjustable), each of which reads only its own batch's images, writes one fragment per
page to `pNNN.tex`, and returns a text report naming the pages written, the uncertainty flags
raised, any notation decision it had to make, and the trailing lines of its final fragment. Scan
images therefore never enter the orchestrating session's context, and the assembly, validation,
review, and pull-request phases run with no images resident.

Per-page fragments are **working files and live outside the corpus**, in the same scratch area as
the prepared page images. They are stitched into `corpus/<work-id>/original.tex`, which is what is
committed; `corpus-format`'s work-directory layout is the authority on what a work directory holds.

Each batch subagent SHALL receive the pinned `prompts/transcribe-chat.md` rules, a
**transcription-relevant extract** of `corpus/HOUSESTYLE.md` rather than the whole file, the work's
notation glossary when one exists, and the previous batch's trailing lines so that text spanning a
batch boundary is joined correctly. The extract is a maintained file, not something each run
re-derives: most of `HOUSESTYLE.md` governs site rendering rather than transcription, and every
subagent re-reads whatever payload it is sent.

Below a work-size threshold of about two batches the skill MAY transcribe inline in the
orchestrating session, because the fixed per-subagent overhead would otherwise exceed the saving.

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

- **WHEN** the requested page range is smaller than about two batches
- **THEN** the skill may transcribe inline rather than dispatching subagents

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

Before proposing anything, the skill SHALL verify the transcription against each scan page, resolve
or flag discrepancies, and record the flagged pages in `provenance.yaml`.

Verification SHALL run in bounded context on the same terms as transcription: one subagent per
batch, reading that batch's fragments together with that batch's scan images in a fresh context and
returning only a discrepancy list. It MUST NOT depend on scan images still being resident from the
transcription phase.

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
one batch.

#### Scenario: Discrepancies are flagged before proposing

- **WHEN** the verification pass finds a discrepancy between the transcription and a scan page
- **THEN** it is resolved or recorded as a flagged page in `provenance.yaml` before anything is proposed

#### Scenario: Verification re-reads its own images

- **WHEN** a batch is verified
- **THEN** its subagent reads that batch's scan images itself rather than relying on images read during transcription

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

#### Scenario: A page is prepared for transcription

- **WHEN** the helper crops a scan page
- **THEN** it emits a single image of the printed text block whose long edge is at most 1568 pixels

#### Scenario: Auto-crop cannot be computed

- **WHEN** the helper cannot safely determine a page's text block
- **THEN** that page is passed through uncropped and reported, and the run continues

#### Scenario: The gate stays dependency-free

- **WHEN** `pipeline/validate.py` or the CI test suite runs
- **THEN** the crop helper, Pillow, and the `anthropic` SDK are not imported

### Requirement: Capped per-page escalation

A batch subagent SHALL be able to crop and magnify a specific doubtful region of its own pages into a
scratch directory, and the number of magnified regions per page MUST be capped (default 3).

The capability is required because one image per page costs roughly 21% of the text width; without
it, a subagent's `\uncertain{}` flags measure the tooling it was given rather than the legibility of
the scan, which would invalidate any quality comparison. The cap is required because the capability
is used freely when ungoverned — an observed run produced 32 magnified crops for 4 pages, which would
add more turns than the one-image-per-page design removes.

Magnification is preferred over raising `\uncertain{}` where it settles the reading, and
`\uncertain{}` is preferred over guessing where it does not.

#### Scenario: A doubtful glyph is magnified rather than guessed

- **WHEN** a subagent cannot resolve a glyph at the prepared page's resolution
- **THEN** it magnifies that region into its scratch directory rather than guessing, and flags `\uncertain{}` only if magnification does not settle it

#### Scenario: Escalation stays bounded

- **WHEN** a page would need more magnified regions than the cap allows
- **THEN** the subagent stops magnifying and flags the remaining doubtful passages instead

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
per-page escalation budget without settling anything. The orchestrating session passes the relevant
rows to each batch.

#### Scenario: A subagent magnifies without guessing coordinates

- **WHEN** a batch subagent needs to magnify a doubtful region
- **THEN** it converts the coordinate using the supplied mapping rather than inferring the crop and scale

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
