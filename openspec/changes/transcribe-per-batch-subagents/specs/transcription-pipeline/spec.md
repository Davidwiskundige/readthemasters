## MODIFIED Requirements

### Requirement: Tier-2 transcription skill

A Claude Code skill at `.claude/skills/transcribe/` SHALL transcribe a work's scan pages into
`corpus/<work-id>/` and open a pull request. Invoked as `/transcribe <work-id> <pages>` (both
arguments optional, requested interactively when absent). In a Claude Code run, Claude itself (with
vision) does the page-level transcription that the Batch API would do in a Tier-3 run.

The skill SHALL execute page-level transcription in **bounded context**, so that the cost of
transcribing a page does not grow with the number of pages already transcribed. The orchestrating
session MUST NOT read scan images itself. Instead it dispatches one subagent per batch of pages
(default 4, adjustable), each of which reads only its own batch's images, writes one fragment per
page to `corpus/<work-id>/pages/pNNN.tex`, and returns a text report naming the pages written, the
uncertainty flags raised, any notation decision it had to make, and the trailing lines of its final
fragment. Scan images therefore never enter the orchestrating session's context, and the assembly,
validation, review, and pull-request phases run with no images resident.

Each batch subagent SHALL receive the pinned `prompts/transcribe-chat.md` rules, the applicable
`corpus/HOUSESTYLE.md` rulings, the work's notation glossary when one exists, and the previous
batch's trailing lines so that text spanning a batch boundary is joined correctly.

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

#### Scenario: Discrepancies are flagged before proposing

- **WHEN** the verification pass finds a discrepancy between the transcription and a scan page
- **THEN** it is resolved or recorded as a flagged page in `provenance.yaml` before anything is proposed

#### Scenario: Verification re-reads its own images

- **WHEN** a batch is verified
- **THEN** its subagent reads that batch's scan images itself rather than relying on images read during transcription

#### Scenario: House-style drift is localized to its batch

- **WHEN** a batch's fragments violate a house-style ruling
- **THEN** `houselint` reports it as those fragments land, before the work is assembled

## ADDED Requirements

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
sized so its long edge does not exceed 1568 pixels — the point above which the vision API downscales,
so that resolution above it is discarded while margin inside it displaces text.

The helper MUST NOT be imported by `pipeline/validate.py` or the CI test suite, and MUST NOT import
the `anthropic` SDK, so the copyright gate and CI keep their single PyYAML dependency. Where an
automatic crop is unsafe — a fold, a plate, a skewed scan — the skill SHALL fall back to a manual
crop for that page and continue, never failing a run over a crop it could not compute.

#### Scenario: A page is prepared for transcription

- **WHEN** the helper crops a scan page
- **THEN** it emits a single image of the printed text block whose long edge is at most 1568 pixels

#### Scenario: Auto-crop cannot be computed

- **WHEN** the helper cannot safely determine a page's text block
- **THEN** the skill falls back to a manual crop for that page and the run continues

#### Scenario: The gate stays dependency-free

- **WHEN** `pipeline/validate.py` or the CI test suite runs
- **THEN** the crop helper and the `anthropic` SDK are not imported

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
