# Alberi decisionali e template per contesto

> Pensiero di design basato sul contesto, non soluzioni fisse.
> **Sono GUIDE per decidere, non template da copiare e incollare.**
> **Per i principi di psicologia UX (Hick, Fitts, ecc.) vedi:** [ux-psychology.md](ux-psychology.md)

---

## ⚠️ Come usare questo file

Questo file ti aiuta a DECIDERE, non a copiare.

- Alberi decisionali → ti aiutano a RAGIONARE sulle opzioni
- Template → mostrano STRUTTURA e PRINCIPI, non valori esatti
- **Chiedi sempre le preferenze dell'utente** prima di applicarli
- **Genera palette nuove** in base al contesto, non copiare i codici hex
- **Applica le leggi UX** di ux-psychology.md per convalidare le scelte

---

## 1. Albero decisionale principale

```text
┌─────────────────────────────────────────────────────────────┐
│                    COSA STAI COSTRUENDO?                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   E-COMMERCE            SaaS/APP              CONTENUTI
   - Pagine prodotto     - Dashboard           - Blog
   - Checkout            - Strumenti           - Portfolio
   - Catalogo            - Admin               - Landing
        │                     │                     │
        ▼                     ▼                     ▼
   PRINCIPI:             PRINCIPI:             PRINCIPI:
   - Fiducia             - Funzionalità        - Storytelling
   - Azione              - Chiarezza           - Emozione
   - Urgenza             - Efficienza          - Creatività
```

---

## 2. Albero decisionale per pubblico

### Chi è il tuo pubblico di riferimento?

```text
PUBBLICO DI RIFERIMENTO
      │
      ├── Gen Z (nati 1997-2012)
      │   ├── Colori: decisi, vivaci, combinazioni inattese
      │   ├── Tipografia: grande, espressiva, variabile
      │   ├── Layout: mobile-first, verticale, a piccole dosi
      │   ├── Effetti: movimento, gamification, interattività
      │   └── Approccio: autentico, veloce, niente aria da azienda
      │
      ├── Millennial (nati 1981-1996)
      │   ├── Colori: tenui, terrosi, sofisticati
      │   ├── Tipografia: pulita, leggibile, funzionale
      │   ├── Layout: responsive, a card, ordinato
      │   ├── Effetti: sottili, solo se hanno uno scopo
      │   └── Approccio: orientato ai valori, trasparente, sostenibile
      │
      ├── Gen X (nati 1965-1980)
      │   ├── Colori: professionali, rassicuranti, conservativi
      │   ├── Tipografia: familiare, chiara, senza fronzoli
      │   ├── Layout: gerarchia tradizionale, prevedibile
      │   ├── Effetti: minimi, feedback funzionale
      │   └── Approccio: diretto, efficiente, affidabile
      │
      ├── Boomer (nati 1946-1964)
      │   ├── Colori: alto contrasto, semplici, chiari
      │   ├── Tipografia: dimensioni grandi, alta leggibilità
      │   ├── Layout: semplice, lineare, senza confusione
      │   ├── Effetti: nessuno o minimi
      │   └── Approccio: chiaro, dettagliato, affidabile
      │
      └── B2B / Enterprise
          ├── Colori: palette professionale, tenue
          ├── Tipografia: pulita, adatta ai dati, facile da scorrere
          ├── Layout: basato su griglia, ordinato, efficiente
          ├── Effetti: professionali, sottili
          └── Approccio: esperto, orientato alle soluzioni e al ROI
```

---

## 3. Albero decisionale per il colore

### Invece di codici hex fissi, segui questo processo

```text
QUALE EMOZIONE/AZIONE VUOI OTTENERE?
            │
            ├── Fiducia e sicurezza
            │   └── Considera: famiglia dei blu, neutri professionali
            │       → CHIEDI all'utente la sfumatura che preferisce
            │
            ├── Crescita e salute
            │   └── Considera: famiglia dei verdi, toni naturali
            │       → CHIEDI se il focus è eco/natura/benessere
            │
            ├── Urgenza e azione
            │   └── Considera: colori caldi (arancio/rosso) come ACCENTI
            │       → Usali con parsimonia, CHIEDI se sono adatti
            │
            ├── Lusso e premium
            │   └── Considera: scuri profondi, metallici, palette sobria
            │       → CHIEDI del posizionamento del brand
            │
            ├── Creativo e giocoso
            │   └── Considera: più colori, combinazioni inattese
            │       → CHIEDI della personalità del brand
            │
            └── Calmo e minimal
                └── Considera: neutri con un solo accento
                    → CHIEDI quale colore d'accento si adatta al brand
```

### Il processo

1. Individua l'emozione che serve
2. Restringi a una FAMIGLIA di colori
3. CHIEDI all'utente la preferenza all'interno della famiglia
4. Genera una palette nuova con i principi HSL

---

## 4. Albero decisionale per la tipografia

```text
CHE TIPO DI CONTENUTO È?
          │
          ├── Ricco di dati (dashboard, SaaS)
          │   ├── Stile: sans-serif, chiaro, compatto
          │   ├── Scala: rapporto più stretto (1.125-1.2)
          │   └── Priorità: facilità di scansione, densità
          │
          ├── Editoriale (blog, rivista)
          │   ├── Stile: titoli serif + testo sans funziona bene
          │   ├── Scala: più drammatica (1.333+)
          │   └── Priorità: comfort di lettura, gerarchia
          │
          ├── Tech moderno (startup, marketing SaaS)
          │   ├── Stile: sans geometrico o umanista
          │   ├── Scala: bilanciata (1.25)
          │   └── Priorità: aspetto moderno, chiarezza
          │
          ├── Lusso (moda, premium)
          │   ├── Stile: serif elegante o sans sottile
          │   ├── Scala: drammatica (1.5-1.618)
          │   └── Priorità: raffinatezza, spazio bianco
          │
          └── Giocoso (bambini, giochi, casual)
              ├── Stile: font arrotondati, amichevoli
              ├── Scala: varia, espressiva
              └── Priorità: divertente, alla mano, leggibile
```

### Processo di scelta

1. Individua il tipo di contenuto
2. Scegli la DIREZIONE stilistica
3. CHIEDI all'utente se ha font del brand
4. Scegli font coerenti con la direzione

---

## 5. Linee guida per l'e-commerce {#e-commerce}

### Principi chiave (non regole fisse)

- **Prima la fiducia:** come mostrerai la sicurezza?
- **Orientato all'azione:** dove sono le CTA?
- **Facile da scorrere:** gli utenti possono confrontare in fretta?

### Ragionare sul colore

```text
Di solito l'e-commerce ha bisogno di:
├── Colore della fiducia (spesso famiglia dei blu) → CHIEDI la preferenza
├── Sfondo pulito (bianco/neutro) → dipende dal brand
├── Accento per l'azione (CTA, saldi) → dipende dal livello di urgenza
├── Semantica successo/errore → le convenzioni standard funzionano
└── Integrazione col brand → CHIEDI dei colori esistenti
```

### Principi di layout

```text
┌────────────────────────────────────────────────────┐
│  HEADER: brand + ricerca + carrello                │
│  (Tieni visibili le azioni essenziali)             │
├────────────────────────────────────────────────────┤
│  ZONA FIDUCIA: perché fidarsi di questo sito?      │
│  (Spedizioni, resi, sicurezza, se pertinenti)      │
├────────────────────────────────────────────────────┤
│  HERO: messaggio o offerta principale              │
│  (CTA chiara, un solo focus)                       │
├────────────────────────────────────────────────────┤
│  CATEGORIE: navigazione facile                     │
│  (Visive, filtrabili, facili da scorrere)          │
├────────────────────────────────────────────────────┤
│  PRODOTTI: confronto facile                        │
│  (Prezzo, valutazione, azioni rapide in vista)     │
├────────────────────────────────────────────────────┤
│  RIPROVA SOCIALE: perché gli altri si fidano       │
│  (Recensioni, testimonianze, se disponibili)       │
├────────────────────────────────────────────────────┤
│  FOOTER: tutti i dettagli                          │
│  (Policy, contatti, badge di fiducia)              │
└────────────────────────────────────────────────────┘
```

### Psicologia da applicare

- Legge di Hick: limita le scelte di navigazione
- Legge di Fitts: dimensiona bene le CTA
- Riprova sociale: mostrala dove serve
- Scarsità: usala con onestà, se proprio la usi

---

## 6. Linee guida per le dashboard SaaS {#saas}

### Principi chiave

- **Prima la funzione:** chiarezza dei dati prima della decorazione
- **UI calma:** riduci il carico cognitivo
- **Coerente:** pattern prevedibili

### Ragionare sul colore

```text
Di solito una dashboard ha bisogno di:
├── Sfondo: chiaro O scuro (CHIEDI la preferenza)
├── Superficie: leggero contrasto rispetto allo sfondo
├── Accento primario: per le azioni chiave
├── Colori dei dati: semantica successo/avviso/pericolo
└── Tenue: per le informazioni secondarie
```

### Principi di layout

```text
Valuta questi pattern (non sono obbligatori):

OPZIONE A: sidebar + contenuto
├── Sidebar fissa per la navigazione
└── Area principale per il contenuto

OPZIONE B: navigazione in alto + contenuto
├── Navigazione orizzontale
└── Più spazio orizzontale per il contenuto

OPZIONE C: compressa + espandibile
├── Sidebar solo icone che si espande
└── Massima area per il contenuto

→ CHIEDI all'utente come preferisce la navigazione
```

### Psicologia da applicare

- Legge di Hick: raggruppa le voci di navigazione
- Legge di Miller: dividi le informazioni in blocchi
- Carico cognitivo: spazio bianco, coerenza

---

## 7. Linee guida per le landing page {#landing-page}

### Principi chiave

- **Centrata sull'hero:** la prima impressione conta più di tutto
- **Un solo focus:** una CTA principale
- **Emotiva:** crea un legame prima di vendere

### Ragionare sul colore

```text
Di solito una landing page ha bisogno di:
├── Primario del brand: sfondo dell'hero o accento
├── Secondario pulito: gran parte della pagina
├── Colore della CTA: spicca su tutto il resto
├── Di supporto: per sezioni e testimonianze
└── CHIEDI prima dei colori del brand!
```

### Principi di struttura

```text
┌────────────────────────────────────────────────────┐
│  Navigazione: minima, CTA visibile                 │
├────────────────────────────────────────────────────┤
│  HERO: gancio + valore + CTA                       │
│  (La sezione più importante, massimo impatto)      │
├────────────────────────────────────────────────────┤
│  PROBLEMA: che difficoltà hanno?                   │
├────────────────────────────────────────────────────┤
│  SOLUZIONE: come la risolvi                        │
├────────────────────────────────────────────────────┤
│  PROVE: perché crederti?                           │
│  (Testimonianze, loghi, numeri)                    │
├────────────────────────────────────────────────────┤
│  COME: spiegazione semplice del processo           │
├────────────────────────────────────────────────────┤
│  PREZZI: se applicabile                            │
├────────────────────────────────────────────────────┤
│  FAQ: rispondi alle obiezioni                      │
├────────────────────────────────────────────────────┤
│  CTA FINALE: ripeti l'azione principale            │
└────────────────────────────────────────────────────┘
```

### Psicologia da applicare

- Viscerale: un hero che colpisce per la bellezza
- Posizione seriale: informazioni chiave in alto e in fondo
- Riprova sociale: le testimonianze funzionano

---

## 8. Linee guida per i portfolio {#portfolio}

### Principi chiave

- **Personalità:** mostra chi sei
- **Centrato sui lavori:** lascia parlare i progetti
- **Memorabile:** distinguiti dai template

### Ragionare sul colore

```text
Il portfolio è personale, le opzioni sono tante:
├── Minimal: neutri + un accento distintivo
├── Deciso: scelte di colore inattese
├── Scuro: atmosfera intensa, artistica
├── Chiaro: aspetto pulito, professionale
└── CHIEDI del personal brand!
```

### Principi di struttura

```text
┌────────────────────────────────────────────────────┐
│  Navigazione: in linea con la tua personalità      │
├────────────────────────────────────────────────────┤
│  INTRO: chi sei, cosa fai                          │
│  (Rendila memorabile, non generica)                │
├────────────────────────────────────────────────────┤
│  LAVORI: progetti in evidenza                      │
│  (Grandi, visivi, interattivi)                     │
├────────────────────────────────────────────────────┤
│  CHI SONO: storia personale                        │
│  (Crea un legame)                                  │
├────────────────────────────────────────────────────┤
│  CONTATTI: facile da raggiungere                   │
│  (Chiaro, diretto)                                 │
└────────────────────────────────────────────────────┘
```

### Psicologia da applicare

- Von Restorff: sii memorabile in modo unico
- Riflessivo: la storia personale crea un legame
- Emotivo: la personalità conta più della professionalità

---

## 9. Checklist prima del design

### Prima di iniziare QUALSIASI design

- [ ] **Pubblico definito?** (chi, esattamente)
- [ ] **Obiettivo principale individuato?** (quale azione)
- [ ] **Vincoli noti?** (tempi, brand, tecnologia)
- [ ] **Contenuti disponibili?** (o servono segnaposto)
- [ ] **Preferenze chieste all'utente?** (colori, stile, layout)

### Prima di scegliere i colori

- [ ] **Hai chiesto la preferenza all'utente?**
- [ ] **Hai considerato il contesto?** (settore, emozione)
- [ ] **È diverso dal tuo default?**
- [ ] **Hai verificato l'accessibilità?**

### Prima di definire il layout

- [ ] **Gerarchia chiara?**
- [ ] **CTA principale evidente?**
- [ ] **Mobile considerato?**
- [ ] **I contenuti stanno nella struttura?**

### Prima della consegna

- [ ] **Sembra premium, non generico?**
- [ ] **Ne andresti fiero?**
- [ ] **È diverso dall'ultimo progetto?**

---

## 10. Stima della complessità

### Progetti rapidi (ore)

```text
Landing page semplice
Portfolio piccolo
Form di base
Singolo componente
```

→ Approccio: poche decisioni, esecuzione mirata

### Progetti medi (giorni)

```text
Sito multipagina
Dashboard con moduli
Categoria di e-commerce
Form complessi
```

→ Approccio: definisci i token, componenti personalizzati

### Progetti grandi (settimane)

```text
Applicazione SaaS completa
Piattaforma e-commerce
Design system personalizzato
Workflow complessi
```

→ Approccio: design system completo, documentazione, test

---

> **Ricorda**: questi template mostrano la STRUTTURA e il processo di RAGIONAMENTO. Ogni progetto richiede scelte nuove di colori, tipografia e stile, basate sul suo contesto. CHIEDI quando qualcosa non è chiaro.
