# Change: transcription-skill

## Why

The corpus has only hand-made transcriptions. PLAN.md §4.1/§10 promise a **Tier-2** on-ramp — a
Claude Code skill, `/transcribe <work-id> <pages>`, that a Pro/Max contributor runs to transcribe a
work's scan pages semi-automatically and open a PR — and CONTRIBUTING.md and the site's Contribute
page already advertise it. It did not exist. This change builds it.

The skill is the first concrete implementation of the long-planned `transcription-pipeline`
capability. In a Claude Code run, Claude itself (with vision) plays the role the Batch API plays in
a Tier-3 run: it reads the scans and emits house-style LaTeX. The project still pays for no AI
compute — it runs on the contributor's own account.

## What changes

- Add `.claude/skills/transcribe/SKILL.md`: a phased workflow (locate work + clear the copyright
  gate → acquire scans → faithful page-by-page transcription → stitch → verification pass →
  provenance → validate → human review checkpoint → DCO-signed PR).
- Add `.claude/skills/transcribe/templates/work.yaml`: an annotated `work.yaml` template for new
  works, emphasizing sourced copyright facts and the controlled vocabulary.
- The skill reuses existing single-source-of-truth artifacts rather than duplicating them: the
  house-style rules (`prompts/transcribe-chat.md`, `corpus/HOUSESTYLE.md`), the shared preamble,
  and the gate (`pipeline/validate.py`).
- Un-mark the skill as "planned" in CONTRIBUTING.md.

## Impact

- New capability: `transcription-pipeline` (this is its first, Tier-2 implementation; the Tier-3
  Batch API path remains future work under the same capability).
- No change to the copyright gate, corpus format, or site — the skill is an authoring workflow that
  produces ordinary corpus files gated by the existing CI. Adding a work stays a plain PR.
- Honesty constraints are baked in: machine output ships as `ai-draft`, the gate is a hard
  precondition, and a human-review checkpoint precedes the PR.
