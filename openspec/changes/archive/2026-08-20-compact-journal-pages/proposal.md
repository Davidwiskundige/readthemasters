## Why

The journal pages render every entry as a boxy card, which is heavy for the little
information a journal row actually needs — a reader only needs the title to navigate.
The current corpus is also sparse (most journals have zero works yet), and the existing
layout treats an empty journal as an anticlimax rather than as what it really is: an
invitation to revive that journal by transcribing from its original run. Making the
pages compact and title-led, and turning empty journals into contribution on-ramps,
serves both browsing and recruitment.

## What Changes

- **Journal index (`/journals/`)** becomes a compact, title-led list instead of cards:
  each row is the journal title linking to its page. Era and place are dropped from the
  index (they live on the detail page and on the timeline). A work count is shown **only
  when non-zero**, as a positive "there's something to read here" marker — never `0 works`.
  Empty journals appear as equals in the same neutral (alphabetical) order, not demoted
  or hidden.
- **Journal detail — with works** keeps the metadata header and the "Find the originals"
  block, and replaces the card boxes around works with **eudml-style collapsible
  dropdowns** (native `<details>`): one section per volume when a work records one,
  otherwise one per dated issue (`month`+`year`), as with the month-cited Acta Eruditorum.
  Each collapsed section shows a label — `Volume {n} ({year})` or `{month} ({year})` — and
  a work count; expanding reveals the works, each with its **English translated title**
  (`title_en`) shown beneath the original.
- **Journal detail — empty** promotes the "Find the originals" block and replaces the flat
  "no works yet" message with a **quiet one-line invitation** to help revive the journal,
  pointing to the Contribute page.
- **Contribute page (`contribute.md`)** gains a referral from Step 1 (transcribing) to the
  journals as the place to discover originals worth reviving, closing the loop with the
  empty-journal invitation.
- The pipeline (`build_site_data.py`) now emits `title_en`, `volume`, and `month` on each
  journal work so the dropdown labels, chronological grouping, and translated titles can
  render. `volume` is absent on every current work (Acta is cited by month), so today all
  sections group by issue; volume-labelled sections engage automatically for any future
  work that records one.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `site-catalog`: The "Journal pages" requirement changes — the index becomes title-led
  with a non-zero-only work count and no era, the detail page groups works by year
  adaptively instead of a flat ordered list, and the empty-journal state becomes a
  contribution invitation rather than a bare empty list. The Contribute informational page
  gains a referral to the journals as a discovery surface.

## Impact

- `site/src/pages/journals/index.astro` — title-led rows, non-zero count, drop era/place.
- `site/src/pages/journals/[slug].astro` — collapsible volume/issue dropdowns with
  translated titles, promoted archives + quiet revive line on the empty state.
- `pipeline/build_site_data.py` — emit `title_en`, `title_en_tex`, `volume`, `month` on
  each journal work.
- `site/src/pages/contribute.md` — add the journals referral in Step 1 (transcribing).
- Journal card styling in the shared stylesheet (`site/src/layouts/Base.astro` or wherever
  `.card`/`.authorlist` for journals is defined) — new compact-row styles.
- `openspec/specs/site-catalog/spec.md` — "Journal pages" requirement and scenarios updated.
- No corpus-format or copyright-gate changes; `title_en`, `volume`, and `month` already
  exist in `work.yaml` and are only newly surfaced into the journal `works.json`.
