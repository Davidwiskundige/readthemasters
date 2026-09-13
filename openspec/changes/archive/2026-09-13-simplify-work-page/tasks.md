## 1. Self-contained served `.tex` (pipeline)

Do this first: the `.sty` download chip cannot be removed from the page until the served `.tex`
compiles without it.

- [x] 1.1 In `pipeline/build_site_data.py`, extend `write_tex_copy()` to substitute the body of
      `corpus/preamble/readmasters.sty` for the `\usepackage{readmasters}` line when writing to
      `site/public/tex/`. Read the `.sty` once per build, strip its leading comment block, and keep
      the five `\RequirePackage` lines and five `\newcommand` definitions.
- [x] 1.2 Leave the corpus `.tex` untouched — assert in the code comment that only the generated,
      git-ignored copy is flattened, so `corpus-format`'s "every `.tex` uses `readmasters.sty`"
      requirement still holds.
- [x] 1.3 Keep emitting `readmasters.sty` to `site/public/tex/readmasters.sty` so existing external
      links and bookmarks keep resolving, even though no page references it any more.
- [x] 1.4 Add a pipeline test asserting a served `.tex` contains `\newcommand{\origpage}` and does
      not contain `\usepackage{readmasters}`.
- [x] 1.5 Run `npm run data`, then compile one served `.tex` with Tectonic in a directory containing
      no `.sty` and confirm it succeeds.

## 2. Source line

- [x] 2.1 In `site/src/pages/works/[id].astro`, remove the `scan_id` parenthetical (currently
      line 129) and the `publication_full` line (currently line 131).
- [x] 2.2 Add a computed edition note rendered only when `work.edition?.year` differs from
      `work.year`, as a short parenthetical after the scan link.
- [x] 2.3 Verify against the three affected works (`leibniz-1689-isochrona`,
      `fagnano-1718-lemniscata`, `fagnano-1718-lemniscata-ii`) that the note appears, and against
      `betti-1871-spazi-numero-qualunque-dimensioni` (longest `scan_id`) that the line is now one
      line.

## 3. Downloads into the tab panels

- [x] 3.1 Delete the `<section class="downloads">` block and the `downloads` array that feeds it.
- [x] 3.2 Render one chip row at the head of each tab panel, merged with that panel's existing
      `attribution()` line: `.tex` (always), PDF (only when built), BibTeX Copy, then the provenance
      text. Omit the text label — the tab already names the panel.
- [x] 3.3 Render nothing where a PDF is absent; remove the "PDF on deploy" placeholder entirely.
- [x] 3.4 Remove the "All citations: `.bib`" row, its `#dl-bib` button, and the `Blob` /
      `URL.createObjectURL` click handler. Keep the hidden `#bib-store` — the Copy buttons read
      from it.
- [x] 3.5 Remove the "Shared preamble: `readmasters.sty`" row and its "(needed to compile a `.tex`)"
      note, now redundant after task 1.
- [x] 3.6 Keep each panel's `sr-only` heading — it carries the `#original` / `#en` anchor that the
      tabs, deep links and Pagefind sub-results depend on.
- [x] 3.7 Mark the chip row `data-pagefind-ignore` so chip text cannot leak into search excerpts,
      matching how `.pop` apparatus is already excluded.
- [x] 3.8 Add the chip-row styles to `site/src/styles/global.css` and remove the now-unused
      `.downloads` rules.

## 4. Related reading: three-slot rail

- [x] 4.1 Add a centred middle slot to `relatedNavHtml()` containing a single `timeline` link to
      `/timeline/?focus=<id>`, present in both the top and bottom instances.
- [x] 4.2 Make both navs render unconditionally — remove the early returns that suppress the nav
      when `recPrev`/`recNext` are absent. An empty side slot renders empty.
- [x] 4.3 Keep `Read first:` out of the bottom nav (unchanged behaviour).
- [x] 4.4 Delete the standalone `<p class="attr worktl">` timeline link and its `.worktl` rule.
- [x] 4.5 Update `.relnav` in `global.css` to a three-slot layout that keeps the middle centred when
      one or both sides are empty.
- [x] 4.6 Verify on `leibniz-1689-isochrona` (next only), `roch-1865-anzahl-constanten` (prev only),
      and `abel-1826-unmoeglichkeit` (neither — expect a lone centred `timeline` in both navs).

## 5. Status badge popover

- [x] 5.1 Wrap the status badge in a `.pop` wrapper with a `.pop-content` card explaining the review
      level, one card per status value (`ai-draft`, `skimmed`). No new script — `pop.js` is already
      loaded globally from `Base.astro` and binds to the whole wrapper.
- [x] 5.2 Style it after the `.signote` variant (baseline-aligned, bordered, accent hover) rather
      than the superscript `.ednote` style.
- [x] 5.3 Confirm the trigger is a real `<button>`, reachable by keyboard, pinned open on click, and
      closed by Escape — and that no `title` attribute is used.
- [x] 5.4 Confirm the card is excluded from the Pagefind index like every other `.pop`.

## 6. Verify

- [x] 6.1 `npm run data && npm run build`; confirm the build and Pagefind index succeed.
- [x] 6.2 Re-measure `/works/leibniz-1689-isochrona/` in the browser preview: the `.text` panel must
      start above 768px (was `y=918`, target ≈624).
- [x] 6.3 Check the tab switching, `#en` deep links, and `#en-p-236` page-marker anchors still work,
      and that KaTeX deferred typesetting is unaffected.
- [x] 6.4 Search a phrase from a work and confirm no chip, badge or popover text appears in the
      excerpt.
- [x] 6.5 Walk every work page once for layout regressions, paying attention to
      `castelnuovo-enriques-1897-surfaces-algebriques` (two authors, prev only) and the one work
      with `external_translations`.
- [x] 6.6 Run `python pipeline/validate.py` and the Python tests — no corpus data changed, so both
      must pass untouched.

## 7. Close out

- [x] 7.1 Run `openspec validate simplify-work-page`.
- [x] 7.2 Sync the `site-catalog` deltas into `openspec/specs/site-catalog/spec.md` and archive the
      change (`/opsx:sync`, then `/opsx:archive`).
