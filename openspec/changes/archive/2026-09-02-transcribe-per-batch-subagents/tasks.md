## 1. Baseline measurement

- [x] 1.1 Record the pre-change baseline for `clebsch-1864-anwendung-abelschen-functionen` pages 189–206 in the change folder: 347 turns, 76M tokens, 4.2M tokens/page, 220k mean context — the figure the A/B in group 5 is measured against → `measurements.md`
- [x] 1.2 Write a small throwaway script that reads a session transcript's `usage` fields and reports turns, mean/peak context, total tokens, and tokens/page, so the post-change run can be measured the same way → `pipeline/measure_session.py`; reproduces the baseline exactly, and adds the residency breakdown that identifies *what* filled the context

## 2. Text-block crop helper

- [x] 2.1 Add `pipeline/prepare_pages.py`: given a scan directory and a page range, emit one image per page cropped to the printed text block, long edge ≤ 1568px, named by printed page number → measured 2,375 tokens/page over Clebsch pp. 207–214
- [x] 2.2 Detect the text block from margin whitespace; expose `--margin`, `--max-edge`, and `--no-crop` overrides for pages the detector gets wrong
- [x] 2.3 Emit a per-page report line (source dimensions, crop box, output dimensions, estimated image tokens) so figure-crop iterations can be settled without a visual check
- [x] 2.4 Exit non-zero only on unreadable input; a page whose text block cannot be determined is reported and passed through uncropped, never fatal
- [x] 2.5 Add `pipeline/tests/test_prepare_pages.py` covering the pure helpers (crop-box computation, scaling, page-number resolution) with no image-library dependency in the test path — 20 tests, including one pinning the portrait-page resolution trade
- [x] 2.6 Confirm `pipeline/validate.py` and the CI suite import neither the helper, Pillow, nor `anthropic` — assert it in the existing dependency test
- [x] 2.7 Add `pipeline/tests/test_measure_session.py` for `measure_session.py`'s pure helpers (image dimensions/tokens, residency, project slug), and assert the gate does not import it — 13 tests; suite now 178 passing (was 145)
- [x] 2.8 Document Pillow in `pipeline/requirements.txt` as a contributor-only, lazily-imported dependency, alongside `anthropic`

## 3. Skill rewrite

- [x] 3.1 Rewrite `SKILL.md` Phase 2 to call `pipeline/prepare_pages.py` and state that prepared pages live outside the corpus — also states the portrait-page resolution trade explicitly
- [x] 3.2 Rewrite Phase 3 as the batch loop: **default batch of 4** (measured optimum is N=2–4; the curve is flat there and 4 keeps adjacent pages comparable), one subagent per batch, fragments written to `corpus/<work-id>/pages/pNNN.tex`
- [x] 3.2a Keep the per-page turn count at 2 (one `Read` of one text-block crop, one `Write`) — `t·(B+P)` is ~75% of the cost, so a third turn per page costs more than any batch-size choice
- [x] 3.2b Give the batch subagent a scratch directory it may write magnified crops into, so `\uncertain{}` reflects legibility rather than missing tooling — **capped at 3 regions per page** (an ungoverned run made 32 crops for 4 pages), with magnification preferred over guessing and `\uncertain{}` preferred over both when it does not settle the reading
- [x] 3.2c Pass a transcription-relevant extract of `HOUSESTYLE.md` (~4k tokens) rather than all 36KB, since every subagent re-reads the whole payload
- [x] 3.3 Write the subagent prompt template: pinned `prompts/transcribe-chat.md` rules, applicable `corpus/HOUSESTYLE.md` rulings, the work's `notation.md`, the previous batch's trailing ~15 lines, and the batch's image paths
- [x] 3.4 Fix the batch report contract: pages written, uncertainty-flag count, new notation decisions, trailing lines of the final fragment — and nothing else, so the report stays small
- [x] 3.5 State explicitly that the orchestrating session never calls `Read` on a scan image, and that Phases 4 and 6–8 run with no images in context — made non-negotiable #5, with the cost consequence named
- [x] 3.6 Add the short-work escape hatch: below ~2 batches, transcribe inline
- [x] 3.7 Rewrite Phase 4 to stitch `pages/pNNN.tex` in page order into `original.tex`, and to grep/sed that file rather than re-reading it whole
- [x] 3.8 Rewrite Phase 5 as per-batch verification subagents returning only a discrepancy list
- [x] 3.9 Run `pipeline/houselint.py` over each batch's fragments as they land, not only over the assembled file

## 4. Notation glossary and flag visibility

- [x] 4.1 Define the `corpus/<work-id>/notation.md` format — decision plus one-line rationale — and document it in `SKILL.md` → Phase 3a
- [x] 4.2 Have the orchestrating session create/append the glossary from batch reports, and pass it into every subsequent batch
- [x] 4.3 Confirm `pipeline/validate.py` tolerates `notation.md` and does not require it; add a test for a work with and without one → `pipeline/tests/test_notation_glossary.py` (4 tests; the gate looks for named files rather than whitelisting, so the glossary is simply ignored)
- [x] 4.4 Add a `corpus/HOUSESTYLE.md` ruling recording the glossary convention and why cross-page decisions are written down rather than remembered → **R27**, including the "say what NOT to do" rule the measurement forced
- [x] 4.5 Carry the uncertainty-flag count through batch report → `provenance.yaml` → the Phase 8 checkpoint, reporting an explicit zero when there are none → new `uncertainty_flags` field
- [x] 4.6 Strengthen the `\uncertain{}` / `\illegible` instruction in the subagent prompt — 151 transcribed pages currently carry zero flags between them → framed as "magnify rather than guess, flag rather than magnify indefinitely", since the observed failure was resolving ambiguity silently rather than ignoring the instruction

## 5. A/B quality check (gates the rollout)

**Isolation is mandatory.** A first attempt at this measurement (2026-08-31) was run with the repo
visible to the batch subagent, which read `corpus/clebsch-.../original.tex` and reproduced it
**byte-for-byte** across four pages — a 1.000 similarity score that looked like validation and was
contamination. Any A/B on already-transcribed pages must isolate the agent from the committed text.

**The mechanical checks are a sampler, not a gate.** `houselint` passed 16/16 fragments that
contained a real notation error, and the contaminated run scored a perfect 1.000 diff. Both compare
the new text to an `ai-draft` baseline, never to the scan. So 5.4–5.5 exist to narrow the sample to
its decision points; 5.6 is what actually decides. Expect far fewer decisions than divergences —
across 18 pages, two batches produced 25 divergent spots but only two decisions to settle.

- [x] 5.1 Build an isolated sandbox: copies of `prompts/transcribe-chat.md`, the HOUSESTYLE extract and the work's `notation.md`, plus the batch's page images and a scratch dir for zoom crops, and nothing else; the subagent prompt forbids reading any other path and requires it to declare every path it read — **isolation held**: every agent declared a repo-free path list, and `git status` independently confirmed no subagent touched the repository. Note that Claude Code offers no *mechanical* path restriction, so the prompt plus the 5.3 tripwire are the whole control; that limitation is now stated in the design
- [x] 5.2 Re-transcribe a sample of Clebsch pages 189–206 into the sandbox output directory, leaving the committed `original.tex` untouched — pp. 189–196, 8 of 18 pages, two batches of 4
- [x] 5.3 **Contamination tripwire**: byte-identical output against the committed text fails the measurement — **passed**; nothing byte-identical, and similarity tracked math density (0.9993 on the prose-only p. 189 against 0.9383 on the formula-dense p. 191) rather than being uniformly near-perfect, which is the signature that distinguishes independent work from copying
- [x] 5.4 Diff the sample against the committed text; classify each divergence — **66 divergent spans across 8 pages, collapsing to 8 distinct decisions** (the design predicted far fewer decisions than divergences; the ratio was 8:1)
- [x] 5.5 Run `pipeline/houselint.py` over both versions and compare violation counts — **0 and 0**, while the baseline carried two page-break bugs and nine R15/R17 violations and the new version carried 28 flattened nested fractions. The linter's blindness is now measured twice over, not asserted
- [x] 5.6 **Adjudicate each substantive decision against the scan** — an isolated adjudication subagent settled all four scan-dependent decisions with pixel measurements; the other four were settled by HOUSESTYLE/corpus convention
- [x] 5.7 Record every adjudicated decision in the work's `notation.md`, at the precision the corrected entry uses — all 8 recorded with the forbidden alternative named. **The glossary then proved itself**: the batch transcribing pp. 231–234 under the corrected nested-fraction entry got the analogous case right
- [x] 5.8 Record measured tokens/page for the sample against the 4.2M baseline → `measurements.md`
- [x] 5.9 Rollout proceeds when every substantive decision has been adjudicated and recorded — **proceeds.** The new architecture did not win uniformly: it lost the nested-fraction decision on ~28 spans. But the loss was a missing glossary entry rather than a reading failure, and the glossary repaired it, which is exactly the mechanism D2 predicts

## 6. First real use and close-out

- [x] 6.1 On a clean A/B, transcribe Clebsch pages **223–243** with the new loop (207–222 were already committed) — 21 pages in five batches; the work is now complete at 55/55 pages, contiguous, houselint-clean, and all 1383 math spans render through the site's KaTeX 0.16.47 build
- [x] 6.2 Record the measured tokens/page and mean context for that run → `measurements.md`. **Batch size needs no change** — per-page cost was flat across the five batches (426k–613k with no drift), which is the property the change exists to buy. **But the headline projection was wrong**: measured 509k/page for transcription (8.3× the 4.2M baseline), not the 149–170k (20–28×) D5 forecast, because `t` is 5.7 turns/page rather than the assumed 2. See 6.7
- [x] 6.3 Run `python pipeline/validate.py` and `python -m pytest pipeline/tests -q` — gate passes on 13 works; 185 tests pass (was 182; +3 for the new `zoom_mapping` helper)
- [x] 6.4 Review checkpoint, then a DCO-signed PR for the Clebsch completion — **done, after the archive**, on the contributor's explicit go-ahead. No new PR was opened: the Clebsch completion went to `transcribe/clebsch-1864-pages-207-222` → **PR #42** (corpus only), and everything else to `impl/transcribe-per-batch-subagents` → **PR #41**. Both PR titles and bodies were rewritten, because both had gone stale and actively misled — #42 still said "pp. 189-222" for what is now the complete 55-page paper, and #41 still said "28/43 — do not merge". CI on both: copyright gate + tests **pass**, DCO sign-off **pass**. Each body states pages covered, model and `prompt_version`, the flagged pages and flag count, `ai-draft` status, and the source scan, per Phase 8
- [x] 6.5 Fold the delta spec into `openspec/specs/transcription-pipeline/spec.md` and archive the change — **the delta specs were first brought in line with what actually shipped**, which they did not describe: the text-only proofread (Phase 5b), the page-marker gate check, the maintained HOUSESTYLE extract, and the prepared-page coordinate mapping. Also resolved a contradiction between the two delta specs: `transcription-pipeline` had fragments written to `corpus/<work-id>/pages/pNNN.tex`, but `corpus-format`'s work-directory layout does not list `pages/`, so committing them would violate it. Fragments are now specified as working files outside the corpus, like the prepared images; `SKILL.md` updated to match
- [x] 6.6 Note whether the two design open questions were resolved — **both resolved, and both by running the thing rather than by argument:**
  - *A/B acceptance criteria.* Settled as: mechanical checks (diff + `houselint`) are a **sampler, not a gate**; they narrow the sample to its decision points, and each substantive decision is then **adjudicated against the scan**. Byte-identical output fails as contamination rather than passing as agreement. This was forced by evidence — `houselint` passed 16/16 fragments carrying a real notation error, and a contaminated run scored a perfect 1.000 similarity. In the real A/B, 66 divergent spans over 8 pages collapsed to **8 decisions**, of which the new architecture won 5, tied 2, and **lost 1**
  - *Is `notation.md` a permanent corpus artifact?* **Yes**, and it earned it: 11 decisions carried across 5 batches that could not see each other, with the glossary demonstrably repairing the one decision the new loop lost. `corpus-format`'s layout now lists it. One caveat the run added: an entry must be **exact and testable** — I wrote one asserting KaTeX rejects `r'^{2p}`, which is false, and a later pass duly "found" three broken spans on its authority. A rule with a fabricated rationale is worse than no rule

## 7. Corrections the run forced (added 2026-09-01)

Recorded here rather than silently applied, because each contradicts something the design or the
tasks asserted.

- [x] 7.1 **D5's "one Read plus one Write per page" is false on a doubtful scan.** Batches magnified 36 regions across 21 pages — escalating on nearly every page, not the 25–50% D5 forecast — and that is what put per-page cost at 509k rather than ~150k. The escalation is not waste (it settled four misprints and kept 21 pages down to one `\uncertain{}`), so the honest correction is to the *forecast*, not the behaviour. `SKILL.md` now states the turn cost of a crop explicitly
- [x] 7.2 **D4's verification pass is not cheap.** "The images are read twice, which is cheap precisely because neither read persists" is true about residency and wrong about cost: verification ran 4.9 turns/page, ~508k/page — as expensive as transcription. Budget it as a second pass, not a rounding error
- [x] 7.3 **Ship the HOUSESTYLE extract as a file, not a per-run derivation.** Task 3.2c specified a ~4k-token extract but no file existed, so every run would have re-derived it from the 37KB source at ~9.5k tokens of orchestrator context. Added `prompts/transcribe-housestyle-extract.md` (2.6k tokens) and pointed `SKILL.md` at it
- [x] 7.4 **Ship the crop-coordinate mapping.** A subagent that had to infer the prepared→raw mapping landed 2 of its 3 magnification crops on the wrong lines and burned its whole per-page budget settling nothing. `prepare_pages.py` now emits `zoom-map.json`; the next batch, given it, hit every crop. New `zoom_mapping` helper with 3 tests
- [x] 7.5 **Fragments were written outside the corpus, not to `corpus/<work-id>/pages/`.** The transcription-pipeline delta spec names that path, but `corpus-format`'s amended work-directory layout does not list `pages/`, so committing it would violate the layout and leaving it untracked would litter the work directory. The two delta specs contradict each other; 6.5 must reconcile them, and the working-directory reading matches Phase 2's existing rule that prepared pages live outside the corpus
- [x] 7.6 **A glossary entry can be over-specific as well as vague.** R27 warns that a vague entry licenses a divergence. The mirror image also bit: an entry pinning continuation rows at "nine `\cdot`s" was wrong for a print that sets 7, 10, 11, 12, 13 and 15 in different rows. Corrected to "count what the print sets", with the measured counts listed
- [x] 7.7 Verification of pp. 233–243 completed on the third attempt (the subagent was cut off twice by transport errors, and resumed from its own transcript rather than restarted). All of pp. 223–243 are now verified against the scans by a subagent that read no repository file
- [x] 7.8 **Previewing the work found a rendering bug the whole toolchain passed** — a text-mode `\ldots` between two formulas (`$x_{1}$, $x_{2}$ \ldots $x_{r}$`) belongs to the prose, never reaches KaTeX, and leaked to the reader as literal `\ldots`. Pre-existing in **four works**, 33 occurrences, and `validate.py` / `texcompare.py` / `houselint.py` all passed it. Fixed in `tex.js` per the R14/R17/R19/R25 precedent of extending the site rather than bending the work, with 2 tests (site suite 27→29) and recorded as **R28**. Verified in the browser: 26 ellipses now render on the Clebsch page and **0 literal macros leak into prose** (the 136 remaining are inside math spans awaiting lazy typesetting, which is correct)
- [x] 7.9 A verification subagent raised, and this closed out, whether `\emph{}` runs containing `$...$` leak their tail the way `\ednote`/`\uncertain` do (R18). **They do not** — `tex.js` stashes math *before* the `\emph` regex, so the brace-carrying math is a brace-free placeholder by then. Checked against all 44 real occurrences in the assembled file: every `<em>` balanced, no brace or macro in the prose. Not a corpus-wide problem
