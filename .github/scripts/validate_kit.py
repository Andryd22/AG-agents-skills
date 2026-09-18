#!/usr/bin/env python3
"""Validate the Antigravity Kit (.agent/) before it ships.

Run from the repository root:  python .github/scripts/validate_kit.py
Needs PyYAML (pip install pyyaml). Node is optional: without it the
installer smoke test is skipped.

Exit code 1 if any ERROR is found. WARNINGS never fail the run.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / ".agent"
SKILLS, AGENTS, WORKFLOWS, RULES = (KIT / d for d in ("skills", "agents", "workflows", "rules"))

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def rel(p):
    return Path(p).relative_to(ROOT).as_posix()


def text(p):
    return Path(p).read_text(encoding="utf-8").replace("\r\n", "\n")


FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def frontmatter(p):
    """Return (dict, body) or (None, text) after recording an error."""
    t = text(p)
    m = FM_RE.match(t)
    if not m:
        err(f"{rel(p)}: missing YAML frontmatter")
        return None, t
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(f"{rel(p)}: invalid YAML frontmatter ({str(e).splitlines()[0]})")
        return None, t
    if not isinstance(data, dict):
        err(f"{rel(p)}: frontmatter is not a mapping")
        return None, t
    body = t[m.end():]
    if re.match(r"\s*---\n[\w-]+\s*:", body):
        err(f"{rel(p)}: second frontmatter block after the first one")
    return data, body


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

# ---------------------------------------------------------------- inventory
skill_dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir())
skill_names = {d.name for d in skill_dirs}
agent_files = sorted(AGENTS.glob("*.md"))
agent_names = {f.stem for f in agent_files}
workflow_files = sorted(WORKFLOWS.glob("*.md"))
workflow_names = {f.stem for f in workflow_files}
counts = {"agents": len(agent_names), "skills": len(skill_names), "workflows": len(workflow_names)}

# ------------------------------------------------------------------- skills
for d in skill_dirs:
    if not (d / "SKILL.md").is_file():
        err(f"{rel(d)}: folder without SKILL.md")
for p in sorted(SKILLS.rglob("SKILL.md")):
    data, _ = frontmatter(p)
    if data is None:
        continue
    top_level = p.parent.parent == SKILLS
    name, desc = data.get("name"), data.get("description")
    if not name or not desc:
        err(f"{rel(p)}: name and description are required")
        continue
    if not NAME_RE.match(str(name)) or len(str(name)) > 64:
        err(f"{rel(p)}: name '{name}' must be lowercase letters, digits and hyphens (max 64)")
    if top_level and name != p.parent.name:
        err(f"{rel(p)}: name '{name}' differs from folder '{p.parent.name}'")
    if len(str(desc)) > 1024:
        err(f"{rel(p)}: description longer than 1024 characters")
    extra = set(data) - SKILL_KEYS
    if extra:
        err(f"{rel(p)}: keys outside the Agent Skills spec: {sorted(extra)} (use metadata:)")
    n = text(p).count("\n")
    if n > 500:
        warn(f"{rel(p)}: {n} lines (spec recommends < 500, move detail to references/)")

# ------------------------------------------------------------------- agents
AGENT_MODELS = {"inherit", "flash", "pro"}
for p in agent_files:
    data, _ = frontmatter(p)
    if data is None:
        continue
    if data.get("name") != p.stem:
        err(f"{rel(p)}: name '{data.get('name')}' differs from file name")
    if not data.get("description"):
        err(f"{rel(p)}: description missing")
    if data.get("model", "inherit") not in AGENT_MODELS:
        err(f"{rel(p)}: model '{data.get('model')}' not in {sorted(AGENT_MODELS)}")
    for s in data.get("skills") or []:
        if s not in skill_names:
            err(f"{rel(p)}: skill '{s}' does not exist")

# ---------------------------------------------------------------- workflows
for p in workflow_files:
    data, _ = frontmatter(p)
    if data is None:
        continue
    if data.get("name") not in (None, p.stem):
        err(f"{rel(p)}: name '{data.get('name')}' differs from file name")
    if not data.get("description"):
        err(f"{rel(p)}: description missing")

# -------------------------------------------------------------------- rules
TRIGGERS = {"always_on", "manual", "model_decision", "glob"}
for p in sorted(RULES.glob("*.md")):
    data, _ = frontmatter(p)
    if len(text(p)) > 12000:
        err(f"{rel(p)}: rules are limited to 12,000 characters")
    if data is None:
        continue
    trig = data.get("trigger")
    if trig not in TRIGGERS:
        err(f"{rel(p)}: trigger '{trig}' not in {sorted(TRIGGERS)}")
    if trig == "model_decision" and not data.get("description"):
        err(f"{rel(p)}: model_decision rules need a description")
    if trig == "glob" and not data.get("globs"):
        err(f"{rel(p)}: glob rules need globs")

# --------------------------------------------------------------- references
AGENT_REF = re.compile(
    r"(?:@|`)([a-z]+(?:-[a-z]+)*-(?:specialist|engineer|architect|writer|agent|planner|manager|owner"
    r"|developer|designer|tester|auditor|optimizer|archaeologist))\b"
)
SKILL_REF = re.compile(r"@\[skills/([\w-]+)\]|\.agent/skills/([\w-]+)/|@\[agents/([\w-]+)\]")
SCRIPT_REF = re.compile(r"(?:[\w./-]*/)?scripts/([\w-]+\.(?:py|sh|js))")
kit_files = {p.name for p in KIT.rglob("*") if p.is_file()}
# skills/README.md is a how-to guide whose examples name skills that do not exist on purpose
doc_files = [p for p in sorted(KIT.rglob("*.md")) if p != SKILLS / "README.md"] + [ROOT / "README.md"]
for p in doc_files:
    t = text(p)
    for m in AGENT_REF.finditer(t):
        if m.group(1) not in agent_names:
            err(f"{rel(p)}: reference to missing agent '{m.group(1)}'")
    for m in SKILL_REF.finditer(t):
        s, s2, a = m.groups()
        if (s or s2) and (s or s2) not in skill_names:
            err(f"{rel(p)}: reference to missing skill '{s or s2}'")
        if a and a not in agent_names:
            err(f"{rel(p)}: reference to missing agent '{a}'")
    for m in SCRIPT_REF.finditer(t):
        if m.group(1) not in kit_files and not (ROOT / m.group(0)).is_file():
            err(f"{rel(p)}: reference to missing script '{m.group(0)}'")

routing = SKILLS / "intelligent-routing" / "SKILL.md"
if routing.is_file():
    rt = text(routing)
    for a in sorted(agent_names):
        if f"`{a}`" not in rt:
            err(f"{rel(routing)}: agent '{a}' is not in the routing tables")

# ------------------------------------------------------------ master scripts
for p in sorted((KIT / "scripts").glob("*.py")):
    for m in re.finditer(r"\"(\.agent/[\w./-]+\.py)\"", text(p)):
        if not (ROOT / m.group(1)).is_file():
            err(f"{rel(p)}: runs missing script {m.group(1)}")

# ------------------------------------------------------------ python / json
for p in sorted(KIT.rglob("*.py")):
    try:
        compile(text(p), str(p), "exec")
    except SyntaxError as e:
        err(f"{rel(p)}: syntax error line {e.lineno}: {e.msg}")
json_files = sorted(KIT.rglob("*.json")) + [ROOT / "package.json", ROOT / "package-lock.json"]
parsed = {}
for p in json_files:
    if p.is_file():
        try:
            parsed[p.name] = json.loads(text(p))
        except json.JSONDecodeError as e:
            err(f"{rel(p)}: invalid JSON ({e.msg}, line {e.lineno})")
pkg, lock = parsed.get("package.json", {}), parsed.get("package-lock.json", {})
if lock and pkg.get("version") != lock.get("version"):
    err(f"package-lock.json version {lock.get('version')} != package.json {pkg.get('version')}")

# ------------------------------------------------------------ generated junk
ignore = text(ROOT / ".gitignore") if (ROOT / ".gitignore").is_file() else ""
if "__pycache__" not in ignore:
    err(".gitignore: __pycache__/ missing")
if (ROOT / ".git").exists() and shutil.which("git"):
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for f in tracked:
        if "__pycache__" in f or f.endswith(".pyc"):
            err(f"{f}: compiled Python file tracked by git")

# ------------------------------------------------------------------- counts
WORDS = {"agents": r"agent[si]?", "skills": r"skills?", "workflows": r"workflows?"}
COUNT_PATTERNS = [
    r"(\d+)\s+(?:specialist\s+)?({w})\b",          # "18 agents", "30 Skills"
    r"({w})\s*\((\d+)\)",                          # "Agents (18)"
    r"\*\*(?:total\s+)?({w})\*\*\s*\|\s*(\d+)",   # "| **Agenti** | 18 |"
]
count_docs = [ROOT / "README.md", KIT / "ARCHITECTURE.md"]
for p in count_docs:
    t = text(p)
    for key, w in WORDS.items():
        for pat in COUNT_PATTERNS:
            for m in re.finditer(pat.format(w=w), t, re.I):
                num = next(g for g in m.groups() if g.isdigit())
                if int(num) != counts[key]:
                    err(f"{rel(p)}: says {m.group(0)!r}, disk has {counts[key]} {key}")
desc = pkg.get("description", "")
for key, w in WORDS.items():
    for m in re.finditer(COUNT_PATTERNS[0].format(w=w), desc, re.I):
        if int(m.group(1)) != counts[key]:
            err(f"package.json description says {m.group(0)!r}, disk has {counts[key]} {key}")

arch = text(KIT / "ARCHITECTURE.md")
for kind, names in (("agent", agent_names), ("skill", skill_names), ("workflow", workflow_names)):
    for n in sorted(names):
        if not re.search(rf"`/?{re.escape(n)}`", arch):
            err(f".agent/ARCHITECTURE.md: {kind} '{n}' not listed")

# ---------------------------------------------------------- installer smoke
node = shutil.which("node")
if node:
    installer = ROOT / "bin" / "install.js"
    expected = sum(1 for p in KIT.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([node, str(installer), "init", "-y"], cwd=tmp, capture_output=True, text=True)
        got = sum(1 for p in (Path(tmp) / ".agent").rglob("*") if p.is_file()) if (Path(tmp) / ".agent").exists() else 0
        if r.returncode != 0 or got != expected:
            err(f"installer: init -y into empty project copied {got}/{expected} files (exit {r.returncode}) {r.stderr.strip()[:200]}")
        # running inside the kit itself must refuse and leave .agent/ untouched
        kit_copy = Path(tmp) / "kit"
        shutil.copytree(ROOT / "bin", kit_copy / "bin")
        shutil.copytree(KIT, kit_copy / ".agent")
        shutil.copy(ROOT / "package.json", kit_copy / "package.json")
        before = sum(1 for p in (kit_copy / ".agent").rglob("*") if p.is_file())
        r = subprocess.run([node, "bin/install.js", "init", "-y"], cwd=kit_copy, capture_output=True, text=True)
        after = sum(1 for p in (kit_copy / ".agent").rglob("*") if p.is_file())
        if r.returncode == 0 or after != before:
            err(f"installer: init -y inside the kit must fail and keep .agent/ ({before} -> {after} files, exit {r.returncode})")
else:
    warn("node not found: installer smoke test skipped")

# ------------------------------------------------------------------- report
print(f"Kit: {counts['agents']} agents, {counts['skills']} skills, {counts['workflows']} workflows")
for w in warnings:
    print(f"WARNING  {w}")
for e in errors:
    print(f"ERROR    {e}")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
