## Why

The header paper band (shipped in `header-paper-band`, PR #92) looks right on a laptop but not on
a phone. On the maintainer's Android phone in Samsung Internet, dark mode, it rendered as a
near-solid block of the band colour with a hard edge where it ends, 16rem down. A test page traced
this to the band being the `body` background, which browsers move onto the whole canvas: the same
gradient on an ordinary element faded correctly. Once fixed, it was still too strong on the phone.
An OLED phone screen shows small differences between dark tones that a laptop LCD blurs, the band
covers more of a small screen, and the glow, a fixed 60rem wide, sat at full strength across a
narrow one. The desktop browser at phone width reproduced none of this. Each fix below was checked
on the real phone over the LAN.

## What Changes

- The band moves off the `body` background onto its own layer behind the content (`body::before`,
  16rem tall, ignoring clicks). `body` goes back to a flat `--bg`.
- The band fades to **transparent** instead of to `--bg`, so its bottom cannot form an edge even
  if a browser draws or recolours the page background differently.
- The glow's width is **37.5% of the viewport** instead of 60rem. That's the same on a 1280px
  laptop, and on a phone it fades out towards the sides again instead of lying on the whole width
  at full strength.
- **Narrow screens (below 40rem)** get a quieter, shorter band: 12rem tall; light `#f8f5ef`, dark
  `#1a1815`, glow at 3% in both. Wider screens keep the approved values: light `#f5f0e8` / 5%,
  dark `#231e18` / 8%.
- A `theme-color` meta tag per scheme and width, matching the band's top colour, so browsers that
  tint their toolbar do not draw a flat bar against it.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities

- `site-catalog`: the "Header paper band" requirement changes. The band is painted on its own
  layer and fades to transparent. The glow is sized to the viewport. Narrow screens get their own
  height and colours. `theme-color` tags are added. Verification on a real phone becomes part of
  the requirement.

## Impact

- `site/src/styles/global.css`: band tokens (plus a narrow-screen block), `body` background back
  to flat `--bg`, a new `body::before` rule, and the print rule now hides the layer.
- `site/src/layouts/Base.astro`: `theme-color` meta tags in the head.
- No data, pipeline or script changes. The header rule stays transparent, as today.
