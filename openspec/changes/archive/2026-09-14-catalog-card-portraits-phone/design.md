## Context

`catalog-card-portraits` put a 69px portrait strip at the left edge of every catalog card, full
height, at every viewport width. Above ~560px that works: the archived change measured a 4.3% cost
at 1280px and a crop that keeps 39–80% of the thumbnail.

Below it, two things compound. The card is ~335px wide at 375px, so the strip takes 83px off a
title column that is already the tightest thing on the card, and `object-fit: cover` — given a card
219–428px tall and 69px wide — crops the thumbnail to a 20–39% vertical sliver.

Everything below was measured against the deployed site (18 works), not estimated. Blocks are
measured by **ink** — first line's top to last line's bottom — not by box height, because a wrapped
flex container stretches its lines to fill its box and box measurements hide exactly the mismatch a
reader sees.

```
375px viewport, cards 335px, body column 250px      total 5885px
   metadata  (author · year · venue · badge · →EN)   2176 px   ← largest block, wraps happily
   title                                             2081 px   ← 5–7 lines, pays for the strip
   English title                                     1003 px
   portrait rendered                                 69 × 219…428  (aspect 0.16–0.31)
```

## Goals / Non-Goals

**Goals:**

- A portrait on a phone that reads as a portrait: never a sliver, never cropped top-to-bottom.
- The title gets the card's full width, where the wrapping cost actually falls.
- The portrait never taller than the text it sits beside, at any card and any width in range.
- No change whatsoever above the breakpoint.
- No new asset, request, field or pipeline step.

**Non-Goals:**

- Any change to `/authors/`. Measured on a phone its cards are 86 or 114px, so its portraits render
  at 0.62–0.82 against a native 0.80 — barely cropped. The sliver is specific to catalog cards,
  which vary in height by 4×.
- Portraits on `/authors/<slug>/`, journal pages, the timeline or search.
- A second portrait for multi-author works, or a second derivative size.
- Reflowing the metadata's own content (shortening venue names on phones, dropping pills).

## Decisions

### 1. Title full width; portrait beside the English title AND the metadata

The card becomes two stacked regions below the breakpoint: the original title spanning the full
width, then a row holding the portrait and — as a single column — the English title and the
metadata.

```
┌──────────────────────────────┐
│ Beweis der Unmöglichkeit     │  original title, full width
│ algebraische Gleichungen von │
│ höheren Graden als dem       │
│ vierten allgemein aufzulösen.│
├──────┬───────────────────────┤
│ face │ Proof of the impossi- │ ─┐
│      │ bility of solving…    │  │  portrait height
│      │ Niels Henrik Abel     │  │  = this block's height
│      │ Journal für die reine │  │
│      │ ai-draft    → EN      │ ─┘
└──────┴───────────────────────┘
```

Pairing the portrait with **both** lower blocks rather than the metadata alone is the decision the
whole design rests on, and it was reached by eliminating the alternatives:

| Pairing | Result |
|---|---|
| Metadata alone, portrait fixed at 69×86 | Portrait overhangs the text on sparse cards — +31px on Leibniz at 430px. The mismatch a reader sees first. |
| Metadata alone, portrait fixed at the *modal* metadata height | Worse. The mode is 106px at 430px but 125px at 375px, and the mode is not the floor: at 69×106 the portrait overhangs on **7 of 18** cards, +51px on Leibniz. |
| Metadata alone, portrait stretched to it | Heights match, but a 2-line metadata block is only 55px against a 69px-wide box — aspect **1.25**, wider than tall, cropping the top of the head off. Appears from ~400px upward, so it hits most phones. |
| Metadata alone, portrait shrunk to 48–55px | Reduces the overhang but *worsens* the sliver: a narrower box against a tall metadata block is aspect 0.38. Trades the complaint for the original one. |
| **English title + metadata, portrait stretched to it** | **Chosen.** That block measures 128–209px at 375px and 120–175px at 430px — always taller than 69px, so the portrait is always taller than it is wide. |

The English title earns its move: full width it was contributing 1003px of card height while
carrying no wrapping pressure, and beside the portrait it supplies exactly the vertical extent the
portrait needs.

### 2. Stretch to the block, and accept a horizontal crop

The portrait fills the row's height with `align-items: stretch`, the same mechanism the wide layout
uses. The crop therefore lands **horizontally**, keeping the centre of the image:

```
                     visible width of the thumbnail
  today, on a phone           20 – 39 %
  this design, 375px          33 – 54 %
  this design, 430px          39 – 57 %
  wide layout (unchanged)     39 – 80 %
```

This is a deliberate trade, and the crop stays horizontal by construction: the text block is never
shorter than 120px against a 69px box, so the box cannot become wider than tall, and the top of the
head is never cut. A horizontal crop of a centre-cropped derivative finds more face, not less.

An optional `max-height` was prototyped (150px gentles the crop to 0.46, 130px to 0.53) at the cost
of the portrait no longer matching the block on the tallest cards. Not adopted: matching exactly on
every card is the property that makes the layout read as deliberate.

### 3. The breakpoint is the card's own, not the sidebar's — and it is 500px, not 560px

`global.css` already carries `@media (max-width: 800px)` — it collapses the filter sidebar. Reusing
it would be wrong, and measurably so. The narrow layout wins only while the card is narrow:

| viewport | card | today | this design | |
|---|---|---|---|---|
| 375px | 335 | 5885 | **5401** | −8.2% |
| 430px | 390 | 4900 | **4598** | −6.2% |
| 500px | 460 | 4305 | **4225** | −1.9% |
| 768px | 713 | 2907 | 3354 | **+15.4%** ✗ |

At tablet width the layout is 15% *taller*, because a wide card's title fits in one or two lines and
gains nothing from the extra width, while the portrait row imposes a floor the old layout did not
have. The sidebar breakpoint and the card breakpoint are answers to different questions and must
stay separate.

**Implementation corrected the value.** This section originally set the breakpoint at 560px, where
the two height curves cross. Measured on the built site, a stricter limit binds first: as the card
widens, the text block beside the portrait shrinks, and once it falls under 86px the `min-height`
floor of decision 1 makes the portrait taller than its own text — the exact defect this layout
exists to remove. Measured: clean at 510px, broken on **3 of 18 cards at 530px**. The breakpoint is
therefore **500px**, which keeps the invariant with ~30px of margin and is still 1.9% shorter than
the strip layout at that width. Height parity was the wrong criterion; the invariant is the right
one, and it is the one the spec states.

### 3a. The wrapped flex's row gap must be zeroed

Found during implementation, and worth recording because it is invisible until measured. The wide
layout sets `gap: .9rem` as a column gap between the strip and the body. Once the narrow layout adds
`flex-wrap: wrap`, that same shorthand also applies *between rows* — inserting 14.4px between the
title and the portrait row on every card, on top of the `.25rem` bottom margin `h3` already carries.
Across 18 cards that was **259px**, most of the difference between the height saving this design
predicted and the one it first delivered. The narrow layout sets `gap: 0 .9rem`, and `h3`'s existing
margin provides the separation, exactly as it does above the breakpoint.

### 4. Markup: one wrapper, no new data

The portrait stops being the card's first child and joins a row with a wrapper around the two lower
blocks. The wide layout is then expressed by the same DOM with different CSS — the row is simply
laid out as the full-height left strip above the breakpoint.

Filtering and sorting are untouched: every `data-*` attribute stays on the `li` itself, and the
sort reorders `li` elements, so the portrait travels with its card as it did before.

### 5. Scoping, unchanged from the archived decision

Every rule stays under `.catalog .card`. Neither bare `.card` nor `.works` may be keyed on —
`/authors/<slug>/`'s work list uses both, and the archived change found that out the hard way when
scoping to `.works .card` stripped that page's cards of their padding. `/authors/` keeps the shared
`.pbox` block untouched.

## Risks / Trade-offs

- **The crop is heavier on a phone than on a laptop** (33–54% vs 39–80%). → Accepted deliberately
  (decision 2); it is a large improvement on the 20–39% that ships today, and the crop direction is
  guaranteed horizontal, so no face is ever decapitated.
- **Two card layouts to maintain**, and a spec requirement that must describe both. → The cost of
  the phone being a genuinely different shape; the alternative measured worse on every phone width.
- **The breakpoint is tuned to today's 18 works.** A corpus with much shorter titles, or a work with
  unusually sparse metadata, shifts the crossover. → 560px has ~40px of margin before the curves
  cross; re-measure if the corpus's title-length distribution changes materially.
- **A card whose metadata is sparse and whose English title is absent** would give a short text
  block. → `title_en` is optional in the schema. Every work in the corpus has one today, and the
  layout degrades to the metadata-only case, which is exactly the letterbox risk decision 1 rules
  out — so the implementation must floor the portrait at its natural height for that case, and a
  task covers verifying it against a work with `title_en` removed.
- **Lifting the English title into the lower row changes reading order** — the reader meets the
  original title, then the translation beside a face. → Prototyped; it reads as a caption block, and
  the English title stays adjacent to the title it translates.

## Migration Plan

CSS and one markup wrapper, one commit, one deploy. Reverting the commit restores the current
layout exactly: no data, no asset and no schema is involved, and the portrait's `thumb_url` is
already being served to every surface that uses it.

## Open Questions

- Should the crop be gentled with a `max-height` after living with it on a real phone for a while?
  The dial exists and costs three characters; the answer needs use, not measurement.
- `/authors/` was measured as not needing this, but its cards grow on a phone when a name wraps
  (86 → 114px). If author names get longer, the same sliver could appear there in miniature. Worth a
  re-measure when the corpus doubles, not now.
