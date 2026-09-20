#!/usr/bin/env python3
"""
Script di conversione: React Best Practices (Vercel) → file di sezione della skill
Unisce le singole regole in 8 file, uno per sezione.

Uso:
    python .agents/skills/nextjs-react-expert/scripts/convert_rules.py

Legge le regole da others/agent-skills/skills/react-best-practices/rules (sorgente Vercel,
in inglese, esclusa da git) e riscrive i file 1-8 di questa skill.
ATTENZIONE: intestazioni, titoli delle sezioni e livelli di impatto escono in italiano,
ma il testo delle regole resta in inglese: dopo la rigenerazione va tradotto di nuovo.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Metadati delle sezioni (da _sections.md, tradotti).
# 'slug' fissa il nome del file, così i link nello SKILL.md non cambiano.
SECTIONS = {
    'async': {
        'number': 1,
        'title': 'Eliminare i waterfall',
        'slug': 'eliminating-waterfalls',
        'impact': 'CRITICAL',
        'description': "I waterfall sono il nemico numero uno delle prestazioni. Ogni await sequenziale aggiunge un'intera latenza di rete. Eliminarli porta i guadagni maggiori.",
        'overview': 'per eliminare i waterfall',
    },
    'bundle': {
        'number': 2,
        'title': 'Ottimizzare la dimensione del bundle',
        'slug': 'bundle-size-optimization',
        'impact': 'CRITICAL',
        'description': 'Ridurre la dimensione del bundle iniziale migliora il Time to Interactive e il Largest Contentful Paint.',
        'overview': 'per ottimizzare la dimensione del bundle',
    },
    'server': {
        'number': 3,
        'title': 'Prestazioni lato server',
        'slug': 'server-side-performance',
        'impact': 'HIGH',
        'description': 'Ottimizzare il rendering lato server e il recupero dei dati elimina i waterfall lato server e riduce i tempi di risposta.',
        'overview': 'per migliorare le prestazioni lato server',
    },
    'client': {
        'number': 4,
        'title': 'Recupero dei dati lato client',
        'slug': 'client-side-data-fetching',
        'impact': 'MEDIUM-HIGH',
        'description': 'La deduplicazione automatica e pattern di fetch efficienti riducono le richieste di rete ridondanti.',
        'overview': 'dedicate al recupero dei dati lato client',
    },
    'rerender': {
        'number': 5,
        'title': 'Ottimizzare i re-render',
        'slug': 're-render-optimization',
        'impact': 'MEDIUM',
        'description': 'Ridurre i re-render non necessari evita calcoli sprecati e rende la UI più reattiva.',
        'overview': "dedicate all'ottimizzazione dei re-render",
    },
    'rendering': {
        'number': 6,
        'title': 'Prestazioni del rendering',
        'slug': 'rendering-performance',
        'impact': 'MEDIUM',
        'description': 'Ottimizzare il processo di rendering riduce il lavoro che il browser deve svolgere.',
        'overview': 'dedicate alle prestazioni del rendering',
    },
    'js': {
        'number': 7,
        'title': 'Prestazioni di JavaScript',
        'slug': 'javascript-performance',
        'impact': 'LOW-MEDIUM',
        'description': 'Le micro-ottimizzazioni negli hot path, sommate, possono portare a miglioramenti significativi.',
        'overview': 'dedicate alle prestazioni di JavaScript',
    },
    'advanced': {
        'number': 8,
        'title': 'Pattern avanzati',
        'slug': 'advanced-patterns',
        'impact': 'VARIABLE',
        'description': "Pattern avanzati per casi specifici che richiedono un'implementazione attenta.",
        'overview': 'dedicate ai pattern avanzati',
    }
}

# Livelli di impatto: sorgente in inglese → testo della skill
IMPACT_IT = {
    'CRITICAL': 'CRITICO',
    'HIGH': 'ALTO',
    'MEDIUM-HIGH': 'MEDIO-ALTO',
    'MEDIUM': 'MEDIO',
    'LOW-MEDIUM': 'MEDIO-BASSO',
    'LOW': 'BASSO',
    'VARIABLE': 'VARIABILE',
}


def translate_impact(value: str) -> str:
    """Traduce il livello di impatto iniziale (es. 'HIGH (…)' → 'ALTO (…)'); il resto resta com'è."""
    match = re.match(r'([A-Z]+(?:-[A-Z]+)?)(.*)', value.strip())
    if not match or match.group(1) not in IMPACT_IT:
        return value
    return IMPACT_IT[match.group(1)] + match.group(2)


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Separa il frontmatter Markdown dal corpo."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    # Frontmatter YAML letto a mano (solo chiave: valore)
    frontmatter = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    body = parts[2].strip()
    return frontmatter, body


def parse_rule_file(filepath: Path) -> Dict:
    """Legge il file di una singola regola."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    # Il prefisso della sezione viene dal nome del file
    filename = filepath.stem
    prefix = filename.split('-')[0]

    return {
        'filename': filepath.name,
        'prefix': prefix,
        'title': frontmatter.get('title', filename),
        'impact': frontmatter.get('impact', ''),
        'impactDescription': frontmatter.get('impactDescription', ''),
        'tags': frontmatter.get('tags', ''),
        'body': body,
        'frontmatter': frontmatter
    }


def group_rules_by_section(rules_dir: Path) -> Dict[str, List[Dict]]:
    """Raggruppa le regole per prefisso di sezione."""
    grouped = {prefix: [] for prefix in SECTIONS.keys()}

    for rule_file in sorted(rules_dir.glob('*.md')):
        # Salta i file speciali
        if rule_file.name.startswith('_'):
            continue

        rule = parse_rule_file(rule_file)
        prefix = rule['prefix']

        if prefix in grouped:
            grouped[prefix].append(rule)
        else:
            print(f"[ATTENZIONE] Prefisso sconosciuto '{prefix}' nel file: {rule_file.name}")

    return grouped


def generate_section_file(section_prefix: str, rules: List[Dict], output_dir: Path) -> bool:
    """Genera il file di una sezione unendo le sue regole; restituisce True se lo ha scritto."""
    if not rules:
        print(f"[ATTENZIONE] Nessuna regola trovata per la sezione: {section_prefix}")
        return False

    section_meta = SECTIONS[section_prefix]
    section_num = section_meta['number']
    section_title = section_meta['title']
    impact = translate_impact(section_meta['impact'])
    description = section_meta['description']

    # Ordina le regole per titolo
    rules.sort(key=lambda r: r['title'])

    # Costruisce il contenuto
    content = f"""# {section_num}. {section_title}

> **Impatto:** {impact}
> **Obiettivo:** {description}

---

## Panoramica

Questa sezione contiene **{len(rules)} regole** {section_meta['overview']}.

"""

    # Aggiunge le regole
    for i, rule in enumerate(rules, 1):
        rule_id = f"{section_num}.{i}"
        title = rule['title']
        rule_impact = translate_impact(rule['impact'])
        tags = rule['tags']
        body = rule['body']

        content += f"""---

## Regola {rule_id}: {title}

"""

        if rule_impact:
            content += f"**Impatto:** {rule_impact}  \n"

        if tags:
            content += f"**Tag:** {tags}  \n"

        content += f"\n{body}\n\n"

    # Scrive il file (CRLF, come il resto del repository)
    output_file = output_dir / f"{section_num}-{section_prefix}-{section_meta['slug']}.md"
    output_file.write_bytes(content.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))
    print(f"[OK] Generato: {output_file.name} ({len(rules)} regole)")
    return True


def main():
    """Conversione completa."""
    # Percorsi: scripts/ → nextjs-react-expert/ → skills/ → .agents/ → radice del repository
    skill_dir = Path(__file__).resolve().parent.parent
    base_dir = skill_dir.parent.parent.parent
    rules_dir = base_dir / "others/agent-skills/skills/react-best-practices/rules"
    output_dir = skill_dir

    print(f"[*] Lettura delle regole da: {rules_dir}")
    print(f"[*] Output in: {output_dir}")
    print()

    # Controlla che la cartella delle regole esista
    if not rules_dir.exists():
        print(f"[ERRORE] Cartella delle regole non trovata: {rules_dir}")
        return

    # Raggruppa le regole
    print("[*] Raggruppamento delle regole per sezione...")
    grouped_rules = group_rules_by_section(rules_dir)

    # Statistiche
    total_rules = sum(len(rules) for rules in grouped_rules.values())
    print(f"[*] Trovate {total_rules} regole in totale")
    print()

    # Genera i file di sezione
    print("[*] Generazione dei file di sezione...")
    generated = 0
    for section_prefix in SECTIONS.keys():
        rules = grouped_rules[section_prefix]
        generated += generate_section_file(section_prefix, rules, output_dir)

    print()
    print("[OK] Conversione completata.")
    print(f"[*] Generati {generated} file di sezione da {total_rules} regole")
    print("[!] Il testo delle regole è in inglese: traducilo di nuovo in italiano.")


if __name__ == '__main__':
    main()
