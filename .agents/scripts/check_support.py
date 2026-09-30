"""Esecuzione e report comuni: un controllo saltato non è un controllo superato."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import time

KIT_ROOT = Path(__file__).resolve().parents[2]
STATUSES = ("passed", "failed", "skipped", "not_applicable")
CHECKS = [
    ("Schema (audit euristico)", ".agents/skills/database-design/scripts/schema_validator.py", []),
    ("Test del progetto", ".agents/skills/test/scripts/test_runner.py", ["--json"]),
    ("UX (audit statico)", ".agents/skills/frontend-design/scripts/ux_audit.py", ["--json"]),
]
EXTRA_CHECKS = [
    ("API (audit statico)", ".agents/skills/api-patterns/scripts/api_validator.py", []),
    ("Accessibilità (audit statico)", ".agents/skills/frontend-design/scripts/accessibility_checker.py", []),
]


def final_json(output):
    """Legge l'ultimo oggetto JSON, anche dopo il resoconto testuale di uno script."""
    decoder = json.JSONDecoder()
    for index, char in enumerate(output):
        if char != "{":
            continue
        try:
            data, end = decoder.raw_decode(output[index:])
            if isinstance(data, dict) and not output[index + end:].strip():
                return data
        except ValueError:
            continue
    return None


def latex_roots(project):
    """main.tex in latex/ o in radice; se mancano, un progetto per ogni sottocartella di latex/ (es. uno per docente)."""
    for candidate in (project / "latex", project):
        if (candidate / "main.tex").is_file():
            return [candidate]
    latex = project / "latex"
    return sorted(sub for sub in latex.iterdir() if (sub / "main.tex").is_file()) if latex.is_dir() else []


def run_script(name, script, target, extra=(), timeout=300, structured=True):
    start = time.monotonic()
    if not script.is_file():
        return {"name": name, "status": "failed", "message": f"Script mancante: {script}"}
    try:
        process = subprocess.run([sys.executable, str(script), str(target), *extra],
                                 capture_output=True, text=True, encoding="utf-8",
                                 errors="replace", timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"name": name, "status": "failed", "message": str(error)}
    data = final_json(process.stdout)
    status = data.get("status") if data else None
    if status == "success":
        status = "passed"
    if process.returncode != 0:
        status = "failed"
    elif status not in STATUSES:
        status = "failed" if structured else "passed"
    message = data.get("message", data.get("summary", "")) if data else ""
    if structured and process.returncode == 0 and (not data or data.get("status") not in (*STATUSES, "success")):
        message = "Lo script non ha restituito uno stato di verifica valido"
    return {"name": name, "status": status, "message": message,
            "duration": round(time.monotonic() - start, 2),
            "output": process.stdout, "error": process.stderr, "details": data}


def summarize(results):
    counts = dict.fromkeys(STATUSES, 0)
    counts.update(Counter(result["status"] for result in results))
    status = "passed"
    if counts["failed"]:
        status = "failed"
    elif counts["skipped"] or not counts["passed"]:
        status = "incomplete"
    return {"status": status, "counts": counts, "results": results,
            "scope": "Solo i controlli elencati; gli audit statici non sostituiscono compilazione, lint o test funzionali."}


def print_report(report, json_only=False):
    if not json_only:
        for result in report["results"]:
            print(f"[{result['status']}] {result['name']}: {result.get('message', '')}")
            if result["status"] == "failed":
                print(result.get("output", ""))
                print(result.get("error", ""))
        print(f"Esito: {report['status']} — {report['scope']}")
    print(json.dumps(report, indent=2, ensure_ascii=False))


def main(full=False):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Controlli pertinenti al progetto, con risultati espliciti")
    parser.add_argument("project")
    parser.add_argument("--url", help="URL per lo smoke test nel browser")
    parser.add_argument("--json", action="store_true", help="solo report JSON, inclusi output ed errori")
    parser.add_argument("--no-e2e", "--skip-performance", dest="no_e2e", action="store_true")
    parser.add_argument("--stop-on-fail", action="store_true")
    args = parser.parse_args()
    project = Path(args.project).resolve()
    if not project.is_dir():
        print_report(summarize([{"name": "Progetto", "status": "failed", "message": "Cartella inesistente"}]), args.json)
        return 1
    roots = latex_roots(project)
    results = []
    for name, relative, extra in CHECKS + (EXTRA_CHECKS if full else []):
        result = run_script(name, KIT_ROOT / relative, project, extra)
        if relative.endswith("test_runner.py") and result["status"] == "skipped" and roots:
            if not any((project / name).exists() for name in ("package.json", "pyproject.toml", "requirements.txt")):
                result.update(status="not_applicable", message="Progetto LaTeX senza una suite software configurata")
        results.append(result)
        if args.stop_on_fail and result["status"] == "failed":
            break
    if not (args.stop_on_fail and any(result["status"] == "failed" for result in results)):
        for root in roots:
            where = "" if len(roots) == 1 else f" {root.relative_to(project).as_posix()}"
            results.append(run_script(f"LaTeX{where} (struttura; non compilazione)",
                                      KIT_ROOT / ".agents/skills/latex-review/scripts/check_project.py",
                                      root, structured=False))
        if not roots:
            results.append({"name": "LaTeX", "status": "not_applicable",
                            "message": "Nessun main.tex in radice, in latex/ o nelle sue sottocartelle"})
        if full or args.url:
            if args.url and not args.no_e2e:
                result = run_script("Browser (smoke test)", KIT_ROOT / ".agents/skills/webapp-testing/scripts/playwright_runner.py", args.url)
            else:
                web_present = any(result["name"].startswith("UX") and result["status"] != "not_applicable" for result in results)
                result = {"name": "Browser (smoke test)", "status": "skipped" if args.url or web_present else "not_applicable",
                          "message": "Disabilitato esplicitamente" if args.no_e2e else "URL non indicato"}
            results.append(result)
    report = summarize(results)
    print_report(report, args.json)
    return {"passed": 0, "failed": 1, "incomplete": 2}[report["status"]]
