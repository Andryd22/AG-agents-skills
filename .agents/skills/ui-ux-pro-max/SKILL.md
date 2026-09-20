---
name: ui-ux-pro-max
description: Progetta e realizza UI con un database di design consultabile - 58 stili, 96 palette di colori, 57 abbinamenti di font, linee guida UX e generazione del design system. Usala quando l'utente lancia /ui-ux-pro-max o chiede di progettare, costruire o revisionare una UI.
---

# ui-ux-pro-max

Guida completa al design di applicazioni web e mobile: 58 stili, 96 palette di colori, 57 abbinamenti di font, 99 linee guida UX e 25 tipi di grafico, per 12 stack tecnologici. Il database è consultabile e dà raccomandazioni ordinate per priorità.

> **Il database è in inglese.** I CSV in `data/` e `data/stacks/` restano in inglese: il motore BM25 confronta le parole della query con quelle dei CSV, quindi scrivi le query con parole chiave **in inglese** (per esempio `"saas dashboard minimal"`, non `"dashboard saas minimale"`). Anche i valori dei risultati (nomi di stili, palette, note) arrivano in inglese: usali come materiale di lavoro e scrivi la risposta all'utente in italiano.

## Prerequisiti

Controlla che Python sia installato:

```bash
python3 --version || python --version
```

Se manca, installalo in base al sistema operativo dell'utente:

**macOS:**

```bash
brew install python3
```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install python3
```

**Windows:**

```powershell
winget install Python.Python.3.12
```

---

## Come usare questa skill

Quando l'utente chiede un lavoro di UI/UX (progettare, costruire, creare, implementare, revisionare, correggere, migliorare), segui questi passi.

### Passo 1: analizza i requisiti

Ricava dalla richiesta le informazioni chiave e trasformale in parole chiave inglesi per la ricerca:

- **Tipo di prodotto**: SaaS, e-commerce, portfolio, dashboard, landing page, ecc.
- **Parole chiave di stile**: minimal, playful, professional, elegant, dark mode, ecc.
- **Settore**: healthcare, fintech, gaming, education, ecc.
- **Stack**: React, Vue, Next.js; se non è indicato, usa `html-tailwind`

### Passo 2: genera il design system (OBBLIGATORIO)

**Parti sempre da `--design-system`** per avere raccomandazioni complete, con le motivazioni:

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Nome progetto"]
```

Il comando:

1. Cerca in 5 domini in parallelo (product, style, color, landing, typography)
2. Applica le regole di ragionamento di `ui-reasoning.csv` per scegliere i risultati migliori
3. Restituisce un design system completo: pattern, stile, colori, tipografia, effetti
4. Elenca gli anti-pattern da evitare

**Esempio:**

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

Output (abbreviato):

```text
+-----------------------------------------------------------------------------------------+
|  PROGETTO: Serenity Spa - DESIGN SYSTEM CONSIGLIATO                                     |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  PATTERN: Hero-Centric + Social Proof                                                   |
|     CTA: Above fold                                                                     |
|     Sezioni:                                                                            |
|       1. Hero                                                                           |
|       2. Features                                                                       |
|       3. CTA                                                                            |
|                                                                                         |
|  STILE: Soft UI Evolution                                                               |
|     Parole chiave: Evolved soft UI, better contrast, modern aesthetics, subtle depth,   |
|     accessibility-focused, improved shadows, hybrid                                     |
|                                                                                         |
|  COLORI:                                                                                |
|     Primario:   #10B981                                                                 |
|     Secondario: #34D399                                                                 |
|     CTA:        #8B5CF6                                                                 |
|     Sfondo:     #ECFDF5                                                                 |
|     Testo:      #064E3B                                                                 |
|                                                                                         |
|  TIPOGRAFIA: Lora / Raleway                                                             |
|     Mood: calm, wellness, health, relaxing, natural, organic                            |
|                                                                                         |
|  EFFETTI CHIAVE:                                                                        |
|     Improved shadows (softer than flat, clearer than neumorphism), modern (200-300ms),  |
|     focus visible, WCAG AA/AAA                                                          |
|                                                                                         |
|  DA EVITARE (anti-pattern):                                                             |
|     Bright neon colors + Harsh animations + Dark mode                                   |
|                                                                                         |
|  CHECKLIST PRIMA DELLA CONSEGNA:                                                        |
|     [ ] Niente emoji come icone (usa SVG: Heroicons/Lucide)                             |
|     [ ] cursor-pointer su tutti gli elementi cliccabili                                 |
|     ...                                                                                 |
+-----------------------------------------------------------------------------------------+
```

Le etichette sono in italiano, i valori arrivano dal database in inglese.

### Passo 2b: salva il design system (pattern Master + Overrides)

Per salvare il design system e ritrovarlo in modo gerarchico tra una sessione e l'altra, aggiungi `--persist`:

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Nome progetto"
```

Il comando crea (`<progetto>` è il nome del progetto in minuscolo, con i trattini al posto degli spazi):

- `design-system/<progetto>/MASTER.md`: la fonte di verità globale, con tutte le regole di design
- `design-system/<progetto>/pages/`: la cartella per gli override delle singole pagine

**Con l'override di una pagina:**

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Nome progetto" --page "dashboard"
```

Crea anche:

- `design-system/<progetto>/pages/dashboard.md`: le differenze della pagina rispetto al Master

I file vanno nella cartella corrente; con `-o <cartella>` li salvi altrove.

**Come funziona il recupero gerarchico:**

1. Quando costruisci una pagina specifica (per esempio "Checkout"), controlla prima `design-system/<progetto>/pages/checkout.md`
2. Se il file della pagina esiste, le sue regole **sostituiscono** quelle del Master
3. Altrimenti usa solo `design-system/<progetto>/MASTER.md`

### Passo 3: approfondisci con ricerche mirate (se serve)

Dopo aver ottenuto il design system, usa le ricerche per dominio per aggiungere dettagli:

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**Quando usare le ricerche mirate:**

| Ti serve | Dominio | Esempio |
| --- | --- | --- |
| Altre opzioni di stile | `style` | `--domain style "glassmorphism dark"` |
| Grafici consigliati | `chart` | `--domain chart "real-time dashboard"` |
| Buone pratiche UX | `ux` | `--domain ux "animation accessibility"` |
| Font alternativi | `typography` | `--domain typography "elegant luxury"` |
| Struttura della landing page | `landing` | `--domain landing "hero social-proof"` |

### Passo 4: linee guida dello stack (predefinito: html-tailwind)

Cerca le buone pratiche specifiche dell'implementazione. Se l'utente non indica uno stack, **usa `html-tailwind`**.

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Stack disponibili: `html-tailwind`, `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Riferimento per la ricerca

### Domini disponibili

| Dominio | A cosa serve | Parole chiave di esempio |
| --- | --- | --- |
| `product` | Raccomandazioni per tipo di prodotto | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | Stili UI, colori, effetti | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Abbinamenti di font, Google Fonts | elegant, playful, professional, modern |
| `color` | Palette di colori per tipo di prodotto | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Struttura della pagina, strategie per le CTA | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Tipi di grafico, librerie consigliate | trend, comparison, timeline, funnel, pie |
| `ux` | Buone pratiche, anti-pattern | animation, accessibility, z-index, loading |
| `icons` | Icone per funzione, con libreria e codice di import | navigation, menu, search, settings, user, arrow |
| `react` | Prestazioni di React/Next.js | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Linee guida per le interfacce web | aria, focus, keyboard, semantic, virtualize |
| `prompt` | Prompt per l'AI, parole chiave CSS | (nome dello stile) |

Se ometti `--domain`, lo script deduce il dominio dalle parole chiave inglesi della query; se non ne riconosce nessuna, usa `style`.

### Stack disponibili

| Stack | Punti chiave |
| --- | --- |
| `html-tailwind` | Utility di Tailwind, responsive, a11y (PREDEFINITO) |
| `react` | State, hook, prestazioni, pattern |
| `nextjs` | SSR, routing, immagini, API route |
| `vue` | Composition API, Pinia, Vue Router |
| `nuxtjs` | Pagine Nuxt, data fetching, SSR |
| `nuxt-ui` | Componenti Nuxt UI e theming |
| `svelte` | Rune, store, SvelteKit |
| `swiftui` | View, State, Navigation, Animation |
| `react-native` | Componenti, Navigation, liste |
| `flutter` | Widget, State, Layout, Theming |
| `shadcn` | Componenti shadcn/ui, theming, form, pattern |
| `jetpack-compose` | Composable, Modifier, State Hoisting, Recomposition |

---

## Esempio di flusso di lavoro

**Richiesta dell'utente:** "Fammi una landing page per un centro estetico professionale"

### Passo 1: analizza i requisiti

- Tipo di prodotto: servizio beauty/spa
- Parole chiave di stile: elegant, professional, soft
- Settore: beauty/wellness
- Stack: html-tailwind (predefinito)

La richiesta è in italiano, ma le parole chiave per la ricerca sono in inglese.

### Passo 2: genera il design system (OBBLIGATORIO)

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Output:** design system completo con pattern, stile, colori, tipografia, effetti e anti-pattern.

### Passo 3: approfondisci con ricerche mirate (se serve)

```bash
# Linee guida UX per animazioni e accessibilità
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Alternative per la tipografia, se servono
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Passo 4: linee guida dello stack

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Poi:** unisci il design system e le ricerche mirate, implementa il design e spiega all'utente le scelte in italiano.

---

## Formati di output

Il flag `--design-system` supporta due formati di output:

```bash
# Riquadro ASCII (predefinito): ideale nel terminale
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown: ideale per la documentazione
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

Il riquadro ASCII ha le sezioni `PATTERN`, `STILE`, `COLORI`, `TIPOGRAFIA`, `EFFETTI CHIAVE`, `DA EVITARE (anti-pattern)` e `CHECKLIST PRIMA DELLA CONSEGNA`; il Markdown ha le stesse sezioni come titoli `###` (Pattern, Stile, Colori, Tipografia, Effetti chiave, Da evitare, Checklist prima della consegna).

---

## Consigli per risultati migliori

1. **Usa parole chiave inglesi e specifiche**: "healthcare SaaS dashboard" è meglio di "app"
2. **Cerca più volte**: parole chiave diverse fanno emergere spunti diversi
3. **Combina i domini**: stile + tipografia + colori = design system completo
4. **Controlla sempre la UX**: cerca "animation", "z-index", "accessibility" per i problemi più comuni
5. **Usa il flag `--stack`**: ottieni buone pratiche specifiche dell'implementazione
6. **Itera**: se la prima ricerca non centra il punto, prova altre parole chiave

---

## Regole comuni per una UI professionale

Questi problemi vengono trascurati spesso e fanno sembrare una UI poco professionale.

### Icone ed elementi visivi

| Regola | Fai | Non fare |
| --- | --- | --- |
| **Niente emoji come icone** | Usa icone SVG (Heroicons, Lucide, Simple Icons) | Usare emoji come 🎨 🚀 ⚙️ come icone della UI |
| **Stati hover stabili** | Usa transizioni di colore o opacità all'hover | Usare trasformazioni di scala che spostano il layout |
| **Loghi dei brand corretti** | Prendi l'SVG ufficiale da Simple Icons | Tirare a indovinare o usare path del logo sbagliati |
| **Icone di dimensione coerente** | Usa un viewBox fisso (24x24) con w-6 h-6 | Mescolare a caso icone di dimensioni diverse |

### Interazione e cursore

| Regola | Fai | Non fare |
| --- | --- | --- |
| **Cursore pointer** | Aggiungi `cursor-pointer` a tutte le card cliccabili o con hover | Lasciare il cursore predefinito sugli elementi interattivi |
| **Feedback all'hover** | Dai un feedback visivo (colore, ombra, bordo) | Nessun segnale che l'elemento è interattivo |
| **Transizioni morbide** | Usa `transition-colors duration-200` | Cambi di stato istantanei o troppo lenti (>500ms) |

### Contrasto in light e dark mode

| Regola | Fai | Non fare |
| --- | --- | --- |
| **Glass card in light mode** | Usa `bg-white/80` o un'opacità maggiore | Usare `bg-white/10` (troppo trasparente) |
| **Contrasto del testo in light mode** | Usa `#0F172A` (slate-900) per il testo | Usare `#94A3B8` (slate-400) per il corpo del testo |
| **Testo attenuato in light mode** | Usa almeno `#475569` (slate-600) | Usare gray-400 o più chiaro |
| **Bordi visibili** | Usa `border-gray-200` in light mode | Usare `border-white/10` (invisibile) |

### Layout e spaziature

| Regola | Fai | Non fare |
| --- | --- | --- |
| **Navbar flottante** | Lascia una distanza con `top-4 left-4 right-4` | Attaccare la navbar a `top-0 left-0 right-0` |
| **Padding del contenuto** | Tieni conto dell'altezza della navbar fissa | Lasciare che il contenuto finisca sotto gli elementi fissi |
| **max-width coerente** | Usa sempre lo stesso `max-w-6xl` o `max-w-7xl` | Mescolare larghezze diverse dei contenitori |

---

## Checklist prima della consegna

Prima di consegnare codice UI, verifica questi punti.

### Qualità visiva

- [ ] Nessuna emoji usata come icona (usa SVG)
- [ ] Tutte le icone da un unico set coerente (Heroicons/Lucide)
- [ ] Loghi dei brand corretti (verificati su Simple Icons)
- [ ] Gli stati hover non spostano il layout
- [ ] Colori del tema usati direttamente (bg-primary), senza wrapper var()

### Interazione

- [ ] Tutti gli elementi cliccabili hanno `cursor-pointer`
- [ ] Gli stati hover danno un feedback visivo chiaro
- [ ] Transizioni morbide (150-300ms)
- [ ] Stati di focus visibili per la navigazione da tastiera

### Light e dark mode

- [ ] Il testo in light mode ha un contrasto sufficiente (almeno 4.5:1)
- [ ] Gli elementi glass o trasparenti si vedono in light mode
- [ ] I bordi si vedono in entrambe le modalità
- [ ] Hai provato entrambe le modalità prima della consegna

### Layout

- [ ] Gli elementi flottanti hanno la giusta distanza dai bordi
- [ ] Nessun contenuto nascosto dietro navbar fisse
- [ ] Responsive a 375px, 768px, 1024px, 1440px
- [ ] Nessuno scroll orizzontale su mobile

### Accessibilità

- [ ] Tutte le immagini hanno il testo alternativo (alt)
- [ ] I campi dei form hanno una label
- [ ] Il colore non è l'unico indicatore
- [ ] `prefers-reduced-motion` rispettato
