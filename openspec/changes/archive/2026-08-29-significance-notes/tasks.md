## 1. Renderer

- [x] 1.1 Move `renderSignificance()` from `site/src/pages/works/[id].astro` into
      `site/src/lib/significance.js`, with the citation behavior byte-identical
- [x] 1.2 Add the `[note n]` branch: resolve against `significance_notes[n-1]`, emit a
      `.pop.signote` wrapper whose marker is the note's label and whose `.pop-content` is its text
- [x] 1.3 Leave an unresolved marker of either kind as the literal text the author wrote
- [x] 1.4 Escape `"` as well as `& < >`, so a label or citation containing a quote is safe in the
      `aria-label`/`href` attributes the renderer builds
- [x] 1.5 Import the renderer in `works/[id].astro` and pass `work.significance_notes`

## 2. Styling

- [x] 2.1 Style `.signote .pop-marker` as an inline chip — the label at reading size on the
      baseline, not a superscript number — reusing the `--surface`/`--border`/`--accent` tokens
- [x] 2.2 Widen and cap `.signote .pop-content` (a paragraph, not a citation line) with
      `overflow-y: auto` so a long aside stays inside the viewport
- [x] 2.3 Confirm no change to citation markers, `\ednote` markers, or timeline node popovers

## 3. Pipeline

- [x] 3.1 `build_site_data.py`: pass `significance_notes` through to `works.json`
- [x] 3.2 `validate.py`: add `check_significance()` — marker/entry resolution both ways, non-empty
      `label`/`text`, label length, and lists that exist with no significance to mark up
- [x] 3.3 `validate.py`: run `houselint` over each aside's text, as it already does for `significance`
- [x] 3.4 Tests in `pipeline/tests/test_validate.py` for each rule, including that the "1" inside
      `[note 1]` is not read as a citation marker

## 4. Content

- [x] 4.1 Rewrite `roch-1865-anzahl-constanten`'s significance: keep the paragraph on what Roch did,
      move the modern-notation dictionary into one "In modern notation" aside
- [x] 4.2 Re-read the aside against `original.tex` (R11): the linear expression on p. 373, the
      italicised result on p. 375, and which factor clears the poles of $dz/(\partial F/\partial s)$

## 5. Verify

- [x] 5.1 `python pipeline/validate.py` and `python -m pytest pipeline/tests -q` — green
- [x] 5.2 `npm --prefix ./site test` — green, including the new `significance.test.mjs`
- [x] 5.3 Preview the Roch page (R18): the chip sits in the prose, the popover opens on hover,
      focus and tap, its math is typeset, and it stays inside the viewport at 1100px and at 375px
- [x] 5.4 Check the popover in dark mode and confirm no console errors

## 6. Documentation and close-out

- [x] 6.1 `corpus/HOUSESTYLE.md`: add ruling R26; update R18's renderer pointer and R11's
      marker-numbering bullet
- [x] 6.2 `prompts/transcribe-chat.md`: mention the optional field in the work.yaml sketch
- [x] 6.3 Fold the delta specs into `openspec/specs/` and archive the change
- [x] 6.4 Open a PR with a DCO sign-off, showing the before/after of the Roch significance
