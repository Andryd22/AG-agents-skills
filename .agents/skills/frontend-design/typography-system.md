# Riferimento sistema tipografico

> Principi tipografici e come prendere decisioni: impara a ragionare, non a memorizzare.
> **Nessun nome di font o dimensione fissa: capisci il sistema.**

---

## 1. Principi della scala modulare

### Cos'è una scala modulare?

```text
Una relazione matematica tra le dimensioni dei font:
├── Scegli una dimensione BASE (di solito il testo del corpo)
├── Scegli un RAPPORTO (ratio, il moltiplicatore)
└── Genera tutte le dimensioni con: base × ratio^n
```

### Rapporti comuni e quando usarli

| Rapporto | Valore | Sensazione | Ideale per |
| --- | --- | --- | --- |
| Seconda minore (Minor Second) | 1.067 | Molto discreta | UI dense, schermi piccoli |
| Seconda maggiore (Major Second) | 1.125 | Discreta | Interfacce compatte |
| Terza minore (Minor Third) | 1.2 | Comoda | App mobile, card |
| Terza maggiore (Major Third) | 1.25 | Equilibrata | Web generico (la più comune) |
| Quarta giusta (Perfect Fourth) | 1.333 | Evidente | Editoriale, blog |
| Quinta giusta (Perfect Fifth) | 1.5 | Drammatica | Titoli, marketing |
| Sezione aurea (Golden Ratio) | 1.618 | Impatto massimo | Sezioni hero, display |

### Genera la tua scala

```text
Dati: base = YOUR_BASE_SIZE, ratio = YOUR_RATIO

Scala:
├── xs:  base ÷ ratio²
├── sm:  base ÷ ratio
├── base: YOUR_BASE_SIZE
├── lg:  base × ratio
├── xl:  base × ratio²
├── 2xl: base × ratio³
├── 3xl: base × ratio⁴
└── ... continua quanto serve
```

### Scegliere la dimensione base

| Contesto | Dimensione base | Perché |
| --- | --- | --- |
| Mobile-first | 16-18px | Leggibilità su schermi piccoli |
| App desktop | 14-16px | Densità di informazioni |
| Editoriale | 18-21px | Comfort nelle letture lunghe |
| Priorità all'accessibilità | 18px+ | Più facile da leggere |

---

## 2. Principi di font pairing

### Cosa fa funzionare bene due font insieme

```text
Contrasto + armonia:
├── Abbastanza DIVERSI da creare gerarchia
├── Abbastanza SIMILI da risultare coerenti
└── Di solito: serif + sans, oppure display + neutro
```

### Strategie di abbinamento

| Strategia | Come | Risultato |
| --- | --- | --- |
| **Contrasto** | Titoli serif + corpo sans | Aspetto classico, editoriale |
| **Stessa famiglia** | Un solo variable font, pesi diversi | Coerente, moderno |
| **Stesso designer** | Font della stessa fonderia | Proporzioni spesso armoniose |
| **Stessa epoca** | Font dello stesso periodo storico | Coerenza storica |

### Cosa guardare

```text
Quando abbini due font, confronta:
├── x-height (altezza delle lettere minuscole)
├── Larghezza delle lettere (strette o larghe)
├── Contrasto del tratto (variazione tra sottile e spesso)
└── Mood generale (formale o informale)
```

### Abbinamenti sicuri

| Stile dei titoli | Stile del corpo | Mood |
| --- | --- | --- |
| Sans geometrico | Sans umanista | Moderno, amichevole |
| Serif display | Sans pulito | Editoriale, sofisticato |
| Sans neutro | Lo stesso sans | Minimal, tech |
| Geometrico bold | Geometrico light | Contemporaneo |

### Evita

- ❌ Due font decorativi insieme
- ❌ Font simili che stonano tra loro
- ❌ Più di 2-3 famiglie di font
- ❌ Font con x-height molto diverse

---

## 3. Principi del line-height

### La relazione

```text
Il line-height dipende da:
├── Dimensione del font (testo più grande = serve meno line-height)
├── Lunghezza della riga (righe più lunghe = più line-height)
├── Disegno del font (alcuni font chiedono più spazio)
└── Tipo di contenuto (titoli o corpo)
```

### Linee guida per contesto

| Tipo di contenuto | Line-height | Perché |
| --- | --- | --- |
| **Titoli** | 1.1 - 1.3 | Righe brevi, meglio compatte |
| **Testo del corpo** | 1.4 - 1.6 | Lettura comoda |
| **Testi lunghi** | 1.6 - 1.8 | Massima leggibilità |
| **Elementi UI** | 1.2 - 1.4 | Uso efficiente dello spazio |

### Fattori di aggiustamento

- **Righe più lunghe** → aumenta il line-height
- **Font più grande** → riduci il rapporto di line-height
- **Tutto maiuscolo** → può servire più line-height
- **Tracking stretto** → può servire più line-height

---

## 4. Principi della lunghezza di riga

### Larghezza di lettura ottimale

```text
Il punto ideale: 45-75 caratteri per riga
├── < 45: troppo spezzettata, interrompe il flusso
├── 45-75: lettura comoda
├── > 75: l'occhio fatica a seguire le righe
```

### Come misurarla

```css
/* Basata sui caratteri (consigliato) */
max-width: 65ch; /* ch = larghezza del carattere "0" */

/* Si adatta da sola alla dimensione del font */
```

### Aggiustamenti per contesto

| Contesto | Caratteri per riga |
| --- | --- |
| Articolo su desktop | 60-75 caratteri |
| Mobile | 35-50 caratteri |
| Testo in sidebar | 30-45 caratteri |
| Monitor larghi | Resta comunque intorno a ~75ch |

---

## 5. Principi di tipografia responsive

### Il problema

```text
Le dimensioni fisse non scalano bene:
├── La dimensione per desktop è troppo grande su mobile
├── La dimensione per mobile è troppo piccola su desktop
└── I salti ai breakpoint risultano bruschi
```

### Tipografia fluida (clamp)

```css
/* Sintassi: clamp(MIN, PREFERRED, MAX) */
font-size: clamp(
  MINIMUM_SIZE,
  FLUID_CALCULATION,
  MAXIMUM_SIZE
);

/* FLUID_CALCULATION di solito: 
   base + unità relativa al viewport */
```

### Strategia di scalatura

| Elemento | Come scala |
| --- | --- |
| Testo del corpo | Poco (1rem → 1.125rem) |
| Sottotitoli | Moderatamente |
| Titoli | In modo più marcato |
| Testo display | In modo molto marcato |

---

## 6. Principi di peso ed enfasi

### Uso semantico dei pesi

| Peso | Nome | Da usare per |
| --- | --- | --- |
| 300-400 | Light/Normal | Testo del corpo, paragrafi |
| 500 | Medium | Enfasi leggera |
| 600 | Semibold | Sottotitoli, etichette |
| 700 | Bold | Titoli, enfasi forte |
| 800-900 | Heavy/Black | Display, testo hero |

### Creare contrasto

```text
Buon contrasto = salta almeno 2 livelli di peso
├── corpo 400 + titolo 700 = buono
├── corpo 400 + enfasi 500 = appena percettibile
├── titolo 600 + sottotitolo 700 = troppo simili
```

### Evita

- ❌ Troppi pesi (massimo 3-4 per pagina)
- ❌ Pesi adiacenti per la gerarchia (400/500)
- ❌ Pesi molto forti per i testi lunghi

---

## 7. Spaziatura tra le lettere (tracking)

### Principi

```text
Testo grande (titoli): tracking più stretto
├── Le lettere sono grandi, gli spazi sembrano più ampi
└── Un tracking leggermente negativo rende meglio

Testo piccolo (corpo): normale o leggermente più largo
├── Migliora la leggibilità alle dimensioni piccole
└── Mai negativo per il testo del corpo

TUTTO MAIUSCOLO: tracking sempre più largo
├── Le maiuscole non hanno ascendenti/discendenti
└── Hanno bisogno di più spazio per risultare equilibrate
```

### Linee guida di aggiustamento

| Contesto | Aggiustamento del tracking |
| --- | --- |
| Display/Hero | da -2% a -4% |
| Titoli | da -1% a -2% |
| Testo del corpo | 0% (normale) |
| Testo piccolo | da +1% a +2% |
| TUTTO MAIUSCOLO | da +5% a +10% |

---

## 8. Principi di gerarchia

### Gerarchia visiva con la tipografia

```text
Modi per creare gerarchia:
├── DIMENSIONE (il più evidente)
├── PESO (il bold risalta)
├── COLORE (livelli di contrasto)
├── SPAZIATURA (i margini separano le sezioni)
└── POSIZIONE (in alto = importante)
```

### Gerarchia tipica

| Livello | Caratteristiche |
| --- | --- |
| Primario (H1) | Il più grande, il più marcato, il più distinto |
| Secondario (H2) | Visibilmente più piccolo ma ancora bold |
| Terziario (H3) | Dimensione media, può distinguersi solo per il peso |
| Corpo | Dimensione e peso standard |
| Didascalie/meta | Più piccolo, spesso di colore più chiaro |

### Verificare la gerarchia

Chiediti: "Capisco al primo sguardo cosa conta di più?"

Anche guardando la pagina con gli occhi socchiusi, la gerarchia deve restare chiara.

---

## 9. Psicologia della leggibilità

### Lettura a F (F-pattern)

```text
Gli utenti scorrono la pagina a F:
├── In orizzontale in alto (prima riga)
├── Giù lungo il lato sinistro
├── Di nuovo in orizzontale (sottotitolo)
└── Poi ancora giù a sinistra
```

**Conseguenza**: metti le informazioni chiave a sinistra e nei titoli

### Suddividere per capire meglio

- Paragrafi brevi (massimo 3-4 righe)
- Sottotitoli chiari
- Elenchi puntati per le liste
- Spazio bianco tra le sezioni

### Facilità cognitiva

- Font familiari = lettura più facile
- Contrasto alto = meno affaticamento
- Pattern coerenti = comportamento prevedibile

---

## 10. Checklist per scegliere la tipografia

Prima di chiudere la tipografia:

- [ ] **Hai chiesto all'utente le sue preferenze sui font?**
- [ ] **Hai considerato brand e contesto?**
- [ ] **Hai scelto un rapporto di scala adatto?**
- [ ] **Ti sei limitato a 2-3 famiglie di font?**
- [ ] **Hai verificato la leggibilità a tutte le dimensioni?**
- [ ] **Hai controllato la lunghezza di riga (45-75ch)?**
- [ ] **Hai verificato il contrasto per l'accessibilità?**
- [ ] **È diversa dal tuo ultimo progetto?**

### Anti-pattern

- ❌ Gli stessi font in ogni progetto
- ❌ Troppe famiglie di font
- ❌ Sacrificare la leggibilità allo stile
- ❌ Dimensioni fisse senza adattamento responsive
- ❌ Font decorativi per il testo del corpo

---

> **Ricorda**: la tipografia serve a comunicare con chiarezza. Scegli in base alle esigenze del contenuto e al pubblico, non ai tuoi gusti personali.
