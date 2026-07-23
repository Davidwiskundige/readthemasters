# Tasks: math-search

- [x] `mathnorm.js`: tokenize, normalize (Layer 1 only), wildcard parse + contiguous match
- [x] `mathindex.js`: extract `$…$` / `\[…\]` formulas with their `\origpage` and artifact
- [x] `/math-index.json` endpoint built from `works.json` at deploy time, not committed
      (598 formulas, 151 KB, every entry page-anchored)
- [x] `/search` gains a "Formulas" mode: TeX input, live KaTeX preview, ranked KaTeX results,
      deep links, `?mode=math&mq=` URL state, graceful no-index message
- [x] Layer 2 / CAS explicitly excluded; `zz` (2 hits) ≠ `z^2` (20 hits) confirmed
- [x] Verified in a built site: `\sqrt{a^4-z^4}` → 14, `a^4 - z^4` sub-expr matches, `\sqrt{?}` →
      136, `\frac{?}{?}` → 134, `a^?` → 32; normalization `x^2`=`x^{2}` (both 4), `\dfrac`=`\frac`
      (`\dfrac{zt}{a}` → 6); `\oint` → none. Results render with KaTeX and deep-link to the right
      panel/page; mode switch + URL state round-trip; no console errors; mobile has no page-level
      horizontal scroll
- [x] Deep links land on the target formula after KaTeX font reflow (re-scroll on `fonts.ready`)
- [x] Copyright gate + 20 pipeline tests pass
- [x] `math-search` spec added, `project.md` updated, change archived
