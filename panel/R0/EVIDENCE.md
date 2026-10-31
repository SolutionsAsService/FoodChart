# R0 premortem evidence: FoodChart as inherited (commit 7a4e144)

The repository holds exactly four files: `Cuisines.json` (1,526 bytes), `DetailedCusines.json` (5,355 bytes), `LICENSE` (MIT), `CONTRIBUTING.md`. Copies of both JSON files are in this folder.

Measured facts:
- No README, no website, no page of any kind. CONTRIBUTING.md says "See the README for how to run or use what is here"; no README exists.
- `DetailedCusines.json` is misspelled (Cusines).
- `Cuisines.json` lists 7 cuisines; `DetailedCuisines` lists 12. The 7 in the first file are all in the second, with influence lists that are equal or shorter in all 7.
- Top-level keys differ in style: `cuisines` vs `DetailedCuisines`.
- In `Cuisines.json`, 3 of 21 key_characteristics are placeholders that say nothing: "Famous dishes", "Popular dishes", "Cooking techniques".
- Fields hold the wrong kind of thing: "Regional diversity" appears as an influence (Chinese, French); "Minimalist Presentation" and "Seasonal Ingredients" appear as Japanese techniques; "Fresh Preparation" as a Vietnamese technique.
- Grouped ingredients cannot be compared across cuisines: "Spices (Turmeric, Cumin, Coriander, Cardamom)", "Cheeses (Parmesan, Mozzarella)", "Herbs (Thyme, Rosemary)", "Herbs (Mint, Parsley)".
- "Middle Eastern" is one entry covering many national cuisines; no note says so.
- No sources are cited for any fact.
- The name "FoodChart" promises a chart; nothing is charted.

The planned redesign: a multi-page static site (home with a chart, a page per cuisine, index pages for ingredients, flavors, techniques and influences, about) built from one cleaned data file.
