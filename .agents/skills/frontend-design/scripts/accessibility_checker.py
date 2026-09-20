#!/usr/bin/env python3
"""
Accessibility Checker - audit di conformità WCAG
Cerca problemi di accessibilità nei file HTML/JSX/TSX.

Uso:
    python accessibility_checker.py <cartella_progetto>

Controlla:
    - Label dei form e testo accessibile dei pulsanti (aria-label)
    - Attributi ARIA e role="button"
    - Attributo lang e skip link
    - Navigazione da tastiera (onKeyDown, tabIndex)
    - Media in autoplay
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Codifica della console di Windows
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


def find_html_files(project_path: Path) -> list:
    """Trova i file HTML/JSX/TSX (al massimo 50)."""
    patterns = ['**/*.html', '**/*.jsx', '**/*.tsx']
    skip_dirs = {'node_modules', '.next', 'dist', 'build', '.git', '.agent', '.agents'}
    
    files = []
    for pattern in patterns:
        for f in project_path.glob(pattern):
            if not any(skip in f.parts for skip in skip_dirs):
                files.append(f)
    
    return files[:50]


def check_accessibility(file_path: Path) -> list:
    """Cerca problemi di accessibilità in un singolo file."""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Input dei form senza label
        inputs = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
        for inp in inputs:
            if 'type="hidden"' not in inp.lower():
                if 'aria-label' not in inp.lower() and 'id=' not in inp.lower():
                    issues.append("Input senza label né aria-label")
                    break
        
        # Pulsanti senza testo accessibile
        buttons = re.findall(r'<button[^>]*>[^<]*</button>', content, re.IGNORECASE)
        for btn in buttons:
            # Il pulsante ha un testo o un aria-label?
            if 'aria-label' not in btn.lower():
                text = re.sub(r'<[^>]+>', '', btn)
                if not text.strip():
                    issues.append("Pulsante senza testo accessibile")
                    break
        
        # Attributo lang mancante
        if '<html' in content.lower() and 'lang=' not in content.lower():
            issues.append("Manca l'attributo lang su <html>")
        
        # Skip link mancante
        if '<main' in content.lower() or '<body' in content.lower():
            if 'skip' not in content.lower() and '#main' not in content.lower():
                issues.append("Valuta un link per saltare al contenuto principale (skip link)")
        
        # Gestori di click senza supporto da tastiera
        onclick_count = content.lower().count('onclick=')
        onkeydown_count = content.lower().count('onkeydown=') + content.lower().count('onkeyup=')
        if onclick_count > 0 and onkeydown_count == 0:
            issues.append("onClick senza gestore da tastiera (onKeyDown)")
        
        # tabIndex positivi (alterano l'ordine naturale del focus), anche nella forma JSX tabIndex={1}
        if 'tabindex=' in content.lower():
            positive_tabindex = re.findall(r'tabindex=["\'{]?([1-9]\d*)', content, re.IGNORECASE)
            if positive_tabindex:
                issues.append("Evita i valori positivi di tabIndex")
        
        # Media in autoplay
        if 'autoplay' in content.lower():
            if 'muted' not in content.lower():
                issues.append("I media in autoplay devono partire senza audio (muted)")
        
        # Uso di role
        if 'role="button"' in content.lower():
            # I div con role="button" devono avere un tabindex
            div_buttons = re.findall(r'<div[^>]*role="button"[^>]*>', content, re.IGNORECASE)
            for div in div_buttons:
                if 'tabindex' not in div.lower():
                    issues.append("role='button' senza tabindex")
                    break
        
    except Exception as e:
        issues.append(f"Errore nella lettura del file: {str(e)[:50]}")
    
    return issues


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[CONTROLLO ACCESSIBILITÀ] Audit di conformità WCAG")
    print(f"{'='*60}")
    print(f"Progetto: {project_path}")
    print(f"Data e ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # Cerca i file HTML
    files = find_html_files(project_path)
    print(f"Trovati {len(files)} file HTML/JSX/TSX")
    
    if not files:
        output = {
            "script": "accessibility_checker",
            "project": str(project_path),
            "files_checked": 0,
            "issues_found": 0,
            "passed": True,
            "message": "Nessun file HTML/JSX/TSX trovato"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    # Controlla ogni file
    all_issues = []
    
    for f in files:
        issues = check_accessibility(f)
        if issues:
            all_issues.append({
                "file": str(f.name),
                "issues": issues
            })
    
    # Riepilogo
    print("\n" + "="*60)
    print("PROBLEMI DI ACCESSIBILITÀ")
    print("="*60)
    
    if all_issues:
        for item in all_issues[:10]:
            print(f"\n{item['file']}:")
            for issue in item["issues"]:
                print(f"  - {issue}")
        
        if len(all_issues) > 10:
            print(f"\n... e altri {len(all_issues) - 10} file con problemi")
    else:
        print("Nessun problema di accessibilità trovato!")
    
    total_issues = sum(len(item["issues"]) for item in all_issues)
    # I problemi di accessibilità sono importanti ma non bloccanti
    passed = total_issues < 5  # Tollera fino a 4 problemi
    
    output = {
        "script": "accessibility_checker",
        "project": str(project_path),
        "files_checked": len(files),
        "files_with_issues": len(all_issues),
        "issues_found": total_issues,
        "passed": passed
    }
    
    print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
