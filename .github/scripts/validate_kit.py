#!/usr/bin/env python3
"""Controlla l'Antigravity Kit (.agents/) prima di pubblicarlo.

Si lancia dalla radice del repository:  python .github/scripts/validate_kit.py
Serve PyYAML (pip install pyyaml). Node è facoltativo: senza, la prova
dell'installer viene saltata.

Codice di uscita 1 se c'è almeno un ERRORE. Gli AVVISI non fanno mai fallire.
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
    sys.exit("PyYAML mancante: pip install pyyaml")

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
    """Restituisce (dict, corpo), oppure (None, testo) dopo aver registrato un errore."""
    t = text(p)
    m = FM_RE.match(t)
    if not m:
        err(f"{rel(p)}: manca il frontmatter YAML")
        return None, t
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(f"{rel(p)}: frontmatter YAML non valido ({str(e).splitlines()[0]})")
        return None, t
    if not isinstance(data, dict):
        err(f"{rel(p)}: il frontmatter non è una mappa chiave-valore")
        return None, t
    body = t[m.end():]
    if re.match(r"\s*---\n[\w-]+\s*:", body):
        err(f"{rel(p)}: secondo blocco di frontmatter dopo il primo")
    return data, body


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

# ---------------------------------------------------------------- inventario
skill_dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir())
skill_names = {d.name for d in skill_dirs}
agent_files = sorted(AGENTS.glob("*.md"))
agent_names = {f.stem for f in agent_files}
counts = {"agents": len(agent_names), "skills": len(skill_names)}
# Antigravity ritira i workflow il 1° novembre 2026: i comandi sono skill
if (KIT / "workflows").exists():
    err(".agents/workflows/: i workflow sono ritirati, trasformali in skill")

# ------------------------------------------------------------------- skills
for d in skill_dirs:
    if not (d / "SKILL.md").is_file():
        err(f"{rel(d)}: cartella senza SKILL.md")
for p in sorted(SKILLS.rglob("SKILL.md")):
    data, _ = frontmatter(p)
    if data is None:
        continue
    top_level = p.parent.parent == SKILLS
    name, desc = data.get("name"), data.get("description")
    if not name or not desc:
        err(f"{rel(p)}: name e description sono obbligatori")
        continue
    if not NAME_RE.match(str(name)) or len(str(name)) > 64:
        err(f"{rel(p)}: name '{name}' deve avere solo lettere minuscole, cifre e trattini (massimo 64)")
    if top_level and name != p.parent.name:
        err(f"{rel(p)}: name '{name}' è diverso dalla cartella '{p.parent.name}'")
    if len(str(desc)) > 1024:
        err(f"{rel(p)}: description più lunga di 1024 caratteri")
    extra = set(data) - SKILL_KEYS
    if extra:
        err(f"{rel(p)}: chiavi fuori dalla spec Agent Skills: {sorted(extra)} (usa metadata:)")
    n = text(p).count("\n")
    if n > 500:
        warn(f"{rel(p)}: {n} righe (la spec consiglia < 500, sposta i dettagli in references/)")

# ------------------------------------------------------------------- agenti
# Custom agent di Antigravity (.agents/agents/<nome>.md). Un nome di strumento sconosciuto può bloccare il subagent.
# Gli agenti ereditano tutte le skill del workspace; una chiave `skills` verrebbe risolta da .agents/agents/ e fallirebbe,
# quindi ogni agente nomina le sue skill nel corpo: "> 📚 Le tue skill: `a`, `b`."
AGENT_KEYS = {"name", "description", "tools", "mainAgent", "subagent", "model", "commandExecutionPolicy",
              "mcpServers", "skills", "plugins"}
# agy 1.2.7 dà a un custom agent solo questi strumenti (più manage_task) e scarta senza avvisare
# multi_replace_file_content, quindi qui non è accettato
AGENT_TOOLS = {"view_file", "list_dir", "grep_search", "run_command", "write_to_file", "replace_file_content",
               "invoke_subagent", "define_subagent", "send_message",
               "manage_subagents", "manage_task", "ask_permission", "list_permissions", "ask_question",
               "call_mcp_tool", "find_by_name", "search_web", "read_url_content", "generate_image", "schedule"}
AGENT_MODELS = {"inherit", "flash", "pro"}
EXEC_POLICIES = {"off", "auto", "eager", "sandbox"}
YOUR_SKILLS = re.compile(r"^> 📚 Le tue skill: (.+?)\. ", re.M)
for p in agent_files:
    data, body = frontmatter(p)
    if data is None:
        continue
    if data.get("name") != p.stem:
        err(f"{rel(p)}: name '{data.get('name')}' è diverso dal nome del file")
    if not data.get("description"):
        err(f"{rel(p)}: manca la description")
    extra = set(data) - AGENT_KEYS
    if extra:
        err(f"{rel(p)}: chiavi sconosciute ai custom agent di Antigravity: {sorted(extra)}")
    if data.get("model", "inherit") not in AGENT_MODELS:
        err(f"{rel(p)}: model '{data.get('model')}' non è tra {sorted(AGENT_MODELS)}")
    if data.get("commandExecutionPolicy", "sandbox") not in EXEC_POLICIES:
        err(f"{rel(p)}: commandExecutionPolicy '{data.get('commandExecutionPolicy')}' non è tra {sorted(EXEC_POLICIES)}")
    for tool in data.get("tools") or []:
        if tool not in AGENT_TOOLS:
            err(f"{rel(p)}: '{tool}' non è uno strumento che Antigravity dà ai custom agent")
    if "skills" in data:
        err(f"{rel(p)}: niente chiave `skills` (i percorsi si risolvono da .agents/agents/ e falliscono): nominale nel corpo")
    m = YOUR_SKILLS.search(body)
    if not m:
        err(f"{rel(p)}: manca la riga '> 📚 Le tue skill: `a`, `b`.' dopo la riga di annuncio")
    else:
        for s in re.findall(r"`([^`]+)`", m.group(1)):
            if s not in skill_names:
                err(f"{rel(p)}: 'Le tue skill' nomina '{s}', che non è una skill")
    if f"🤖 @{p.stem}" not in body:
        err(f"{rel(p)}: manca la riga di annuncio con 🤖 @{p.stem}")

# -------------------------------------------------------------------- regole
TRIGGERS = {"always_on", "manual", "model_decision", "glob"}
for p in sorted(RULES.glob("*.md")):
    data, _ = frontmatter(p)
    if len(text(p)) > 12000:
        err(f"{rel(p)}: le regole hanno un limite di 12.000 caratteri")
    if data is None:
        continue
    trig = data.get("trigger")
    if trig not in TRIGGERS:
        err(f"{rel(p)}: trigger '{trig}' non è tra {sorted(TRIGGERS)}")
    if trig == "model_decision" and not data.get("description"):
        err(f"{rel(p)}: le regole model_decision vogliono una description")
    if trig == "glob" and not data.get("globs"):
        err(f"{rel(p)}: le regole glob vogliono globs")

# --------------------------------------------------------------- riferimenti
AGENT_REF = re.compile(
    r"(?:@|`)([a-z]+(?:-[a-z]+)*-(?:specialist|engineer|architect|writer|agent|planner|manager|owner"
    r"|developer|designer|tester|auditor|optimizer|archaeologist))\b"
)
SKILL_REF = re.compile(r"@\[skills/([\w-]+)\]|\.agents/skills/([\w-]+)/|@\[agents/([\w-]+)\]")
SCRIPT_REF = re.compile(r"(?:[\w./-]*/)?scripts/([\w-]+\.(?:py|sh|js))")
kit_files = {p.name for p in KIT.rglob("*") if p.is_file()}
# skills/README.md è una guida i cui esempi nominano apposta skill che non esistono
doc_files = [p for p in sorted(KIT.rglob("*.md")) if p != SKILLS / "README.md"] + [ROOT / "README.md"]
for p in doc_files:
    t = text(p)
    for m in AGENT_REF.finditer(t):
        if m.group(1) not in agent_names:
            err(f"{rel(p)}: riferimento all'agente inesistente '{m.group(1)}'")
    for m in SKILL_REF.finditer(t):
        s, s2, a = m.groups()
        if (s or s2) and (s or s2) not in skill_names:
            err(f"{rel(p)}: riferimento alla skill inesistente '{s or s2}'")
        if a and a not in agent_names:
            err(f"{rel(p)}: riferimento all'agente inesistente '{a}'")
    for m in SCRIPT_REF.finditer(t):
        if m.group(1) not in kit_files and not (ROOT / m.group(0)).is_file():
            err(f"{rel(p)}: riferimento allo script inesistente '{m.group(0)}'")

# `/nome` tra backtick è un comando: deve essere una skill (alcuni percorsi tra backtick non sono comandi,
# e /agents è un comando integrato della CLI di Antigravity)
NOT_COMMANDS = {"g", "nome", "agents"}
for p in doc_files:
    for m in re.finditer(r"`/([a-z][a-z0-9-]*)`", text(p)):
        if m.group(1) not in skill_names and m.group(1) not in NOT_COMMANDS:
            err(f"{rel(p)}: il comando '/{m.group(1)}' non è una skill")

routing = SKILLS / "intelligent-routing" / "SKILL.md"
if routing.is_file():
    rt = text(routing)
    for a in sorted(agent_names):
        if f"`{a}`" not in rt:
            err(f"{rel(routing)}: l'agente '{a}' non è nelle tabelle del routing")

# ------------------------------------------------------------ script master
for p in sorted((KIT / "scripts").glob("*.py")):
    for m in re.finditer(r"\"(\.agents/[\w./-]+\.py)\"", text(p)):
        if not (ROOT / m.group(1)).is_file():
            err(f"{rel(p)}: lancia uno script inesistente: {m.group(1)}")

# ------------------------------------------------------------ python / json
for p in sorted(KIT.rglob("*.py")):
    try:
        compile(text(p), str(p), "exec")
    except SyntaxError as e:
        err(f"{rel(p)}: errore di sintassi alla riga {e.lineno}: {e.msg}")
json_files = sorted(KIT.rglob("*.json")) + [ROOT / "package.json", ROOT / "package-lock.json"]
parsed = {}
for p in json_files:
    if p.is_file():
        try:
            parsed[p.name] = json.loads(text(p))
        except json.JSONDecodeError as e:
            err(f"{rel(p)}: JSON non valido ({e.msg}, riga {e.lineno})")
pkg, lock = parsed.get("package.json", {}), parsed.get("package-lock.json", {})
if lock and pkg.get("version") != lock.get("version"):
    err(f"versione di package-lock.json {lock.get('version')} != package.json {pkg.get('version')}")

# ------------------------------------------------------------ file generati
ignore = text(ROOT / ".gitignore") if (ROOT / ".gitignore").is_file() else ""
if "__pycache__" not in ignore:
    err(".gitignore: manca __pycache__/")
if (ROOT / ".git").exists() and shutil.which("git"):
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for f in tracked:
        if "__pycache__" in f or f.endswith(".pyc"):
            err(f"{f}: file Python compilato tracciato da git")

# ------------------------------------------------------------------- conteggi
WORDS = {"agents": r"agent[si]?", "skills": r"skills?"}   # inglese e italiano ("agenti", "skill")
LABEL = {"agents": "agenti", "skills": "skill"}
COUNT_PATTERNS = [
    r"(\d+)\s+(?:specialist\s+)?({w})\b",          # "12 agenti", "32 skill"
    r"({w})\s*\((\d+)\)",                          # "Agenti (12)"
    r"\*\*(?:total\s+)?({w})\*\*\s*\|\s*(\d+)",   # "| **Agenti** | 12 |"
]
count_docs = [ROOT / "README.md", KIT / "ARCHITECTURE.md"]
for p in count_docs:
    t = text(p)
    for key, w in WORDS.items():
        for pat in COUNT_PATTERNS:
            for m in re.finditer(pat.format(w=w), t, re.I):
                num = next(g for g in m.groups() if g.isdigit())
                if int(num) != counts[key]:
                    err(f"{rel(p)}: dice {m.group(0)!r}, su disco ci sono {counts[key]} {LABEL[key]}")
desc = pkg.get("description", "")
for key, w in WORDS.items():
    for m in re.finditer(COUNT_PATTERNS[0].format(w=w), desc, re.I):
        if int(m.group(1)) != counts[key]:
            err(f"la description di package.json dice {m.group(0)!r}, su disco ci sono {counts[key]} {LABEL[key]}")

arch = text(KIT / "ARCHITECTURE.md")
for kind, names in (("agente", agent_names), ("skill", skill_names)):
    for n in sorted(names):
        if not re.search(rf"`/?{re.escape(n)}`", arch):
            err(f".agents/ARCHITECTURE.md: {kind} '{n}' non elencato")

# ---------------------------------------------------------- prova dell'installer
def files_in(d):
    return sorted(p.relative_to(d).as_posix() for p in Path(d).rglob("*") if p.is_file()) if Path(d).exists() else []


node = shutil.which("node")
if node:
    installer = ROOT / "bin" / "install.js"
    kit = [f for f in files_in(KIT) if "__pycache__" not in f and not f.endswith(".pyc")]
    with tempfile.TemporaryDirectory() as tmp:
        # 1. progetto vuoto: tutti i file del kit più il manifest
        proj = Path(tmp) / "empty"
        proj.mkdir()
        r = subprocess.run([node, str(installer), "init", "-y"], cwd=proj, capture_output=True, text=True)
        got = files_in(proj / ".agents")
        if r.returncode != 0 or got != sorted(kit + [".ag-kit.json"]):
            err(f"installer: init -y in un progetto vuoto ha copiato {len(got)}/{len(kit) + 1} file (uscita {r.returncode}) {r.stderr.strip()[:200]}")
        # 2. progetto con una sua skill, una voce lasciata da una vecchia versione del kit e una vecchia .agent/
        proj = Path(tmp) / "existing"
        (proj / ".agents" / "skills" / "mine").mkdir(parents=True)
        (proj / ".agents" / "skills" / "mine" / "SKILL.md").write_text("---\nname: mine\ndescription: own skill\n---\n")
        (proj / ".agents" / "skills" / "old-kit-skill").mkdir()
        (proj / ".agents" / ".ag-kit.json").write_text(json.dumps({"entries": ["skills/old-kit-skill"]}))
        (proj / ".agent").mkdir()
        (proj / ".agent" / "ARCHITECTURE.md").write_text("old kit")
        r = subprocess.run([node, str(installer), "init", "-y"], cwd=proj, capture_output=True, text=True)
        if r.returncode != 0:
            err(f"installer: init -y in un progetto esistente è fallito (uscita {r.returncode}) {r.stderr.strip()[:200]}")
        if not (proj / ".agents" / "skills" / "mine" / "SKILL.md").is_file():
            err("installer: ha tolto la skill del progetto")
        if (proj / ".agents" / "skills" / "old-kit-skill").exists():
            err("installer: non ha tolto una voce della versione precedente del kit")
        if (proj / ".agent").exists() or not (proj / ".agent.bak" / "ARCHITECTURE.md").is_file():
            err("installer: non ha spostato la vecchia cartella .agent/ in .agent.bak/")
        # 3. lanciato dentro il kit stesso deve rifiutarsi e lasciare .agents/ intatta
        kit_copy = Path(tmp) / "kit"
        shutil.copytree(ROOT / "bin", kit_copy / "bin")
        shutil.copytree(KIT, kit_copy / ".agents")
        shutil.copy(ROOT / "package.json", kit_copy / "package.json")
        before = len(files_in(kit_copy / ".agents"))
        r = subprocess.run([node, "bin/install.js", "init", "-y"], cwd=kit_copy, capture_output=True, text=True)
        after = len(files_in(kit_copy / ".agents"))
        if r.returncode == 0 or after != before:
            err(f"installer: init -y dentro il kit deve fallire e lasciare .agents/ ({before} -> {after} file, uscita {r.returncode})")
else:
    warn("node non trovato: prova dell'installer saltata")

# ------------------------------------------------------------------- report
print(f"Kit: {counts['agents']} agenti, {counts['skills']} skill")
for w in warnings:
    print(f"AVVISO   {w}")
for e in errors:
    print(f"ERRORE   {e}")
print(f"\nerrori: {len(errors)}, avvisi: {len(warnings)}")
sys.exit(1 if errors else 0)
