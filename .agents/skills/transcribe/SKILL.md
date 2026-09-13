---
name: transcribe
description: >-
  Transcribe scanned pages of a public-domain mathematics or physics text into
  house-style LaTeX and assemble them into the ReadTheMasters corpus, then open a
  pull request. Use when the user runs `/transcribe <work-id> <pages>` or asks to
  transcribe a work's scan pages in Antigravity using Gemini 3.8 Flash.
---

# Transcribe a work into the corpus (Antigravity & Gemini 3.8 Flash)

You are running the repository's semi-automatic transcription pipeline in Google Antigravity.
You (with Gemini 3.8 Flash vision and reasoning) read scan pages directly, establish global
notational consistency, emit faithful house-style LaTeX, proofread and verify against the scans,
and assemble the submission for contributor review. **The human contributor reviews before anything is pushed.**

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
   authoritative.
3. **Honest provenance.** Machine output ships as `ai-draft`. Do not set a higher status than the
   review that actually happened (see the status ladder in PLAN.md §4.3: `ai-draft` → `skimmed` →
   `verified`).
4. **You do not decide public-domain status.** You compute it from sourced facts via the gate. If
   in doubt, surface it to the contributor; do not guess.
5. **Take the title from the print, not from a catalogue.** Catalogues (EuDML, Wikidata, libraries)
   routinely modernize spelling (ruling R12, e.g. `Variabeln` vs `Variablen`). Read the title line
   off the scan when you first see it.

## Architecture and Cost Model (Gemini 3.8 Flash)

In Gemini 3.8 Flash, the cost structure is inverted compared to legacy Claude Opus pipelines:
- **Multimodal input is ultra-cheap** and context is 1M+ tokens. You do not need to starve the model
  of resolution or enforce lossy 1568px long-edge downscaling that blurs subscripts. High-resolution
  scans or half-page split tiles are ingested directly upfront.
- **Whole-document context enables upfront notation locking.** Rather than letting isolated batches
  diverge on mathematical notation (e.g. `\sum` vs `\Sigma`), a **Phase 0 Global Notation Scan**
  inspects all document scans at the start to establish `corpus/<work-id>/notation.md` before
  generating page 1.
- **Proofread-first verification sequencing.** Following the measured architecture in
  `transcribe-turn-cost`, whole-document text-only proofreading runs *before* visual verification.
  Structural, linguistic, and delimiter issues are classified without images, and all `NEEDS SCAN`
  queries are routed directly into the scan verification pass so each scan image is opened only once.
- **Thinking effort.** Always run with `effort: high` across transcription and verification.
  Flash thinking tokens are economical and provide the reasoning runway needed for complex Fraktur
  ligatures and display math.
- **Generation chunking.** While input context is 1M+ tokens, output tokens per response are capped
  (~8k tokens). LaTeX fragments are generated in logical chunks (e.g. 4 pages at a time or
  page-by-page) into scratch files.

## Before you start

Read these to ensure output matches the house style exactly:
- `prompts/transcribe-chat.md` — canonical transcription rules and current `prompt_version`.
- `prompts/transcribe-housestyle-extract.md` — transcription-relevant house-style rulings.
- `corpus/HOUSESTYLE.md` — the complete rulings log.
- `corpus/<work-id>/notation.md`, if already present — work-specific decisions.
- `corpus/preamble/readmasters.sty` — apparatus macros (`\origpage`, `\uncertain`, `\illegible`,
  `\ednote`, `\rmfigure`).

---

## Phase 1 — Isolate workspace, locate the work, and clear the gate

0. **Isolate your branch or worktree before touching files**:
   Never start transcription on `main` or an unrelated feature branch.
   - **Single session**: create and switch to a dedicated branch off `origin/main`:
     ```bash
     git checkout -b transcribe/<work-id> origin/main
     ```
   - **Parallel sessions (recommended for concurrent runs)**: If transcribing multiple works in
     parallel (e.g. across multiple terminal sessions, subagents, or between Claude Code and
     Antigravity), create an isolated git worktree:
     ```bash
     git worktree add ../rtm-<work-id> -b transcribe/<work-id> origin/main
     cd ../rtm-<work-id>
     ```
     *Why?* `pipeline/validate.py` inspects the entire `corpus/` tree. Multiple sessions sharing
     a single working copy will cross-contaminate the directory with untracked or in-progress files
     from other works, causing validation to fail, and branch switching will disrupt running sessions.

1. If `corpus/<work-id>/work.yaml` exists, read it. Otherwise the work is new:
   - Help the contributor create `corpus/<work-id>/work.yaml` from
     `.agents/skills/transcribe/templates/work.yaml`. The `<work-id>` follows PLAN.md §3.2
     (Wikidata QID → DOI → `author-year-shorttitle` slug) and must equal the directory name.
   - Every copyright-critical fact (author death dates, first-publication year, edition) MUST be
     **sourced** in the `sources:` block, or the gate fails by design.
2. Fill/refresh the `copyright_assessment` block by running the gate in write mode:

   ```bash
   python pipeline/validate.py --write --only <work-id>
   git diff corpus/<work-id>/work.yaml
   ```

   `--write` rewrites `work.yaml`, updating the computed assessment. Review the diff and confirm
   public-domain status. If `public_domain: false`, STOP and inform the contributor.
3. Read the title from the print scan (not modernized catalogue entries) and confirm it matches
   `work.yaml` orthography.

---

## Phase 2 — Prepare the pages (high-resolution)

1. Use `source.scan_url` / `scan_id` in `work.yaml` to locate pages `<pages>`.
2. Prepare working images in a temporary scratch directory (`scratch/<work-id>/prepared/`):
   - For standard or landscape pages: use the source scans directly or crop to text block without
     reducing resolution below 1500px text width.
   - For narrow portrait pages (where long edge exceeds width by >1.5×): split into top/bottom
     half-page tiles to preserve subscript and punctuation clarity.
   - If using `pipeline/prepare_pages.py`:
     ```bash
     python pipeline/prepare_pages.py --images <scans> --pages <spec> --out <scratch>/prepared
     ```
3. Prepared page images live **outside the corpus** in scratch. Only figure crops
   (`corpus/<work-id>/figures/`) are ever committed.

---

## Phase 3 — Phase 0 Global Notation Scan

Before generating any LaTeX fragments, perform an upfront global notation pass:
1. Ingest all prepared page images for the work in a single context inspection pass.
2. Inspect the typography and mathematics across the entire text to identify:
   - Author's specific symbols (e.g. Clebsch summation `\Sigma` vs `\sum`, Leibniz `d`, multiplication dots).
   - Display math punctuation (periods or commas ending displayed formulas).
   - Footnote and back-reference conventions.
   - Subscript and superscript bracing patterns.
3. Write or update `corpus/<work-id>/notation.md` with explicit rules, rationales, and forbidden
   alternatives. **State rules explicitly; do not merely show them in examples.**

---

## Phase 4 — Transcribe with high thinking effort

1. Transcribe pages sequentially in 4-page chunks (or page-by-page) into scratch fragments
   `<scratch>/p<N>.tex`:
   - Each fragment starts with `\origpage{N}` (the printed page number) and contains body LaTeX only.
   - Transcribe faithfully: author's spelling, symbols, and archaic forms (`zz` for $z^2$, `arc.`).
   - Normalize typography only (Fraktur/long-ſ → modern letters, expand ligatures, drop line-break hyphens).
   - Figures: emit `\rmfigure{figures/fig-XX.png}{<fig-num>}{<alt text>}` — never redraw.
   - Apparent printer's errors: reproduce faithfully and note them (ruling R4); do not silently fix.
   - Do not transcribe running heads, signature marks, or isolated page numbers.
2. **Early Linting**: Immediately after each fragment is written, run the house-style linter:

   ```bash
   python pipeline/houselint.py <scratch>/p<N>.tex
   ```

   Fix any formatting or macro violations immediately before moving to the next chunk.
3. If an obscure glyph is unreadable even at high resolution:
   - Call `pipeline/magnify.py` if localized sub-pixel cropping is needed:
     ```bash
     python pipeline/magnify.py --prepared <prepared> --scans <scans> --page <N> --regions "l,t,r,b" --out <scratch>
     ```
   - If still doubtful after magnification, mark `\uncertain{...}` or `\illegible`.

---

## Phase 4a — Stitch and normalize

1. Concatenate all `<scratch>/p<N>.tex` fragments in ascending page order into
   `corpus/<work-id>/original.tex` inside the standard document scaffold:

   ```latex
   \documentclass{article}
   \usepackage{readmasters}
   \begin{document}
   ... \origpage-delimited fragments ...
   \end{document}
   ```

2. Verify that `\origpage` markers are strictly contiguous with no gaps or duplicate page numbers.
3. Check page boundary joins: a page opening mid-sentence must have **no blank line** following `\origpage`.

---

## Phase 5 — Proofread assembled text (text-only, whole-work)

Before opening any scan images for verification, run a whole-document text-only proofread of
`corpus/<work-id>/original.tex` and `notation.md`:
1. Mechanical checks:
   - Delimiter balance: `begin`/`end`, `\[`/`\]`, `$` parity, curly brace balance.
   - Equation numbering: monotonic `\tag{n}` sequence.
   - Invariant check: run `python pipeline/texcompare.py` against previous drafts if applicable.
2. Cross-work consistency & prose checks:
   - Conformance to `notation.md` throughout.
   - Seamless text joins across page boundaries.
   - German / French syntax parsing.
3. Classify all findings:
   - **DEFECT**: Internal syntax/markup error (fix immediately in `original.tex`).
   - **INCONSISTENCY**: Two parts of the text diverge from `notation.md` (resolve or record).
   - **NEEDS SCAN**: Ambiguous math, punctuation, or reading that only the printed scan can settle.
     Compile these into a targeted query list grouped by page.

---

## Phase 5a — Verify against scans (carrying NEEDS SCAN items)

Verify each page against its source scan image:
1. Verify line-by-line fidelity of all displayed formulas, subscripts, exponents, and punctuation.
2. Settle every targeted **NEEDS SCAN** query from Phase 5 using the scan.
3. Any unresolved ambiguity that remains doubtful must be marked with `\uncertain{...}`.
4. Record all pages containing `\uncertain{}` or `\illegible` flags.

---

## Phase 6 — Write provenance

Create or update `corpus/<work-id>/provenance.yaml`:

```yaml
changelog:
  - date: "YYYY-MM-DD"
    summary: Transcription added (AI draft).
transcription:
  status: ai-draft
  model: gemini-3-8-flash
  effort: high
  prompt_version: transcribe-v1
  submitted_via: skill
  produced: "YYYY-MM-DD"
  verification:
    model: gemini-3-8-flash
    flagged_pages: []
    date: "YYYY-MM-DD"
  uncertainty_flags: 0
```

- Record `model: gemini-3-8-flash` and `effort: high`.
- Record the `verification.model` explicitly.
- Record the exact integer count of `uncertainty_flags` (state 0 explicitly when none exist).
- Set `status: ai-draft` unless human verification against scans has occurred.

---

## Phase 7 — Validate

Run the project verification suite:

```bash
python pipeline/validate.py
python -m pytest pipeline/tests -q
```

Fix any schema, vocab, or house-style issues. Both commands must pass cleanly with zero errors.

---

## Phase 8 — Review checkpoint and pull request

1. **Show the contributor the result before pushing**:
   - Pages transcribed.
   - Notation decisions documented in `notation.md`.
   - Total uncertainty flags count and flagged pages.
   - Copyright gate validation result.
2. Upon contributor approval, commit with DCO sign-off (`-s`), and open the PR (the branch was already established in Phase 1):

   ```bash
   git add corpus/<work-id>/
   git commit -s -m "Add <work-id> transcription (ai-draft)"
   gh pr create --fill
   ```

   Do not push directly to `main`.
   If you worked in a separate git worktree, remove it once the PR is merged or closed:
   ```bash
   cd ../ReadTheMastersAI
   git worktree remove ../rtm-<work-id>
   ```
