"""Build the FoodChart site from _src/data/cuisines.json into site/.

Every page is written from the one data file. The counts the site prints
("in 4 of 12", "shares 5 items") are computed here, so they cannot drift
from the data. The build fails if a page links to a file that does not exist.

    python _src/build.py
"""
import html
import json
import pathlib
import re
import shutil
import sys
from collections import defaultdict

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
OUT = ROOT / "site"
DATA = json.loads((SRC / "data" / "cuisines.json").read_text(encoding="utf-8"))
DOMAIN = "https://foodchart.shadw.app/"
NAME = "FoodChart"
CUISINES = DATA["cuisines"]
N = len(CUISINES)
BY_SLUG = {c["slug"]: c for c in CUISINES}
REGIONS = ["The Americas", "Europe", "West Asia and North Africa", "South Asia", "East Asia", "Southeast Asia"]
CUISINES.sort(key=lambda c: (REGIONS.index(c["region"]), c["name"]))
FACETS = [("ingredients", "Ingredients", "ingredient"), ("flavors", "Flavors", "flavor"),
          ("techniques", "Techniques", "technique"), ("influences", "Influences", "influence")]
NAV = [("index", "Chart"), ("cuisines", "Cuisines"), ("ingredients", "Ingredients"), ("flavors", "Flavors"),
       ("techniques", "Techniques"), ("influences", "Influences"), ("about", "About")]
e = html.escape


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("é", "e")).strip("-")


def items(c, field):
    """A cuisine's list for a field, as plain names (influences are {name, kind})."""
    return [x["name"] if isinstance(x, dict) else x for x in c[field]]


KIND = {(c["slug"], i["name"]): i["kind"] for c in CUISINES for i in c["influences"]}


def index_of(field):
    """item -> list of cuisines that list it, most shared first."""
    idx = defaultdict(list)
    for c in CUISINES:
        for item in items(c, field):
            idx[item].append(c)
    return dict(sorted(idx.items(), key=lambda kv: (-len(kv[1]), kv[0].lower())))


IDX = {f: index_of(f) for f, _, _ in FACETS}


def shared_items(a, b):
    out = []
    for f, label, _ in FACETS[:3]:
        out += [(label, x) for x in items(a, f) if x in items(b, f)]
    return out


def closest(c, k=3):
    others = [(o, shared_items(c, o)) for o in CUISINES if o is not c]
    others.sort(key=lambda t: (-len(t[1]), t[0]["name"]))
    return [t for t in others[:k] if t[1]]


def rarity(x):
    """How many cuisines list an ingredient or technique."""
    return len(IDX["ingredients"].get(x) or IDX["techniques"].get(x))


ADJACENT ={frozenset(p) for p in [("Europe", "West Asia and North Africa"), ("East Asia", "Southeast Asia"),
                                   ("South Asia", "Southeast Asia"), ("South Asia", "West Asia and North Africa")]}


def far_neighbors(k=4):
    """Pairs from regions that are neither the same nor adjacent, ranked by how rare the ingredients and
    techniques they share are: each shared item weighs 1 / the number of cuisines that list it.
    Flavor words are left out as too general. Ties go to the pair whose rarest item is rarer."""
    pairs = []
    for i, a in enumerate(CUISINES):
        for b in CUISINES[i + 1:]:
            if a["region"] == b["region"] or frozenset((a["region"], b["region"])) in ADJACENT:
                continue
            concrete = [x for _, x in shared_items(a, b) if x not in IDX["flavors"]]
            if concrete:
                pairs.append((a, b, concrete))
    score = lambda t: sum(1 / rarity(x) for x in t[2])
    pairs.sort(key=lambda t: (-score(t), min(rarity(x) for x in t[2]), t[0]["name"], t[1]["name"]))
    tied = [t for t in pairs[k:] if abs(score(t) - score(pairs[k - 1])) < 1e-9]
    return pairs[:k], tied


def page_url(name):
    return DOMAIN if name == "index" else DOMAIN + name


def cuisine_link(c):
    return f'<a href="{c["slug"]}.html">{e(c["name"])}</a>'


def count_cell(n):
    return f'<span class="dv">{n}<span class="of"> of {N}</span></span>'


# ---------- layout

def layout(name, title, description, body, crumb=None, ld_extra=None):
    nav = "\n".join(
        f'        <li><a href="{slug}.html"{" aria-current=\"page\"" if slug == name or (slug == "cuisines" and name in BY_SLUG) else ""}>{label}</a></li>'
        for slug, label in NAV)
    graph = [{"@type": "WebSite", "@id": DOMAIN + "#site", "url": DOMAIN, "name": NAME, "inLanguage": "en-US"},
             {"@type": "WebPage", "@id": page_url(name) + "#page", "url": page_url(name), "name": title,
              "description": description, "isPartOf": {"@id": DOMAIN + "#site"}, "inLanguage": "en-US"}]
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate([("Chart", DOMAIN)] + crumb)]})
    graph += ld_extra or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    head = "" if name == "404" else f"""<link rel="canonical" href="{page_url(name)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{page_url(name)}">
<meta property="og:image" content="{DOMAIN}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A nutrition-facts style label reading Food Chart: twelve cuisines, their dishes, ingredients, flavors and techniques.">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld}</script>"""
    robots = '<meta name="robots" content="noindex">' if name == "404" else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{robots}
{head}
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,600;0,800;0,900;1,400&display=swap">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-row">
    <a class="brand" href="index.html"><span class="brand-word">Food Chart</span><span class="brand-sub">{N} cuisines per chart</span></a>
    <nav aria-label="Main">
      <ul class="site-nav">
{nav}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <p class="foot-word">Food Chart</p>
      <p>{N} cuisines, the influences that shaped them, and what they cook with. Open data under the MIT license.</p>
    </div>
    <div>
      <p class="foot-h">Cuisines</p>
      <ul class="foot-list">{"".join(f"<li>{cuisine_link(c)}</li>" for c in CUISINES)}</ul>
    </div>
    <div>
      <p class="foot-h">Indexes</p>
      <ul class="foot-list"><li><a href="ingredients.html">Ingredients</a></li><li><a href="flavors.html">Flavors</a></li><li><a href="techniques.html">Techniques</a></li><li><a href="influences.html">Influences</a></li><li><a href="about.html">About the data</a></li><li><a href="data/cuisines.json">Download the JSON</a></li></ul>
    </div>
  </div>
  <p class="wrap foot-fine">* Every count on this site is a count of this chart's {N} cuisines, not of the world's kitchens.</p>
</footer>
</body>
</html>
"""


# ---------- pieces

def matrix(field, caption, cols=None):
    cols = cols or list(IDX[field])
    head = "".join(f'<th scope="col"><span>{e(x)}</span></th>' for x in cols)
    rows = []
    for c in CUISINES:
        cells = "".join(
            f'<td class="{"on" if x in items(c, field) else "off"}">{"<span class=dot aria-hidden=true></span><span class=sr-only>yes</span>" if x in items(c, field) else "<span class=sr-only>no</span>"}</td>'
            for x in cols)
        rows.append(f'<tr><th scope="row">{cuisine_link(c)}</th>{cells}</tr>')
    tot = "".join(f"<td>{len(IDX[field][x])}</td>" for x in cols)
    return f"""<div class="matrix-wrap" role="region" aria-labelledby="cap-{field}" tabindex="0">
  <table class="matrix">
    <caption id="cap-{field}">{caption}</caption>
    <thead><tr><th scope="col" class="corner"><span class="sr-only">Cuisine</span></th>{head}</tr></thead>
    <tbody>
{chr(10).join(rows)}
    </tbody>
    <tfoot><tr><th scope="row">Cuisines</th>{tot}</tr></tfoot>
  </table>
</div>"""


IMPOSED = ("Empire and conquest", "Colonial rule", "Forced migration and enslavement")


def shaped_by(c):
    """Influences on the label: chosen and shared first, then a heavy rule and the imposed ones."""
    def lis(xs):
        return "".join(f'<li><a href="influences.html#{slugify(i["name"])}-{slugify(i["kind"])}">{e(i["name"])}</a>'
                       f'<span class="kind">{e(i["kind"])}</span></li>' for i in xs)
    free = [i for i in c["influences"] if i["kind"] not in IMPOSED]
    forced = [i for i in c["influences"] if i["kind"] in IMPOSED]
    out = f'<div class="l-sec"><h3 class="l-h">Shaped by</h3><ul class="l-rows">{lis(free)}</ul></div>'
    if forced:
        out += f'<div class="bar mid"></div><div class="l-sec"><h3 class="l-h">Imposed</h3><ul class="l-rows">{lis(forced)}</ul></div>'
    return out


def label(c, mini=False):
    def rows(field, title, shared=True):
        lis = "".join(
            f'<li><span>{e(x)}</span>{count_cell(len(IDX[field][x])) if shared and not mini else ""}</li>' for x in items(c, field))
        return f'<div class="l-sec"><h3 class="l-h">{title}{"<span class=dv-h>Shared*</span>" if shared and not mini else ""}</h3><ul class="l-rows">{lis}</ul></div>'
    dishes = f'<div class="l-sec"><h3 class="l-h">Dishes</h3><p class="l-dishes">{", ".join(e(d) for d in c["dishes"])}</p></div>'
    tag = "a" if mini else "section"
    attrs = f' href="{c["slug"]}.html"' if mini else f' aria-labelledby="l-{c["slug"]}"'
    head = f'<p class="l-title"{"" if mini else f" id=l-{c["slug"]}"}>{e(c["name"])}</p>'
    if mini:
        return f"""<{tag} class="label mini"{attrs}>
  <p class="l-kicker">Cuisine Facts</p>{head}
  <p class="l-serv">{e(c["region"])}</p>
  <div class="bar"></div>
  {dishes}
  <p class="l-mini-flav"><strong>Flavors</strong> {", ".join(e(x) for x in c["flavors"])}</p>
</{tag}>"""
    return f"""<{tag} class="label"{attrs}>
  <p class="l-kicker">Cuisine Facts</p>
  {head}
  <p class="l-serv"><span>Region</span> <strong>{e(c["region"])}</strong></p>
  <p class="l-serv"><span>Scope</span> <strong>{e(c["scope"])}</strong></p>
  <div class="bar"></div>
  {dishes}
  <div class="bar mid"></div>
  {rows("ingredients", "Ingredients")}
  {rows("flavors", "Flavors")}
  {rows("techniques", "Techniques")}
  {shaped_by(c)}
  {f'<div class="l-sec"><h3 class="l-h">Sets it apart</h3><p class="l-dishes">{" · ".join(e(x) for x in c["principles"])}</p></div>' if c["principles"] else ""}
  <div class="bar"></div>
  <p class="l-serv l-src"><span>Sources</span> <strong>{", ".join(e(s) for s in c["sources"]) or '<a href="about.html#sources">None cited yet</a>'}</strong></p>
  <p class="l-foot">* Shared tells you how many of the {N} cuisines in this chart list the same item. It is a count from this chart's data, not a measure of the world's cooking.</p>
</{tag}>"""


# ---------- pages

def tied_pair(a, b, shared):
    items_ = " and ".join(f"{x.lower()} ({rarity(x)} of {N})" for x in shared)
    return f"{cuisine_link(a)} and {cuisine_link(b)}, {e(items_)}"


def page_index():
    lens = sorted(len(c["flavors"]) for c in CUISINES)
    flav = matrix("flavors", f"{N} cuisines chosen by hand, not a sample of the world. A square means the cuisine's entry lists that flavor; "
                             f"entries list {lens[0]} to {lens[-1]} flavors each, so a cuisine with more squares is not a stronger-tasting one. "
                             f"The bottom row counts the cuisines that list each flavor. Curated and incomplete.")
    shared_ing = [(x, cs) for x, cs in IDX["ingredients"].items() if len(cs) > 1]
    top = "".join(f'<li><a href="ingredients.html#{slugify(x)}">{e(x)}</a> {count_cell(len(cs))}</li>' for x, cs in shared_ing[:8])
    shown, tied = far_neighbors()
    tie_note = ""
    if tied:
        left_off = "; ".join(tied_pair(a, b, s) for a, b, s in tied)
        tie_note = (f'<p class="hint">Scoring the same as the last pair, and left off: {left_off}. '
                    "Ties go to the pair whose rarest shared item is rarer, then alphabetically.</p>")
    pairs = "".join(
        f'<li><p class="pair">{cuisine_link(a)} <span>and</span> {cuisine_link(b)}</p>'
        f'<p class="regions">{e(a["region"])} · {e(b["region"])}</p><p>Both list {" and ".join(f"{e(x.lower())} ({rarity(x)} of {N})" for x in s)}.</p></li>'
        for a, b, s in shown)
    body = f"""<header class="hero wrap">
  <p class="kicker">An open chart of world cooking</p>
  <h1>Twelve cuisines, read like the back of a box.</h1>
  <p class="lede">What each cuisine cooks, tastes of, and who shaped it, charted against the other {N - 1}. <a href="#label-h">How to read a label</a> · <a href="cuisines.html">All {N} labels</a></p>
</header>
<section class="section wrap chart-sec" id="chart" aria-labelledby="chart-h">
  <h2 id="chart-h">The flavor chart</h2>
  <p class="section-lede">Read across for a cuisine, down for a flavor.</p>
  {flav}
</section>
<section class="section wrap" aria-labelledby="far-h">
  <h2 id="far-h">Far apart, something in common</h2>
  <p class="section-lede">Cuisines from regions that do not border each other, whose entries name the same ingredient or technique. The rarer the shared item in this chart, the higher the pair ranks: lime, listed by 2 of the {N}, counts for more than grilling, listed by 6. Flavor words are left out as too general. A shared item says the lists overlap, not that the kitchens are alike.</p>
  <ul class="pairs">{pairs}</ul>
  {tie_note}
</section>
<section class="section wrap split" aria-labelledby="label-h">
  <div>
    <h2 id="label-h">How to read a label</h2>
    <p>Every cuisine gets a label laid out like the Nutrition Facts on a box. Instead of nutrients it lists dishes, ingredients, flavors, techniques and the peoples, empires and trade that shaped it.</p>
    <p>Where a food label prints % Daily Value, this one prints <strong>Shared</strong>: how many of the {N} cuisines in the chart list the same item. <strong>Scope</strong> says whether the entry is one country's cooking or a family of them. <strong>Sources</strong> says what the facts rest on; none are cited yet, and the label says so.</p>
    <p><a class="btn" href="cuisines.html">Read all {N} labels</a></p>
  </div>
  {label(BY_SLUG["mexican"])}
</section>
<section class="section wrap split" aria-labelledby="shared-h">
  <div>
    <h2 id="shared-h">Most shared ingredients</h2>
    <p>Out of {len(IDX["ingredients"])} ingredients in the chart, {len(shared_ing)} turn up in more than one cuisine.</p>
    <p><a class="pad" href="ingredients.html">Every ingredient →</a></p>
  </div>
  <ul class="l-rows shared-list">{top}</ul>
</section>
<section class="section wrap" aria-labelledby="idx-h">
  <h2 id="idx-h">Read it another way</h2>
  <ul class="index-cards">
    <li><a href="ingredients.html"><strong>Ingredients</strong><span>{len(IDX["ingredients"])} ingredients and who uses them</span></a></li>
    <li><a href="flavors.html"><strong>Flavors</strong><span>{len(IDX["flavors"])} flavors across {N} cuisines</span></a></li>
    <li><a href="techniques.html"><strong>Techniques</strong><span>{len(IDX["techniques"])} ways of cooking</span></a></li>
    <li><a href="influences.html"><strong>Influences</strong><span>{len(IDX["influences"])} peoples, empires and trade routes</span></a></li>
  </ul>
</section>"""
    return layout("index", "FoodChart: 12 World Cuisines Charted · Dishes, Ingredients, Flavors",
                  "An open chart of twelve world cuisines: their dishes, ingredients, flavors, techniques and influences, set out as food labels and compared side by side.", body)


def page_cuisines():
    groups = []
    for r in REGIONS:
        cs = [c for c in CUISINES if c["region"] == r]
        if cs:
            groups.append(f'<h2 class="region-h">{e(r)}</h2><ul class="labels">{"".join(f"<li>{label(c, mini=True)}</li>" for c in cs)}</ul>')
    body = f"""<header class="page-head wrap">
  <p class="kicker">Cuisines</p>
  <h1>{N} cuisines, {len(groups)} regions.</h1>
  <p class="lede">Each label opens the cuisine's full facts: dishes, ingredients, flavors, techniques, influences, and the cuisines in this chart it has most in common with.</p>
</header>
<section class="section wrap">
{chr(10).join(groups)}
</section>
<section class="section wrap gaps" aria-labelledby="gaps-h">
  <h2 id="gaps-h">Not on the chart yet</h2>
  <p>Twelve entries leave most of the world's kitchens out. Among the missing:</p>
  <ul class="gap-list">{"".join(f"<li>{e(x)}</li>" for x in DATA["not_yet_charted"])}</ul>
  <p><a href="about.html#add">How to add a cuisine</a></p>
</section>"""
    return layout("cuisines", f"All {N} Cuisines · FoodChart",
                  f"The {N} cuisines in FoodChart, grouped by region: Mexican, Italian, French, Greek, Spanish, Middle Eastern, Indian, Chinese, Japanese, Korean, Thai and Vietnamese.",
                  body, crumb=[("Cuisines", page_url("cuisines"))])


def page_cuisine(c):
    i = CUISINES.index(c)
    prev, nxt = CUISINES[i - 1], CUISINES[(i + 1) % N]
    near = "".join(
        f'<li><p><strong>{cuisine_link(o)}</strong> shares {len(s)}: {", ".join(e(x) for _, x in s)}</p></li>' for o, s in closest(c))
    body = f"""<header class="page-head wrap">
  <p class="kicker"><a href="cuisines.html">Cuisines</a> · {e(c["region"])}</p>
  <h1>{e(c["name"])} cuisine</h1>
  <p class="lede">{e(c["summary"])}</p>
</header>
<section class="section wrap split label-split">
  {label(c)}
  <div class="aside">
    <h2>Closest in this chart</h2>
    <p class="hint">Counted from shared ingredients, flavors and techniques.</p>
    <ul class="near">{near or "<li>No shared items with the other cuisines here.</li>"}</ul>
    <nav class="pager" aria-label="More cuisines">
      <a href="{prev["slug"]}.html"><span>Previous</span> {e(prev["name"])}</a>
      <a href="{nxt["slug"]}.html"><span>Next</span> {e(nxt["name"])}</a>
    </nav>
  </div>
</section>"""
    title = f"{c['name']} Cuisine: Dishes, Ingredients, Flavors and Influences · FoodChart"
    desc = f"{c['name']} cuisine at a glance: {', '.join(c['dishes'][:3])} and more, cooked with {', '.join(x.lower() for x in c['ingredients'][:3])}. {c['summary']}"
    if len(desc) > 165:
        desc = f"{c['name']} cuisine at a glance: {', '.join(c['dishes'][:3])}, its key ingredients, flavors, techniques and influences."
    return layout(c["slug"], title, desc, body, crumb=[("Cuisines", page_url("cuisines")), (c["name"], page_url(c["slug"]))])


def page_facet(field, label_, noun):
    idx = IDX[field]
    sections = []
    groups = [("Shared", [(x, cs) for x, cs in idx.items() if len(cs) > 1]),
              ("In one cuisine only", [(x, cs) for x, cs in idx.items() if len(cs) == 1])]
    if field == "influences":
        groups = [(k, [(x, [c for c in cs if KIND[(c["slug"], x)] == k]) for x, cs in idx.items()]) for k in DATA["kinds"]]
        groups = [(k, [(x, cs) for x, cs in g if cs]) for k, g in groups]
    for gname, rows_in in groups:
        if not rows_in:
            continue
        rows = "".join(
            f'<tr id="{slugify(x)}{"-" + slugify(gname) if field == "influences" else ""}"><th scope="row">{e(x)}</th><td>{", ".join(cuisine_link(c) for c in cs)}</td><td class="num">{count_cell(len(cs))}</td></tr>'
            for x, cs in rows_in)
        sections.append(f"""<h2>{gname} <span class="count">{len(rows_in)}</span></h2>
<table class="facet">
  <thead><tr><th scope="col">{e(noun.capitalize())}</th><th scope="col">Cuisines</th><th scope="col" class="num">Shared*</th></tr></thead>
  <tbody>{rows}</tbody>
</table>""")
    intro = {
        "ingredients": f"Every ingredient the {N} cuisines list, with the cuisines that use it. Olive oil and rice cross the most borders.",
        "flavors": f"Every flavor the {N} cuisines are described with. The chart below shows them all at once; the tables underneath list them one by one.",
        "techniques": f"Every way of cooking the {N} cuisines list. Grilling is the one most of them share.",
        "influences": "The peoples, empires and trade routes each cuisine was shaped by, grouped by how they arrived: a cuisine's own roots, trade and exchange, migration, empire and conquest, colonial rule, and forced migration and enslavement. The kinds were assigned by this project's one author, from outside these kitchens, and are open to correction.",
    }[field]
    lead = sorted(idx.items(), key=lambda kv: -len(kv[1]))[0]
    extra = matrix("flavors", f"Which of the {N} cuisines list each flavor.") if field == "flavors" else ""
    body = f"""<header class="page-head wrap">
  <p class="kicker">Index · {len(idx)} {e(label_.lower())}</p>
  <h1>{e(label_)}</h1>
  <p class="lede">{e(intro)}</p>
</header>
<section class="section wrap">
  <p class="stat"><strong>{e(lead[0])}</strong> is the most shared: {len(lead[1])} of {N} cuisines.</p>
  {extra}
  {chr(10).join(sections)}
  <p class="hint">* Shared counts the cuisines in this chart that list the {e(noun)}.</p>
</section>"""
    return layout(field, f"{label_} Across {N} World Cuisines · FoodChart",
                  f"Which of {N} world cuisines share each {noun}: an index of {len(idx)} {label_.lower()} from Mexican to Vietnamese, with the cuisines that use each one.",
                  body, crumb=[(label_, page_url(field))])


def page_about():
    ds = {"@type": "Dataset", "name": "FoodChart cuisines", "description": DATA["about"], "url": page_url("about"),
          "license": "https://opensource.org/licenses/MIT", "creator": {"@type": "Organization", "name": "SolutionsAsService"},
          "distribution": {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": DOMAIN + "data/cuisines.json"}}
    body = f"""<header class="page-head wrap">
  <p class="kicker">About</p>
  <h1>About the chart and its data</h1>
  <p class="lede">FoodChart is a small, open dataset of {N} cuisines and this site, which reads it. It is a starting point for comparing kitchens, not an authority on any of them.</p>
</header>
<section class="section wrap prose">
  <h2>What is in it</h2>
  <p>For each cuisine: the region, the influences that shaped it, four well-known dishes, its key ingredients, the flavors it is known for, its main techniques, and anything that sets it apart. That is {sum(len(c["dishes"]) for c in CUISINES)} dishes, {len(IDX["ingredients"])} ingredients, {len(IDX["flavors"])} flavors, {len(IDX["techniques"])} techniques and {len(IDX["influences"])} influences in all.</p>
  <h2>What it leaves out</h2>
  <p>No dietary or allergen information is held. A dish listed here may or may not contain meat, dairy, gluten, nuts or anything else; check a recipe, not this chart.</p>
  <p>Twelve entries cannot hold the world's cooking. Most of these cuisines are many cuisines: Sichuan and Cantonese cooking differ more than many neighbouring countries do, and "Middle Eastern" here stands for a family that includes Lebanese, Syrian, Palestinian, Turkish and Persian cooking. Each list is the short version a curious cook would start from.</p>
  <h2>Every count is a count of this chart</h2>
  <p>When a label says an ingredient is shared by "4 of {N}", it means four of the {N} cuisines in this dataset list it. Each entry lists a handful of characteristic ingredients, not everything its cooks use, so an item listed for four cuisines may well be cooked with in many more.</p>
  <h2>Whose categories these are</h2>
  <p>The template every label follows (dishes, ingredients, flavors, techniques, influences) and the kinds of influence are this project's way of comparing kitchens, not the way these cuisines describe themselves. They were set by one author from outside them. Where a cook from one of these traditions would draw the lines differently, that is a correction worth sending.</p>
  <h2>Use the data</h2>
  <p>The whole dataset is one JSON file, free to use under the MIT license: <a href="data/cuisines.json">data/cuisines.json</a>. Each cuisine has <code>slug</code>, <code>name</code>, <code>region</code>, <code>scope</code>, <code>summary</code>, <code>influences</code> (each a <code>name</code> and a <code>kind</code>), <code>dishes</code>, <code>ingredients</code>, <code>flavors</code>, <code>techniques</code>, <code>principles</code> and <code>sources</code>.</p>
  <h2 id="sources">Sources</h2>
  <p>None are cited yet. The facts here are general knowledge as written by the project, and every label says so in its Sources row. If you can point to a cookbook, a food history or a cook's own account for any line, add it to that cuisine's <code>sources</code> list and the label will print it.</p>
  <h2>How influences are sorted</h2>
  <p>Each influence carries a kind: the cuisine's own roots, trade and exchange, migration, empire and conquest, colonial rule, or forced migration and enslavement. "Spanish" beside "Mexican" means something different from "Silk Road trade" beside "Chinese", and the kind says how. These are judgments, not settled facts; correct them the same way as anything else.</p>
  <h2 id="add">Fix something or add a cuisine</h2>
  <p>Not on the chart yet: {", ".join(e(x) for x in DATA["not_yet_charted"])}. A new cuisine needs the same fields as the others, ideally from someone who cooks it.</p>
  <p>The source is on GitHub at <a href="https://github.com/SolutionsAsService/FoodChart">SolutionsAsService/FoodChart</a>. Open an issue for a wrong fact, ideally with a source, or send a pull request that edits <code>_src/data/cuisines.json</code>.</p>
  <h2>Where it came from</h2>
  <p>The data began in July 2024 as two files, <code>Cuisines.json</code> and <code>DetailedCusines.json</code>. This site merged them into one: the detailed file already held every cuisine and influence in the short one, grouped ingredients such as "Spices (Turmeric, Cumin, Coriander, Cardamom)" were split so they can be compared, and entries that were in the wrong field, such as "Regional diversity" listed as an influence, moved to where they belong.</p>
</section>"""
    return layout("about", "About FoodChart: An Open Dataset of 12 World Cuisines",
                  f"What FoodChart's data holds and leaves out, how its counts work, and how to download the JSON or correct a fact. Open data under the MIT license.",
                  body, crumb=[("About", page_url("about"))], ld_extra=[ds])


def page_404():
    body = """<header class="page-head wrap">
  <p class="kicker">Not on the chart</p>
  <h1>That page isn't on the menu.</h1>
  <p class="lede">Try <a href="index.html">the chart</a>, <a href="cuisines.html">all the cuisines</a> or <a href="ingredients.html">the ingredient index</a>.</p>
</header>"""
    return layout("404", "Page not found · FoodChart", "This page does not exist.", body)


# ---------- assets and checks

def favicon():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<style>.p{fill:#fff}.i{fill:#111}@media (prefers-color-scheme: dark){.p{fill:#111}.i{fill:#f4f1ea}}</style>
<rect class="i" x="3" y="1" width="26" height="30" rx="2"/>
<rect class="p" x="6" y="4" width="20" height="24"/>
<rect class="i" x="8" y="6" width="16" height="6"/>
<rect class="i" x="8" y="14" width="16" height="3"/>
<rect class="i" x="8" y="19" width="10" height="2"/>
<rect class="i" x="8" y="23" width="13" height="2"/>
</svg>
"""


def check_links():
    bad = []
    for p in OUT.glob("*.html"):
        for href in re.findall(r'href="([^"#:?]+)(?:#[^"]*)?"', p.read_text(encoding="utf-8")):
            if href.startswith(("http", "mailto", "//")):
                continue
            if not (OUT / href).exists():
                bad.append(f"{p.name} -> {href}")
    for p in OUT.glob("*.html"):
        s = p.read_text(encoding="utf-8")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            json.loads(block)
        ids = re.findall(r' id="([^"]+)"', s)
        bad += [f"{p.name}: duplicate id {i}" for i in sorted(set(ids)) if ids.count(i) > 1]
        for target, frag in re.findall(r'href="([a-z0-9-]+\.html)#([^"]+)"', s):
            if f'id="{frag}"' not in (OUT / target).read_text(encoding="utf-8"):
                bad.append(f"{p.name} -> {target}#{frag}")
    if bad:
        sys.exit("broken links:\n  " + "\n  ".join(bad))


def main():
    pages = {"index": page_index(), "cuisines": page_cuisines(), "about": page_about(), "404": page_404()}
    for c in CUISINES:
        pages[c["slug"]] = page_cuisine(c)
    for f, lab, noun in FACETS:
        pages[f] = page_facet(f, lab, noun)
    for n, s in pages.items():
        (OUT / f"{n}.html").write_text(s, encoding="utf-8")
    (OUT / "data").mkdir(exist_ok=True)
    shutil.copy(SRC / "data" / "cuisines.json", OUT / "data" / "cuisines.json")
    (OUT / "favicon.svg").write_text(favicon(), encoding="utf-8")
    listed = [n for n in pages if n != "404"]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "\n".join(f"  <url><loc>{page_url(n)}</loc></url>" for n in listed) + "\n</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}sitemap.xml\n", encoding="utf-8")
    llms = [f"# {NAME}", "", f"> An open chart of {N} world cuisines: dishes, ingredients, flavors, techniques and influences. Data: {DOMAIN}data/cuisines.json (MIT).", ""]
    for n in listed:
        t = re.search(r"<title>(.*?)</title>", pages[n]).group(1)
        d = re.search(r'<meta name="description" content="(.*?)">', pages[n]).group(1)
        llms.append(f"- [{html.unescape(t)}]({page_url(n)}): {html.unescape(d)}")
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    check_links()
    print(f"built {len(pages)} pages into site/, links checked")


if __name__ == "__main__":
    main()
