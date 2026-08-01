# Change: about-epigraph

## Why

The About page should open by stating, in a master's own words, why the project exists. Abel's
remark — "study the masters, not the pupils" — is the project's namesake and thesis, so it belongs
at the top of the page that explains what ReadTheMasters is. The reader should also be able to reach
the full provenance (manuscript, page, archive) and the French original without cluttering the
epigraph itself.

The site already had the interaction for that: the `.pop` popover used by significance citation
markers and in-text editorial notes (hidden apparatus that reveals a source card on hover/click).
But its JavaScript lived inline in the work-page template only, so no other page could use it, and
the trigger was a small inner marker rather than the whole element.

## What changes

- **About page opens with the Abel epigraph.** `site/src/pages/about.md` starts with the quotation
  and `— Niels Henrik Abel` inline. The source (manuscript Ms.fol.351 A, National Library of Norway,
  p. 79, 9 August 1826) and the French original appear in a `.pop` popover.
- **The popover apparatus becomes a shared, global behavior.** The inline popover JS is extracted
  from `site/src/pages/works/[id].astro` into `site/src/scripts/pop.js` and loaded once from
  `Base.astro`, so every page — including Markdown pages like About — gets it. The work-page copy is
  removed (no duplication, no double-binding).
- **The trigger is the whole `.pop` wrapper.** Hover, keyboard focus (`focusin`), and click/tap-pin
  now bind to the entire wrapper, so the whole quote + attribution reveals the source card (not just
  a small marker). A click inside the open card (e.g. a citation link) acts normally instead of
  toggling the card shut.

## Impact

- Extends **site-catalog**: a new "Source popovers (shared apparatus)" requirement, and the About
  page requirement now names the opening epigraph.
- Touches `site/src/pages/about.md`, `site/src/scripts/pop.js` (new), `site/src/layouts/Base.astro`,
  and `site/src/pages/works/[id].astro` (inline popover JS removed). No pipeline, corpus, or
  copyright-gate change. Existing significance-citation and editorial-note popovers are unchanged in
  behavior; the `search` capability still excludes `.pop` apparatus from the index.
