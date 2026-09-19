#!/usr/bin/env python3
"""Legge le slide di una lezione da un PDF: testo di ogni slide, immagini delle slide, ritagli delle figure.

Funziona con una slide per pagina e con gli handout (più slide incorniciate per
pagina). Le slide sono numerate 1..N in ordine di lettura. Le coordinate sono
percentuali della slide (0-100), x da sinistra, y dall'alto.

Uso:
    python slides.py info   slides.pdf
    python slides.py text   slides.pdf [--slides 3-7,10]
    python slides.py render slides.pdf --slides 5 [--out tmp] [--grid] [--dpi 150]
    python slides.py figures slides.pdf [--slides 5]
    python slides.py crop   slides.pdf --slide 5 --box 10,30,90,95 --out images/ch05_name.png
    python slides.py crop   slides.pdf --slide 5 --auto --out images/ch05_name.png

Richiede PyMuPDF: pip install pymupdf
"""
import argparse
import collections
import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:  # PyMuPDF < 1.24.3
    try:
        import fitz as pymupdf
    except ImportError:
        sys.exit("PyMuPDF mancante: pip install pymupdf")


# ------------------------------------------------------------------- slide
def frame_candidates(page):
    """Rettangoli grandi in una pagina: le cornici delle slide degli handout (e qualche riquadro grande)."""
    w, h = page.rect.width, page.rect.height
    found = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.width > 0.4 * w and r.height > 0.2 * h and not (r.width > 0.97 * w and r.height > 0.97 * h):
            if not any(abs(r.x0 - f.x0) < 4 and abs(r.y0 - f.y0) < 4 and abs(r.x1 - f.x1) < 4 and abs(r.y1 - f.y1) < 4 for f in found):
                found.append(pymupdf.Rect(r))
    return found


def all_slides(doc):
    """[(numero, pagina, rettangolo)] in ordine di lettura.

    La cornice di un handout è un rettangolo grande che si trova nello stesso punto
    di molte pagine; un riquadro grande disegnato dentro una slide no. Senza
    cornici, una pagina è una slide.
    """
    key = lambda r: tuple(round(v / 5) for v in r)
    per_page = [frame_candidates(page) for page in doc]
    count = collections.Counter(key(r) for rects in per_page for r in rects)
    common = {k for k, c in count.items() if c >= max(2, 0.3 * doc.page_count)}
    out = []
    for page, rects in zip(doc, per_page):
        frames = [r for r in rects if key(r) in common]
        frames = [f for f in frames if not any(g != f and f.contains(g) for g in frames)]
        for rect in sorted(frames, key=lambda r: (round(r.y0 / 10), r.x0)) or [page.rect]:
            out.append((len(out) + 1, page, rect))
    return out


def parse_range(spec, total):
    if not spec:
        return list(range(1, total + 1))
    chosen = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        chosen += range(int(a), int(b or a) + 1)
    return [n for n in chosen if 1 <= n <= total]


def rel(box, frame):
    """Riquadro assoluto -> percentuali della cornice della slide."""
    return (100 * (box.x0 - frame.x0) / frame.width, 100 * (box.y0 - frame.y0) / frame.height,
            100 * (box.x1 - frame.x0) / frame.width, 100 * (box.y1 - frame.y0) / frame.height)


def fmt_box(b):
    return ",".join(f"{max(0.0, min(100.0, v)):.0f}" for v in b)


# --------------------------------------------------------------- elementi
_CACHE = {}


def elements(page, frame):
    """Immagini, disegni e righe di testo di una slide, con una chiave che resta uguale su ogni slide."""
    cache_key = (page.number, tuple(frame))
    if cache_key in _CACHE:
        return _CACHE[cache_key]
    items = []
    for info in page.get_image_info(xrefs=True):
        box = pymupdf.Rect(info["bbox"]) & frame
        if box.is_empty:
            continue
        r = rel(box, frame)
        items.append(("image", box, ("image", info.get("xref"), tuple(round(v / 2) for v in r))))
    for d in page.get_drawings():
        box = pymupdf.Rect(d["rect"])
        if not frame.contains(box) or (box.width > 0.95 * frame.width and box.height > 0.95 * frame.height):
            continue
        r = rel(box, frame)
        items.append(("drawing", box, ("drawing", tuple(round(v) for v in r))))
    for block in page.get_text("dict", clip=frame)["blocks"]:
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if text:
                box = pymupdf.Rect(line["bbox"])
                key = ("text", re.sub(r"\d+", "#", text), round(rel(box, frame)[1] / 5))
                items.append(("text", box, key, text))
    _CACHE[cache_key] = items
    return items


def template_keys(slides):
    """Chiavi presenti in almeno metà delle slide: loghi, intestazioni, piè di pagina, numeri di pagina."""
    count = collections.Counter()
    for _, page, frame in slides:
        count.update({item[2] for item in elements(page, frame)})
    limit = max(2, len(slides) // 2)
    return {k for k, c in count.items() if c >= limit}


def figure_candidates(page, frame, template):
    items = [it for it in elements(page, frame) if it[2] not in template]
    area = frame.width * frame.height
    found = [("image", it[1]) for it in items if it[0] == "image" and it[1].width * it[1].height > 0.01 * area]
    # unisce i disegni vicini in gruppi (diagrammi, grafici, tabelle disegnate con linee)
    pad = 0.02 * frame.width
    clusters = []
    for it in items:
        if it[0] != "drawing":
            continue
        box = pymupdf.Rect(it[1])
        grown = pymupdf.Rect(box.x0 - pad, box.y0 - pad, box.x1 + pad, box.y1 + pad)
        hit = [c for c in clusters if grown.intersects(c[0])]
        for c in hit:
            clusters.remove(c)
            box |= c[0]
        clusters.append((box, 1 + sum(c[1] for c in hit)))
    found += [("drawing", box) for box, n in clusters if n >= 3 and box.width * box.height > 0.03 * area]
    return sorted(found, key=lambda f: (f[1].y0, f[1].x0))


# ---------------------------------------------------------------- comandi
def cmd_info(doc, slides, args):
    per_page = collections.Counter(page.number for _, page, _ in slides)
    print(f"{args.pdf}: {doc.page_count} pagine, {len(slides)} slide "
          f"({max(per_page.values())} per pagina)")


def cmd_text(doc, slides, args):
    template = template_keys(slides)
    for n in parse_range(args.slides, len(slides)):
        _, page, frame = slides[n - 1]
        lines = [it[3] for it in elements(page, frame) if it[0] == "text" and it[2] not in template]
        print(f"=== slide {n} (pagina {page.number + 1}) ===")
        print("\n".join(lines) if lines else "(nessun testo: guarda la slide renderizzata)")
        print()


def render_slide(page, frame, dpi, grid):
    out = pymupdf.open()
    target = out.new_page(width=frame.width, height=frame.height)
    target.show_pdf_page(target.rect, page.parent, page.number, clip=frame)
    if grid:
        for i in range(1, 10):
            x, y = target.rect.width * i / 10, target.rect.height * i / 10
            target.draw_line((x, 0), (x, target.rect.height), color=(1, 0, 0), width=0.4, dashes="[2] 2")
            target.draw_line((0, y), (target.rect.width, y), color=(1, 0, 0), width=0.4, dashes="[2] 2")
            target.insert_text((x + 1, 7), str(i * 10), fontsize=6, color=(1, 0, 0))
            target.insert_text((1, y - 1), str(i * 10), fontsize=6, color=(1, 0, 0))
    return target.get_pixmap(dpi=dpi, alpha=False)


def cmd_render(doc, slides, args):
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in parse_range(args.slides, len(slides)):
        _, page, frame = slides[n - 1]
        path = out_dir / f"slide-{n:03d}{'-grid' if args.grid else ''}.png"
        render_slide(page, frame, args.dpi, args.grid).save(path)
        print(path)


KIND = {"image": "immagine", "drawing": "disegno"}


def cmd_figures(doc, slides, args):
    template = template_keys(slides)
    for n in parse_range(args.slides, len(slides)):
        _, page, frame = slides[n - 1]
        for i, (kind, box) in enumerate(figure_candidates(page, frame, template), 1):
            r = rel(box, frame)
            print(f"slide {n} (pagina {page.number + 1}) figura {i}: {KIND[kind]:8s} box {fmt_box(r)}"
                  f"  ({(r[2] - r[0]) * (r[3] - r[1]) / 100:.0f}% della slide)")


def cmd_crop(doc, slides, args):
    if not 1 <= args.slide <= len(slides):
        sys.exit(f"slide {args.slide} fuori intervallo 1-{len(slides)}")
    _, page, frame = slides[args.slide - 1]
    if args.box:
        x0, y0, x1, y1 = (float(v) for v in args.box.split(","))
    else:
        figs = figure_candidates(page, frame, template_keys(slides))
        if not figs:
            sys.exit(f"slide {args.slide}: nessuna figura trovata, passa --box dopo aver guardato la slide renderizzata")
        union = figs[0][1]
        for _, box in figs[1:]:
            union |= box
        x0, y0, x1, y1 = rel(union, frame)
        x0, y0, x1, y1 = x0 - args.margin, y0 - args.margin, x1 + args.margin, y1 + args.margin
    clip = pymupdf.Rect(frame.x0 + frame.width * x0 / 100, frame.y0 + frame.height * y0 / 100,
                        frame.x0 + frame.width * x1 / 100, frame.y0 + frame.height * y1 / 100) & frame
    if clip.is_empty:
        sys.exit("riquadro vuoto")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix = page.get_pixmap(clip=clip, dpi=args.dpi, alpha=False)
    pix.save(out)
    print(f"{out}  {pix.width}x{pix.height}px  box {fmt_box(rel(clip, frame))}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("info", "text", "render", "figures", "crop"):
        p = sub.add_parser(name)
        p.add_argument("pdf")
        if name in ("text", "render", "figures"):
            p.add_argument("--slides", help="es. 3-7,10 (predefinito: tutte)")
        if name == "render":
            p.add_argument("--out", default="slides-render")
            p.add_argument("--grid", action="store_true", help="sovrappone una griglia al 10%% per leggere le coordinate")
            p.add_argument("--dpi", type=int, default=150)
        if name == "crop":
            p.add_argument("--slide", type=int, required=True)
            p.add_argument("--box", help="x0,y0,x1,y1 in percentuale della slide")
            p.add_argument("--auto", action="store_true", help="unione delle figure trovate (predefinito senza --box)")
            p.add_argument("--margin", type=float, default=1.0, help="percentuale aggiunta intorno al ritaglio --auto")
            p.add_argument("--dpi", type=int, default=200)
            p.add_argument("--out", required=True)
    args = ap.parse_args()
    # il testo delle slide ha simboli (−, →, •) che la code page della console di Windows non sa stampare
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    doc = pymupdf.open(args.pdf)
    slides = all_slides(doc)
    {"info": cmd_info, "text": cmd_text, "render": cmd_render, "figures": cmd_figures, "crop": cmd_crop}[args.cmd](doc, slides, args)


if __name__ == "__main__":
    main()
