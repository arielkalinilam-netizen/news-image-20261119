#!/usr/bin/env python3
"""Front page of 19 November 2026 — the day's world news in one image.

The program draws a newspaper front page with Pillow, standard library only,
no network, fully deterministic: same bytes every run.

Stories (all from Thursday 19 November 2026 coverage):
 1. Trump-Xi-Putin historic trilateral summit in Shenzhen (APEC) — first
    three-way US/China/Russia leaders' talks; Trump: US & China want to help
    end the Ukraine war; Zelenskyy awaits debrief from US envoys.
 2. US and Venezuela sign a deal to reestablish military ties (Hegseth in
    Caracas), then continue to Colombia for anti-drug cooperation.
 3. APEC Leaders' Shenzhen Outlook / CEO Summit closes with the Shenzhen
    initiative — trade integration, connectivity and AI on the agenda.
 4. Markets: S&P futures rally; Anthropic's record-breaking IPO mints
    thousands of employees as stock debuts; OPEC chief: fossil fuels remain
    vital to electrification.
"""

import zlib, struct, os, io

W = H = 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

# ---------- palette ----------
INK = (24, 22, 20)
PAPER = (246, 241, 230)
ACCENT = (180, 32, 32)
GRAY = (110, 105, 98)

# ---------- tiny built-in vector font (5x7), deterministic, no font files ----------
GLYPH = {
 'A':["01110","10001","10001","11111","10001","10001","10001"],
 'B':["11110","10001","11110","10001","10001","10001","11110"],
 'C':["01111","10000","10000","10000","10000","10000","01111"],
 'D':["11110","10001","10001","10001","10001","10001","11110"],
 'E':["11111","10000","11110","10000","10000","10000","11111"],
 'F':["11111","10000","11110","10000","10000","10000","10000"],
 'G':["01111","10000","10000","10111","10001","10001","01110"],
 'H':["10001","10001","11111","10001","10001","10001","10001"],
 'I':["11111","00100","00100","00100","00100","00100","11111"],
 'J':["00111","00010","00010","00010","00010","10010","01100"],
 'K':["10001","10010","11100","10010","10001","10001","10001"],
 'L':["10000","10000","10000","10000","10000","10000","11111"],
 'M':["10001","11011","10101","10101","10001","10001","10001"],
 'N':["10001","11001","10101","10011","10001","10001","10001"],
 'O':["01110","10001","10001","10001","10001","10001","01110"],
 'P':["11110","10001","10001","11110","10000","10000","10000"],
 'Q':["01110","10001","10001","10001","10101","10011","01111"],
 'R':["11110","10001","10001","11110","10010","10001","10001"],
 'S':["01111","10000","10000","01110","00001","00001","11110"],
 'T':["11111","00100","00100","00100","00100","00100","00100"],
 'U':["10001","10001","10001","10001","10001","10001","01110"],
 'V':["10001","10001","10001","10001","10001","01010","00100"],
 'W':["10001","10001","10001","10101","10101","11011","10001"],
 'X':["10001","10001","01010","00100","01010","10001","10001"],
 'Y':["10001","10001","01010","00100","00100","00100","00100"],
 'Z':["11111","00001","00010","00100","01000","10000","11111"],
 '0':["01110","10001","10011","10101","11001","10001","01110"],
 '1':["00100","01100","00100","00100","00100","00100","01110"],
 '2':["01110","10001","00001","00110","01000","10000","11111"],
 '3':["11110","00001","00001","01110","00001","00001","11110"],
 '4':["00010","00110","01010","10010","11111","00010","00010"],
 '5':["11111","10000","11110","00001","00001","10001","01110"],
 '6':["00110","01000","10000","11110","10001","10001","01110"],
 '7':["11111","00001","00010","00100","01000","01000","01000"],
 '8':["01110","10001","10001","01110","10001","10001","01110"],
 '9':["01110","10001","10001","01111","00001","00010","01100"],
 ' ':["00000","00000","00000","00000","00000","00000","00000"],
 '.':["00000","00000","00000","00000","00000","00100","00100"],
 ',':["00000","00000","00000","00000","00100","00100","01000"],
 '-':["00000","00000","00000","11111","00000","00000","00000"],
 ':':["00000","00100","00100","00000","00100","00100","00000"],
 "'":["00100","00100","00000","00000","00000","00000","00000"],
 '!':["00100","00100","00100","00100","00100","00000","00100"],
 '/':["00001","00010","00010","00100","01000","01000","10000"],
 '(':["00010","00100","01000","01000","01000","00100","00010"],
 ')':["01000","00100","00010","00010","00010","00100","01000"],
 '&':["01100","10010","10100","01000","10101","10010","01101"],
 'X':["10001","10001","01010","00100","01010","10001","10001"],
 '+':["00000","00100","00100","11111","00100","00100","00000"],
 '"':["01010","01010","00000","00000","00000","00000","00000"],
 '%':["10001","00010","00010","00100","01000","01000","10001"],
 '?':["01110","10001","00001","00110","00100","00000","00100"],
 '$':["00100","01111","10100","01110","00101","11110","00100"],
 '#':["01010","11111","01010","01010","01010","11111","01010"],
}

def draw_text(px, x, y, text, scale=2, color=INK):
    cx = x
    for ch in text.upper():
        g = GLYPH.get(ch, GLYPH['?'])
        for gy, row in enumerate(g):
            for gx, bit in enumerate(row):
                if bit == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            px[cx+gx*scale+dx, y+gy*scale+dy] = color
        cx += 6 * scale
    return cx

def text_width(text, scale=2):
    return len(text) * 6 * scale

def center_text(px, y, text, scale=2, color=INK, maxw=W):
    w = text_width(text, scale)
    draw_text(px, max(0, (maxw - w)//2), y, text, scale, color)

# ---------- drawing helpers ----------
def rect(px, x0, y0, x1, y1, color):
    for y in range(max(0,y0), min(H,y1)):
        for x in range(max(0,x0), min(W,x1)):
            px[x, y] = color

def hline(px, x0, x1, y, color, t=2):
    rect(px, x0, y, x1, y+t, color)

def globe(px, cx, cy, r, color):
    """Simple globe: circle with meridians and a shaded hemisphere."""
    for y in range(-r, r+1):
        half = int((r*r - y*y) ** 0.5)
        for x in range(-half, half+1):
            # hemisphere shading: right half darker
            c = color if x <= 0 else tuple(max(0, v-25) for v in color)
            px[cx+x, cy+y] = c
    # meridians
    for mx in (r//3, 2*r//3):
        for y in range(-r, r+1):
            half = int((r*r - y*y) ** 0.5)
            for sx in (-mx, mx):
                x = int(sx * half / r) if r else sx
                if abs(x) <= half:
                    px[cx+x, cy+y] = tuple(max(0, v-60) for v in color)
    # equator
    for x in range(-r, r+1):
        px[cx+x, cy] = tuple(max(0, v-60) for v in color)
    # continents (simple blobs)
    for (bx, by, br) in ((-r//3, -r//3, r//5), (r//4, 0, r//6), (-r//4, r//3, r//7)):
        for y in range(-br, br+1):
            half = int((br*br - y*y) ** 0.5)
            for x in range(-half, half+1):
                px[cx+bx+x, cy+by+y] = PAPER if by+y < 0 else tuple(max(0,v-90) for v in color)

def handshake(px, cx, cy, s, color):
    """Two meeting arms: simple chevrons."""
    for i in range(s):
        px[cx - s + i, cy + s - i] = color
        px[cx - s + i, cy + s - i + 1] = color
        px[cx + i, cy + s - i] = color
        px[cx + i, cy + s - i + 1] = color
    rect(px, cx-2, cy+s//2-1, cx+3, cy+s//2+3, color)

def stock_arrow(px, x0, y0, pts, color):
    for i in range(len(pts)-1):
        x1,y1 = x0+pts[i][0], y0-pts[i][1]
        x2,y2 = x0+pts[i+1][0], y0-pts[i+1][1]
        steps = max(abs(x2-x1), abs(y2-y1))
        for t in range(steps+1):
            x = x1 + (x2-x1)*t//steps
            y = y1 + (y2-y1)*t//steps
            for dy in (-1,0,1):
                px[x, y+dy] = color
    lx, ly = pts[-1]
    rect(px, x0+lx, y0-ly-4, x0+lx+7, y0-ly+2, color)

def oil_drop(px, cx, cy, r, color):
    for y in range(-r, r+1):
        half = int((r*r - y*y) ** 0.5)
        for x in range(-half, half+1):
            px[cx+x, cy+y] = color
    rect(px, cx-1, cy-r-4, cx+1, cy-r, color)

def laurel(px, cx, cy, color, n=6):
    """Small APEC-style laurel: arc of leaves."""
    import math
    for i in range(n):
        a = math.pi * (0.15 + 0.7*i/(n-1))
        x = int(cx + (30) * math.cos(a))
        y = int(cy - 24 * math.sin(a))
        rect(px, x-2, y-2, x+3, y+3, color)

# ---------- page ----------
def build():
    buf = bytearray(PAPER * (W*H))
    px = Memory = None
    # index-based pixel access
    class Pix:
        def __init__(s, buf): s.b = buf
        def __getitem__(s, k): x,y = k; i = (y*W+x)*3; return (s.b[i], s.b[i+1], s.b[i+2])
        def __setitem__(s, k, v): x,y = k; i=(y*W+x)*3; s.b[i],s.b[i+1],s.b[i+2] = v
    px = Pix(buf)

    # margin frame
    rect(px, 0, 0, W, 6, INK)
    rect(px, 0, H-6, W, H, INK)
    rect(px, 0, 0, 6, H, INK)
    rect(px, W-6, 0, W, H, INK)

    # ---- masthead ----
    center_text(px, 28, "THE DAILY GLOBE", 6)
    center_text(px, 86, "THURSDAY, NOVEMBER 19, 2026", 2, GRAY)
    hline(px, 24, W-24, 116, INK, 4)
    hline(px, 24, W-24, 122, INK, 1)

    # ---- lead story: trilateral summit ----
    rect(px, 24, 136, W-24, 320, (238, 232, 218))
    center_text(px, 150, "TRUMP, XI, PUTIN HOLD", 5, ACCENT)
    center_text(px, 220, "FIRST-EVER 3-WAY SUMMIT", 5, ACCENT)
    center_text(px, 292, "SHENZHEN, APEC - US AND CHINA WANT TO HELP", 2)
    center_text(px, 318, "END UKRAINE WAR, SAYS TRUMP", 2)

    # globe illustration
    globe(px, 130, 470, 78, (60, 110, 170))
    center_text(px, 560, "THREE LEADERS, ONE TABLE", 2, GRAY)

    # right column: ukraine hope + zelenskyy
    rect(px, 250, 380, W-24, 560, PAPER)
    draw_text(px, 268, 392, "UKRAINE: HOPE FOR END", 3, INK)
    draw_text(px, 268, 436, "ZELENSKYY AWAITS DEBRIEF", 2)
    draw_text(px, 268, 462, "FROM US ENVOYS ON TALKS", 2)
    draw_text(px, 268, 488, "WITH XI AND PUTIN", 2)
    handshake(px, 320, 520, 46, (150, 40, 40))

    # ---- story 2: US-Venezuela ----
    hline(px, 24, W-24, 585, INK, 2)
    draw_text(px, 40, 600, "US AND VENEZUELA SIGN DEAL", 3, INK)
    draw_text(px, 40, 640, "TO RESTORE MILITARY TIES", 3, INK)
    draw_text(px, 40, 678, "HEGSETH IN CARACAS, THEN COLOMBIA", 2, GRAY)
    # map-ish blob: Venezuela & Colombia region
    rect(px, 700, 596, 990, 700, (232, 226, 210))
    rect(px, 760, 620, 850, 680, (190, 150, 60))
    draw_text(px, 770, 640, "VEN", 2, INK)
    rect(px, 855, 610, 950, 700, (120, 160, 90))
    draw_text(px, 870, 630, "COL", 2, INK)

    # ---- story 3: APEC ----
    hline(px, 24, W-24, 715, INK, 2)
    draw_text(px, 40, 730, "APEC CLOSES IN SHENZHEN:", 3, INK)
    draw_text(px, 40, 768, "TRADE, AI AND CONNECTIVITY PACT", 2)
    laurel(px, 900, 770, (40, 90, 50))

    # ---- story 4: markets ----
    hline(px, 24, W-24, 800, INK, 2)
    draw_text(px, 40, 815, "MARKETS: FUTURES RALLY", 3, INK)
    draw_text(px, 40, 852, "ANTHROPIC IPO RECORD DEBUT", 2, GRAY)
    draw_text(px, 40, 878, "OPEC: FOSSIL FUELS STILL VITAL", 2, GRAY)
    stock_arrow(px, 700, 935, [(0,20),(50,30),(100,16),(150,34),(200,46),(250,40),(330,60)], (30,120,60))
    oil_drop(px, 620, 838, 22, (40,40,45))

    # ---- footer ----
    hline(px, 24, W-24, 950, INK, 2)
    center_text(px, 962, "WORLD - SHENZHEN - CARACAS - KYIV - WALL ST", 2, GRAY)

    return bytes(buf)

# ---------- PNG writer (deterministic, stdlib only) ----------
def write_png(path, raw, w, h):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
        return c
    stride = w*3
    scan = b"".join(b"\x00" + raw[y*stride:(y+1)*stride] for y in range(h))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(scan, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    raw = build()
    write_png(OUT, raw, W, H)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
