# Spec (delta): site-catalog

## MODIFIED: Work page

Adds panel identity and indexing markup to the existing work-page requirement:

Each text panel (the original and each translation) has a stable id and a visually-hidden heading
naming it, and the tabs read and write `location.hash` — so `/works/<id>/#en` opens the English
translation directly and a link to a panel survives being shared. Page markers (`\origpage`) are
unique per panel: the original uses `p-<n>`, a translation uses `<lang>-p-<n>`.

The reader section is marked `data-pagefind-body` so the search index (see the `search` capability)
covers the texts and nothing else on the page; math spans within it are marked
`data-pagefind-ignore`.
