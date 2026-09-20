#!/usr/bin/env python3
"""
React Performance Checker
Audit automatico delle prestazioni per progetti React/Next.js,
basato sulle best practice di Vercel Engineering.

Uso:
    python react_performance_checker.py <cartella_progetto>
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

# Codifica della console di Windows
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

class PerformanceChecker:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.issues = []
        self.warnings = []
        self.passed = []

    SKIP_DIRS = {'node_modules', '.git', '.next', 'dist', 'build', '.agent', '.agents'}

    def _files(self, exts):
        """File sorgente con le estensioni indicate (pathlib non supporta l'espansione {a,b})."""
        for filepath in self.project_path.rglob('*'):
            if filepath.suffix in exts and filepath.is_file() and not self.SKIP_DIRS.intersection(filepath.parts):
                yield filepath

    def check_waterfalls(self):
        """Cerca gli await in sequenza (sezione 1)"""
        print("\n[*] Cerco i waterfall (await in sequenza)...")

        for filepath in self._files(('.ts', '.tsx', '.js', '.jsx')):
            if 'node_modules' in str(filepath):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')

                # Pattern: più await in sequenza senza Promise.all
                sequential_awaits = re.findall(r'await\s+\w+.*?\n\s*await\s+\w+', content)

                if sequential_awaits:
                    self.issues.append({
                        'file': str(filepath.relative_to(self.project_path)),
                        'type': 'CRITICAL',
                        'issue': 'Await in sequenza (waterfall)',
                        'fix': 'Usa Promise.all() per eseguire i fetch in parallelo',
                        'section': '1-async-eliminating-waterfalls.md'
                    })
            except Exception as e:
                continue

    def check_barrel_imports(self):
        """Cerca i barrel import (sezione 2)"""
        print("[*] Cerco i barrel import...")

        for filepath in self._files(('.ts', '.tsx', '.js', '.jsx')):
            if 'node_modules' in str(filepath):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')

                # Pattern: import da file index o da barrel export
                barrel_imports = re.findall(r"import.*from\s+['\"](@/.*?)/index['\"]", content)
                barrel_imports += re.findall(r"import.*from\s+['\"]\.\.?/.*?['\"](?!.*?\.tsx?)", content)

                if barrel_imports:
                    self.warnings.append({
                        'file': str(filepath.relative_to(self.project_path)),
                        'type': 'CRITICAL',
                        'issue': 'Possibili barrel import',
                        'fix': 'Importa direttamente dai singoli file',
                        'section': '2-bundle-bundle-size-optimization.md'
                    })
            except Exception as e:
                continue

    def check_dynamic_imports(self):
        """Controlla che i componenti grandi usino import dinamici (sezione 2)"""
        print("[*] Cerco gli import dinamici mancanti...")

        for filepath in self._files(('.ts', '.tsx')):
            if 'node_modules' in str(filepath):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')

                # Dimensione del file: oltre i 10KB probabilmente conviene un import dinamico
                if len(content) > 10000:
                    # È importato staticamente da qualche parte?
                    filename = filepath.stem

                    # Cerca gli import statici di questo componente
                    for check_file in self._files(('.ts', '.tsx')):
                        if check_file == filepath or 'node_modules' in str(check_file):
                            continue

                        check_content = check_file.read_text(encoding='utf-8')
                        if f"import {filename}" in check_content or f"import {{ {filename}" in check_content:
                            if 'dynamic(' not in check_content:
                                self.warnings.append({
                                    'file': str(check_file.relative_to(self.project_path)),
                                    'type': 'CRITICAL',
                                    'issue': f'Componente grande {filename} importato staticamente',
                                    'fix': 'Usa dynamic() per il code splitting',
                                    'section': '2-bundle-bundle-size-optimization.md'
                                })
                                break
            except Exception as e:
                continue

    def check_useEffect_fetching(self):
        """Cerca il data fetching dentro useEffect (sezione 4)"""
        print("[*] Cerco il data fetching in useEffect...")

        for filepath in self._files(('.ts', '.tsx')):
            if 'node_modules' in str(filepath):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')

                # Pattern: fetch dentro useEffect
                if 'useEffect' in content:
                    if re.search(r'useEffect.*?fetch\(', content, re.DOTALL):
                        self.warnings.append({
                            'file': str(filepath.relative_to(self.project_path)),
                            'type': 'MEDIUM-HIGH',
                            'issue': 'Data fetching dentro useEffect',
                            'fix': 'Valuta SWR o React Query per deduplicare le richieste',
                            'section': '4-client-client-side-data-fetching.md'
                        })
            except Exception as e:
                continue

    def check_missing_memoization(self):
        """Cerca React.memo, useMemo e useCallback mancanti (sezione 5)"""
        print("[*] Cerco la memoizzazione mancante...")

        for filepath in self._files(('.tsx',)):
            if 'node_modules' in str(filepath):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')

                # Definizioni di componenti senza memo
                components = re.findall(r'(?:export\s+)?(?:const|function)\s+([A-Z]\w+)', content)

                if components and 'React.memo' not in content and 'memo(' not in content:
                    # Il componente riceve props?
                    if 'props:' in content or 'Props>' in content:
                        self.warnings.append({
                            'file': str(filepath.relative_to(self.project_path)),
                            'type': 'MEDIUM',
                            'issue': 'Componente con props non memoizzato',
                            'fix': 'Valuta React.memo se le props sono stabili',
                            'section': '5-rerender-re-render-optimization.md'
                        })
            except Exception as e:
                continue

    def check_image_optimization(self):
        """Cerca le immagini non ottimizzate (sezione 6)"""
        print("[*] Controllo l'ottimizzazione delle immagini...")

        for filepath in self._files(('.ts', '.tsx', '.js', '.jsx')):
            if 'node_modules' in str(filepath):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')

                # Tag <img> al posto di next/image
                if '<img' in content and 'next/image' not in content:
                    self.warnings.append({
                        'file': str(filepath.relative_to(self.project_path)),
                        'type': 'MEDIUM',
                        'issue': 'Uso di <img> al posto di next/image',
                        'fix': "Usa next/image per l'ottimizzazione automatica",
                        'section': '6-rendering-rendering-performance.md'
                    })
            except Exception as e:
                continue

    def generate_report(self):
        """Genera il report finale"""
        print("\n" + "="*60)
        print("REPORT SULLE PRESTAZIONI REACT")
        print("="*60)

        print(f"\n[PROBLEMI CRITICI] ({len([i for i in self.issues if i['type'] == 'CRITICAL'])})")
        for issue in self.issues:
            if issue['type'] == 'CRITICAL':
                print(f"  - {issue['file']}")
                print(f"    Problema: {issue['issue']}")
                print(f"    Correzione: {issue['fix']}")
                print(f"    Riferimento: {issue['section']}\n")

        print(f"\n[AVVISI] ({len(self.warnings)})")
        for warning in self.warnings[:10]:  # Mostra i primi 10
            print(f"  - {warning['file']}")
            print(f"    Problema: {warning['issue']}")
            print(f"    Correzione: {warning['fix']}")
            print(f"    Riferimento: {warning['section']}\n")

        if len(self.warnings) > 10:
            print(f"  ... e altri {len(self.warnings) - 10} avvisi")

        print("\n" + "="*60)
        print(f"RIEPILOGO:")
        print(f"  Problemi critici: {len([i for i in self.issues if i['type'] == 'CRITICAL'])}")
        print(f"  Avvisi: {len(self.warnings)}")
        print("="*60)

        if len(self.issues) == 0 and len(self.warnings) == 0:
            print("\n[OK] Nessun problema di prestazioni rilevante!")
        else:
            print("\n[AZIONE RICHIESTA] Controlla e correggi i problemi qui sopra")
            print("Priorità: CRITICAL > HIGH > MEDIUM > LOW")

    def run(self):
        """Esegue tutti i controlli"""
        print("="*60)
        print("React Performance Checker (Vercel Engineering)")
        print("="*60)
        print(f"Cartella analizzata: {self.project_path}")

        self.check_waterfalls()
        self.check_barrel_imports()
        self.check_dynamic_imports()
        self.check_useEffect_fetching()
        self.check_missing_memoization()
        self.check_image_optimization()

        self.generate_report()


def main():
    if len(sys.argv) < 2:
        print("Uso: python react_performance_checker.py <cartella_progetto>")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"[ERRORE] Percorso non trovato: {project_path}")
        sys.exit(1)

    checker = PerformanceChecker(project_path)
    checker.run()


if __name__ == '__main__':
    main()
