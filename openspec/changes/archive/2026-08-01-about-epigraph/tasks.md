# Tasks: about-epigraph

## Epigraph

- [x] `about.md` opens with the Abel quotation and `— Niels Henrik Abel` on the same line; the
      source citation and the French original live in a `.pop` popover.

## Shared popover

- [x] Extract the inline popover JS from `works/[id].astro` into `site/src/scripts/pop.js`.
- [x] Load `pop.js` once from `Base.astro` so every page (incl. Markdown pages) gets it.
- [x] Remove the duplicated inline popover JS from `works/[id].astro`.
- [x] Bind hover (`mouseenter`), keyboard focus (`focusin`), and click-to-pin to the whole `.pop`
      wrapper; ignore clicks that land inside an open `.pop-content` so its links still work.

## Verification

Client-side, so verified in the preview (no JS unit harness — house convention).

- [x] About page — hovering the middle of the quote (not the name) opens the source card with the
      French original; 0 console errors.
- [x] Work page — the "Citation 1" popover still pins open on click and its thesis link still works;
      the generalized script did not regress existing popovers; 0 console errors.

## Ship

- [x] Fold the delta into `openspec/specs/site-catalog`; archive the change; update `project.md`.
