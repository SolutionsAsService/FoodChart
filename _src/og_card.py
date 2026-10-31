"""Draw site/og.png, the 1200x630 social card: a Food Chart label beside the flavor chart.

Needs Pillow. Run once after the data changes: python _src/og_card.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

SRC = pathlib.Path(__file__).resolve().parent
DATA = json.loads((SRC / "data" / "cuisines.json").read_text(encoding="utf-8"))["cuisines"]
INK, PAPER = (20, 18, 16), (255, 253, 248)


def font(size, bold=True):
    for name in (["arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold else ["arial.ttf", "DejaVuSans.ttf"]):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


im = Image.new("RGB", (1200, 630), PAPER)
d = ImageDraw.Draw(im)
d.rectangle([48, 40, 560, 590], outline=INK, width=4)
d.text((66, 50), "Food Chart", font=font(78), fill=INK)
d.line([66, 142, 542, 142], fill=INK, width=2)
d.text((66, 152), f"{len(DATA)} cuisines per chart", font=font(28, False), fill=INK)
d.rectangle([60, 200, 548, 214], fill=INK)
def distinct(field):
    return str(len({x if isinstance(x, str) else x["name"] for c in DATA for x in c[field]}))


rows = [("Dishes", str(sum(len(c["dishes"]) for c in DATA))), ("Ingredients", distinct("ingredients")),
        ("Flavors", distinct("flavors")), ("Techniques", distinct("techniques")), ("Influences", distinct("influences"))]
y = 228
for k, v in rows:
    d.text((66, y), k, font=font(34), fill=INK)
    w = d.textlength(v, font=font(34))
    d.text((542 - w, y), v, font=font(34), fill=INK)
    y += 54
    d.line([66, y - 8, 542, y - 8], fill=INK, width=1)
d.rectangle([60, y + 4, 548, y + 12], fill=INK)
d.text((66, y + 24), "Open data · foodchart.shadw.app", font=font(26, False), fill=INK)

flavors = sorted({f for c in DATA for f in c["flavors"]}, key=lambda f: -sum(f in c["flavors"] for c in DATA))
x0, y0, s = 620, 70, 34
for j, c in enumerate(DATA):
    for i, f in enumerate(flavors):
        cx, cy = x0 + i * s, y0 + j * 42
        if f in c["flavors"]:
            d.rectangle([cx, cy, cx + 24, cy + 24], fill=INK)
        else:
            d.rectangle([cx + 10, cy + 10, cx + 14, cy + 14], fill=(200, 194, 184))
im.save(SRC.parent / "site" / "og.png", optimize=True)
print("site/og.png")
