#!/usr/bin/env python3
"""The World Today: a newspaper front page summing up Friday 20 November 2026.

Draws one 1024x1024 PNG to /output/entry.png with pure procedural PIL art.
No network, no randomness, no clock: two runs produce identical bytes.

Stories (all reported on 20 Nov 2026):
  1. GTA VI takes $3.79bn on day one - biggest entertainment launch ever.
  2. Russia's huge barrage hits Kyiv bridges; three objects (two missiles and a drone) land in Poland.
  3. Trump, Xi and Putin issue a joint peace pledge after Shenzhen talks.
  4. Myanmar rejects the world court's genocide ruling, a day after it.
  5. COP31 climate talks stall in Antalya over fossil fuels.
  6. Anthropic shares slide 9% on day two after the record $2tn debut.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (248, 244, 233)
INK = (24, 24, 24)
RED = (178, 24, 28)
RED_DARK = (140, 16, 20)
GREY = (105, 100, 92)
RULE = (60, 58, 52)
PANEL_BG = (255, 253, 247)
PANEL_LINE = (178, 172, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    import math
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- illustrations

def draw_skyline(d, x, y, w, h):
    """Neon Vice City sunset: banded sky, sun, tower silhouettes, palms."""
    bands = [(255, 94, 150), (255, 140, 90), (255, 190, 90),
             (122, 62, 160), (46, 24, 96)]
    n = len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=col)
    d.ellipse([x + w // 2 - 52, y + 26, x + w // 2 + 52, y + 130],
              fill=(255, 240, 170))
    towers = [(0, 150, 62, 210), (58, 120, 52, 240), (106, 168, 60, 142),
              (162, 96, 54, 264), (212, 140, 58, 196), (266, 112, 56, 252),
              (318, 158, 56, 172)]
    for tx, th, tw, base in towers:
        bx = x + tx
        d.rectangle([bx, y + h - th - 34, bx + tw, y + h - 34],
                    fill=(30, 16, 52))
        for wy in range(y + h - th - 20, y + h - 44, 18):
            for wx in range(bx + 8, bx + tw - 8, 16):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 90))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(18, 10, 38))
    d.rectangle([x, y + h - 34, x + w, y + h - 28], fill=(255, 94, 150))
    # two palm trees
    for px, lean in ((x + 30, -1), (x + w - 34, 1)):
        d.line([px, y + h - 34, px + lean * 14, y + h - 108],
               fill=(16, 40, 20), width=6)
        for k in range(5):
            ang = -70 + k * 32
            import math
            ex = px + lean * 14 + 34 * math.cos(math.radians(ang + 90))
            ey = y + h - 108 + 30 * math.sin(math.radians(ang + 90))
            d.line([px + lean * 14, y + h - 108, ex, ey],
                   fill=(22, 110, 60), width=5)


def draw_bridge(d, x, y, w, h):
    """River, bridge deck and arches, two explosion bursts, smoke.
    All coordinates are relative to the (x, y, w, h) art box."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(84, 128, 158))
    for i in range(3):
        ax0 = x + 8 + i * (w - 16) // 3
        ax1 = x + 8 + (i + 1) * (w - 16) // 3
        d.arc([ax0, y + h - 104, ax1, y + h - 28], 180, 360,
              fill=(70, 70, 78), width=6)
    d.rectangle([x, y + h - 84, x + w, y + h - 72], fill=(52, 52, 60))
    for lx in (x + 26, x + w // 2, x + w - 26):
        d.line([lx, y + h - 84, lx, y + h - 112], fill=(52, 52, 60), width=4)
    starburst(d, x + w * 3 // 10, y + 52, 34, 15, 9, (255, 150, 30))
    starburst(d, x + w * 3 // 10, y + 52, 21, 9, 9, (255, 214, 80))
    starburst(d, x + w * 3 // 4, y + 36, 26, 11, 9, (255, 120, 20))
    starburst(d, x + w * 3 // 4, y + 36, 16, 7, 9, (255, 200, 60))
    for sx, sy, sr in ((x + 14, y + 22, 11), (x + w - 12, y + 14, 9)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 112))


def draw_flags(d, x, y, w, h):
    """Three summit flags side by side: USA, China, Russia."""
    fw = (w - 24) // 3
    # USA
    fx = x
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (245, 245, 240)
        d.rectangle([fx, y + i * h // 7, fx + fw, y + (i + 1) * h // 7],
                    fill=col)
    d.rectangle([fx, y, fx + fw * 2 // 5, y + h * 4 // 7], fill=(32, 48, 96))
    for sy in range(3):
        for sx in range(4):
            d.ellipse([fx + 6 + sx * 12, y + 8 + sy * 16,
                       fx + 11 + sx * 12, y + 13 + sy * 16],
                      fill=(255, 255, 255))
    # China
    fx = x + fw + 12
    d.rectangle([fx, y, fx + fw, y + h], fill=(222, 32, 24))
    starburst(d, fx + 22, y + 24, 13, 5, 5, (255, 222, 40))
    for sx, sy in ((fx + 48, y + 12), (fx + 58, y + 28), (fx + 52, y + 48),
                   (fx + 36, y + 56)):
        starburst(d, sx, sy, 6, 2, 5, (255, 222, 40))
    # Russia
    fx = x + 2 * (fw + 12)
    for i, col in enumerate(((245, 245, 240), (0, 70, 160), (200, 24, 24))):
        d.rectangle([fx, y + i * h // 3, fx + fw, y + (i + 1) * h // 3],
                    fill=col)
    d.rectangle([x, y, x + w, y + h], outline=(90, 84, 72), width=2)


def draw_scales(d, x, y, w, h):
    """Courthouse columns behind the scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.polygon([(x + 12, y + 34), (x + w - 12, y + 34),
               (x + w // 2, y + 6)], fill=(150, 138, 112))
    for cx in (x + 34, x + w // 2 - 8, x + w - 50):
        d.rectangle([cx, y + 40, cx + 16, y + h - 26], fill=(196, 186, 162))
    d.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 18], fill=(150, 138, 112))
    cx = x + w // 2
    d.line([cx, y + 44, cx, y + h - 30], fill=(52, 44, 30), width=6)
    d.line([cx - 44, y + 58, cx + 44, y + 58], fill=(52, 44, 30), width=5)
    d.polygon([(cx - 26, y + 40), (cx + 26, y + 40), (cx, y + 56)],
              fill=(178, 24, 28))
    for sgn in (-1, 1):
        px = cx + sgn * 44
        d.line([px, y + 58, px, y + 88], fill=(52, 44, 30), width=4)
        d.arc([px - 22, y + 82, px + 22, y + 126], 0, 180,
              fill=(52, 44, 30), width=5)
        d.line([px - 22, y + 104, px + 22, y + 104], fill=(52, 44, 30),
               width=4)
    d.rectangle([cx - 34, y + h - 34, cx + 34, y + h - 22], fill=(52, 44, 30))


def draw_climate(d, x, y, w, h):
    """Globe with a leaf and a rising thermometer."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 216, 232))
    cx, cy, r = x + w // 2 - 18, y + h // 2 + 6, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 200))
    d.ellipse([cx - 30, cy - 34, cx + 4, cy - 6], fill=(86, 178, 92))
    d.ellipse([cx - 4, cy + 10, cx + 32, cy + 36], fill=(86, 178, 92))
    d.ellipse([cx + 16, cy - 32, cx + 38, cy - 4], fill=(86, 178, 92))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 330, fill=(255, 255, 255),
          width=3)
    tx = x + w - 22
    d.rounded_rectangle([tx - 6, y + 26, tx + 6, y + h - 34], radius=6,
                        fill=(245, 245, 240), outline=(52, 52, 52), width=2)
    d.ellipse([tx - 11, y + h - 46, tx + 11, y + h - 24], fill=(220, 40, 30),
              outline=(52, 52, 52), width=2)
    d.rectangle([tx - 2, y + 34, tx + 2, y + h - 36], fill=(220, 40, 30))
    for ty in range(y + 34, y + 70, 10):
        d.line([tx + 6, ty, tx + 11, ty], fill=(52, 52, 52), width=2)
    d.ellipse([x + 12, y + 12, x + 32, y + 32], fill=(255, 200, 40))
    for k in range(8):
        import math
        a = math.pi * k / 4
        d.line([x + 22 + 13 * math.cos(a), y + 22 + 13 * math.sin(a),
                x + 22 + 19 * math.cos(a), y + 22 + 19 * math.sin(a)],
               fill=(255, 200, 40), width=3)


def draw_chart(d, x, y, w, h):
    """Share-price line: a steep rise, then a sharp red fall."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    d.line([x + 14, y + 12, x + 14, y + h - 14], fill=(120, 120, 120), width=2)
    d.line([x + 14, y + h - 14, x + w - 8, y + h - 14], fill=(120, 120, 120),
           width=2)
    pts = [(x + 16, y + h - 30), (x + 40, y + h - 44), (x + 62, y + h - 40),
           (x + 84, y + h - 62), (x + 106, y + 22), (x + 122, y + 18),
           (x + 138, y + h - 52), (x + 158, y + h - 34)]
    d.line(pts, fill=(30, 120, 70), width=4, joint="curve")
    d.line(pts[4:], fill=(200, 30, 30), width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(24, 24, 24))
    ax, ay = x + 122, y + 18
    d.polygon([(ax, ay + 26), (ax - 11, ay + 6), (ax - 3, ay + 6),
               (ax - 3, ay - 12), (ax + 3, ay - 12), (ax + 3, ay + 6),
               (ax + 11, ay + 6)], fill=(200, 30, 30))


# ---------------------------------------------------------------- page layout

def story_panel(d, x, y, w, h, kicker, headline, sub, art):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG,
                outline=PANEL_LINE, width=2)
    iw = 150
    art(d, x + 10, y + 10, iw, h - 20)
    d.line([x + 170, y + 10, x + 170, y + h - 10], fill=PANEL_LINE, width=1)
    tx = x + 184
    tw = w - 198
    d.text((tx, y + 12), kicker, font=font(SANS_B, 14), fill=RED)
    # shrink the headline until it fits on two lines, never below 20pt
    size = 27
    while size > 20:
        hl = wrap(d, headline, font(SERIF_B, size), tw)
        if len(hl) <= 2:
            break
        size -= 2
    yy = text_block(d, tx, y + 36, hl[:2], font(SERIF_B, size), INK,
                    size + 5)
    sl = wrap(d, sub, font(SANS, 18), tw)
    text_block(d, tx, yy + 6, sl[:2], font(SANS, 18), (64, 60, 54), 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 86)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    d.line([28, 122, W - 28, 122], fill=RULE, width=3)
    d.line([28, 128, W - 28, 128], fill=RULE, width=1)

    # red date band
    d.rectangle([28, 140, W - 28, 202], fill=RED)
    df = font(SANS_B, 38)
    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 152), date, font=df, fill=(255, 255, 255))

    # lead story: GTA VI
    lx, ly, lw, lh = 28, 218, W - 56, 282
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL_BG,
                outline=PANEL_LINE, width=2)
    draw_skyline(d, lx + 10, ly + 10, 392, lh - 20)
    d.line([lx + 412, ly + 10, lx + 412, ly + lh - 10], fill=PANEL_LINE,
           width=1)
    tx = lx + 430
    d.text((tx, ly + 16), "LEAD STORY  •  ENTERTAINMENT",
           font=font(SANS_B, 17), fill=RED)
    hl = wrap(d, "GTA VI SMASHES ALL RECORDS", font(SERIF_B, 44), lw - 448)
    yy = text_block(d, tx, ly + 48, hl, font(SERIF_B, 44), INK, 50)
    sl = wrap(d, "$3.79bn in a day - the biggest entertainment launch in history.",
              font(SANS, 22), lw - 448)
    text_block(d, tx, yy + 10, sl, font(SANS, 22), (64, 60, 54), 28)
    d.text((tx, ly + lh - 40), "32.5m copies pre-sold  •  99 on Metacritic",
           font=font(SANS_B, 18), fill=(64, 60, 54))

    # four middle stories, 2 x 2
    gx, gy = 28, 516
    pw, ph, gap = 474, 186, 20
    stories = [
        ("WAR IN EUROPE", "KYIV BRIDGES HIT IN HUGE BARRAGE",
         "400+ drones, 110 missiles; three fall in Poland.",
         draw_bridge),
        ("DIPLOMACY", "TRUMP, XI AND PUTIN PLEDGE PEACE",
         "Joint declaration after the first three-way summit.",
         draw_flags),
        ("JUSTICE", "MYANMAR REJECTS GENOCIDE RULING",
         "The junta calls it unfair, a day after the verdict.",
         draw_scales),
        ("CLIMATE", "CLIMATE TALKS STALL IN ANTALYA",
         "COP31 draft deadlocked over fossil-fuel wording.",
         draw_climate),
    ]
    for i, (kick, head, sub, art) in enumerate(stories):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        story_panel(d, px, py, pw, ph, kick, head, sub, art)

    # bottom strip: Anthropic
    bx, by, bw, bh = 28, 928, W - 56, 62
    d.rectangle([bx, by, bx + bw, by + bh], fill=PANEL_BG,
                outline=PANEL_LINE, width=2)
    draw_chart(d, bx + 8, by + 6, 170, bh - 12)
    d.line([bx + 186, by + 8, bx + 186, by + bh - 8], fill=PANEL_LINE, width=1)
    d.text((bx + 200, by + 5), "ANTHROPIC SLIDES 9% AFTER RECORD DEBUT",
           font=font(SERIF_B, 22), fill=INK)
    d.text((bx + 200, by + 35),
           "Day-two dip after the $2tn debut; record $93.5bn IPO closes.",
           font=font(SANS, 16), fill=(64, 60, 54))

    # footer
    ff = font(SANS, 15)
    foot = "SIX STORIES, ONE PAGE  •  THE WORLD TODAY  •  20 NOVEMBER 2026"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1000), foot, font=ff, fill=GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
