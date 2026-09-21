## Context

Three pages filter a list client-side by setting the `hidden` attribute on each excluded row:

| Page | Row element | Rule that defeats `hidden` |
|---|---|---|
| `/` catalog | `.catalog .card` | `global.css:84` `display: flex` (and again at `:113` under the phone breakpoint) |
| `/authors/` | `.authorlist .card` | `global.css:161` `display: flex` |
| `/journals/` | `.journallist .jrow` | `global.css:228` `display: flex` |

`hidden` is not a CSS-level primitive. It hides an element only because the user-agent stylesheet
ships `[hidden] { display: none }`, and UA-origin declarations lose to author-origin ones whatever
their specificity. Each of the three rules above was added for an unrelated reason — seating a 69px
portrait beside the card text, or laying out a title-led journal row — and silently disarmed the
attribute for that list.

Verified against the dev server: after setting `hidden` on 26 of 27 catalog cards,
`getComputedStyle(card).display` is `"flex"` and all 27 remain in flow. `/authors/` (18 rows) and
`/journals/` (15 rows) behave identically.

Everything else about the filters is correct. `apply()` computes `ok` correctly, the live count and
the empty-state paragraph both update, and the catalog's URL sync round-trips. The count element is
a `<span>` and the empty-state is a `<p>`, neither carrying an author `display` rule — which is
exactly why the count kept telling the truth while the list did not.

The site has no DOM- or CSS-level test harness: `npm test` runs `node --test` over three pure-function
suites in `src/lib/` (`fitmath`, `significance`, `tex`).

## Goals / Non-Goals

**Goals:**

- A row excluded by any client-side filter is removed from the rendered list on all three pages.
- The fix holds for lists added later without anyone having to remember this failure mode.
- No change to filter logic, markup, or the portrait layout the `display: flex` rules exist for.

**Non-Goals:**

- Introducing a DOM/CSS test harness (jsdom, Playwright) to the site. Worth discussing on its own
  merits; disproportionate as a gate on a one-line invariant.
- Touching the `hidden` usages that work correctly today — the work page's text-panel tabs, the
  search page's mode panels, and its formula preview — all on elements with no author `display` rule.
- Reworking the filter scripts to use a class instead of the attribute.

## Decisions

**Decision: restore `hidden` globally with `[hidden] { display: none !important; }` in `global.css`.**

`!important` is the only mechanism that makes an author-origin `[hidden]` rule beat another
author-origin `display` rule whose selector may be arbitrarily more specific. A non-`!important`
`[hidden] { display: none }` would lose to `.catalog .card` on specificity — an attribute selector
counts at the class level, so (0,1,0) against (0,2,0) — and the bug would persist unchanged.

This is the conventional idiom rather than a local invention: Normalize.css, Tailwind's Preflight,
and the Artifact runtime reset all ship exactly this declaration, for exactly this reason.

*Alternatives considered:*

- **Targeted attribute selectors** — `.catalog .card[hidden], .authorlist .card[hidden],
  .journallist .jrow[hidden] { display: none }`. Avoids `!important` and fixes today's three
  surfaces. Rejected: it is a hand-maintained list that rots by construction. The bug arrived
  because someone added `display: flex` to a filtered list without knowing this coupling existed;
  that is precisely the event this option fails to cover. The next filtered list reintroduces it.
- **Stop using `hidden` in the filter scripts** — a `.is-out { display: none }` class set by JS
  instead. Rejected: three files changed instead of one, it gives up the attribute's accessibility
  semantics (`hidden` removes the element from the accessibility tree as well as from paint), and
  it leaves the trap armed for the `hidden` usages that remain elsewhere in the site.
- **`content-visibility` / `[hidden] { display: revert-layer }`** — rejected as strictly more
  obscure with no advantage.

**Decision: state the guarantee in the spec as a rendering outcome, not as a CSS mechanism.**

The delta requirement says the excluded row is not rendered and that the rendered row count equals
the displayed count. It deliberately does not name `hidden`, `display: none`, or `!important`: a
future rewrite that swaps the attribute for a class should still satisfy the spec, and the spec
should not have to be edited to permit it. The mechanism lives here in design.md.

**Decision: place the rule near the top of `global.css`, with a comment naming the coupling.**

Placement is cosmetic given `!important`, but a reader who meets the rule mid-file will wonder why
it shouts. The comment should say what the rule defends against — that `hidden` loses to any author
`display` rule — so the next person adding `display: flex` to a card does not have to rediscover it.

## Risks / Trade-offs

- **`!important` overrides a future deliberate "hidden but displayed" element** → No such element
  exists in the site today, and the combination is self-contradictory: an element that should be
  visible should not carry `hidden`. If one is ever genuinely needed, it can carry a different
  attribute or a class.
- **`!important` is a blunt instrument and invites imitation** → Mitigated by the comment scoping
  the justification to this one case (an author rule restoring a UA guarantee), and by it being a
  recognized library idiom rather than a local pattern.
- **Pagefind indexes the work page's non-default text panels, which carry `hidden`** → Unchanged.
  `section[data-panel]` has no author `display` rule, so the UA `[hidden]` rule already computes
  `display: none` on those panels today; the new rule reaches the same result by the same path.
  Nothing about what Pagefind sees at build time changes.
- **The fix is invisible to `npm test` and to CI** → Accepted for a one-line change whose effect is
  directly observable. Verification is manual against the dev server, enumerated in tasks.md, on
  all three pages and at both the desktop and phone breakpoints (the catalog re-declares
  `display: flex` inside its media query, so the phone width is a distinct check).
