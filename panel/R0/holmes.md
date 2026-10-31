# Critic: Inclusion (Holmes), R0

- **Anchor used:** Kat Holmes, *Mismatch*: exclusion is a mismatch between a person and the design, not a trait of the person. Solve for one, extend to many; use the persona spectrum (permanent, temporary, situational).

- **Observed:**
  - There is no interface at all. CONTRIBUTING.md says "See the README for how to run or use what is here"; no README exists. Anyone who cannot read raw JSON (most people, anyone on a phone, a screen-reader user with no markup) is excluded entirely.
  - The name promises a chart, but "nothing is charted". A reader who thinks visually is mismatched; a reader who needs text equivalents has nothing to compare against either.
  - Cuisines are reduced to a US-centric canon of 7 (12 detailed). "Middle Eastern" is "one entry covering many national cuisines; no note says so". Whole regions (African, Caribbean, South American beyond Mexico) are absent. People whose food is missing are excluded by data design.
  - Placeholder strings ("Famous dishes", "Popular dishes", "Cooking techniques") and category errors ("Regional diversity" as an influence) force the reader to already know the subject. Newcomers and non-native English readers are mismatched.
  - Dietary and situational needs are unaddressed: "Vegetarian dishes" appears once as a characteristic; no allergens, halal, kosher, vegan or gluten-free filters.
  - No sources, so users cannot judge or correct what is said about their own food.

- **Verdict:** OBJECT

- **Requested change:**
  1. Solve for one: a keyboard- and screen-reader-first reader of a single cuisine page. Every chart gets a text/table twin; colour is never the only encoding; high contrast, large touch targets, readable on a phone in a kitchen (situational: one hand, glare).
  2. Extend to many: plain-language labels and a short glossary; no placeholders; one controlled vocabulary per field.
  3. Add a dietary/ingredient-restriction filter and a visible "regions not yet covered" note; split "Middle Eastern" into sub-regions or label it explicitly.
  4. Cite sources and give a "suggest a correction" path that works without an endpoint (mailto/issue link).
  5. Add a real README that states who this is for.

- **Statement of meaning:** The artifact currently says "this is data for people who already know both the subject and how to read JSON", and it treats a narrow set of cuisines as the whole world.
