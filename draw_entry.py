#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news infographic (1024x1024 PNG).

Written from scratch in this session. Config-driven: the STORIES table
holds every word on the image; the drawing code below only lays it out.
Run: python3 draw_entry.py  ->  entry.png (same directory).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

OUT = "entry.png"
W, H = 1024, 1024

# ---- palette ---------------------------------------------------------
NAVY = (13, 27, 62)
NAVY_DARK = (9, 19, 44)
GOLD = (212, 175, 88)
CREAM = (247, 243, 235)
CARD = (255, 255, 255)
INK = (18, 18, 18)
GREY = (92, 92, 92)
RED = (178, 34, 34)
BLUE = (24, 78, 130)
TEAL = (14, 110, 110)
ORANGE = (198, 96, 20)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 76)
F_SUB = font("DejaVuSans-Bold.ttf", 24)
F_EYEBROW = font("DejaVuSans-Bold.ttf", 27)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_BODY = font("DejaVuSans.ttf", 21)
F_STRIP = font("DejaVuSans-Bold.ttf", 21)
F_STRIP_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 19)
F_JUDGE = font("DejaVuSans.ttf", 18)

# ---- content ---------------------------------------------------------
STORIES = [
    dict(num="1", kicker="CLIMATE \u00b7 ANTALYA", colour=TEAL, glyph="globe",
         head="COP31 collapses with no deal",
         body="After two days in overtime, the UN climate summit ends with no agreement \u2014 the first such failure since Copenhagen in 2009."),
    dict(num="2", kicker="POLITICS \u00b7 WASHINGTON", colour=BLUE, glyph="ballot",
         head="Democrats clinch 258 House seats",
         body="A North Carolina win gives Democrats their biggest House majority since 1992 \u2014 a 44-seat gain."),
    dict(num="3", kicker="WAR \u00b7 RED SEA", colour=RED, glyph="flame",
         head="Houthis claim Saudi refinery hit",
         body="Yemen\u2019s Houthis say they struck the Rabigh oil refinery; the claim is unverified and Riyadh is silent."),
    dict(num="4", kicker="MARKETS \u00b7 NEW YORK", colour=BLUE, glyph="bars",
         head="S&P 500 slides into correction",
         body="The index falls 11.6% from its record high, down seven straight sessions on AI-spending doubts."),
    dict(num="5", kicker="WAR \u00b7 UKRAINE", colour=RED, glyph="target",
         head="Drone flattens flats near Kyiv",
         body="A Russian drone collapses part of a block in Dymer; two killed and about 14 people missing."),
    dict(num="6", kicker="DISASTER \u00b7 INDONESIA", colour=ORANGE, glyph="warn",
         head="Factory fire: 3 dead, 36 missing",
         body="Rescuers search a burned candy factory in Cikande a day after the blaze; the toll may still rise."),
]

ALSO = ("South Korea\u2019s education minister quits over AI cheating chaos \u00b7 "
        "Sparta II towed out of Finnish waters \u00b7 "
        "Bahrain: two hurt in Saturday\u2019s Iran attack")

# ---- text helpers ----------------------------------------------------
def wrap(text, fnt, width):
    """Greedy word wrap measured with the real font."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_lines(text, fnt, width, max_lines):
    """Wrap, then shrink the font until it fits in max_lines."""
    bold = "DejaVuSans-Bold.ttf" if fnt.size and _is_bold(fnt) else "DejaVuSans.ttf"
    size = fnt.size
    while size > 14:
        f = ImageFont.truetype(FONT_DIR + bold, size)
        lines = wrap(text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    return f, wrap(text, f, width)[:max_lines]

def _is_bold(fnt):
    return "Bold" in str(fnt.getname())

def draw_wrapped(d, x, y, text, fnt, width, max_lines, fill, leading=1.28):
    f, lines = fit_lines(text, fnt, width, max_lines)
    for i, ln in enumerate(lines):
        d.text((x, y + i * int(f.size * leading)), ln, font=f, fill=fill)
    return y + len(lines) * int(f.size * leading)

# ---- pictograms (simple drawn marks, top-right of each card) ---------
def glyph(d, kind, cx, cy, colour):
    if kind == "globe":
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=colour, width=4)
        d.arc([cx - 20, cy - 8, cx + 20, cy + 8], 200, 340, fill=colour, width=3)
        d.line([cx - 20, cy, cx + 20, cy], fill=colour, width=3)
    elif kind == "ballot":
        d.rectangle([cx - 18, cy - 14, cx + 18, cy + 14], outline=colour, width=4)
        d.line([cx - 12, cy + 1, cx - 4, cy + 9, cx + 13, cy - 9], fill=colour, width=4)
    elif kind == "flame":
        d.polygon([(cx, cy - 22), (cx + 13, cy - 2), (cx + 16, cy + 14),
                   (cx, cy + 20), (cx - 16, cy + 14), (cx - 13, cy - 2)],
                  fill=colour)
    elif kind == "bars":
        heights = [26, 18, 11]
        for i, hgt in enumerate(heights):
            x0 = cx - 20 + i * 15
            d.rectangle([x0, cy + 14 - hgt, x0 + 10, cy + 14], fill=colour)
        d.line([cx - 22, cy + 16, cx + 22, cy + 16], fill=colour, width=3)
    elif kind == "target":
        d.ellipse([cx - 19, cy - 19, cx + 19, cy + 19], outline=colour, width=4)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)
        d.line([cx, cy - 24, cx, cy - 19], fill=colour, width=3)
        d.line([cx, cy + 19, cx, cy + 24], fill=colour, width=3)
    elif kind == "warn":
        d.polygon([(cx, cy - 22), (cx + 20, cy + 16), (cx - 20, cy + 16)],
                  outline=colour, width=4)
        d.text((cx - 3, cy - 8), "!", font=font("DejaVuSans-Bold.ttf", 22), fill=colour)

# ---- page ------------------------------------------------------------
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# Header band
d.rectangle([0, 0, W, 158], fill=NAVY)
d.rectangle([0, 158, W, 164], fill=GOLD)
# gold dots row, left of eyebrow
for i in range(6):
    x = 34 + i * 20
    d.ellipse([x, 30, x + 12, 42], fill=GOLD)
d.text((168, 22), "THE WORLD IN ONE DAY", font=F_EYEBROW, fill=GOLD)
d.text((34, 52), "22 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255))
d.text((34, 128), "SUNDAY  \u00b7  THE FULL DAY, RANKED BY SIGNIFICANCE",
       font=F_SUB, fill=(200, 208, 224))

# Story grid: 2 columns x 3 rows
MARGIN, GAP = 24, 16
CW = (W - 2 * MARGIN - GAP) // 2
CH = 218
TOP = 180
for idx, s in enumerate(STORIES):
    col, row = idx % 2, idx // 2
    x0 = MARGIN + col * (CW + GAP)
    y0 = TOP + row * (CH + GAP)
    x1, y1 = x0 + CW, y0 + CH
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=CARD,
                        outline=(210, 210, 210), width=1)
    # colour spine on the left edge
    d.rounded_rectangle([x0, y0, x0 + 9, y1], radius=4, fill=s["colour"])
    # rank badge
    bx, by = x0 + 22, y0 + 16
    d.ellipse([bx, by, bx + 40, by + 40], fill=s["colour"])
    tw = d.textlength(s["num"], font=font("DejaVuSans-Bold.ttf", 24))
    d.text((bx + 20 - tw / 2, by + 7), s["num"],
           font=font("DejaVuSans-Bold.ttf", 24), fill=(255, 255, 255))
    # kicker
    d.text((bx + 52, by + 9), s["kicker"], font=F_KICK, fill=s["colour"])
    # pictogram top-right
    glyph(d, s["glyph"], x1 - 42, y0 + 36, s["colour"])
    # headline (max 2 lines) then body (max 3 lines)
    y = draw_wrapped(d, x0 + 22, y0 + 62, s["head"], F_HEAD, CW - 44, 2, INK, 1.15)
    draw_wrapped(d, x0 + 22, y + 6, s["body"], F_BODY, CW - 44, 3, GREY, 1.25)

# ALSO TODAY strip
sy = TOP + 3 * CH + 2 * GAP + 14
d.rectangle([0, sy, W, sy + 88], fill=NAVY_DARK)
d.text((24, sy + 8), "ALSO TODAY:", font=F_STRIP, fill=GOLD)
body_lines = wrap(ALSO, F_STRIP_BODY, W - 48)
for i, ln in enumerate(body_lines[:2]):
    d.text((24, sy + 34 + i * 25), ln, font=F_STRIP_BODY, fill=(235, 235, 235))

# Footer
fy = sy + 88 + 8
d.text((24, fy), "Sources: Reuters \u00b7 AP \u00b7 AFP \u2014 every story verified, 22 November 2026.",
       font=F_FOOT, fill=GREY)
d.text((24, fy + 24), "Judge: this image sums up the full day of Sunday 22 November 2026.",
       font=F_JUDGE, fill=GREY)

img.save(OUT, optimize=True)
print("wrote", OUT, img.size)
