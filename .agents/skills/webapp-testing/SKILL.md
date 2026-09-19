---
name: webapp-testing
description: Principi di test delle applicazioni web. E2E, Playwright, strategie di audit approfondito.
---

# Test delle web app

> Scopri e testa tutto. Nessuna route resta senza test.

## 🔧 Script da eseguire

**Eseguili per i test automatici nel browser:**

| Script | A cosa serve | Uso |
| --- | --- | --- |
| `scripts/playwright_runner.py` | Test di base nel browser | `python .agents/skills/webapp-testing/scripts/playwright_runner.py https://example.com` |
| | Con screenshot | `python .agents/skills/webapp-testing/scripts/playwright_runner.py <url> --screenshot` |
| | Controllo di accessibilità | `python .agents/skills/webapp-testing/scripts/playwright_runner.py <url> --a11y` |

**Richiede:** `pip install playwright && playwright install chromium`

L'output è un JSON (chiavi in inglese, messaggi in italiano); il codice di uscita è diverso da 0 se il controllo non va a buon fine, così `checklist.py` e `verify_all.py` non lo contano come superato.

---

## 1. Audit approfondito

### Prima la scoperta

| Obiettivo | Come trovarlo |
| --- | --- |
| Route | Scansiona `app/`, `pages/`, i file del router |
| Endpoint API | Cerca con grep i metodi HTTP |
| Componenti | Trova le cartelle dei componenti |
| Funzionalità | Leggi la documentazione |

### Test sistematico

1. **Mappa**: elenca tutte le route e le API
2. **Scansiona**: verifica che rispondano
3. **Testa**: copri i percorsi critici

---

## 2. Piramide dei test per il web

```text
        /\          E2E (pochi)
       /  \         Flussi utente critici
      /----\
     /      \       Integrazione (alcuni)
    /--------\      API, flusso dei dati
   /          \
  /------------\    Componenti (molti)
                    Singoli pezzi di UI
```

---

## 3. Principi dei test E2E

### Cosa testare

| Priorità | Test |
| --- | --- |
| 1 | Flussi utente del caso felice (happy path) |
| 2 | Flussi di autenticazione |
| 3 | Azioni di business critiche |
| 4 | Gestione degli errori |

### Buone pratiche E2E

| Pratica | Perché |
| --- | --- |
| Usa `data-testid` | Selettori stabili |
| Aspetta gli elementi | Eviti test instabili (flaky) |
| Stato pulito | Test indipendenti |
| Evita i dettagli di implementazione | Testi il comportamento dell'utente |

---

## 4. Principi di Playwright

### Concetti chiave

| Concetto | A cosa serve |
| --- | --- |
| Page Object Model | Incapsula la logica della pagina |
| Fixture | Setup dei test riutilizzabile |
| Asserzioni | Attesa automatica integrata |
| Trace Viewer | Debug dei fallimenti |

### Configurazione

| Impostazione | Consiglio |
| --- | --- |
| Retries | 2 in CI |
| Trace | `on-first-retry` |
| Screenshot | `only-on-failure` |
| Video | `retain-on-failure` |

---

## 5. Test visivi

### Quando usarli

| Scenario | Valore |
| --- | --- |
| Design system | Alto |
| Pagine di marketing | Alto |
| Libreria di componenti | Medio |
| Contenuti dinamici | Più basso |

### Strategia

- Screenshot di riferimento (baseline)
- Confronto a ogni modifica
- Revisione delle differenze visive
- Aggiornamento delle modifiche volute

---

## 6. Principi dei test delle API

### Aree da coprire

| Area | Test |
| --- | --- |
| Codici di stato | 200, 400, 404, 500 |
| Forma della risposta | Rispetta lo schema |
| Messaggi di errore | Comprensibili per l'utente |
| Casi limite | Vuoto, molto grande, caratteri speciali |

---

## 7. Organizzazione dei test

### Struttura dei file

```text
tests/
├── e2e/           # Flussi utente completi
├── integration/   # API, dati
├── component/     # Unità di UI
└── fixtures/      # Dati condivisi
```

### Convenzione per i nomi

| Schema | Esempio |
| --- | --- |
| Per funzionalità | `login.spec.ts` |
| Descrittivo | `user-can-checkout.spec.ts` |

I nomi dei file restano in inglese, come il resto del codice.

---

## 8. Integrazione con la CI

### Passi della pipeline

1. Installa le dipendenze
2. Installa i browser
3. Esegui i test
4. Carica gli artefatti (trace, screenshot)

### Parallelizzazione

| Strategia | Quando |
| --- | --- |
| Per file | Predefinita in Playwright |
| Sharding | Suite grandi |
| Worker | Più browser |

---

## 9. Anti-pattern

| ❌ Non fare | ✅ Fai |
| --- | --- |
| Testare l'implementazione | Testa il comportamento |
| Attese fisse nel codice | Usa l'attesa automatica |
| Saltare la pulizia | Isola i test |
| Ignorare i test instabili | Correggi la causa |

---

> **Ricorda:** i test E2E costano. Usali solo per i percorsi critici.
