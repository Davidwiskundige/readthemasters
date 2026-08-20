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

#### Scenario: Invoked to transcribe a work

- **WHEN** a contributor runs `/transcribe <work-id> <pages>`
- **THEN** the skill transcribes those scan pages into `corpus/<work-id>/` and opens a pull request

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

Before proposing anything, the skill SHALL re-read the assembled `original.tex` against each scan
page, resolve or flag discrepancies, and record the flagged pages in `provenance.yaml`.

#### Scenario: Discrepancies are flagged before proposing

- **WHEN** the verification pass finds a discrepancy between `original.tex` and a scan page
- **THEN** it is resolved or recorded as a flagged page in `provenance.yaml` before anything is proposed

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

### Requirement: CI and the gate stay AI-free

The Tier-3 path depends on the `anthropic` SDK, which SHALL be imported lazily and listed as a
contributor-only dependency. `pipeline/validate.py` and the CI test suite MUST NOT import it, so the
copyright gate and CI keep their single PyYAML dependency and cost the project nothing.

#### Scenario: Gate never imports the AI SDK

- **WHEN** `pipeline/validate.py` or the CI test suite runs
- **THEN** the `anthropic` SDK is not imported
