# Critic: Inclusion (Mace), R0

- Anchor used: Perceptible information (with Simple and intuitive, Tolerance for error).
- Observed:
  - No page exists. EVIDENCE.md: "No README, no website, no page of any kind." CONTRIBUTING.md points to a README that does not exist. A person who cannot read raw JSON, which is most people, has no way in at all.
  - The data carries no meaning a non-visual user could use: 3 of 21 characteristics are placeholders ("Famous dishes", "Popular dishes", "Cooking techniques"). A screen reader would announce empty labels.
  - Wrong kinds of things in fields ("Regional diversity" as an influence; "Minimalist Presentation" as a Japanese technique) and ungrouped ingredients ("Spices (Turmeric, Cumin, Coriander, Cardamom)") mean a reader cannot trust or compare entries.
  - "Middle Eastern" is one entry for many nations with no note; "FoodChart" promises a chart and nothing is charted.
  - Inconsistent keys (`cuisines` vs `DetailedCuisines`) and the misspelt "DetailedCusines.json" cause errors for anyone searching or reusing the data.
- Verdict: OBJECT
- Requested change:
  - Every fact must reach the user as real text, not only as a chart. The home chart needs a text equivalent: a data table or list with a caption, plus a summary sentence of what it shows. Never encode meaning by colour alone; pair colour with labels or patterns, 4.5:1 contrast minimum.
  - Keyboard: every control reachable and operable by Tab, Enter and Space, in visual order, with no traps. First element is a "Skip to content" link. Chart points, filters and sorting must work from the keyboard, not hover.
  - Focus visibility: a persistent, high-contrast focus ring (at least 3:1 against both the element and the page, 2px or more, not removed by CSS), kept clear of sticky headers.
  - Screen reader: landmarks (header, nav, main, footer), one h1 per page with ordered headings, a descriptive title per page, `aria-current` on the nav, `lang="en"`, no empty links or buttons, real `<table>` markup with headers and scope. Chart SVG gets a title and description and is not the only route to the data.
  - Targets of at least 44px, readable at 200% zoom and on a phone, with `prefers-reduced-motion` honoured.
  - Tolerance for error: clean the data to one schema, remove placeholders, split grouped ingredients, add a note on regional scope, and cite sources. Use forgiving search that handles misspellings, and give a clear empty state.
- Statement of meaning: The artifact currently says "food data exists here, but only for those who can read raw JSON, and even that is inconsistent and unsourced."
