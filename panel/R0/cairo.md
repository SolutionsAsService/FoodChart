# Critic: Evidence (Cairo), R0

- Anchor used: Cairo's "truthful, functional, insightful" test; every count needs a stated denominator and procedure (How Charts Lie).

- Observed (python on the JSON copies):
  - No chart exists. Cuisines.json has 7 cuisines; DetailedCusines.json has 12 (the 7 are a subset).
  - Detailed slots, total vs distinct (exact string): ingredients 61/40, flavors 39/15, techniques 36/18, dishes 48/48, influences 37/29.
  - Top repeats: Savory 7 of 12, Grilling 6, Olive Oil 4, Garlic 4, Rice 4. These are "listed in N of 12 entries", not facts about cuisines.
  - List lengths vary (ingredients 4-6 per cuisine; Italian has 4 influences, the rest 3), so counts reward longer lists.
  - Bundled items ("Spices (...)", "Cheeses (...)", "Herbs (...)") hide components; exact-match counting misses them.
  - Category errors (Seasonal Ingredients as a technique, Regional diversity as an influence) would plot as false data.
  - Unequal units: "Middle Eastern" is a region beside nations. No selection rule for the 12, no sources.

- Verdict: OBJECT

- Requested change: The home chart's caption must state: the denominator ("12 cuisines chosen by the author, not a sample of the world"); the procedure (items hand-listed, split from bundles, counted as "listed in N of 12"); a fixed list length or a note that lengths differ; the source per cuisine; and "curated, incomplete" in the title. Draw bars from zero or a presence matrix, never world percentages. Remove category errors, label Middle Eastern as a region, and offer the cleaned data file for download.

- Statement of meaning: The artifact says that twelve unexplained cuisines have a few uncited traits each, and it charts none of them.
