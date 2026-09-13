## Why

The per-batch-subagent architecture made per-page cost flat, but it landed at **509k tokens/page for
transcription and ~1.0M/page including verification** — 8.3× the old baseline, against the 20–28× the
design projected. The measurements name the reason precisely: **turns**. D5 assumed `t = 2` turns per
page; measured `t = 5.7` for transcription and ~4.9 for verification, because magnification runs at
1.7 crops per page and each crop costs a compute-and-save plus a read. The dominant cost term is
`t·(B+P)` — turns multiplied by the 62.7k fixed payload re-sent every turn — at ~212k of the 509k.

Wall-clock has the same shape: the batch verifiers run one after another even though nothing makes
them wait for each other.

We first asked whether to replace the reader entirely with an OCR-first pipeline. The answer is no,
and the evidence is recorded in `ocr-assessment.md` — it targets a few dollars per book and imports a
silent notation-drift class that `houselint` demonstrably cannot see. This change therefore attacks
the cost where the measurements say it lives.

## What Changes

- **Batch the magnification crops.** A new `pipeline/magnify.py` takes several regions for a page in
  one invocation, applies the `zoom-map.json` mapping itself, and writes all the crops at once. A
  subagent then produces a page's crops in **one Bash call and reads them in one turn** (parallel
  `Read`s in a single message), instead of the current 2 turns per crop. This is the single largest
  lever: at 1.7 crops/page it removes roughly 2.4 turns per page.
- **Run the verification subagents concurrently.** They have no ordering dependency at all — the
  spec already requires each to re-read its own images in a fresh context and forbids depending on
  transcription's residency. They are simply being run serially today. This is free wall-clock with
  no quality trade-off.
- **Run the text-only proofread before the batch verifiers, not after**, and hand each verifier the
  proofread's `needs scan` findings for its own pages. A `needs scan` finding is by definition one
  only the print settles, and the verifiers are the only pass that reads the print; today they
  arrive after that reading has finished and need a further subagent to resolve. Three waves become
  two, and each page's scan is read once.
- **A/B the verification pass on a cheaper model tier**, with a stated kill criterion. Verification
  is ~50% of the run's cost. PLAN.md §4.1 step 4 already envisages a cheap model here; it has never
  been measured. Adopt only if the A/B shows no regression.
- Provenance records the **verification model** for Tier-2 runs, which today it records only for
  Tier-3.
- Each batch report additionally states its **magnified-region count**, so that a run which starts
  magnifying freely once magnification is cheap is visible rather than silent.

**Transcription stays strictly sequential, one batch at a time.** Parallelizing it was considered and
rejected: see design D4. The trailing-lines handoff and the per-batch `notation.md` update are
unchanged.

Non-goal: changing what a faithful transcription is. `prompts/transcribe-chat.md` and
`corpus/HOUSESTYLE.md` are untouched.

## Capabilities

### New Capabilities

None. This changes how the existing pipeline spends its turns, not what it produces.

### Modified Capabilities

- `transcription-pipeline`: batched magnification replaces per-crop escalation turns and the
  magnification helper owns the coordinate conversion; the text-only proofread runs ahead of the
  batch verifiers and routes its `needs scan` findings to them; verification subagents run
  concurrently and may run on a cheaper model tier once measured; provenance records the
  verification model.

**Scope — this change governs the Claude Code skill only.** The corpus is transcribed by two skills
with deliberately different cost dynamics: `.claude/skills/transcribe/` on Claude models, built
around bounded-context subagents, and `.agents/skills/transcribe/` on Gemini 3.8 Flash, built around
its long context and high-resolution ingestion. The Antigravity skill carries its own requirements
in this spec and is explicitly exempt from `magnify.py` escalation. The three requirements this
change modifies are therefore scoped to `.claude/skills/` in the delta, so that a mandate written for
one skill's economics does not silently bind the other's.

## Impact

- **New**: `pipeline/magnify.py` (stdlib + Pillow only, consistent with `prepare_pages.py`), plus
  tests under `pipeline/tests/`.
- **Modified**: `.claude/skills/transcribe/SKILL.md` — Phase 3 (crop batching, report contents),
  Phase 5 (concurrent verification), Phase 6 (verification model in provenance).
- **Modified**: `openspec/specs/transcription-pipeline/spec.md` via this change's delta. The Tier-2
  transcription-skill requirement is **not** touched — sequential batching, the trailing-lines
  handoff and the glossary loop all stand as specified.
- **Unaffected**: `pipeline/validate.py`, CI, and the copyright gate stay dependency-free and AI-free.
  `pipeline/transcribe.py` (Tier-3) is already bounded per page and is not touched.
