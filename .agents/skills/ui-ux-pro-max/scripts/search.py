#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Search - motore di ricerca BM25 sulle guide di stile UI/UX.
Il database in data/ è in inglese: scrivi le query con parole chiave in inglese.

Uso: python search.py "<query>" [--domain <dominio>] [--stack <stack>] [--max-results 3]
     python search.py "<query>" --design-system [-p "Nome progetto"]
     python search.py "<query>" --design-system --persist [-p "Nome progetto"] [--page "dashboard"]

Domini: style, prompt, color, chart, landing, product, ux, typography, icons, react, web
Stack: html-tailwind, react, nextjs, vue, nuxtjs, nuxt-ui, svelte, swiftui,
       react-native, flutter, shadcn, jetpack-compose

Salvataggio su file (pattern Master + Overrides):
  --persist    salva il design system in design-system/<progetto>/MASTER.md
  --page       crea anche il file di override della pagina in design-system/<progetto>/pages/
"""

import argparse
from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack
from design_system import generate_design_system, persist_design_system


def format_output(result):
    """Formatta i risultati per Claude, usando pochi token."""
    if "error" in result:
        return f"Errore: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max: linee guida dello stack")
        output.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        output.append(f"## UI Pro Max: risultati della ricerca")
        output.append(f"**Dominio:** {result['domain']} | **Query:** {result['query']}")
    output.append(f"**Fonte:** {result['file']} | **Trovati:** {result['count']} risultati\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### Risultato {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ricerca UI Pro Max nel database di design (in inglese: usa parole chiave in inglese)")
    parser.add_argument("query", help="query di ricerca, con parole chiave in inglese")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="dominio in cui cercare (se manca, viene dedotto dalla query)")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="cerca nelle linee guida di uno stack")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="numero massimo di risultati (predefinito: 3)")
    parser.add_argument("--json", action="store_true", help="stampa il risultato in JSON")
    # Generazione del design system
    parser.add_argument("--design-system", "-ds", action="store_true", help="genera un design system completo con le motivazioni")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="nome del progetto da mostrare nel design system")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="formato di output del design system")
    # Salvataggio su file (pattern Master + Overrides)
    parser.add_argument("--persist", action="store_true", help="salva il design system in design-system/<progetto>/MASTER.md (crea la struttura gerarchica)")
    parser.add_argument("--page", type=str, default=None, help="crea anche il file di override della pagina in design-system/<progetto>/pages/")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="cartella in cui salvare i file (predefinita: cartella corrente)")

    args = parser.parse_args()

    # Il design system ha la precedenza
    if args.design_system:
        result = generate_design_system(
            args.query, 
            args.project_name, 
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        # Conferma del salvataggio
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ Design system salvato in design-system/{project_slug}/")
            print(f"   📄 design-system/{project_slug}/MASTER.md (fonte di verità globale)")
            if args.page:
                page_filename = args.page.lower().replace(' ', '-')
                print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md (override della pagina)")
            print("")
            print(f"📖 Uso: quando costruisci una pagina, controlla prima design-system/{project_slug}/pages/[pagina].md.")
            print(f"   Se esiste, le sue regole sostituiscono MASTER.md. Altrimenti usa MASTER.md.")
            print("=" * 60)
    # Ricerca per stack
    elif args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    # Ricerca per dominio
    else:
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
