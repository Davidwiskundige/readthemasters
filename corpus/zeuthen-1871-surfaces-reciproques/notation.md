# Notation decisions — Zeuthen (1871), Note sur la théorie de surfaces réciproques

Permanent record of notation and typographic decisions for this work (HOUSESTYLE R27).

## Mathematics and symbols

- **Summation sign**: The capital Greek letter `\Sigma` is used as an algebraic sum/operator symbol (e.g. `\Sigma [2\mu + v]`, `\Sigma(\cdots)`), following Clebsch, Salmon, and Zeuthen's convention in the *Annalen*.
  - **Rule**: Write `\Sigma`, `\Sigma'`.
  - **Forbidden**: `\sum`.

- **Greek vs Latin letters for surface singularities**:
  - `\chi`, `\chi'`: Close-points (*points-clos*) and close-planes (*plans-clos*), following Cayley's notation.
    - **Rule**: Write `\chi`, `\chi'`.
    - **Forbidden**: Latin `x`, `x'`.
  - `\eta`, `\eta'`: Singularities related to binodes and biplanes.
    - **Rule**: Write `\eta`, `\eta'`.
    - **Forbidden**: Latin `n`, Greek `\beta`.
  - `\xi`, `\xi'`: Singularities of definition ponctuelle / tangentielle.
    - **Rule**: Write `\xi`, `\xi'`.
    - **Forbidden**: Greek `\zeta`.
  - `\varrho`, `\varrho'`: Class of the developable tangent along the double curve.
    - **Rule**: Write `\varrho`, `\varrho'`.
    - **Forbidden**: Latin `p`.
  - `\gamma`, `\gamma'`: Stationary / cuspidal points of the double curve.
    - **Rule**: Write `\gamma`, `\gamma'`.
    - **Forbidden**: Latin `y`, `y'`.
  - `\mu`, `\mu'`: Multiplicity of conical points ($\mu$-tuples).
    - **Rule**: Write `\mu`, `\mu'`.
  - `$v$`, `$v'$`: Number associated with contact order in `\Sigma [2\mu + v]`.
    - **Rule**: Write Latin italic `$v$`, `$v'$`.
    - **Forbidden**: Greek `\nu`.

- **Multiplication dot**:
  - The coefficient product in the formula on p. 637 is set with an explicit centered dot: `A \cdot \chi`, `A \cdot \chi'`.
  - **Rule**: Write `A \cdot \chi`, `A \cdot \chi'`.
  - **Forbidden**: Juxtaposition without dot `A\chi` or `A \times \chi`.

## Typography and prose

- **Quotations**: The German publisher (B. G. Teubner) sets German-style low-high quotation marks `„..."` around citations and titles (e.g. `„Annalen“`, `„binodes“`, `„biplans“`).
  - **Rule**: Preserve the edition's own quotation marks as literal Unicode `„..."` (HOUSESTYLE R22).
  - **Forbidden**: English double quotes `"..."` or French guillemets `«...»`.

- **Ordinals**: French abbreviations for ordinals use superscript `me`:
  - **Rule**: Write `$4^{\text{me}}$`, `$26^{\text{me}}$`, `$3^{\text{me}}$` (using `\text{me}` per HOUSESTYLE R21 so that translation to English `$4^{\text{th}}$`, `$26^{\text{th}}$`, `$3^{\text{rd}}$` preserves mathematical structure in `texcompare.py`).

- **Emphasis**: Italicized words in running text are transcribed as `\emph{...}` (HOUSESTYLE R20).

- **Footnotes**: The original print uses asterisks `*)` for footnotes.
  - **Rule**: Place footnotes inline at the foot of their respective page using in-text callout `${}^{*)}$` and paragraph lead `\textbf{*)}` (HOUSESTYLE R15).
