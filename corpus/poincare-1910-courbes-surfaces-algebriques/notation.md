# Notation decisions — Poincaré 1910

Cross-page rendering decisions for Henri Poincaré's 1910 memoir in *Annales scientifiques de l'École Normale Supérieure*,
*Sur les courbes tracées sur les surfaces algébriques* (3e série, tome 27, pp. 55–108), established under HOUSESTYLE R27.

## Letterforms and variables

- **The Poincaré normal functions $v_i$:** Written as standard math italic `$v_i$` (and plural `$v_1, v_2, \ldots, v_p$`).
  The 19th/early 20th-century French letterpress font uses a round-shouldered italic $v$.
  **Do not** write Greek `\nu` or `\upsilon`; **do not** write `\mathbf{v}` or `\mathrm{v}`.
- **The abelian integrals $u_i$ and $U$:** Written as standard math italic `$u_i$`, `$u_1, u_2, \ldots, u_{2p}$`, and `$U$`.
  **Do not** write `\mathrm{U}`.
- **Rational functions and polynomials $R, H, M, \Pi$:**
  Single-letter variables set in roman type in French letterpress are presentation, not notation (HOUSESTYLE R1).
  Transcribe as standard math italic `$R$`, `$R_i$`, `$H$`, `$M$`.
  The abelian integral sum `$\Pi$` is standard uppercase Greek `\Pi`.
- **Greek letters:**
  - `\varphi` for algebraic surfaces and curve equations: $\varphi(x, y) = 0$. **Do not** write `\phi`.
  - `\psi` for auxiliary polynomials.
  - `\rho` for coefficients in the abelian decomposition $\rho_1, \rho_2, \ldots, \rho_{2p}$.
  - `\Delta` for the differential operator $\Delta u_i = \frac{du_i}{dy} - \sum \rho^i u$.
  - `\Theta` for theta functions.
  - `\Sigma` for summation when printed as a capital Sigma operator `\sum` vs `\Sigma`. Follow the print: where an explicit index range or subscript is used as a summation operator, use `\sum`; where printed as standalone `\Sigma \rho^i u`, use `\sum`.

## Subscripts, superscripts, and primes

- **Subscripts are always braced:** `$u_{i}$`, `$v_{i}$`, `$x_{0}$`, `$x_{1}$`, `$\rho_{2p}$`.
  **Do not** write bare `u_i` or `x_0`.
- **Superscripts and dual indices:**
  In expressions like $\rho_k^i$, $\Pi_1^i$, $\Pi_0^i$, $u_i^m$, write `\rho_k^i`, `\Pi_1^i`, `\Pi_0^i`, `u_i^m` with braced sub/superscripts: `\rho_{k}^{i}`, `\Pi_{1}^{i}`, `\Pi_{0}^{i}`, `u_{i}^{m}`.
- **Partial derivative primes:** `$f'_z$`, `$f'_x$`, `\varphi'_y`, `\varphi'_x`.
  The apostrophe prime precedes the variable subscript: `$f'_{z}$`, `$\varphi'_{y}$`.

## Differentials and operators

- **Differentials carry a thin space:** `\,dx`, `\,dy`, `\,dz`, `\,dt`. **Do not** write bare `dx`.
- **Derivatives:** `\frac{df}{dz}`, `\frac{du_i}{dy}`, `\frac{\partial u_i}{\partial y}`, `\frac{\partial x_1}{\partial y}`.
- **Inline large operators:** Every inline `\int` carries `\displaystyle`: `$\displaystyle\int R \frac{dx}{f'_z}$`.

## Displays, tags, and alignment

- **Display math wrapping:** All display formulas must be wrapped in `\[ ... \]` (HOUSESTYLE R16).
  Multiline displays use `\[ \begin{gathered} ... \end{gathered} \]` or `\[ \begin{aligned} ... \end{aligned} \]`.
  **Never** write bare `\begin{gather*}` or `\begin{align*}` outside `\[ ... \]`.
- **Display punctuation:** Trailing commas, semicolons, and periods are kept inside `\[ ... \]`.
- **Equation numbers:** Equation tags are placed via `\tag{n}` inside the display:
  - `\tag{1}`, `\tag{2}`, `\tag{3}`, `\tag{4}`, `\tag{5}`.
  - Sub-equations: `\tag{5 a}`, `\tag{5 b}`, `\tag{5 c}`, `\tag{5 d}`.

## Structure and typography

- **Section headings:**
  - `\section*{I. --- Introduction.}`
  - `\section*{II. --- Définition des fonctions $v_i$.}`
  - `\section*{III. --- Propriétés des fonctions $v_i$.}`
  - `\section*{IV. --- Courbes correspondant aux fonctions $v_i$.}`
  - `\section*{V. --- Classification des courbes algébriques.}`
  - `\section*{VI. --- Intégrales de différentielles totales de première espèce.}`
  - `\section*{VII. --- Systèmes linéaires.}`
  - `\section*{VIII. --- Nombre des valeurs critiques.}`
  No text-mode braces inside `\section*{...}` (HOUSESTYLE R25).
- **Page furniture omitted:**
  Running heads ("H. POINCARÉ.", "SUR LES COURBES TRACÉES SUR LES SURFACES ALGÉBRIQUES."),
  page numbers (55–108), and bottom signature marks ("Ann. Éc. Norm., (3), XXVII. — FÉVRIER 1910.", etc.) are omitted.
- **Footnotes:**
  Follow HOUSESTYLE R15: place footnotes inline as a complete unit at the end of the page's text, led by `\textbf{(1)}`, with in-text references as `${}^{(1)}$`.
