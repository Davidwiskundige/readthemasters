## Why

The reader renders every `\rmfigure` as its own full-width block, so figures a print sets side by
side come out stacked. For Klein's 1882 *Riemann's Theorie* that loses meaning, not just looks: the
text refers to "linker Hand" and "rechter Hand" within a pair (p. 4), and the pairs exist to be
compared (a flow and its conjugate, a surface before and after deformation). Separately, figures
printed between lines of the running text were being moved to the end of the paragraph, which
breaks sentences such as "…die sich auf p = 3 beziehen: [Figs. 25, 26] Dieselben entstehen …".

## What Changes

- Adjacent `\rmfigure` lines with no blank line between them SHALL render as one row of figures,
  bottom-aligned, wrapping to a single column on narrow screens. A blank line keeps figures stacked,
  so every existing work renders exactly as before (none has adjacent figures today).
- HOUSESTYLE ruling R30 records the layout rule and the placement rule (a figure printed between
  lines of text goes exactly there; one printed beside the text goes before its paragraph), and the
  transcription house-style extract carries it to batch subagents.
- The PDF build is unchanged: each `\rmfigure` stays a float.
- `klein-1882-riemanns-theorie` is the first user: its figures are restored to their printed
  positions and its side-by-side pairs are written as rows.

## Impact

- `site/src/lib/tex.js`, `site/src/styles/global.css`, tests in `site/src/lib/tex.test.mjs`.
- `corpus/HOUSESTYLE.md` (R30), `prompts/transcribe-housestyle-extract.md`.
