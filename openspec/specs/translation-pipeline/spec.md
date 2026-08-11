# translation-pipeline

## Purpose

How a work's LaTeX transcription becomes a faithful, house-style translation in the corpus. Two
contributor tiers (PLAN.md §4.2, §10), both run on the **contributor's** own account; the project
runs only the free non-AI gate in CI. Established by the `translation-pipeline` change (2026-07-24).

## Requirements

### Requirement: Translate only from our own transcription

A translation SHALL be made **only** from our own `original.tex`, never from an existing human
translation (the `translation_source` copyright rule, PLAN.md §2.2). Provenance records
`source: transcription` for every hosted translation, and `pipeline/validate.py` fails any hosted
translation that is not derived from our transcription (or an explicitly licensed open translation).

#### Scenario: Translation not from our transcription is refused

- **WHEN** a hosted translation's provenance `source` is not `transcription` (or an explicitly licensed `external-open`)
- **THEN** `pipeline/validate.py` fails the build

### Requirement: Math and structure are preserved verbatim

Only prose SHALL be translated. Every math expression, `\tag{}`, label, `\ref`/`\eqref`,
`\origpage{N}` marker, and `\rmfigure{path}{}{}` image path MUST appear unchanged in the
translation; only the human-readable caption/alt text inside a figure is translated. This invariant
is machine-checkable: `pipeline/texcompare.py` extracts the invariant tokens from `original.tex` and
a `translations/<lang>.tex` and reports any dropped, added, or altered token.

#### Scenario: Altered formula is detected

- **WHEN** a translation drops, adds, or alters a math expression, tag, label, page marker, or figure path
- **THEN** `pipeline/texcompare.py` reports the mismatched token

### Requirement: The check is enforced in the CI gate

`pipeline/validate.py` SHALL run the preservation check on every `translations/<lang>.tex` against
its `original.tex` and **fail the build** on any mismatch — a translation that alters a formula does
not merge. The check is stdlib-only, so the gate stays AI-free and free.

#### Scenario: Mismatch fails the build

- **WHEN** the preservation check finds any mismatch in a `translations/<lang>.tex`
- **THEN** the gate fails the build and the translation does not merge

### Requirement: Tier-2 translation skill

A Claude Code skill at `.claude/skills/translate/` SHALL translate a work's transcription into a
target language and open a pull request, invoked as `/translate <work-id> <lang>`. Claude Code (with
no per-token billing on a Pro/Max subscription) does the translation the Batch API would do in a
Tier-3 run. It refuses a work that fails the gate or has no `original.tex`, follows
`prompts/translate-chat.md` and `corpus/HOUSESTYLE.md`, applies an optional per-work glossary, runs
the preservation check, and stops at a human-review checkpoint before a DCO-signed PR.

#### Scenario: Skill refuses an ineligible work

- **WHEN** `/translate` targets a work that fails the gate or has no `original.tex`
- **THEN** the skill refuses and opens no PR

### Requirement: Tier-3 Batch API pipeline

A script at `pipeline/translate.py` SHALL translate a work using the Anthropic Batch API on the
contributor's own account, invoked as `python pipeline/translate.py <work-id> --lang <code>`. It
clears the gate (public domain, and `original.tex` present), chunks the transcription by
`\origpage` boundaries, and issues one Batch request per chunk whose instructions are the pinned
`prompts/translate-chat.md` (prompt-cached shared prefix, with the target language filled in and any
`corpus/<work-id>/glossary.yaml` appended) plus the chunk. Chunks are reassembled in order into
`translations/<lang>.tex`. Model defaults to Claude Opus 4.8, selectable per run.

#### Scenario: Chunks reassemble in order

- **WHEN** the pipeline issues one Batch request per `\origpage` chunk
- **THEN** the returned chunks are reassembled in page order into `translations/<lang>.tex`

### Requirement: Honest provenance and status

The run SHALL record, under `translations.<lang>`, `status: ai-draft` with `model`, `effort`,
`prompt_version` (matching `prompts/translate-chat.md`), `submitted_via` (`skill` or `pipeline`),
`source: transcription`, the `produced` date, and (Tier-3) the `batch_ids`. It preserves the
`transcription:` block and other languages. A higher status on the ladder is set only by a human
reviewer, with a `reviewers:` entry.

The run also seeds a starter `changelog` entry in `provenance.yaml` —
`{date: today, summary: "Translation (<lang>) added (AI draft)."}` — appended only when no entry
with that summary already exists, preserving the transcription's entry and other languages' entries.
Both the Tier-2 skill and the Tier-3 pipeline seed it (via `validate.add_changelog_entry`); the
entry is a starting point the maintainer may edit.

#### Scenario: Machine output recorded as ai-draft

- **WHEN** a translation run completes
- **THEN** `translations.<lang>` records `status: ai-draft` with model, effort, prompt_version, submitted_via, and `source: transcription`

#### Scenario: Higher status requires a human reviewer

- **WHEN** a status above `ai-draft` is set
- **THEN** a `reviewers:` entry naming the human reviewer is present

### Requirement: Human review checkpoint, then a DCO-signed PR

Both tiers SHALL present the translation, the uncertain passages, the preservation-check result, and
the gate result to the contributor **before** anything is pushed; the Tier-3 script writes the files
and stops without committing. Validation (`pipeline/validate.py` and `pytest pipeline/tests`) and a
DCO `-s`-signed commit on a branch (never `main`) precede a PR whose body states the work, language,
model, `prompt_version`, `source: transcription`, and the `ai-draft` status pending review.

#### Scenario: Nothing is pushed before review

- **WHEN** a translation run finishes
- **THEN** the contributor reviews the output and gate result before any commit, and the PR is a DCO-signed branch (never `main`)

### Requirement: CI stays AI-free

The Tier-3 path depends on the `anthropic` SDK (reused from `transcribe.py`), which SHALL be imported
lazily and listed as a contributor-only dependency. `pipeline/validate.py`, `pipeline/texcompare.py`,
and the CI test suite MUST NOT import it, so the copyright gate and preservation check keep their
PyYAML + stdlib footprint and cost the project nothing.

#### Scenario: Gate never imports the AI SDK

- **WHEN** `pipeline/validate.py`, `pipeline/texcompare.py`, or the CI test suite runs
- **THEN** the `anthropic` SDK is not imported
