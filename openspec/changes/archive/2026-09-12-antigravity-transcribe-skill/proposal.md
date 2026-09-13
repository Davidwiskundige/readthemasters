## Why

The existing Tier-2 transcription skill (`.claude/skills/transcribe/`) was architected around the cost profile and context limitations of Claude Opus: expensive input/vision tokens, severe penalties for image residency across turns, and tight context limits requiring narrow 4-page subagent batches and lossy image downscaling.

With contributors using Google Antigravity and Gemini 3.8 Flash, this cost distribution is inverted: multimodal input is ultra-cheap, the context window is 1M+ tokens, and high-effort thinking tokens are economical. Adding a native Antigravity skill in `.agents/skills/transcribe/` enables an optimized workflow that eliminates the resolution sacrifice, extracts work-wide notation upfront in a global scan, and performs comprehensive verification without Opus-style token parsimony.

Furthermore, recent findings from the Claude skill optimization (`transcribe-turn-cost`) demonstrate that reordering the pipeline—running a text-only proofreader before visual verification, running `houselint.py` early on fragments, and recording explicit verification models—drastically improves defect detection and eliminates stranded queries. Incorporating these pipeline improvements ensures the Antigravity skill reflects the project's state-of-the-art methodology.

## What Changes

- **Add Antigravity Tier-2 skill**: Create `.agents/skills/transcribe/SKILL.md` configured for Antigravity's discovery path and tool semantics.
- **High-resolution inputs upfront**: Remove the 1568px long-edge resolution cap and interactive crop budgeting for Antigravity runs; supply full-resolution or half-page tiles directly.
- **Phase 0 Global Notation Scan**: Ingest all document scans upfront into Gemini Flash's long context to generate `corpus/<work-id>/notation.md` before transcription begins, eliminating cross-batch notation drift at the root.
- **Early house-style linting**: Run `pipeline/houselint.py` over fragments as they land so house-style drift is caught immediately before stitching.
- **Optimized pipeline ordering**: Run the whole-work text-only proofread *before* scan verification; route classified `NEEDS SCAN` queries directly into the scan verification pass so each page's scan is opened only once.
- **Concurrent & resident verification**: Leverage long context and concurrent subagents to verify transcriptions against scans without losing cross-page context or leaving queries stranded.
- **High-effort thinking by default**: Instruct Gemini 3.8 Flash to run with high thinking effort (`effort: high`) across transcription and verification passes, recording `effort: high` in provenance.
- **Strict provenance**: Record `verification: { model: gemini-3-8-flash, flagged_pages: [...], date: ... }` and explicit `uncertainty_flags: N` (even when 0).
- **Automated skill testing**: Add `pipeline/tests/test_skills.py` to test frontmatter, referenced path integrity, and template validity in CI.
- **Keep invariants intact**: Retain the strict preconditions: the automated copyright gate (`pipeline/validate.py`), faithful house-style transcription (`HOUSESTYLE.md`, `prompts/transcribe-chat.md`), and the human review ladder (`ai-draft` status).

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `transcription-pipeline`: Expand Tier-2 requirements to support Google Antigravity agent environments at `.agents/skills/transcribe/` utilizing Gemini 3.8 Flash cost economics (long-context ingestion, upfront high-resolution scans, upfront global notation extraction) and optimized proofread-first verification sequencing with automated skill tests.

## Impact

- **New files**: `.agents/skills/transcribe/SKILL.md`, `.agents/skills/transcribe/templates/work.yaml`, and `pipeline/tests/test_skills.py`.
- **Modified specs**: `openspec/specs/transcription-pipeline/spec.md` (delta spec).
- **Tooling/Scripts**: Antigravity runs can invoke existing repo scripts (`pipeline/validate.py`, `pipeline/houselint.py`, `pipeline/texcompare.py`, `pipeline/prepare_pages.py`) directly via Antigravity command execution.
- **Existing Claude Code skill**: `.claude/skills/transcribe/SKILL.md` remains completely untouched and functional for Claude Code users.
