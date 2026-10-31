# R3 WHOLE round evidence (final round): FoodChart after M1 to M10

Artifact: E:\UBM\FoodChart\site\ (HTML, css\site.css). Data: E:\UBM\FoodChart\_src\data\cuisines.json. Log: E:\UBM\FoodChart\DESIGN-LOG.md (R2 panel and records M9, M10 at the end). Your R2 verdict is in E:\UBM\FoodChart\panel\R2\<seat>.md. Screenshot: mexican-label-R3.jpg.

In R2 all seven seats passed. Since then:
- M9: the duplicate "Shaped by" list beside each label is deleted; the label's influence rows now link to their influences.html row. Empty chart cells carry screen-reader text "no"; the chart's corner cell is a th ("Cuisine"); footer links are 44 px tall; the "None cited yet" and "Every ingredient" links and the page-head breadcrumb link are padded to 24 px or more. about.html says no dietary or allergen information is held.
- M10 (ambition push on the far-apart pairs): pairs are now ranked by how rare the shared ingredients and techniques are (each weighs 1 / the number of cuisines listing it), single shared items allowed, each item printed with its count, and the rule stated on the page. Result: Mexican and Vietnamese (lime 2 of 12, grilling 6 of 12), Middle Eastern and Vietnamese (mint 2, grilling 6), Mexican and Chinese (chili peppers 3, steaming 3), Greek and Indian (yogurt 2). Mexican and Thai dropped out.
- Declined: rewording "12 cuisines per chart" (it is the label's "servings per container" line).

Measured after the last edit (in-app browser, 2026-10-31): footer links 44 px; every link 24 px or more except three cuisine names inline in sentences under "Closest in this chart" (20 px, WCAG inline exception); 0 px horizontal overflow at 375 px on index, mexican, influences, cuisines; focus ring 3 px, 6.18:1; links 6.18:1, muted text 7.85:1. Build: 20 pages, all links and #anchors resolve, no duplicate ids, JSON-LD parses.
