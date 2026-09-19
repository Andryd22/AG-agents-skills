---
name: nodejs-best-practices
description: Principi di sviluppo in Node.js e come decidere. Scelta del framework, schemi asincroni, sicurezza e architettura. Insegna a ragionare, non a copiare.
---

# Buone pratiche per Node.js

> Principi e decisioni per lo sviluppo in Node.js.
> **Impara a RAGIONARE, non a memorizzare codice.**

---

## ⚠️ Come usare questa skill

Questa skill insegna **principi per decidere**, non codice fisso da copiare.

- CHIEDI all'utente le sue preferenze quando non sono chiare
- Scegli framework e schemi in base al CONTESTO
- Non ripetere ogni volta la stessa soluzione

---

## 1. Scelta del framework

### Albero di decisione

```text
Cosa stai costruendo?
│
├── Edge/serverless (Cloudflare, Vercel)
│   └── Hono (nessuna dipendenza, avvio a freddo velocissimo)
│
├── API ad alte prestazioni
│   └── Fastify (2-3 volte più veloce di Express)
│
├── Azienda / il team lo conosce già
│   └── NestJS (strutturato, dependency injection, decoratori)
│
├── Codice esistente / stabilità / ecosistema più ampio
│   └── Express (maturo, più middleware di tutti)
│
└── Full-stack con il frontend
    └── Route API di Next.js o tRPC
```

### Confronto

| Fattore | Hono | Fastify | Express |
| --- | --- | --- | --- |
| **Ideale per** | Edge, serverless | Prestazioni | Codice esistente, imparare |
| **Avvio a freddo** | Il più veloce | Veloce | Medio |
| **Ecosistema** | In crescita | Buono | Il più ampio |
| **TypeScript** | Nativo | Ottimo | Buono |
| **Curva di apprendimento** | Bassa | Media | Bassa |

### Domande per scegliere

1. Dove verrà eseguito?
2. Il tempo di avvio a freddo è critico?
3. Il team ha già esperienza con qualcosa?
4. C'è codice esistente da mantenere?

---

## 2. Il runtime

### TypeScript nativo

```text
Node.js 22.18+ / 23.6+: type stripping attivo di default (prima serviva --experimental-strip-types)
├── Esegue direttamente i file .ts
├── Nessun passo di build per i progetti semplici
├── Solo sintassi che si può togliere: niente enum, namespace, parameter property
└── Da valutare per: script, API semplici
```

### Sistema di moduli

```text
ESM (import/export)
├── Lo standard moderno
├── Tree-shaking migliore
├── Caricamento asincrono dei moduli
└── Per: i progetti nuovi

CommonJS (require)
├── Compatibilità con il codice vecchio
├── Supportato da più pacchetti npm
└── Per: codebase esistenti, alcuni casi limite
```

### Scelta del runtime

| Runtime | Ideale per |
| --- | --- |
| **Node.js** | Uso generale, l'ecosistema più ampio |
| **Bun** | Prestazioni, bundler integrato |
| **Deno** | Sicurezza prima di tutto, TypeScript integrato |

---

## 3. Principi di architettura

### Struttura a livelli

```text
Percorso di una richiesta:
│
├── Livello controller/route
│   ├── Gestisce i dettagli HTTP
│   ├── Valida l'input al confine
│   └── Chiama il livello dei servizi
│
├── Livello dei servizi
│   ├── Logica di business
│   ├── Indipendente dal framework
│   └── Chiama il livello repository
│
└── Livello repository
    ├── Solo accesso ai dati
    ├── Query al database
    └── Interazioni con l'ORM
```

### Perché conta

- **Testabilità**: i livelli si simulano uno per uno
- **Flessibilità**: cambi database senza toccare la logica di business
- **Chiarezza**: ogni livello ha una sola responsabilità

### Quando semplificare

- Script piccoli → va bene un solo file
- Prototipi → accettabile meno struttura
- Chiediti sempre: "Crescerà?"

---

## 4. Gestione degli errori

### Gestione centralizzata

```text
Schema:
├── Crea classi di errore personalizzate
├── Lanciale da qualsiasi livello
├── Catturale al livello più alto (middleware)
└── Rispondi sempre nello stesso formato
```

### Cosa esce e cosa resta nei log

```text
Al client:
├── Lo stato HTTP giusto
├── Un codice di errore per la gestione nel codice
├── Un messaggio comprensibile
└── NESSUN dettaglio interno (sicurezza!)

Nei log:
├── Lo stack trace completo
├── Il contesto della richiesta
├── L'ID dell'utente (se c'è)
└── Il timestamp
```

### Scelta del codice di stato

| Situazione | Stato | Quando |
| --- | --- | --- |
| Input errato | 400 | Il client ha mandato dati non validi |
| Non autenticato | 401 | Credenziali mancanti o non valide |
| Senza permesso | 403 | Autenticato, ma non autorizzato |
| Non trovato | 404 | La risorsa non esiste |
| Conflitto | 409 | Duplicato o conflitto di stato |
| Validazione | 422 | Schema valido ma regole di business violate |
| Errore del server | 500 | Colpa nostra, registra tutto nei log |

---

## 5. Schemi asincroni

### Quando usare cosa

| Schema | Quando |
| --- | --- |
| `async/await` | Operazioni asincrone in sequenza |
| `Promise.all` | Operazioni indipendenti in parallelo |
| `Promise.allSettled` | In parallelo, quando alcune possono fallire |
| `Promise.race` | Timeout, o vince la prima risposta |

### L'event loop

```text
Legate all'I/O (l'async aiuta):
├── Query al database
├── Richieste HTTP
├── File system
└── Operazioni di rete

Legate alla CPU (l'async non aiuta):
├── Crittografia
├── Elaborazione di immagini
├── Calcoli complessi
└── → Usa i worker thread o sposta il lavoro altrove
```

### Non bloccare l'event loop

- Mai metodi sincroni in produzione (fs.readFileSync e simili)
- Sposta altrove il lavoro pesante per la CPU
- Usa gli stream per i dati grandi

---

## 6. Validazione

### Valida ai confini

```text
Dove validare:
├── All'ingresso dell'API (corpo e parametri della richiesta)
├── Prima delle operazioni sul database
├── Sui dati esterni (risposte di API, file caricati)
└── Sulle variabili d'ambiente (all'avvio)
```

### Scelta della libreria

| Libreria | Ideale per |
| --- | --- |
| **Zod** | TypeScript prima di tutto, inferenza dei tipi |
| **Valibot** | Bundle più piccolo (tree-shakeable) |
| **ArkType** | Prestazioni critiche |
| **Yup** | Già usata nei form React |

### Filosofia

- Fallisci subito: valida presto
- Sii preciso: messaggi di errore chiari
- Non fidarti: nemmeno dei dati "interni"

---

## 7. Sicurezza

### Checklist di sicurezza (non codice)

- [ ] **Validazione degli input**: tutti gli input validati
- [ ] **Query parametrizzate**: niente concatenazione di stringhe per l'SQL
- [ ] **Hash delle password**: bcrypt o argon2
- [ ] **Verifica dei JWT**: sempre firma e scadenza
- [ ] **Rate limiting**: protezione dagli abusi
- [ ] **Header di sicurezza**: Helmet.js o equivalente
- [ ] **HTTPS**: ovunque in produzione
- [ ] **CORS**: configurato bene
- [ ] **Segreti**: solo nelle variabili d'ambiente
- [ ] **Dipendenze**: controllate regolarmente

### Mentalità

```text
Non fidarti di niente:
├── Parametri della query → valida
├── Corpo della richiesta → valida
├── Header → verifica
├── Cookie → valida
├── File caricati → controlla
└── API esterne → valida la risposta
```

---

## 8. Test

### Strategia

| Tipo | Scopo | Strumenti |
| --- | --- | --- |
| **Unitari** | Logica di business | node:test, Vitest |
| **Integrazione** | Endpoint delle API | Supertest |
| **E2E** | Flussi completi | Playwright |

### Cosa testare (priorità)

1. **Percorsi critici**: autenticazione, pagamenti, nucleo del business
2. **Casi limite**: input vuoti, valori al limite
3. **Gestione degli errori**: cosa succede quando qualcosa fallisce?
4. **Non vale la pena**: codice del framework, getter banali

### Test runner integrato (Node.js 22+)

```bash
node --test src/**/*.test.ts
├── Nessuna dipendenza esterna
├── Report di copertura
└── Modalità watch disponibile
```

---

## 9. Anti-pattern da evitare

### ❌ NON

- Usare Express per i progetti nuovi sull'edge (usa Hono)
- Usare metodi sincroni nel codice di produzione
- Mettere la logica di business nei controller
- Saltare la validazione degli input
- Scrivere i segreti nel codice
- Fidarsi dei dati esterni senza validarli
- Bloccare l'event loop con lavoro per la CPU

### ✅ SÌ

- Scegliere il framework in base al contesto
- Chiedere all'utente le preferenze quando non sono chiare
- Usare un'architettura a livelli per i progetti che crescono
- Validare tutti gli input
- Usare variabili d'ambiente per i segreti
- Profilare prima di ottimizzare

---

## 10. Checklist di decisione

Prima di implementare:

- [ ] **Hai chiesto all'utente le preferenze sullo stack?**
- [ ] **Hai scelto il framework per QUESTO contesto?** (non per abitudine)
- [ ] **Hai considerato dove verrà eseguito?**
- [ ] **Hai pianificato la gestione degli errori?**
- [ ] **Hai individuato i punti di validazione?**
- [ ] **Hai considerato i requisiti di sicurezza?**

---

> **Ricorda**: le buone pratiche di Node.js riguardano il modo di decidere, non schemi da memorizzare. Ogni progetto merita una valutazione nuova, in base ai suoi requisiti.
