# Project conventions — ReadTheMasters

This file orients an AI assistant (and human contributors) working in this repo. See
[PLAN.md](../PLAN.md) for the full design; this is the quick reference for *how we work*.

## What this project is

A static website + git-versioned corpus that publishes AI LaTeX transcriptions and translations of
**public-domain** mathematics and physics texts. Goals and non-goals: PLAN.md §1.1.

## Stack

- **Corpus:** plain-text LaTeX + YAML, one folder per work under `corpus/`.
- **Validation / pipeline:** Python 3.11+ (only dependency: PyYAML). Entry point `pipeline/validate.py`.
- **Site:** Astro static site, KaTeX for math, Pagefind for search, client-side facet filtering
  over a build-time `catalog.json`. Hosted on Cloudflare Pages / GitHub Pages.
- **PDFs:** Tectonic in CI (later phase).
- **CI:** GitHub Actions — the copyright gate + LaTeX compile must pass before anything merges.

## Non-negotiable rules

1. **The copyright gate is absolute.** Nothing publishes unless `pipeline/validate.py` passes.
   It evaluates BOTH life+70 (author death date) AND the US 95-year rule (first-publication date),
   plus edition rights and translation provenance. Copyright-critical facts must be *sourced*
   (PLAN.md §2.5).
2. **Faithful content, standardized markup.** Transcribe the original faithfully; never modernize
   notation. Standardize only the LaTeX markup via the shared preamble (PLAN.md §4.4).
3. **The project pays for no AI compute.** All AI runs on contributors' own accounts (PLAN.md §7).
4. **Provenance is mandatory.** Every artifact records model, effort, prompt version, status.

## Spec-driven workflow

Each feature is a change proposal under `openspec/changes/<name>/` with `proposal.md`, delta
`specs/`, and `tasks.md`. When a change ships, its specs fold into `openspec/specs/` (the source of
truth for what the system IS) and the change moves to `openspec/changes/archive/`.

**Adding a new text is NOT a spec change** — it is an ordinary pull request, gated by CI.

**Shipped (in `specs/`, archived under `changes/archive/`):** `corpus-format`, `copyright-gate`,
`site-catalog`, `transcription-pipeline` (Tier-2 Claude Code skill so far — see
`.claude/skills/transcribe/`).

**Upcoming proposals (not yet built):** `transcription-pipeline` Tier-3 (Batch API scan → LaTeX),
`translation-pipeline` (LaTeX → LaTeX + glossary), `search` (Pagefind full-text). Before extending
a shipped capability, write a change under `changes/<name>/` with delta specs, implement, then fold
the deltas into `specs/` and archive.

## Conventions

- ISO dates (`YYYY-MM-DD`) or bare years where only a year is known.
- Canonical work IDs: Wikidata QID → DOI → deterministic slug (PLAN.md §3.2).
- Controlled vocabulary in `corpus/vocab.yaml`; CI rejects values outside it.
- Commits/PRs carry a DCO `Signed-off-by` line (PLAN.md §11.1).
