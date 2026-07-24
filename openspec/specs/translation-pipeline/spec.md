# Capability: translation-pipeline

How a work's LaTeX transcription becomes a faithful, house-style translation in the corpus. Two
contributor tiers (PLAN.md §4.2, §10), both run on the **contributor's** own account; the project
runs only the free non-AI gate in CI. Established by the `translation-pipeline` change (2026-07-24).

## Requirement: Translate only from our own transcription

A translation is made **only** from our own `original.tex`, never from an existing human
translation (the `translation_source` copyright rule, PLAN.md §2.2). Provenance records
`source: transcription` for every hosted translation, and `pipeline/validate.py` fails any hosted
translation that is not derived from our transcription (or an explicitly licensed open translation).

## Requirement: Math and structure are preserved verbatim

Only prose is translated. Every math expression, `\tag{}`, label, `\ref`/`\eqref`, `\origpage{N}`
marker, and `\rmfigure{path}{}{}` image path MUST appear unchanged in the translation; only the
human-readable caption/alt text inside a figure is translated. This invariant is machine-checkable:
`pipeline/texcompare.py` extracts the invariant tokens from `original.tex` and a `translations/
<lang>.tex` and reports any dropped, added, or altered token.

## Requirement: The check is enforced in the CI gate

`pipeline/validate.py` runs the preservation check on every `translations/<lang>.tex` against its
`original.tex` and **fails the build** on any mismatch — a translation that alters a formula does
not merge. The check is stdlib-only, so the gate stays AI-free and free.

## Requirement: Tier-2 translation skill

A Claude Code skill at `.claude/skills/translate/` translates a work's transcription into a target
language and opens a pull request, invoked as `/translate <work-id> <lang>`. Claude Code (with no
per-token billing on a Pro/Max subscription) does the translation the Batch API would do in a
Tier-3 run. It refuses a work that fails the gate or has no `original.tex`, follows
`prompts/translate-chat.md` and `corpus/HOUSESTYLE.md`, applies an optional per-work glossary, runs
the preservation check, and stops at a human-review checkpoint before a DCO-signed PR.

## Requirement: Tier-3 Batch API pipeline

A script at `pipeline/translate.py` translates a work using the Anthropic Batch API on the
contributor's own account, invoked as `python pipeline/translate.py <work-id> --lang <code>`. It
clears the gate (public domain, and `original.tex` present), chunks the transcription by
`\origpage` boundaries, and issues one Batch request per chunk whose instructions are the pinned
`prompts/translate-chat.md` (prompt-cached shared prefix, with the target language filled in and any
`corpus/<work-id>/glossary.yaml` appended) plus the chunk. Chunks are reassembled in order into
`translations/<lang>.tex`. Model defaults to Claude Opus 4.8, selectable per run.

## Requirement: Honest provenance and status

The run records, under `translations.<lang>`, `status: ai-draft` with `model`, `effort`,
`prompt_version` (matching `prompts/translate-chat.md`), `submitted_via` (`skill` or `pipeline`),
`source: transcription`, the `produced` date, and (Tier-3) the `batch_ids`. It preserves the
`transcription:` block and other languages. A higher status on the ladder is set only by a human
reviewer, with a `reviewers:` entry.

## Requirement: Human review checkpoint, then a DCO-signed PR

Both tiers present the translation, the uncertain passages, the preservation-check result, and the
gate result to the contributor **before** anything is pushed; the Tier-3 script writes the files and
stops without committing. Validation (`pipeline/validate.py` and `pytest pipeline/tests`) and a
DCO `-s`-signed commit on a branch (never `main`) precede a PR whose body states the work, language,
model, `prompt_version`, `source: transcription`, and the `ai-draft` status pending review.

## Requirement: CI stays AI-free

The Tier-3 path depends on the `anthropic` SDK (reused from `transcribe.py`), imported lazily and
listed as a contributor-only dependency. `pipeline/validate.py`, `pipeline/texcompare.py`, and the
CI test suite MUST NOT import it, so the copyright gate and preservation check keep their PyYAML +
stdlib footprint and cost the project nothing.
