# Change: translation-pipeline

## Why

The corpus has hand-made English translations but no reproducible way to produce them — Phase 4 of
the roadmap (PLAN.md §6) and the `translation-pipeline` proposal (PLAN.md §5) were never built. This
change adds that capability across both contributor tiers, mirroring `transcription-pipeline`: a
Tier-2 `/translate` Claude Code skill (free on a Pro/Max subscription) and a Tier-3
`pipeline/translate.py` Batch API script (a contributor's own API key). The Tier-1 chat prompt
(`prompts/translate-chat.md`) already exists; this completes the tiers and the product promise —
faithful transcription **and** readable translation.

Translation carries a risk transcription does not: the prose is rewritten while every formula,
label, and `\origpage{N}` marker must survive **unchanged** (PLAN.md §4.2). That invariant is
machine-checkable, so this change also adds `pipeline/texcompare.py` and wires it into the CI gate —
a translation that alters a formula fails the build, not just review. The `translation_source`
copyright rule (PLAN.md §2.2) is honored end to end: we translate only from our own `original.tex`,
recorded as `source: transcription` (already enforced by the gate).

## What changes

- Add `pipeline/texcompare.py`: extracts the invariant tokens (math spans, `\origpage` markers,
  label/ref keys, `\rmfigure` paths) from two LaTeX bodies and reports any that were altered,
  dropped, or added. Stdlib-only, so it runs in the free CI gate.
- Wire the check into `pipeline/validate.py`: every `translations/<lang>.tex` must reproduce its
  `original.tex`'s math/markers verbatim, or the gate fails. The three existing translations pass.
- Add `pipeline/translate.py`: a Batch API CLI (`python pipeline/translate.py <work-id> --lang en`)
  that clears the gate, chunks `original.tex` by `\origpage` boundaries, translates each chunk
  (pinned `translate-chat.md` prompt, prompt-cached, plus an optional per-work glossary), reassembles
  `translations/<lang>.tex`, runs the preservation check, writes `source: transcription` provenance,
  and stops for human review (no commit/push).
- Add `.claude/skills/translate/SKILL.md`: the Tier-2 phased workflow (gate → glossary → translate
  preserving math → assemble → preservation check → provenance → validate → review → DCO PR).
- Add `pipeline/tests/test_texcompare.py` and `pipeline/tests/test_translate.py`: unit tests for the
  pure logic, including that the real corpus passes and that a corrupted formula is caught. No
  network.
- Reuse `transcribe.py`'s generic helpers (`load_prompt`, `run_batch`, `_client`); `anthropic` stays
  a lazily-imported, contributor-only dependency.

## Impact

- New capability: `translation-pipeline` (Tier-2 skill + Tier-3 Batch API).
- The copyright gate gains a **new hard check** (math preservation) — additive; the existing corpus
  passes, and a translation that alters a formula now fails CI instead of merging.
- No change to corpus format or the site — translations are the same ordinary files, gated by CI.
- Honesty constraints match transcription: the gate is a hard precondition, output ships as
  `ai-draft`, `source: transcription` is mandatory, and a human-review checkpoint precedes the PR.
- CI stays AI-free: `texcompare.py` is stdlib-only and `anthropic` is never imported by the gate.
