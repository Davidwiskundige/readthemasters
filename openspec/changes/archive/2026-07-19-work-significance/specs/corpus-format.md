# Spec (delta): work-significance

## MODIFIED: work.yaml schema

Adds one optional field:

- `significance` (string, optional) — a short **editorial** paragraph on the work's historical
  importance and influence. This is our commentary, kept distinct from the faithful
  transcription; it does not affect the copyright gate. Best added at review time by someone with
  the domain context.
- `significance_sources` (list, optional) — references backing the significance note, each
  `{citation, url?}`; shown as a "Sources" line under the callout.

## MODIFIED: Work page (site-catalog)

When `significance` is present, the work page shows it as a clearly-labelled "Significance"
callout, visually distinct from the transcription so it reads as editorial context, not the
author's text.
