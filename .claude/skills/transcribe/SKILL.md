---
name: transcribe
description: >-
  Transcribe scanned pages of a public-domain mathematics or physics text into
  house-style LaTeX and assemble them into the ReadTheMasters corpus, then open a
  pull request. Use when the user runs `/transcribe <work-id> <pages>`, or asks to
  transcribe a work's scan pages into the corpus. This is the Tier-2 contributor
  path (PLAN.md §4.1, §10): Claude Code does the vision transcription on the
  contributor's own account — the project pays for no AI compute.
---

# Transcribe a work into the corpus

You are running the repository's semi-automatic transcription pipeline. You (Claude Code, with
vision) play the role the Batch API plays in a Tier-3 run: you read the scan pages directly and
emit faithful, house-style LaTeX, then assemble, validate, and open a PR. **The human contributor
reviews before anything is pushed.**

Invocation: `/transcribe <work-id> <pages>` — e.g. `/transcribe fagnano-1718-lemniscata 293-297`.
Both arguments may be omitted; ask for whatever is missing.

## Non-negotiables (read first)

1. **The copyright gate is absolute.** Never transcribe or open a PR for a work that does not pass
   `pipeline/validate.py`. If `work.yaml` is missing sourced copyright facts, STOP at Phase 1 and
   resolve that first — the gate evaluates BOTH life+70 and the US 95-year rule, plus edition
   rights and translation provenance (`openspec/specs/copyright-gate/spec.md`).
2. **Faithful content, standardized markup.** Transcribe exactly what is printed. Never modernize
   notation, correct the author, or paraphrase. Standardize only LaTeX markup. The full rules are
   in `prompts/transcribe-chat.md` and the rulings log in `corpus/HOUSESTYLE.md` — treat both as
   authoritative and read them before you transcribe.
3. **Honest provenance.** Machine output ships as `ai-draft`. Do not set a higher status than the
   review that actually happened (see the status ladder in PLAN.md §4.3: `ai-draft` → `skimmed` →
   `verified`).
4. **You do not decide public-domain status.** You compute it from sourced facts via the gate. If
   in doubt, surface it to the contributor; do not guess.

## Before you start

Read these so your output matches the house style exactly:

- `prompts/transcribe-chat.md` — the canonical transcription rules and current `prompt_version`.
- `corpus/HOUSESTYLE.md` — the notation-vs-presentation principle and the rulings log (R1–R10).
- `corpus/preamble/readmasters.sty` — the macros available (`\origpage`, `\uncertain`,
  `\illegible`, `\ednote`, `\rmfigure`).
- An existing work as a shape reference, e.g. `corpus/fagnano-1718-lemniscata/`.

## Phase 1 — Locate the work and clear the gate

1. If `corpus/<work-id>/work.yaml` exists, read it. Otherwise the work is new:
   - Help the contributor create `corpus/<work-id>/work.yaml` from
     `.claude/skills/transcribe/templates/work.yaml`. The `<work-id>` follows PLAN.md §3.2
     (Wikidata QID → DOI → `author-year-shorttitle` slug) and must equal the directory name.
   - Every copyright-critical fact (author death dates, first-publication year, edition) MUST be
     **sourced** in the `sources:` block, or the gate fails by design.
2. Fill/refresh the `copyright_assessment` block by running the gate in write mode, then reviewing
   the diff — never hand-write the verdicts:

   ```bash
   python pipeline/validate.py --write
   git diff corpus/<work-id>/work.yaml
   ```

3. Confirm the work is public domain. If `public_domain: false`, STOP and tell the contributor
   which rule failed — this work cannot be published.

## Phase 2 — Acquire the scan pages

- Use `source.scan_url` / `scan_id` in `work.yaml` to locate the pages named in `<pages>`.
- If the contributor has the images/PDF locally, use those. If pages must be downloaded, confirm
  the source and the page range with the contributor first (downloading is a side effect).
- Work in small batches (a few pages) so quality stays high, exactly as the chat prompt advises.

## Phase 3 — Transcribe, page by page

For each page, following `prompts/transcribe-chat.md` and `corpus/HOUSESTYLE.md`:

- Start the page with `\origpage{N}` (N = the printed page number).
- Transcribe faithfully: keep the author's spelling, symbols, and notation (`zz` for z², archaic
  spelling, `arc.`); normalize typography only (Fraktur/long-ſ → normal letters, expand ligatures,
  drop line-break hyphenation).
- Mark anything you are unsure of with `\uncertain{...}`; use `\illegible` for unrecoverable text.
  These are honest flags for the reviewer — prefer them over a confident guess.
- For a figure, emit `\rmfigure{figures/fig-XX.png}{<figure number only>}{<alt text>}` — do **not**
  redraw it. The crop is added separately.
- Reproduce apparent printer's errors faithfully and note them for the reviewer (ruling R4); never
  silently "fix" the author.

## Phase 4 — Stitch and normalize

- Assemble the page fragments in order into `corpus/<work-id>/original.tex`, wrapped in the
  standard document scaffold (see any existing `original.tex`):

  ```latex
  \documentclass{article}
  \usepackage{readmasters}
  \begin{document}
  ... your \origpage-delimited body ...
  \end{document}
  ```

- One cleanup pass: fix heading structure (`\section*{}` only where the source has a heading),
  paragraph breaks, and macro consistency. Keep a leading comment noting the source and that this
  is a faithful transcription (match the style of existing files).

## Phase 5 — Verification pass

Re-read the assembled `original.tex` against each scan page:

- Check every formula, equation number (`\tag{n}`), label, and `\origpage{N}` against the image.
- Where the transcription and the scan disagree, fix it or flag it with `\uncertain{}`.
- Keep a short list of the pages you flagged; it goes into provenance and the PR body.

## Phase 6 — Write provenance

Create/update `corpus/<work-id>/provenance.yaml` (see the template and existing works):

```yaml
transcription:
  status: ai-draft            # machine output; a human has not yet checked it
  model: claude-opus-4-8      # the model you are actually running as
  effort: high                # your thinking/effort level, or null if unknown
  prompt_version: transcribe-v1   # match prompts/transcribe-chat.md
  submitted_via: skill
  produced: "YYYY-MM-DD"      # today
  verification: { flagged_pages: [...], date: "YYYY-MM-DD" }
```

Set `status: ai-draft` unless the contributor tells you they have reviewed it against the scan —
only then may it be `skimmed`, recorded with a `reviewers:` entry naming them.

## Phase 7 — Validate

Both must pass before a PR:

```bash
python pipeline/validate.py
python -m pytest pipeline/tests -q
```

Fix any schema/vocab/gate errors. Vocabulary values (`discipline`, `tags`, `venue`, `type`,
`language`) must already exist in `corpus/vocab.yaml`; if a genuinely new value is needed, add it in
the same PR and say so.

## Phase 8 — Review checkpoint, then open the PR

1. **Show the contributor the result before pushing**: the rendered transcription (or a summary of
   what was transcribed), the flagged/uncertain passages, and the gate result. Give them the chance
   to correct anything. This checkpoint is required — do not skip straight to the PR.
2. Create a branch, commit with a DCO sign-off, and open the PR:

   ```bash
   git checkout -b transcribe/<work-id>
   git add corpus/<work-id>/
   git commit -s -m "Add <work-id> transcription (ai-draft)"
   gh pr create --fill
   ```

   The `-s` adds the `Signed-off-by` line the DCO requires (PLAN.md §11.1). Do not push to `main`.
3. In the PR body, state: pages covered, model + prompt_version, the flagged/uncertain pages, and
   that the status is `ai-draft` pending human review. Link the source scan.

## Notes

- **Translations** are a separate step (`prompts/translate-chat.md`, `translate-v1`): translate
  only from our own `original.tex`, preserve every math token and `\origpage` marker, and record
  `source: transcription` in provenance. A translation can be added in the same PR or a later one.
- Keep `prompt_version` in provenance in sync with the prompt file you followed. If you deviate
  from the pinned prompt, say so in the PR rather than silently recording the old version.
