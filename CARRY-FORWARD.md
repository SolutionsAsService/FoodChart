# FoodChart carry-forward ledger

Facts this run established by measurement. Read before any later design run on this project.

| Fact | How it was measured | Move it changed |
|---|---|---|
| A count of "how many cuisines list X" rewards entries with longer lists; entries list 3 to 5 flavors and 5 to 7 ingredients, so raw overlap counts favour long entries and generic words. | R0 Cairo recount; R1 Shklovsky on the Greek / Middle Eastern pair | M8, M10: rank pairs by 1 / (cuisines listing the item), leave flavor words out |
| Grouping a facet page by a second key (influence kind) must filter the row's cuisines by that key too, or every group repeats the full list and inflates its count. | influences.html "Chinese" listed 4 cuisines under Migration; data gave 1 | M7 |
| One item can appear in several groups on one page, so row ids need the group in them (`chinese-migration`), or the page carries duplicate ids and `#` links land on the first. | build check found 3 × `id="chinese"` | M7; the build now fails on duplicate ids and on any `#anchor` that does not resolve |
| An `<a>` inside a `<th>` or a small-caps kicker measures at its line box (15 to 20 px), under the 24 px target, even when the cell is tall. `display: inline-block` plus vertical padding fixes it; a taller cell does not. | in-app browser, `getBoundingClientRect().height` | M9 |
| `element.focus()` from a script does not trigger `:focus-visible`, so a focus-ring check must press Tab; a scripted focus reports `outline-style: none` and looks like a defect. | in-app browser: scripted focus gave `none`, Tab gave `solid 3px` | measurement procedure |
| Measuring computed styles immediately after `navigate` can read the page before the stylesheet applies (nav links measured 17 px, contrast 1:1). Wait for load or re-measure. | in-app browser, first R1 measurement | measurement procedure |
| Text written by hand into an image (the social card) drifts from the data: two of five figures were wrong on first draw. Compute every figure the card prints. | `og_card.py` printed 53 and 19; the data gives 45 and 18 | og_card.py |
| Panel seats write their verdict files to the same drive as the project; a full drive (E: at 640 KB free) silently leaves empty files while the seat still returns its text. Check free space before a round, and save returned text when a file is empty. | R3: three seats reported ENOSPC | R3 collection |
