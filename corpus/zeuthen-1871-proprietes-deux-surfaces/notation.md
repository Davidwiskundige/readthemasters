# Notation Decisions for Zeuthen (1871): Études géométriques de deux surfaces

## Overview
Hieronymus Georg Zeuthen's 1871 memoir establishes the geometric theory of birational (one-to-one) correspondences between algebraic surfaces, introducing what is now known as the Zeuthen–Segre invariant. The text uses classical French algebraic geometry notation following Cayley, Salmon, Clebsch, and Noether.

---

## Explicit Notation Rules

### 1. Surfaces in Square Brackets
- **Rule**: Surfaces are denoted by letters enclosed in square brackets: `$[F_1]$`, `$[F_2]$`, `$[F_3]$`, `$[F_4]$`.
- **Rationale**: This is Zeuthen's explicit notation to distinguish surfaces from curves and numbers.
- **Forbidden**: Do not strip brackets (e.g., `$F_1$`) or replace with parentheses (`$(F_1)$`).

### 2. Curves and Lines in Parentheses
- **Rule**: Curves and straight lines are enclosed in parentheses: `$(B_1)$`, `$(B_2)$`, `$(B_{1, 2})$`, `$(C_1)$`, `$(C_{1, 2})$`, `$(S_1)$`, `$(L)$`, `$(P_{1, 2} P'_{1, 2})$`, `$(M_3)$`.
- **Rationale**: Distinguishes curves/lines from surfaces `$[F_i]$` and point sets.
- **Forbidden**: Do not alter to bare letters or square brackets.

### 3. Double Indices for Correspondences
- **Rule**: For curves and characters on one surface corresponding to singularities on the other, use comma-separated subscripts: `$b_{1, 2}$`, `$b_{2, 1}$`, `$c_{1, 2}$`, `$c_{2, 1}$`, `$\mu_{1, 2}$`, `$\mu_{2, 1}$`, `$P_{1, 2}$`, `$P'_{1, 2}$`.
- **Rationale**: The first index indicates the surface of origin or role, and the second indicates the related surface.

### 4. Summation Operator: Capital Greek Sigma
- **Rule**: Discrete summations over singular points or fundamental points are set as `\Sigma`, not `\sum`.
  - Example: `\Sigma [\mu_{1, 2}(\mu_1 - 2)]`, `\Sigma(\mu)`, `\Sigma'(\mu')`.
  - Reciprocal summation: `\Sigma'`.
- **Rationale**: Zeuthen, following Clebsch and Noether, uses capital Greek $\Sigma$ as a discrete sum symbol.
- **Forbidden**: Never modernize to `\sum`.

### 5. Overbars and Primes
- **Rule**: Overbars designate auxiliary or reduced quantities: `$\bar{n}'$`, `$\bar{n}$`, `$\bar{t}$`, `$\bar{\beta}'$`. Primes denote dual/reciprocal characters or second points: `$n'$`, `$c'$`, `$r'$`, `$b'$`, `$k'$`, `$P'$`.
- **Rationale**: Faithful reproduction of the print typography.

### 6. Display Math Wrapping (HOUSESTYLE R16)
- **Rule**: All display equations must be enclosed in `\[ ... \]`. Multiline display equations must use `\begin{aligned} ... \end{aligned}` or `\begin{gathered} ... \end{gathered}` inside `\[ ... \]`.
- **Forbidden**: Never use bare `\begin{align*}` or `\begin{gather*}` outside `\[ ... \]`.

### 7. Equation Numbering
- **Rule**: Equation numbers are enclosed in parentheses, matching the scan: `\tag{1}`, `\tag{2}`, `\tag{$\mathrm{I}_a^{*)}$}`, `\tag{$\mathrm{I}_b$}`, `\tag{$3_a$}`, `\tag{$3_b$}`.

### 8. Footnotes (HOUSESTYLE R15)
- **Rule**: In-text footnote callouts are set as superscript `${}^{*)}$` in math mode. The footnote body is placed at the foot of the page, led by `\textbf{*)}`.
- **Forbidden**: Do not leave `{}^{*)}` in text mode without `$` delimiters.

### 9. French Typography and Ordinals
- **Rule**:
  - Ordinals: `$1^{\text{re}}$`, `$2^{\text{me}}$`, `$3^{\text{me}}$`, `$k^{\text{me}}$`, `$(s+1)\text{-ième}$` (using `\text` per HOUSESTYLE R21).
  - Number abbreviations: `\no` or `n$^{\mathrm{o}}$`, `\nos` or `n$^{\mathrm{os}}$`.
  - Section headers: Roman numerals `\section*{I. ...}`, `\section*{II. ...}`, etc.
  - Section paragraphs: Bold numbers `\textbf{1.}`, `\textbf{2.}`, etc.
