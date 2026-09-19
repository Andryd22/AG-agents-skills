#!/usr/bin/env python3
"""
Suite di verifica completa - Antigravity Kit
============================================

Esegue tutti i controlli del kit, E2E compresi.
Usala prima di un deploy o di un rilascio importante.

Uso:
    python .agents/scripts/verify_all.py . --url <URL>

Comprende:
    ✅ Validazione dello schema (Prisma)
    ✅ Suite di test (unitari + integrazione)
    ✅ Validazione delle API (OpenAPI / file delle rotte)
    ✅ Audit UX + controllo dell'accessibilità
    ✅ E2E con Playwright (serve --url)
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Colori ANSI
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
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

# Suite di verifica completa
VERIFICATION_SUITE = [
    # P1: dati
    {
        "category": "Dati",
        "checks": [
            ("Validazione dello schema", ".agents/skills/database-design/scripts/schema_validator.py", False),
        ]
    },

    # P2: test
    {
        "category": "Test",
        "checks": [
            ("Suite di test", ".agents/skills/test/scripts/test_runner.py", True),
        ]
    },

    # P3: API
    {
        "category": "API",
        "checks": [
            ("Validazione delle API", ".agents/skills/api-patterns/scripts/api_validator.py", False),
        ]
    },

    # P4: UX e accessibilità
    {
        "category": "UX e accessibilità",
        "checks": [
            ("Audit UX", ".agents/skills/frontend-design/scripts/ux_audit.py", False),
            ("Controllo dell'accessibilità", ".agents/skills/frontend-design/scripts/accessibility_checker.py", False),
        ]
    },

    # P5: test E2E (serve l'URL)
    {
        "category": "Test E2E",
        "requires_url": True,
        "checks": [
            ("E2E con Playwright", ".agents/skills/webapp-testing/scripts/playwright_runner.py", False),
        ]
    },
]

def run_script(name: str, script_path: Path, project_path: str, url: Optional[str] = None) -> dict:
    """Esegue uno script di controllo"""
    if not script_path.exists():
        print_warning(f"{name}: script non trovato, lo salto")
        return {"name": name, "passed": True, "skipped": True, "duration": 0}
    
    print_step(f"Eseguo: {name}")
    start_time = datetime.now()
    
    # Comando da eseguire
    # Lo stesso interprete di questo script (un semplice "python" può non esistere, es. su macOS)
    if url and "playwright" in script_path.name.lower():
        cmd = [sys.executable, str(script_path), url]  # playwright_runner.py legge l'URL da argv[1]
    else:
        cmd = [sys.executable, str(script_path), project_path]
    
    # Esecuzione
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minuti al massimo, per i controlli lenti
        )
        
        duration = (datetime.now() - start_time).total_seconds()
        passed = result.returncode == 0
        
        if passed:
            print_success(f"{name}: SUPERATO ({duration:.1f} s)")
        else:
            print_error(f"{name}: FALLITO ({duration:.1f} s)")
            if result.stderr:
                print(f"  {result.stderr[:300]}")
        
        return {
            "name": name,
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr,
            "skipped": False,
            "duration": duration
        }
    
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        print_error(f"{name}: TIMEOUT (>{duration:.0f} s)")
        return {"name": name, "passed": False, "skipped": False, "duration": duration, "error": "Timeout"}
    
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        print_error(f"{name}: ERRORE - {str(e)}")
        return {"name": name, "passed": False, "skipped": False, "duration": duration, "error": str(e)}

def print_final_report(results: List[dict], start_time: datetime):
    """Stampa il report finale completo"""
    total_duration = (datetime.now() - start_time).total_seconds()
    
    print_header("📊 REPORT DELLA VERIFICA COMPLETA")
    
    # Statistiche
    total = len(results)
    passed = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped = sum(1 for r in results if r.get("skipped"))
    
    print(f"Durata totale: {total_duration:.1f} s")
    print(f"Controlli totali: {total}")
    print(f"{Colors.GREEN}✅ Superati: {passed}{Colors.ENDC}")
    print(f"{Colors.RED}❌ Falliti: {failed}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏭️  Saltati: {skipped}{Colors.ENDC}")
    print()
    
    # Risultati per categoria
    print(f"{Colors.BOLD}Risultati per categoria:{Colors.ENDC}")
    current_category = None
    for r in results:
        # Intestazione della categoria, se è cambiata
        if r.get("category") and r["category"] != current_category:
            current_category = r["category"]
            print(f"\n{Colors.BOLD}{Colors.CYAN}{current_category}:{Colors.ENDC}")
        
        # Risultato
        if r.get("skipped"):
            status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}✅{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌{Colors.ENDC}"
        
        duration_str = f"({r.get('duration', 0):.1f} s)" if not r.get("skipped") else ""
        print(f"  {status} {r['name']} {duration_str}")
    
    print()
    
    # Dettaglio dei controlli falliti
    if failed > 0:
        print(f"{Colors.BOLD}{Colors.RED}❌ CONTROLLI FALLITI:{Colors.ENDC}")
        for r in results:
            if not r["passed"] and not r.get("skipped"):
                print(f"\n{Colors.RED}✗ {r['name']}{Colors.ENDC}")
                if r.get("error"):
                    error_preview = r["error"][:200]
                    print(f"  Errore: {error_preview}")
        print()
    
    # Verdetto finale
    if failed > 0:
        print_error(f"VERIFICA FALLITA - {failed} controllo/i da sistemare")
        print(f"\n{Colors.YELLOW}💡 Consiglio: correggi prima i problemi critici (test, schema){Colors.ENDC}")
        return False
    else:
        print_success("✨ TUTTI I CONTROLLI SUPERATI - pronto per il deploy! ✨")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Esegue la suite di verifica completa dell'Antigravity Kit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python .agents/scripts/verify_all.py . --url http://localhost:3000
  python .agents/scripts/verify_all.py . --url https://staging.example.com --no-e2e
        """
    )
    parser.add_argument("project", help="cartella del progetto da controllare")
    parser.add_argument("--url", required=True, help="URL dell'app avviata, per i controlli E2E")
    parser.add_argument("--no-e2e", action="store_true", help="salta i test E2E")
    parser.add_argument("--stop-on-fail", action="store_true", help="si ferma al primo errore")
    
    args = parser.parse_args()
    
    project_path = Path(args.project).resolve()
    
    if not project_path.exists():
        print_error(f"La cartella del progetto non esiste: {project_path}")
        sys.exit(1)
    
    print_header("🚀 ANTIGRAVITY KIT - SUITE DI VERIFICA COMPLETA")
    print(f"Progetto: {project_path}")
    print(f"URL: {args.url}")
    print(f"Inizio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    results = []
    
    # Tutte le categorie di verifica
    for suite in VERIFICATION_SUITE:
        category = suite["category"]
        requires_url = suite.get("requires_url", False)
        
        # Salta se serve l'URL e non c'è
        if requires_url and not args.url:
            continue
        
        # Salta gli E2E se richiesto
        if args.no_e2e and category == "Test E2E":
            continue
        
        print_header(f"📋 {category.upper()}")
        
        for name, script_path, required in suite["checks"]:
            script = project_path / script_path
            result = run_script(name, script, str(project_path), args.url)
            result["category"] = category
            results.append(result)
            
            # Con --stop-on-fail si ferma al primo controllo obbligatorio fallito
            if args.stop_on_fail and required and not result["passed"] and not result.get("skipped"):
                print_error(f"CRITICO: {name} è fallito. Interrompo la verifica.")
                print_final_report(results, start_time)
                sys.exit(1)
    
    # Report finale
    all_passed = print_final_report(results, start_time)
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
