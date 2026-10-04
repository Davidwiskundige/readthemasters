## 1. Site

- [x] 1.1 `site/src/lib/tex.js`: treat a run of adjacent `\rmfigure` lines as one block and render it as `<div class="rmfig-row">`; a single figure renders as before.
- [x] 1.2 `site/src/styles/global.css`: `.rmfig-row` flex row, bottom-aligned, wrapping below ~31rem.
- [x] 1.3 Tests in `tex.test.mjs`: adjacent figures form a row; blank-line-separated figures do not; a figure directly under a text line is still its own block.
- [x] 1.4 Confirm no existing work has adjacent `\rmfigure` lines (none found), so no rendering changes elsewhere.

## 2. House style

- [x] 2.1 HOUSESTYLE ruling R30 (layout and placement) and the matching entry in `prompts/transcribe-housestyle-extract.md`.

## 3. First user

- [x] 3.1 Klein 1882: check every figure's printed layout and position on the scan; restore printed positions and write side-by-side pairs as rows; update notation.md.
- [x] 3.2 Verify in the preview at desktop and phone width.

## 4. Close

- [x] 4.1 `openspec validate figure-rows --strict`, sync into `openspec/specs/corpus-format/spec.md`, archive.
