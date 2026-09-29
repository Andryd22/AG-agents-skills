#!/usr/bin/env python3
"""
Test Runner - esecuzione dei test e report di copertura
Esegue i test e genera il report di copertura in base al tipo di progetto.

Uso:
    python test_runner.py <cartella_progetto> [--coverage]

Supporta:
    - Node.js: npm test, jest, vitest
    - Python: pytest (unittest tramite lo script test del progetto)
"""

import subprocess
import sys
import json
import argparse
import shutil
import os
import re
from pathlib import Path

# Codifica della console di Windows
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


def detect_test_framework(project_path: Path) -> dict:
    """Riconosce il framework di test e i comandi."""
    result = {
        "type": "unknown",
        "framework": None,
        "cmd": None,
        "coverage_cmd": None
    }
    
    # Progetto Node.js
    package_json = project_path / "package.json"
    if package_json.exists():
        result["type"] = "node"
        try:
            pkg = json.loads(package_json.read_text(encoding='utf-8'))
            scripts = pkg.get("scripts", {})
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            # C'è uno script "test"?
            if "test" in scripts:
                result["framework"] = "npm test"
                result["cmd"] = ["npm", "test"]
                
                # Prova a riconoscere il framework per la copertura
                if "vitest" in deps:
                    result["framework"] = "vitest"
                    result["coverage_cmd"] = ["npx", "vitest", "run", "--coverage"]
                elif "jest" in deps:
                    result["framework"] = "jest"
                    result["coverage_cmd"] = ["npx", "jest", "--coverage"]
            elif "vitest" in deps:
                result["framework"] = "vitest"
                result["cmd"] = ["npx", "vitest", "run"]
                result["coverage_cmd"] = ["npx", "vitest", "run", "--coverage"]
            elif "jest" in deps:
                result["framework"] = "jest"
                result["cmd"] = ["npx", "jest"]
                result["coverage_cmd"] = ["npx", "jest", "--coverage"]
                
        except (OSError, ValueError) as error:
            raise ValueError(f"package.json non leggibile: {error}") from error

    if result["cmd"]:
        return result
    # Un requirements.txt con pandas/sklearn non configura automaticamente pytest.
    has_tests = False
    excluded = {'.git', '.agents', '.agent', '.agents.backups', '.venv', 'venv',
                'node_modules', '__pycache__', 'build', 'dist'}
    for _, directories, files in os.walk(project_path):
        directories[:] = [name for name in directories if name not in excluded]
        if any(name.endswith('.py') and (name.startswith('test_') or name.endswith('_test.py')) for name in files):
            has_tests = True
            break
    configured = (project_path / 'pytest.ini').is_file()
    pyproject = project_path / 'pyproject.toml'
    if pyproject.is_file():
        configured = configured or '[tool.pytest' in pyproject.read_text(encoding='utf-8')
    if has_tests or configured or pyproject.exists() or (project_path / 'requirements.txt').exists():
        result["type"] = "python"
    if has_tests or configured:
        result["framework"] = "pytest"
        result["cmd"] = [sys.executable, "-m", "pytest", "-v"]
        result["coverage_cmd"] = [sys.executable, "-m", "pytest", "--cov", "--cov-report=term-missing"]
    
    return result


def run_tests(cmd: list, cwd: Path) -> dict:
    """Esegue i test e restituisce i risultati."""
    result = {
        "passed": False,
        "output": "",
        "error": "",
        "tests_run": None,
        "tests_passed": None,
        "tests_failed": None
    }
    
    try:
        # CreateProcess su Windows non risolve npm/npx nei rispettivi file .cmd.
        executable = shutil.which(cmd[0])
        if not executable:
            raise FileNotFoundError(cmd[0])
        cmd = [executable, *cmd[1:]]
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 minuti al massimo per i test
        )
        
        result["output"] = proc.stdout or ""
        result["error"] = proc.stderr or ""
        result["returncode"] = proc.returncode
        result["passed"] = proc.returncode == 0
        
        # Il conteggio resta sconosciuto se il comando non espone una sintesi nota.
        output = (proc.stdout or '') + '\n' + (proc.stderr or '')
        passed_match = re.search(r'(\d+)\s+passed', output, re.IGNORECASE)
        failed_match = re.search(r'(\d+)\s+failed', output, re.IGNORECASE)
        if passed_match or failed_match:
            result['tests_passed'] = int(passed_match.group(1)) if passed_match else 0
            result['tests_failed'] = int(failed_match.group(1)) if failed_match else 0
            result['tests_run'] = result['tests_passed'] + result['tests_failed']
        
    except FileNotFoundError:
        result["error"] = f"Comando non trovato: {cmd[0]}"
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout dopo 300 s"
    except Exception as e:
        result["error"] = str(e)
    
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--json", action="store_true", help="solo risultato JSON")
    args = parser.parse_args()
    project_path = Path(args.project).resolve()
    if not project_path.is_dir():
        print(json.dumps({"status": "failed", "passed": False, "message": "Cartella del progetto inesistente"}))
        return 1
    try:
        test_info = detect_test_framework(project_path)
    except ValueError as error:
        print(json.dumps({"status": "failed", "passed": False, "message": str(error)}))
        return 1
    output = {"script": "test_runner", "project": str(project_path),
              "type": test_info["type"], "framework": test_info["framework"]}
    if not test_info["cmd"]:
        output.update(status="skipped", passed=None, message="Nessun test configurato")
    else:
        cmd = test_info["coverage_cmd"] if args.coverage and test_info["coverage_cmd"] else test_info["cmd"]
        result = run_tests(cmd, project_path)
        output.update(result)
        output["status"] = "passed" if result["passed"] else "failed"
        if test_info["framework"] == "pytest" and result.get("returncode") == 5:
            output.update(status="skipped", passed=None, message="pytest non ha raccolto test")
        if not args.json:
            print(f"Eseguo: {' '.join(cmd)}")
            print(result["output"])
            if result["error"]:
                print(result["error"])
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 1 if output["status"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
