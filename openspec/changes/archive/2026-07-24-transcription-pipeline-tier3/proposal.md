# Change: transcription-pipeline-tier3

## Why

The `transcription-pipeline` capability shipped only its **Tier-2** path — the `/transcribe` Claude
Code skill (PLAN.md §10, tier 2). PLAN.md §4.1 and §7.4 also promise a **Tier-3** path: repo-local
Python scripts a technical contributor runs on their own API key, using the **Batch API** (−50%),
to transcribe a work's scan pages into house-style LaTeX and open a PR. CONTRIBUTING.md already
advertises this tier ("Run `pipeline/` scripts on their own API key"), but the script did not
exist. This change builds it, completing Phase 3 of the roadmap (PLAN.md §6).

Tier-3 is what makes full books practical: the skill (tier 2) runs interactively against
subscription rate limits, whereas the Batch API transcribes hundreds of pages in one non-latency-
critical job at half price. Both tiers produce the same corpus files gated by the same CI, and the
project still pays for no AI compute — the run is on the contributor's own account (principle 5).

## What changes

- Add `pipeline/transcribe.py`: a CLI (`python pipeline/transcribe.py <work-id> --pages <spec>
  --images <dir>`) that
  - refuses any work that is not `public_domain` per the gate (hard precondition, reusing
    `pipeline/validate.py`);
  - builds one **Batch API** request per scan page — the pinned `prompts/transcribe-chat.md`
    instructions (prompt-cached shared prefix) + the page image (the request shape also supports a
    previous-page tail for continuity; a full-book batch runs its pages in parallel, so cross-page
    continuity is caught by the verification pass and human review rather than by chaining output);
  - submits the batch, polls to completion, and stitches the per-page LaTeX fragments into
    `corpus/<work-id>/original.tex` with the standard scaffold;
  - runs a second-pass **verification** batch (cheap model re-reads each page against the scan and
    flags discrepancies) unless `--no-verify`;
  - writes `provenance.yaml` with `status: ai-draft`, `submitted_via: pipeline`, the model,
    `effort`, `prompt_version`, `batch_ids`, and the verification-flagged pages;
  - stops before committing so the contributor reviews, then validates and opens a DCO-signed PR
    (the same human-review checkpoint the skill enforces).
- Add `anthropic` to `pipeline/requirements.txt` as a **contributor-only** dependency, imported
  lazily so the free CI gate (`validate.py`) keeps its single PyYAML dependency.
- Add `pipeline/tests/test_transcribe.py`: unit tests for the pure logic (prompt/version parsing,
  page-range parsing, image→source encoding, request building, stitching, tail continuity,
  provenance shape) with no network calls.

## Impact

- Extends the shipped `transcription-pipeline` capability with its Tier-3 requirements; the Tier-2
  skill requirements are unchanged.
- No change to the copyright gate, corpus format, or site — Tier-3 produces the same ordinary
  corpus files gated by the existing CI. Adding a work stays a plain PR.
- Honesty constraints match the skill: the gate is a hard precondition, machine output ships as
  `ai-draft`, provenance is mandatory, and a human-review checkpoint precedes the PR.
- CI stays AI-free and free: `anthropic` is never imported by `validate.py` or the CI test run.
