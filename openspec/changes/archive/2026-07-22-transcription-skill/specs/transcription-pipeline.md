# Spec (delta): transcription-skill

## ADDED: Tier-2 transcription skill

A Claude Code skill at `.claude/skills/transcribe/` transcribes a work's scan pages into the corpus
and opens a pull request. Invoked as `/transcribe <work-id> <pages>`; both arguments may be omitted
and requested interactively. It runs on the contributor's own Claude Code account — the project
pays for no AI compute.

The skill MUST:

- **Gate first.** Refuse to transcribe or open a PR unless the work passes `pipeline/validate.py`.
  For a new work it helps author `work.yaml` from the bundled template, requires the
  copyright-critical facts to be sourced, and fills `copyright_assessment` via `--write` (never
  hand-written verdicts).
- **Transcribe faithfully** per `prompts/transcribe-chat.md` and `corpus/HOUSESTYLE.md`: preserve
  the author's notation and spelling; normalize only typography; emit `\origpage{N}` per page; flag
  uncertainty with `\uncertain{}`/`\illegible`; never redraw figures (`\rmfigure` placeholder);
  reproduce printer's errors and flag them rather than "fixing" them.
- **Run a verification pass** comparing the assembled `original.tex` against each scan page, and
  record the flagged pages in provenance.
- **Record honest provenance.** `status: ai-draft` for machine output; `model`, `effort`,
  `prompt_version` (matching the prompt followed), `submitted_via: skill`, `produced` date. A higher
  status is set only when a human has actually done that level of review.
- **Validate** (`pipeline/validate.py` and `pytest pipeline/tests`) before proposing anything.
- **Checkpoint with the human** — present the transcription, uncertain passages, and gate result
  for correction — then commit with a DCO `-s` sign-off on a branch and open a PR (never push to
  `main`). The PR body states pages, model, `prompt_version`, flagged pages, and `ai-draft` status.

Translation is a separate step (`prompts/translate-chat.md`), out of scope for this delta.
