## 1. Fix the instrument

- [x] 1.1 `measure_session.py`: per-model price table (Opus 5, Opus 5.5 at minimum), cache writes priced by TTL from `cache_creation`; price-weighted totals and shares per subagent and per session, raw volume kept as a separate labelled column.
- [x] 1.2 Reconstruct output per turn as context growth minus tool results (images at `w·h/750` from the image stored in the transcript; text at a chars-per-token estimate); last turn falls back to visible content. Report visible and thinking separately, marked as an estimate.
- [x] 1.3 Read per-turn usage from `<session>/subagents/*.jsonl` with the description from `.meta.json`; de-duplicate rows by message id, keeping the last.
- [x] 1.4 Tests: a small synthetic transcript with known output (the probe-B shape), the de-duplication, TTL pricing. Reconstructed total within 5% of known.
- [x] 1.5 Calibrate the LaTeX chars-per-token ratio from turns whose output is nearly all visible (fragment `Write`s with little reasoning); record it and use it for the visible/thinking split.
- [x] 1.6 `python -m pytest pipeline/tests -q` and `python pipeline/validate.py` pass.

## 2. Re-score what we have (no new pages)

- [x] 2.1 Picard pp. 281–300 (session `4912ad8e`) and pp. 301–346 (`50b4018c`): cost structure at Opus 5 prices and re-priced at Opus 5.5; per pass (transcribe / verify / proofread).
- [x] 2.2 Confirm which session holds Clebsch pp. 223–243 (likely `4f364d40`)
  - **Found:** Clebsch pp. 223–243 is in `edaf63a8` (with Noether work — use `--only "Clebsch pp.2"`); `4f364d40` is Betti 140–158, also re-scored. All five sessions have subagent transcripts. and castelnuovo pp. 241–316 (`f815a075`); re-score both. Say plainly if a session's subagent transcripts are missing.
- [x] 2.3 Read the Picard proofread transcript (33 turns, ~82k output, ~20% of the run): real work or a loop? Record what it spent turns on.
  - **Real work, mostly re-deriving tooling** (~25 of 33 turns built check scripts). 19% of the run at 5.5 prices. Candidate lever for 4.2.
- [x] 2.4 From 2.1–2.3, write down which term dominates across works and therefore the experiment order. If cache reads are not a minor share after all, reinstate the batch-size question here.

## 3. Measure on Opus 5.5

- [x] 3.1 Choose an untranscribed range, ~12 pages, on a work whose scan `prepare_pages.py` does not warn on. Record why it is comparable.
- [x] 3.2 Confirm how effort reaches subagents (`CLAUDE_EFFORT` / session setting); set up one session per arm accordingly.
- [x] 3.3 Build the sandbox: scans, style files, glossary only — no `original.tex`, no other arm's fragments.
- [x] 3.4 Arm M: effort `medium`, current skill. Per batch: cost (price-weighted and raw), turns, output split, magnified regions.
- [x] 3.5 Arm L: effort `low`, same pages, same skill, same records.
- [x] 3.6 Diff M against L; adjudicate every difference against the scan. Byte-identical output is a failed measurement. Judge transcription and verification separately against the kill criterion (design D4).
- [x] 3.7 **Not run — condition not met** (images are 5–12% of cost; see measurements, Experiment order). Only if 2.4 found image writes material: resolution arm at `prepare_pages.py --max-edge 2000` against 1568, at the effort 3.6 selected. Record magnified regions per page.

## 4. Decide

- [x] 4.1 Write all results to `measurements.md`: per-batch figures, not just means, and whether each difference exceeds batch-to-batch spread.
- [x] 4.2 List the levers that earn a skill change, with their measured saving and quality outcome — or record that none do.
- [x] 4.3 Update the `transcribe-token-cost` memory with the price-weighted numbers.
- [x] 4.4 *One PR with `transcribe-turn-cost` and `transcribe-skill-rebaseline`, at the contributor's request.* Show the contributor the summary; open the PR (DCO sign-off); sync the spec delta and archive.
