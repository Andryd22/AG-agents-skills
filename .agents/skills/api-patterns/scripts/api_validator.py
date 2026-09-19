#!/usr/bin/env python3
"""
API Validator - controlla che gli endpoint delle API seguano le buone pratiche.
Valida le specifiche OpenAPI, il formato delle risposte e i problemi più comuni.

Uso:
    python api_validator.py <cartella_progetto>
"""
import sys
import json
import re
from pathlib import Path

# Codifica della console di Windows per l'output Unicode
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

def find_api_files(project_path: Path) -> list:
    """Trova i file che riguardano le API."""
    patterns = [
        "**/*api*.ts", "**/*api*.js", "**/*api*.py",
        "**/routes/*.ts", "**/routes/*.js", "**/routes/*.py",
        "**/controllers/*.ts", "**/controllers/*.js",
        "**/endpoints/*.ts", "**/endpoints/*.py",
        "**/*.openapi.json", "**/*.openapi.yaml",
        "**/swagger.json", "**/swagger.yaml",
        "**/openapi.json", "**/openapi.yaml"
    ]
    
    files = []
    for pattern in patterns:
        files.extend(project_path.glob(pattern))
    
    # Esclude node_modules e simili
    skip = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.agent', '.agents'}
    return [f for f in files if not skip.intersection(f.parts)]

def check_openapi_spec(file_path: Path) -> dict:
    """Controlla una specifica OpenAPI/Swagger."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        if file_path.suffix == '.json':
            spec = json.loads(content)
        else:
            # Controllo di base sullo YAML
            if 'openapi:' in content or 'swagger:' in content:
                passed.append("[OK] Versione OpenAPI/Swagger definita")
            else:
                issues.append("[X] Nessuna versione OpenAPI trovata")
            
            if 'paths:' in content:
                passed.append("[OK] La sezione paths esiste")
            else:
                issues.append("[X] Nessun path definito")
            
            if 'components:' in content or 'definitions:' in content:
                passed.append("[OK] Componenti dello schema definiti")
            
            return {'file': str(file_path), 'passed': passed, 'issues': issues, 'type': 'openapi'}
        
        # Controlli sull'OpenAPI in JSON
        if 'openapi' in spec or 'swagger' in spec:
            passed.append("[OK] Versione OpenAPI definita")
        
        if 'info' in spec:
            if 'title' in spec['info']:
                passed.append("[OK] Titolo dell'API definito")
            if 'version' in spec['info']:
                passed.append("[OK] Versione dell'API definita")
            if 'description' not in spec['info']:
                issues.append("[!] Manca la descrizione dell'API")
        
        if 'paths' in spec:
            path_count = len(spec['paths'])
            passed.append(f"[OK] {path_count} endpoint definiti")
            
            # Controlla ogni path
            for path, methods in spec['paths'].items():
                for method, details in methods.items():
                    if method in ['get', 'post', 'put', 'patch', 'delete']:
                        if 'responses' not in details:
                            issues.append(f"[X] {method.upper()} {path}: nessuna risposta definita")
                        if 'summary' not in details and 'description' not in details:
                            issues.append(f"[!] {method.upper()} {path}: nessuna descrizione")
        
    except Exception as e:
        issues.append(f"[X] Errore di lettura della specifica: {e}")
    
    return {'file': str(file_path), 'passed': passed, 'issues': issues, 'type': 'openapi'}

def check_api_code(file_path: Path) -> dict:
    """Cerca i problemi più comuni nel codice di un'API."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Gestione degli errori
        error_patterns = [
            r'try\s*{', r'try:', r'\.catch\(',
            r'except\s+', r'catch\s*\('
        ]
        has_error_handling = any(re.search(p, content) for p in error_patterns)
        if has_error_handling:
            passed.append("[OK] Gestione degli errori presente")
        else:
            issues.append("[X] Nessuna gestione degli errori trovata")
        
        # Codici di stato
        status_patterns = [
            r'status\s*\(\s*\d{3}\s*\)', r'statusCode\s*[=:]\s*\d{3}',
            r'HttpStatus\.', r'status_code\s*=\s*\d{3}',
            r'\.status\(\d{3}\)', r'res\.status\('
        ]
        has_status = any(re.search(p, content) for p in status_patterns)
        if has_status:
            passed.append("[OK] Codici di stato HTTP usati")
        else:
            issues.append("[!] Nessun codice di stato HTTP esplicito")
        
        # Validazione
        validation_patterns = [
            r'validate', r'schema', r'zod', r'joi', r'yup',
            r'pydantic', r'@Body\(', r'@Query\('
        ]
        has_validation = any(re.search(p, content, re.I) for p in validation_patterns)
        if has_validation:
            passed.append("[OK] Validazione degli input presente")
        else:
            issues.append("[!] Nessuna validazione degli input trovata")
        
        # Middleware di autenticazione
        auth_patterns = [
            r'auth', r'jwt', r'bearer', r'token',
            r'middleware', r'guard', r'@Authenticated'
        ]
        has_auth = any(re.search(p, content, re.I) for p in auth_patterns)
        if has_auth:
            passed.append("[OK] Autenticazione/autorizzazione trovata")
        
        # Rate limiting
        rate_patterns = [r'rateLimit', r'throttle', r'rate.?limit']
        has_rate = any(re.search(p, content, re.I) for p in rate_patterns)
        if has_rate:
            passed.append("[OK] Rate limiting presente")
        
        # Log
        log_patterns = [r'console\.log', r'logger\.', r'logging\.', r'log\.']
        has_logging = any(re.search(p, content) for p in log_patterns)
        if has_logging:
            passed.append("[OK] Log presenti")
        
    except Exception as e:
        issues.append(f"[X] Errore di lettura: {e}")
    
    return {'file': str(file_path), 'passed': passed, 'issues': issues, 'type': 'code'}

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    project_path = Path(target)
    
    print("\n" + "=" * 60)
    print("  API VALIDATOR - buone pratiche degli endpoint")
    print("=" * 60 + "\n")
    
    api_files = find_api_files(project_path)
    
    if not api_files:
        print("[!] Nessun file di API trovato.")
        print("   Cerco: routes/, controllers/, api/, openapi.json/yaml")
        sys.exit(0)
    
    results = []
    for file_path in api_files[:15]:  # al massimo 15 file
        if 'openapi' in file_path.name.lower() or 'swagger' in file_path.name.lower():
            result = check_openapi_spec(file_path)
        else:
            result = check_api_code(file_path)
        results.append(result)
    
    # Stampa i risultati
    total_issues = 0
    total_passed = 0
    
    for result in results:
        print(f"\n[FILE] {result['file']} [{result['type']}]")
        for item in result['passed']:
            print(f"   {item}")
            total_passed += 1
        for item in result['issues']:
            print(f"   {item}")
            if item.startswith("[X]"):
                total_issues += 1
    
    print("\n" + "=" * 60)
    print(f"[RISULTATI] {total_passed} superati, {total_issues} problemi critici")
    print("=" * 60)
    
    if total_issues == 0:
        print("[OK] Validazione delle API superata")
        sys.exit(0)
    else:
        print("[X] Correggi i problemi critici prima del deploy")
        sys.exit(1)

if __name__ == "__main__":
    main()
