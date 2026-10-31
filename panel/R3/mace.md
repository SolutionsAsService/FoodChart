# Critic: Inclusion (Mace), R3
(Saved by the caller from the seat's returned text: the seat's own write left this file empty with ENOSPC, E: full.)

- Anchor used: Perceptible information (with Equitable use, Size and space for approach and use).
- Observed: All three R2 later fixes landed. Chart corner is now th scope=col with sr-only "Cuisine"; every off cell carries sr-only "no" and every on cell "yes" beside an aria-hidden dot, so the grid reads in full by screen reader. Footer links have min-height 44px. Mexican label's influence rows link to influences.html anchors; the duplicate "Shaped by" list is gone, so there is one route to each fact. Favicon linked relatively. No outline:none anywhere. No regression found. Inline sentence links at 20px fall under the WCAG inline exception; acceptable. M10 states its ranking rule and item counts on the page, so the claim is checkable by everyone.
- Focus visibility: check = `:focus-visible` rule in css/site.css line 38, plus grep for outline:none. Result: 3px solid accent, 2px offset, 6.18:1, global; 0 suppressions; mini-labels add a shadow on focus too. PASS.
- Verdict: PASS
- Requested change: none
- Statement of meaning: Anyone who arrives, by any sense or device, now gets the same facts, the same routes to them, and a plain statement of how they were ranked.
