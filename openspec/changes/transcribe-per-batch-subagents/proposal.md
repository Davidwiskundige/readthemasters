## Why

The Tier-2 `/transcribe` skill keeps every scan page in the session's context for the rest of the
run, so the cost of transcribing page *N* grows with *N*. Measured over three long works:

| work | pages | turns | mean context/turn | total tokens | tokens/page |
|---|---|---|---|---|---|
| `abel-1841-fonctions-transcendantes` | 91 | 1241 | 482k | 600M | 5.8M |
| `riemann-1857-abelsche-functionen` | 42 | 735 | 362k | 267M | 5.4M |
| `clebsch-1864-anwendung-abelschen-functionen` | 18 of 55 | 347 | 220k | 76M | 4.2M |

Attributing each context block by residency (its token size × the number of later turns it stays
resident), page scans are **60.8% / 47.2% / 62.6%** of all context spent in those three runs. Abel's
context ran from 162k at its 5th-percentile page to 773k at its 95th — the last pages cost roughly
five times the first for identical work — and peaked at 920k.

Three consequences follow, all measured:

- **The tail pays for scans it does not use.** In the Abel run, 323 turns (26% of the session) ran
  *after* the last page image was read — stitching, linting, site preview, the PR — consuming 178M
  tokens (30% of the session) while carrying 380k of dead scans.
- **Cache misses scale with context.** 2.3% / 9.4% / 9.5% of turns lost the cache prefix beyond the
  first ~39k and re-wrote the whole conversation, accounting for 23% / 52% / 61% of each run's cost.
  The trigger is not visible in the transcripts and is not something the skill causes, but the cost
  of each miss is linear in context size.
- **Whole-work memory is partly illusory anyway.** The Abel run compacted at turn 1071, discarding
  the early pages outright — so for its last stretch the cross-page context this design is supposed
  to buy was already gone.

The Tier-3 path (`pipeline/transcribe.py`) already solves this — one request per page carrying only
the pinned prompt, the page image, and the previous page's tail — but it runs on the Anthropic Batch
API against a contributor's `ANTHROPIC_API_KEY`. Tier-2 exists precisely so a contributor can work
on a Claude Code subscription instead, so the fix must keep the vision work inside Claude Code.

## What Changes

- **Per-batch subagents do the page-level vision work.** The main session stops calling `Read` on
  scan images entirely. For each batch of pages it dispatches one subagent that reads that batch's
  images, writes `pages/pNNN.tex` fragments, and returns a short text report. The images never enter
  the main session, so its context stays flat across the whole work.
- **A per-work notation glossary carries cross-page consistency.** Work-spanning rendering decisions
  (this work's Fraktur usage, its long-ſ/ß handling, its function-application notation — the class
  of decision recorded as HOUSESTYLE R12, R13, R19, R23) move out of conversational context into a
  reviewable file that every batch reads and may append to. Each batch also receives the previous
  batch's trailing lines so text spanning a page break is joined correctly.
- **The verification pass becomes per-batch too**, reading fragment plus images in a fresh context
  and returning only a discrepancy list, rather than relying on scans still being resident.
- **One image per page, cropped to the printed text block, with capped per-page escalation.** A new
  `pipeline/` helper replaces ad-hoc half-page crops: measured at 2,375 tokens/page against 4,274 for
  two half-crops, and — the part that matters — one `Read` per page instead of two, since turns
  dominate the cost. This does cost resolution: the 1568px cap applies to the long edge, which on a
  portrait page is the height, so a full page yields ~1180px of text width against a half-crop's
  1500px, and cropping margins cannot close that gap. It is bought back per page instead, by
  magnifying a specific doubtful region (capped, default 3 per page). Abel 1841's 91 pages were
  transcribed at exactly this resolution.
- **An A/B quality check gates the rollout.** Clebsch pages 189–206 are already transcribed under
  the current architecture; re-transcribing a sample under the new one and diffing against the
  committed text measures any quality change on the same work and the same scans before the
  remaining 37 pages are committed.
- **`\uncertain{}` / `\illegible` flagging is made to actually happen.** All three works above carry
  **zero** flags across 151 transcribed pages, so there is currently no signal of where the model was
  unsure — and therefore no instrumentation to detect a quality regression from this change or any
  other. Provenance records the flag count so an empty result is visible rather than silent.

No change to what a transcription *is*: faithfulness, house style, the copyright gate, provenance
honesty, and the human review checkpoint are all untouched.

## Capabilities

### New Capabilities

None. This changes how the existing Tier-2 path executes, not what the system offers.

### Modified Capabilities

- `transcription-pipeline`: the Tier-2 skill requirement gains a bounded-context execution model
  (per-batch subagents, main session free of scan images); the verification-pass requirement becomes
  per-batch; new requirements cover the per-work notation glossary, the text-block crop helper, and
  recording the uncertainty-flag count in provenance.
- `corpus-format`: the work-directory layout gains the optional, **permanent** `notation.md`
  artifact — committed with the transcription and retained after it reaches `verified`.

## Impact

- `.claude/skills/transcribe/SKILL.md` — Phases 3–5 rewritten around the batch loop; Phases 4 and
  6–8 stated as running with no images in context.
- `pipeline/` — new text-block crop helper (PyYAML-only or standard-library; must not add a
  dependency to the CI gate, and must not import `anthropic`).
- `corpus/<work-id>/notation.md` — new optional per-work artifact; `pipeline/validate.py` must
  tolerate its presence.
- `corpus/HOUSESTYLE.md` — a ruling recording the glossary convention.
- `prompts/transcribe-chat.md` — unchanged in substance; `prompt_version` bumps only if the wording
  the subagent follows changes.
- `openspec/specs/transcription-pipeline/spec.md` — folded in when this ships.
- Out of scope: the Tier-3 Batch API path (already bounded), and the `/translate` skill (works from
  `original.tex`, reads no images — same accumulation shape but far smaller, worth a separate
  change).
