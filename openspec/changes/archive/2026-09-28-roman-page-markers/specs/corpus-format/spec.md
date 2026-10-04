## ADDED Requirements

### Requirement: Roman page markers

An `\origpage{…}` marker SHALL accept either an arabic page number (`\origpage{12}`) or a
lower-case roman numeral (`\origpage{iii}`), copied as the page is printed. A roman marker MUST
render in the reader as `page iii` with the anchor `p-iii` (`<lang>-p-iii` in a translation
panel), MUST be kept as printed by the formula index and the search page, and MUST pass the gate on
the same terms as an arabic marker. Roman markers MUST all precede the first arabic marker; within
the roman run and within the arabic run, markers MUST ascend without duplicates, and a skipped page
is a warning, not an error.

#### Scenario: A roman marker renders as a page anchor

- **WHEN** a transcription contains `\origpage{iii}`
- **THEN** the reader shows `page iii` with the anchor `p-iii`, not the literal macro

#### Scenario: A formula on a roman page is indexed under that page

- **WHEN** a formula follows `\origpage{vii}` and precedes the next marker
- **THEN** the formula index records its page as `vii` and links it to `#p-vii`

#### Scenario: Front matter followed by the text passes the gate

- **WHEN** a work's markers run `iii, iv, v, vi, vii, viii, 1, 2, …, 82`
- **THEN** the page-marker check reports no error

#### Scenario: A roman marker after the arabic run fails the gate

- **WHEN** a work's markers run `1, 2, iii`
- **THEN** the page-marker check reports an ordering error

#### Scenario: A duplicated roman marker fails the gate

- **WHEN** a work's markers contain `\origpage{iv}` twice
- **THEN** the page-marker check reports a duplicate
