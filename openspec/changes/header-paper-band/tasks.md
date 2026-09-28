## 1. Styles

- [x] 1.1 In `site/src/styles/global.css`, add `--band-top: #f5f0e8` and `--band-glow: rgba(122,75,43,.05)` to `:root`, and `--band-top: #231e18` and `--band-glow: rgba(214,154,106,.08)` to the dark `:root` block
- [x] 1.2 Give `body` the layered background: a radial glow (`ellipse 60rem 10rem at 50% -2.5rem`, `--band-glow` → transparent 70%), a linear fade from `--band-top` to `--bg` at 16rem, both `no-repeat` and sized `100% 16rem`, over `var(--bg)`
- [x] 1.3 Make `header.site`'s bottom border transparent, leaving the footer's top rule as it is
- [x] 1.4 Add `@media print { body { background: none; } }`
- [x] 1.5 Add a short comment by the tokens: fixed height (not document-relative), and re-check `--muted` contrast (≥ 4.5:1) if the band colours change

## 2. Verification

- [x] 2.1 Build the site and check catalog, timeline, search, an author page, a journal page, a work page and a legal page, in light and dark: the band is there, the header has no hairline, and nothing is laid out differently
- [x] 2.2 Compare a short page and a long work page: same band height and colours; flat `--bg` below 16rem
- [x] 2.3 Check at phone width (375px), where the nav wraps: the band still reads, and header and content remain distinguishable
- [x] 2.4 Look for visible banding in the dark fade; if there is any, apply the design's mitigation
- [x] 2.5 Print preview a work page: no background printed
- [x] 2.6 Measure `--muted` and `--link` contrast against `--band-top` in both schemes (expected ≈ 4.9:1 and 7.8:1 light, 6.1:1 and 7.9:1 dark)

## 3. Spec

- [ ] 3.1 On shipping, fold the ADDED "Header paper band" requirement into `openspec/specs/site-catalog/spec.md` and archive the change
