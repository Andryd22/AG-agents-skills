# Antigravity Kit — Architecture Refinement (v3)

**Date:** 2026-05-09
**Scope:** Fase 1 — Architettura (Layer-by-Layer, step 1 di 3)

## Obiettivo

Rafforzare le fondamenta architetturali del kit `.agent/` eliminando ridondanze, consolidando il routing, e standardizzando agenti/skill prima di procedere a miglioramenti di qualità (Fase 2) ed espansione (Fase 3).

## Modifiche

### 1. `intelligent-routing/SKILL.md` — Diventa fonte unica di routing

Unificare in un solo file:
- Request Classifier (attualmente in GEMINI.md)
- Domain Detection Rules (già presente)
- Agent Selection Matrix (unificando GEMINI.md + orchestrate.md + orchestrator.md)
- Complexity Assessment (già presente)
- Auto-Selection Protocol (già presente)
- Response Format (già presente)

Risultato: un file, una matrice, zero divergenze.

### 2. `GEMINI.md` — Sfoltire da 273 a ~90 righe

**Rimosso:**
- Request Classifier → delegato a intelligent-routing
- Intelligent Agent Routing + checklist → delegato a intelligent-routing
- Tabella 12 script → ogni agente sa quali script invocare
- Project Type Routing → presente in orchestrate.md / orchestrator.md

**Mantenuto:**
- Modular Skill Loading Protocol (P0)
- Tier 0 universale: lingua, clean-code, file dependency, read-understand-apply
- Socratic Gate (essenziale)
- Final Checklist Protocol con comandi
- Quick Reference (puntatori, non duplicati)

**Aggiunto:**
- Regola esplicita: `intelligent-routing` è **always_on**, deve eseguire prima di ogni risposta.
- Riferimento esplicito a `@[skills/intelligent-routing]` per routing.

### 3. `workflows/orchestrate.md` + `agents/orchestrator.md` — Rimuovere duplicati

Entrambi i file duplicano la matrice di selezione agenti.

**Rimosso da entrambi:**
- Agent Selection Matrix
- Available Agents table (quando duplicata)

**Aggiunto:**
- Riferimento a `@[skills/intelligent-routing]` per la selezione agenti

### 4. `verify_all.py` — Lasciare riferimenti a script futuri

`dependency_analyzer.py` e `bundle_analyzer.py` referenziati ma non ancora creati.
Nessuna modifica: rimangono come placeholder per sviluppo futuro.

### 5. 20 Agenti — Standardizzazione frontmatter

Per ogni file in `.agent/agents/`:
- Verificare che ogni skill in `skills:` esista come cartella con `SKILL.md`
- Rimuovere riferimenti a skill rinominate (es. `react-best-practices` → `nextjs-react-expert`)
- Uniformare i campi frontmatter: `name`, `description`, `tools`, `model`, `skills`

### 6. Nuovo file `tasks/lessons.md`

Template vuoto per catturare pattern post-correzione:
```markdown
# Lessons Learned

## Patterns da evitare
-

## Patterns da ripetere
-

## Decisioni architetturali
-
```

## Non incluso in questa fase

- Creazione script mancanti (Fase 3 — Espansione)
- Miglioramento qualità prompt agenti (Fase 2 — Qualità)
- Nuovi agenti/skill (Fase 3 — Espansione)
- Modifiche alla web app Next.js

## Ordine di esecuzione

1. `intelligent-routing/SKILL.md`
2. `GEMINI.md`
3. `workflows/orchestrate.md` + `agents/orchestrator.md`
4. Standardizzazione 20 agenti
5. `tasks/lessons.md`
