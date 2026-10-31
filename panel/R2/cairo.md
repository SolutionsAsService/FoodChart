# Critic: Evidence (Cairo), R2

- Anchor used: Cairo, How Charts Lie / The Truthful Art: every count needs a stated denominator and procedure; recompute, do not trust.

- Measured (Python on cuisines.json vs site\*.html):
  - Shared "N of 12", all 142 ingredient/flavor/technique rows on 12 labels: printed = recomputed, 0 mismatches.
  - "Out of 45 ingredients ... 13 in more than one": 45 and 13, match.
  - Index "most shared" lines: ingredients 4 (Garlic, Olive oil, Rice), flavors 7 (Savory), techniques 6 (Grilling), influences 4 (Chinese): all match.
  - Chart bottom row (15 flavors): printed 7 5 4 3 3 3 3 2 2 2 1 1 1 1 1; recomputed identical, same order.
  - About totals 48 dishes, 45 ingredients, 15 flavors, 18 techniques, 28 influences: all match (distinct strings).
  - "Entries list 3 to 5 flavors each": recomputed 3 to 5, match. (Ingredient lists run 5 to 7; the caption claims only flavors, so no error.)
  - Far-apart pairs (non-adjacent regions, 2+ shared ingredients/techniques): printed 4 (Mexican-Chinese, -Thai, -Vietnamese; Middle Eastern-Vietnamese); recomputed the same 4 with the same shared items. Greek-Middle Eastern (4) correctly excluded as adjacent.
  - Caption: states denominator ("12 cuisines chosen by hand, not a sample of the world"), procedure ("a square means the entry lists that flavor"; bottom row counts cuisines), length caveat, and "Curated and incomplete". Labels say Sources: none cited yet. R0 requests all answered.

- Verdict: PASS

- Requested change: none (open item only: the pair ranking tie order and the adjacency rule are in DESIGN-LOG, not on the page; optional one-line note).

- Statement of meaning: The site says that twelve hand-picked cuisines list these items, with every count verifiably true to its file and its limits stated beside it.
