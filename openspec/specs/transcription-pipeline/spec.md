# Capability: transcription-pipeline

How scan pages become a faithful, house-style LaTeX transcription in the corpus. Established by the
`transcription-skill` change (2026-07-22), which built the Tier-2 Claude Code path. The Tier-3
Batch API path (PLAN.md §4.1) is future work under this same capability.

All AI compute runs on the **contributor's** own account; the project runs only the free non-AI
gate in CI.

## Requirement: Tier-2 transcription skill

A Claude Code skill at `.claude/skills/transcribe/` transcribes a work's scan pages into
`corpus/<work-id>/` and opens a pull request. Invoked as `/transcribe <work-id> <pages>` (both
arguments optional, requested interactively when absent). In a Claude Code run, Claude itself (with
vision) does the page-level transcription that the Batch API would do in a Tier-3 run.

## Requirement: The gate is a hard precondition

The skill MUST NOT transcribe or open a PR for a work that fails `pipeline/validate.py`. For a new
work it authors `work.yaml` from `.claude/skills/transcribe/templates/work.yaml`, requires the
copyright-critical facts (author death dates, first-publication year, edition) to be **sourced**,
and fills `copyright_assessment` by running the gate in `--write` mode — never hand-writing the
verdicts. A work assessed `public_domain: false` is refused.

## Requirement: Faithful transcription in house style

Output follows `prompts/transcribe-chat.md` and the rulings log in `corpus/HOUSESTYLE.md`: the
author's notation and spelling are preserved; only typography is normalized; each page begins with
`\origpage{N}`; uncertainty is flagged with `\uncertain{}`/`\illegible`; figures are never redrawn
(a `\rmfigure{}` placeholder is emitted for a separately-added crop); apparent printer's errors are
reproduced and flagged, never silently corrected.

## Requirement: Verification pass

Before proposing anything, the skill re-reads the assembled `original.tex` against each scan page,
resolves or flags discrepancies, and records the flagged pages in `provenance.yaml`.

## Requirement: Honest provenance and status

Machine output is recorded as `status: ai-draft` with `model`, `effort`, `prompt_version` (matching
the prompt actually followed), `submitted_via: skill`, and the `produced` date. A higher status on
the ladder (`skimmed`, `verified`) is set only when a human has performed that level of review, with
a `reviewers:` entry naming them.

## Requirement: Human review checkpoint, then a DCO-signed PR

The skill presents the transcription, the uncertain/flagged passages, and the gate result to the
contributor for correction **before** anything is pushed. It then validates
(`pipeline/validate.py` and `pytest pipeline/tests`), commits on a branch with a DCO `-s` sign-off
(never pushing to `main`), and opens a PR whose body states the pages covered, model,
`prompt_version`, flagged pages, source scan, and the `ai-draft` status pending review.
