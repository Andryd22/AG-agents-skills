#!/usr/bin/env python3
"""Mechanical checks on a LaTeX course project, before or after compiling.

Follows main.tex through \\input and \\include and reports:
  CRITICAL  undefined references, duplicate labels, missing image files,
            citation tags ([cite], <source>, ...) that break the compile
  IMPORTANT image placeholders still to replace, chapter/section numbers
            written by hand instead of \\ref
  MINOR     unused files in images/, \\uline, \\tikzstyle, cases instead of dcases

Usage:
    python check_project.py [project_dir] [--main main.tex]

Exit code 1 when there is at least one CRITICAL issue.
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
HAND_NUMBER = re.compile(r"\b(?:Chapter|Section|Sec\.|Chap\.)~?\s?\d+(?:\.\d+)*")
VERBATIM = re.compile(r"\\begin\{(lstlisting|verbatim|minted)\}.*?\\end\{\1\}", re.S)
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".pdf", ".eps")


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in text.split("\n"))


def blank_verbatim(text):
    """Keep line numbers, drop code listings (their content is not LaTeX)."""
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
    if not (root / args.main).is_file():
        sys.exit(f"{root / args.main} not found")

    issues = {"CRITICAL": [], "IMPORTANT": [], "MINOR": []}
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
                issues["CRITICAL"].append(f"{rel}:{line_of(text, m.start())} image file not found: {name}")
        for m in TAGS.finditer(text):
            issues["CRITICAL"].append(f"{rel}:{line_of(text, m.start())} citation tag {m.group(0)!r} breaks the compile")
        for m in re.finditer(r"INSERT IMAGE[^}]*", text):
            issues["IMPORTANT"].append(f"{rel}:{line_of(text, m.start())} placeholder: {m.group(0).strip()}")
        for m in HAND_NUMBER.finditer(text):
            issues["IMPORTANT"].append(f"{rel}:{line_of(text, m.start())} number written by hand: {m.group(0)!r} (use \\ref)")
        for pattern, message in ((r"\\uline\{", "\\uline (use \\textbf)"), (r"\\tikzstyle", "\\tikzstyle is deprecated (use \\tikzset or picture options)"),
                                 (r"\\begin\{cases\}", "cases (use dcases)")):
            for m in re.finditer(pattern, text):
                issues["MINOR"].append(f"{rel}:{line_of(text, m.start())} {message}")

    for name, places in sorted(labels.items()):
        if len(places) > 1:
            issues["CRITICAL"].append(f"label {name!r} defined {len(places)} times: {', '.join(places)}")
    for name, place in refs:
        if name not in labels:
            issues["CRITICAL"].append(f"{place} reference to undefined label {name!r}")
    images_dir = root / "images"
    if images_dir.is_dir():
        for f in sorted(images_dir.rglob("*")):
            if f.is_file() and f.suffix.lower() in IMAGE_EXT and f.resolve() not in used_images:
                issues["MINOR"].append(f"unused image: {f.relative_to(root).as_posix()}")

    files = collect(root, args.main)
    print(f"{len(files)} files, {len(labels)} labels, {len(refs)} references, {len(used_images)} images used")
    for level, found in issues.items():
        if found:
            print(f"\n{level} ({len(found)})")
            for item in found:
                print(f"  {item}")
    total = sum(len(v) for v in issues.values())
    print(f"\n{len(issues['CRITICAL'])} critical, {len(issues['IMPORTANT'])} important, {len(issues['MINOR'])} minor" if total else "\nno issues")
    sys.exit(1 if issues["CRITICAL"] else 0)


if __name__ == "__main__":
    main()
