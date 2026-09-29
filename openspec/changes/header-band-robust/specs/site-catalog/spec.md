## MODIFIED Requirements

### Requirement: Header paper band

Every page of the site SHALL paint a warm band of colour behind its top, fading out into the page
background: a linear fade from a band-top tone to transparent, under a faint radial glow in the
accent colour centred just above the header. The band MUST be drawn on its own layer behind the
page content, not as the background of `body` or `html`. Those stay a flat `--bg`, because some
browsers (Samsung Internet on Android, seen in practice) mis-draw a sized gradient there as a near-solid block with
a hard edge. The layer MUST NOT receive clicks or change the layout of anything on the page.

The band MUST fade to transparent rather than to a named colour, so its bottom can never form an
edge, whatever colour a browser actually draws the page in.

The band has a fixed height measured from the top of the document, independent of how long the
page is, and it scrolls with the page. Below it the page MUST be exactly the flat `--bg`. The
glow's width MUST be proportional to the viewport width (37.5%), not a fixed length, so its
strength is the same on narrow and wide screens.

The band's height and colours are tokens set per colour scheme and per screen width. Below 40rem
the band is quieter and shorter, because a phone screen shows it much more strongly than a laptop
does:

| Width | Scheme | Height | `--band-top` | `--band-glow` |
| --- | --- | --- | --- | --- |
| ≥ 40rem | light | 16rem | `#f5f0e8` | light accent `#7a4b2b` at 5% |
| ≥ 40rem | dark | 16rem | `#231e18` | dark accent `#d69a6a` at 8% |
| < 40rem | light | 12rem | `#f8f5ef` | light accent at 3% |
| < 40rem | dark | 12rem | `#1a1815` | dark accent at 3% |

Each page MUST carry `theme-color` meta tags that give the band's top colour for the visitor's
scheme and width, so a browser that tints its toolbar matches the band rather than cutting against
it.

Text drawn on the band MUST keep WCAG AA contrast (4.5:1) at the band's top. The lowest-contrast
text token, `--muted`, measures about 4.9:1 on `#f5f0e8`, 5.1:1 on `#f8f5ef`, 6.1:1 on `#231e18`
and 6.6:1 on `#1a1815`. A later change to these colours MUST re-check this.

Where the band is painted, the site header's bottom rule MUST be transparent. The footer's top
rule is unchanged. In print the band MUST NOT be drawn.

A change to the band MUST be checked on a real phone in dark mode, not only in a desktop browser
at phone width. A desktop browser reproduced neither of the two phone failures this requirement
guards against.

#### Scenario: Every page has the band

- **WHEN** a visitor opens any page (catalog, timeline, search, an author, a journal, a work, or a legal page)
- **THEN** the top of the page shows the warm band behind the header, fading out into the flat paper colour, and the header carries no bottom hairline

#### Scenario: The band fades out on a phone browser

- **WHEN** a visitor opens the site on a phone in Samsung Internet with the system in dark mode
- **THEN** the band fades out gradually over its height, with no solid block and no hard edge where it ends

#### Scenario: No edge at the band's end even if the page is recoloured

- **WHEN** a browser draws the page background in a colour other than `--bg`, as a forced dark mode does
- **THEN** the band still fades into it without a visible edge, because the band ends transparent

#### Scenario: A long page and a short page look the same at the top

- **WHEN** a visitor compares a one-screen page with a work page many screens long, at the same window size
- **THEN** the band has the same height and the same colours on both, and the long page is flat `--bg` everywhere below it

#### Scenario: The band scrolls away

- **WHEN** a visitor scrolls a page down past the band's height
- **THEN** the band has scrolled out of view with the header, and the visible background is flat `--bg`

#### Scenario: A phone gets the quieter band

- **WHEN** the viewport is narrower than 40rem
- **THEN** the band is 12rem tall with the narrow-screen colours of the current scheme, and at 40rem or wider it is 16rem with the wide-screen colours

#### Scenario: The glow keeps its strength on a narrow screen

- **WHEN** the same page is viewed on a 390px-wide and a 1280px-wide screen
- **THEN** the glow fades out towards both sides on both, rather than lying at full strength across the narrow one

#### Scenario: Each colour scheme has its own band

- **WHEN** the visitor's system is in dark mode
- **THEN** the band starts from the dark scheme's band-top colour for the current width, not the light one

#### Scenario: The toolbar matches the band

- **WHEN** a browser that honours `theme-color` shows the top of any page
- **THEN** its toolbar is tinted with the band's top colour for the current scheme and width

#### Scenario: Text on the band stays legible

- **WHEN** muted or link text sits at the very top of the band, in either scheme and at either width
- **THEN** its contrast against the band is at least 4.5:1

#### Scenario: The band does not print

- **WHEN** a visitor prints any page
- **THEN** the band is not printed
