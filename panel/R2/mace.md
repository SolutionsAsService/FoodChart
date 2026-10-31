# Critic: Inclusion (Mace), R2

- Anchor used: Perceptible information (with Equitable use and Size and space for approach and use).
- Observed:
  - R0 answered. There is now a real site. Every page has lang="en", a skip link (hidden at top:-60px, shown on focus), header, nav aria-label="Main" with aria-current, main, footer, one h1 and ordered h2/h3.
  - The home chart is a real table with caption, th scope col and row, and a tfoot count row. Meaning is not colour alone: "on" is a dark square plus sr-only "yes". The scroll region is a labelled, focusable region.
  - Labels use headings and lists. The Imposed block has its own heading, so structure is not carried by the heavy rule alone. Sources, scope and denominator are stated.
  - Weak spots, none blocking: "off" cells are empty, so a screen reader hears nothing for "no". The thead corner is a bare td. Footer links have only 3px padding (about 33px tall). There is no prefers-reduced-motion rule, but the CSS has no animation or transition, so nothing needs reducing.
- Focus visibility: check = `:focus-visible` rule in site.css. Result: a 3px solid accent outline with 2px offset on all elements, 6.18:1 on paper, and no outline:none anywhere. Skip link, chart region and mini-labels show it. PASS.
- Verdict: PASS
- Requested change: none now. For later: add sr-only "no" to off cells, make the corner cell a th with sr-only text, pad footer links to 44px.
- Statement of meaning: The artifact now says "these facts are for everyone who arrives, by any route", with its own limits stated plainly.
