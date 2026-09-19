---
name: orchestrate
description: 'Coordina almeno tre agenti specialisti su un compito complesso che tocca più domini: prima il piano con /plan, poi l''approvazione, poi il lavoro in parallelo e la verifica. Usala quando l''utente lancia /orchestrate o il compito attraversa più domini.'
---

# Orchestrazione di più agenti

Sei in **MODALITÀ ORCHESTRAZIONE**. Il tuo compito: coordinare agenti specializzati per risolvere questo problema complesso.

## Compito da orchestrare

La richiesta è il testo che segue `/orchestrate`.

---

## 🔴 CRITICO: minimo di agenti

> ⚠️ **ORCHESTRAZIONE = ALMENO 3 AGENTI DIVERSI**
>
> Con meno di 3 agenti NON stai orchestrando: stai solo delegando.
>
> **Controllo prima di chiudere:**
>
> - Conta gli agenti chiamati
> - Se `agent_count < 3` → FERMATI e chiamane altri
> - Un solo agente = orchestrazione FALLITA

### Scelta degli agenti

> 🔴 **OBBLIGATORIO:** la tabella completa di scelta degli agenti, gli agenti richiesti per tipo di compito e quelli disponibili sono in `@[skills/intelligent-routing]`.

---

## Controllo iniziale: modalità

| Modalità attuale | Tipo di compito | Azione |
| --- | --- | --- |
| **plan** | Qualsiasi | ✅ Procedi partendo dal piano |
| **edit** | Esecuzione semplice | ✅ Procedi direttamente |
| **edit** | Complesso / più file | ⚠️ Chiedi: "Questo compito richiede un piano. Passo alla modalità plan?" |
| **ask** | Qualsiasi | ⚠️ Chiedi: "Pronto a orchestrare. Passo alla modalità edit o plan?" |

---

## 🔴 ORCHESTRAZIONE IN 2 FASI

### FASE 1: PIANO (in sequenza, NIENTE agenti in parallelo)

| Passo | Chi | Azione |
| --- | --- | --- |
| 1 | tu, con `/plan` | Crei `docs/PLAN-{slug}.md` |
| 2 | (facoltativo) `explorer-agent` | Esplorazione del codice, se serve |

> 🔴 **NESSUN ALTRO AGENTE durante il piano!** Solo explorer-agent, per esplorare il codice.

### ⏸️ CHECKPOINT: approvazione dell'utente

```text
Quando il piano è pronto, CHIEDI:

"✅ Piano creato: docs/PLAN-{slug}.md

Lo approvi? (S/N)
- S: inizio l'implementazione
- N: rivedo il piano"
```

> 🔴 **NON passare alla Fase 2 senza l'approvazione esplicita dell'utente!**

### FASE 2: IMPLEMENTAZIONE (agenti in parallelo dopo l'approvazione)

| Gruppo in parallelo | Agenti |
| --- | --- |
| Fondamenta | `api-designer`, `backend-specialist` (schema) |
| Nucleo | `backend-specialist`, `frontend-specialist` |
| Rifinitura | `test-engineer`, `qa-automation-engineer` |

> ✅ Dopo l'approvazione dell'utente, chiama più agenti IN PARALLELO.

---

## Protocollo di orchestrazione

### Passo 1: individua i domini

Individua TUTTI i domini che il compito tocca:

```text
□ Backend/API   → backend-specialist (anche database, revisioni di sicurezza, deploy)
□ Design di API → api-designer
□ Frontend/UI   → frontend-specialist (anche prestazioni e SEO)
□ Test          → test-engineer, qa-automation-engineer (E2E)
□ AI / LLM / ML → ai-ml-engineer
□ Scroll / 3D   → scroll-experience-architect
□ LaTeX         → latex-specialist
```

### Passo 2: in che fase sei

| Se il piano esiste | Azione |
| --- | --- |
| NIENTE `docs/PLAN-{slug}.md` | → FASE 1 (solo il piano) |
| C'è `docs/PLAN-{slug}.md` + l'utente l'ha approvato | → FASE 2 (implementazione) |

### Passo 3: esegui la fase

**FASE 1 (piano):**

```text
Scrivi docs/PLAN-{slug}.md seguendo .agents/skills/plan/SKILL.md
→ FERMATI quando il piano è scritto
→ CHIEDI all'utente di approvarlo
```

**FASE 2 (implementazione, dopo l'approvazione):**

```text
Chiama gli agenti IN PARALLELO:
Usa l'agente frontend-specialist per [compito]
Usa l'agente backend-specialist per [compito]
Usa l'agente test-engineer per [compito]
```

#### 🔴 CRITICO: passare il contesto (OBBLIGATORIO)

Quando chiami QUALSIASI subagent, DEVI includere:

1. **Richiesta originale:** il testo completo di quello che ha chiesto l'utente
2. **Decisioni prese:** tutte le risposte dell'utente alle domande del Socratic Gate
3. **Lavoro precedente:** riassunto di cosa hanno fatto gli agenti prima
4. **Stato del piano:** se nel workspace ci sono file di piano, includili

**Esempio con il contesto COMPLETO:**

```text
Usa l'agente frontend-specialist per costruire il feed descritto in docs/PLAN-social-studenti.md:

**CONTESTO:**
- Richiesta dell'utente: "Un social per studenti, con dati finti"
- Decisioni: tecnologia = Vue 3, layout = widget a griglia, autenticazione = finta, design = giovane e dinamico
- Lavoro precedente: l'orchestrator ha fatto 3 domande e l'utente ha risposto a tutte
- Piano: docs/PLAN-social-studenti.md, approvato dall'utente

**COMPITO:** costruisci i componenti del feed previsti dal piano, seguendo le decisioni QUI SOPRA. NON dedurre niente dal nome della cartella.
```

> ⚠️ **VIOLAZIONE:** chiamare un subagent senza il contesto completo = il subagent farà supposizioni sbagliate!

### Passo 4: verifica (OBBLIGATORIA)

L'ULTIMO agente deve lanciare gli script di verifica adatti:

```bash
python .agents/scripts/checklist.py .
# con l'app avviata, la suite completa:
python .agents/scripts/verify_all.py . --url http://localhost:3000
```

### Passo 5: sintesi dei risultati

Unisci i risultati di tutti gli agenti in un unico report.

---

## Formato dell'output

```markdown
## 🎼 Report dell'orchestrazione

### Compito
[riassunto del compito originale]

### Modalità
[modalità attuale dell'agente di Antigravity: plan/edit/ask]

### Agenti chiamati (ALMENO 3)
| # | Agente | Ambito | Stato |
|---|--------|--------|-------|
| 1 | backend-specialist | API e dati | ✅ |
| 2 | frontend-specialist | Interfaccia | ✅ |
| 3 | test-engineer | Script di verifica | ✅ |

### Script di verifica eseguiti
- [x] checklist.py → superato/fallito
- [x] verify_all.py → superato/fallito (se c'è un URL dell'app)

### Risultati principali
1. **[Agente 1]**: risultato
2. **[Agente 2]**: risultato
3. **[Agente 3]**: risultato

### Consegne
- [ ] docs/PLAN-{slug}.md creato
- [ ] Codice implementato
- [ ] Test che passano
- [ ] Script verificati

### Riepilogo
[un paragrafo che riassume il lavoro di tutti gli agenti]
```

---

## 🔴 CONTROLLO DI USCITA

Prima di chiudere l'orchestrazione, verifica:

1. ✅ **Numero di agenti:** `invoked_agents >= 3`
2. ✅ **Script eseguiti:** almeno `checklist.py`
3. ✅ **Report generato:** report dell'orchestrazione con tutti gli agenti elencati

> **Se un controllo fallisce → NON chiudere l'orchestrazione. Chiama altri agenti o lancia gli script.**

---

**Inizia subito l'orchestrazione. Scegli 3+ agenti, esegui in sequenza, lancia gli script di verifica, sintetizza i risultati.**
