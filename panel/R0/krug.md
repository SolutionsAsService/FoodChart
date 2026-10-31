# Critic: Usability (Krug), R0

- Anchor used: Don't Make Me Think, the trunk test (what is this, where am I, what can I do here).

- Observed: No page exists, so the trunk test fails at step one: "No README, no website, no page of any kind." CONTRIBUTING.md says "See the README for how to run or use what is here"; there is no README, so the only signpost points at nothing. The name "FoodChart" promises a chart; "nothing is charted". "DetailedCusines.json" is misspelled, and two overlapping files (7 vs 12 cuisines, `cuisines` vs `DetailedCuisines`) leave me unsure which is true. Placeholders ("Famous dishes", "Popular dishes", "Cooking techniques") look like content and say nothing. Mis-filed items ("Regional diversity" as an influence, "Seasonal Ingredients" as a technique) make labels untrustworthy. Groups like "Herbs (Mint, Parsley)" cannot be scanned.

- Verdict: OBJECT

- Requested change:
  1. Home answers in one screen: name, one-line purpose, and the chart first; each cuisine clickable.
  2. Same global nav on every page (Home, Cuisines, Ingredients, Flavors, Techniques, Influences, About), current page marked, logo links home.
  3. Page titles plus breadcrumbs (Home > Cuisines > Thai).
  4. Identical cuisine-page layout and headings so pages scan; items link to index pages.
  5. Delete placeholders, refile mis-filed items, split grouped ingredients, label "Middle Eastern" as a region.
  6. One cleaned data file, one spelling, a README stating what the site is.
  7. Plain text labels; no mystery icons.

- Statement of meaning: The artifact currently says "here is some food data, work it out yourself", under a name that promises a chart and a README that does not exist.
