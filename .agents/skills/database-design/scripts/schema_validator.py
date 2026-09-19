#!/usr/bin/env python3
"""
Schema Validator - controllo degli schema del database
Controlla gli schema Prisma e cerca i problemi più comuni (gli schema Drizzle
li trova ma per ora non li analizza).

Uso:
    python schema_validator.py <cartella_progetto>

Controlla:
    - nomi dei model e degli enum (PascalCase)
    - campo @id
    - campo createdAt
    - indici sulle foreign key
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


def find_schema_files(project_path: Path) -> list:
    """Trova i file di schema del database."""
    schemas = []
    
    # Schema Prisma
    prisma_files = list(project_path.glob('**/prisma/schema.prisma'))
    schemas.extend([('prisma', f) for f in prisma_files])
    
    # File di schema Drizzle
    drizzle_files = list(project_path.glob('**/drizzle/*.ts'))
    drizzle_files.extend(project_path.glob('**/schema/*.ts'))
    for f in drizzle_files:
        if 'schema' in f.name.lower() or 'table' in f.name.lower():
            schemas.append(('drizzle', f))
    
    skip = {'node_modules', '.git', 'dist', 'build', '.next', '.agent', '.agents'}
    schemas = [(kind, f) for kind, f in schemas if not skip.intersection(f.parts)]
    return schemas[:10]  # al massimo 10 file


def validate_prisma_schema(file_path: Path) -> list:
    """Controlla un file di schema Prisma."""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Trova tutti i model
        models = re.findall(r'model\s+(\w+)\s*{([^}]+)}', content, re.DOTALL)
        
        for model_name, model_body in models:
            # Convenzione dei nomi (PascalCase)
            if not model_name[0].isupper():
                issues.append(f"Il model '{model_name}' dovrebbe essere in PascalCase")
            
            # Campo id
            if '@id' not in model_body and 'id' not in model_body.lower():
                issues.append(f"Al model '{model_name}' forse manca il campo @id")
            
            # createdAt/updatedAt
            if 'createdAt' not in model_body and 'created_at' not in model_body:
                issues.append(f"Al model '{model_name}' manca il campo createdAt (consigliato)")
            
            # @relation senza fields
            relations = re.findall(r'@relation\([^)]*\)', model_body)
            for rel in relations:
                if 'fields:' not in rel and 'references:' not in rel:
                    pass  # relazione implicita, va bene
            
            # Suggerimenti di @@index
            foreign_keys = re.findall(r'(\w+Id)\s+\w+', model_body)
            for fk in foreign_keys:
                if f'@@index([{fk}])' not in content and f'@@index(["{fk}"])' not in content:
                    issues.append(f"Valuta di aggiungere @@index([{fk}]) in {model_name} per query più veloci")
        
        # Definizioni degli enum
        enums = re.findall(r'enum\s+(\w+)\s*{', content)
        for enum_name in enums:
            if not enum_name[0].isupper():
                issues.append(f"L'enum '{enum_name}' dovrebbe essere in PascalCase")
        
    except Exception as e:
        issues.append(f"Errore nella lettura dello schema: {str(e)[:50]}")
    
    return issues


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print("[SCHEMA VALIDATOR] Controllo degli schema del database")
    print(f"{'='*60}")
    print(f"Progetto: {project_path}")
    print(f"Ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # Trova i file di schema
    schemas = find_schema_files(project_path)
    print(f"Trovati {len(schemas)} file di schema")
    
    if not schemas:
        output = {
            "script": "schema_validator",
            "project": str(project_path),
            "schemas_checked": 0,
            "issues_found": 0,
            "passed": True,
            "message": "Nessun file di schema trovato"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    # Controlla ogni schema
    all_issues = []
    
    for schema_type, file_path in schemas:
        print(f"\nControllo: {file_path.name} ({schema_type})")
        
        if schema_type == 'prisma':
            issues = validate_prisma_schema(file_path)
        else:
            issues = []  # il controllo degli schema Drizzle non c'è ancora
        
        if issues:
            all_issues.append({
                "file": str(file_path.name),
                "type": schema_type,
                "issues": issues
            })
    
    # Riepilogo
    print("\n" + "="*60)
    print("PROBLEMI DEGLI SCHEMA")
    print("="*60)
    
    if all_issues:
        for item in all_issues:
            print(f"\n{item['file']} ({item['type']}):")
            for issue in item["issues"][:5]:  # al massimo 5 per file
                print(f"  - {issue}")
            if len(item["issues"]) > 5:
                print(f"  ... e altri {len(item['issues']) - 5} problemi")
    else:
        print("Nessun problema negli schema.")
    
    total_issues = sum(len(item["issues"]) for item in all_issues)
    # I problemi degli schema sono avvisi, non errori
    passed = True
    
    output = {
        "script": "schema_validator",
        "project": str(project_path),
        "schemas_checked": len(schemas),
        "issues_found": total_issues,
        "passed": passed,
        "issues": all_issues
    }
    
    print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0)


if __name__ == "__main__":
    main()
