# Notation decisions — Poincaré 1911

Cross-page rendering decisions for Henri Poincaré's 1911 memoir in *Sitzungsberichte der Berliner Mathematischen Gesellschaft*,
*Sur les courbes tracées sur une surface algébrique* (10. Jahrgang, pp. 28–55; reprinted in *Œuvres*, t. VI, pp. 140–178), established under HOUSESTYLE R27.

## Letterforms and variables

- **Title orthography:**
  The title is printed with the singular: *Sur les courbes tracées sur une surface algébrique* (in contrast to the 1910 *Annales* memoir which has the plural *sur les surfaces algébriques*).
- **The normal functions $v_i$:**
  Written as math italic `$v_i$` (and plural `$v_1, v_2, \ldots, v_p$`).
  Note: in this 1911 memoir, Poincaré defines $v_i = u_i^1 + u_i^2 + \ldots + u_i^m$ directly (p. 148), explicitly noting this differs from his 1910 memoir where he had set $m v_i = \sum u_i$.
  **Do not** write Greek `\nu` or `\upsilon`; **do not** write `\mathbf{v}` or `\mathrm{v}`.
- **Abelian integrals and points:**
  - Integrals: `$u_i$`, `$u_1, u_2, \ldots, u_{2p}$`, and superscripted evaluations at points `$u_i^1, u_i^2, \ldots, u_i^m$`.
  - Points: `$M_1, M_2, \ldots, M_m$`, `$A_1, A_2, \ldots, A_n$`, `$B_i$`.
  - Curves: `$C$`, plane section `$K_y$`, surface `$S$`.
- **Rational functions and polynomials:**
  - Standard math italic `$P_i$`, `$Q$`, `$R$`, `$R_i$`, `$H$`.
  - Surface equation: homogeneous `$F(x, y, z, t) = 0$`.
- **Greek letters:**
  - `\varphi` for auxiliary equations: `\varphi(x, y) = 0`. **Do not** write `\phi`.
  - `\psi` for auxiliary polynomials.
  - `\rho` for coefficients in the abelian decomposition and Picard invariant.
  - `\omega` for periods: `\omega_{ki}`, `\omega_{1i}, \ldots, \omega_{2p,i}`.
  - `\Delta` for the Picard differential operator `\Delta_i(\omega) = 0`.
  - `\Theta` and `\theta` for theta functions.
- **Imaginary unit:**
  Poincaré consistently writes `\sqrt{-1}` (e.g. `2\pi\sqrt{-1}`). Transcribe as `\sqrt{-1}`, not `i`.

## Subscripts, superscripts, and primes

- **Subscripts are always braced:** `$u_{i}$`, `$v_{i}$`, `$K_{y}$`, `$\omega_{ki}$`, `$\omega_{2p,i}$`.
- **Superscripts and dual indices:**
  In expressions like $u_i^m$, $u_i^1$, write `u_{i}^{m}`, `u_{i}^{1}` with braced sub/superscripts.
- **Partial derivatives:**
  `$F'_{z}$`, `$f'_{z}$`. The apostrophe prime precedes the variable subscript.

## Differentials and operators

- **Differentials carry a thin space:** `\,dx`, `\,dy`, `\,dz`, `\,dt`. **Do not** write bare `dx`.
- **Derivatives:** `\frac{d\omega}{dy}`, `\frac{d^{2p}\omega}{dy^{2p}}`, `\frac{\partial u_i}{\partial y}`.
- **Inline large operators:** Every inline `\int` carries `\displaystyle`: `$\displaystyle\int \frac{P_i\,dx}{Q F'_z}$`.

## Displays, tags, and alignment

- **Display math wrapping:** All display formulas must be wrapped in `\[ ... \]` (HOUSESTYLE R16).
  Multiline displays use `\[ \begin{gathered} ... \end{gathered} \]` or `\[ \begin{aligned} ... \end{aligned} \]`.
  **Never** write bare `\begin{gather*}` or `\begin{align*}` outside `\[ ... \]`.
- **Display punctuation:** Trailing commas, semicolons, and periods are kept inside `\[ ... \]`.
- **Equation numbers:** Equation tags are placed via `\tag{n}` inside the display: `\tag{1}`, `\tag{2}`, etc.

## Structure and typography

- **Section headings:**
  The print numbers sections with Arabic numerals followed by an em-dash:
  - `\section*{1. --- Valeurs critiques.}`
  - `\section*{2. --- Les fonctions $v_i$.}`
  - `\section*{3. --- Formation des fonctions normales.}`
  - `\section*{4. --- Introduction des fonctions abéliennes.}`
  - `\section*{5. --- Classification des courbes.}`
  - `\section*{6. --- Équations des courbes $C$.}`
  - `\section*{7. --- Élimination des valeurs critiques de la seconde sorte.}`
  No text-mode braces inside `\section*{...}` (HOUSESTYLE R25).
- **Page furniture omitted:**
  Running heads ("COURBES TRACÉES SUR UNE SURFACE ALGÉBRIQUE."), page numbers (140–178), and volume signature marks ("H. P. — VI. 19", etc.) are omitted.
- **Original vs editorial footnotes:**
  - Authorial footnotes (by Poincaré) are transcribed following HOUSESTYLE R15: in-text reference as `${}^{(1)}$`, and footnote text inline at the bottom of the page preceded by `\textbf{(1)}`.
  - Modern critical apparatus and editorial commentary added by René Garnier in the 1953 *Œuvres* edition (notes signed `(R. G.)`, cross-references to "ce tome", post-1912 citations) are **omitted**, ensuring a faithful, clean public-domain transcription of Poincaré's 1911 work.
- **Hyphenation across page breaks:**
  Words hyphenated across page breaks in the print edition are completed on the page where they begin before the `\origpage` tag:
  - `première` completed at the foot of p. 141 before `\origpage{142}`.
  - `déterminées` completed at the foot of p. 175 before `\origpage{176}`.
- **Printer's letterpress error on p. 151:**
  On p. 151, the print lists the sequence of cuts as `Q_{1}, Q_{2}, \ldots, Q_{l}` due to a broken/misset character `l` instead of `h` (where $h$ denotes the number of singular points and cuts, consistently referenced as $h$ throughout Sections 2 and 3: "les $h$ coupures", $\rho_{hj}$). Silently corrected to `$Q_h$`.
