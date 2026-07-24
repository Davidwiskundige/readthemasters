# Capability: transcription-pipeline (delta)

Adds the **Tier-3 Batch API** requirements (PLAN.md §4.1, §7.4) to the existing capability. The
Tier-2 skill requirements are unchanged; these describe the repo-local Python path a technical
contributor runs on their own API key.

## Requirement: Tier-3 Batch API pipeline

A script at `pipeline/transcribe.py` transcribes a work's scan pages into `corpus/<work-id>/` using
the Anthropic **Batch API**, run on the **contributor's** own account. Invoked as
`python pipeline/transcribe.py <work-id> --pages <spec> --images <dir>`, where `<spec>` is a page
range/list (e.g. `293-297`) and `<dir>` holds one image file per page named by its printed page
number. Model defaults to Claude Opus 4.8 for hard material, with a flag to select Claude Sonnet 5
for clean modern typography; the run records which was used.

## Requirement: The gate is a hard precondition

The script MUST NOT transcribe a work that is not public domain. It reads `corpus/<work-id>/
work.yaml`, computes the copyright verdict via `pipeline/validate.py` (never hand-writing it), and
refuses — with the failing rule named — when the work is assessed `public_domain: false` or its
`work.yaml` is missing the sourced copyright-critical facts. The gate stays pure code with no AI.

## Requirement: One Batch request per page, in house style

Each page becomes one Batch request whose instructions are the pinned `prompts/transcribe-chat.md`
(prompt-cached as the shared prefix), followed by the page image. The request shape also carries an
optional previous-page tail for continuity; because a batch transcribes its pages in parallel,
cross-page continuity is caught by the verification pass and human review rather than by chaining
one page's output into the next. Output follows the house style enforced elsewhere
(`corpus/HOUSESTYLE.md`, the shared preamble): the author's notation and spelling are preserved,
only typography is normalized, each page begins with `\origpage{N}`, uncertainty is flagged with
`\uncertain{}`/`\illegible`, and figures are never redrawn.

## Requirement: Stitch into house-style LaTeX

The per-page fragments are reassembled in page order into `corpus/<work-id>/original.tex`, wrapped
in the standard `\documentclass{article}` / `\usepackage{readmasters}` / `document` scaffold, with a
leading provenance comment. Results are keyed by page (never by arrival order), since Batch results
return in arbitrary order.

## Requirement: Verification pass

Unless disabled with `--no-verify`, a second Batch pass on a cheaper model re-reads the assembled
transcription against each scan page and flags discrepancies. The flagged pages are recorded in
`provenance.yaml` and surfaced to the contributor.

## Requirement: Honest provenance and status

The run records `status: ai-draft` with `model`, `effort`, `prompt_version` (matching
`prompts/transcribe-chat.md`), `submitted_via: pipeline`, the `produced` date, the `batch_ids`, and
the verification-flagged pages. A higher status on the ladder is set only by a human reviewer, with
a `reviewers:` entry — the script never promotes past `ai-draft`.

## Requirement: Human review checkpoint, then a DCO-signed PR

The script writes the corpus files and stops — it does not commit or push. It surfaces the flagged/
uncertain passages and the gate result, then leaves the contributor to review, run
`pipeline/validate.py` + `pytest pipeline/tests`, commit with a DCO `-s` sign-off on a branch (never
`main`), and open a PR stating pages covered, model, `prompt_version`, flagged pages, source scan,
and the `ai-draft` status pending review.

## Requirement: CI stays AI-free

The Batch-API path depends on the `anthropic` SDK, which is imported lazily and listed as a
contributor-only dependency. `pipeline/validate.py` and the CI test suite MUST NOT import it, so the
copyright gate and CI continue to run with only PyYAML and cost the project nothing.
