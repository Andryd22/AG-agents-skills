# Domande costruite sul caso

> **PRINCIPIO:** le domande non servono a raccogliere dati: servono a **far emergere le conseguenze sull'architettura**.
>
> Ogni domanda deve essere legata a una decisione concreta di implementazione che incide su costi, complessità o tempi.

---

## 🧠 Principi

### 1. Le domande rivelano conseguenze

Una buona domanda non è "Che colore vuoi?", ma:

```markdown
❌ MALE: "Quale metodo di autenticazione?"
✅ BENE: "Gli utenti si registrano con email e password o con login social?

   Impatto:
   - Email/password → servono reset della password, hashing, infrastruttura 2FA
   - Social → provider OAuth, mappatura del profilo utente, meno controllo

   Compromesso: sicurezza contro tempo di sviluppo contro attrito per l'utente"
```

### 2. Prima il contesto

Prima capisci **dove** si colloca la richiesta:

| Contesto | Su cosa puntano le domande |
| --- | --- |
| **Progetto nuovo** | Decisioni di base: stack, hosting, scala |
| **Nuova funzionalità** | Punti di integrazione, schemi esistenti, modifiche che rompono qualcosa |
| **Refactoring** | Perché? Prestazioni? Manutenibilità? Cosa non va? |
| **Debug** | Sintomi → causa radice → come riprodurlo |

### 3. Il minimo di domande

**PRINCIPIO:** ogni domanda deve eliminare un bivio nella strada dell'implementazione.

```text
Prima della domanda:
├── Strada A: fai X (5 min)
├── Strada B: fai Y (15 min)
└── Strada C: fai Z (1 ora)

Dopo la domanda:
└── Strada confermata: fai X (5 min)
```

Se una domanda non riduce le strade possibili → **TOGLILA**.

### 4. Le domande producono dati, non supposizioni

```markdown
❌ SUPPOSIZIONE: "Probabilmente l'utente vuole Stripe per i pagamenti"
✅ DOMANDA: "Quale provider di pagamento fa per te?

   Stripe → documentazione migliore, 2,9% + 0,30 $, pensato per gli USA
   LemonSqueezy → Merchant of Record, 5% + 0,50 $, gestisce le tasse ovunque
   Paddle → prezzi complessi, gestisce l'IVA UE, orientato alle aziende"
```

---

## 📋 Algoritmo per generare le domande

```text
INPUT: richiesta dell'utente + contesto (nuovo/funzionalità/refactoring/debug)
│
├── PASSO 1: analizza la richiesta
│   ├── Ricava il dominio (e-commerce, auth, realtime, cms, ...)
│   ├── Ricava le funzionalità (esplicite e implicite)
│   └── Ricava gli indizi sulla scala (utenti, volume di dati, frequenza)
│
├── PASSO 2: trova i punti di decisione
│   ├── Cosa VA deciso prima di scrivere codice? (bloccante)
│   ├── Cosa si PUÒ decidere dopo? (rimandabile)
│   └── Cosa ha impatto sull'ARCHITETTURA? (grande effetto)
│
├── PASSO 3: genera le domande (in ordine di priorità)
│   ├── P0: decisioni bloccanti (senza risposta non si procede)
│   ├── P1: grande effetto (tocca >30% dell'implementazione)
│   ├── P2: effetto medio (tocca funzionalità specifiche)
│   └── P3: facoltative (casi limite, ottimizzazione)
│
└── PASSO 4: formatta ogni domanda
    ├── Cosa: domanda chiara
    ├── Perché: impatto sull'implementazione
    ├── Opzioni: compromessi (non solo A contro B)
    └── Predefinito: cosa succede se l'utente non risponde
```

---

## 🎯 Banche di domande per dominio

### E-commerce

| Domanda | Perché conta | Compromessi |
| --- | --- | --- |
| **Un solo venditore o più venditori?** | Più venditori → logica delle commissioni, dashboard dei venditori, pagamenti divisi | +ricavi, -complessità |
| **Gestione del magazzino?** | Servono tabelle delle scorte, logica di prenotazione, avvisi di scorta bassa | +precisione, -tempo di sviluppo |
| **Prodotti digitali o fisici?** | Digitali → link di download, niente spedizione | Fisici → API di spedizione, tracciamento |
| **Abbonamento o acquisto singolo?** | Abbonamento → addebiti ricorrenti, solleciti, pro rata | +ricavi, -complessità |

### Autenticazione

| Domanda | Perché conta | Compromessi |
| --- | --- | --- |
| **Serve il login social?** | Provider OAuth contro infrastruttura per il reset della password | +UX, -controllo |
| **Permessi per ruolo?** | Tabelle RBAC, applicazione delle policy, UI di amministrazione | +sicurezza, -tempo di sviluppo |
| **Serve la 2FA?** | Infrastruttura TOTP/SMS, codici di backup, procedura di recupero | +sicurezza, -attrito nella UX |
| **Verifica dell'email?** | Token di verifica, servizio email, logica di reinvio | +sicurezza, -attrito in registrazione |

### Tempo reale

| Domanda | Perché conta | Compromessi |
| --- | --- | --- |
| **WebSocket o polling?** | WS → scalare il server, gestire le connessioni | Polling → più semplice, più latenza |
| **Utenti contemporanei previsti?** | <100 → un server, >1000 → Redis pub/sub, >10k → infrastruttura dedicata | +scala, -complessità |
| **Messaggi da conservare?** | Tabelle dello storico, costi di storage, paginazione | +UX, -spazio |
| **Effimeri o persistenti?** | Effimeri → in memoria, persistenti → scrittura su database prima dell'invio | +affidabilità, -latenza |

### Contenuti/CMS

| Domanda | Perché conta | Compromessi |
| --- | --- | --- |
| **Rich text o Markdown?** | Rich text → sanificazione, rischi XSS | Markdown → semplice, niente WYSIWYG |
| **Flusso bozza/pubblicazione?** | Campo di stato, job programmati, versioni | +controllo, -complessità |
| **Gestione dei media?** | Endpoint di upload, storage, ottimizzazione | +funzionalità, -tempo di sviluppo |
| **Più lingue?** | Tabelle i18n, UI di traduzione, logica di ripiego | +pubblico, -complessità |

---

## 📐 Modello di domande

```markdown
In base alla tua richiesta di [DOMINIO] [FUNZIONALITÀ]:

## 🔴 CRITICHE (decisioni bloccanti)

### 1. **[PUNTO DI DECISIONE]**

**Domanda:** [domanda chiara e precisa]

**Perché conta:**
- [conseguenza sull'architettura]
- [incide su: costo / complessità / tempi / scala]

**Opzioni:**
| Opzione | Pro | Contro | Ideale per |
|---------|-----|--------|------------|
| A | [vantaggio] | [svantaggio] | [caso d'uso] |
| B | [vantaggio] | [svantaggio] | [caso d'uso] |

**Se non specificato:** [scelta predefinita + motivo]

---

## 🟡 GRANDE EFFETTO (cambiano l'implementazione)

### 2. **[PUNTO DI DECISIONE]**
[stesso formato]

---

## 🟢 FACOLTATIVE (casi limite)

### 3. **[PUNTO DI DECISIONE]**
[stesso formato]
```

---

## 🔄 Domande per giri successivi

### Primo giro (1-3 domande)

Punta sulle **decisioni bloccanti**, come vuole il Socratic Gate di `GEMINI.md`. Senza risposte non si procede.

### Secondo giro (dopo la prima implementazione)

Quando emergono gli schemi, chiedi:

- "Questa funzionalità implica [X]. Gestiamo adesso [caso limite] o lo rimandiamo?"
- "Stiamo usando [schema A]. [Funzionalità B] deve seguire lo stesso schema?"

### Terzo giro (ottimizzazione)

Quando tutto funziona:

- "Collo di bottiglia su [X]. Ottimizziamo ora o per adesso va bene così?"
- "Facciamo refactoring di [Y] per la manutenibilità o lo rilasciamo così?"

---

## 🎭 Esempio completo

```text
RICHIESTA: "Costruisci un clone di Instagram"

PASSO 1: analisi
├── Dominio: social media
├── Funzionalità: condivisione di foto, interazioni (like/commenti), profili utente
├── Implicite: feed, follower, autenticazione
└── Scala: potenzialmente alta (le app social diventano virali)

PASSO 2: punti di decisione
├── Bloccanti: strategia di storage, metodo di autenticazione, tipo di feed
├── Grande effetto: notifiche in tempo reale, complessità del modello dati
└── Rimandabili: analytics, ricerca avanzata, reel/video

PASSO 3: domande (per priorità)

P0 (bloccanti):
1. Strategia di storage → incide su architettura, costi, velocità
2. Algoritmo del feed → incide sulle query al database, complessità
3. Metodo di autenticazione → incide su tempi, UX, sicurezza

P1 (grande effetto):
4. Notifiche in tempo reale → WebSocket o polling
5. Elaborazione dei media → ottimizzazione lato client o lato server

P2 (rimandabili):
6. Storie/reel → grosso allargamento del perimetro, rimandare alla v2
7. Messaggi diretti → sottosistema a parte, rimandare alla v2

PASSO 4: formatta l'output
```

---

## 📊 Output generato (esempio)

```text
In base alla tua richiesta di un clone di Instagram:

## 🔴 DECISIONI CRITICHE (senza risposta non si procede)

### 1. **Dove salvare le foto**

**Domanda:** dove vengono salvate e servite le foto degli utenti?

**Perché conta:**
- Incide su: costi mensili di hosting, velocità di caricamento, complessità della CDN
- App social ad alto volume: 1000 utenti × 10 foto × 2 MB = 20 GB di spazio

**Opzioni:**
| Opzione | Costo | Velocità | Complessità | Ideale per |
|---------|-------|----------|-------------|------------|
| **Cloudinary** | 89 $/mese (25 GB) | Veloce (CDN) | Bassa | MVP, lancio rapido |
| **AWS S3 + CloudFront** | 0,023 $/GB | Veloce (CDN) | Media | Produzione, costi ottimizzati |
| **Supabase Storage** | Gratis fino a 1 GB | Media | Bassa | Piccola scala, semplice |
| **Disco locale** | Costo del server | Lenta | Bassa | Solo sviluppo |

**Se non specificato:** Cloudinary (equilibrato per un MVP)

---

### 2. **Algoritmo del feed**

**Domanda:** come funziona il feed principale?

**Perché conta:**
- Incide su: complessità delle query, strategia di cache, tempi di sviluppo
- I feed algoritmici richiedono infrastruttura ML e segnali di ranking

**Opzioni:**
| Opzione | Complessità | Impatto sul database | Ideale per |
|---------|-------------|----------------------|------------|
| **Cronologico** | Bassa | Query semplice | Fase iniziale, trasparenza |
| **Solo chi segui** | Media | JOIN con paginazione | La maggior parte dei social |
| **Algoritmico** | Alta | Tabelle di feed precalcolate | Concorrente di Instagram |

**Se non specificato:** solo chi segui (equilibrato per un social)

---

### 3. **Autenticazione**

**Domanda:** come si registrano e accedono gli utenti?

**Perché conta:**
- Incide su: tempo di sviluppo (2-5 ore), sicurezza, attrito nella UX

**Opzioni:**
| Opzione | Tempo | Sicurezza | UX | Ideale per |
|---------|-------|-----------|-----|------------|
| **Email/password** | 4-5 ore | Alta (con 2FA) | Media | Serve pieno controllo |
| **Solo social** | 1-2 ore | Dipende dal provider | Fluida | B2C, lancio rapido |
| **Magic link** | 2-3 ore | Media | Molto fluida | Attenzione alla sicurezza |
| **Clerk/Auth0** | 1 ora | Alta | Fluida | Arrivare prima sul mercato |

**Se non specificato:** Clerk (il più rapido per un MVP)

---

## 🟡 GRANDE EFFETTO (cambiano l'architettura)

### 4. **Notifiche in tempo reale**

**Domanda:** gli utenti devono ricevere subito le notifiche di like e commenti?

**Perché conta:**
- WebSocket aggiunge complessità all'infrastruttura (Redis pub/sub per scalare)
- Il polling è più semplice ma ha più latenza

**Opzioni:**
| Opzione | Complessità | Costo per scalare | Ideale per |
|---------|-------------|-------------------|------------|
| **WebSocket + Redis** | Alta | 10+ $/mese | >1000 utenti contemporanei |
| **Polling (30 s)** | Bassa | Query al DB | <1000 utenti |
| **Niente tempo reale** | Nessuna | Nessuno | MVP, prima validare |

**Se non specificato:** polling per l'MVP (WebSocket dopo la validazione)

---

## 🟢 FACOLTATIVE (rimandare alla v2)

### 5. **Video/reel**
- Grande complessità (elaborazione video, infrastruttura di streaming)
- Raccomandazione: lanciare solo con le foto, aggiungere i video dopo la validazione

### 6. **Messaggi diretti**
- Sottosistema a parte (l'infrastruttura di chat è diversa da quella del feed)
- Raccomandazione: Pusher/Stream per il tempo reale, oppure rimandare del tutto

---

## 📋 Riepilogo

| Decisione | Raccomandazione | Se cambia |
|-----------|-----------------|-----------|
| Storage | Cloudinary | +3 ore di configurazione |
| Feed | Solo chi segui | +2 ore di ottimizzazione delle query |
| Autenticazione | Clerk | -3 ore di sviluppo |
| Tempo reale | Polling | +5 ore per WebSocket |
| Video | Rimandato alla v2 | - |
| Messaggi | Rimandati alla v2 | - |

**Tempo stimato per l'MVP:** 15-20 ore con le raccomandazioni qui sopra
```

---

## 🎯 Riepilogo dei principi

1. **Ogni domanda = una decisione di architettura** → non raccolta di dati
2. **Mostra i compromessi** → l'utente capisce le conseguenze
3. **Prima le decisioni bloccanti** → senza, non si procede
4. **Dai un predefinito** → se l'utente non risponde, si va avanti lo stesso
5. **Attento al dominio** → le domande di un e-commerce ≠ autenticazione ≠ tempo reale
6. **Per giri successivi** → nuove domande quando emergono gli schemi durante l'implementazione
