# R1 WHOLE round evidence: the redesigned FoodChart

Artifact: the built site in E:\UBM\FoodChart\site\ (read the HTML: index.html, cuisines.html, vietnamese.html, middle-eastern.html, influences.html, ingredients.html, about.html; styles in site\css\site.css). Data: E:\UBM\FoodChart\_src\data\cuisines.json. Screenshots: home-desktop.jpg (1280 wide, first screen), vietnamese-phone.jpg (375 wide).

What changed since R0 (moves M1 to M6, see E:\UBM\FoodChart\DESIGN-LOG.md section 2):
- M1 one cleaned data file; grouped ingredients split; mis-filed items moved to a `principles` field; old files deleted (kept on branch legacy-2026-10-30); README written.
- M2 every cuisine is a "Cuisine Facts" label in the Nutrition Facts form, with a "Shared*" column ("3 of 12") where % Daily Value would be, and a footnote saying it is a count of this chart, not of the world.
- M3 home: chart first.
- M4 every label has "Sources: None cited yet" linked to the about page; "Not on the chart yet" lists 12 missing cuisines; the chart caption states the denominator, the procedure, that entries list 3 to 5 flavors, and "Curated and incomplete".
- M5 each influence has a kind (Roots, Trade and exchange, Migration, Empire and conquest, Colonial rule, Forced migration and enslavement); influences page grouped by kind; Scope row on each label.
- M6 home "Unexpected neighbors": the 4 cross-region pairs sharing the most items, computed at build.

Measured on the rendered pages (in-app browser, 2026-10-30):
- Home at 1280x768: chart heading top y = 378 px (was 968 before M3), chart grid top 486 px.
- Contrast on the light paper: links 6.18:1, muted text 7.85:1; body ink about 18:1. Dark mode tokens also exist.
- Keyboard focus (Tab): solid 3 px outline in the accent, 6.18:1 against the page.
- Targets: all links 24 px or taller except two inline text links ("None cited yet" 19 px, "Every ingredient →" 20 px).
- Horizontal page overflow at 375 px wide: 0 px on index, vietnamese, influences, cuisines. The chart scrolls inside its own labelled, focusable region.
- One h1 per page; skip link; nav marks the current page with aria-current; the chart is a real <table> with th scope row/col and a caption; filled squares carry visually hidden "yes".
- Build: 20 pages, every internal link resolves, every JSON-LD block parses.
