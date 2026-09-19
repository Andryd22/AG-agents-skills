#!/usr/bin/env python3
"""Rimozione dello sfondo a partire dai bordi, per le immagini dei diorami.

Toglie lo sfondo piatto di un'immagine di scena (il diorama resta sospeso sulla
trasparenza) con un riempimento che parte dai bordi e si estende ai pixel vicini al
colore degli angoli. Le zone interne che per caso hanno il colore dello sfondo (es. le
pareti crema dentro la scena) restano, perché il riempimento raggiunge solo i pixel
collegati ai bordi. La morbida ombra di contatto resta come base naturale.

Uso:
    python3 knockout.py scena1.png scena2.png ...
    # scrive scena1.rgba.png, scena2.rgba.png, ...
    # facoltativo: la variabile d'ambiente TOL (predefinita 34) allarga/stringe la somiglianza con lo sfondo

Poi codifica in webp con alpha, es.:
    cwebp -q 84 -alpha_q 95 -resize 1800 0 scena1.rgba.png -o scena1.webp

Non servono numpy né ImageMagick: solo PIL. Va con il passo 3 di SKILL.md.
"""
import os
import sys
from collections import deque
from PIL import Image, ImageFilter

TOL = float(os.environ.get("TOL", "34"))   # distanza euclidea RGB che conta come sfondo


def corner_color(im):
    w, h = im.size
    px = im.load()
    pts = [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)]
    r = sum(px[x, y][0] for x, y in pts) // 4
    g = sum(px[x, y][1] for x, y in pts) // 4
    b = sum(px[x, y][2] for x, y in pts) // 4
    return (r, g, b)


def knock(inp, outp):
    im = Image.open(inp).convert("RGB")
    w, h = im.size
    px = im.load()
    cr, cg, cb = corner_color(im)
    tol2 = TOL * TOL

    def is_bg(x, y):
        r, g, b = px[x, y]
        dr, dg, db = r - cr, g - cg, b - cb
        return dr * dr + dg * dg + db * db <= tol2

    bg = bytearray(w * h)
    seen = bytearray(w * h)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            i = y * w + x
            if not seen[i] and is_bg(x, y):
                seen[i] = 1; bg[i] = 1; dq.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            i = y * w + x
            if not seen[i] and is_bg(x, y):
                seen[i] = 1; bg[i] = 1; dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                i = ny * w + nx
                if not seen[i]:
                    seen[i] = 1
                    if is_bg(nx, ny):
                        bg[i] = 1; dq.append((nx, ny))

    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        base = y * w
        for x in range(w):
            if bg[base + x]:
                ap[x, y] = 0
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.4))   # ammorbidisce il contorno della soglia
    out = im.convert("RGBA")
    out.putalpha(alpha)
    out.save(outp)
    print("sfondo rimosso:", outp)


if __name__ == "__main__":
    for name in sys.argv[1:]:
        knock(name, name.rsplit(".", 1)[0] + ".rgba.png")
