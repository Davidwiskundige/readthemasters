# Change: work-significance

## Why

A reader landing on a historic paper benefits from a short editorial note on *why it matters* — its
place in the history of mathematics. This is context we can add that the faithful transcription
deliberately does not carry.

## What changes

- Add an optional `significance` field to `work.yaml`: a short editorial paragraph on the work's
  historical importance. Editorial content (ours), distinct from the faithful transcription.
- Surface it on the work page as a clearly-labelled "Significance" callout.
- Add it to the Fagnano example (elliptic/Abelian function theory → Riemann surfaces …).

## Impact

- Extends `corpus-format` (optional field, no gate change) and `site-catalog` (display).
- New: `significance` in `build_site_data` output and the work page.
