#!/usr/bin/env python3
"""Front page of 19 November 2026 - the day's world news in one image.

Deterministic, network-free, stdlib only: every pixel drawn here.

Stories (Thursday 19 November 2026):
  1. Shenzhen - Trump, Xi and Putin hold the first-ever three-way summit
     at APEC; Washington and Beijing say they want to help end the Ukraine
     war, Zelenskyy awaits the envoys' debrief.
  2. APEC - Xi chairs the leaders' meeting and calls for a shared
     Asia-Pacific community; the Shenzhen initiative carries forward.
  3. Caracas - the US and Venezuela sign a deal to restore military ties
     (Hegseth in Caracas), then on to Colombia for anti-drug cooperation.
  4. Markets - S&P futures rally, Anthropic's IPO debuts at a record,
     the OPEC chief says fossil fuels stay vital to electrification.
"""

import os
import struct
import zlib

W = H = 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

INK = (26, 24, 22)
PAPER = (247, 242, 231)
CREAM = (238, 231, 215)
ACCENT = (168, 30, 30)
NAVY = (28, 52, 92)
GRAY = (112, 106, 98)
GREEN = (34, 108, 66)
SAND = (198, 168, 108)

# ---------------------------------------------------------------- 5x7 glyphs
GLYPH = {
 'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
 'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
 'C': ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
 'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
 'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
 'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
 'G': ["01111", "10000", "10000", "10111", "10001", "10001", "01110"],
 'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
 'I': ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
 'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
 'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
 'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
 'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
 'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
 'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
 'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
 'Q': ["01110", "10001", "10001", "10001", "10101", "10011", "01111"],
 'R': ["11110", "10001", "10001", "11110", "10010", "10001", "10001"],
 'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
 'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
 'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
 'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
 'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
 'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
 'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
 'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
 '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
 '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
 '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
 '3': ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
 '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
 '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
 '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
 '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
 '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
 '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
 ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
 '.': ["00000", "00000", "00000", "00000", "00000", "00110", "00110"],
 ',': ["00000", "00000", "00000", "00000", "00110", "00110", "01100"],
 '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
 ':': ["00000", "00110", "00110", "00000", "00110", "00110", "00000"],
 "'": ["00110", "00110", "00000", "00000", "00000", "00000", "00000"],
 '!': ["00110", "00110", "00110", "00110", "00110", "00000", "00110"],
 '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
 '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
 ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
 '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
 '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
 '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
 '%': ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
 '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
 '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
 '#': ["01010", "11111", "01010", "01010", "01010", "11111", "01010"],
 '>': ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
 '<': ["00001", "00010", "00100", "01000", "00100", "00010", "00001"],
 '=': ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
}


class Pix:
    """Tiny RGB pixel surface over a bytearray."""

    def __init__(self, buf):
        self.b = buf

    def __setitem__(self, k, v):
        x, y = k
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.b[i], self.b[i + 1], self.b[i + 2] = v

    def __getitem__(self, k):
        x, y = k
        i = (y * W + x) * 3
        return (self.b[i], self.b[i + 1], self.b[i + 2])


def draw_text(px, x, y, text, scale=2, color=INK):
    cx = x
    for ch in text.upper():
        g = GLYPH.get(ch, GLYPH['?'])
        for gy, row in enumerate(g):
            for gx, bit in enumerate(row):
                if bit == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            px[cx + gx * scale + dx, y + gy * scale + dy] = color
        cx += 6 * scale
    return cx


def text_w(text, scale=2):
    return len(text) * 6 * scale


def center_text(px, y, text, scale=2, color=INK, x0=0, x1=W):
    w = text_w(text, scale)
    draw_text(px, x0 + max(0, ((x1 - x0) - w) // 2), y, text, scale, color)


def wrap(px, x, y, text, scale, color, maxw, lead=1.8):
    """Word-wrap into lines; returns the y after the last line."""
    words = text.upper().split()
    line = ""
    step = int(scale * 7 * lead)
    for w in words:
        trial = (line + " " + w).strip()
        if text_w(trial, scale) <= maxw or not line:
            line = trial
        else:
            draw_text(px, x, y, line, scale, color)
            y += step
            line = w
    if line:
        draw_text(px, x, y, line, scale, color)
        y += step
    return y


def rect(px, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            px[x, y] = color


def frame(px, x0, y0, x1, y1, color, t=1):
    rect(px, x0, y0, x1, y0 + t, color)
    rect(px, x0, y1 - t, x1, y1, color)
    rect(px, x0, y0, x0 + t, y1, color)
    rect(px, x1 - t, y0, x1, y1, color)


def hline(px, x0, x1, y, color, t=2):
    rect(px, x0, y, x1, y + t, color)


def vline(px, x, y0, y1, color, t=2):
    rect(px, x, y0, x + t, y1, color)


def disc(px, cx, cy, r, color, shade=None):
    for y in range(-r, r + 1):
        half = int((r * r - y * y) ** 0.5)
        for x in range(-half, half + 1):
            c = color
            if shade and x > 0:
                c = tuple(max(0, v - shade) for v in color)
            px[cx + x, cy + y] = c


def globe(px, cx, cy, r, ocean, land):
    """Globe with meridians, a shaded limb and simple continents."""
    disc(px, cx, cy, r, ocean, 34)
    # graticule
    for f in (0.36, 0.72):
        mx = int(r * f)
        for y in range(-r, r + 1):
            half2 = r * r - y * y
            if half2 <= 0:
                continue
            half = half2 ** 0.5
            for sx in (-mx, mx):
                x = int(sx * half / r)
                px[cx + x, cy + y] = tuple(max(0, v - 40) for v in ocean)
    for f in (0.30, 0.62):
        yy = int(r * f)
        for sgn in (-1, 1):
            half2 = r * r - yy * yy
            if half2 <= 0:
                continue
            half = int(half2 ** 0.5)
            for x in range(-half, half + 1):
                px[cx + x, cy + sgn * yy] = tuple(max(0, v - 40) for v in ocean)
    # continents: Europe/Africa, Americas, Asia
    for (bx, by, bw, bh) in ((-int(r * .42), -int(r * .35), int(r * .22), int(r * .55)),
                             (int(r * .18), -int(r * .55), int(r * .28), int(r * .38)),
                             (int(r * .30), int(r * .05), int(r * .26), int(r * .30))):
        for y in range(bh):
            for x in range(bw):
                if (x - bw / 2) ** 2 / (bw / 2) ** 2 + (y - bh / 2) ** 2 / (bh / 2) ** 2 <= 1.0:
                    px[cx + bx + x, cy + by + y] = land


def laurel(px, cx, cy, r, color):
    """Two curved leaf branches, APEC-style."""
    import math
    for sgn in (-1, 1):
        for i in range(7):
            a = math.pi * (0.08 + 0.13 * i)
            x = int(cx + sgn * r * math.cos(a) * 0.82)
            y = int(cy - r * math.sin(a) * 0.9)
            disc(px, x, y, 4, color)
        for i in range(1, 7):
            a0 = math.pi * (0.08 + 0.13 * (i - 1))
            a1 = math.pi * (0.08 + 0.13 * i)
            x0 = int(cx + sgn * r * math.cos(a0) * 0.82)
            y0 = int(cy - r * math.sin(a0) * 0.9)
            x1 = int(cx + sgn * r * math.cos(a1) * 0.82)
            y1 = int(cy - r * math.sin(a1) * 0.9)
            steps = max(abs(x1 - x0), abs(y1 - y0), 1)
            for t in range(steps + 1):
                px[x0 + (x1 - x0) * t // steps, y0 + (y1 - y0) * t // steps] = color


def handshake(px, cx, cy, s, color):
    """Two forearms meeting: tapered arms plus clasped hands."""
    for i in range(s):
        px[cx - s + i, cy + i // 2] = color
        px[cx + s - i, cy + i // 2] = color
        for d in (1, 2):
            px[cx - s + i, cy + i // 2 + d] = color
            px[cx + s - i, cy + i // 2 + d] = color
    rect(px, cx - 7, cy - 2, cx + 7, cy + 9, color)


def chart(px, x0, y0, w, h, pts, color, axis=GRAY):
    """Line chart with axes and an arrow head."""
    vline(px, x0, y0 - h - 6, y0, axis, 2)
    hline(px, x0, x0 + w + 6, y0, axis, 2)
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        x1, y1 = x0 + ax, y0 - ay
        x2, y2 = x0 + bx, y0 - by
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for t in range(steps + 1):
            px[x1 + (x2 - x1) * t // steps, y1 + (y2 - y1) * t // steps] = color
    lx, ly = pts[-1]
    for d in range(7):
        px[x0 + lx - d, y0 - ly - 6 + d] = color
        px[x0 + lx + d, y0 - ly - 6 + d] = color


def barrel(px, cx, cy, w, h, color):
    """Oil barrel silhouette: body, two hoops, top ellipse."""
    rect(px, cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2, color)
    for hy in (cy - h // 4, cy + h // 4):
        rect(px, cx - w // 2, hy, cx + w // 2, hy + 4, tuple(min(255, v + 40) for v in color))
    for y in range(-6, 7):
        half = int((36 - y * y) ** 0.5) if y * y < 36 else 0
        for x in range(-half, half + 1):
            px[cx + x, cy - h // 2 + y] = tuple(min(255, v + 55) for v in color)


def refinery(px, cx, cy, color, flame):
    """Oil refinery: two towers, a stack, a flare."""
    rect(px, cx - 46, cy, cx - 26, cy + 54, color)
    rect(px, cx - 20, cy - 16, cx + 2, cy + 54, color)
    rect(px, cx + 8, cy + 10, cx + 26, cy + 54, color)
    rect(px, cx + 34, cy - 34, cx + 42, cy + 54, color)
    for i in range(5):
        for j in range(5 - i):
            px[cx + 38 - j, cy - 40 - i] = flame
            px[cx + 38 + j, cy - 40 - i] = flame
    for x in range(cx - 46, cx + 43, 9):
        px[x, cy + 10] = color


def flag_us(px, x, y, w, h):
    rect(px, x, y, x + w, y + h, (250, 250, 250))
    for i in range(0, 13, 2):
        rect(px, x, y + i * h // 13, x + w, y + (i + 1) * h // 13, (178, 34, 52))
    rect(px, x, y, x + w // 2, y + 7 * h // 13, (28, 52, 116))
    for sy in range(y + 3, y + 7 * h // 13, 6):
        for sx in range(x + 4, x + w // 2 - 2, 7):
            rect(px, sx, sy, sx + 2, sy + 2, (250, 250, 250))


def flag_ph(px, x, y, w, h):
    rect(px, x, y, x + w, y // 1 + h, (0, 56, 168))
    rect(px, x, y, x + w, y + h // 2, (0, 56, 168))
    rect(px, x, y + h // 2, x + w, y + h, (206, 17, 38))
    for yy in range(y, y + h, 3):
        for xx in range(x, x + w // 2, 3):
            pass
    rect(px, x, y, x + w // 2, y + h, (255, 255, 255))
    disc(px, x + w // 4, y + h // 2, 6, (252, 209, 22))


def page():
    buf = bytearray(PAPER * (W * H))
    px = Pix(buf)

    # paper: very light vertical rule texture, exact and deterministic
    for x in range(0, W, 64):
        for y in range(0, H):
            if (x + y) % 97 == 0:
                px[x, y] = (241, 235, 223)

    # border
    frame(px, 0, 0, W, H, INK, 8)

    # ---------------- masthead ----------------
    rule_y = 132
    for xx in range(24, W - 24):
        px[xx, rule_y] = INK
    center_text(px, 34, "THE DAILY GLOBE", 7)
    draw_text(px, 40, 100, "WORLD EDITION", 2, GRAY)
    center_text(px, 100, "THURSDAY, 19 NOVEMBER 2026", 2, GRAY)
    draw_text(px, W - 200, 100, "NO. 19", 2, GRAY)
    hline(px, 24, W - 24, 128, INK, 5)

    # ---------------- lead ----------------
    rect(px, 24, 146, W - 24, 400, CREAM)
    center_text(px, 158, "TRUMP, XI, PUTIN MEET", 7, ACCENT)
    center_text(px, 228, "FIRST-EVER 3-WAY SUMMIT, SHENZHEN", 3, INK)
    wrap(px, 60, 276, "Shenzhen, Nov 19 - The US, Chinese and Russian leaders "
         "hold the first-ever three-way summit. Washington and Beijing say "
         "they want to help end the Ukraine war.", 2, INK, W - 120, 1.7)

    # summit illustration: three lecterns with flags
    base_y = 396
    for i, (col, label) in enumerate(((NAVY, "US"), ((178, 34, 52), "CN"), ((40, 70, 40), "RU"))):
        cx = 200 + i * 312
        rect(px, cx - 44, base_y - 44, cx + 44, base_y, col)
        rect(px, cx - 52, base_y - 52, cx + 52, base_y - 44, tuple(max(0, v - 40) for v in col))
        draw_text(px, cx - 12, base_y - 32, label, 3, (250, 246, 238))

    # ---------------- second row ----------------
    top = 414
    hline(px, 24, W - 24, top, INK, 4)
    vline(px, 512, top + 12, 748, INK, 3)

    # story A: refineries struck / war
    draw_text(px, 40, top + 20, "KYIV AWAITS THE", 3, INK)
    draw_text(px, 40, top + 52, "ENVOYS' DEBRIEF", 3, ACCENT)
    refinery(px, 120, top + 118, (60, 56, 52), (232, 132, 40))
    wrap(px, 40, top + 190, "Zelenskyy welcomed the plan taking shape "
         "behind the summit, as fighting went on.", 2, GRAY, 440, 1.6)

    # story B: APEC / Xi
    draw_text(px, 548, top + 20, "APEC OPENS IN SHENZHEN", 3, INK)
    draw_text(px, 548, top + 52, "XI: ONE ASIA-PACIFIC", 3, ACCENT)
    laurel(px, 920, top + 208, 44, GREEN)
    draw_text(px, 896, top + 250, "APEC", 2, GREEN)
    wrap(px, 548, top + 96, "The CEO Summit released the Shenzhen "
         "initiative on trade and AI.", 2, GRAY, 300, 1.6)
    wrap(px, 548, top + 160, "Xi and President Lee held their third "
         "summit, 34 minutes long.", 2, GRAY, 300, 1.6)

    # ---------------- third row ----------------
    top2 = 760
    hline(px, 24, W - 24, top2, INK, 4)
    vline(px, 512, top2 + 12, 916, INK, 3)

    # story C: US-Philippines trade
    draw_text(px, 40, top2 + 16, "US, VENEZUELA RESTORE", 3, INK)
    draw_text(px, 40, top2 + 48, "MILITARY TIES", 3, ACCENT)
    flag_us(px, 40, top2 + 84, 92, 52)
    flag_ph(px, 148, top2 + 84, 92, 52)
    wrap(px, 40, top2 + 148, "HEGSETH IN CARACAS - THEN BOGOTA",
         2, GRAY, 440, 1.6)

    # story D: markets
    draw_text(px, 548, top2 + 16, "MARKETS: FUTURES RALLY", 3, INK)
    draw_text(px, 548, top2 + 48, "AI RECORD RUN", 3, ACCENT)
    chart(px, 566, top2 + 146, 200, 52,
          [(0, 18), (30, 30), (58, 14), (86, 34), (112, 24), (140, 42), (176, 48), (200, 54)],
          GREEN)
    barrel(px, 890, top2 + 104, 40, 54, (52, 48, 44))
    draw_text(px, 830, top2 + 142, "OPEC: OIL VITAL", 2, GRAY)

    # ---------------- footer ----------------
    hline(px, 24, W - 24, 938, INK, 4)
    draw_text(px, 40, 950, "ANTHROPIC IPO DEBUTS AT A RECORD - OIL AND GOLD SLIP", 2, INK)
    center_text(px, 984, "SHENZHEN - CARACAS - KYIV - WASHINGTON - WALL STREET", 2, GRAY)

    return bytes(buf)


def write_png(path, raw, w, h):
    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        return out + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    stride = w * 3
    scan = b"".join(b"\x00" + raw[y * stride:(y + 1) * stride] for y in range(h))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(scan, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    write_png(OUT, page(), W, H)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
