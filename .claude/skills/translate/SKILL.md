---
name: translate
description: >-
  Translate a work's LaTeX transcription (original.tex) into another language as
  house-style LaTeX, preserving every formula and marker, and assemble it into the
  ReadTheMasters corpus, then open a pull request. Use when the user runs
  `/translate <work-id> <lang>`, or asks to translate a corpus work. This is the
  Tier-2 contributor path (PLAN.md §4.2, §10): Claude Code does the translation on
  the contributor's own account — the project pays for no AI compute.
---

# Translate a work into the corpus

You are running the repository's semi-automatic translation pipeline. You (Claude Code) play the
role the Batch API plays in a Tier-3 run: you translate our transcription's prose into the target
language while reproducing all mathematics verbatim, then assemble, check, validate, and open a PR.
**The human contributor reviews before anything is pushed.**

Invocation: `/translate <work-id> <lang>` — e.g. `/translate fagnano-1718-lemniscata en`. Both
arguments may be omitted; ask for whatever is missing. `<lang>` is a language code (`en`, `fr`, …).

## Non-negotiables (read first)

1. **The copyright gate is absolute.** Never translate or open a PR for a work that does not pass
   `pipeline/validate.py`. The work must already be public domain and already have an
   `original.tex` — you translate **only from our own transcription**.
2. **Translate only from our transcription (the `translation_source` rule, PLAN.md §2.2).** Never
   translate from an existing published translation, even to "check" your wording. Provenance
   records `source: transcription`, and the gate enforces it.
3. **Preserve the mathematics and structure verbatim.** Every math expression, `\tag{}`, label,
   `\ref`/`\eqref`, `\origpage{N}` marker, and `\rmfigure{path}{}{}` first argument must appear
   **unchanged**. Translate only prose and the human-readable caption/alt text. This is
   machine-checkable — `pipeline/texcompare.py` (and the CI gate) will reject an altered formula.
4. **Honest provenance.** Machine output ships as `ai-draft`. Do not set a higher status than the
   review that actually happened (PLAN.md §4.3: `ai-draft` → `skimmed` → `verified`).

## Before you start

Read these so your output matches the house style and translation rules exactly:

- `prompts/translate-chat.md` — the canonical translation rules and current `prompt_version`.
- `corpus/HOUSESTYLE.md` — the notation-vs-presentation principle and the rulings log.
- `corpus/preamble/readmasters.sty` — the macros (`\origpage`, `\uncertain`, `\ednote`, `\rmfigure`).
- An existing translation as a shape reference, e.g. `corpus/leibniz-1689-isochrona/translations/en.tex`.

## Phase 1 — Locate the work and clear the gate

1. Read `corpus/<work-id>/work.yaml` and `corpus/<work-id>/original.tex`. If `original.tex` does
   not exist, STOP — the work must be transcribed first (Tier-2 `/transcribe` or Tier-3).
2. Confirm the work is public domain:

   ```bash
   python pipeline/validate.py
   ```

   If it does not pass, STOP and tell the contributor which rule failed.

## Phase 2 — Glossary

- If `corpus/<work-id>/glossary.yaml` exists (or the contributor points you at an era glossary),
  read it and apply the term renderings consistently — including any period term to be **kept
  untranslated** (e.g. Leibniz's *potentia*). If none exists and the work has recurring specialized
  terminology, propose a short glossary and offer to save it alongside the work.

## Phase 3 — Translate, section by section

Working from `original.tex`, following `prompts/translate-chat.md`:

- Translate the prose into the target language in faithful, readable scholarly style; prefer
  period-appropriate terminology.
- Reproduce every math expression, symbol, equation number, label, and `\ref`/`\eqref`
  **unchanged**. Keep each `\origpage{N}` marker in place — they align the translation to the
  original. Keep `\section*{}`, environments, and `\rmfigure{}{}{}`; translate only the
  caption/alt text inside a figure, never the image path.
- For the author's own period technical term, prefer a literal untranslated rendering over an
  inline gloss; if a gloss is truly needed use **square brackets**, never parentheses. Put
  historical context in the work's significance note, not inside the translation.
- Use `\uncertain{...}` where you are unsure; add `\ednote{translator's note: …}` sparingly for a
  genuinely ambiguous rendering. Do not add or remove content.

## Phase 4 — Assemble

- Write `corpus/<work-id>/translations/<lang>.tex`, wrapped in the standard scaffold, with a
  leading comment noting it was made from `original.tex` (not an existing translation) and that
  math/markers are preserved (match an existing translation's header).

## Phase 5 — Preservation check + verification

- Run the math-preservation check; it must pass before you propose anything:

  ```bash
  python pipeline/texcompare.py corpus/<work-id>/original.tex corpus/<work-id>/translations/<lang>.tex
  ```

  If it reports a MISMATCH, fix the translation so every listed token matches the original — a
  changed formula is a bug, not a stylistic choice.
- Re-read the translation against `original.tex` section by section: the meaning should match and
  only the prose should differ. Note anything you flagged with `\uncertain{}` for the reviewer.

## Phase 6 — Write provenance

Update `corpus/<work-id>/provenance.yaml`, adding under `translations:`:

```yaml
translations:
  <lang>:
    status: ai-draft            # machine output; a human has not yet checked it
    model: claude-opus-4-8      # the model you are actually running as
    effort: high                # your thinking/effort level, or null if unknown
    prompt_version: translate-v1    # match prompts/translate-chat.md
    submitted_via: skill
    source: transcription       # REQUIRED — from our own original.tex (PLAN §2.2)
    produced: "YYYY-MM-DD"      # today
```

Preserve the existing `transcription:` block and any other languages. Set `status: ai-draft` unless
the contributor tells you they have reviewed it, in which case record a `reviewers:` entry.

## Phase 7 — Validate

Both must pass before a PR (the gate now includes the math-preservation check):

```bash
python pipeline/validate.py
python -m pytest pipeline/tests -q
```

## Phase 8 — Review checkpoint, then open the PR

1. **Show the contributor the result before pushing**: a summary of what was translated, the
   uncertain passages, the preservation-check result, and the gate result. Give them the chance to
   correct anything. This checkpoint is required.
2. Create a branch, commit with a DCO sign-off, and open the PR:

   ```bash
   git checkout -b translate/<work-id>-<lang>
   git add corpus/<work-id>/
   git commit -s -m "Add <work-id> <lang> translation (ai-draft)"
   gh pr create --fill
   ```

   The `-s` adds the `Signed-off-by` line the DCO requires. Do not push to `main`. In the PR body,
   state: work, language, model + prompt_version, `source: transcription`, uncertain passages, and
   that the status is `ai-draft` pending human review.

## Notes

- **Tier-3 equivalent:** `python pipeline/translate.py <work-id> --lang <lang>` runs the same flow
  via the Batch API on a contributor's own API key (paid). This skill is the free-on-subscription
  path; both produce identical corpus files gated by the same CI.
- Keep `prompt_version` in provenance in sync with `prompts/translate-chat.md`. If you deviate from
  the pinned prompt, say so in the PR rather than silently recording the old version.
