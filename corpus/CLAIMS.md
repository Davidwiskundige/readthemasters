# Claims — who is working on what

Claims are tracked as **GitHub issues**, not in this file. Before starting a work, open a
[**Claim a work**](https://github.com/Davidwiskundige/readthemasters/issues/new?template=claim.yml)
issue so two people don't transcribe the same text. First check the work isn't already in `corpus/`
(search by author + year, or by Wikidata QID) or already claimed.

**Live claim list:** [open issues labelled `claim`](https://github.com/Davidwiskundige/readthemasters/issues?q=is%3Aissue+is%3Aopen+label%3Aclaim).

## How claims expire

A daily GitHub Action (`.github/workflows/claim-expiry.yml`) keeps the list fresh — the work goes
fast with your own AI, so claims are short-lived:

- **No pull request within 24 hours** of opening the claim → it expires and the work is open again.
- **A pull request is linked** (mention the claim issue in the PR, e.g. `Claims #123`) → the claim
  lives as long as that PR is open, and is released when the PR is merged or closed.

## Already in the corpus (no claim needed)

These are done or in progress and live under `corpus/` with their status in `provenance.yaml`:

- `fagnano-1718-lemniscata` — transcription (pp. 293–297), `skimmed`; a full human check is welcome.
- `leibniz-1689-isochrona` — transcription `skimmed` (math checked); English translation in progress.
