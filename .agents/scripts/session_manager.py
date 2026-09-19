#!/usr/bin/env python3
"""
Session Manager - Antigravity Kit
=================================
Analizza lo stato del progetto, riconosce lo stack, conta i file e riassume la
sessione in corso.

Uso:
    python .agents/scripts/session_manager.py status [path]
    python .agents/scripts/session_manager.py info [path]
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

def get_project_root(path: str) -> Path:
    return Path(path).resolve()

def analyze_package_json(root: Path) -> Dict[str, Any]:
    pkg_file = root / "package.json"
    if not pkg_file.exists():
        return {"type": "unknown", "dependencies": {}}
    
    try:
        with open(pkg_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        deps = data.get("dependencies", {})
        dev_deps = data.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}
        
        stack = []
        if "next" in all_deps: stack.append("Next.js")
        elif "react" in all_deps: stack.append("React")
        elif "vue" in all_deps: stack.append("Vue")
        elif "svelte" in all_deps: stack.append("Svelte")
        elif "express" in all_deps: stack.append("Express")
        elif "nestjs" in all_deps or "@nestjs/core" in all_deps: stack.append("NestJS")
        
        if "tailwindcss" in all_deps: stack.append("Tailwind CSS")
        if "prisma" in all_deps: stack.append("Prisma")
        if "typescript" in all_deps: stack.append("TypeScript")
        
        return {
            "name": data.get("name", "unnamed"),
            "version": data.get("version", "0.0.0"),
            "stack": stack,
            "scripts": list(data.get("scripts", {}).keys())
        }
    except Exception as e:
        return {"error": str(e)}

def count_files(root: Path) -> Dict[str, int]:
    stats = {"created": 0, "modified": 0, "total": 0}
    # Per ora un conteggio semplice: un tracciamento completo richiederebbe git diff o una cronologia estesa
    exclude = {".git", "node_modules", ".next", "dist", "build", ".agent", ".agents", ".gemini", "__pycache__"}
    
    for root_dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in exclude]
        stats["total"] += len(files)
        
    return stats

def detect_features(root: Path) -> List[str]:
    # Euristica: guarda i nomi delle cartelle in src/
    features = []
    src = root / "src"
    if src.exists():
        possible_dirs = ["components", "modules", "features", "app", "pages", "services"]
        for d in possible_dirs:
            p = src / d
            if p.exists() and p.is_dir():
                # Le sottocartelle sono probabilmente funzionalità
                for child in p.iterdir():
                    if child.is_dir():
                        features.append(child.name)
    return features[:10] # al massimo 10

def print_status(root: Path):
    info = analyze_package_json(root)
    stats = count_files(root)
    features = detect_features(root)
    
    print("\n=== Stato del progetto ===")
    print(f"\n📁 Progetto: {info.get('name', root.name)}")
    print(f"📂 Percorso: {root}")
    print(f"🏷️  Tipo: {', '.join(info.get('stack') or ['generico'])}")
    print("📊 Stato: attivo")

    print("\n🔧 Stack:")
    for tech in info.get('stack', []):
        print(f"   • {tech}")
        
    print(f"\n✅ Moduli/funzionalità trovati ({len(features)}):")
    for feat in features:
        print(f"   • {feat}")
    if not features:
        print("   (nessun modulo di funzionalità riconosciuto)")
        
    print(f"\n📄 File: {stats['total']} in totale")
    print("\n====================\n")

def main():
    parser = argparse.ArgumentParser(description="Stato del progetto e della sessione")
    parser.add_argument("command", choices=["status", "info"], help="comando da eseguire")
    parser.add_argument("path", nargs="?", default=".", help="cartella del progetto")
    
    args = parser.parse_args()
    root = get_project_root(args.path)
    
    if args.command == "status":
        print_status(root)
    elif args.command == "info":
        print(json.dumps(analyze_package_json(root), indent=2))

if __name__ == "__main__":
    main()
