---
name: transcribe
description: >-
  Transcribe scanned pages of a public-domain mathematics or physics text into
  house-style LaTeX and assemble them into the ReadTheMasters corpus, then open a
  pull request. Use when the user runs `/transcribe <work-id> <pages>`, or asks to
  transcribe a work's scan pages into the corpus. This is the Tier-2 contributor
  path (PLAN.md §4.1, §10): Claude Code does the vision transcription on the
  contributor's own account — the project pays for no AI compute.
---

# Transcribe a work into the corpus

You are running the repository's semi-automatic transcription pipeline. You (Claude Code, with
vision) play the role the Batch API plays in a Tier-3 run: you read the scan pages directly and
emit faithful, house-style LaTeX, then assemble, validate, and open a PR. **The human contributor
reviews before anything is pushed.**

Invocation: `/transcribe <work-id> <pages>` — e.g. `/transcribe fagnano-1718-lemniscata 293-297`.
Both arguments may be omitted; ask for whatever is missing.

## Non-negotiables (read first)

1. **The copyright gate is absolute.** Never transcribe or open a PR for a work that does not pass
   `pipeline/validate.py`. If `work.yaml` is missing sourced copyright facts, STOP at Phase 1 and
   resolve that first — the gate evaluates BOTH life+70 and the US 95-year rule, plus edition
   rights and translation provenance (`openspec/specs/copyright-gate/spec.md`).
2. **Faithful content, standardized markup.** Transcribe exactly what is printed. Never modernize
   notation, correct the author, or paraphrase. Standardize only LaTeX markup. The full rules are
   in `prompts/transcribe-chat.md` and the rulings log in `corpus/HOUSESTYLE.md` — treat both as
   authoritative.
3. **Honest provenance.** Machine output ships as `ai-draft`. Do not set a higher status than the
   review that actually happened (see the status ladder in PLAN.md §4.3: `ai-draft` → `skimmed` →
   `verified`).
4. **You do not decide public-domain status.** You compute it from sourced facts via the gate. If
   in doubt, surface it to the contributor; do not guess.
5. **You do not read scan images yourself.** Page images go to batch subagents (Phase 3). This is
   not a style preference — it is the difference between ~4.2M and ~150–200k tokens per page.

## Why this skill is shaped the way it is

A scan image read into a context stays there, and is re-sent on every later turn. Transcribing in
one long session therefore costs more for each page than the page before it: measured across three
long works, **4–6M tokens per page**, with page scans making up 47–63% of all context spent. The
worst run peaked at 920k context and compacted mid-work, losing its early pages anyway.

So page-level vision work happens in **subagents**, one per small batch. A subagent has a fresh
context, reads only its own batch's images, writes fragments to disk, and returns a short report.
The images never enter your context, so your context stays flat across a whole work, and the
assembly, validation and PR phases run with nothing heavy resident.

Measured cost model, if you need to reason about it: a subagent costs a fixed **~63k** plus about
**7.3k per page**, at roughly 2 turns per page. Three quarters of the total is the fixed part being
re-sent every turn, which is why **turns per page matter far more than batch size**. Keep pages at
one image and one write each.

## Before you start

Read these so your output matches the house style exactly:

- `prompts/transcribe-chat.md` — the canonical transcription rules and current `prompt_version`.
- `corpus/HOUSESTYLE.md` — the notation-vs-presentation principle and the rulings log.
- `corpus/<work-id>/notation.md`, if the work has one — this work's own cross-page decisions.
- `corpus/preamble/readmasters.sty` — the macros available (`\origpage`, `\uncertain`,
  `\illegible`, `\ednote`, `\rmfigure`).

## Phase 1 — Locate the work and clear the gate

1. If `corpus/<work-id>/work.yaml` exists, read it. Otherwise the work is new:
   - Help the contributor create `corpus/<work-id>/work.yaml` from
     `.claude/skills/transcribe/templates/work.yaml`. The `<work-id>` follows PLAN.md §3.2
     (Wikidata QID → DOI → `author-year-shorttitle` slug) and must equal the directory name.
   - Every copyright-critical fact (author death dates, first-publication year, edition) MUST be
     **sourced** in the `sources:` block, or the gate fails by design.
2. Fill/refresh the `copyright_assessment` block by running the gate in write mode, then reviewing
   the diff — never hand-write the verdicts:

   ```bash
   python pipeline/validate.py --write
   git diff corpus/<work-id>/work.yaml
   ```

3. Confirm the work is public domain. If `public_domain: false`, STOP and tell the contributor
   which rule failed — this work cannot be published.

## Phase 2 — Prepare the pages

- Use `source.scan_url` / `scan_id` in `work.yaml` to locate the pages named in `<pages>`.
- If the contributor has the images/PDF locally, use those. If pages must be downloaded, confirm
  the source and the page range with the contributor first (downloading is a side effect).
- Turn the raw scans into one prepared image per page:

  ```bash
  python pipeline/prepare_pages.py --images <scans> --pages <spec> --out <prepared>
  ```

  This crops each page to its printed text block and caps the long edge at 1568px, which is where
  the vision API downscales anyway. It prints a line per page (source size, crop box, output size,
  estimated tokens) and passes through any page whose text block it cannot find — check those by
  eye before transcribing.

- It also writes `<prepared>/zoom-map.json`, giving `offset_x`, `offset_y` and `scale` per page so a
  coordinate seen in a prepared image can be mapped back onto the source scan
  (`source_x = offset_x + prepared_x / scale`). **Pass the relevant rows to each batch subagent.**
  Without them a subagent has to infer the mapping, and a batch that did landed 2 of its 3
  magnification crops on the wrong lines — spending its whole per-page budget to settle nothing.
  Keep the raw scans reachable too: magnification crops come from those, not from the prepared
  image, which is where the lost resolution has to be bought back.

- Prepared pages live **outside the corpus**, in a scratch directory. They are working files; only
  figure crops (`corpus/<work-id>/figures/`) are ever committed.
- **A portrait page loses width to the 1568px cap** (~1180px of text against a half-page crop's
  1500px). That is the accepted trade — one image per page saves a turn, and turns dominate. Where
  a specific glyph is genuinely unreadable at that size, the batch subagent magnifies that region
  (see Phase 3), rather than every page being split in advance.

## Phase 3 — Transcribe in batches, via subagents

**You do not read the page images.** For each batch of pages, dispatch one subagent.

**Batch size: 4 by default.** The measured optimum is 2–4 and the curve is flat there; 4 keeps
several adjacent pages visible to one agent, which is what lets it join text across page breaks and
compare a doubtful glyph against a clearer instance nearby. Below about two batches' worth of pages,
just transcribe inline yourself — one subagent's fixed cost exceeds the saving on a very short work.

Give each batch subagent:

- the pinned rules from `prompts/transcribe-chat.md`;
- `prompts/transcribe-housestyle-extract.md` — the transcription-relevant house-style rulings
  (~2.6k tokens), not all of `corpus/HOUSESTYLE.md` (~9.5k), most of whose rulings concern site
  rendering; every subagent re-reads whatever you send. Do not re-derive the extract per run, and
  do not paraphrase it into the prompt — send the file;
- the work's `corpus/<work-id>/notation.md` if it exists, and an instruction to follow it;
- the **previous batch's trailing ~15 lines**, so text spanning the batch boundary joins correctly;
- the paths of its own prepared page images, and nothing else;
- the raw scans for those pages plus their `zoom-map.json` rows, for magnification only;
- a scratch directory it may write magnified crops into, **capped at 3 regions per page**.

**Budget the magnification honestly.** It is the escalation that buys back the resolution one image
per page gives up (Phase 2), and it is also where the turns go: two measured batches spent 7 and 8
crops on 4 pages each, pushing them to 22 and 27 tool calls against the 14 of a batch that made
none. That roughly doubles the per-page cost, so it is worth it only where a reading is genuinely
in doubt. Say so in the batch prompt.

Instruct each subagent to:

- write one fragment per page to `corpus/<work-id>/pages/p<N>.tex`, starting with `\origpage{N}`
  (the printed page number) and containing body LaTeX only;
- transcribe faithfully — keep the author's spelling, symbols, and notation (`zz` for z², archaic
  spelling, `arc.`); normalize typography only (Fraktur/long-ſ → normal letters, expand ligatures,
  drop line-break hyphenation);
- **magnify rather than guess, and flag rather than magnify indefinitely**: where a glyph is
  doubtful, crop and enlarge that region; if that does not settle it, mark `\uncertain{...}`, or
  `\illegible` for unrecoverable text. These are honest signals for the reviewer;
- emit `\rmfigure{figures/fig-XX.png}{<figure number only>}{<alt text>}` for a figure — never
  redraw it. The crop is added separately;
- reproduce apparent printer's errors faithfully and report them (ruling R4); never silently "fix"
  the author;
- not transcribe running heads, page numbers, or signature lines.

Require a report back with exactly these sections, and nothing else — the report is what enters
**your** context, so it must stay small:

1. **PAGES WRITTEN**
2. **FLAGS** — count of `\uncertain{}` and `\illegible` per page
3. **NOTATION DECISIONS** — decisions that must hold across the rest of the work, one line each
   with a rationale; "none" if none
4. **TRAILING LINES** — the last ~15 lines of the final fragment, verbatim
5. **DIFFICULTIES** — anything about the scan or the mathematics that made a page hard

After each batch: append any reported decisions to `corpus/<work-id>/notation.md` (Phase 3a), run
`python pipeline/houselint.py corpus/<work-id>/pages/p<N>.tex` over the new fragments so house-style
drift is caught at the batch that caused it, and carry the trailing lines into the next batch.

### Phase 3a — Keep the notation glossary

`corpus/<work-id>/notation.md` records this work's cross-page rendering decisions. It is a
**permanent, committed artifact**, not a scratch file (corpus-format).

This matters more than it sounds. Two isolated batches of the same work, same model, same scans,
**disagreed on that work's most frequent symbol** — one wrote Clebsch's summation sign `\sum` 19
times where the rest of the work uses the Sigma letter. Given the glossary, a later batch got it
right 19 times out of 19. Batches cannot see each other; the file is how they agree.

**Write entries exactly, and say what NOT to do.** A vague entry is worse than none: an entry that
said only that spacing "is normalized" produced 11 spaced dots where the work uses 63 tight ones.
Record the decision, one line of rationale, and the forbidden alternatives. When a batch reports a
decision, write it down at that precision — do not paraphrase it.

Author back-references (`équation (92)`, `Gleichung (3)`, section numbers) are printed on the page
being transcribed and are copied verbatim. They are not glossary entries.

## Phase 4 — Stitch and normalize

- Concatenate `corpus/<work-id>/pages/p<N>.tex` **in page order** into
  `corpus/<work-id>/original.tex`, wrapped in the standard scaffold (see any existing
  `original.tex`):

  ```latex
  \documentclass{article}
  \usepackage{readmasters}
  \begin{document}
  ... your \origpage-delimited body ...
  \end{document}
  ```

- Check `\origpage` markers are contiguous with no gaps or duplicates.
- One cleanup pass: heading structure (`\section*{}` only where the source has a heading),
  paragraph breaks, macro consistency.
- **Do not re-read the whole assembled file repeatedly** — grep or sed the parts you need. It is the
  largest text object in the run and every full read of it stays in your context.

## Phase 5 — Verification pass

Verify each batch against its scans, **in a subagent, per batch** — do not rely on images being
resident, and do not read them yourself. Give each verification subagent that batch's fragments and
its prepared page images, and ask for only a discrepancy list back.

- Check every formula, equation number (`\tag{n}`), label, and `\origpage{N}` against the image.
- Resolve each discrepancy or flag it with `\uncertain{}`.
- Keep the list of flagged pages; it goes into provenance and the PR body.

### Phase 5b — Proofread the assembled text, without the scans

**Required, and cheap.** Phase 5a compares page N's text to page N's image, so it is structurally
blind to everything that spans a join or makes two parts of the work disagree — which is exactly
what a batched architecture endangers. One subagent reads the whole assembled `original.tex` plus
`notation.md` and **no images**, and returns findings only. A 130KB work is ~32k tokens: about a
twentieth of what scan-verifying the same pages costs, for whole-work coverage.

Tell it to script the mechanical checks rather than eyeball them — `\origpage` contiguity, `\tag`
sequence, `\begin`/`\end` and `\[`/`\]` pairing, `$` parity, brace balance, `notation.md`
conformance work-wide, any hyphen before a page break — and to spend its reading on:

- **every page join**, and especially the batch joins, where two agents met with no shared context;
- **a page that opens mid-sentence**, which must have *no* blank line after its `\origpage`;
- **recurring constructions** set two ways in different parts of the work;
- **the German**, for sentences that do not parse.

Require each finding classified **DEFECT** (internally broken) / **INCONSISTENCY** (two parts
disagree) / **NEEDS SCAN** (only the print settles it), and tell it not to re-report the printer's
errors provenance already documents. Give it `provenance.yaml` so it can tell the difference.

*Measured on Clebsch:* this pass found a word split across a page break that a trailing-hyphen grep
had missed (the hyphen sat behind a closing brace), six paragraph breaks inserted mid-sentence, and
four separate conventions on which one batch disagreed with the rest of the work — none of which
any per-page check, `houselint`, or `validate.py` can see.

**Verify its claims before acting on them.** It cannot see the print, so a confident-sounding
finding may be inference. One run reported that `r'^{2p}` fails to render; it renders fine in both
KaTeX and pdfLaTeX. Test the mechanical claims; send the rest back to the scan.

## Phase 6 — Write provenance

Create/update `corpus/<work-id>/provenance.yaml` (see the template and existing works):

```yaml
changelog:                    # seeds the work page's revision history
  - date: "YYYY-MM-DD"        # today
    summary: Transcription added (AI draft).
transcription:
  status: ai-draft            # machine output; a human has not yet checked it
  model: claude-opus-5        # the model you are actually running as
  effort: high                # your thinking/effort level, or null if unknown
  prompt_version: transcribe-v1   # match prompts/transcribe-chat.md
  submitted_via: skill
  produced: "YYYY-MM-DD"      # today
  verification: { flagged_pages: [...], date: "YYYY-MM-DD" }
  uncertainty_flags: N        # total \uncertain{} + \illegible; report 0 explicitly
```

Record the **total uncertainty-flag count**, and state it even when it is zero — an absence of flags
must be distinguishable from an absence of flagging. If a batch could not magnify, say so: its flag
count then reflects its tooling, not the scan.

Set `status: ai-draft` unless the contributor tells you they have reviewed it against the scan —
only then may it be `skimmed`, recorded with a `reviewers:` entry naming them.

Add the `changelog` starter entry only if one with that summary isn't already there (an existing
work being re-transcribed keeps its history); preserve any entries already present.

## Phase 7 — Validate

Both must pass before a PR:

```bash
python pipeline/validate.py
python -m pytest pipeline/tests -q
```

Fix any schema/vocab/gate errors. Vocabulary values (`discipline`, `tags`, `venue`, `type`,
`language`) must already exist in `corpus/vocab.yaml`; if a genuinely new value is needed, add it in
the same PR and say so.

`validate.py` includes the mechanical house-style linter (`pipeline/houselint.py`), which enforces
presentation rulings such as HOUSESTYLE R2. Where a work has math the site must render, check it
through the site's own KaTeX build as well — a fragment can pass `houselint` and still fail to
typeset.

## Phase 8 — Review checkpoint, then open the PR

1. **Show the contributor the result before pushing**: what was transcribed, the flagged/uncertain
   passages and their count, any notation decisions recorded, and the gate result. This checkpoint
   is required — do not skip straight to the PR.
2. Create a branch, commit with a DCO sign-off, and open the PR:

   ```bash
   git checkout -b transcribe/<work-id>
   git add corpus/<work-id>/
   git commit -s -m "Add <work-id> transcription (ai-draft)"
   gh pr create --fill
   ```

   The `-s` adds the `Signed-off-by` line the DCO requires (PLAN.md §11.1). Do not push to `main`.
3. In the PR body, state: pages covered, model + prompt_version, the flagged/uncertain pages, the
   flag count, and that the status is `ai-draft` pending human review. Link the source scan.

## Notes

- **Translations** are a separate step (`prompts/translate-chat.md`, `translate-v1`): translate
  only from our own `original.tex`, preserve every math token and `\origpage` marker, and record
  `source: transcription` in provenance.
- Keep `prompt_version` in provenance in sync with the prompt file you followed. If you deviate
  from the pinned prompt, say so in the PR rather than silently recording the old version.
- To see what a run actually cost, and what filled the context:
  `python pipeline/measure_session.py --list`, then `... <session-id> --pages N`.
