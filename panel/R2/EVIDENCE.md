# R2 WHOLE round evidence: FoodChart after moves M1 to M8

Artifact: the built site in E:\UBM\FoodChart\site\ (read the HTML; styles site\css\site.css). Data: E:\UBM\FoodChart\_src\data\cuisines.json. Design log with every move: E:\UBM\FoodChart\DESIGN-LOG.md. Screenshots here: mexican-label-desktop.jpg (lower half of a cuisine label), far-apart-phone.jpg (home section at 375 px), home-desktop-R1.jpg (home first screen; unchanged above the chart since R1).

Moves: M1 one cleaned data file, README, old files removed. M2 every cuisine is a "Cuisine Facts" label in the Nutrition Facts form with a "Shared*" count column. M3 chart first on home. M4 "Sources: None cited yet" on every label, "Not on the chart yet" list, chart caption states denominator and procedure. M5 influences carry a kind; Scope row. M6/M8 home section "Far apart, something in common": pairs from non-adjacent regions ranked only by shared ingredients and techniques. M7 the label's "Shaped by" now splits with a heavy rule into a separate "Imposed" block (empire and conquest, colonial rule, forced migration and enslavement); "African" renamed "Enslaved Africans"; influences.html lists under each kind only the cuisines that kind applies to (it previously repeated all of them); about.html says the template and kinds are this project's, set by one outside author. M8 also lifted "Sets it apart" into the label.

Measured on the rendered pages (in-app browser, 2026-10-31, after the last edit):
- Home at 1280x768: chart heading top y = 386 px, chart grid top 497 px (968 before M3).
- Contrast on light paper: links 6.18:1; muted text 7.85:1; ink about 18:1. Dark-mode tokens exist.
- Keyboard focus (Tab): solid 3 px accent outline, 6.18:1.
- Targets: every link 24 px or taller except two inline text links ("None cited yet" 19 px, "Every ingredient →" 20 px).
- Horizontal page overflow at 375 px: 0 on index, mexican, influences, cuisines, vietnamese. The chart scrolls inside its own labelled, focusable region.
- Build: 20 pages; every internal link and every #anchor resolves; no duplicate ids; JSON-LD parses.
