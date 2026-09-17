# Notation decisions — Cayley 1871, *On the Deficiency of Certain Surfaces* (Math. Ann. 3)

Work-spanning rendering decisions for this transcription. The paper is four printed pages
(pp. 526–529) in *Mathematische Annalen*, Band 3 (1871).

## Symbols

- **Cuspidal lines are Greek kappa $\varkappa$ (`\varkappa`), never Latin $x$ or modern $\kappa$.**
  On pp. 526–527, the singularities of the tangent-cone at an $i$-conical point are given as
  $\delta$ double lines and $\varkappa$ cuspidal lines, yielding the deficiency terms
  $(\delta + \varkappa)$. In classical curve theory (Plücker, Salmon, Cayley), $\delta$ is the
  number of nodes and $\kappa$ the number of cusps. In Teubner's 19th-century mathematical font,
  lowercase Greek kappa is set as the rounded script variant `\varkappa`. Magnified, the glyph
  features an ascender loop on the left and two rounded lobes on the right, distinct from the
  crossed italic strokes of Latin $x$. Write `\varkappa`.
- **Latin $x$ on p. 528 is the number of double points of a space curve.** In the torse formulas
  on p. 528, Cayley cites Salmon's notation for space curves and developables: $m$ is order, $n$ is
  class, $r$ is rank, $\alpha$ is cusps (stationary points), $\beta$ is stationary planes, and $x$
  is actual double points of the space curve ($x = \frac{1}{2}(r^2 - r - n - 3m)$). Here $x$ is
  the Latin letter $x$.
- **Latin $x, y, z$ and Greek $\omega$ on p. 529 are homogeneous coordinates.** Cayley writes
  $x : y : z : \omega = \alpha : \beta : \gamma : \delta$. The fourth coordinate is Greek $\omega$
  (`\omega`), never Latin $w$.
- **Theta is capital Greek $\Theta$ (`\Theta`).** On p. 527, $\Theta$ denotes "the number of
  certain singular points on $c$, the nature of wich I do not completely understand, and which is
  here taken to be $= 0$."
- **Gamma is Greek $\gamma$ (`\gamma`).** On p. 527, $\gamma$ is the number of stationary points on
  cuspidal curve $c$. On p. 528, $\gamma = rm + 12r - 14m - 6n$.
- **Do. is the 19th-century abbreviation for "Ditto".** On p. 527, the explanations of symbols read:
  `q, class of Do.,` and `r, class of Do.,`. Written as `\text{Do.,}`.
- **Cayley's symbolic form notation is preserved.** On p. 529, Cayley writes
  $(\delta x - \alpha\omega, \delta y - \beta\omega, \delta z - \gamma\omega)^3 = 0$,
  $(\alpha, \beta, \gamma)^3 = 0$, and $(x, y, z)^2$ to denote homogeneous forms of degree 3 and 2.
  Preserved as standard math parentheses.
- **Fractions in displays.** Numerical fractions multiplying expressions ($\frac{1}{6}$, $\frac{1}{2}$)
  are written with `\frac{1}{6}`, `\frac{1}{2}`.

## Typography

- **German quotation marks `„..."` are preserved as literal Unicode** (HOUSESTYLE R22).
  Although the paper is written in English, the journal was published by B. G. Teubner in Leipzig,
  and the compositor used German low-opening and high-closing quotes: `„Postulation“`,
  `„deficiency“`, `„Memoir on the theory of Reciprocal surfaces“`.
- **`quà` is set with a grave accent in `\emph`** (`\emph{quà}`). This is the Latin/Italian/French
  particle "quà" ("in the capacity of"), set in italics with a grave accent in the print.
- **Archaic contraction `thro'` is kept verbatim** (R3). On p. 529, Cayley writes "the cone to pass
  thro' the point $x = 0, y = 0, z = 0$". Kept as printed.
- **Author byline and names.** On p. 526, the byline is "By A. Cayley." with the name set in small
  capitals, which collapses to `\emph` (R20): `By \emph{A.~Cayley}.` Names in text (`Dr.~Noether`,
  `Dr.~Clebsch`, `Salmon's`) use a non-breaking space after the title abbreviation.
- **Closing dateline.** On p. 529, the paper concludes with `Cambridge, 5.\ Jan.\ 1871.` with
  control spaces after abbreviation dots (R17).

## Structure & Page Boundaries

- **`\origpage` markers are contiguous: 526, 527, 528, 529.**
- **Page 527 opens mid-sentence** with the continuation of the definition of deficiency from p. 526:
  `\origpage{527}` is placed immediately before the display equation $D = \dots$ with no paragraph break.
- **Page 528 opens with a new paragraph**: `I find that the same property exists \emph{first}...`.
- **Page 529 opens mid-sentence** with the calculation of $D$ for the quintic surface:
  `\origpage{529}` precedes the display equation without a blank line.

## Printer's Errors Reproduced (R4)

Each printer's error is accompanied by an inline `\ednote{...}` popover in `original.tex`
explaining the error for the reader without modifying the author's printed text.

- **p. 527, "the nature of wich I do not completely understand"**: `wich` is printed without an `h`.
  Faithfully reproduced as printed.
- **p. 528, in $h = \frac{1}{2}(m^2 - 10m -- 3n + 8r)$**: A double hyphen `--` is set between
  $10m$ and $3n$.
- **p. 528, in $D = -\frac{1}{2}(m+n) + r - 1 = -\frac{1}{2}(m - 1)(m-2) + h + \beta$**: The minus
  sign in $(m - 1)$ shows a small ink defect or dot above the rule. It represents the standard
  minus sign $(m - 1)$ matching the identical formula earlier on the same page.
- **p. 529, in $(\delta x - \alpha\omega, \delta y -- \beta\omega, \delta z - \gamma\omega)^3 = 0$**:
  A double hyphen `--` is set between $\delta y$ and $\beta\omega$, matching the double hyphen in
  the formula for $h$ on p. 528.


