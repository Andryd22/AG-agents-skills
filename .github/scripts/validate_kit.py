#!/usr/bin/env python3
"""Validate the Antigravity Kit (.agents/) before it ships.

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
KIT = ROOT / ".agents"
SKILLS, AGENTS, RULES = (KIT / d for d in ("skills", "agents", "rules"))

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
counts = {"agents": len(agent_names), "skills": len(skill_names)}
# Antigravity retires workflows on 1 November 2026: commands are skills
if (KIT / "workflows").exists():
    err(".agents/workflows/: workflows are retired, turn them into skills")

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
# Antigravity custom agents (.agents/agents/<name>.md). An unknown tool name can hang the subagent.
# Agents inherit every workspace skill; a `skills` key would be resolved from .agents/agents/ and fail,
# so each agent names its skills in the body: "> 📚 Your skills: `a`, `b`."
AGENT_KEYS = {"name", "description", "tools", "mainAgent", "subagent", "model", "commandExecutionPolicy",
              "mcpServers", "skills", "plugins"}
# agy 1.2.7 gives a custom agent only these tools (plus manage_task) and silently drops
# multi_replace_file_content, so it is not accepted here
AGENT_TOOLS = {"view_file", "list_dir", "grep_search", "run_command", "write_to_file", "replace_file_content",
               "invoke_subagent", "define_subagent", "send_message",
               "manage_subagents", "manage_task", "ask_permission", "list_permissions", "ask_question",
               "call_mcp_tool", "find_by_name", "search_web", "read_url_content", "generate_image", "schedule"}
AGENT_MODELS = {"inherit", "flash", "pro"}
EXEC_POLICIES = {"off", "auto", "eager", "sandbox"}
YOUR_SKILLS = re.compile(r"^> 📚 Your skills: (.+?)\. ", re.M)
for p in agent_files:
    data, body = frontmatter(p)
    if data is None:
        continue
    if data.get("name") != p.stem:
        err(f"{rel(p)}: name '{data.get('name')}' differs from file name")
    if not data.get("description"):
        err(f"{rel(p)}: description missing")
    extra = set(data) - AGENT_KEYS
    if extra:
        err(f"{rel(p)}: keys unknown to Antigravity custom agents: {sorted(extra)}")
    if data.get("model", "inherit") not in AGENT_MODELS:
        err(f"{rel(p)}: model '{data.get('model')}' not in {sorted(AGENT_MODELS)}")
    if data.get("commandExecutionPolicy", "sandbox") not in EXEC_POLICIES:
        err(f"{rel(p)}: commandExecutionPolicy '{data.get('commandExecutionPolicy')}' not in {sorted(EXEC_POLICIES)}")
    for tool in data.get("tools") or []:
        if tool not in AGENT_TOOLS:
            err(f"{rel(p)}: tool '{tool}' is not a tool Antigravity gives custom agents")
    if "skills" in data:
        err(f"{rel(p)}: no `skills` key (paths resolve from .agents/agents/ and fail): name them in the body")
    m = YOUR_SKILLS.search(body)
    if not m:
        err(f"{rel(p)}: missing the line '> 📚 Your skills: `a`, `b`.' after the announce line")
    else:
        for s in re.findall(r"`([^`]+)`", m.group(1)):
            if s not in skill_names:
                err(f"{rel(p)}: 'Your skills' names '{s}', which is not a skill")
    if f"🤖 @{p.stem}" not in body:
        err(f"{rel(p)}: missing the announce line with 🤖 @{p.stem}")

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
SKILL_REF = re.compile(r"@\[skills/([\w-]+)\]|\.agents/skills/([\w-]+)/|@\[agents/([\w-]+)\]")
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

# `/name` in backticks is a command: it must be a skill (a few backticked paths are not commands,
# and /agents is an Antigravity CLI built-in)
NOT_COMMANDS = {"g", "nome", "agents"}
for p in doc_files:
    for m in re.finditer(r"`/([a-z][a-z0-9-]*)`", text(p)):
        if m.group(1) not in skill_names and m.group(1) not in NOT_COMMANDS:
            err(f"{rel(p)}: command '/{m.group(1)}' is not a skill")

routing = SKILLS / "intelligent-routing" / "SKILL.md"
if routing.is_file():
    rt = text(routing)
    for a in sorted(agent_names):
        if f"`{a}`" not in rt:
            err(f"{rel(routing)}: agent '{a}' is not in the routing tables")

# ------------------------------------------------------------ master scripts
for p in sorted((KIT / "scripts").glob("*.py")):
    for m in re.finditer(r"\"(\.agents/[\w./-]+\.py)\"", text(p)):
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
WORDS = {"agents": r"agent[si]?", "skills": r"skills?"}
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
for kind, names in (("agent", agent_names), ("skill", skill_names)):
    for n in sorted(names):
        if not re.search(rf"`/?{re.escape(n)}`", arch):
            err(f".agents/ARCHITECTURE.md: {kind} '{n}' not listed")

# ---------------------------------------------------------- installer smoke
def files_in(d):
    return sorted(p.relative_to(d).as_posix() for p in Path(d).rglob("*") if p.is_file()) if Path(d).exists() else []


node = shutil.which("node")
if node:
    installer = ROOT / "bin" / "install.js"
    kit = [f for f in files_in(KIT) if "__pycache__" not in f and not f.endswith(".pyc")]
    with tempfile.TemporaryDirectory() as tmp:
        # 1. empty project: every kit file plus the manifest
        proj = Path(tmp) / "empty"
        proj.mkdir()
        r = subprocess.run([node, str(installer), "init", "-y"], cwd=proj, capture_output=True, text=True)
        got = files_in(proj / ".agents")
        if r.returncode != 0 or got != sorted(kit + [".ag-kit.json"]):
            err(f"installer: init -y into an empty project copied {len(got)}/{len(kit) + 1} files (exit {r.returncode}) {r.stderr.strip()[:200]}")
        # 2. project with its own skill, an entry left by an older kit version and an old .agent/
        proj = Path(tmp) / "existing"
        (proj / ".agents" / "skills" / "mine").mkdir(parents=True)
        (proj / ".agents" / "skills" / "mine" / "SKILL.md").write_text("---\nname: mine\ndescription: own skill\n---\n")
        (proj / ".agents" / "skills" / "old-kit-skill").mkdir()
        (proj / ".agents" / ".ag-kit.json").write_text(json.dumps({"entries": ["skills/old-kit-skill"]}))
        (proj / ".agent").mkdir()
        (proj / ".agent" / "ARCHITECTURE.md").write_text("old kit")
        r = subprocess.run([node, str(installer), "init", "-y"], cwd=proj, capture_output=True, text=True)
        if r.returncode != 0:
            err(f"installer: init -y into an existing project failed (exit {r.returncode}) {r.stderr.strip()[:200]}")
        if not (proj / ".agents" / "skills" / "mine" / "SKILL.md").is_file():
            err("installer: the project's own skill was removed")
        if (proj / ".agents" / "skills" / "old-kit-skill").exists():
            err("installer: an entry of the previous kit version was not removed")
        if (proj / ".agent").exists() or not (proj / ".agent.bak" / "ARCHITECTURE.md").is_file():
            err("installer: the old .agent/ kit folder was not moved to .agent.bak/")
        # 3. running inside the kit itself must refuse and leave .agents/ untouched
        kit_copy = Path(tmp) / "kit"
        shutil.copytree(ROOT / "bin", kit_copy / "bin")
        shutil.copytree(KIT, kit_copy / ".agents")
        shutil.copy(ROOT / "package.json", kit_copy / "package.json")
        before = len(files_in(kit_copy / ".agents"))
        r = subprocess.run([node, "bin/install.js", "init", "-y"], cwd=kit_copy, capture_output=True, text=True)
        after = len(files_in(kit_copy / ".agents"))
        if r.returncode == 0 or after != before:
            err(f"installer: init -y inside the kit must fail and keep .agents/ ({before} -> {after} files, exit {r.returncode})")
else:
    warn("node not found: installer smoke test skipped")

# ------------------------------------------------------------------- report
print(f"Kit: {counts['agents']} agents, {counts['skills']} skills")
for w in warnings:
    print(f"WARNING  {w}")
for e in errors:
    print(f"ERROR    {e}")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
