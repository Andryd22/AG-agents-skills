#!/usr/bin/env python3
"""
Checklist principale - Antigravity Kit
======================================

Esegue gli script di controllo in ordine di priorità.
Usala per controllare il lavoro passo passo durante lo sviluppo.

Uso:
    python .agents/scripts/checklist.py .                # controlli di base
    python .agents/scripts/checklist.py . --url <URL>    # anche i controlli E2E

Ordine di priorità:
    P1: validazione dello schema (se c'è un database)
    P2: test (unitari e di integrazione)
    P3: audit UX (leggi di psicologia, accessibilità)
    P4: E2E (Playwright, richiede l'URL)
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# Colori ANSI per il terminale
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

# Controlli in ordine di priorità
CORE_CHECKS = [
    ("Validazione dello schema", ".agents/skills/database-design/scripts/schema_validator.py", False),
    ("Test", ".agents/skills/test/scripts/test_runner.py", False),
    ("Audit UX", ".agents/skills/frontend-design/scripts/ux_audit.py", False),
]

# Controlli che richiedono l'app avviata: ricevono l'URL invece della cartella del progetto
PERFORMANCE_CHECKS = [
    ("E2E con Playwright", ".agents/skills/webapp-testing/scripts/playwright_runner.py", False),
]

def check_script_exists(script_path: Path) -> bool:
    """Controlla che il file dello script esista"""
    return script_path.exists() and script_path.is_file()

def run_script(name: str, script_path: Path, project_path: str, url: Optional[str] = None) -> dict:
    """
    Esegue uno script di controllo e ne raccoglie il risultato

    Restituisce:
        dict con le chiavi: name, passed, output, skipped
    """
    if not check_script_exists(script_path):
        print_warning(f"{name}: script non trovato, lo salto")
        return {"name": name, "passed": True, "output": "", "skipped": True}
    
    print_step(f"Eseguo: {name}")
    
    # Comando da eseguire
    # Lo stesso interprete di questo script (un semplice "python" può non esistere, es. su macOS)
    if url and "playwright" in script_path.name.lower():
        cmd = [sys.executable, str(script_path), url]  # playwright_runner.py legge l'URL da argv[1]
    else:
        cmd = [sys.executable, str(script_path), project_path]
    
    # Esegue lo script
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minuti al massimo
        )
        
        passed = result.returncode == 0
        
        if passed:
            print_success(f"{name}: SUPERATO")
        else:
            print_error(f"{name}: FALLITO")
            if result.stderr:
                print(f"  Errore: {result.stderr[:200]}")
        
        return {
            "name": name,
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr,
            "skipped": False
        }
    
    except subprocess.TimeoutExpired:
        print_error(f"{name}: TIMEOUT (>5 minuti)")
        return {"name": name, "passed": False, "output": "", "error": "Timeout", "skipped": False}
    
    except Exception as e:
        print_error(f"{name}: ERRORE - {str(e)}")
        return {"name": name, "passed": False, "output": "", "error": str(e), "skipped": False}

def print_summary(results: List[dict]):
    """Stampa il riepilogo finale"""
    print_header("📊 RIEPILOGO DELLA CHECKLIST")
    
    passed_count = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed_count = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped_count = sum(1 for r in results if r.get("skipped"))
    
    print(f"Controlli totali: {len(results)}")
    print(f"{Colors.GREEN}✅ Superati: {passed_count}{Colors.ENDC}")
    print(f"{Colors.RED}❌ Falliti: {failed_count}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏭️  Saltati: {skipped_count}{Colors.ENDC}")
    print()
    
    # Risultati nel dettaglio
    for r in results:
        if r.get("skipped"):
            status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}✅{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌{Colors.ENDC}"
        
        print(f"{status} {r['name']}")
    
    print()
    
    if failed_count > 0:
        print_error(f"{failed_count} controllo/i FALLITO/I - correggi prima di andare avanti")
        return False
    else:
        print_success("Tutti i controlli SUPERATI ✨")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Esegue la checklist di controllo dell'Antigravity Kit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python .agents/scripts/checklist.py .                                  # solo i controlli di base
  python .agents/scripts/checklist.py . --url http://localhost:3000      # anche gli E2E
        """
    )
    parser.add_argument("project", help="cartella del progetto da controllare")
    parser.add_argument("--url", help="URL dell'app avviata, per i controlli E2E (playwright)")
    parser.add_argument("--skip-performance", action="store_true", help="salta i controlli E2E anche se c'è l'URL")
    
    args = parser.parse_args()
    
    project_path = Path(args.project).resolve()
    
    if not project_path.exists():
        print_error(f"La cartella del progetto non esiste: {project_path}")
        sys.exit(1)
    
    print_header("🚀 ANTIGRAVITY KIT - MASTER CHECKLIST")
    print(f"Progetto: {project_path}")
    print(f"URL: {args.url if args.url else 'non indicato (controlli E2E saltati)'}")
    
    results = []
    
    # Controlli di base
    print_header("📋 CONTROLLI DI BASE")
    for name, script_path, required in CORE_CHECKS:
        script = project_path / script_path
        result = run_script(name, script, str(project_path))
        results.append(result)
        
        # Se fallisce un controllo obbligatorio, si ferma
        if required and not result["passed"] and not result.get("skipped"):
            print_error(f"CRITICO: {name} è fallito. Interrompo la checklist.")
            print_summary(results)
            sys.exit(1)
    
    # Controlli E2E, se c'è l'URL
    if args.url and not args.skip_performance:
        print_header("🌐 CONTROLLI E2E")
        for name, script_path, required in PERFORMANCE_CHECKS:
            script = project_path / script_path
            result = run_script(name, script, str(project_path), args.url)
            results.append(result)
    
    # Riepilogo
    all_passed = print_summary(results)
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
