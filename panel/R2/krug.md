# Critic: Usability (Krug), R2

- Anchor used: Don't Make Me Think, the trunk test (what is this, where am I, what can I do here).

- Observed: Home answers "what is this" at once: h1 "Twelve cuisines, read like the back of a box.", lede "What each cuisine cooks, tastes of, and who shaped it, charted against the other 11", then the chart directly below; row names are links. "Where am I": the same 7-item nav on all three pages with aria-current marked (Chart, Cuisines on thai.html, Ingredients on ingredients.html); logo links home; thai.html has the kicker "Cuisines . Southeast Asia" as a link back. "What can I do": Thai's "Closest in this chart" and Previous/Next, ingredients rows link every cuisine. The ingredients page opens with a stat ("Garlic is the most shared: 4 of 12") and two tables with identical columns, so it scans. The label is repeated identically on each cuisine. Remaining small friction: the visible breadcrumb exists only as JSON-LD, and the ingredients page has no "Home >" trail; the brand sub-line "12 cuisines per chart" is odd wording; "Shaped by" appears twice on thai.html (label and aside); two inline links are under 24 px ("None cited yet", "Every ingredient").

- Verdict: PASS

- Requested change: none (optional later: reword "12 cuisines per chart"; drop the duplicate "Shaped by" aside).

- Statement of meaning: A first-time visitor now sees a food chart of twelve cuisines, knows which page they are on, and can click through to any cuisine or index without working anything out.
