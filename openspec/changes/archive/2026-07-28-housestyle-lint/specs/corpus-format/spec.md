# Delta: corpus-format — mechanical house-style enforcement

## MODIFIED: LaTeX house style

Extends the house-style requirement: presentation conventions that are unambiguous from the source
text are now **mechanically enforced**, not merely documented.

`pipeline/houselint.py` (stdlib-only, a rule registry) checks each work's `original.tex` and every
`translations/*.tex`. `pipeline/validate.py` runs it as part of the gate, so a violation fails CI and
cannot merge. Display math (`\[ … \]`, math environments, `$$…$$`) is never flagged — only inline
`$…$` spans. The linter enforces only rulings that are unambiguous from the text; judgement-based
rulings (faithful vs. normalized notation, translation wording) are never linted.

Currently enforced:

- **R2** — an inline integral whose integrand is a fraction must be set with `\displaystyle` and use
  `\frac` (not the redundant `\dfrac`): `$\displaystyle\int \frac{...}{...}$`. A lone inline `\int`
  without a fraction integrand is out of scope.

#### Scenario: An inline integral over a fraction lacks \displaystyle

- **WHEN** a `.tex` in a work contains an inline span `$\int \dfrac{dx}{\sqrt{1-x^{4}}}$`
- **THEN** `houselint` reports an R2 violation (naming the file and line)
- **AND** `validate.py` fails, so the work does not pass the gate

#### Scenario: The house-style-correct form passes

- **WHEN** the same integral is written `$\displaystyle\int \frac{dx}{\sqrt{1-x^{4}}}$`
- **THEN** `houselint` reports no violation and the gate passes

#### Scenario: Display math and lone integrals are not flagged

- **WHEN** an integral appears in display math (`\[ … \int \frac{…}{…} … \]`), or an inline `\int`
  has no fraction integrand (`$\int dx\,\sqrt{1+x^{4}}$`)
- **THEN** `houselint` reports no violation
