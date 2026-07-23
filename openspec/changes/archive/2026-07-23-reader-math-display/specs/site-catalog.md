# Spec (delta): reader-math-display

## MODIFIED: Work page

Adds the display-math behaviour to the existing rendering requirement:

Display math never collides with its equation number. Each display equation is its own horizontal
scroll area, a formula wider than the text column is left-aligned so scrolling starts at the
beginning of the formula, and a `\tag{n}` that cannot fit beside its formula moves to a line of
its own, right-aligned beneath it. Which layout applies is decided by measuring the rendered
formula, not by a viewport breakpoint, so a long formula stacks its number at any screen width.

## MODIFIED: Significance note

Math in the significance note is rendered by KaTeX, as in the transcription, so notation written
in the editorial prose reads as notation.
