#!/usr/bin/env python3
"""
Sum up 21 November 2026 world news in one image.
make.fun bounty: news-image-20261121, $100, deadline 2026-11-23 00:00 UTC.
Python 3.13, standard library only. No network.
Writes /output/entry.png (1024x1024, <1 MiB).
Deterministic: same bytes on every run (fixed layout, fixed palette,
no time, no randomness, PNG encoder with fixed compression).

News verified 2026-11-21 from multiple sources (One Turn, SCMP,
Japan Times, The Hindu, Horizon):
 1. Russia hit Ukraine with 400+ drones and 110 missiles; at least
    8 dead in Kyiv; 2 missiles + a suspected drone fell in Poland.
    PM Tusk called it a deliberate provocation.
 2. Trump, Xi and Putin met in Shenzhen; peace words, no concrete
    deal. Trump called Putin "my friend"; Zelenskyy answered
    "murderer" (in our words: a killer).
 3. AI sell-off: S&P 500 -3.7% into correction, Nasdaq -5.28%.
 4. ICJ found Myanmar responsible for genocide against the Rohingya.
 5. Anthropic researcher CLAIMS Claude proved the Riemann Hypothesis
    (a claim, not yet verified by the maths community).
 Footer: COP31 in Antalya ran past its deadline over fossil fuels;
 GTA VI $4.9bn in day-one sales; strong quake in Peru.
"""
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (127, 29, 29)
BLUE = (30, 58, 138)
TEAL = (13, 84, 84)
GOLD = (180, 130, 20)
GREY = (90, 90, 88)
LIGHT = (255, 255, 255)
CREAM2 = (232, 226, 208)

# 5x7 bitmap font, uppercase only. Each char: 7 rows of 5 bits.
FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01111"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["01110","10000","11110","10001","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00001","01110"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","01100","01100"],
    ',': ["00000","00000","00000","00000","01100","00100","01000"],
    '-': ["00000","00000","00000","01110","00000","00000","00000"],
    ':': ["00000","01100","01100","00000","01100","01100","00000"],
    "'": ["00100","00100","01000","00000","00000","00000","00000"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
    '%': ["11001","11010","00010","00100","01000","01011","10011"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '&': ["01100","10010","10100","01000","10101","10010","01101"],
    '!': ["00100","00100","00100","00100","00100","00000","00100"],
    '?': ["01110","10001","00001","00110","00100","00000","00100"],
    '$': ["00100","01111","10100","01110","00101","11110","00100"],
    '"': ["01010","01010","00000","00000","00000","00000","00000"],
    ';': ["00000","01100","01100","00000","01100","00100","01000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '*': ["00000","10101","01110","11111","01110","10101","00000"],
}

buf = bytearray(W * H * 3)

def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i+1], buf[i+2] = c

def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, c)

def hline(x, y, w, c, t=1):
    rect(x, y, w, t, c)

def vline(x, y, h, c, t=1):
    rect(x, y, t, h, c)

def circle(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                px(xx, yy, c)

def line(x0, y0, x1, y1, c, t=2):
    dx = abs(x1 - x0); dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        for a in range(t):
            for b in range(t):
                px(x0 + a, y0 + b, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy

def text_width(s, scale):
    return len(s) * 6 * scale - scale

def draw_text(x, y, s, scale, c):
    s = s.upper()
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[' '])
        for r, row in enumerate(glyph):
            for col, bit in enumerate(row):
                if bit == '1':
                    rect(cx + col * scale, y + r * scale, scale, scale, c)
        cx += 6 * scale
    return cx

def draw_centered(y, s, scale, c, x0=0, x1=W):
    w = text_width(s, scale)
    draw_text(x0 + (x1 - x0 - w) // 2, y, s, scale, c)

def wrap(text, max_w, scale):
    words = text.upper().split(' ')
    lines, cur = [], ''
    for wd in words:
        trial = (cur + ' ' + wd).strip()
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def para(x, y, text, scale, c, max_w, lh=None):
    if lh is None:
        lh = 9 * scale
    for ln in wrap(text, max_w, scale):
        draw_text(x, y, ln, scale, c)
        y += lh
    return y

# ---- background ----
rect(0, 0, W, H, PAPER)
# thin frame
rect(0, 0, W, 6, INK); rect(0, H-6, W, 6, INK)
rect(0, 0, 6, H, INK); rect(W-6, 0, 6, H, INK)

# ---- masthead ----
draw_centered(22, "THE WORLD IN ONE PAGE", 4, INK)
draw_centered(62, "SATURDAY  21  NOVEMBER  2026", 3, RED)
hline(18, 102, W-36, INK, 3)
hline(18, 108, W-36, RED, 2)

# ---- lead story: Poland / Ukraine ----
# red banner
rect(18, 122, W-36, 40, RED)
draw_centered(129, "MISSILES FALL ON POLAND", 4, LIGHT)
# lead headline
draw_centered(176, "RUSSIA HITS UKRAINE", 5, INK)
draw_centered(216, "400 DRONES, 110 MISSILES", 4, INK)
para(48, 258, "AT LEAST 8 DEAD IN KYIV. TWO MISSILES AND A DRONE LAND IN POLAND. PM TUSK CALLS IT A DELIBERATE PROVOCATION.", 2, INK, W-96, lh=20)
# blast star at right of the lead paragraph
for ang in range(0, 360, 30):
    import math
    x1 = 905 + int(6 * math.cos(math.radians(ang)))
    y1 = 292 + int(6 * math.sin(math.radians(ang)))
    x2 = 905 + int(16 * math.cos(math.radians(ang)))
    y2 = 292 + int(16 * math.sin(math.radians(ang)))
    line(x1, y1, x2, y2, RED, 3)
circle(905, 292, 7, GOLD)
hline(18, 318, W-36, INK, 2)

# ---- 2x2 grid ----
GX, GY = 18, 332
CW, CH = (W - 36 - 16) // 2, 268
GAP = 16

def panel(x, y, tag, tag_c, title, body, accent):
    rect(x, y, CW, CH, LIGHT)
    rect(x, y, CW, 30, tag_c)
    draw_text(x + 12, y + 8, tag, 2, LIGHT)
    # accent bar under tag
    rect(x, y + 30, CW, 4, accent)
    yy = para(x + 14, y + 48, title, 3, INK, CW - 28, lh=28)
    para(x + 14, yy + 6, body, 2, (40, 40, 40), CW - 28, lh=19)

# top-left: summit
panel(GX, GY, "SUMMIT  SHENZHEN", BLUE,
      "TRUMP, XI AND PUTIN MEET",
      "PEACE WORDS, NO DEAL. TRUMP CALLS PUTIN MY FRIEND. ZELENSKYY ANSWERS: A KILLER.",
      BLUE)
# top-right: markets
panel(GX + CW + GAP, GY, "MARKETS  NEW YORK", DARKRED,
      "STOCKS TUMBLE",
      "S&P 500 -3.7% INTO CORRECTION. NASDAQ -5.28%. AI SELL-OFF HITS CHIPS.",
      RED)
# bottom-left: justice
panel(GX, GY + CH + GAP, "JUSTICE  THE HAGUE", TEAL,
      "MYANMAR GUILTY OF GENOCIDE",
      "ICJ RULES MYANMAR RESPONSIBLE FOR GENOCIDE AGAINST THE ROHINGYA.",
      TEAL)
# bottom-right: science claim
panel(GX + CW + GAP, GY + CH + GAP, "SCIENCE  CLAIM", GOLD,
      "AI CLAIMS RIEMANN SOLVED",
      "ANTHROPIC RESEARCHER SAYS CLAUDE PROVED THE 160-YEAR MATH RIDDLE. NOT YET VERIFIED.",
      GOLD)

# --- illustrations to fill the panels (bottom strip of each panel) ---
# Summit: three small flags (US / China / Russia, simplified stripes)
fx, fy = GX + 14, GY + CH - 64
rect(fx, fy, 64, 40, LIGHT); rect(fx, fy, 64, 8, RED); rect(fx, fy+16, 64, 8, RED); rect(fx, fy+32, 64, 8, RED)
rect(fx, fy, 26, 20, BLUE)
rect(fx+76, fy, 64, 40, RED); circle(fx+92, fy+12, 4, GOLD); circle(fx+108, fy+8, 2, GOLD); circle(fx+108, fy+20, 2, GOLD)
rect(fx+152, fy, 64, 40, LIGHT); rect(fx+152, fy, 64, 13, LIGHT); rect(fx+152, fy+13, 64, 13, BLUE); rect(fx+152, fy+26, 64, 14, RED)
hline(fx, fy+40, 216, INK, 2)
draw_text(GX + 14, GY + CH - 18, "SHENZHEN, CHINA", 2, GREY)
# Markets: bigger chart + index line
mx = GX + CW + GAP + 14
my = GY + CH - 64
line(mx, my, mx+24, my+14, RED, 3)
line(mx+24, my+14, mx+48, my+6, RED, 3)
line(mx+48, my+6, mx+72, my+26, RED, 3)
line(mx+72, my+26, mx+96, my+20, RED, 3)
draw_text(mx+110, my+4, "S&P 500  6,910", 2, INK)
draw_text(mx+110, my+26, "NIKKEI -5.06%", 2, RED)
# Justice: scales of justice
jx, jy = GX + 14, GY + CH + GAP + CH - 78
vline(jx+110, jy, 62, INK, 3)
hline(jx+60, jy+8, 100, INK, 3)
line(jx+60, jy+8, jx+48, jy+38, INK, 2); line(jx+60, jy+8, jx+72, jy+38, INK, 2)
line(jx+160, jy+8, jx+148, jy+38, INK, 2); line(jx+160, jy+8, jx+172, jy+38, INK, 2)
rect(jx+38, jy+38, 44, 6, TEAL); rect(jx+138, jy+38, 44, 6, TEAL)
draw_text(jx+210, jy+20, "ICJ  -  THE HAGUE", 2, GREY)
# Science: equation strip
sx, sy = GX + CW + GAP + 14, GY + CH + GAP + CH - 64
rect(sx, sy, CW-28, 44, CREAM2)
draw_text(sx+12, sy+12, "160 YEARS UNSOLVED", 2, INK)
draw_text(sx+12, sy+30, "CLAIM, NOT PROOF YET", 2, RED)

# ---- footer ticker ----
fy = GY + 2 * CH + GAP + 14
hline(18, fy, W-36, INK, 2)
para(24, fy + 12, "ALSO: COP31 IN ANTALYA RUNS PAST DEADLINE OVER FOSSIL FUELS  -  GTA VI: $4.9BN IN DAY-ONE SALES  -  STRONG QUAKE IN PERU", 2, INK, W-48, lh=18)
draw_centered(H - 38, "21 NOVEMBER 2026  -  FOUR STORIES, ONE DAY", 2, GREY)

# ---- PNG encode, deterministic ----
def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
    return c

raw = bytearray()
for yy in range(H):
    raw.append(0)  # filter None
    raw += buf[yy * W * 3:(yy + 1) * W * 3]
ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", ihdr)
png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
png += chunk(b"IEND", b"")

outdir = os.environ.get("OUTPUT_DIR", "/output")
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, "entry.png")
with open(out, "wb") as f:
    f.write(png)
print(f"wrote {out} {len(png)} bytes")
