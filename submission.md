# Submission — TSK-1ZQ87Q8M (Tempo): Fuse Gothic Style with Cyberpunk Design

**Font:** Afterhours Regular — an original Latin display font.
**Public download (.otf):** https://github.com/bayusd/afterhours-font/raw/main/Afterhours-Regular.otf
**Preview page:** https://bayusd.github.io/afterhours-font/
**Repo (source + specimen):** https://github.com/bayusd/afterhours-font
**Files attached here:** Afterhours-Regular.otf, preview-hero.png,
preview-specimen.png (same files as the repo).

## What it is

A Gothic manuscript hacked by a city from the future. Pointed-arch
blackletter bones (every stem peaks, every round letter is a vesica, never
a plain circle), dramatic thick/thin contrast and sharp terminals — plus
cyberpunk details: a neon inline slit inside every stem and circuit-node
counters punched into selected letters. Dark, electric, a little playful,
readable on a phone.

## System (consistent rules)

1. Pointed arch everywhere — stems peak, bowls are vesicas.
2. Neon inline — a 24-unit slit runs each straight stem, echoing the peak.
3. Circuit nodes — small square counters in A, C, O.
4. Glitch cuts — diagonals (K, R, X, Y, Z, 2, 4, 7) are hard angles, no curves.
5. One weight, two voices — expressive neon hero and quiet flat heading.

## Preview

- Hero treatment: "AFTER HOURS" in neon cyan on near-black (preview-hero.png).
- Simpler website-heading version: "After Hours - heading sample"
  (preview-specimen.png).
- Specimen shows uppercase, lowercase, numerals and punctuation.

## Coverage (labelled honestly)

- Supported (72 chars): A–Z, a–z, 0–9, space, `. , ! ? - ' : ; &`.
- Incomplete: no accented / non-Latin characters, no other punctuation,
  no ligatures or kerning pairs yet. Slashed zero is deliberate.
- Cap height 720, x-height 500, UPM 1000. Verified loadable: fontTools
  reads all tables, renders correctly (see specimen renders).

## Design choices

The brief asked for Gothic bones with cyberpunk energy, so the skeleton is
pure blackletter — pointed arches and high-contrast strokes — while the
cyberpunk lives in the details: a neon slit inside every stem and circuit
nodes instead of decoration. I kept the system to five repeatable rules so
the style holds across caps, lowercase and numerals instead of decorating
one word. It is drawn from scratch as parametric vector outlines
(`build_font.py`, fontTools) — no existing typeface was traced or used
as a base.

## Licence

Free to use and adapt, including on a personal website, with credit to
`bayusd` (LICENSE.md in the repo).
