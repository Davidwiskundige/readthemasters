# Transcription prompt (chat) — prompt_version: transcribe-v1

Copy everything in the box below into your AI chat app, then attach a few scan pages (as images or
PDF). Work in batches of a few pages so quality stays high. The prompt produces **two things** — the
LaTeX transcription and the work's `work.yaml` metadata file — and the **"Chat transcription" issue
form** has a field for each, so the submission is complete and ready to commit.

> Keep this prompt in sync with the pipeline. The `prompt_version` you used goes into the
> submission so provenance is accurate.

---

You are transcribing a page from a historic mathematics/physics text into LaTeX for a
public-domain digitization project. Follow these rules exactly:

1. **Be faithful.** Transcribe exactly what is printed. Do **not** modernize notation, correct the
   author, or paraphrase. Preserve the original language (do not translate).
2. **Normalize typography, not content.** Render Fraktur/blackletter and long-s (ſ) as normal
   letters; expand ligatures; drop original line breaks and end-of-line hyphenation. Keep the
   author's spelling and symbols.
3. **Use the house style.** Assume `\usepackage{readmasters}` is loaded. Use these macros:
   - `\origpage{N}` at the start of each original page (N = the printed page number).
   - `\uncertain{...}` for text you are not fully sure of; `\illegible` for unrecoverable text.
   - `\ednote{...}` only for genuinely editorial remarks (rare).
   - For a figure/diagram, output `\rmfigure{figures/fig-XX.png}{<caption>}{<alt text>}` — do
     **not** attempt to redraw it; we crop the figure from the scan separately. The visible
     `<caption>` is **only the original's figure number** (e.g. `Fig.~24.`); put any description of
     what the figure shows in `<alt text>` (for accessibility), not in the caption.
4. **Math in LaTeX.** Use standard LaTeX/`amsmath` math. Keep it within what KaTeX supports.
   Preserve the author's notation even where it differs from modern usage (e.g. `zz` for z²).
   Follow the math-typography house style (see `corpus/HOUSESTYLE.md`): write multi-letter
   geometric labels as plain math letters (`$CQ$`, `$ADFNA$` — no wrapper macro); for an inline
   large operator with a fraction integrand use `\displaystyle\int \frac{...}{...}` (not
   `\int \dfrac{...}{...}`); use `x^{2}` and `\,dz`. Put equation numbers on the right with the
   author's own number via `\tag{n}` inside the display: `\[ ... \tag{1} \]`. These presentation
   rules are machine-checked by `pipeline/houselint.py` (part of the gate), so a violation such as
   an un-`\displaystyle`d inline integral blocks the PR.
5. **Structure.** Use `\section*{...}` for headings actually present. Output a paragraph break
   (blank line) where the original has one.
6. **Output the LaTeX body first** — no commentary, no preamble, no `\documentclass` or
   `\begin{document}`. Start at the first page you were given. If several pages are attached,
   transcribe them in order, each preceded by its `\origpage{N}`.

7. **Then output the work's `work.yaml`** as a second, separate code block (produce it **once** for
   the whole work, not per batch). Fill every field you can from the title page and the scan. Leave
   `copyright_assessment` **out entirely** — it is computed automatically by the project's validator
   and must never be hand-written. Use this skeleton:

   ```yaml
   id: author-year-shorttitle          # lowercase slug; must equal the corpus directory name
   title: "Title exactly as printed"
   title_en: "English title"           # optional
   authors:
     - name: "Full Name"
       wikidata_id: Qxxxxx             # if known — enables a death-date cross-check
       death_year: 0000                # required (or use `anonymous: true` instead)
   publication:
     year: 0000                        # first-publication year (drives the US 95-year rule)
     venue: journal-key                # a key from corpus/vocab.yaml; if unsure, put TODO-<journal> and give the full name in title_full
     volume: ""                        # optional
     pages: ""                         # optional, e.g. "293–297"
     title_full: >-
       Full citation of the first publication.
   edition:
     year: 0000
     is_transcribed_edition: true
     rights_cleared: true              # true only for an original/early edition with no modern apparatus
     rights_note: >-
       Which physical edition this scan is, and that no modern critical apparatus, commentary, or
       re-typesetting is included in what you transcribed.
   discipline: mathematics             # a vocab key, or a list e.g. [mathematics, physics]
   tags: [analysis]                    # each a vocab key
   language: la                        # ISO 639-1
   type: paper                         # paper|book|chapter|letter|lecture|manuscript
   source:
     scan_url: "https://…"
     scan_id: "library:identifier"
   sources:                            # copyright-critical facts MUST be sourced, or the gate fails
     death_date: "wikidata:Qxxxxx / reference"
     publication_date: "catalogue record / DOI / library id"
     edition: "identifier of the edition transcribed"
   # significance: >-                  # optional editorial context (ours, not the author's) — may be left out
   # significance_notes:               # optional asides, each {label, text}, addressed from the
   #                                   # significance prose as [note 1] and shown in a popover (HOUSESTYLE R26)
   ```

   The vocab fields (`discipline`, `tags`, `venue`, `type`, `language`) must match keys in
   `corpus/vocab.yaml`; when you can't be sure a value exists, keep it simple and flag it — the
   copyright gate confirms every value and a maintainer can adjust a single key. Never invent a
   `copyright_assessment`, and never guess a public-domain verdict: give the sourced facts and let
   the validator compute it.
