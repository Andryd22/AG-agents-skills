#!/usr/bin/env python3
"""
React Performance Checker
Audit automatico delle prestazioni per progetti React/Next.js, basato sulle regole
di Vercel Engineering raccolte nella skill nextjs-react-expert.

Uso:
    python react_performance_checker.py <cartella_progetto>

Controlli:
    - await consecutivi e indipendenti, cioè waterfall (sezione 1)      -> critico
    - import da barrel file locali e da librerie non ottimizzate (sez. 2) -> avviso
    - componenti grandi importati staticamente (sezione 2)              -> avviso
    - fetch dentro useEffect (sezione 4)                                -> avviso
    - memoizzazione, solo se il React Compiler non è attivo (sezione 5) -> avviso
    - <img> invece di next/image, solo nei progetti Next.js (sezione 6) -> avviso

Codice di uscita 1 se trova almeno un problema critico; gli avvisi non lo cambiano.
"""

import json
import re
import sys
from pathlib import Path

# Codifica della console di Windows
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

SOURCE_EXTS = ('.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs')
SKIP_DIRS = {'node_modules', '.git', '.next', 'dist', 'build', 'out', 'coverage', '.agent', '.agents'}
TEST_FILE = re.compile(r'\.(?:test|spec)\.[jt]sx?$')

# Librerie che Next.js ottimizza da solo (optimizePackageImports predefinito, documentazione di Next.js 16)
NEXT_AUTO_OPTIMIZED = {
    'lucide-react', 'date-fns', 'lodash-es', 'ramda', 'antd', 'react-bootstrap', 'ahooks',
    '@ant-design/icons', '@headlessui/react', '@headlessui-float/react', '@heroicons/react',
    '@visx/visx', '@tremor/react', 'rxjs', '@mui/material', '@mui/icons-material', 'recharts',
    'react-use', '@material-ui/core', '@material-ui/icons', '@tabler/icons-react', 'mui-core', 'effect',
}
NEXT_AUTO_PREFIXES = ('react-icons/', '@effect/')

# Altre librerie con barrel file molto grandi, da aggiungere a optimizePackageImports in Next.js
OTHER_HEAVY = {
    '@phosphor-icons/react', '@chakra-ui/react', '@mantine/core', '@fortawesome/free-solid-svg-icons',
    '@fortawesome/free-regular-svg-icons', '@fortawesome/free-brands-svg-icons',
}

INDEX_FILES = ('index.ts', 'index.tsx', 'index.js', 'index.jsx', 'index.mjs')
RE_EXPORT = re.compile(r'^\s*export\s+(?:type\s+)?(?:\*|\{[^}]*\})\s*(?:as\s+[\w$]+\s*)?from\s', re.M)
IMPORT = re.compile(r'^\s*import\s+(?!type\b)((?:(?!\bimport\b)[^;\'"])*?)\s*from\s*[\'"]([^\'"]+)[\'"]', re.M)
AWAIT_STMT = re.compile(r'^(\s*)(?:(?:const|let|var)\s+(?P<lhs>.+?)\s*=\s*)?await\s+(?P<expr>\S.*)$')
IDENT = re.compile(r'[A-Za-z_$][\w$]*')
BLOCK_COMMENT = re.compile(r'/\*[\s\S]*?\*/')
LINE_COMMENT = re.compile(r'(?<![:\'"`\\])//[^\n]*')

SECTION = {
    'async': '1-async-eliminating-waterfalls.md',
    'bundle': '2-bundle-bundle-size-optimization.md',
    'client': '4-client-client-side-data-fetching.md',
    'rerender': '5-rerender-re-render-optimization.md',
    'rendering': '6-rendering-rendering-performance.md',
}


# ------------------------------------------------------------------ supporto
def strip_comments(text):
    """Toglie i commenti tenendo i numeri di riga."""
    text = BLOCK_COMMENT.sub(lambda m: '\n' * m.group(0).count('\n'), text)
    return LINE_COMMENT.sub('', text)


def strip_jsonc(raw):
    """Toglie commenti e virgole finali da un JSON con commenti (tsconfig.json), senza toccare le stringhe."""
    out, i, n, in_str = [], 0, len(raw), False
    while i < n:
        c = raw[i]
        if in_str:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(raw[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif raw.startswith('//', i):
            j = raw.find('\n', i)
            i = n if j < 0 else j
        elif raw.startswith('/*', i):
            j = raw.find('*/', i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return re.sub(r',\s*([}\]])', r'\1', ''.join(out))


def statement_end(lines, start, limit=30):
    """Ultima riga dell'istruzione che comincia a `start` (parentesi bilanciate, al massimo `limit` righe)."""
    depth = 0
    for i in range(start, min(len(lines), start + limit)):
        for ch in lines[i]:
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth -= 1
        if depth <= 0:
            return i
    return start


def bound_names(lhs):
    """Variabili dichiarate a sinistra di `=`: un nome o una destrutturazione."""
    lhs = lhs.strip()
    if lhs[:1] in ('{', '['):
        end = lhs.rfind('}' if lhs[0] == '{' else ']')
        body = lhs[1:end] if end > 0 else lhs[1:]
        body = re.sub(r'=\s*[^,}\]]+', '', body)                  # valori predefiniti
        body = re.sub(r'[\w$]+\s*:\s*(?=[\w${\[])', '', body)      # chiave: alias -> alias
        return set(IDENT.findall(body.replace('...', '')))
    m = IDENT.match(lhs)
    return {m.group(0)} if m else set()


def uses(name, text):
    """True se `text` usa la variabile `name` (non una proprietà con lo stesso nome)."""
    return re.search(r'(?<![\w$.])' + re.escape(name) + r'(?![\w$])', text) is not None


def awaits_existing_promise(expr):
    """`await p` o `await this.p`: la promessa è già partita prima, non è un waterfall."""
    return re.fullmatch(r'[\w$.]+\s*;?', expr.strip()) is not None


def package_name(spec):
    parts = spec.split('/')
    return '/'.join(parts[:2]) if spec.startswith('@') else parts[0]


def call_arguments(text, name):
    """(posizione, argomenti) di ogni chiamata name(...), con le parentesi bilanciate."""
    for m in re.finditer(r'\b' + re.escape(name) + r'\s*\(', text):
        start = m.end() - 1
        depth = 0
        for j in range(start, min(len(text), start + 20000)):
            if text[j] == '(':
                depth += 1
            elif text[j] == ')':
                depth -= 1
                if depth == 0:
                    yield m.start(), text[start + 1:j]
                    break


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


# ------------------------------------------------------------------ controlli
class PerformanceChecker:
    def __init__(self, project_path: str):
        self.root = Path(project_path).resolve()
        self.issues = []      # critici
        self.warnings = []
        self.passed = []
        self.sources = {}     # percorso -> testo senza commenti
        for path in sorted(self.root.rglob('*')):
            if (path.suffix in SOURCE_EXTS and path.is_file() and not path.name.endswith('.d.ts')
                    and not SKIP_DIRS.intersection(path.relative_to(self.root).parts)):
                try:
                    self.sources[path] = strip_comments(path.read_text(encoding='utf-8'))
                except (OSError, UnicodeDecodeError):
                    continue
        self._read_project()

    def _read_project(self):
        """Tipo di progetto: dipendenze, next.config, alias dei percorsi."""
        deps = {}
        package = self.root / 'package.json'
        if package.is_file():
            try:
                data = json.loads(package.read_text(encoding='utf-8'))
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
            except (ValueError, OSError):
                pass
        configs = [p for p in self.root.glob('next.config.*') if p.is_file()]
        config = '\n'.join(strip_comments(p.read_text(encoding='utf-8', errors='replace')) for p in configs)
        self.is_next = ('next' in deps or bool(configs)
                        or any(re.search(r'from\s+[\'"]next(?:/[\w/-]+)?[\'"]', t) for t in self.sources.values()))
        self.react_compiler = (re.search(r'reactCompiler\s*:\s*(?:true|\{)', config) is not None
                               or 'babel-plugin-react-compiler' in deps)
        self.optimized = set()
        for group in re.findall(r'optimizePackageImports\s*:\s*\[([^\]]*)\]', config):
            self.optimized |= set(re.findall(r'[\'"]([^\'"]+)[\'"]', group))
        self.aliases = self._read_aliases()

    def _read_aliases(self):
        """Alias dei percorsi (compilerOptions.paths di tsconfig.json o jsconfig.json)."""
        for name in ('tsconfig.json', 'jsconfig.json'):
            path = self.root / name
            if not path.is_file():
                continue
            try:
                options = json.loads(strip_jsonc(path.read_text(encoding='utf-8'))).get('compilerOptions', {})
            except (ValueError, OSError):
                break
            base = self.root / options.get('baseUrl', '.')
            aliases = []
            for key, targets in (options.get('paths') or {}).items():
                if key.endswith('/*') and targets:
                    aliases.append((key[:-1], [base / t.rstrip('*') for t in targets]))
            return aliases
        return [('@/', [self.root / 'src', self.root]), ('~/', [self.root / 'src', self.root])]

    def _files(self, exts, tests=False):
        for path, text in self.sources.items():
            if path.suffix in exts and (tests or not TEST_FILE.search(path.name)):
                yield path, text

    def _rel(self, path):
        return path.relative_to(self.root).as_posix()

    def _add(self, critical, path, level, issue, fix, section):
        (self.issues if critical else self.warnings).append({
            'file': self._rel(path) if isinstance(path, Path) else path,
            'level': level, 'issue': issue, 'fix': fix, 'section': SECTION[section],
        })

    def check_waterfalls(self):
        """Await consecutivi nello stesso blocco, il secondo non usa il risultato del primo (sezione 1)."""
        print("\n[*] Cerco i waterfall (await consecutivi e indipendenti)...")
        found = 0
        for path, text in self._files(SOURCE_EXTS):
            lines = text.split('\n')
            pairs, i = [], 0
            while i < len(lines):
                first = AWAIT_STMT.match(lines[i])
                if not first or not first.group('lhs'):
                    i += 1
                    continue
                end_first = statement_end(lines, i)
                j = end_first + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                second = AWAIT_STMT.match(lines[j]) if j < len(lines) else None
                if (second and second.group('lhs') and second.group(1) == first.group(1)
                        and not awaits_existing_promise(first.group('expr'))
                        and not awaits_existing_promise(second.group('expr'))):
                    names = bound_names(first.group('lhs'))
                    second_text = '\n'.join(lines[j:statement_end(lines, j) + 1])
                    second_text = second_text.split('=', 1)[1] if '=' in second_text else second_text
                    if names and not any(uses(name, second_text) for name in names):
                        pairs.append(f"{i + 1}-{j + 1}")
                i = end_first + 1
            if pairs:
                found += len(pairs)
                self._add(True, path, 'CRITICO',
                          f"Await consecutivi e indipendenti alle righe {', '.join(pairs[:5])}"
                          + (f" (e altri {len(pairs) - 5})" if len(pairs) > 5 else ''),
                          "Falli partire insieme con Promise.all() (o avvia le promesse prima e fai await dopo)",
                          'async')
        if not found:
            self.passed.append('Nessun waterfall evidente')

    def _local_barrel(self, spec, path):
        """Il file index che riesporta altri moduli, se `spec` punta a un barrel file del progetto."""
        if spec.startswith('.'):
            bases = [path.parent / spec]
        else:
            bases = [target / spec[len(prefix):] for prefix, targets in self.aliases
                     if spec.startswith(prefix) for target in targets]
        for base in bases:
            if base.name == 'index':
                candidates = [base.with_name(name) for name in INDEX_FILES]
            elif base.is_dir():
                candidates = [base / name for name in INDEX_FILES]
            else:
                continue
            for index in candidates:
                if index.is_file():
                    count = len(RE_EXPORT.findall(index.read_text(encoding='utf-8', errors='replace')))
                    if count >= 2:
                        return index, count
        return None

    def _library_barrel(self, spec, clause):
        """Consiglio per un import da una libreria con un barrel file grande, o None."""
        named = '{' in clause
        if spec == 'lodash' and named:
            return ("lodash è CommonJS: un import con nome porta dentro tutta la libreria",
                    "Usa lodash-es oppure l'import della singola funzione (lodash/debounce)")
        package = package_name(spec)
        if not (self.is_next and named and spec == package and package in OTHER_HEAVY):
            return None
        if package in self.optimized:
            return None
        return (f"Import dal barrel file di {package}, che Next.js non ottimizza da solo",
                f"Aggiungi '{package}' a experimental.optimizePackageImports in next.config")

    def check_barrel_imports(self):
        """Import da barrel file locali e da librerie non ottimizzate (sezione 2)."""
        print("[*] Cerco i barrel import...")
        found = 0
        for path, text in self._files(SOURCE_EXTS):
            local = []
            for m in IMPORT.finditer(text):
                clause, spec = m.group(1), m.group(2)
                advice = self._library_barrel(spec, clause)
                if advice:
                    found += 1
                    self._add(False, path, 'ALTO', f"{advice[0]} (riga {line_of(text, m.start(2))})", advice[1], 'bundle')
                    continue
                barrel = self._local_barrel(spec, path)
                if barrel:
                    local.append(f"'{spec}' → {self._rel(barrel[0])} ({barrel[1]} riesportazioni)")
            if local:
                found += len(local)
                self._add(False, path, 'ALTO', 'Import da barrel file del progetto: ' + '; '.join(local[:3]),
                          'Importa dal file del modulo (es. @/components/Button): i barrel file rallentano '
                          "l'avvio in sviluppo e il cold start", 'bundle')
        if not found:
            self.passed.append('Nessun barrel import problematico')

    def check_dynamic_imports(self):
        """Componenti grandi importati staticamente (sezione 2)."""
        print("[*] Cerco gli import dinamici mancanti...")
        big = [p for p, t in self._files(('.tsx', '.jsx')) if len(t) > 10000]
        for component in big:
            name = component.stem
            pattern = re.compile(r'import\s+' + re.escape(name) + r'\b|import\s*\{[^}]*\b' + re.escape(name) + r'\b')
            for path, text in self._files(SOURCE_EXTS):
                if path != component and pattern.search(text) and 'dynamic(' not in text and 'lazy(' not in text:
                    self._add(False, path, 'MEDIO', f"Componente grande {name} ({len(self.sources[component]) // 1000} KB) importato staticamente",
                              "Se non serve al primo render, caricalo con next/dynamic (o React.lazy)", 'bundle')
                    break

    def check_useEffect_fetching(self):
        """Fetch dentro useEffect (sezione 4)."""
        print("[*] Cerco il data fetching in useEffect...")
        for path, text in self._files(('.ts', '.tsx', '.js', '.jsx')):
            lines = [line_of(text, pos) for pos, body in call_arguments(text, 'useEffect')
                     if re.search(r'\bfetch\s*\(|\baxios\b', body)]
            if lines:
                where = f"riga {lines[0]}" if len(lines) == 1 else f"righe {', '.join(map(str, lines[:5]))}"
                self._add(False, path, 'MEDIO-ALTO', f"Fetch dentro useEffect ({where})",
                          'Carica i dati in un Server Component, oppure usa SWR o React Query per deduplicare e mettere in cache',
                          'client')

    def check_missing_memoization(self):
        """Componenti con props senza memo, se il React Compiler non è attivo (sezione 5)."""
        print("[*] Cerco la memoizzazione mancante...")
        if self.react_compiler:
            self.passed.append('React Compiler attivo: memoizzazione automatica')
            return
        files = [self._rel(p) for p, t in self._files(('.tsx', '.jsx'))
                 if re.search(r'(?:export\s+)?(?:const|function)\s+[A-Z]\w+', t)
                 and 'memo(' not in t and ('props:' in t or 'Props>' in t or 'Props)' in t)]
        if files:
            self._add(False, f"{len(files)} file (es. {', '.join(files[:3])})", 'MEDIO',
                      'Componenti con props senza memo',
                      'Usa React.memo solo dove un componente si ri-renderizza spesso con le stesse props, '
                      'oppure attiva il React Compiler (reactCompiler: true in next.config)', 'rerender')

    def check_image_optimization(self):
        """<img> al posto di next/image, nei progetti Next.js (sezione 6)."""
        print("[*] Controllo l'ottimizzazione delle immagini...")
        if not self.is_next:
            return
        for path, text in self._files(('.tsx', '.jsx', '.js')):
            count = len(re.findall(r'<img\b', text))
            if count and 'next/image' not in text:
                self._add(False, path, 'MEDIO', f"{count} tag <img> al posto di next/image",
                          "Usa next/image per il ridimensionamento e il lazy loading automatici", 'rendering')

    # -------------------------------------------------------------- report
    def generate_report(self):
        print("\n" + "=" * 60)
        print("REPORT SULLE PRESTAZIONI REACT")
        print("=" * 60)

        print(f"\n[PROBLEMI CRITICI] ({len(self.issues)})")
        for issue in self.issues:
            self._print_item(issue)

        print(f"\n[AVVISI] ({len(self.warnings)})")
        for warning in self.warnings[:15]:
            self._print_item(warning)
        if len(self.warnings) > 15:
            print(f"  ... e altri {len(self.warnings) - 15} avvisi")

        if self.passed:
            print("\n[SUPERATI]")
            for item in self.passed:
                print(f"  + {item}")

        print("\n" + "=" * 60)
        print("RIEPILOGO:")
        print(f"  Problemi critici: {len(self.issues)}")
        print(f"  Avvisi: {len(self.warnings)}")
        print("=" * 60)
        if not self.issues and not self.warnings:
            print("\n[OK] Nessun problema di prestazioni rilevante!")
        elif self.issues:
            print("\n[AZIONE RICHIESTA] Correggi i problemi critici, poi valuta gli avvisi")
        else:
            print("\n[OK] Nessun problema critico: valuta gli avvisi qui sopra")

    @staticmethod
    def _print_item(item):
        print(f"  - [{item['level']}] {item['file']}")
        print(f"    Problema: {item['issue']}")
        print(f"    Correzione: {item['fix']}")
        print(f"    Riferimento: {item['section']}\n")

    def run(self):
        print("=" * 60)
        print("React Performance Checker (Vercel Engineering)")
        print("=" * 60)
        print(f"Cartella analizzata: {self.root}")
        print(f"Progetto: {'Next.js' if self.is_next else 'React'} · React Compiler: "
              f"{'attivo' if self.react_compiler else 'non attivo'} · {len(self.sources)} file sorgente")

        self.check_waterfalls()
        self.check_barrel_imports()
        self.check_dynamic_imports()
        self.check_useEffect_fetching()
        self.check_missing_memoization()
        self.check_image_optimization()

        self.generate_report()
        return 1 if self.issues else 0


def main():
    if len(sys.argv) < 2:
        print("Uso: python react_performance_checker.py <cartella_progetto>")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    if not project_path.is_dir():
        print(f"[ERRORE] Cartella non trovata: {project_path}")
        sys.exit(1)

    sys.exit(PerformanceChecker(str(project_path)).run())


if __name__ == '__main__':
    main()
