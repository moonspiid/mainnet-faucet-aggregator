"""Generate the PWA PNG icons from the same geometry as icons/icon.svg.

Pure standard library: no Pillow, no ImageMagick.
Run from the repository root: python3 tools/make-icons.py
"""

import math
import struct
import zlib
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "icons"

BG_TOP = (13, 26, 43)
BG_BOTTOM = (6, 11, 20)
DROP_A = (34, 211, 238)
DROP_B = (52, 211, 153)
GLOW = (34, 211, 238)
INK = (4, 18, 26)

DROP_CENTER_V = 0.234
DROP_RADIUS = 0.5
DROP_APEX_V = -0.625
TANGENT_HALF_WIDTH = 0.4065
TANGENT_V = -0.057

ARROW = [
    ((0.0, -0.023), (0.0, 0.477)),
    ((0.0, 0.477), (-0.1797, 0.2969)),
    ((0.0, 0.477), (0.1797, 0.2969)),
]
ARROW_HALF = 0.0508


def segment_distance(u, v, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length_sq = dx * dx + dy * dy
    t = 0.0 if length_sq == 0 else ((u - ax) * dx + (v - ay) * dy) / length_sq
    t = min(1.0, max(0.0, t))
    px, py = ax + t * dx, ay + t * dy
    return math.hypot(u - px, v - py)


def rounded_box_distance(u, v, radius):
    qx = abs(u) - (1.0 - radius)
    qy = abs(v) - (1.0 - radius)
    outside = math.hypot(max(qx, 0.0), max(qy, 0.0))
    inside = min(max(qx, qy), 0.0)
    return outside + inside - radius


def droplet_inside(u, v, scale):
    u /= scale
    v /= scale
    if (u * u + (v - DROP_CENTER_V) ** 2) <= DROP_RADIUS ** 2:
        return True
    if v > DROP_APEX_V and v <= TANGENT_V:
        span = (v - DROP_APEX_V) / (TANGENT_V - DROP_APEX_V)
        return abs(u) <= TANGENT_HALF_WIDTH * span
    return False


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def shade(u, v, rounded, scale):
    """Return (r, g, b, a) for a sample point in [-1, 1]."""
    if rounded and rounded_box_distance(u, v, 0.4375) > 0:
        return None

    t = (v + 1.0) / 2.0
    colour = mix(BG_TOP, BG_BOTTOM, t)

    glow = 1.0 - min(1.0, math.hypot(u, v - 0.12) / 0.72)
    if glow > 0:
        colour = mix(colour, GLOW, 0.26 * glow)

    if droplet_inside(u, v, scale):
        du, dv = u / scale, v / scale
        gradient = min(1.0, max(0.0, (du + dv + 0.62) / 1.6))
        colour = mix(DROP_A, DROP_B, gradient)
        for a, b in ARROW:
            if segment_distance(du, dv, a, b) <= ARROW_HALF:
                colour = INK
                break

    return colour


def render(size, rounded, scale, samples=3):
    rows = []
    step = 1.0 / (size * samples)
    for y in range(size):
        row = bytearray()
        for x in range(size):
            acc = [0.0, 0.0, 0.0]
            hits = 0
            for sy in range(samples):
                v = -1.0 + (y * samples + sy + 0.5) * 2.0 / (size * samples)
                for sx in range(samples):
                    u = -1.0 + (x * samples + sx + 0.5) * 2.0 / (size * samples)
                    colour = shade(u, v, rounded, scale)
                    if colour is not None:
                        acc[0] += colour[0]
                        acc[1] += colour[1]
                        acc[2] += colour[2]
                        hits += 1
            total = samples * samples
            if hits == 0:
                row += b"\x00\x00\x00\x00"
            else:
                row += bytes(
                    (
                        int(acc[0] / hits + 0.5),
                        int(acc[1] / hits + 0.5),
                        int(acc[2] / hits + 0.5),
                        int(255 * hits / total + 0.5),
                    )
                )
        rows.append(row)
    return rows


def write_png(path, size, rows):
    raw = b"".join(b"\x00" + bytes(row) for row in rows)

    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)


VARIANTS = [
    ("icon-192.png", 192, True, 1.0),
    ("icon-512.png", 512, True, 1.0),
    ("icon-maskable-512.png", 512, False, 0.78),
    ("apple-touch-icon.png", 180, False, 0.92),
]

if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, size, rounded, scale in VARIANTS:
        write_png(OUT_DIR / name, size, render(size, rounded, scale))
        print("wrote", OUT_DIR / name, size)
