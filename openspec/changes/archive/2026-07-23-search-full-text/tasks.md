# Tasks: search-full-text

- [x] Pagefind added as a devDependency; `npm run build` runs it over `dist` after `astro build`
- [x] Work-page reader regions scoped with `data-pagefind-body`; chrome, heading block, downloads,
      notices and BibTeX store excluded (heading block keeps supplying metadata only)
- [x] Math wrapped in `data-pagefind-ignore` spans by `texToHtml`; KaTeX still renders it
- [x] Citation and editorial-note popovers excluded from the index
- [x] `\origpage` and section anchors made unique per panel (`p-236` / `en-p-236`, `sec-1` /
      `en-sec-1`)
- [x] Panels get ids + visually-hidden headings; tabs sync `location.hash`; `#en` opens on load
- [x] `data-pagefind-meta` for title, author, year, status, language
- [x] `/search` page: query box, ranked results, excerpts, artifact + section + page sub-results,
      `?q=` URL state
- [x] Nav link + cross-links between catalog and search
- [x] Graceful message when no index exists (dev server); `site-preview` launch config for
      searching a built site locally
- [x] Verified against a built site: index covers 3 pages / 1884 words; "lemniscate" → 3 works with
      both Italian original and EN translation sub-results; "isochrona" → Leibniz only; "hyperbola"
      → 2 works, highlighted, no TeX in any excerpt; `#en-p-293` opens the English panel and scrolls
      to page 293; live typing updates results and the URL
- [x] Reader unaffected by the math wrappers: 26 KaTeX blocks render, no raw `$` left, and at a
      335px column 0 equation/number collisions, 5 `.wide`, 4 `.tag-below`, no left-cut formula, no
      page-level horizontal scroll — same as before the change
- [x] Copyright gate + 20 pipeline tests pass
- [x] `search` + `site-catalog` specs updated, `project.md` shipped list updated, change archived
