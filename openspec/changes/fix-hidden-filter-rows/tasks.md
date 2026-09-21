## 1. The fix

- [x] 1.1 Add `[hidden] { display: none !important; }` near the top of `site/src/styles/global.css`, above the layout rules
- [x] 1.2 Comment it with what it defends against — that `hidden` hides only via a user-agent rule, which any author `display` rule beats, and that three filtered lists (`.catalog .card`, `.authorlist .card`, `.journallist .jrow`) set `display: flex` for their own layout reasons

## 2. Verify on the running site

- [x] 2.1 Start the dev server and open the catalog; apply a facet and confirm the rendered card count matches the "N of M works" count
- [x] 2.2 Confirm a filtered-out card computes `display: none` (not `flex`) and that the remaining cards keep their portraits and their layout
- [x] 2.3 Repeat 2.1 at the phone breakpoint, where `.catalog .card` re-declares `display: flex` inside its media query
- [x] 2.4 Check the free-text box and the year range on the catalog, and that filtering to zero results shows the empty-state message with no cards behind it
- [x] 2.5 Check `/authors/` — type in the name/bio search box and confirm only matching cards remain, count included
- [x] 2.6 Check `/journals/` — type in the journal search box and confirm only matching rows remain, count included

## 3. Confirm nothing else regressed

- [x] 3.1 Open a work page and switch text panels; confirm the tabs still show and hide correctly (they use `hidden` on elements with no `display` rule)
- [x] 3.2 Open `/search`, switch between text and formula modes, and type a formula; confirm the mode panels and the formula preview still behave
- [x] 3.3 Run `npm test --prefix site` and confirm the existing suites still pass
- [x] 3.4 Run `npm run build --prefix site` and confirm the build and the Pagefind index still succeed

## 4. Land it

- [ ] 4.1 Commit with a DCO `Signed-off-by` line and open a pull request describing the coupling the rule fixes
- [ ] 4.2 After merge, fold the delta into `openspec/specs/site-catalog/spec.md` and archive the change
