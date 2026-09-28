## ADDED Requirements

### Requirement: Header paper band

Every page of the site SHALL paint a warm band of colour behind its top, fading into the page
background `--bg`: a linear fade from a band-top tone to `--bg`, under a faint radial glow in the
accent colour centred just above the header. The band MUST be a page background only — it adds no
element, markup or script, and nothing on the page is laid out differently because of it.

The band MUST have a fixed height of 16rem measured from the top of the document, independent of
how long the page is, and it scrolls with the page. Below it the background MUST be exactly the flat
`--bg` it is today.

The band's colours are tokens defined per colour scheme, next to `--bg`:

| Scheme | `--band-top` | `--band-glow` |
| --- | --- | --- |
| light | `#f5f0e8` | the light accent `#7a4b2b` at 5% alpha |
| dark | `#231e18` | the dark accent `#d69a6a` at 8% alpha |

Text drawn on the band MUST keep WCAG AA contrast (4.5:1) at the band's darkest point — the
lowest-contrast text token, `--muted`, measures about 4.9:1 on `#f5f0e8` and 6.1:1 on `#231e18`.
A later change to the band's colours MUST re-check this.

Where the band is painted, the site header's bottom rule MUST be transparent — the band's tonal
change separates header from content. The footer's top rule is unchanged. In print the page
background MUST be dropped, so the band never prints.

#### Scenario: Every page has the band

- **WHEN** a visitor opens any page — catalog, timeline, search, an author, a journal, a work, or a legal page
- **THEN** the top of the page shows the warm band behind the header, fading into the flat paper colour, and the header carries no bottom hairline

#### Scenario: A long page and a short page look the same at the top

- **WHEN** a visitor compares a one-screen page with a work page many screens long, at the same window size
- **THEN** the band has the same height and the same colours on both, and the long page is flat `--bg` everywhere below it

#### Scenario: The band scrolls away

- **WHEN** a visitor scrolls a page down past its first 16rem
- **THEN** the band has scrolled out of view with the header and the visible background is flat `--bg`

#### Scenario: Each colour scheme has its own band

- **WHEN** the visitor's system is in dark mode
- **THEN** the band fades from `#231e18` into the dark `--bg`, not from the light band's colour

#### Scenario: Text on the band stays legible

- **WHEN** muted or link text sits at the very top of the band in either scheme
- **THEN** its contrast against the band is at least 4.5:1

#### Scenario: The band does not print

- **WHEN** a visitor prints any page
- **THEN** no page background is printed, the band included
