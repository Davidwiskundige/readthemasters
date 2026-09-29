## Context

`header-paper-band` put the band on the `body` background: a radial glow and a linear fade to
`--bg`, both sized `100% 16rem` and not repeated, over `--bg`. On the maintainer's phone (Samsung
Internet, Android, dark mode) a screenshot showed the band as a near-constant `#231e18` for its
whole height, then a jump over about 6px to `--bg` at 16rem. A test page with the same gradient on
an ordinary `div` faded correctly. So the failure is specific to the background moving from
`body` onto the canvas, not to gradients in general.

After the band moved to its own layer, it faded correctly on the phone but still read as too
strong, even at half the colour difference (`#1d1a16`), while the same CSS looked right on the
laptop. A comparison page with five strengths, and then a narrow-screen block, settled the values
below, checked on the phone at each step. Every value in this change was approved on the real
device.

## Goals / Non-Goals

**Goals:**
- A band that cannot form an edge in any browser, whatever it does with the page background.
- The same perceived strength on phone and laptop, laptop values unchanged.
- The toolbar matches the band where browsers tint it.

**Non-Goals:**
- Detecting OLED or screen brightness. CSS cannot do that reliably, so width is the proxy.
- Changing the laptop look: the wide-screen values stay exactly as approved in PR #92.
- Fixing the colour above the page when it is pulled down past the top. That area shows the canvas
  colour `--bg` and is left as is.

## Decisions

**Own layer: `body::before`, absolutely positioned at the top of the document.** `top: 0; left: 0;
right: 0; height: var(--band-h); z-index: -1; pointer-events: none`. With `body` not positioned,
the layer is placed against the initial containing block, so it sits at the top of the document
and scrolls with it. `z-index: -1` paints it above the canvas background but below all in-flow
content.
*Alternative:* a real element in `Base.astro`. Rejected: it needs markup for pure decoration, and
the pseudo-element is enough. *Alternative:* keep `body` and add `html { background: var(--bg) }`
to stop the background moving to the canvas. Rejected: it relies on the same fragile path through
browser-specific handling. The test page showed that an ordinary element works.

**Fade to `transparent`, not to `--bg`.** The band then only ever adds tone over whatever the page
is. Chromium, WebKit and Gecko interpolate gradients in premultiplied alpha, so fading to
`transparent` does not grey out halfway.

**Glow width `37.5%`.** The old glow was 960px (60rem) wide at every width. On a 1280px laptop
that is 37.5% of the width, so the laptop look stays the same. On a 390px phone, the average glow
strength at the top drops from 0.52 to 0.19, the laptop's value. The percentage is of the layer's
width, which is the viewport width.

**Narrow-screen tokens below 40rem, and a height token `--band-h`.** A phone's OLED screen shows
dark-tone differences that a laptop LCD's backlight blurs, and 16rem covers a larger share of a
phone screen. Halving the colour difference alone (`#1d1a16`) made no visible difference on the
phone. What was approved was `#1a1815` with a 3% glow and 12rem height in dark, and `#f8f5ef` with
a 3% glow in light, from the same comparison. 40rem (640px) sits above every phone width and below
the laptop, and matches the layout's own narrow breakpoints.

**`theme-color` per scheme and width.** Four `<meta name="theme-color">` tags with `media`
queries combining `prefers-color-scheme` and `max-width: 40rem`, set to the matching
`--band-top`. Samsung Internet ignored the tag in dark mode in testing. Chrome for Android and iOS
Safari use it. The values are repeated from the CSS tokens because a meta tag cannot read a CSS
variable, so a comment beside the tokens points at `Base.astro`.

## Risks / Trade-offs

- **Two copies of the colours** (CSS tokens and meta tags). → A comment at both places. The spec's
  scenario "The toolbar matches the band" makes a mismatch a spec violation.
- **Width is only a proxy for "phone".** A narrow desktop window gets the quiet band, and a large
  phone in landscape (over 640px) gets the laptop band. → Acceptable: both look fine, just
  stronger or quieter than intended.
- **`z-index: -1` layer behind content.** Any future element with a transparent background
  and its own stacking context stays above it. An element given `z-index` below −1 would slip
  under it. → None exists today. The rule's comment says why the layer is at −1.
- **Pulling past the top** still shows flat `--bg` above the band. → Out of scope (see Non-Goals).

## Migration Plan

CSS plus four meta tags. Rolling back means reverting the commit, which restores the
`header-paper-band` behaviour. Before merging, check on the real phone over the LAN
(`astro preview --host`).
