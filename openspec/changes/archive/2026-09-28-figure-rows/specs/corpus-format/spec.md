## ADDED Requirements

### Requirement: Figure rows

Figures that the print sets side by side SHALL be written as adjacent `\rmfigure` lines with no
blank line between them, and the reader MUST render such a run as one row of figures that wraps
into a single column on a narrow screen. Figures separated by a blank line MUST render stacked, as
single figures. A figure printed between lines of the text column MUST be placed at that point in
the transcription, even where this splits a paragraph; a figure printed beside the text is placed
before the paragraph it stands beside. Grouping MUST follow the print and is never applied to
figures the print does not set side by side (HOUSESTYLE R30).

#### Scenario: Side-by-side figures render as a row

- **WHEN** a transcription has `\rmfigure{figures/fig-27.png}{Fig.~27.}{…}` on one line and `\rmfigure{figures/fig-28.png}{Fig.~28.}{…}` on the next, with no blank line between them
- **THEN** the reader renders both figures inside one row container

#### Scenario: Separated figures stay stacked

- **WHEN** two `\rmfigure` lines are separated by a blank line
- **THEN** the reader renders two separate figure blocks and no row container

#### Scenario: A row wraps on a narrow screen

- **WHEN** a row of two figures is displayed at phone width
- **THEN** the figures are shown one above the other, each at the width of the text column

#### Scenario: A figure printed mid-paragraph keeps its printed position

- **WHEN** the print sets a figure between two lines of one paragraph
- **THEN** the transcription places the `\rmfigure` between the text of those two lines
