#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Design System Generator - combina i risultati di più ricerche e applica le regole
di ragionamento per generare raccomandazioni complete di design system.
Il database in data/ è in inglese: query, parole chiave e valori dei CSV restano in inglese.

Uso:
    from design_system import generate_design_system
    result = generate_design_system("SaaS dashboard", "My Project")
    
    # Con salvataggio su file (pattern Master + Overrides)
    result = generate_design_system("SaaS dashboard", "My Project", persist=True)
    result = generate_design_system("SaaS dashboard", "My Project", persist=True, page="dashboard")
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from core import search, DATA_DIR


# ============ CONFIGURAZIONE ============
REASONING_FILE = "ui-reasoning.csv"

SEARCH_CONFIG = {
    "product": {"max_results": 1},
    "style": {"max_results": 3},
    "color": {"max_results": 2},
    "landing": {"max_results": 2},
    "typography": {"max_results": 2}
}


# ============ GENERATORE DEL DESIGN SYSTEM ============
class DesignSystemGenerator:
    """Genera le raccomandazioni di design system combinando più ricerche."""

    def __init__(self):
        self.reasoning_data = self._load_reasoning()

    def _load_reasoning(self) -> list:
        """Carica dal CSV le regole di ragionamento."""
        filepath = DATA_DIR / REASONING_FILE
        if not filepath.exists():
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _multi_domain_search(self, query: str, style_priority: list = None) -> dict:
        """Esegue le ricerche su più domini."""
        results = {}
        for domain, config in SEARCH_CONFIG.items():
            if domain == "style" and style_priority:
                # Per lo stile cerca anche con le parole chiave prioritarie
                priority_query = " ".join(style_priority[:2]) if style_priority else query
                combined_query = f"{query} {priority_query}"
                results[domain] = search(combined_query, domain, config["max_results"])
            else:
                results[domain] = search(query, domain, config["max_results"])
        return results

    def _find_reasoning_rule(self, category: str) -> dict:
        """Trova la regola di ragionamento adatta a una categoria."""
        category_lower = category.lower()

        # Prima prova la corrispondenza esatta
        for rule in self.reasoning_data:
            if rule.get("UI_Category", "").lower() == category_lower:
                return rule

        # Poi la corrispondenza parziale
        for rule in self.reasoning_data:
            ui_cat = rule.get("UI_Category", "").lower()
            if ui_cat in category_lower or category_lower in ui_cat:
                return rule

        # Infine la corrispondenza per parole chiave
        for rule in self.reasoning_data:
            ui_cat = rule.get("UI_Category", "").lower()
            keywords = ui_cat.replace("/", " ").replace("-", " ").split()
            if any(kw in category_lower for kw in keywords):
                return rule

        return {}

    def _apply_reasoning(self, category: str, search_results: dict) -> dict:
        """Applica le regole di ragionamento ai risultati della ricerca."""
        rule = self._find_reasoning_rule(category)

        if not rule:
            return {
                "pattern": "Hero + Features + CTA",
                "style_priority": ["Minimalism", "Flat Design"],
                "color_mood": "Professional",
                "typography_mood": "Clean",
                "key_effects": "Subtle hover transitions",
                "anti_patterns": "",
                "decision_rules": {},
                "severity": "MEDIUM"
            }

        # Legge il JSON con le regole di decisione
        decision_rules = {}
        try:
            decision_rules = json.loads(rule.get("Decision_Rules", "{}"))
        except json.JSONDecodeError:
            pass

        return {
            "pattern": rule.get("Recommended_Pattern", ""),
            "style_priority": [s.strip() for s in rule.get("Style_Priority", "").split("+")],
            "color_mood": rule.get("Color_Mood", ""),
            "typography_mood": rule.get("Typography_Mood", ""),
            "key_effects": rule.get("Key_Effects", ""),
            "anti_patterns": rule.get("Anti_Patterns", ""),
            "decision_rules": decision_rules,
            "severity": rule.get("Severity", "MEDIUM")
        }

    def _select_best_match(self, results: list, priority_keywords: list) -> dict:
        """Sceglie il risultato migliore in base alle parole chiave prioritarie."""
        if not results:
            return {}

        if not priority_keywords:
            return results[0]

        # Primo tentativo: il nome dello stile corrisponde
        for priority in priority_keywords:
            priority_lower = priority.lower().strip()
            for result in results:
                style_name = result.get("Style Category", "").lower()
                if priority_lower in style_name or style_name in priority_lower:
                    return result

        # Secondo tentativo: punteggio per le parole chiave trovate nei campi
        scored = []
        for result in results:
            result_str = str(result).lower()
            score = 0
            for kw in priority_keywords:
                kw_lower = kw.lower().strip()
                # Punteggio alto se compare nel nome dello stile
                if kw_lower in result.get("Style Category", "").lower():
                    score += 10
                # Punteggio minore se compare nel campo Keywords
                elif kw_lower in result.get("Keywords", "").lower():
                    score += 3
                # Punteggio ancora minore se compare negli altri campi
                elif kw_lower in result_str:
                    score += 1
            scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored and scored[0][0] > 0 else results[0]

    def _extract_results(self, search_result: dict) -> list:
        """Estrae la lista dei risultati dal dict restituito dalla ricerca."""
        return search_result.get("results", [])

    def generate(self, query: str, project_name: str = None) -> dict:
        """Genera la raccomandazione completa di design system."""
        # Passo 1: cerca prima il tipo di prodotto per ricavare la categoria
        product_result = search(query, "product", 1)
        product_results = product_result.get("results", [])
        category = "General"
        if product_results:
            category = product_results[0].get("Product Type", "General")

        # Passo 2: prende le regole di ragionamento della categoria
        reasoning = self._apply_reasoning(category, {})
        style_priority = reasoning.get("style_priority", [])

        # Passo 3: ricerca su più domini guidata dagli stili prioritari
        search_results = self._multi_domain_search(query, style_priority)
        search_results["product"] = product_result  # Riusa la ricerca del prodotto

        # Passo 4: sceglie il risultato migliore di ogni dominio in base alla priorità
        style_results = self._extract_results(search_results.get("style", {}))
        color_results = self._extract_results(search_results.get("color", {}))
        typography_results = self._extract_results(search_results.get("typography", {}))
        landing_results = self._extract_results(search_results.get("landing", {}))

        best_style = self._select_best_match(style_results, reasoning.get("style_priority", []))
        best_color = color_results[0] if color_results else {}
        best_typography = typography_results[0] if typography_results else {}
        best_landing = landing_results[0] if landing_results else {}

        # Passo 5: costruisce la raccomandazione finale
        # Combina gli effetti delle regole di ragionamento e della ricerca di stile
        style_effects = best_style.get("Effects & Animation", "")
        reasoning_effects = reasoning.get("key_effects", "")
        combined_effects = style_effects if style_effects else reasoning_effects

        return {
            "project_name": project_name or query.upper(),
            "category": category,
            "pattern": {
                "name": best_landing.get("Pattern Name", reasoning.get("pattern", "Hero + Features + CTA")),
                "sections": best_landing.get("Section Order", "Hero > Features > CTA"),
                "cta_placement": best_landing.get("Primary CTA Placement", "Above fold"),
                "color_strategy": best_landing.get("Color Strategy", ""),
                "conversion": best_landing.get("Conversion Optimization", "")
            },
            "style": {
                "name": best_style.get("Style Category", "Minimalism"),
                "type": best_style.get("Type", "General"),
                "effects": style_effects,
                "keywords": best_style.get("Keywords", ""),
                "best_for": best_style.get("Best For", ""),
                "performance": best_style.get("Performance", ""),
                "accessibility": best_style.get("Accessibility", "")
            },
            "colors": {
                "primary": best_color.get("Primary (Hex)", "#2563EB"),
                "secondary": best_color.get("Secondary (Hex)", "#3B82F6"),
                "cta": best_color.get("CTA (Hex)", "#F97316"),
                "background": best_color.get("Background (Hex)", "#F8FAFC"),
                "text": best_color.get("Text (Hex)", "#1E293B"),
                "notes": best_color.get("Notes", "")
            },
            "typography": {
                "heading": best_typography.get("Heading Font", "Inter"),
                "body": best_typography.get("Body Font", "Inter"),
                "mood": best_typography.get("Mood/Style Keywords", reasoning.get("typography_mood", "")),
                "best_for": best_typography.get("Best For", ""),
                "google_fonts_url": best_typography.get("Google Fonts URL", ""),
                "css_import": best_typography.get("CSS Import", "")
            },
            "key_effects": combined_effects,
            "anti_patterns": reasoning.get("anti_patterns", ""),
            "decision_rules": reasoning.get("decision_rules", {}),
            "severity": reasoning.get("severity", "MEDIUM")
        }


# ============ FORMATTAZIONE DELL'OUTPUT ============
BOX_WIDTH = 90  # riquadro largo per contenere più testo

def format_ascii_box(design_system: dict) -> str:
    """Formatta il design system come riquadro ASCII (stile MCP)."""
    project = design_system.get("project_name", "PROGETTO")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")

    def wrap_text(text: str, prefix: str, width: int) -> list:
        """Manda a capo il testo lungo su più righe."""
        if not text:
            return []
        words = text.split()
        lines = []
        current_line = prefix
        for word in words:
            if len(current_line) + len(word) + 1 <= width - 2:
                current_line += (" " if current_line != prefix else "") + word
            else:
                if current_line != prefix:
                    lines.append(current_line)
                current_line = prefix + word
        if current_line != prefix:
            lines.append(current_line)
        return lines

    # Ricava le sezioni dal pattern
    sections = pattern.get("sections", "").split(">")
    sections = [s.strip() for s in sections if s.strip()]

    # Costruisce le righe di output
    lines = []
    w = BOX_WIDTH - 1

    lines.append("+" + "-" * w + "+")
    lines.append(f"|  PROGETTO: {project} - DESIGN SYSTEM CONSIGLIATO".ljust(BOX_WIDTH) + "|")
    lines.append("+" + "-" * w + "+")
    lines.append("|" + " " * w + "|")

    # Sezione pattern
    lines.append(f"|  PATTERN: {pattern.get('name', '')}".ljust(BOX_WIDTH) + "|")
    if pattern.get('conversion'):
        lines.append(f"|     Conversione: {pattern.get('conversion', '')}".ljust(BOX_WIDTH) + "|")
    if pattern.get('cta_placement'):
        lines.append(f"|     CTA: {pattern.get('cta_placement', '')}".ljust(BOX_WIDTH) + "|")
    lines.append("|     Sezioni:".ljust(BOX_WIDTH) + "|")
    for i, section in enumerate(sections, 1):
        lines.append(f"|       {i}. {section}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * w + "|")

    # Sezione stile
    lines.append(f"|  STILE: {style.get('name', '')}".ljust(BOX_WIDTH) + "|")
    if style.get("keywords"):
        for line in wrap_text(f"Parole chiave: {style.get('keywords', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if style.get("best_for"):
        for line in wrap_text(f"Ideale per: {style.get('best_for', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if style.get("performance") or style.get("accessibility"):
        perf_a11y = f"Prestazioni: {style.get('performance', '')} | Accessibilità: {style.get('accessibility', '')}"
        lines.append(f"|     {perf_a11y}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * w + "|")

    # Sezione colori
    lines.append("|  COLORI:".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Primario:   {colors.get('primary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Secondario: {colors.get('secondary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     CTA:        {colors.get('cta', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Sfondo:     {colors.get('background', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Testo:      {colors.get('text', '')}".ljust(BOX_WIDTH) + "|")
    if colors.get("notes"):
        for line in wrap_text(f"Note: {colors.get('notes', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * w + "|")

    # Sezione tipografia
    lines.append(f"|  TIPOGRAFIA: {typography.get('heading', '')} / {typography.get('body', '')}".ljust(BOX_WIDTH) + "|")
    if typography.get("mood"):
        for line in wrap_text(f"Mood: {typography.get('mood', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if typography.get("best_for"):
        for line in wrap_text(f"Ideale per: {typography.get('best_for', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if typography.get("google_fonts_url"):
        lines.append(f"|     Google Fonts: {typography.get('google_fonts_url', '')}".ljust(BOX_WIDTH) + "|")
    if typography.get("css_import"):
        lines.append(f"|     Import CSS: {typography.get('css_import', '')[:70]}...".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * w + "|")

    # Sezione effetti chiave
    if effects:
        lines.append("|  EFFETTI CHIAVE:".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(effects, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * w + "|")

    # Sezione anti-pattern
    if anti_patterns:
        lines.append("|  DA EVITARE (anti-pattern):".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(anti_patterns, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * w + "|")

    # Sezione checklist prima della consegna
    lines.append("|  CHECKLIST PRIMA DELLA CONSEGNA:".ljust(BOX_WIDTH) + "|")
    checklist_items = [
        "[ ] Niente emoji come icone (usa SVG: Heroicons/Lucide)",
        "[ ] cursor-pointer su tutti gli elementi cliccabili",
        "[ ] Stati hover con transizioni morbide (150-300ms)",
        "[ ] Light mode: contrasto del testo di almeno 4.5:1",
        "[ ] Stati di focus visibili per la navigazione da tastiera",
        "[ ] prefers-reduced-motion rispettato",
        "[ ] Responsive: 375px, 768px, 1024px, 1440px"
    ]
    for item in checklist_items:
        lines.append(f"|     {item}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * w + "|")

    lines.append("+" + "-" * w + "+")

    return "\n".join(lines)


def format_markdown(design_system: dict) -> str:
    """Formatta il design system in markdown."""
    project = design_system.get("project_name", "PROGETTO")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")

    lines = []
    lines.append(f"## Design System: {project}")
    lines.append("")

    # Sezione pattern
    lines.append("### Pattern")
    lines.append(f"- **Nome:** {pattern.get('name', '')}")
    if pattern.get('conversion'):
        lines.append(f"- **Obiettivo di conversione:** {pattern.get('conversion', '')}")
    if pattern.get('cta_placement'):
        lines.append(f"- **Posizione della CTA:** {pattern.get('cta_placement', '')}")
    if pattern.get('color_strategy'):
        lines.append(f"- **Strategia dei colori:** {pattern.get('color_strategy', '')}")
    lines.append(f"- **Sezioni:** {pattern.get('sections', '')}")
    lines.append("")

    # Sezione stile
    lines.append("### Stile")
    lines.append(f"- **Nome:** {style.get('name', '')}")
    if style.get('keywords'):
        lines.append(f"- **Parole chiave:** {style.get('keywords', '')}")
    if style.get('best_for'):
        lines.append(f"- **Ideale per:** {style.get('best_for', '')}")
    if style.get('performance') or style.get('accessibility'):
        lines.append(f"- **Prestazioni:** {style.get('performance', '')} | **Accessibilità:** {style.get('accessibility', '')}")
    lines.append("")

    # Sezione colori
    lines.append("### Colori")
    lines.append(f"| Ruolo | Hex |")
    lines.append(f"|-------|-----|")
    lines.append(f"| Primario | {colors.get('primary', '')} |")
    lines.append(f"| Secondario | {colors.get('secondary', '')} |")
    lines.append(f"| CTA | {colors.get('cta', '')} |")
    lines.append(f"| Sfondo | {colors.get('background', '')} |")
    lines.append(f"| Testo | {colors.get('text', '')} |")
    if colors.get("notes"):
        lines.append(f"\n*Note: {colors.get('notes', '')}*")
    lines.append("")

    # Sezione tipografia
    lines.append("### Tipografia")
    lines.append(f"- **Titoli:** {typography.get('heading', '')}")
    lines.append(f"- **Testo:** {typography.get('body', '')}")
    if typography.get("mood"):
        lines.append(f"- **Mood:** {typography.get('mood', '')}")
    if typography.get("best_for"):
        lines.append(f"- **Ideale per:** {typography.get('best_for', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** {typography.get('google_fonts_url', '')}")
    if typography.get("css_import"):
        lines.append(f"- **Import CSS:**")
        lines.append(f"```css")
        lines.append(f"{typography.get('css_import', '')}")
        lines.append(f"```")
    lines.append("")

    # Sezione effetti chiave
    if effects:
        lines.append("### Effetti chiave")
        lines.append(f"{effects}")
        lines.append("")

    # Sezione anti-pattern
    if anti_patterns:
        lines.append("### Da evitare (anti-pattern)")
        newline_bullet = '\n- '
        lines.append(f"- {anti_patterns.replace(' + ', newline_bullet)}")
        lines.append("")

    # Sezione checklist prima della consegna
    lines.append("### Checklist prima della consegna")
    lines.append("- [ ] Niente emoji come icone (usa SVG: Heroicons/Lucide)")
    lines.append("- [ ] cursor-pointer su tutti gli elementi cliccabili")
    lines.append("- [ ] Stati hover con transizioni morbide (150-300ms)")
    lines.append("- [ ] Light mode: contrasto del testo di almeno 4.5:1")
    lines.append("- [ ] Stati di focus visibili per la navigazione da tastiera")
    lines.append("- [ ] prefers-reduced-motion rispettato")
    lines.append("- [ ] Responsive: 375px, 768px, 1024px, 1440px")
    lines.append("")

    return "\n".join(lines)


# ============ PUNTO DI INGRESSO PRINCIPALE ============
def generate_design_system(query: str, project_name: str = None, output_format: str = "ascii", 
                           persist: bool = False, page: str = None, output_dir: str = None) -> str:
    """
    Punto di ingresso principale per generare il design system.

    Args:
        query: query di ricerca con parole chiave in inglese (es. "SaaS dashboard", "e-commerce luxury")
        project_name: nome del progetto per l'intestazione (facoltativo)
        output_format: "ascii" (predefinito) o "markdown"
        persist: se True, salva il design system nella cartella design-system/<progetto>/
        page: nome della pagina per il file di override (facoltativo)
        output_dir: cartella di output (facoltativa, predefinita: la cartella di lavoro corrente)

    Returns:
        il design system formattato, come stringa
    """
    generator = DesignSystemGenerator()
    design_system = generator.generate(query, project_name)
    
    # Salva su file se richiesto
    if persist:
        persist_design_system(design_system, page, output_dir, query)

    if output_format == "markdown":
        return format_markdown(design_system)
    return format_ascii_box(design_system)


# ============ SALVATAGGIO SU FILE ============
def persist_design_system(design_system: dict, page: str = None, output_dir: str = None, page_query: str = None) -> dict:
    """
    Salva il design system nella cartella design-system/<progetto>/ con il pattern Master + Overrides.
    
    Args:
        design_system: il dict del design system generato
        page: nome della pagina per il file di override (facoltativo)
        output_dir: cartella di output (facoltativa, predefinita: la cartella di lavoro corrente)
        page_query: query per generare override mirati per la pagina (facoltativa)
    
    Returns:
        dict con i percorsi dei file creati e lo stato
    """
    base_dir = Path(output_dir) if output_dir else Path.cwd()
    
    # Usa il nome del progetto per la sua cartella
    project_name = design_system.get("project_name", "default")
    project_slug = project_name.lower().replace(' ', '-')
    
    design_system_dir = base_dir / "design-system" / project_slug
    pages_dir = design_system_dir / "pages"
    
    created_files = []
    
    # Crea le cartelle
    design_system_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    master_file = design_system_dir / "MASTER.md"
    
    # Genera e scrive MASTER.md
    master_content = format_master_md(design_system)
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write(master_content)
    created_files.append(str(master_file))
    
    # Se è indicata una pagina, crea il suo file di override con contenuto mirato
    if page:
        page_file = pages_dir / f"{page.lower().replace(' ', '-')}.md"
        page_content = format_page_override_md(design_system, page, page_query)
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
        created_files.append(str(page_file))
    
    return {
        "status": "success",
        "design_system_dir": str(design_system_dir),
        "created_files": created_files
    }


def format_master_md(design_system: dict) -> str:
    """Formatta il design system come MASTER.md, con la logica gerarchica degli override."""
    project = design_system.get("project_name", "PROGETTO")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = []
    
    # Intestazione con la logica
    lines.append("# Design System: file Master")
    lines.append("")
    lines.append("> **LOGICA:** quando costruisci una pagina specifica, controlla prima `pages/[nome-pagina].md` accanto a questo file.")
    lines.append("> Se quel file esiste, le sue regole **sostituiscono** questo file Master.")
    lines.append("> Altrimenti segui alla lettera le regole qui sotto.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Progetto:** {project}")
    lines.append(f"**Generato il:** {timestamp}")
    lines.append(f"**Categoria:** {design_system.get('category', 'General')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Sezione regole globali
    lines.append("## Regole globali")
    lines.append("")
    
    # Palette dei colori
    lines.append("### Palette dei colori")
    lines.append("")
    lines.append("| Ruolo | Hex | Variabile CSS |")
    lines.append("|-------|-----|---------------|")
    lines.append(f"| Primario | `{colors.get('primary', '#2563EB')}` | `--color-primary` |")
    lines.append(f"| Secondario | `{colors.get('secondary', '#3B82F6')}` | `--color-secondary` |")
    lines.append(f"| CTA/Accento | `{colors.get('cta', '#F97316')}` | `--color-cta` |")
    lines.append(f"| Sfondo | `{colors.get('background', '#F8FAFC')}` | `--color-background` |")
    lines.append(f"| Testo | `{colors.get('text', '#1E293B')}` | `--color-text` |")
    lines.append("")
    if colors.get("notes"):
        lines.append(f"**Note sui colori:** {colors.get('notes', '')}")
        lines.append("")
    
    # Tipografia
    lines.append("### Tipografia")
    lines.append("")
    lines.append(f"- **Font dei titoli:** {typography.get('heading', 'Inter')}")
    lines.append(f"- **Font del testo:** {typography.get('body', 'Inter')}")
    if typography.get("mood"):
        lines.append(f"- **Mood:** {typography.get('mood', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** [{typography.get('heading', '')} + {typography.get('body', '')}]({typography.get('google_fonts_url', '')})")
    lines.append("")
    if typography.get("css_import"):
        lines.append("**Import CSS:**")
        lines.append("```css")
        lines.append(typography.get("css_import", ""))
        lines.append("```")
        lines.append("")
    
    # Variabili di spaziatura
    lines.append("### Variabili di spaziatura")
    lines.append("")
    lines.append("| Token | Valore | Uso |")
    lines.append("|-------|-------|-------|")
    lines.append("| `--space-xs` | `4px` / `0.25rem` | Spazi stretti |")
    lines.append("| `--space-sm` | `8px` / `0.5rem` | Spazi tra icone, spaziatura inline |")
    lines.append("| `--space-md` | `16px` / `1rem` | Padding standard |")
    lines.append("| `--space-lg` | `24px` / `1.5rem` | Padding delle sezioni |")
    lines.append("| `--space-xl` | `32px` / `2rem` | Spazi ampi |")
    lines.append("| `--space-2xl` | `48px` / `3rem` | Margini tra le sezioni |")
    lines.append("| `--space-3xl` | `64px` / `4rem` | Padding dell'hero |")
    lines.append("")
    
    # Livelli di ombra
    lines.append("### Livelli di ombra")
    lines.append("")
    lines.append("| Livello | Valore | Uso |")
    lines.append("|-------|-------|-------|")
    lines.append("| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Leggero rilievo |")
    lines.append("| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Card, pulsanti |")
    lines.append("| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modali, menu a tendina |")
    lines.append("| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Immagini hero, card in evidenza |")
    lines.append("")
    
    # Sezione specifiche dei componenti
    lines.append("---")
    lines.append("")
    lines.append("## Specifiche dei componenti")
    lines.append("")
    
    # Pulsanti
    lines.append("### Pulsanti")
    lines.append("")
    lines.append("```css")
    lines.append("/* Pulsante primario */")
    lines.append(".btn-primary {")
    lines.append(f"  background: {colors.get('cta', '#F97316')};")
    lines.append("  color: white;")
    lines.append("  padding: 12px 24px;")
    lines.append("  border-radius: 8px;")
    lines.append("  font-weight: 600;")
    lines.append("  transition: all 200ms ease;")
    lines.append("  cursor: pointer;")
    lines.append("}")
    lines.append("")
    lines.append(".btn-primary:hover {")
    lines.append("  opacity: 0.9;")
    lines.append("  transform: translateY(-1px);")
    lines.append("}")
    lines.append("")
    lines.append("/* Pulsante secondario */")
    lines.append(".btn-secondary {")
    lines.append(f"  background: transparent;")
    lines.append(f"  color: {colors.get('primary', '#2563EB')};")
    lines.append(f"  border: 2px solid {colors.get('primary', '#2563EB')};")
    lines.append("  padding: 12px 24px;")
    lines.append("  border-radius: 8px;")
    lines.append("  font-weight: 600;")
    lines.append("  transition: all 200ms ease;")
    lines.append("  cursor: pointer;")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Card
    lines.append("### Card")
    lines.append("")
    lines.append("```css")
    lines.append(".card {")
    lines.append(f"  background: {colors.get('background', '#FFFFFF')};")
    lines.append("  border-radius: 12px;")
    lines.append("  padding: 24px;")
    lines.append("  box-shadow: var(--shadow-md);")
    lines.append("  transition: all 200ms ease;")
    lines.append("  cursor: pointer;")
    lines.append("}")
    lines.append("")
    lines.append(".card:hover {")
    lines.append("  box-shadow: var(--shadow-lg);")
    lines.append("  transform: translateY(-2px);")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Campi di input
    lines.append("### Campi di input")
    lines.append("")
    lines.append("```css")
    lines.append(".input {")
    lines.append("  padding: 12px 16px;")
    lines.append("  border: 1px solid #E2E8F0;")
    lines.append("  border-radius: 8px;")
    lines.append("  font-size: 16px;")
    lines.append("  transition: border-color 200ms ease;")
    lines.append("}")
    lines.append("")
    lines.append(".input:focus {")
    lines.append(f"  border-color: {colors.get('primary', '#2563EB')};")
    lines.append("  outline: none;")
    lines.append(f"  box-shadow: 0 0 0 3px {colors.get('primary', '#2563EB')}20;")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Modali
    lines.append("### Modali")
    lines.append("")
    lines.append("```css")
    lines.append(".modal-overlay {")
    lines.append("  background: rgba(0, 0, 0, 0.5);")
    lines.append("  backdrop-filter: blur(4px);")
    lines.append("}")
    lines.append("")
    lines.append(".modal {")
    lines.append("  background: white;")
    lines.append("  border-radius: 16px;")
    lines.append("  padding: 32px;")
    lines.append("  box-shadow: var(--shadow-xl);")
    lines.append("  max-width: 500px;")
    lines.append("  width: 90%;")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Sezione stile
    lines.append("---")
    lines.append("")
    lines.append("## Linee guida di stile")
    lines.append("")
    lines.append(f"**Stile:** {style.get('name', 'Minimalism')}")
    lines.append("")
    if style.get("keywords"):
        lines.append(f"**Parole chiave:** {style.get('keywords', '')}")
        lines.append("")
    if style.get("best_for"):
        lines.append(f"**Ideale per:** {style.get('best_for', '')}")
        lines.append("")
    if effects:
        lines.append(f"**Effetti chiave:** {effects}")
        lines.append("")
    
    # Pattern della pagina
    lines.append("### Pattern della pagina")
    lines.append("")
    lines.append(f"**Nome del pattern:** {pattern.get('name', '')}")
    lines.append("")
    if pattern.get('conversion'):
        lines.append(f"- **Strategia di conversione:** {pattern.get('conversion', '')}")
    if pattern.get('cta_placement'):
        lines.append(f"- **Posizione della CTA:** {pattern.get('cta_placement', '')}")
    lines.append(f"- **Ordine delle sezioni:** {pattern.get('sections', '')}")
    lines.append("")
    
    # Sezione anti-pattern
    lines.append("---")
    lines.append("")
    lines.append("## Anti-pattern (da NON usare)")
    lines.append("")
    if anti_patterns:
        anti_list = [a.strip() for a in anti_patterns.split("+")]
        for anti in anti_list:
            if anti:
                lines.append(f"- ❌ {anti}")
    lines.append("")
    lines.append("### Altri pattern vietati")
    lines.append("")
    lines.append("- ❌ **Emoji come icone** — usa icone SVG (Heroicons, Lucide, Simple Icons)")
    lines.append("- ❌ **cursor:pointer mancante** — tutti gli elementi cliccabili devono avere cursor:pointer")
    lines.append("- ❌ **Hover che spostano il layout** — evita le trasformazioni di scala che spostano il layout")
    lines.append("- ❌ **Testo a basso contrasto** — mantieni un rapporto di contrasto di almeno 4.5:1")
    lines.append("- ❌ **Cambi di stato istantanei** — usa sempre le transizioni (150-300ms)")
    lines.append("- ❌ **Stati di focus invisibili** — gli stati di focus devono essere visibili per l'accessibilità")
    lines.append("")
    
    # Checklist prima della consegna
    lines.append("---")
    lines.append("")
    lines.append("## Checklist prima della consegna")
    lines.append("")
    lines.append("Prima di consegnare codice UI, verifica:")
    lines.append("")
    lines.append("- [ ] Nessuna emoji usata come icona (usa SVG)")
    lines.append("- [ ] Tutte le icone da un unico set coerente (Heroicons/Lucide)")
    lines.append("- [ ] `cursor-pointer` su tutti gli elementi cliccabili")
    lines.append("- [ ] Stati hover con transizioni morbide (150-300ms)")
    lines.append("- [ ] Light mode: contrasto del testo di almeno 4.5:1")
    lines.append("- [ ] Stati di focus visibili per la navigazione da tastiera")
    lines.append("- [ ] `prefers-reduced-motion` rispettato")
    lines.append("- [ ] Responsive: 375px, 768px, 1024px, 1440px")
    lines.append("- [ ] Nessun contenuto nascosto dietro navbar fisse")
    lines.append("- [ ] Nessuno scroll orizzontale su mobile")
    lines.append("")
    
    return "\n".join(lines)


def format_page_override_md(design_system: dict, page_name: str, page_query: str = None) -> str:
    """Formatta il file di override di una pagina, con contenuto mirato ricavato dalle ricerche."""
    project = design_system.get("project_name", "PROGETTO")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_title = page_name.replace("-", " ").replace("_", " ").title()
    
    # Riconosce il tipo di pagina e genera override mirati
    page_overrides = _generate_intelligent_overrides(page_name, page_query, design_system)
    
    lines = []
    
    lines.append(f"# Override della pagina {page_title}")
    lines.append("")
    lines.append(f"> **PROGETTO:** {project}")
    lines.append(f"> **Generato il:** {timestamp}")
    lines.append(f"> **Tipo di pagina:** {page_overrides.get('page_type', 'Generale')}")
    lines.append("")
    lines.append("> ⚠️ **IMPORTANTE:** le regole di questo file **sostituiscono** quelle del file Master (`../MASTER.md`).")
    lines.append("> Qui sono documentate solo le differenze rispetto al Master. Per tutte le altre regole vale il Master.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Regole specifiche della pagina, con contenuto reale
    lines.append("## Regole specifiche della pagina")
    lines.append("")
    
    # Override del layout
    lines.append("### Override del layout")
    lines.append("")
    layout = page_overrides.get("layout", {})
    if layout:
        for key, value in layout.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Nessun override: usa il layout del Master")
    lines.append("")
    
    # Override della spaziatura
    lines.append("### Override della spaziatura")
    lines.append("")
    spacing = page_overrides.get("spacing", {})
    if spacing:
        for key, value in spacing.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Nessun override: usa la spaziatura del Master")
    lines.append("")
    
    # Override della tipografia
    lines.append("### Override della tipografia")
    lines.append("")
    typography = page_overrides.get("typography", {})
    if typography:
        for key, value in typography.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Nessun override: usa la tipografia del Master")
    lines.append("")
    
    # Override dei colori
    lines.append("### Override dei colori")
    lines.append("")
    colors = page_overrides.get("colors", {})
    if colors:
        for key, value in colors.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Nessun override: usa i colori del Master")
    lines.append("")
    
    # Override dei componenti
    lines.append("### Override dei componenti")
    lines.append("")
    components = page_overrides.get("components", [])
    if components:
        for comp in components:
            lines.append(f"- {comp}")
    else:
        lines.append("- Nessun override: usa le specifiche dei componenti del Master")
    lines.append("")
    
    # Componenti specifici della pagina
    lines.append("---")
    lines.append("")
    lines.append("## Componenti specifici della pagina")
    lines.append("")
    unique_components = page_overrides.get("unique_components", [])
    if unique_components:
        for comp in unique_components:
            lines.append(f"- {comp}")
    else:
        lines.append("- Nessun componente specifico per questa pagina")
    lines.append("")
    
    # Raccomandazioni
    lines.append("---")
    lines.append("")
    lines.append("## Raccomandazioni")
    lines.append("")
    recommendations = page_overrides.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            lines.append(f"- {rec}")
    lines.append("")
    
    return "\n".join(lines)


def _generate_intelligent_overrides(page_name: str, page_query: str, design_system: dict) -> dict:
    """
    Genera override mirati in base al tipo di pagina, con ricerche a più livelli.
    
    Usa il motore di ricerca esistente per trovare dati pertinenti su stile, UX e layout,
    invece di tipi di pagina scritti a mano nel codice.
    """
    from core import search
    
    page_lower = page_name.lower()
    query_lower = (page_query or "").lower()
    combined_context = f"{page_lower} {query_lower}"
    
    # Cerca indicazioni per la pagina su più domini
    style_search = search(combined_context, "style", max_results=1)
    ux_search = search(combined_context, "ux", max_results=3)
    landing_search = search(combined_context, "landing", max_results=1)
    
    # Estrae i risultati dalle risposte della ricerca
    style_results = style_search.get("results", [])
    ux_results = ux_search.get("results", [])
    landing_results = landing_search.get("results", [])
    
    # Ricava il tipo di pagina dal contesto o dai risultati
    page_type = _detect_page_type(combined_context, style_results)
    
    # Costruisce gli override dai risultati della ricerca
    layout = {}
    spacing = {}
    typography = {}
    colors = {}
    components = []
    unique_components = []
    recommendations = []
    
    # Override ricavati dallo stile
    if style_results:
        style = style_results[0]
        style_name = style.get("Style Category", "")
        keywords = style.get("Keywords", "")
        best_for = style.get("Best For", "")
        effects = style.get("Effects & Animation", "")
        
        # Deduce il layout dalle parole chiave (in inglese) dello stile
        if any(kw in keywords.lower() for kw in ["data", "dense", "dashboard", "grid"]):
            layout["Larghezza massima"] = "1400px o a tutta larghezza"
            layout["Griglia"] = "12 colonne, per gestire i dati con flessibilità"
            spacing["Densità dei contenuti"] = "Alta: ottimizza per mostrare molte informazioni"
        elif any(kw in keywords.lower() for kw in ["minimal", "simple", "clean", "single"]):
            layout["Larghezza massima"] = "800px (stretta, concentrata)"
            layout["Layout"] = "Una colonna, centrata"
            spacing["Densità dei contenuti"] = "Bassa: punta sulla chiarezza"
        else:
            layout["Larghezza massima"] = "1200px (standard)"
            layout["Layout"] = "Sezioni a tutta larghezza, contenuto centrato"
        
        if effects:
            recommendations.append(f"Effetti: {effects}")
    
    # Usa le linee guida UX come raccomandazioni
    for ux in ux_results:
        category = ux.get("Category", "")
        do_text = ux.get("Do", "")
        dont_text = ux.get("Don't", "")
        if do_text:
            recommendations.append(f"{category}: {do_text}")
        if dont_text:
            components.append(f"Evita: {dont_text}")
    
    # Ricava la struttura delle sezioni dal pattern della landing page
    if landing_results:
        landing = landing_results[0]
        sections = landing.get("Section Order", "")
        cta_placement = landing.get("Primary CTA Placement", "")
        color_strategy = landing.get("Color Strategy", "")
        
        if sections:
            layout["Sezioni"] = sections
        if cta_placement:
            recommendations.append(f"Posizione della CTA: {cta_placement}")
        if color_strategy:
            colors["Strategia"] = color_strategy
    
    # Valori predefiniti se le ricerche non hanno dato risultati
    if not layout:
        layout["Larghezza massima"] = "1200px"
        layout["Layout"] = "Griglia responsive"
    
    if not recommendations:
        recommendations = [
            "Fai riferimento a MASTER.md per tutte le regole di design",
            "Aggiungi gli override specifici che servono a questa pagina"
        ]
    
    return {
        "page_type": page_type,
        "layout": layout,
        "spacing": spacing,
        "typography": typography,
        "colors": colors,
        "components": components,
        "unique_components": unique_components,
        "recommendations": recommendations
    }


def _detect_page_type(context: str, style_results: list) -> str:
    """Ricava il tipo di pagina dal contesto e dai risultati della ricerca."""
    context_lower = context.lower()
    
    # Cerca i tipi di pagina più comuni (parole chiave in inglese)
    page_patterns = [
        (["dashboard", "admin", "analytics", "data", "metrics", "stats", "monitor", "overview"], "Dashboard / Vista dati"),
        (["checkout", "payment", "cart", "purchase", "order", "billing"], "Checkout / Pagamento"),
        (["settings", "profile", "account", "preferences", "config"], "Impostazioni / Profilo"),
        (["landing", "marketing", "homepage", "hero", "home", "promo"], "Landing / Marketing"),
        (["login", "signin", "signup", "register", "auth", "password"], "Autenticazione"),
        (["pricing", "plans", "subscription", "tiers", "packages"], "Prezzi / Piani"),
        (["blog", "article", "post", "news", "content", "story"], "Blog / Articolo"),
        (["product", "item", "detail", "pdp", "shop", "store"], "Dettaglio prodotto"),
        (["search", "results", "browse", "filter", "catalog", "list"], "Risultati di ricerca"),
        (["empty", "404", "error", "not found", "zero"], "Stato vuoto"),
    ]
    
    for keywords, page_type in page_patterns:
        if any(kw in context_lower for kw in keywords):
            return page_type
    
    # Ripiego: prova a dedurlo dai risultati di stile
    if style_results:
        style_name = style_results[0].get("Style Category", "").lower()
        best_for = style_results[0].get("Best For", "").lower()
        
        if "dashboard" in best_for or "data" in best_for:
            return "Dashboard / Vista dati"
        elif "landing" in best_for or "marketing" in best_for:
            return "Landing / Marketing"
    
    return "Generale"


# ============ USO DA RIGA DI COMANDO ============
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Genera un design system (il database è in inglese: usa parole chiave in inglese)")
    parser.add_argument("query", help="query di ricerca con parole chiave in inglese (es. 'SaaS dashboard')")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="nome del progetto")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="formato di output")

    args = parser.parse_args()

    result = generate_design_system(args.query, args.project_name, args.format)
    print(result)
