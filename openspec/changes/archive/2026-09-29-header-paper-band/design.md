## Context

The page background is one flat token, `--bg` (`#fbfaf7` light, `#171614` dark), set on `body` in
`site/src/styles/global.css`. The header is separated from the content by a 1px `--border` rule.
All pages share `Base.astro` and `global.css`, so a `body` background reaches every page.

Several gradient options were explored: a whole-page wash, an edge vignette, and a band at the top.
The band won because it adds character where a page begins and leaves the long reading stretch
untouched. It was then tried on the real site, as a stylesheet appended to the built `dist/` and
served with `astro preview`, and the light values were softened after a first pass read too strong
next to the dark ones.

## Goals / Non-Goals

**Goals:**
- A quiet, warm head to every page, equal in strength in both colour schemes.
- Identical at the top of every page, whatever its length.
- CSS only, confined to `global.css`.

**Non-Goals:**
- Any change to the reading area below the band, to cards, badges or figures.
- Page transitions, fades on load, or other motion. These were explored and set aside.
- Scroll-edge fades on the timeline or wide equations. That's a separate idea, maybe for a later change.
- A user-facing toggle.

## Decisions

**Background layers on `body`, sized to a fixed 16rem.** Three layers: a radial glow, a linear fade
from `--band-top` to `--bg`, then `--bg` itself. The first two have `no-repeat` and
`background-size: 100% 16rem`.
*Alternative:* a gradient over the full document height. Rejected: it stretches with page length, so
it's steep on the contact page and invisible on a memoir. *Alternative:* `background-attachment:
fixed`. Rejected: iOS Safari ignores it, and it forces a repaint on every scroll.

**Tokens, not literals.** `--band-top` and `--band-glow` live beside `--bg` in both `:root` blocks,
so the band follows the scheme the same way everything else does. The glow is the scheme's accent at
low alpha (5% light, 8% dark), written as an `rgba()` literal of the accent rather than
`color-mix()`. That keeps the tokens plain values and avoids depending on `color-mix` support.

**Light values matched to the dark band's strength.** The dark band moves roughly +12/+8/+4 per RGB
channel from its `--bg`. The first light value, `#f1e8db`, moved −10/−18/−28, much further and
warmer, and read as "extreme". `#f5f0e8` (−6/−10/−15) and a 5% glow read as equally quiet.

**Drop the header's bottom rule.** Keeping it on top of the band looked like two separators at once.
Set it with `border-bottom-color: transparent`, not `border: none`, so the header keeps its height and
nothing below it moves.

**Print: `body { background: none }` under `@media print`.** Browsers that print backgrounds would
otherwise print a grey wash.

## Risks / Trade-offs

- **Dark-mode banding.** Over 16rem the dark fade spans only a few 8-bit steps per channel, which
  can show as stripes on low-quality panels. → No stripes were visible in the preview. If it shows
  up, add a tiny noise layer, or shorten the dark band.
- **Opaque boxes high on the page cut through the band.** The timeline's `.tl-scroll`, the search
  input and `.significance` sit on `--surface` or their own colour. → Checked on catalog, timeline
  and a work page, where they read as paper laid on the tone, not a clash. Recheck search, author and
  journal pages during implementation.
- **Phone width.** The nav wraps to two or three lines, so the header grows and uses more of the
  band. → The band still reaches past the header into the page title. Acceptable, but check it.
- **Header separation.** Without the hairline, a page whose content starts with its own light box
  could lose the header/content boundary. → Part of the page-by-page check. If a page needs it,
  restore the rule there rather than site-wide.

## Migration Plan

CSS only. Rolling back means reverting one commit. No data, URLs or markup change.
