## Context

`/authors/` renders one `li.card` per author from the `authors` array in `works.json`. Each card is
969 × 86 px at desktop width and holds a heading and one meta line — about 55px of content in a box
that is 935px wide inside its padding. The same array already carries a `portrait` object with
`url`, `alt`, `credit` and `source`, populated by `resolve_portrait()` in
`pipeline/build_site_data.py` and consumed by `/authors/<slug>/`, which renders it at 120px wide.
The index simply never reads the field.

Measurements taken against production before writing this (13 author cards, 1024 × 768 viewport):

```
card                    969 × 86 px
padding                 .9rem 1.1rem  → 14.4px vertical, 17.6px horizontal
content box             ~935 × 55 px
title column @375px     298px
portrait aspect ratios  0.68 – 0.87, 11 of 13 within 0.77 – 0.87
full portraits, total   1,040 KB  (largest: jacob-bernoulli, 236 KB)
```

Three constraints shape the design. The cards must not grow — that is the request. CI installs only
PyYAML (project context; `pipeline/requirements.txt` says so explicitly, and the copyright gate's
independence from optional packages is deliberate), so the build cannot grow an image-processing
step. And the `portrait` block is authored per *work*, duplicated across every `work.yaml` by the
same author, so any new key in it is a synchronization burden — `abel-1826-unmoeglichkeit` and
`abel-1828-remarques` already carry byte-identical copies.

## Goals / Non-Goals

**Goals:**

- A portrait on every card of `/authors/`, large enough to recognize a face at a glance.
- Zero change to card height at desktop widths, verified by measurement, not by inspection.
- Page weight that stays in the tens of kilobytes, not the megabyte the full portraits would cost.
- No new hard dependency for CI or for the site build.
- No new `work.yaml` field, and no edit to the 20+ existing `portrait` blocks.
- Portrait-less authors leave the column alignment intact.

**Non-Goals:**

- Portraits on catalog cards, work-page headers, search results, or the timeline.
- Any change to `/authors/<slug>/`, which keeps the full-size portrait, its `credit` caption and
  its Commons `source` link.
- Attribution on the index card — there is no room, and the card links to the page that carries it.
- Responsive `srcset` / multiple densities. At 66 KB total for the whole page, a second breakpoint's
  worth of derivatives would cost more in complexity than it saves in bytes.
- Changing the single-column list into a gallery grid. A multi-column layout would allow far larger
  portraits without taller cards, but it changes what the page *is*; out of scope for this change.

## Decisions

### 1. Full-bleed thumbnail, not an inset avatar

The image occupies the card's left edge from top border to bottom border — 69 × 86, flush, with the
card's `overflow: hidden` and `border-radius: 10px` clipping its corners. The text column gets its
own padding back; the card's own padding drops to zero.

Both variants were prototyped against the live page. The inset alternative (44 × 55, rounded, inside
the existing padding) fits within the 55px content box and is the more conservative change, but at
44px wide the faces read as grey smudges — Leibniz's wig and Euler's cap are the only things still
identifiable. The full-bleed version buys 57% more width by reclaiming the padding the image does
not need, and it reads like a printed catalogue entry rather than a chat contact list, which suits
the site.

Circular crops were rejected outright: the sources are 4:5, so a circle discards the shoulders and
the top of the head that make these engravings legible, and a round avatar sits badly among the
site's otherwise rectilinear cards.

### 2. The image must not be able to push the card

A plain `<img>` in a flex row contributes its intrinsic aspect ratio to the row's height, which in
prototyping produced cards of 86, 87, 89, 91 and 98px — the defect this change exists to avoid. The
image is therefore taken out of flow inside a fixed-width box:

```
.authorlist .card       display:flex; padding:0; overflow:hidden; align-items:stretch
.authorlist .card .pbox flex:0 0 69px; position:relative     ← width fixed, height from the row
.authorlist .card .pbox img  position:absolute; inset:0; object-fit:cover
.authorlist .card .body      padding:.9rem 1.1rem .9rem 0; min-width:0
```

`position:absolute` removes the image from height computation entirely, so the row's height is set
by the text alone, exactly as today. `object-fit: cover` then fills whatever height it is given.
Measured across all 13 cards with this rule applied to production: uniformly 86px. `min-width: 0`
on the body is required — a flex item defaults to `min-width:auto` and would refuse to shrink below
its longest unbreakable word.

Explicit `width`/`height` attributes on the `<img>` keep the browser from reflowing when the image
arrives; `loading="lazy"` is set, though with a 66 KB total the whole set fetches immediately anyway.

### 3. Committed derivatives, generated by an optional contributor script

The full portraits average 80 KB and peak at 236 KB for an image drawn at 69px. A 138 × 172
derivative (2× the display box) at quality 82 costs 3.4–7.1 KB, 66 KB for the set — a 16× reduction.

Three ways to produce them were considered:

| Approach | Verdict |
|---|---|
| Commit `portrait-thumb.jpg` beside the portrait | **Chosen.** No build-time dependency; CI stays PyYAML-only. The corpus already holds committed binaries in exactly this folder, so there is no new category of file. |
| Generate in `build_site_data.py` with Pillow | Rejected. Puts Pillow in `pipeline/requirements.txt`, which CI installs for *both* jobs, including the copyright gate that is deliberately dependency-light. |
| Astro `<Image>` / sharp | Rejected. Portraits reach the site through `public/`, which Astro copies verbatim by design. Routing them through `src/assets` means restructuring how the Python pipeline hands images to Astro, for a page that needs 66 KB of images. |

`pipeline/make_portrait_thumb.py` produces them, importing Pillow lazily and failing with an
install hint — the pattern `pipeline/prepare_pages.py` already establishes. Contributors run it once
when adding an author.

A pleasant consequence: the derivative is an ordinary committed file, so an author whose automatic
crop lands badly can be cropped by hand and committed instead. The pipeline has no opinion about
where the bytes came from, which is why no per-author crop-focus field is needed.

### 4. The thumbnail is found by convention, not declared in schema

`resolve_portrait()` derives the sibling name from `portrait.file` — `portrait.jpg` →
`portrait-thumb.jpg` — and emits `thumb_url` when the file exists:

```
corpus/authors/<slug>/portrait.jpg        ──┐
corpus/authors/<slug>/portrait-thumb.jpg  ──┤ both copied
                                            ▼
site/public/authors/<slug>/{portrait,portrait-thumb}.jpg
                                            │
              works.json  authors[].portrait ┤ url        → detail page, 120px
                                             └ thumb_url  → index card, 69px
```

The alternative — a `thumb:` key in the `portrait` block — was rejected because that block is
duplicated per work.yaml: adding Abel's thumbnail would mean editing two files that must stay
identical, and the count grows with the corpus. Convention costs one line of path manipulation and
cannot drift.

When the derivative is absent, `thumb_url` falls back to `url` and the build prints a warning. The
page stays correct and merely heavier, which is the right failure mode for a cosmetic asset. In
particular `pipeline/validate.py` is not touched: the gate rules on copyright, and a missing
thumbnail is not a copyright question.

### 5. Monogram placeholder, and a decorative `alt`

An author with no portrait — `Émile Picard` today — renders a `.pbox.mono` in the same 69 × 86
footprint carrying the initial of the last whitespace-separated token of the name, in `var(--muted)`
on `var(--border)`. Omitting the box instead would leave that one card's text flush against the
border while every neighbour is indented 83px, drawing the eye to the gap rather than away from it.

The `<img>` takes `alt=""` and the monogram takes `aria-hidden="true"`. The author's name is in the
adjacent `<h3>`, inside the same link; a non-empty `alt` would make a screen reader announce
"Portrait of Leonhard Euler, Leonhard Euler" on every row of a fourteen-row list.

### 6. Scope the CSS to `.authorlist .card`

`.card` is shared by the catalog, the author detail page's work list and the journal pages.
`global.css` already carries a comment (near the journal rules) warning that shared `.card` and
`ul.authorlist` styles must stay untouched. Every rule this change adds is prefixed
`.authorlist .card`, so no other page can shift.

### 7. Mobile: 69px everywhere, two cards gain a line

At 375px the title column is 298px; the thumbnail and its gap reduce it to 215px. Three names
exceed that — Leibniz (238px), Fagnano (227px), Jacobi (226px) — and Fagnano already wraps today,
so **two of fourteen cards grow from 86px to 114px** on a phone.

**Measured after implementing:** the built page leaves 232px, not the 215px estimated here, and the
real cost is smaller than predicted — **one** card newly wraps, not two. Fagnano and Leibniz are the
two at 115px, and Fagnano already wrapped before the change, so Leibniz is the only regression.
Jacobi fits on one line at 226px in a 226px column: it survives, but with nothing to spare, so a
font or metric change could tip it over. The decision below stands on the smaller cost.

Holding 86px everywhere is possible: a `max-width: 480px` breakpoint narrowing the box to ~46px
restores a 240px title column and fits all three. It was considered and declined. 46px is below the
threshold where these engravings resolve into faces, so it would spend the whole benefit of the
change on the screen where the list is longest and the scanning value highest. Hiding portraits
under the breakpoint has the same defect in a starker form. Two wrapped lines is the smaller cost.

## Risks / Trade-offs

- **A face-biased crop is a heuristic and will sometimes be wrong** (a wide engraving with the
  subject off-centre, a full-length portrait). → The generator's default is centre-x, 18%-from-top;
  the output is a committed file, so any bad crop is fixed by hand-cropping and committing over it,
  with no code or schema change. Review the 13 generated thumbnails as part of this change.
- **Committing derived bytes duplicates data already in the repo.** → 66 KB across 13 files, in the
  folder that already holds the 1,040 KB of sources. The alternative costs CI a dependency the
  project has deliberately kept out.
- **A contributor adds a portrait and forgets the thumbnail.** → Build-time warning names the slug;
  the page still renders using the full image. Degradation, not breakage.
- **One card gets taller on phones** (Leibniz; measured, against two predicted). → Accepted
  deliberately (decision 7). If it reads worse in practice than on paper, the breakpoint is a
  three-line addition. Jacobi sits exactly on the boundary and would be the next to go.
- **Long names have 83px less room at every width.** → Desktop keeps 850px for titles of at most
  ~240px, so only the narrowest viewports are affected, and only as described above.
- **The card's `overflow: hidden` now does real work.** Without it the square-cornered image would
  overhang the 10px border radius. → It is in the rule set and covered by the height/appearance
  check in tasks.

## Migration Plan

No data migration. `works.json` gains an optional key; both consumers tolerate its absence. The
change is a single deploy, and reverting the commit restores the previous page exactly — the
committed derivatives become unreferenced files, harmless until garbage-collected by a later commit.

## Open Questions

- Should the catalog and work-page author links eventually carry the same thumbnail? Deliberately
  out of scope here; worth revisiting once the derivative exists and is proven.
- `Émile Picard` is the only author without a portrait today. If a suitable public-domain image
  exists on Commons, sourcing it would make the monogram path dead code on the live site — it
  should be implemented and tested regardless, since the next author added may arrive without one.
