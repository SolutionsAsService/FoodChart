# Critic: Evidence (Cairo), R3

- Anchor used: Cairo, The Truthful Art / How Charts Lie: every number needs its denominator and a procedure the reader can rerun; a ranking must be reproducible from its stated rule.

- Measured (Python, cuisines.json vs site\*.html):
  - Shared "N of 12", all 142 ingredient/flavor/technique rows on 12 labels: printed = recomputed, 0 mismatches.
  - Home pair counts: lime 2, mint 2, grilling 6, chili peppers 3, steaming 3, yogurt 2: all match.
  - Rule rerun (weight 1/n per shared ingredient or technique, adjacent and same-region pairs excluded): Mexican-Chinese 0.667, Mexican-Vietnamese 0.667, Middle Eastern-Vietnamese 0.667, then a three-way tie at 0.5: Mexican-Thai, Greek-Indian, Japanese-Spanish (seafood 2). Printed top 3 = recomputed; printed 4th (Greek-Indian) is valid but chosen from a 3-way tie. The page does not state the tie-break, and the printed order differs from tie order only by an unstated rule.
  - About totals 48 dishes, 45 ingredients, 15 flavors, 18 techniques, 28 influences: match. Chart bottom row 7 5 4 3 3 3 3 2 2 2 1 1 1 1 1: match.

- Verdict: PASS

- Requested change: none required. Optional one line on the page: "Ties at the cut-off are broken by [rule]; Mexican-Thai and Japanese-Spanish score the same as the last pair shown." Otherwise "top 4" overstates.

- Statement of meaning: Twelve hand-picked cuisines are compared by a stated, rerunnable rule, and every printed count is true to its file, with one tie at the cut-off left unexplained.
