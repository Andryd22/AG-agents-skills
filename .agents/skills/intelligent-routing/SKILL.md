---
name: intelligent-routing
description: Scelta automatica dell'agente e smistamento dei compiti. Classifica ogni richiesta, sceglie gli agenti specialisti in .agents/agents/ e passa loro il lavoro con invoke_subagent, senza che l'utente debba nominarli.
metadata:
  version: "2.0.0"
---

# Routing intelligente degli agenti

**Scopo**: analizzare ogni richiesta e affidarla agli agenti specialisti giusti, senza che l'utente debba nominarli.

> **L'AI fa da project manager**: classifica la richiesta, sceglie gli specialisti e passa loro il lavoro con tutto il contesto.

## 1. Classificazione della richiesta

**Prima di QUALSIASI azione, classifica la richiesta:**

| Tipo di richiesta | Parole chiave | Livelli attivi | Risultato |
| --- | --- | --- | --- |
| **DOMANDA** | "cos'è", "come funziona", "spiegami" | Solo LIVELLO 0 | Risposta testuale |
| **ANALISI** | "analizza", "elenca i file", "panoramica" | LIVELLO 0 + explorer-agent | Resoconto in chat (nessun file) |
| **CODICE SEMPLICE** | "correggi", "aggiungi", "cambia" (un solo file) | LIVELLO 0 + LIVELLO 1 (leggero) | Modifica diretta |
| **CODICE COMPLESSO** | "costruisci", "crea", "implementa", "refactoring" | LIVELLO 0 + LIVELLO 1 (completo) + agente | **Serve `docs/PLAN-{slug}.md`** |
| **DESIGN/UI** | "design", "UI", "pagina", "dashboard" | LIVELLO 0 + LIVELLO 1 + agente | **Serve `docs/PLAN-{slug}.md`** |
| **SLASH COMMAND** | /plan, /orchestrate, /debug, ... | La skill con quel nome | Variabile |

## 2. Tabella di scelta degli agenti

**Usa questa tabella per scegliere gli agenti.** Elenca tutti gli agenti di `.agents/agents/`; tienila completa quando se ne aggiungono o se ne tolgono.

| Intento dell'utente | Parole chiave / dominio | Agenti scelti (minimo) | Automatico? |
| --- | --- | --- | --- |
| **Autenticazione** | "login", "auth", "registrazione", "password", "jwt" | `backend-specialist` + `test-engineer` | ✅ SÌ |
| **Componente UI** | "pulsante", "card", "layout", "stile" | `frontend-specialist` | ✅ SÌ |
| **App web** | "webapp", "nextjs", "react", "vue" | `frontend-specialist` + `backend-specialist` + `test-engineer` | ⚠️ PRIMA CHIEDI |
| **Design di API** | "design delle API", "OpenAPI", "contratto", "versioning" | `api-designer` | ✅ SÌ |
| **Endpoint** | "endpoint", "rotta", "POST", "GET" | `backend-specialist` + `test-engineer` | ✅ SÌ |
| **Database** | "schema", "migrazione", "query", "tabella" | `backend-specialist` | ✅ SÌ |
| **Bug** | "errore", "bug", "non funziona", "rotto" | `debugger` + `explorer-agent` + `test-engineer` | ✅ SÌ |
| **Test unitari e di integrazione** | "test", "copertura", "unit", "tdd" | `test-engineer` | ✅ SÌ |
| **E2E / QA** | "e2e", "playwright", "cypress", "regressione" | `qa-automation-engineer` | ✅ SÌ |
| **Deploy** | "deploy", "produzione", "CI/CD", "docker" | `backend-specialist` | ✅ SÌ |
| **Revisione di sicurezza** | "sicurezza", "vulnerabilità", "owasp" | `backend-specialist` (non c'è un agente per la sicurezza) | ✅ SÌ |
| **Prestazioni** | "lento", "ottimizza", "prestazioni", "velocità" | `frontend-specialist` (web) o `backend-specialist` (server) | ✅ SÌ |
| **SEO / Web Vitals** | "seo", "meta", "core web vitals", "sitemap" | `frontend-specialist` | ✅ SÌ |
| **AI / LLM** | "LLM", "RAG", "prompt", "embedding", "agente AI" | `ai-ml-engineer` | ✅ SÌ |
| **ML / data mining** | "scikit-learn", "classificazione", "clustering", "pandas", "regole di associazione", "cross-validation" | `ai-ml-engineer` (con la skill `classic-ml`) | ✅ SÌ |
| **Esperienza scroll** | "scrollytelling", "scroll 3D", "fly-through", "WebGL" | `scroll-experience-architect` | ✅ SÌ |
| **LaTeX / università** | "latex", "appunti", "dalle slide al capitolo", "tesi", "paper", "tikz" | `latex-specialist` | ✅ SÌ |
| **Documentazione** | "README", "documentazione delle API", "changelog" | `documentation-writer` | ❌ SOLO SE RICHIESTO |
| **Analisi del codice** | "analizza il repo", "spiega il codice", "mappa la struttura" | `explorer-agent` | ✅ SÌ |
| **Requisiti** | "user story", "criteri di accettazione", "specifiche", "backlog", "roadmap", "MVP", "PRD" | Nessun agente: la skill `plan` | ✅ SÌ |
| **Piano** | "piano", "pianifica", "suddividi", "lista dei task" | Nessun agente: la skill `plan` | ✅ SÌ |
| **Full stack** | "costruisci un'app", "fullstack", "piattaforma" | `orchestrator` (piano con `/plan`, poi `frontend-specialist` + `backend-specialist`) | ⚠️ PRIMA CHIEDI |
| **Nuova funzionalità** | "costruisci", "crea", "implementa", "nuova app" | `orchestrator` → più agenti | ⚠️ PRIMA CHIEDI |
| **Compito complesso** | Più domini riconosciuti | `orchestrator` → più agenti | ⚠️ PRIMA CHIEDI |

**Regola dei più domini:** se la richiesta corrisponde a 2 o più domini di righe diverse (es. "login sicuro con UI in dark mode" = backend + frontend), affidala all'`orchestrator`, che prima pianifica e poi coordina gli specialisti.

## 3. Passare il lavoro

- **Nativo (app e CLI di Antigravity):** chiama `invoke_subagent` con il nome dell'agente. Il subagent parte con un contesto pulito, quindi il prompt deve contenere la richiesta completa dell'utente, le decisioni già prese (risposte al Socratic Gate), i file che servono e, se esiste, il piano in `docs/PLAN-{slug}.md`.
- **Ripiego (senza custom agent, es. l'IDE di Antigravity finché non li supporta):** leggi `.agents/agents/<nome>.md` e lo `SKILL.md` di ogni skill nominata nella sua riga "Le tue skill", poi rispondi applicandoli.
- **Domande e modifiche banali** non hanno bisogno di un agente: rispondi direttamente.

## 4. Complessità

| Livello | Segnali | Azione |
| --- | --- | --- |
| **SEMPLICE** | Un file, un dominio, compito chiaro ("sistema lo stile del pulsante di login") | Un agente |
| **MEDIA** | 2-3 file, 2 domini, requisiti chiari ("aggiungi un endpoint per il profilo") | Gli agenti coinvolti, uno dopo l'altro |
| **COMPLESSA** | Molti file o domini, scelte di architettura, requisiti poco chiari ("costruisci un social") | `orchestrator`, che prima fa le domande del Socratic Gate |

## 5. Regole

1. **Analisi silenziosa:** non annunciare "Sto analizzando la tua richiesta...".
2. **Di' quali agenti e skill usi**, nella prima riga della risposta, come stabilito in "Annuncia agenti e skill" in `rules/GEMINI.md`:

   ```text
   🤖 @backend-specialist + @test-engineer · 📚 api-patterns, test
   ```

   Prima di passare il lavoro scrivi `↪ @<agente>: <compito>`, quando torna `↩ @<agente>`.

3. **Precedenza:** una menzione esplicita vince ("Usa @backend-specialist per rivedere questo").
4. **Prima il Socratic Gate:** il routing non salta mai le domande di GEMINI.md quando non è chiaro qualcosa che cambia il risultato.
5. **Priorità:** regole di GEMINI.md > intelligent-routing.

## 6. Casi limite

| Caso | Esempio | Azione |
| --- | --- | --- |
| Domanda generica | "Come funziona React?" | Nessun agente, rispondi direttamente |
| Molto vaga | "Miglioralo" | Chiedi cosa migliorare, poi scegli l'agente |
| Contraddittoria | "Aggiungi il supporto mobile alla web app" | Chiedi: web responsive (`frontend-specialist`) o app nativa (il kit non la copre)? Poi scegli l'agente |
