# Notation decisions — neumann-1870-logarithmischen-newtonschen-potentiales-i

Cross-page decisions for this work (pp. 49–56). Each states the rule, why, and what NOT to write.

## Greek and script letters

- **φ is `\varphi`, never `\phi`.** The print sets the curly italic form of phi (the one with an
  open loop), as it does for ψ. Do not write `\phi`.
- **ψ is `\psi`**, **ξ, η are `\xi`, `\eta`**, **π is `\pi`**, **ϑ is `\vartheta`** (the script
  theta, the angle's absolute value on p. 51), **ϱ is `\varrho`** (the tailed rho of the density
  `ϱ_s^{(2n)}`), **ϰ is `\varkappa`** (the curved, kappa-like constant `ϰ` on p. 54, set bold-italic;
  checked at magnified size and distinct from the italic `x` of the coordinates). Do not write
  `\theta`, `\rho`, `\kappa` or a plain `x` for these.
- **Ω is `\Omega` (capital omega) and Σ is `\Sigma`**: the two region labels and the sum of
  moments are Greek capitals, `$\Omega$`, `$\Sigma_{z}$`, `$\Omega_{z}$`, `$\Omega_{p}$`. Do not use
  `\sum` for Σ_z (the print's Σ is a letter, not a summation sign) and do not use `\mathfrak` for Ω.
- **𝔓 is `\mathfrak{P}`** (Fraktur capital P naming the interior region), the only Fraktur letter.
  Do not normalise it to a roman P (R13).

## Primes

- **Where the print sets primes before the subscript, write them before it**: `u'_{p}`, `v'_{s}`,
  `w''_{q}` (pp. 53–54). **Where it sets them after the subscript, write them after**: `u_{s}''`,
  `u_{s}''''`, `w_{s}''`, `v_{s}'` (p. 55, formulas for `ϱ` and the double layer). This inconsistency
  is the printer's; reproduce each as printed (R23). Do not unify.
- The primed forms of one letter are consecutive `'` marks (`u'''_{p}`, `u_{s}''''`), never `^{\prime\prime}`.

## Dots

- **A run of dots is `\ldots\ldots`** when the print sets a long run (`a, b, c, d, ……`), a single
  `\ldots` when it sets a short one (`cd, …`). The exact printed dot count of the long runs varies
  between four and six and is not reproduced dot for dot. Do not write `\cdots` or `\dots`.
- A comma that follows the dots in the print is kept: `\ldots\ldots,`.

## Spacing and punctuation

- **A thin or medium space (`\;`) separates the comma-separated items of the point and value
  lists** in displays (`a,\; b,\; c,\;`), but not in inline math, where a plain `, ` between
  separate `$...$` spans is used. A literal space inside math is not spacing (TeX ignores it).
- **The multiplication of a constant and a power is `(M-m)\,\varkappa^{n+1}`** with a thin space
  before the κ, as printed; no `\cdot`.
- **The em dash in running text is `---`**, set with spaces around it in the German (`mag --- nach
  dem Vorgange \emph{Riemann's} --- angesehen`).
- **Author name with a possessive or adjective ending: the italic/spaced part is the name only for
  `\emph{Dirichlet}'schen`**, but the possessive `'s` is inside the run for `\emph{Riemann's}`
  because the print sets it in the same italic.

## Emphasis

- **Both italic and letterspaced (Sperrdruck) emphasis are `\emph`** (R24). The italic statements
  of the general problem on p. 50 are single `\emph{...}` paragraphs in which math stays math; the
  letterspaced words inside one (`dieselben`) are not marked a second time.
- **Roman-numeral conditions `I)`, `II)`, `III)`** are plain text inside the italic run (they are
  italic in the print), not math.

## Orthography

- **No eszett**: this Antiqua print sets round s throughout, so `dass`, `Grösse`, `gewisse`,
  `Anschluss` are written with `ss`. Do not convert any `ss` to `ß` (R19).
- **Edition spelling kept**: `Werthe`, `Puncte`, `Functionen`, `convex`, `Curve`, `conformen`,
  `ächter`, `Radiivectores`, `jenachdem`, `hinerstreckt`, `sämmtlich`, `andrerseits`/`andererseits`
  each as printed (R12). Do not modernise.
- **Section separators (short centred rules) are not transcribed**; the section simply starts a new
  paragraph.
