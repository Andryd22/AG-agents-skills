#!/usr/bin/env python3
"""Controlli meccanici su un progetto LaTeX di un corso, prima o dopo la compilazione.

Segue main.tex attraverso \\input e \\include e segnala:
  CRITICO     riferimenti non definiti, label duplicate, file di immagine mancanti,
              tag di citazione ([cite], <source>, ...) che rompono la compilazione
  IMPORTANTE  figure e tabelle senza \\caption o \\label, didascalie dal lato
              sbagliato (tabelle sopra, figure sotto), segnaposto di immagini
              ancora da sostituire, numeri di capitolo/sezione scritti a mano,
              elenchi le cui voci non finiscono tutte con ";" o tutte con ".",
              immagini non chiamate chXY-nome_figura o con XY diverso dal capitolo,
              formule nei titoli fuori da \\texorpdfstring (segnalibri del PDF sbagliati)
  MINORE      file non usati in images/, \\uline, \\tikzstyle, cases invece di dcases,
              formule in display chiuse da virgola o punto

Uso:
    python check_project.py [cartella_progetto] [--main main.tex]

Cerca main.tex in latex/ (i corsi preparati con /latex setup) e poi nella cartella;
se mancano entrambi, controlla ogni latex/<nome>/main.tex: un corso con più
documenti indipendenti, per esempio uno per docente.

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
CHAPTER = re.compile(r"\\chapter(?:\[[^\]]*\])?\{")
IMAGE_NAME = re.compile(r"ch(\d{2})-[a-z0-9]+(?:_[a-z0-9]+)*")
DISPLAY = re.compile(r"(?<!\\)\\\[(.*?)\\\]|\\begin\{(equation|align|gather|multline|flalign)(\*?)\}(.*?)\\end\{\2\3\}", re.S)
DISPLAY_TAIL = re.compile(r"(?:\s|\\\\|\\label\{[^}]*\}|\\nonumber\b|\\notag\b)+$")
LISTING_START = re.compile(r"\\begin\{lstlisting\}\s*\[|\\lstinputlisting\s*\[")
OPTION_LABEL = re.compile(r"(?:^|,)\s*label\s*=\s*\{?\s*([^,{}\s]+)")
HEADING = re.compile(r"\\(?:part|chapter|section|subsection|subsubsection)(?![A-Za-z*])\s*")
TEXORPDF = re.compile(r"\\texorpdfstring\s*")
MATH = re.compile(r"(?<!\\)\$|\\\(")
LIST_TOKEN = re.compile(r"\\begin\{(itemize|enumerate)\}|\\end\{(itemize|enumerate)\}|\\item\b(?:\[[^\]]*\])?")


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in text.split("\n"))


def blank_verbatim(text):
    """Tiene i numeri di riga, toglie i listati di codice (il loro contenuto non è LaTeX)."""
    return VERBATIM.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def listing_labels(text):
    """Label date nelle opzioni dei listati (label={lst:...}), che blank_verbatim toglie insieme al codice."""
    for m in LISTING_START.finditer(text):
        depth, end = 0, m.end()
        while end < len(text) and not (text[end] == "]" and depth == 0):
            depth += {"{": 1, "}": -1}.get(text[end], 0)
            end += 1
        for label in OPTION_LABEL.finditer(text[m.end():end]):
            yield label.group(1), m.start()


def braced(text, start):
    """Contenuto della graffa che si apre in text[start] e posizione dopo quella che la chiude; None se non c'è."""
    if start >= len(text) or text[start] != "{":
        return None
    depth, i = 0, start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        if depth == 0:
            return text[start + 1:i], i + 1
        i += 1
    return None


def title_without_texorpdf(title):
    """Il titolo senza i \\texorpdfstring{...}{...}, per cercare la matematica rimasta fuori."""
    out, pos = [], 0
    for m in TEXORPDF.finditer(title):
        if m.start() < pos:
            continue
        first = braced(title, m.end())
        if not first:
            continue
        rest = first[1]
        while rest < len(title) and title[rest].isspace():
            rest += 1
        second = braced(title, rest)
        if second:
            out.append(title[pos:m.start()])
            pos = second[1]
    return "".join(out) + title[pos:]


def heading_titles(text):
    """(posizione, titolo) dei titoli che vanno nei segnalibri: quello breve tra [] se c'è."""
    for m in HEADING.finditer(text):
        i, short = m.end(), None
        if text[i:i + 1] == "[":
            depth, j = 0, i + 1
            while j < len(text) and not (text[j] == "]" and depth == 0):
                depth += {"{": 1, "}": -1}.get(text[j], 0)
                j += 1
            short, i = text[i + 1:j], j + 1
            while i < len(text) and text[i].isspace():
                i += 1
        full = braced(text, i)
        if full:
            yield m.start(), short if short is not None else full[0]


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


def item_ending(text):
    """Ultimo segno della voce, senza graffe finali; None se finisce con matematica o un ambiente."""
    text = text.rstrip()
    if not text or text.endswith(("\\]", "$$")) or re.search(r"\\end\{[^}]*\}$", text):
        return None
    return text.rstrip("}").rstrip()[-1:] or None


def list_issues(text):
    """Elenchi itemize/enumerate le cui voci non finiscono tutte con ";" o tutte con ".".

    Le voci che contengono un sottoelenco sono escluse (di solito finiscono con ":");
    un elenco di sole domande, tutte chiuse da "?", va bene.
    """
    found, stack, last = [], [], 0
    for m in LIST_TOKEN.finditer(text):
        if stack and stack[-1]["items"]:
            stack[-1]["items"][-1]["text"] += text[last:m.start()]
        last = m.end()
        if m.group(1):
            if stack and stack[-1]["items"]:
                stack[-1]["items"][-1]["nested"] = True
            stack.append({"pos": m.start(), "items": []})
        elif m.group(2):
            if not stack:
                continue
            frame = stack.pop()
            ends = [item_ending(i["text"]) for i in frame["items"] if not i["nested"]]
            ends = [e for e in ends if e is not None]
            if ends and (len(set(ends)) > 1 or ends[0] not in ";.?"):
                found.append((frame["pos"], sorted({e if e in ";.:,!?" else "nessuno" for e in ends})))
        elif stack:
            stack[-1]["items"].append({"text": "", "nested": False})
    return found


def project_roots(folder, main_file):
    """Le radici con main.tex: latex/, la cartella, oppure ogni latex/<nome>/ (corsi con più documenti)."""
    for candidate in (folder / "latex", folder):
        if (candidate / main_file).is_file():
            return [candidate]
    latex = folder / "latex"
    return sorted(sub for sub in latex.iterdir() if (sub / main_file).is_file()) if latex.is_dir() else []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", nargs="?", default=".")
    ap.add_argument("--main", default="main.tex")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    folder = Path(args.project).resolve()
    roots = project_roots(folder, args.main)
    if not roots:
        sys.exit(f"{args.main} non trovato in {folder / 'latex'}, in {folder} o in una sottocartella di latex/")
    critical = []
    for index, root in enumerate(roots):
        if index:
            print()
        critical.append(check(root, args.main))
    sys.exit(1 if any(critical) else 0)


def check(root, main_file):
    """Controlla un progetto e stampa il resoconto; True se ci sono problemi critici."""
    issues = {"CRITICO": [], "IMPORTANTE": [], "MINORE": []}
    labels, refs, used_images = {}, [], set()
    chapter = 0  # capitoli numerati visti nei file precedenti, nell'ordine di main.tex
    for path in collect(root, main_file):
        rel = path.relative_to(root).as_posix()
        source = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        text = blank_verbatim(source)
        for m in LABEL.finditer(text):
            labels.setdefault(m.group(1), []).append(f"{rel}:{line_of(text, m.start())}")
        for name, start in listing_labels(source):
            labels.setdefault(name, []).append(f"{rel}:{line_of(source, start)}")
        for m in REF.finditer(text):
            for name in m.group(1).split(","):
                refs.append((name.strip(), f"{rel}:{line_of(text, m.start())}"))
        for m in GRAPHIC.finditer(text):
            name = m.group(1).strip()
            candidates = [root / name] + [root / (name + ext) for ext in IMAGE_EXT]
            found = next((c for c in candidates if c.is_file()), None)
            if found:
                used_images.add(found.resolve())
                n = chapter + len(CHAPTER.findall(text, 0, m.start()))
                prefix = IMAGE_NAME.fullmatch(found.stem)
                if n and prefix and int(prefix.group(1)) != n:
                    issues["IMPORTANTE"].append(f"{rel}:{line_of(text, m.start())} {found.name} usata nel capitolo {n}: "
                                                f"il nome deve iniziare con ch{n:02d}-")
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
        for pos, ends in list_issues(text):
            issues["IMPORTANTE"].append(f"{rel}:{line_of(text, pos)} elenco: le voci devono finire tutte con ; "
                                        f"o tutte con . (trovati: {' '.join(ends)})")
        chapter += len(CHAPTER.findall(text))
        for m in DISPLAY.finditer(text):
            body = DISPLAY_TAIL.sub("", m.group(1) if m.group(1) is not None else m.group(4))
            if body.endswith((",", ".", ";")) and not body.endswith(("\\,", "\\;")):
                issues["MINORE"].append(f"{rel}:{line_of(text, m.start())} formula in display chiusa da {body[-1]!r}: dopo la formula non va nessun segno")
        for pos, title in heading_titles(text):
            if MATH.search(title_without_texorpdf(title)):
                issues["IMPORTANTE"].append(f"{rel}:{line_of(text, pos)} formula nel titolo fuori da \\texorpdfstring: "
                                            f"{' '.join(title.split())[:70]}")
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
            if not (f.is_file() and f.suffix.lower() in IMAGE_EXT):
                continue
            if not IMAGE_NAME.fullmatch(f.stem):
                issues["IMPORTANTE"].append(f"nome fuori schema: {f.relative_to(root).as_posix()} (usa chXY-nome_figura, XY = capitolo su due cifre)")
            if f.resolve() not in used_images:
                issues["MINORE"].append(f"immagine non usata: {f.relative_to(root).as_posix()}")

    files = collect(root, main_file)
    print(f"Progetto: {root}")
    print(f"{len(files)} file, {len(labels)} label, {len(refs)} riferimenti, {len(used_images)} immagini usate")
    for level, found in issues.items():
        if found:
            print(f"\n{level} ({len(found)})")
            for item in found:
                print(f"  {item}")
    total = sum(len(v) for v in issues.values())
    print(f"\ncritici {len(issues['CRITICO'])}, importanti {len(issues['IMPORTANTE'])}, minori {len(issues['MINORE'])}" if total else "\nnessun problema")
    return bool(issues["CRITICO"])


if __name__ == "__main__":
    main()
