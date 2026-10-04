## 1. Site

- [x] 1.1 `site/src/lib/tex.js`: accept `\origpage{<arabic or lower-case roman>}` in both the block-promotion and the anchor replacement.
- [x] 1.2 `site/src/lib/mathindex.js`: match roman markers and keep the page as printed (number for arabic, string for roman).
- [x] 1.3 `site/src/pages/search.astro`: resolve `p-iii` / `en-p-iii` anchors in `pageIndex`.
- [x] 1.4 Tests: roman marker rendering in `tex.test.mjs`; formula page on a roman page in a mathindex test.

## 2. Gate

- [x] 2.1 `pipeline/validate.py` `check_page_markers`: parse roman markers, require them before the first arabic marker, and apply ascending/duplicate/gap rules within each run.
- [x] 2.2 `pipeline/tests/test_page_markers.py`: front matter then text passes; roman after arabic fails; duplicate roman fails.

## 3. First user

- [x] 3.1 Transcribe and verify Klein 1882 pp. iii–viii (Vorrede, Inhalt) into `corpus/klein-1882-riemanns-theorie/original.tex`, and update its header comment, notation.md and provenance.

## 4. Close

- [x] 4.1 `openspec validate roman-page-markers --strict`, then sync the requirement into `openspec/specs/corpus-format/spec.md` and archive the change.
