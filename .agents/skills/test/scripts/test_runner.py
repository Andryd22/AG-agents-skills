#!/usr/bin/env python3
"""
Test Runner - esecuzione dei test e report di copertura
Esegue i test e genera il report di copertura in base al tipo di progetto.

Uso:
    python test_runner.py <cartella_progetto> [--coverage]

Supporta:
    - Node.js: npm test, jest, vitest
    - Python: pytest, unittest
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

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
                
        except:
            pass
    
    # Progetto Python
    if (project_path / "pyproject.toml").exists() or (project_path / "requirements.txt").exists():
        result["type"] = "python"
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
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0
    }
    
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 minuti al massimo per i test
        )
        
        result["output"] = proc.stdout[:3000] if proc.stdout else ""
        result["error"] = proc.stderr[:500] if proc.stderr else ""
        result["passed"] = proc.returncode == 0
        
        # Prova a leggere dall'output quanti test sono passati e falliti
        output = proc.stdout or ""
        
        # Formato di Jest/Vitest: "Tests: X passed, Y failed, Z total"
        if "passed" in output.lower() and "failed" in output.lower():
            import re
            match = re.search(r'(\d+)\s+passed', output, re.IGNORECASE)
            if match:
                result["tests_passed"] = int(match.group(1))
            match = re.search(r'(\d+)\s+failed', output, re.IGNORECASE)
            if match:
                result["tests_failed"] = int(match.group(1))
            result["tests_run"] = result["tests_passed"] + result["tests_failed"]
        
        # Formato di pytest: "X passed, Y failed"
        if "pytest" in str(cmd):
            import re
            match = re.search(r'(\d+)\s+passed', output)
            if match:
                result["tests_passed"] = int(match.group(1))
            match = re.search(r'(\d+)\s+failed', output)
            if match:
                result["tests_failed"] = int(match.group(1))
            result["tests_run"] = result["tests_passed"] + result["tests_failed"]
        
    except FileNotFoundError:
        result["error"] = f"Comando non trovato: {cmd[0]}"
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout dopo 300 s"
    except Exception as e:
        result["error"] = str(e)
    
    return result


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    with_coverage = "--coverage" in sys.argv
    
    print(f"\n{'='*60}")
    print("[TEST RUNNER] Esecuzione dei test")
    print(f"{'='*60}")
    print(f"Progetto: {project_path}")
    print(f"Copertura: {'attiva' if with_coverage else 'disattivata'}")
    print(f"Ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Riconosce il framework di test
    test_info = detect_test_framework(project_path)
    print(f"Tipo: {test_info['type']}")
    print(f"Framework: {test_info['framework']}")
    print("-"*60)
    
    if not test_info["cmd"]:
        print("Nessun framework di test trovato in questo progetto.")
        output = {
            "script": "test_runner",
            "project": str(project_path),
            "type": test_info["type"],
            "framework": None,
            "passed": True,
            "message": "Nessun test configurato"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    # Sceglie il comando
    cmd = test_info["coverage_cmd"] if with_coverage and test_info["coverage_cmd"] else test_info["cmd"]
    
    print(f"Eseguo: {' '.join(cmd)}")
    print("-"*60)
    
    # Esegue i test
    result = run_tests(cmd, project_path)
    
    # Stampa l'output (troncato)
    if result["output"]:
        lines = result["output"].split("\n")
        for line in lines[:30]:
            print(line)
        if len(lines) > 30:
            print(f"... (altre {len(lines) - 30} righe)")
    
    # Riepilogo
    print("\n" + "="*60)
    print("RIEPILOGO")
    print("="*60)
    
    if result["passed"]:
        print("[OK] Tutti i test sono passati")
    else:
        print("[KO] Alcuni test sono falliti")
        if result["error"]:
            print(f"Errore: {result['error'][:200]}")
    
    if result["tests_run"] > 0:
        print(f"Test: {result['tests_run']} in totale, {result['tests_passed']} passati, {result['tests_failed']} falliti")
    
    output = {
        "script": "test_runner",
        "project": str(project_path),
        "type": test_info["type"],
        "framework": test_info["framework"],
        "tests_run": result["tests_run"],
        "tests_passed": result["tests_passed"],
        "tests_failed": result["tests_failed"],
        "passed": result["passed"]
    }
    
    print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
