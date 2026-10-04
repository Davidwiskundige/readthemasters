## 1. Styles

- [x] 1.1 In `site/src/styles/global.css`, add `--band-h: 16rem` beside the band tokens, and a `@media (max-width: 40rem)` block setting `--band-h: 12rem`, `--band-top: #f8f5ef`, `--band-glow: rgba(122,75,43,.03)`, plus a narrow-and-dark block setting `--band-top: #1a1815`, `--band-glow: rgba(214,154,106,.03)`. The wide-screen tokens stay unchanged
- [x] 1.2 Set `body`'s background back to flat `var(--bg)` and remove `background-size`
- [x] 1.3 Add the `body::before` layer: absolute, top/left/right 0, height `var(--band-h)`, `z-index: -1`, `pointer-events: none`, background = radial glow `ellipse 37.5% 10rem at 50% -2.5rem` over `linear-gradient(to bottom, var(--band-top), transparent)`
- [x] 1.4 Change the print rule to hide the layer (`body::before { display: none }`)
- [x] 1.5 Update the band comments: own layer and why (Samsung Internet mis-draws a sized `body` background), fade to transparent, width breakpoint, and that the `theme-color` values in `Base.astro` must match

## 2. Theme colour

- [x] 2.1 In `site/src/layouts/Base.astro`, add four `<meta name="theme-color">` tags after the viewport meta, one per scheme × width, with the matching `--band-top` values and a comment pointing at `global.css` (ordered narrow-first, since the first matching tag wins — simpler than `min-width` queries)

## 3. Verification

- [x] 3.1 Build the site and check, in desktop Chrome at wide and narrow widths, in light and dark: the band fades out with no edge, header has no hairline, layout and clicks unchanged, band 16rem wide and 12rem narrow
- [x] 3.2 Confirm the computed tokens at 390px and 1280px in both schemes match the spec's table, and that the layer sits behind all content (links in the header still click)
- [x] 3.3 Serve the build over the LAN (`astro preview --host`) and have the maintainer check on their phone (Samsung Internet, dark and light): a gradual fade, no block, no edge, strength as approved
- [x] 3.4 Print preview a work page: the band is not printed (checked as the built `@media print{body{background:none}body:before{display:none}}` rule; no browser print preview run)
- [x] 3.5 Run `npm test` in `site/`

## 4. Spec

- [ ] 4.1 On shipping, sync the MODIFIED "Header paper band" requirement into `openspec/specs/site-catalog/spec.md` and archive the change
