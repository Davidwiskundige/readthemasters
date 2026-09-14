## Context

The catalog card's portrait strip is an `<a>` whose `href` is `w.url` — the work — carrying
`aria-hidden="true"` and `tabindex="-1"`. It sits at `site/src/pages/index.astro:133`, and its
geometry comes from `.pbox` / `.catalog .card .pbox` in `site/src/styles/global.css`, none of which
keys on the element being an anchor. `/authors/` renders the same box as a `<div>` already
(`site/src/pages/authors/index.astro:28`), which is the practical proof that the CSS is
element-agnostic.

Three facts from the data shape the work (measured against `site/src/data/works.json`, 19 works,
14 authors):

1. Every work has at least one author, and every author slug appearing on a work has a page in the
   `authors` array — the meta row already links `/authors/<slug>/` unconditionally, so the same
   assumption is safe for the portrait.
2. Every catalogued first author currently has a portrait, so the monogram branch is live code with
   no live instance. It must keep working regardless.
3. One work is multi-author (`castelnuovo-enriques-1897-surfaces-algebriques`); its card shows
   Castelnuovo's portrait, so the portrait must point at Castelnuovo, not at "the authors".

The requirement text being modified is currently authoritative in the **unarchived**
`catalog-card-portraits-phone` change, not in `openspec/specs/site-catalog/spec.md`: that change
shipped in PR #62 but its delta was never folded in, so the main spec still describes the pre-phone
single-layout card. The delta here is written against the shipped text.

## Goals / Non-Goals

**Goals:**

- The portrait links to the page of the author whose face it shows.
- The accessibility posture is unchanged in effect: no new tab stop, no new announcement, nothing
  reachable only through the portrait.
- Zero visual difference. The same pixels in the same places in both layouts, at every width, in
  both colour schemes.

**Non-Goals:**

- No change to layout, geometry, breakpoints, crop behaviour, or which portrait a card shows.
- No hover affordance, cursor change, title tooltip or focus ring added to distinguish the two
  targets. That is a separate question about whether the strip should be visible to keyboard users
  at all, and answering it here would smuggle an a11y change into a one-line redirect.
- No change to `/authors/`, `/authors/<slug>/`, journals, timeline or search.
- Not folding or archiving `catalog-card-portraits-phone`. This change depends on that text but does
  not own it.

## Decisions

### 1. Destination is the first author, not a disambiguating hover or a split target

`href={`/authors/${lead.slug}/`}` — the same author the portrait depicts and the same URL the meta
row's first name already carries.

Alternatives considered:

- *Keep the work, add a small author badge.* Two targets in 69px, one of them tiny. Worse than
  either single answer.
- *Point at the author only when the work has one author.* A rule a reader cannot see cannot be
  learned. The multi-author card shows one face; that face should mean what every other face means.
- *Make the strip a second link to the work but with an author tooltip.* Keeps the mismatch and adds
  a hover-only explanation for it.

### 2. Keep `aria-hidden` + `tabindex="-1"`, on a re-pointed justification

The archived rationale was "redundant with the title link". After this change it is "redundant with
the meta row's first author link" — which is present on every card, on the same card, pointing at
the same URL. The invariant that matters is not *which* link it duplicates but that it duplicates
one: the portrait never offers a destination that is otherwise unreachable, so hiding it costs a
screen reader or keyboard user nothing and saves them a nameless stop.

This is worth stating as a requirement rather than leaving as a code comment, because it is exactly
the property a future change could silently break — pointing the strip somewhere new without adding
a visible equivalent would turn a harmless hidden link into hidden functionality.

Alternative considered: expose the link with `aria-label="Portrait of <name>"`. Rejected — it adds a
tab stop per card (19 today) whose destination is already one stop away in the same card, which is
the noise the original decision avoided.

### 3. No first author ⇒ a `<div>`, not an `<a>`

A link needs a destination. With no `lead`, the current code still renders an anchor (to the work);
after this change there is nothing sensible to aim it at, and `href="/authors/undefined/"` is a
404 that CI would not catch. The box becomes a `<div class="pbox mono">` — precisely what
`/authors/` already renders for a portrait-less author, so the branch reuses a proven shape rather
than inventing one.

This costs one conditional in the template. It is a guard: no such work exists today, and
`pipeline/validate.py` would have to change for one to.

### 4. No CSS change, verified rather than assumed

Every rule in the portrait's path is class-keyed: `.pbox`, `.pbox img`, `.pbox.mono`,
`.catalog .card .pbox`, and the `order` / `flex` rules in the ≤500px media query. `.pbox.mono`
already sets `display: flex` explicitly, so the anchor's inline default is not load-bearing. The
no-author `<div>` therefore lands in the same box. Task 3 verifies this by measurement instead of by
reading, because "the CSS does not care" is the kind of claim that is true until a UA stylesheet
disagrees.

### 5. The delta is written against the phone change's text, and ordering is called out

Two unarchived deltas would otherwise both claim to restate the same requirement from the stale main
spec, and whichever folded second would revert the other. Writing this one on top of the shipped
text and recording the ordering in tasks keeps the fold deterministic: phone first, then this.

## Risks / Trade-offs

- **The card's left edge stops leading to the work.** → Accepted; it is the point of the change. The
  title, the English title row and the card's whole text column still open the work, and the portrait
  was never the card's primary target — it has no label and no focus stop.
- **Two adjacent destinations on one card may read as ambiguous.** → Mitigated by meaning rather than
  by chrome: the face and the author name now agree, which is one *fewer* rule to learn than the
  current arrangement, where the face and the name disagree.
- **The phone change is folded after this one, reverting the paragraph.** → Mitigated by decision 5
  and by task 5.2; if the fold happens out of order, the symptom is the spec, not the site, and
  `openspec validate --changes` plus a diff of the requirement catches it.
- **A future change points the strip somewhere with no visible equivalent.** → Mitigated by making
  the redundancy a normative requirement with its own scenario, not a comment.

## Migration Plan

None. A static-site markup change: the next build emits different `href`s. Rollback is reverting the
commit — no data, no schema, no cached artefact, no URL that anything else links to.
