# Schulte's coefficient and lattice-path conjectures

This note proves Werner Schulte's coefficient and nonnegative-path
conjectures for implicit trinomial and quadrinomial series, extending the
coefficient-transfer formula in Vladimir Kruchinin's 2011 Theorem 8.1
(retained as Theorem 28 of the 2013 two-author revision). The general
positive-power transfer is prior work, not a new theorem of this note.
The common integer-parameter statement includes `nk+m=0` explicitly.
Written corollaries cover the binomial-square exponential identities
recorded by Paul D. Hanna and the positive-power specializations of Peter Bala.
Earlier ordinary quadrinomial identities are credited to their recorded
authors, including Roberto Blanco Gómez's proof of 12 October 2026.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
python3 verify.py > verification.json
```

Alternatively, with a current LaTeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; there are no external figures or
BibTeX dependencies. Python 3.10 or later and its standard library suffice
for the exact integer and rational comparisons. For reproducible PDF dates,
set `SOURCE_DATE_EPOCH=1794787200` before building.

## Mathematical coverage

- Theorem 1 constructs the unique integer series `P=Q_d(x P^n)` for every
  integer `n` and `d>=1`, where `Q_d=1+t+...+t^d`. It gives every coefficient
  of `P^m` for every integer `m`, with the constant term and `nk+m=0` handled
  explicitly. The alternating binomial form applies when `d=2,3` and
  `nk+m!=0`, with polynomial binomial coefficients for negative upper indices.
- Corollary 2 gives the nonnegative-path interpretation for positive integers
  `d,n,m`. The negative-parameter extension is algebraic, not a counting claim.
- Corollaries 3–5 give logarithms, substitutions, ordinary quadrinomial rows,
  and Hanna's exponential identities, with complete written proofs.
- The source coverage table identifies proved source assertions, credited
  earlier formulas, the restored `x^k` in the exponential statements, the
  integer-parameter extension, and the other models outside these arguments.

The first abstract sentence identifies the precise posing statement in
OEIS A262082, revision 23, FORMULA. The companion posing source is A261440,
revision 32. The cited OEIS snapshot is
`https://github.com/oeis/oeisdata/tree/49db7744e1fdbefbe376d1d018370c017d4c288b`.

## Prior formulas and path results

- Kruchinin, *Compositae and their properties*, arXiv:1103.2582v1,
  Theorem 8.1, pp. 13–14 (14 March 2011), gives the general transfer.
  The 2013 revision by Vladimir V. and Dmitry V. Kruchinin retains it
  as Theorem 28, equation (26), pp. 23–24. Section 1 of the note gives
  the exact translation of its composita indices.
- Banderier–Flajolet (2002), Corollary 2 and Example 3, supply the
  bridge/excursion logarithm and tree-coding mechanisms. Sokal (2009),
  Propositions 3.1–3.2, supplies general formal-series and ordered-forest
  formulas; Gessel (2016), Sections 2.2 and 4.5, gives later treatments.
- Yan, arXiv:2501.01152v1 (2 January 2025), Section 5,
  Corollary 5.2(D1), proves the entire trinomial excursion family:
  substitute his odd parameter `2n-1`. His paper identifies this path
  class with Yang–Zhang–Yang's 2024 enumeration. The arbitrary-power
  forest correspondence has the complete written proof in Corollary 2.
- The note also cites the later composita treatment of Kruchinin–Perminova
  (2021), the polynomial coefficient argument of Myerson (2014), and the
  bounded-composition summation analysis of Belbachir–Mendonça (2026).

These references establish overlap at the specified scopes; no priority
claim is made for assembling the Schulte formulas.

## Formal declarations and finite comparisons

The declaration `result` in
`https://github.com/the-omega-institute/trureturing/blob/2f8421f6b90d37b4815b887f6c60987553831b20/D5/S3/Combinatorics/PowerSeries/SchulteImplicitQuadrinomialPowers.lean`
proves integer-series unique existence and the quadrinomial power-coefficient
formula for `n,m>=1` and every `k>=0`. Its `Native` definition is the same
quadrinomial equation as in the note.

The declaration `result` in
`https://github.com/the-omega-institute/trureturing/blob/2f8421f6b90d37b4815b887f6c60987553831b20/D5/S1/Recurrence/SchulteQuadrinomialAlternatingBinomialExpansion.lean`
proves the ordinary alternating quadrinomial coefficient identity for
`N>=0` and `0<=k<=3N`, where `T N k` is the coefficient of `t^k` in `Q_3^N`.

The integer-parameter extension, zero-denominator value, paths, trinomial
identities, substitutions and binomial-square identities are written proofs.
`verify.py` implements independent finite comparisons by coefficient recursion,
integer reciprocals, polynomial convolution, generalized binomial sums,
nonnegative-height path enumeration, logarithmic differentiation and composition.
`verification.json` gives the ranges and counts for each family. These finite
comparisons supplement the all-index arguments, rather than replacing them.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Creative Commons Attribution 4.0 International (CC BY 4.0), `cc-by-4.0`.
