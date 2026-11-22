#!/usr/bin/env python3
"""Render the THE WORLD TODAY front page for Saturday 21 November 2026.

Draws a professional newspaper front page (1024x1024 PNG) summing up the
day's world news: lead story with drawn artwork, a grid of secondary
stories, a numbers box and an IN BRIEF ticker. Original artwork only,
drawn with Pillow primitives; deterministic (fixed seed).
"""

import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36

PAPER = (248, 244, 236)
INK = (20, 22, 26)
RED = (179, 18, 46)
NAVY = (22, 40, 63)
GRAY = (74, 74, 68)
GOLD = (176, 124, 22)
GREEN = (28, 110, 66)
TEAL = (18, 96, 120)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- artwork
def lead_artwork(w, h):
    """Night skyline under missile fire, drawn from primitives."""
    rnd = random.Random(20261121)
    art = Image.new("RGB", (w, h), (16, 18, 38))
    d = ImageDraw.Draw(art, "RGBA")

    # sky gradient
    for yy in range(h):
        t = yy / h
        r = int(14 + 26 * t)
        g = int(16 + 14 * t)
        b = int(40 + 18 * (1 - t))
        d.line([(0, yy), (w, yy)], fill=(r, g, b))

    # stars
    for _ in range(90):
        sx, sy = rnd.uniform(0, w), rnd.uniform(0, h * 0.55)
        s = rnd.uniform(0.6, 1.8)
        d.ellipse([sx, sy, sx + s, sy + s], fill=(230, 232, 245, 200))

    # moon
    d.ellipse([w - 92, 18, w - 52, 58], fill=(232, 230, 214))
    d.ellipse([w - 80, 14, w - 44, 50], fill=(20, 22, 44))

    # missile arcs (two incoming trails with glowing heads)
    for (x0, y0, cx, cy, x1, y1) in [
        (40, 6, 210, 26, 400, 122),
        (330, 2, 470, 22, 560, 106),
    ]:
        pts = []
        for i in range(41):
            t = i / 40
            px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
            py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
            pts.append((px, py))
        d.line(pts, fill=(255, 196, 90, 120), width=3)
        d.line(pts[-9:], fill=(255, 150, 60, 230), width=4)
        hx, hy = pts[-1]
        d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(255, 214, 130))

    # skyline blocks
    base = h
    buildings = [
        (0, 80, 88), (84, 114, 70), (150, 86, 96), (242, 128, 74),
        (312, 98, 92), (400, 138, 66), (462, 104, 84), (542, 122, 62),
    ]
    for bx, bh, bw in buildings:
        top = base - bh
        d.rectangle([bx, top, bx + bw, base], fill=(10, 11, 22))
        # lit windows
        for wy in range(top + 10, base - 12, 16):
            for wx in range(bx + 8, bx + bw - 10, 15):
                if rnd.random() < 0.42:
                    d.rectangle([wx, wy, wx + 6, wy + 8],
                                fill=(255, 204, 110, 235))

    # struck building: irregular fireball in its upper floors
    fx, fy = 433, base - 112
    for _ in range(16):
        ox = fx + rnd.uniform(-26, 26)
        oy = fy + rnd.uniform(-16, 16)
        rr = rnd.uniform(8, 22)
        col = rnd.choice([(255, 110, 30), (255, 140, 45), (255, 170, 70),
                          (240, 90, 25)])
        d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], fill=col + (200,))
    d.ellipse([fx - 9, fy - 9, fx + 9, fy + 9], fill=(255, 232, 170))
    # flames licking from the roofline
    for i in range(6):
        lx = fx - 27 + i * 11
        d.polygon([(lx, base - 138), (lx + 5, base - 156 - (i % 2) * 7),
                   (lx + 10, base - 138)], fill=(255, 140, 50, 230))
    # smoke plume drifting up
    for i in range(6):
        sx = fx + rnd.uniform(-10, 26) + i * 4
        sy = fy - 36 - i * 13
        sr = 9 + i * 4
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                  fill=(74, 72, 84, 85))

    # rescue lights at street level
    for lx, col in [(150, (255, 60, 60)), (176, (90, 140, 255)),
                    (470, (255, 60, 60)), (496, (90, 140, 255))]:
        d.ellipse([lx - 9, base - 16, lx + 9, base - 4], fill=col + (90,))
        d.ellipse([lx - 3, base - 13, lx + 3, base - 7], fill=col)

    return art


# ------------------------------------------------------------------ icons
def icon_thermo(d, x, y, col):
    d.rounded_rectangle([x + 6, y, x + 14, y + 22], radius=4, outline=col, width=3)
    d.ellipse([x + 3, y + 18, x + 17, y + 32], outline=col, width=3)
    d.ellipse([x + 7, y + 22, x + 13, y + 28], fill=col)
    d.line([(x + 10, y + 24), (x + 10, y + 8)], fill=col, width=3)


def icon_chart_down(d, x, y, col):
    d.line([(x, y + 26), (x, y)], fill=col, width=3)
    d.line([(x, y + 26), (x + 24, y + 26)], fill=col, width=3)
    d.line([(x + 3, y + 6), (x + 10, y + 12), (x + 15, y + 9),
            (x + 22, y + 20)], fill=col, width=3)
    d.polygon([(x + 22, y + 20), (x + 15, y + 19), (x + 21, y + 13)], fill=col)


def icon_shield(d, x, y, col):
    d.polygon([(x + 12, y), (x + 23, y + 4), (x + 23, y + 15),
               (x + 12, y + 28), (x + 1, y + 15), (x + 1, y + 4)],
              outline=col, width=3)
    d.line([(x + 7, y + 14), (x + 11, y + 19), (x + 18, y + 9)],
           fill=col, width=3)


def icon_globe(d, x, y, col):
    d.ellipse([x, y, x + 26, y + 26], outline=col, width=3)
    d.ellipse([x + 8, y, x + 18, y + 26], outline=col, width=2)
    d.line([(x, y + 13), (x + 26, y + 13)], fill=col, width=2)


def icon_scales(d, x, y, col):
    d.line([(x + 13, y), (x + 13, y + 24)], fill=col, width=3)
    d.line([(x + 2, y + 5), (x + 24, y + 5)], fill=col, width=3)
    d.line([(x + 7, y + 26), (x + 19, y + 26)], fill=col, width=3)
    for cx in (x + 2, x + 24):
        d.line([(cx, y + 5), (cx - 5, y + 14)], fill=col, width=2)
        d.line([(cx, y + 5), (cx + 5, y + 14)], fill=col, width=2)
        d.arc([cx - 6, y + 9, cx + 6, y + 19], start=0, end=180, fill=col, width=2)


def icon_cross(d, x, y, col):
    d.rounded_rectangle([x + 1, y + 1, x + 25, y + 25], radius=4,
                        outline=col, width=3)
    d.line([(x + 13, y + 6), (x + 13, y + 20)], fill=col, width=4)
    d.line([(x + 6, y + 13), (x + 20, y + 13)], fill=col, width=4)


def icon_ball(d, x, y, col):
    d.ellipse([x, y, x + 26, y + 26], outline=col, width=3)
    d.arc([x - 8, y + 2, x + 10, y + 24], start=290, end=70, fill=col, width=2)
    d.arc([x + 16, y + 2, x + 34, y + 24], start=110, end=250, fill=col, width=2)


def icon_doc(d, x, y, col):
    d.polygon([(x + 4, y), (x + 17, y), (x + 23, y + 6), (x + 23, y + 27),
               (x + 4, y + 27)], outline=col, width=3)
    d.line([(x + 17, y), (x + 17, y + 6), (x + 23, y + 6)], fill=col, width=2)
    for ly in (y + 12, y + 17, y + 22):
        d.line([(x + 8, ly), (x + 19, ly)], fill=col, width=2)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # top bar
    f_top = font(SANS_B, 16)
    d.text((MARGIN, 24), "SATURDAY, 21 NOVEMBER 2026", font=f_top, fill=INK)
    right = "WORLD EDITION"
    d.text((W - MARGIN - text_w(d, right, f_top), 24), right,
           font=f_top, fill=INK)
    hline(d, MARGIN, W - MARGIN, 50, width=2)

    # masthead
    f_mast = font(SERIF_B, 80)
    mast = "THE WORLD TODAY"
    mw = text_w(d, mast, f_mast)
    d.text(((W - mw) / 2, 56), mast, font=f_mast, fill=INK)

    # red date badge with flanking rules
    f_badge = font(SANS_B, 21)
    badge = "21 NOV 2026"
    bw = text_w(d, badge, f_badge) + 36
    bx = (W - bw) / 2
    by = 150
    hline(d, MARGIN, bx - 14, by + 16, width=2)
    hline(d, bx + bw + 14, W - MARGIN, by + 16, width=2)
    d.rounded_rectangle([bx, by, bx + bw, by + 32], radius=6, fill=RED)
    d.text((bx + 18, by + 4), badge, font=f_badge, fill=(255, 255, 255))

    # double rule
    hline(d, MARGIN, W - MARGIN, 194, width=3)
    hline(d, MARGIN, W - MARGIN, 201, width=1)

    # lead kicker + headline
    f_kick = font(SANS_B, 18)
    d.text((MARGIN, 212), "EUROPE  •  WAR IN UKRAINE", font=f_kick, fill=RED)
    f_lead = font(SERIF_B, 44)
    lead_lines = ["DOUBLE-TAP STRIKE ON ZELENSKYY'S",
                  "HOMETOWN KILLS 2, WOUNDS 60"]
    y = 238
    for line in lead_lines:
        d.text((MARGIN, y), line, font=f_lead, fill=INK)
        y += 50

    # lead artwork + right rail
    art = lead_artwork(604, 150)
    img.paste(art, (MARGIN, 340))
    d.rectangle([MARGIN, 340, MARGIN + 604, 340 + 150], outline=INK, width=1)
    f_cap = font(SANS_R, 13)
    d.text((MARGIN, 496),
           "Kryvyi Rih under fire: a second wave of missiles hit rescuers "
           "at the scene.", font=f_cap, fill=GRAY)

    rail_x = MARGIN + 620
    rail_w = W - MARGIN - rail_x
    f_body = font(SERIF_R, 16)
    body = ("Ballistic missiles struck Kryvyi Rih on Friday night, "
            "killing a 7-year-old boy and a 20-year-old woman. Three "
            "more rockets then hit doctors and rescue crews; 25 "
            "buildings were damaged. Kyiv said 148 drones were "
            "launched overnight, 117 of them shot down.")
    yy = draw_lines(d, wrap(d, body, f_body, rail_w), rail_x, 340,
                    f_body, INK, 21)
    yy += 4
    f_chip = font(SANS_B, 14)
    chip_rows = [["2 KILLED", "60 WOUNDED"], ["25 BUILDINGS HIT"]]
    for row in chip_rows:
        cx = rail_x
        for chip in row:
            cw = text_w(d, chip, f_chip) + 18
            d.rounded_rectangle([cx, yy, cx + cw, yy + 24],
                                radius=5, outline=RED, width=2)
            d.text((cx + 9, yy + 3), chip, font=f_chip, fill=RED)
            cx += cw + 10
        yy += 30

    # markets strip
    hline(d, MARGIN, W - MARGIN, 526, width=2)
    f_mkt_lab = font(SANS_B, 13)
    f_mkt = font(SANS_R, 13)
    d.text((MARGIN, 533), "MARKETS", font=f_mkt_lab, fill=RED)
    mkt = ("S&P 500 6,910 ▼3.70%    NIKKEI ▼5.06%    FTSE 100 10,346 "
           "▼1.02%    BOVESPA ▼0.69%    BRENT $89.95 ▲0.57%    "
           "NAT GAS 3.75 ▲1.82%")
    d.text((MARGIN + 78, 533), mkt, font=f_mkt, fill=INK)
    hline(d, MARGIN, W - MARGIN, 556, width=2)

    # secondary grid: 3 columns x 3 rows (8 stories + numbers box)
    stories = [
        (icon_thermo, GOLD, "CLIMATE",
         "COP31 TALKS RUN INTO OVERTIME, STILL NO DEAL",
         "Antalya summit misses its Friday deadline; draft drops "
         "fossil-fuel language as UN warns 1.5°C will likely be "
         "overshot."),
        (icon_chart_down, RED, "MARKETS",
         "CHIP ROUT: NVIDIA −14%, NASDAQ ERASES 2026 GAINS",
         "S&P 500 falls 3.7% to 6,910 as the AI sell-off spreads; "
         "VIX jumps 26% to 35.9, traders price 91% odds of a "
         "December Fed hike."),
        (icon_shield, GREEN, "AMERICAS",
         "MEXICO CAPTURES 'EL CHAPO ISIDRO', FBI MOST-WANTED",
         "Fausto Isidro Meza Flores seized in Guasave, Sinaloa with "
         "US intel help; flown to Mexico City as violence follows "
         "the arrest."),
        (icon_globe, TEAL, "EUROPE",
         "UK AND EU SEAL POST-BREXIT RESET AT BRUSSELS",
         "Food trade, linked emissions trading and youth mobility "
         "for 100,000 people a year each way agreed at the Brussels "
         "summit."),
        (icon_scales, NAVY, "ASIA • WORLD COURT",
         "COURT: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
         "Landmark 9–6 ICJ judgment orders reparations; Bangladesh "
         "vows to act on compensation and Türkiye welcomes the "
         "verdict."),
        (icon_cross, GREEN, "HEALTH",
         "BACTERIUM MOSQUITOES CUT DENGUE CASES BY 69%",
         "Brazilian researchers report mosquitoes carrying a "
         "bacterium slashed dengue infections by 69% in trial "
         "areas."),
        (icon_ball, RED, "SPORT",
         "ALCARAZ EDGES SHELTON TO SET UP ZVEREV FINAL",
         "The Spaniard wins 3–6 6–3 7–6(1) in Turin despite a thigh "
         "scare; Zverev beat Medvedev 7–6 6–4 in the other "
         "semi-final."),
        (icon_doc, TEAL, "ASIA • TRADE",
         "EU–INDONESIA PACT SEALED AFTER 10 YEARS OF TALKS",
         "Brussels and Jakarta close a decade of negotiations, "
         "sealing a trade agreement between the EU and Indonesia."),
    ]
    col_w = 308
    col_xs = [MARGIN, MARGIN + col_w + 14, MARGIN + 2 * (col_w + 14)]
    f_skick = font(SANS_B, 15)
    f_shead = font(SERIF_B, 18)
    f_sbody = font(SANS_R, 13)
    row_ys = [566, 684, 802]
    for i, (icon, col, kick, head, body_s) in enumerate(stories):
        cx = col_xs[i % 3]
        cy = row_ys[i // 3]
        icon(d, cx, cy, col)
        d.text((cx + 34, cy + 4), kick, font=f_skick, fill=col)
        hy = draw_lines(d, wrap(d, head, f_shead, col_w), cx, cy + 30,
                        f_shead, INK, 21)
        draw_lines(d, wrap(d, body_s, f_sbody, col_w), cx, hy + 1,
                   f_sbody, GRAY, 15)

    # day in numbers box (9th cell): 8 figures in 2 columns
    nx, ny = col_xs[2], row_ys[2]
    d.text((nx, ny + 4), "THE DAY IN NUMBERS", font=f_skick, fill=GOLD)
    f_num = font(SERIF_B, 19)
    f_nlab = font(SANS_R, 11)
    numbers = [("60", "wounded, Kryvyi Rih"),
               ("148", "drones at Ukraine"),
               ("−3.7%", "S&P 500 Friday"),
               ("35.9", "VIX gauge, +26%"),
               ("69%", "dengue cut, Brazil"),
               ("9–6", "ICJ Myanmar vote"),
               ("100k", "UK–EU youth/yr"),
               ("700k", "displaced, Ethiopia")]
    for j, (num, lab) in enumerate(numbers):
        fx = nx + (j % 2) * 158
        fy = ny + 30 + (j // 2) * 21
        d.text((fx, fy), num, font=f_num, fill=INK)
        d.text((fx + text_w(d, num, f_num) + 6, fy + 5), lab,
               font=f_nlab, fill=GRAY)

    # IN BRIEF ticker band
    band_y = 920
    d.rectangle([MARGIN, band_y, W - MARGIN, band_y + 72], fill=NAVY)
    f_tlab = font(SANS_B, 14)
    d.text((MARGIN + 14, band_y + 6), "IN BRIEF", font=f_tlab,
           fill=(255, 209, 102))
    f_tick = font(SANS_R, 13)
    tick = ("Trump tells Europe to defund Ukraine after Putin summit  •  "
            "Anthropic debuts on Wall Street at ~$2 trillion  •  "
            "Houthis strike Saudi capital; 71 Saudi airstrikes hit 8 "
            "Yemen regions  •  "
            "Israeli fire kills 3 aid workers in Gaza  •  "
            "Chelsea humiliated 4–1 by Leeds at Stamford Bridge  •  "
            "BepiColombo arrives at Mercury  •  "
            "FBI crime database suffers suspected breach  •  "
            "Bitcoin bounces 9% to retake $60,000")
    draw_lines(d, wrap(d, tick, f_tick, W - 2 * MARGIN - 28),
               MARGIN + 14, band_y + 25, f_tick, (255, 255, 255), 15)

    # footer
    f_foot = font(SANS_R, 12)
    foot = ("THE WORLD TODAY  •  Saturday 21 November 2026  •  "
            "The day's world news on one page")
    d.text(((W - text_w(d, foot, f_foot)) / 2, H - 20), foot,
           font=f_foot, fill=GRAY)

    img.save("entry.png", "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
