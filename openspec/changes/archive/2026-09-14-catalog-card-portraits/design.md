## Context

The catalog (`site/src/pages/index.astro`) renders one `li.card` per work from the `works` array in
`works.json`: a title (which may carry inline LaTeX), an optional English title, and a meta row of
author links, year, venue pill, status badge and translation pills. The same JSON already carries an
`authors` array whose `portrait` objects hold `url` and `thumb_url`, populated by
`resolve_portrait()` in `pipeline/build_site_data.py` and consumed today only by `/authors/` and
`/authors/<slug>/`.

`author-index-portraits` (archived 2026-09-13) built the thumbnail machinery: a committed
`portrait-thumb.jpg` derivative beside each portrait, 138 × 172 at quality 82, 66 KB for the set,
found by convention rather than declared in `work.yaml`. That change explicitly excluded catalog
cards. This one reverses that exclusion, and everything it needs already exists.

Measurements taken against production before writing this — 17 works, four variants prototyped as
injected CSS on the live page, not estimated:

```
1280px viewport, cards 760px wide
                              list height    cards that grew
  off (today)                   2493 px            —
  stretch  (full-bleed 69px)    2600 px    +4.3%   3 of 17
  top      (69 x 86 pinned)     2600 px    +4.3%   3 of 17
  inset    (44 x 55, in pad)    2600 px    +4.3%   3 of 17

375px viewport, cards 335px wide
  off (today)                   4621 px            —
  stretch                       5557 px   +20.3%  16 of 17

card heights today   108 / 141 (median) / 219 px
portrait box         69 x 86  → fits inside the shortest card with 22px to spare
```

Two facts from that table drive the whole design. First, **the image never adds height**: the
shortest catalog card is 108px against an 86px box, so all three portrait variants cost exactly the
same 107px, and every pixel of it comes from titles wrapping in a narrower column — three cards, on
a 760px layout. Second, **the inset variant costs the same as the full-bleed one**. It keeps the
card's padding and adds 57px to the left of it, so it buys back no width at all while rendering the
faces at a size the archived design already measured as illegible.

## Goals / Non-Goals

**Goals:**

- A portrait on every catalog card, at the size where these engravings resolve into faces.
- No height contributed by the image itself, at any card height, verified by measurement.
- Reuse of the existing derivative, its `thumb_url`, and its monogram fallback — no second asset
  pipeline, no new bytes, no new `work.yaml` field.
- No Python, no CI, and no `works.json` schema change.
- `/authors/` and `/authors/<slug>/` render identically after the change, verified by measurement.

**Non-Goals:**

- Portraits on journal pages, the timeline, search results, or the work-page header. Journal pages
  deliberately use compact `.jrow` rows with no card box; there is nothing to put a portrait in.
- Portraits on `/authors/<slug>/`'s work list, which shares the `.card` class. Every work there is
  by the same author, so the column would be the same face repeated.
- A second portrait for multi-author works.
- A narrow-screen breakpoint (decision 4).
- `srcset` or a second derivative size. The 69px box is unchanged from `/authors/`; the existing
  2× derivative already covers it.

## Decisions

### 1. Full-bleed strip, not a pinned box or an inset avatar

The image occupies the card's left edge from top border to bottom border — 69px wide, flush,
clipped by the card's `overflow: hidden` and `border-radius: 10px`, with the text column keeping its
own padding. Structurally identical to `/authors/`, so the two pages read as one system.

| Variant | Verdict |
|---|---|
| **stretch** — full-bleed, image fills the card's height | **Chosen.** Matches `/authors/`. No dead space at any card height. |
| **top** — image pinned 69 × 86 at the top, flat `--border` below | Rejected. Same cost, and on a 219px card it leaves a 133px grey tail that reads as a loading failure. |
| **inset** — 44 × 55 rounded, inside the existing padding | Rejected twice over: measured at the same 2600px list height as stretch, so it saves nothing, and 44px is below the threshold the archived design measured, where "faces read as grey smudges". |
| **off** | The status quo this change exists to move off. |

Circular crops stay rejected for the reason `author-index-portraits` gives: the sources are 4:5, a
circle discards the shoulders and crown that make an engraving legible, and a round avatar sits
badly among the site's rectilinear cards.

### 2. The image must not be able to push the card

Same mechanism as the author index, and it matters more here because the failure would be larger:

```
.works .card        display:flex; padding:0; overflow:hidden; align-items:stretch
.works .card .pbox  flex:0 0 69px; position:relative      ← width fixed, height from the row
.works .card .pbox img   position:absolute; inset:0; object-fit:cover
.works .card .body       padding:.9rem 1.1rem .9rem 0; min-width:0
```

`position: absolute` takes the image out of height computation, so the card's height comes from its
text exactly as it does today. `min-width: 0` on the body is required — a flex item defaults to
`min-width: auto` and refuses to shrink below its longest unbreakable word, of which Latin titles
have several. Explicit `width`/`height` attributes and `loading="lazy"` stay as on the author index.

### 3. Variable card height means variable crop, and that is accepted

The author index escapes this: its cards are uniformly 86px, so the strip is always the thumbnail's
native 4:5. Catalog cards run 108–219px, and `object-fit: cover` scales the image to fill the box's
height, cropping horizontally. Measured across the cards, the visible slice is **39% to 80% of the
thumbnail's width** — the tallest card shows a tight head crop, the shortest a near-full frame.

**On a phone this is considerably stronger, and it was measured only after implementing.** At 375px
the same cards run 219–428px, so the visible slice is **20% to 39%** and every portrait becomes a
large, tightly framed head. All twelve remain recognizable — the derivative is already centred on
the face, so cropping inward finds more face, not less — and the effect reads as a deliberate
portrait column rather than as damage. It is nevertheless the most conspicuous consequence of
decision 1 on the surface where most readers will meet it, and the first thing to revisit if the
phone layout is ever revisited.

Two consequences, both accepted deliberately:

- The face gets *larger* on cards with longer titles. There is no meaning behind that, and a reader
  could read one into it. Prototyped side by side, it looks like ordinary editorial variation
  rather than emphasis, and the alternative (decision 1, "top") trades it for grey tails.
- A portrait whose subject sits off-centre horizontally could lose the face at 39%. The generator
  already crops centre-x into the derivative, so the face is centred before this crop begins; and
  the derivative is a committed file, so a bad case is fixed by hand-cropping and committing over
  it, with no code change. Reviewing all 14 at the tallest card height is a task.

### 4. 69px at every width — no breakpoint

On a phone the strip takes 69px of a 335px card and 16 of 17 cards gain a line: **+20.3% scroll**.
That is the real price of this change, and it is paid rather than dodged.

The two escapes were both considered. Hiding portraits below 480px removes the benefit exactly where
the list is longest and scanning value highest, and makes the catalog look like two different pages.
Shrinking to ~46px halves the cost and lands below the legibility threshold, spending the width and
getting nothing for it. `author-index-portraits` reached the same conclusion for the same reason and
declined the same breakpoint; holding the line keeps one rule instead of two.

### 5. The join happens in the template, not the pipeline

`works[].authors[]` carries the raw `portrait` block from `work.yaml` — `file`, `alt`, `credit`,
`source` — with no resolved URL. `authors[].portrait` carries `url` and `thumb_url`. Both arrays are
in the same `works.json`, which `index.astro` already imports whole, so the page builds its own
`slug → thumb_url` map at build time:

```
works.json ─┬─ works[].authors[].slug ───┐
            │                            ├─→ map, built in index.astro frontmatter
            └─ authors[].portrait.thumb_url ┘
```

The alternative — having `resolve_portrait()` write `thumb_url` back into every work's author block
— was rejected: it duplicates a resolved URL across 18+ work records that must stay in agreement,
grows `works.json` for no consumer that cannot do the join itself, and touches Python for what is a
presentation concern. The join costs three lines and cannot drift.

### 6. Scope every rule to `.catalog .card`, and share only the box

`.card` is shared by the catalog, `/authors/<slug>/`'s work list, and (historically) the journal
pages; `global.css` already carries a comment warning that bare `.card` and `ul.authorlist` rules
must stay untouched.

`.works .card` is **not** a safe scope either, and this was caught by measurement during
implementation rather than by reading: `ul.works` is the catalog's list *and* the work list on
`/authors/<slug>/`. Scoping to it silently gave that page's cards `display:flex` and `padding:0`
with no `.body` wrapper to restore the inset — the text went flush against the border. The catalog's
list therefore carries an additional `catalog` class (`<ul class="works catalog" id="works">`),
`works` keeping the shared grid layout and `catalog` scoping every portrait rule. This follows the
convention `.authorlist` and `.journallist` already set: a list that styles its cards differently
gets its own class rather than borrowing a shared one.

The portrait box's *visual* rules — the absolute-positioned `object-fit: cover` image and the
monogram placeholder — are identical on both pages and are lifted into a `.pbox` block that
`.authorlist .card` and `.works .card` both opt into. Layout (flex direction, padding, the 69px
basis) stays per-list. Duplicating the rules instead would leave two copies to drift; lifting them
touches the author index's CSS path, so verifying `/authors/` still measures 86px per card is a
task, not an assumption.

### 7. The strip links to the work; the first author only

The strip is wrapped in an `<a>` to the work, the same target as the card's title, so the card's
left edge becomes a forgiving hit area for its main action rather than a second competing
destination. The link takes `aria-hidden="true"` and `tabindex="-1"`, and the image `alt=""`: it is
a redundant path to a link that is already in the tab order and already announced, and without that
the card would offer a keyboard stop and a screen-reader announcement with no accessible name.

A multi-author work shows its first author's portrait. There is one such work today
(`castelnuovo-enriques-1897-surfaces-algebriques`); splitting the strip into two half-height images
would break the uniform 69px column for a single card, and the meta row already names both authors.

### 8. Monogram fallback, unchanged

A work whose first author has no portrait — Émile Picard today — renders `.pbox.mono` with the
initial of the last whitespace-separated token of the name, `aria-hidden`, exactly as on the author
index. Omitting the box would leave one card's text flush against the border while its neighbours
are indented 83px, drawing the eye to the gap.

## Risks / Trade-offs

- **+20.3% scroll on phones**, 16 of 17 cards gaining a line. → Accepted deliberately (decision 4);
  the breakpoint that would undo it is a three-line addition if it reads worse in practice than in
  the prototype.
- **Face size varies with title length** — 39–80% of the thumbnail's width visible at desktop, and
  only 20–39% on a phone, where cards run 219–428px. → Accepted (decision 3); all twelve portraits
  that appear on catalog cards were reviewed at the worst-case crop and every face survives, so no
  hand-cropping was needed.
- **The same face repeats down the list** — Abel 3×, Bernoulli 2×, Clebsch 2×, Fagnano 2× in 18
  works, scattered because the default sort is by year. → This is the change working as intended
  (three Abels are now visible without reading three names), but it is untested at corpus scale.
  Revisit if one author ever dominates the catalog.
- **Lifting `.pbox` rules touches the author index's CSS path.** → Measure `/authors/` before and
  after; every card must still be 86px at desktop width.
- **`.card` is shared with `/authors/<slug>/`, and so is `ul.works`.** → No bare `.card` rule
  changes and no rule keys off `.works`; the catalog's list carries its own `catalog` class
  (decision 6). Verified by measuring that page after the change: cards back to `display:list-item`
  with their padding intact and no `.pbox` present.
- **Titles carrying KaTeX re-layout after the math renders**, so a card's height — and therefore its
  crop — settles slightly after load. → Pre-existing behaviour, unchanged by this design; the image
  is absolutely positioned, so a re-layout re-crops rather than reflowing the list.
- **A contributor adds an author with no thumbnail.** → Existing build warning names the slug and
  `thumb_url` falls back to the full portrait; the catalog renders correctly and merely heavier.

## Migration Plan

No data migration; no schema change. `index.astro` and `global.css` change in one commit and deploy
as one build. Reverting that commit restores the previous catalog exactly — nothing else consumes
what it adds, and the thumbnails it reads were already being served to `/authors/`.

## Open Questions

- Does the repeated face read as useful grouping or as noise once a single author holds ten works?
  Not answerable at 18 works; revisit when the corpus is larger.
- Should sorting by author gain explicit visual grouping now that runs of identical faces make the
  runs obvious? Out of scope here, worth its own change if the answer turns out to be yes.
