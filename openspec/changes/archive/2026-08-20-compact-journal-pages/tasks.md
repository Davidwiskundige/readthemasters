## 1. Journal index — title-led rows

- [x] 1.1 In `site/src/pages/journals/index.astro`, replace the `.card` list items with compact title-led rows: each row is `j.name` linking to `j.url`, and drop the era and place meta from the index.
- [x] 1.2 Show the work count only when `j.work_count > 0` (as a positive marker); render no count for zero-work venues. Keep alphabetical order and the sentinel exclusion unchanged.
- [x] 1.3 Keep the search box, `#jcount` "X of Y" line, and the filter script working against the new rows (update selectors/`data-search` if the markup changed).

## 2. Pipeline — emit the fields the dropdowns need

- [x] 2.1 In `pipeline/build_site_data.py`, add `month` to the flat work dict, and carry `title_en`, `title_en_tex`, `volume`, and `month` into each journal work in `build_journals`.

## 3. Journal detail — eudml-style volume/issue dropdowns

- [x] 3.1 In `site/src/pages/journals/[slug].astro`, group works into collapsible `<details>` sections: one per `volume` when a work records one, otherwise one per dated issue (`month` + `year`); sort sections chronologically (year → volume → month).
- [x] 3.2 The collapsed `<summary>` shows the label — `Volume {n} ({year})`, or `{month} ({year})` for month-cited journals like Acta Eruditorum (falling back to `{year}` when no month) — plus a work count. Sections are open by default (the reader can collapse any).
- [x] 3.3 Each expanded work row shows the title (→ work page), its English translation (`title_en_tex`/`title_en`) when present, author, `venue_full`, status badge, and scan link.
- [x] 3.4 Retarget the `renderMathInElement` KaTeX pass at the `.jvols` container so both title and translation math render.

## 4. Journal detail — empty state as invitation

- [x] 4.1 When a journal has zero works, promote the "Find the originals" block and replace the "No works from this journal yet" message with a single quiet line inviting the reader to help revive the journal, linking to `/contribute/`.
- [x] 4.2 Ensure the empty state still renders the metadata header and archive links (behavior already present) and reads coherently without a works section.

## 5. Contribute page referral

- [x] 5.1 In `site/src/pages/contribute.md`, add a referral in Step 1 (transcribing bullet) pointing readers to `/journals/` as the place to discover originals worth reviving.

## 6. Styles

- [x] 6.1 In `site/src/styles/global.css`, add the compact index-row styles and the `.jvols`/`.jvol` dropdown styles (native `<details>`, ▸/▾ marker, label + count summary, muted italic translation line), without regressing other pages that share `.card`/`.authorlist`.

## 7. Verify

- [x] 7.1 Build the site and verify in the preview: the title-led index (non-zero counts only, no era); a populated detail page (Acta Eruditorum) with collapsible `April (1689)` / `June (1694)` / `September (1694)` dropdowns that expand to the works and their English translations; and an empty journal showing promoted archives + the quiet revive line.
- [x] 7.2 Confirm the dropdowns toggle (▸/▾), KaTeX titles/translations render, no console/build errors, and no horizontal overflow at mobile width.

## 8. Sync spec

- [x] 8.1 On completion, fold `specs/site-catalog/spec.md` from this change into `openspec/specs/site-catalog/spec.md` and archive the change (per the in-sync workflow).
