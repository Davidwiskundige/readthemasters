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

- [ ] 3.1 Rewrite `SKILL.md` Phase 2 to call `pipeline/prepare_pages.py` and state that prepared pages live outside the corpus
- [ ] 3.2 Rewrite Phase 3 as the batch loop: **default batch of 4** (measured optimum is N=2–4; the curve is flat there and 4 keeps adjacent pages comparable), one subagent per batch, fragments written to `corpus/<work-id>/pages/pNNN.tex`
- [ ] 3.2a Keep the per-page turn count at 2 (one `Read` of one text-block crop, one `Write`) — `t·(B+P)` is ~75% of the cost, so a third turn per page costs more than any batch-size choice
- [ ] 3.2b Give the batch subagent a scratch directory it may write magnified crops into, so `\uncertain{}` reflects legibility rather than missing tooling — **capped at 3 regions per page** (an ungoverned run made 32 crops for 4 pages), with magnification preferred over guessing and `\uncertain{}` preferred over both when it does not settle the reading
- [ ] 3.2c Pass a transcription-relevant extract of `HOUSESTYLE.md` (~4k tokens) rather than all 36KB, since every subagent re-reads the whole payload
- [ ] 3.3 Write the subagent prompt template: pinned `prompts/transcribe-chat.md` rules, applicable `corpus/HOUSESTYLE.md` rulings, the work's `notation.md`, the previous batch's trailing ~15 lines, and the batch's image paths
- [ ] 3.4 Fix the batch report contract: pages written, uncertainty-flag count, new notation decisions, trailing lines of the final fragment — and nothing else, so the report stays small
- [ ] 3.5 State explicitly that the orchestrating session never calls `Read` on a scan image, and that Phases 4 and 6–8 run with no images in context
- [ ] 3.6 Add the short-work escape hatch: below ~2 batches, transcribe inline
- [ ] 3.7 Rewrite Phase 4 to stitch `pages/pNNN.tex` in page order into `original.tex`, and to grep/sed that file rather than re-reading it whole
- [ ] 3.8 Rewrite Phase 5 as per-batch verification subagents returning only a discrepancy list
- [ ] 3.9 Run `pipeline/houselint.py` over each batch's fragments as they land, not only over the assembled file

## 4. Notation glossary and flag visibility

- [ ] 4.1 Define the `corpus/<work-id>/notation.md` format — decision plus one-line rationale — and document it in `SKILL.md`
- [ ] 4.2 Have the orchestrating session create/append the glossary from batch reports, and pass it into every subsequent batch
- [ ] 4.3 Confirm `pipeline/validate.py` tolerates `notation.md` and does not require it; add a test for a work with and without one
- [ ] 4.4 Add a `corpus/HOUSESTYLE.md` ruling recording the glossary convention and why cross-page decisions are written down rather than remembered
- [ ] 4.5 Carry the uncertainty-flag count through batch report → `provenance.yaml` → the Phase 8 checkpoint, reporting an explicit zero when there are none
- [ ] 4.6 Strengthen the `\uncertain{}` / `\illegible` instruction in the subagent prompt — 151 transcribed pages currently carry zero flags between them

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

- [ ] 5.1 Build an isolated sandbox: copies of `prompts/transcribe-chat.md`, the HOUSESTYLE extract and the work's `notation.md`, plus the batch's page images and a scratch dir for zoom crops, and nothing else; the subagent prompt forbids reading any other path and requires it to declare every path it read
- [ ] 5.2 Re-transcribe a sample of Clebsch pages 189–206 into the sandbox output directory, leaving the committed `original.tex` untouched
- [ ] 5.3 **Contamination tripwire**: byte-identical output against the committed text fails the measurement — never record it as agreement; re-run with tighter isolation
- [ ] 5.4 Diff the sample against the committed text; classify each divergence as substantive (wording, formula, notation) or markup-only, and collapse the substantive ones into the distinct *decisions* behind them
- [ ] 5.5 Run `pipeline/houselint.py` over both versions and compare violation counts
- [ ] 5.6 **Adjudicate each substantive decision against the scan** — contributor, or a verification subagent reading the page images. The diff cannot say which side is right: both versions descend from an `ai-draft` baseline that no human has checked
- [ ] 5.7 Record every adjudicated decision in the work's `notation.md`, at the precision the corrected entry uses — say what not to do, not just what to do (a vague entry licenses a fresh divergence: see design, Resolved)
- [ ] 5.8 Record measured tokens/page for the sample against the 4.2M baseline from task 1.1
- [ ] 5.9 Rollout proceeds when every substantive decision has been adjudicated and recorded; markup-only divergence does not block. An unadjudicated substantive divergence sends the design back to group 3

## 6. First real use and close-out

- [ ] 6.1 On a clean A/B, transcribe Clebsch pages 207–243 with the new loop
- [ ] 6.2 Record the measured tokens/page and mean context for that run, and adjust the default batch size if the observed subagent baseline differs materially from the ~35k estimate
- [ ] 6.3 Run `python pipeline/validate.py` and `python -m pytest pipeline/tests -q`
- [ ] 6.4 Review checkpoint, then a DCO-signed PR for the Clebsch completion
- [ ] 6.5 Fold the delta spec into `openspec/specs/transcription-pipeline/spec.md` and archive the change
- [ ] 6.6 Note in the archived change whether the two design open questions were resolved: A/B acceptance criteria, and whether `notation.md` is a permanent corpus artifact
