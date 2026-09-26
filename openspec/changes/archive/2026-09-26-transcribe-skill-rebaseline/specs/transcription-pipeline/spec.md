## MODIFIED Requirements

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

## ADDED Requirements

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
