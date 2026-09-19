---
name: parallel-agents
description: Schemi per coordinare più agenti. Usala quando più compiti indipendenti possono andare avanti con competenze di dominio diverse, o quando un'analisi completa richiede più punti di vista.
---

# Agenti in parallelo nativi

> Orchestrazione con lo strumento `invoke_subagent` di Antigravity

## Panoramica

Questa skill coordina gli agenti specialisti del kit, che sono custom agent di Antigravity in `.agents/agents/`, con `invoke_subagent`. Ogni subagent parte con un contesto pulito (non vede questa conversazione), ha gli strumenti del suo frontmatter, legge le skill nominate nel suo corpo e restituisce il risultato a chi l'ha chiamato. Dove i custom agent non ci sono (l'IDE di Antigravity finché non li supporta), leggi `.agents/agents/<nome>.md` e applicalo tu, un dominio alla volta.

## Quando orchestrare

✅ **Va bene per:**

- Compiti complessi che richiedono più domini di competenza
- Analisi del codice dal punto di vista di sicurezza, prestazioni e qualità
- Revisioni complete (architettura + sicurezza + test)
- Funzionalità che richiedono lavoro su backend + frontend + database

❌ **Non serve per:**

- Compiti semplici, di un solo dominio
- Correzioni veloci o piccole modifiche
- Compiti per cui basta un agente

---

## Chiamare gli agenti

### Un agente

```text
Usa l'agente backend-specialist per cercare vulnerabilità nell'autenticazione
```

### Catena in sequenza

```text
Prima usa explorer-agent per scoprire la struttura del progetto.
Poi usa backend-specialist per rivedere gli endpoint delle API.
Infine usa test-engineer per individuare i test mancanti.
```

### Passando il contesto

```text
Usa frontend-specialist per analizzare i componenti React.
In base a quello che trova, fai generare a test-engineer i test dei componenti.
```

### Continuare un lavoro

```text
Manda un altro messaggio allo stesso subagent: tiene il suo contesto e riparte quando riceve il messaggio.
```

---

## Schemi di orchestrazione

### Schema 1: analisi completa

```text
Agenti: explorer-agent → [agenti di dominio] → sintesi

1. explorer-agent: mappa la struttura del codice
2. backend-specialist: qualità delle API e sicurezza
3. frontend-specialist: schemi UI/UX
4. test-engineer: copertura dei test
5. Sintesi di tutti i risultati
```

### Schema 2: revisione di una funzionalità

```text
Agenti: agenti dei domini coinvolti → test-engineer

1. Individua i domini coinvolti (backend? frontend? entrambi?)
2. Chiama gli agenti di quei domini
3. test-engineer verifica le modifiche
4. Sintesi delle raccomandazioni
```

### Schema 3: revisione di sicurezza

```text
Agenti: explorer-agent → backend-specialist → sintesi

1. explorer-agent: mappa autenticazione, segreti, configurazione e file di deploy
2. backend-specialist: autenticazione, validazione degli input, accesso ai dati, segreti e superficie di deploy
3. Sintesi con le correzioni in ordine di priorità
```

---

## Agenti disponibili

L'elenco completo degli agenti, con i loro domini e le parole chiave, sta in `@[skills/intelligent-routing]` (sezione "Tabella di scelta degli agenti"). Usa quella tabella invece di tenerne una seconda copia qui.

Antigravity ha anche dei subagent integrati (`research` per esplorare il codice, `browser` per i test sul web): usali per le ricerche veloci e gli agenti del kit per le competenze di dominio.

---

## Sintesi finale

Quando tutti gli agenti hanno finito, fai la sintesi:

```markdown
## Sintesi dell'orchestrazione

### Riepilogo del compito
[cosa è stato fatto]

### Contributi degli agenti
| Agente | Risultato |
|--------|-----------|
| backend-specialist | Ha trovato X |
| test-engineer | Ha individuato Y |

### Raccomandazioni unificate
1. **Critico**: [problema dall'agente A]
2. **Importante**: [problema dall'agente B]
3. **Facoltativo**: [miglioramento dall'agente C]

### Azioni
- [ ] Correggere il problema di sicurezza critico
- [ ] Rifare l'endpoint dell'API
- [ ] Aggiungere i test mancanti
```

---

## Buone pratiche

1. **Agenti disponibili** - si può orchestrare ogni agente elencato in `@[skills/intelligent-routing]`
2. **Ordine logico** - scoperta → analisi → implementazione → test
3. **Condividi il contesto** - passa agli agenti successivi i risultati che servono
4. **Una sola sintesi** - un report unico, non output separati
5. **Verifica le modifiche** - con modifiche al codice includi sempre test-engineer

---

## Vantaggi

- ✅ **Contesti puliti** - ogni agente vede solo il prompt che gli passi, quindi passagli tutto il contesto
- ✅ **Guidato dall'AI** - il modello orchestra da solo
- ✅ **Integrazione nativa** - funziona insieme ai subagent integrati di Antigravity
- ✅ **Messaggi successivi** - un subagent può ricevere altri messaggi e continuare il lavoro
- ✅ **Passaggio del contesto** - i risultati passano da un agente all'altro
