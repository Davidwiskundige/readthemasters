## Why

A reader who opens a work page scrolls **918px of apparatus before the first word of the text**,
measured on `/works/leibniz-1689-isochrona/` against a 768px viewport. Roughly 40% of that height
(367px) is machinery — a provenance identifier, a restated citation, a download box, a navigation
line — none of which is what the reader came for. The text begins below the fold on every work in
the corpus.

Most of that apparatus is redundant rather than merely bulky, and the redundancy is measurable:

- **`publication_full` restates the header on 15 of 18 works.** `"De linea isochrona…", Acta
  Eruditorum, Leipzig (April 1689)` is already `Leibniz · 1689 · Acta Eruditorum, April` two lines
  above it. Only 3 works (`leibniz-1689-isochrona`, `fagnano-1718-lemniscata`,
  `fagnano-1718-lemniscata-ii`) carry a fact the header cannot — that the scan is a later reprint,
  not the first printing.
- **`scan_id` is an internal provenance key rendered as prose.** On `betti-1871` it renders as three
  sentences inside parentheses following a two-word link; `clebsch-1868` and `jacobi-1832` are
  similar.
- **"Original (Latin)" is printed three times** — the tab button, the Downloads row label, and the
  panel's screen-reader heading.
- **"PDF on deploy" renders on every download row of every work.** `original_pdf` is null for all 18
  works and no PDFs exist outside a deploy, so a build-state placeholder is permanently visible where
  a link should be. `pdf_url()`'s own docstring already states the intended behaviour — "the work
  page simply omits the download link" — only the template disagrees.
- **The status badge is unexplained.** `ai-draft` gets a notice box; `skimmed` gets a bare pill
  defined nowhere on the page.

This is a presentation change. No corpus data is touched: `scan_id`, `publication_full` and `edition`
all stay in the YAML for validation and audit.

## What Changes

- **Source line collapses to one line.** Drop `scan_id` and `publication_full` from display. Where
  `edition.year !== work.year`, append a short parenthetical giving the transcribed edition's year
  — `Source: original scan (from the 1858 edition) ⧉ BibTeX`. 79px → 28px, measured.
- **Downloads move into the tab panels.** The 181px box (4 rows, 9 controls) becomes a single chip
  row at the head of each panel, merged with the provenance attribution line already there:
  `↓ .tex  ⧉ BibTeX    claude-opus-4-8 · reviewed DvdL`. Inside a panel the tab already names the
  text, so the duplicated labels go with it.
- **Absent PDFs render nothing** instead of the italic "PDF on deploy".
- **"Download all as .bib" is removed.** Per-artifact BibTeX buttons already cover citation; the
  whole-file download was a third citation affordance on one page.
- **Served `.tex` files become self-contained.** `write_tex_copy()` substitutes
  `\usepackage{readmasters}` with the body of `readmasters.sty` when emitting to `site/public/tex/`.
  A downloaded `.tex` then compiles on the first try, and the `.sty` chip and its "(needed to compile
  a `.tex`)" note both become unnecessary. The corpus copy is unchanged.
- **The timeline link folds into the related-reading nav** as a centred `timeline` word between
  `Read first:` and `Next:`, in both the top and bottom instances. Because the middle slot always has
  content, **both navs now always render** — which also gives the 4 works with no recommendations a
  timeline link they would otherwise lose, and balances the row on the 6 works whose left side is
  empty.
- **The status badge explains itself** through the site's existing `.pop` popover — the same
  mechanism as `\ednote` editorial notes and significance citations.

No breaking changes. Every URL, anchor and download path is unchanged.

Expected result:

```
  before                        after
  ─────────────────────────     ─────────────────────────
  workhead        176           workhead        176
  source           79     →     source           28
  significance    150           significance    150
  relnav (top)     41           relnav           41   (gains timeline)
  timeline link    22     →     (folded)          0
  downloads       181     →     (into panels)     0
  tabs             44           tabs             44
  ─────────────────────────     ─────────────────────────
  text at y=918                 text at y≈624  ← inside the 768px fold
```

## Capabilities

### New Capabilities

None. This change modifies how an existing capability presents itself.

### Modified Capabilities

- `site-catalog`: six requirements change behaviour.
  - **Work page** — the source line drops `scan_id` and `publication_full`, gaining a conditional
    edition note; the status badge gains a popover explaining its review level.
  - **Downloads** — no longer "one consolidated list" above the text, and no longer offers the
    shared preamble; per-text downloads move into their own tab panel and the served `.tex` is
    self-contained.
  - **PDF compilation (deploy-time)** — an absent PDF renders nothing rather than being labelled
    "compiled on deploy". This directly replaces the existing scenario *"Absent PDF is labelled, not
    a dead link"*.
  - **Citations (BibTeX)** — the "Download all as `.bib`" affordance is removed; per-artifact Copy
    buttons remain.
  - **Related reading (dependency graph)** — the standalone "See this work in the timeline →" link
    becomes a centred slot inside the nav, and both navs render unconditionally. This replaces the
    existing scenarios *"Top nav appears only when there is a recommendation"* and *"Bottom nav is
    absent without a recommended next"*.
  - **Source popovers (shared apparatus)** — the list of `.pop` uses gains the work-page status
    badge.

`corpus-format` is **not** modified: every corpus `.tex` still uses `corpus/preamble/readmasters.sty`.
Only the generated, git-ignored copy under `site/public/tex/` is flattened.

## Impact

**Code**

| File | Change |
|---|---|
| `site/src/pages/works/[id].astro` | Source line, downloads into panels, relnav middle slot, badge popover, drop `.bib` button and its handler |
| `site/src/styles/global.css` | Three-slot relnav; per-panel chip row; badge-as-`.pop` styling (follow the `.signote` variant) |
| `pipeline/build_site_data.py` | `write_tex_copy()` inlines the preamble |

**Not affected**: corpus YAML and `.tex` (no data migration), `bibtex.js` (entries unchanged — only
the whole-file download button goes), `pop.js` (reused as-is), all URLs and anchors.

**Risks**

- Inlining the preamble puts ~20 lines of macro definitions ahead of the human-readable provenance
  comment in a served `.tex`. Accepted: the file is for compiling, and `original.tex` in the corpus
  is unchanged for reading.
- Removing the `.sty` download makes `site/public/tex/readmasters.sty` unreferenced by any page.
  It stays emitted and served, so no existing link breaks.
- Seven works will show a bottom nav containing only the word `timeline`. Accepted deliberately (see
  design.md) to keep the two nav instances rendering through one shared path.

**Verification**: re-measure the Leibniz page in the browser preview after implementation and confirm
the text panel starts above 768px; spot-check `betti-1871` (longest `scan_id`), `fagnano-1718-lemniscata`
(edition note), and `abel-1826` (no recommendations, lone `timeline`).
