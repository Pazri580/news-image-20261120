#!/usr/bin/env python3
"""Paint the 20 November 2026 world-news front page for make.fun.

Builds one 1024x1024 PNG with Pillow and saves it as entry.png beside
this file. Nothing moves between runs: fixed geometry, fixed colours,
fixed fonts and fixed words, no clock, no random numbers, no network,
so the bytes are identical every time. The grading sandbox only ever
runs main.py, which copies this finished picture; this file is the
workshop step that produces it.

The page is laid out top-down: masthead, dateline, then a lead story,
two rows of two stories each, and a ticker bar at the foot. Each block
is measured before it is drawn, so nothing ever overlaps the block
below it.

The five stories, all first reported on Friday 20 November 2026:
  1. LEAD — Russia fires 110+ missiles at Ukraine overnight into
     Friday, the biggest attack of the year; nine killed, at least 28
     hurt in Kyiv; the Austrian and Dutch embassies damaged.
  2. MARKETS — Tokyo's Nikkei falls 4.8% and the S&P 500 drops 2%,
     its fifth straight day of losses, as investors doubt AI
     valuations after Anthropic's Nasdaq debut.
  3. BRUSSELS — The EU and the UK hold their second summit since
     their renewed partnership began; Costa and von der Leyen meet
     Prime Minister Burnham.
  4. HORMUZ — A tanker catches fire after hitting a mine in the
     Strait of Hormuz as attacks on shipping intensify and the Iran
     war enters its ninth month.
  5. ANTALYA — The COP31 draft drops any call to phase out fossil
     fuels; negotiators strip the reference from the slimmed-down deal.
Ticker: Trump on Putin; Israeli troops cross the Gaza Yellow Line;
Italy fines Meta 805 million euros; FAA ground stop strands 1.5M
travellers; Estonia to shut its border with Russia.
"""

import os
from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
MARGIN = 36
PAPER = (250, 248, 240)
INK = (18, 18, 18)
RED = (176, 32, 28)
BLUE = (28, 64, 140)
GREY = (110, 108, 100)
NIGHT = (16, 24, 48)
EMBER = (230, 120, 30)
PALE = (232, 228, 218)

FONTS = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def serif_b(size):
    return load("DejaVuSerif-Bold.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def split_lines(d, text, fnt, width):
    """Greedy wrap: longest prefix of words that fits `width` pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_height(d, text, fnt, width, gap=1.32):
    return len(split_lines(d, text, fnt, width)) * int(fnt.size * gap)


def write_block(d, x, y, width, text, fnt, fill=INK, gap=1.32):
    """Draw a wrapped paragraph; hand back the y just under it."""
    for line in split_lines(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * gap)
    return y


def tag(d, x, y, text):
    d.text((x, y), text, font=sans_b(17), fill=RED)
    return y + 24


def headline(d, x, y, width, text, size=32):
    return write_block(d, x, y, width, text, serif_b(size), gap=1.12)


def rule(d, y, weight=2, colour=INK):
    d.line([(MARGIN, y), (SIDE - MARGIN, y)], fill=colour, width=weight)
    return y + 10


def kyiv_night(d, x, y, w, h):
    """Night skyline over Kyiv: dark sky, lit windows, missile streaks."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(28, 18), (90, 42), (150, 14), (210, 36), (280, 20),
                   (330, 48), (60, 70), (190, 64), (250, 80), (320, 12)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(240, 240, 220))
    for (x0, y0, x1, y1) in [(40, 30, 120, 110), (200, 18, 260, 96), (300, 44, 330, 108)]:
        d.line([(x + x0, y + y0), (x + x1, y + y1)], fill=(255, 255, 255), width=3)
        d.ellipse([x + x1 - 5, y + y1 - 5, x + x1 + 5, y + y1 + 5], fill=EMBER)
    for (cx, cy, r) in [(120, 116, 16), (262, 102, 13), (330, 114, 10)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=EMBER)
        d.ellipse([x + cx - r // 2, y + cy - r // 2, x + cx + r // 2, y + cy + r // 2],
                  fill=(255, 200, 60))
    base = y + h
    tops = [150, 120, 165, 135, 175, 145, 160, 125, 170, 140, 155, 130]
    bw = w // len(tops)
    for i, top in enumerate(tops):
        bx = x + i * bw
        d.rectangle([bx, base - top, bx + bw - 3, base], fill=(8, 10, 22))
        for wy in range(base - top + 12, base - 10, 22):
            if (i * 7 + wy) % 3 == 0:
                d.rectangle([bx + 4, wy, bx + 9, wy + 7], fill=(255, 210, 90))


def market_bars(d, x, y, w):
    """Two horizontal bars: Nikkei -4.8% (red) and S&P 500 -2.0% (grey)."""
    rows = [("NIKKEI", "-4.8%", 4.8, RED), ("S&P 500", "-2.0%", 2.0, (90, 88, 80))]
    yy = y
    for name, val, mag, colour in rows:
        d.text((x, yy), name, font=sans_b(16), fill=INK)
        bx = x + 92
        bar = int(mag / 5.0 * (w - 160))
        d.rectangle([bx, yy + 2, bx + bar, yy + 14], fill=colour)
        d.text((bx + bar + 8, yy), val, font=sans_b(16), fill=colour)
        yy += 24
    return yy


def summit_discs(d, x, y, r=24):
    """Two overlapping discs: EU blue and UK red."""
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=BLUE)
    d.text((x + r - 14, y + r - 13), "EU", font=sans_b(24), fill=(255, 255, 255))
    d.ellipse([x + 46, y + 18, x + 46 + 2 * r, y + 18 + 2 * r], fill=(178, 34, 34))
    d.text((x + 46 + r - 14, y + 18 + r - 13), "UK", font=sans_b(24), fill=(255, 255, 255))
    d.ellipse([x + 46, y + 18, x + 46 + 2 * r, y + 18 + 2 * r],
              outline=(255, 255, 255), width=3)
    return y + 18 + 2 * r


def tanker(d, x, y, w):
    """A tanker hull with containers, flames and smoke above it."""
    d.rectangle([x, y + 28, x + w, y + 46], fill=(40, 40, 44))
    d.rectangle([x + w - 40, y + 16, x + w - 8, y + 28], fill=(40, 40, 44))
    for i, c in enumerate([(176, 32, 28), (28, 64, 140), (200, 160, 40)]):
        d.rectangle([x + 10 + i * 36, y + 8, x + 40 + i * 36, y + 28], fill=c)
    for fx in [20, 50, 82]:
        d.polygon([(x + fx, y + 8), (x + fx + 8, y - 10), (x + fx + 16, y + 8)],
                  fill=EMBER)
    for sx, sy in [(24, -18), (56, -22), (88, -20)]:
        d.ellipse([x + sx, y + sy, x + sx + 10, y + sy + 10], fill=(150, 148, 140))
    return y + 46


def draft_doc(d, x, y, w, h):
    """A draft document with FOSSIL FUELS struck through in red."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    d.text((x + 12, y + 7), "COP31 DRAFT", font=sans_b(14), fill=INK)
    d.text((x + 12, y + 28), "FOSSIL FUELS", font=sans_b(18), fill=INK)
    d.line([(x + 9, y + 39), (x + w - 9, y + 39)], fill=RED, width=4)
    for i in range(3):
        d.line([(x + 12, y + 50 + i * 10), (x + w - 24 - i * 18, y + 50 + i * 10)],
               fill=GREY, width=3)
    return y + h


def story(d, x, y, width, kicker, head, body, head_size=30, body_size=17,
          head_width=None):
    """One story column: kicker, headline, body. Returns the y below it.

    `head_width` lets a side graphic share the headline's row: the
    headline wraps in `head_width` while the body keeps the full width.
    """
    y = tag(d, x, y, kicker)
    y = headline(d, x, y + 4, head_width or width, head, size=head_size)
    y = write_block(d, x, y + 6, width, body, sans(body_size))
    return y


def main():
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(img)
    col_w = 458
    rx = SIDE - MARGIN - col_w

    # Masthead
    title = "THE WORLD IN ONE PAGE"
    d.text(((SIDE - d.textlength(title, font=serif_b(60))) / 2, 16),
           title, font=serif_b(60), fill=INK)
    d.line([(MARGIN, 98), (SIDE - MARGIN, 98)], fill=INK, width=5)

    # Dateline
    d.text((MARGIN, 112), "FRIDAY, 20 NOVEMBER 2026", font=sans_b(20), fill=INK)
    right = "ONE IMAGE  ·  FIVE STORIES"
    d.text((SIDE - MARGIN - d.textlength(right, font=sans_b(20)), 112),
           right, font=sans_b(20), fill=GREY)
    y = rule(d, 144) + 6

    # ---- LEAD: Kyiv (text left, night panel right) ----
    lead_top = y
    y = tag(d, MARGIN, y, "KYIV  ·  UKRAINE")
    y = headline(d, MARGIN, y + 4, 556, "Russia's biggest missile attack of the year", size=38)
    y = write_block(d, MARGIN, y + 8, 556,
                    "Russia fired more than 110 missiles at Ukraine overnight "
                    "into Friday \u2014 the biggest attack of the year, President "
                    "Zelenskyy said. Nine were killed and at least 28 hurt in Kyiv.",
                    sans(20))
    lead_bottom = y
    panel_h = lead_bottom - lead_top - 28
    kyiv_night(d, 628, lead_top, 360, panel_h)
    d.text((628, lead_bottom - 22), "9 KILLED  ·  28 HURT  ·  EMBASSIES DAMAGED",
           font=sans_b(14), fill=GREY)
    y = rule(d, lead_bottom + 10) + 4

    # ---- Middle row: markets (left) + Brussels (right) ----
    row_top = y
    y_left = story(d, MARGIN, row_top, col_w, "MARKETS",
                   "Stocks slide as AI doubts spread",
                   "Tokyo's Nikkei fell 4.8% and the S&P 500 dropped 2% \u2014 "
                   "its fifth straight day of losses \u2014 as investors doubted "
                   "AI valuations after Anthropic's Nasdaq debut.",
                   head_size=30, body_size=17)
    y_left = market_bars(d, MARGIN, y_left + 10, col_w)
    summit_discs(d, rx + 318, row_top + 26)
    y_right = story(d, rx, row_top, col_w, "BRUSSELS",
                    "EU and UK meet in Brussels",
                    "The European Union and the United Kingdom held their second "
                    "summit since their renewed partnership began. Costa and "
                    "von der Leyen met Prime Minister Burnham.",
                    head_size=30, body_size=17, head_width=296)
    y = rule(d, max(y_left, y_right) + 10) + 4

    # ---- Bottom row: Hormuz (left) + COP31 (right) ----
    row_top = y
    tanker(d, MARGIN + 300, row_top + 24, 150)
    y_left = story(d, MARGIN, row_top, col_w, "STRAIT OF HORMUZ",
                   "Tanker on fire after mine strike",
                   "A tanker caught fire after hitting a mine in the Strait of "
                   "Hormuz, as attacks on shipping intensify and the Iran war "
                   "enters its ninth month.",
                   head_size=28, body_size=17, head_width=288)
    draft_doc(d, rx + 292, row_top + 22, 160, 66)
    y_right = story(d, rx, row_top, col_w, "ANTALYA  ·  COP31",
                    "COP31 draft drops fossil-fuel phase-out",
                    "Negotiators removed any reference to ending fossil fuel use "
                    "from the slimmed-down draft deal at the climate talks in "
                    "Antalya, Turkey.",
                    head_size=28, body_size=17, head_width=280)
    y = max(y_left, y_right)

    # ---- Ticker (anchored to the foot) ----
    d.rectangle([0, 922, SIDE, SIDE], fill=INK)
    write_block(d, MARGIN, 934, SIDE - 2 * MARGIN,
                "ALSO TODAY \u2014  Trump: Putin is \u2018tired\u2019 and ready for a deal  ·  "
                "Israeli troops cross the Gaza Yellow Line  ·  Italy fines Meta \u20ac805M  ·  "
                "FAA ground stop strands 1.5M travellers  ·  Estonia to shut its Russia border",
                sans_b(18), fill=(255, 255, 255), gap=1.5)
    print("content ends at y =", y, "(ticker starts at 922)")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
