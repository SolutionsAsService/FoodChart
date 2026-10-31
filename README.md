# FoodChart

An open chart of twelve world cuisines: the dishes, ingredients, flavors and techniques each one is known for, and the peoples, empires and trade routes that shaped it. Every cuisine is set out as a label laid out like the Nutrition Facts on a box, and charted against the others.

Live at https://foodchart.shadw.app/ once deployed.

## The data

Everything lives in one file, [`_src/data/cuisines.json`](_src/data/cuisines.json), also published at `/data/cuisines.json` (MIT license). Each cuisine has:

| Field | What it holds |
|---|---|
| `slug`, `name`, `region` | identity and the region it is grouped under |
| `scope` | `National cuisine`, `Many regional cuisines` or `A family of national cuisines` |
| `summary` | one sentence |
| `influences` | `{ "name", "kind" }`; kind is one of `kinds` at the top of the file |
| `dishes`, `ingredients`, `flavors`, `techniques` | one item each, so they can be compared across cuisines |
| `principles` | what sets the cuisine apart that is not a technique |
| `sources` | citations; empty for now, and every label says so |

`not_yet_charted` lists cuisines the chart does not cover yet.

This file replaces the original `Cuisines.json` and `DetailedCusines.json` (2024). The detailed file already held every cuisine and influence in the short one; grouped ingredients such as "Spices (Turmeric, Cumin, Coriander, Cardamom)" were split, and entries in the wrong field (for example "Regional diversity" as an influence) were moved. The originals are on the `legacy-2026-10-30` branch.

## The site

- `site/`: the published site (committed, built output). 20 pages: the chart, all cuisines, one page per cuisine, indexes of ingredients, flavors, techniques and influences, about, 404.
- `_src/build.py`: the generator. Python 3, standard library only.
- `index.html`: root redirect into `site/`.
- `vercel.json` (root, `outputDirectory: site`) and `site/vercel.json` (`outputDirectory: .`): deploys with the Root Directory blank or set to `site`, on Vercel or Shadw. No framework markers at the root.
- `DESIGN-LOG.md`, `panel/`: the design run that produced the site.

To change anything, edit the data or the generator, then:

```bash
python _src/build.py
```

The build writes every page, the sitemap, `robots.txt`, `llms.txt` and the favicon, computes every count the site prints, and fails on a broken link or invalid structured data.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections with a source are the most useful thing you can send.
