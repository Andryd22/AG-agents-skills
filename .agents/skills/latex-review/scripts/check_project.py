#!/usr/bin/env python3
"""Controlli meccanici su un progetto LaTeX di un corso, prima o dopo la compilazione.

Segue main.tex attraverso \\input e \\include e segnala:
  CRITICO     riferimenti non definiti, label duplicate, file di immagine mancanti,
              tag di citazione ([cite], <source>, ...) che rompono la compilazione
  IMPORTANTE  figure e tabelle senza \\caption o \\label, didascalie dal lato
              sbagliato (tabelle sopra, figure sotto), segnaposto di immagini
              ancora da sostituire, numeri di capitolo/sezione scritti a mano
  MINORE      file non usati in images/, \\uline, \\tikzstyle, cases invece di dcases

Uso:
    python check_project.py [cartella_progetto] [--main main.tex]

Se nella cartella non c'è main.tex ma c'è latex/main.tex (i corsi preparati con
/latex setup), controlla latex/.

Codice di uscita 1 se c'è almeno un problema CRITICO.
"""
import argparse
import re
import sys
from pathlib import Path

INCLUDE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|eqref|pageref|autoref|cref|Cref|nameref)\{([^}]+)\}")
GRAPHIC = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
TAGS = re.compile(r"\[cite[^\]]*\]|<source>|\[source\]|<ref>|\[citation\]|<citation>|:contentReference\[")
HAND_NUMBER = re.compile(r"\b(?:Chapter|Section|Sec\.|Chap\.|Capitolo|Sezione|Cap\.|Sez\.)~?\s?\d+(?:\.\d+)*")
PLACEHOLDER = re.compile(r"(?:INSERT IMAGE|INSERISCI IMMAGINE)[^}]*")
FLOAT = re.compile(r"\\begin\{(figure|table)\*?\}(.*?)\\end\{\1\*?\}", re.S)
BODY = {"figure": re.compile(r"\\includegraphics|\\begin\{tikzpicture\}|\\fbox|\\begin\{subfigure\}"),
        "table": re.compile(r"\\begin\{(?:tabular|tabularx|longtable)\*?\}")}
VERBATIM = re.compile(r"\\begin\{(lstlisting|verbatim|minted)\}.*?\\end\{\1\}", re.S)
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".pdf", ".eps")


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in text.split("\n"))


def blank_verbatim(text):
    """Tiene i numeri di riga, toglie i listati di codice (il loro contenuto non è LaTeX)."""
    return VERBATIM.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def collect(root, main):
    files, queue = [], [root / main]
    while queue:
        path = queue.pop(0)
        if path.suffix != ".tex":
            path = path.with_suffix(".tex")
        if not path.is_file() or path in files:
            continue
        files.append(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        queue += [root / name for name in INCLUDE.findall(text)]
    return files


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", nargs="?", default=".")
    ap.add_argument("--main", default="main.tex")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = Path(args.project).resolve()
    if not (root / args.main).is_file() and (root / "latex" / args.main).is_file():
        root = root / "latex"  # corso preparato con /latex setup: il progetto sta in latex/
    if not (root / args.main).is_file():
        sys.exit(f"{root / args.main} non trovato")

    issues = {"CRITICO": [], "IMPORTANTE": [], "MINORE": []}
    labels, refs, used_images = {}, [], set()
    for path in collect(root, args.main):
        rel = path.relative_to(root).as_posix()
        text = blank_verbatim(strip_comments(path.read_text(encoding="utf-8", errors="replace")))
        for m in LABEL.finditer(text):
            labels.setdefault(m.group(1), []).append(f"{rel}:{line_of(text, m.start())}")
        for m in REF.finditer(text):
            for name in m.group(1).split(","):
                refs.append((name.strip(), f"{rel}:{line_of(text, m.start())}"))
        for m in GRAPHIC.finditer(text):
            name = m.group(1).strip()
            candidates = [root / name] + [root / (name + ext) for ext in IMAGE_EXT]
            found = next((c for c in candidates if c.is_file()), None)
            if found:
                used_images.add(found.resolve())
            else:
                issues["CRITICO"].append(f"{rel}:{line_of(text, m.start())} file di immagine non trovato: {name}")
        for m in TAGS.finditer(text):
            issues["CRITICO"].append(f"{rel}:{line_of(text, m.start())} il tag di citazione {m.group(0)!r} rompe la compilazione")
        for m in FLOAT.finditer(text):
            kind, body = m.group(1), m.group(2)
            where = f"{rel}:{line_of(text, m.start())} {'figura' if kind == 'figure' else 'tabella'}"
            if "\\caption" not in body:
                issues["IMPORTANTE"].append(f"{where} senza \\caption")
                continue
            if "\\label" not in body:
                issues["IMPORTANTE"].append(f"{where} senza \\label")
            content = BODY[kind].search(body)
            if content and "subfigure" not in content.group(0):
                caption_first = body.index("\\caption") < content.start()
                if kind == "table" and not caption_first:
                    issues["IMPORTANTE"].append(f"{where}: didascalia sotto la tabella (va sopra)")
                if kind == "figure" and caption_first:
                    issues["IMPORTANTE"].append(f"{where}: didascalia sopra la figura (va sotto)")
        for m in PLACEHOLDER.finditer(text):
            issues["IMPORTANTE"].append(f"{rel}:{line_of(text, m.start())} segnaposto: {m.group(0).strip()}")
        for m in HAND_NUMBER.finditer(text):
            issues["IMPORTANTE"].append(f"{rel}:{line_of(text, m.start())} numero scritto a mano: {m.group(0)!r} (usa \\ref)")
        for pattern, message in ((r"\\uline\{", "\\uline (usa \\textbf)"), (r"\\tikzstyle", "\\tikzstyle è deprecato (usa \\tikzset o le opzioni della figura)"),
                                 (r"\\begin\{cases\}", "cases (usa dcases)")):
            for m in re.finditer(pattern, text):
                issues["MINORE"].append(f"{rel}:{line_of(text, m.start())} {message}")

    for name, places in sorted(labels.items()):
        if len(places) > 1:
            issues["CRITICO"].append(f"label {name!r} definita {len(places)} volte: {', '.join(places)}")
    for name, place in refs:
        if name not in labels:
            issues["CRITICO"].append(f"{place} riferimento alla label non definita {name!r}")
    images_dir = root / "images"
    if images_dir.is_dir():
        for f in sorted(images_dir.rglob("*")):
            if f.is_file() and f.suffix.lower() in IMAGE_EXT and f.resolve() not in used_images:
                issues["MINORE"].append(f"immagine non usata: {f.relative_to(root).as_posix()}")

    files = collect(root, args.main)
    print(f"Progetto: {root}")
    print(f"{len(files)} file, {len(labels)} label, {len(refs)} riferimenti, {len(used_images)} immagini usate")
    for level, found in issues.items():
        if found:
            print(f"\n{level} ({len(found)})")
            for item in found:
                print(f"  {item}")
    total = sum(len(v) for v in issues.values())
    print(f"\ncritici {len(issues['CRITICO'])}, importanti {len(issues['IMPORTANTE'])}, minori {len(issues['MINORE'])}" if total else "\nnessun problema")
    sys.exit(1 if issues["CRITICO"] else 0)


if __name__ == "__main__":
    main()
